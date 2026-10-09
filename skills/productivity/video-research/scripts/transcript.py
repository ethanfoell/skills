#!/usr/bin/env python3
"""Check a whisper.cpp transcript and build its timed reading copy.

Python 3 standard library only; `check` also needs ffmpeg and ffprobe on PATH.
Input is whisper.cpp JSON output (`-oj`); other engines' JSON is not read.
Re-transcribed clips are spliced in with `--clip PATH OFFSET_SECONDS`, applied
in the order given; each clip replaces everything before it inside its own span.

  python3 -I transcript.py check FULL.json --audio AUDIO [--clip C.json 660 ...]
  python3 -I transcript.py reading-copy FULL.json OUT.txt [--clip C.json 660 ...]

`check` exits 0 when nothing is flagged, 1 when something is (a loop or heavily
repeated line, a gap or blank span that is mostly sound, a window loud but
nearly wordless, an unreadable level, an empty transcript), and 2 when it could
not run (missing or mismatched audio, ffmpeg missing, unreadable JSON).
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

NOISE = re.compile(r"^\s*[\[\(][^\]\)]*[\]\)]\s*$")  # [BLANK_AUDIO], (music), ...
SILENCE_DB = -50  # silencedetect threshold: quieter than this counts as silence
AUDIO_SLACK_S = 5  # whisper's last segment may end a little past the audio
SEAM_MAX_MS = 30_000  # longest seam-crossing segment kept whole when splicing a clip

Segment = collections.namedtuple("Segment", "start_ms end_ms text")
Hole = collections.namedtuple("Hole", "start_ms end_ms kind")


class Unusable(Exception):
    """Input or tooling problem: the check could not run."""


def hms(ms):
    # Same helper as flatten_chat.py: the scripts run with `python3 -I`, which
    # keeps a script's own folder off sys.path, so neither can import the other.
    s = max(0, int(ms) // 1000)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def load(path, offset_ms=0):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        return [
            Segment(s["offsets"]["from"] + offset_ms, s["offsets"]["to"] + offset_ms, s["text"].strip())
            for s in data["transcription"]
        ]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise Unusable(f"{path}: not readable as whisper.cpp -oj JSON ({type(e).__name__}: {e})")


def spliced(full_path, clips):
    segs = load(full_path)
    notes = []
    for path, offset_s in clips:
        clip = load(path, round(float(offset_s) * 1000))
        if not clip:
            notes.append(f"clip {path}: no segments, skipped")
            continue
        lo, hi = clip[0].start_ms, clip[-1].end_ms
        # A short speech segment crossing a seam stays whole, and the clip gives
        # way to it; otherwise the words on either side of the seam are lost.
        keep = [s for s in segs if s.end_ms <= lo or s.start_ms >= hi]
        for s in segs:
            crosses = (s.start_ms < lo < s.end_ms) or (s.start_ms < hi < s.end_ms)
            if crosses and is_speech(s.text) and s.end_ms - s.start_ms <= SEAM_MAX_MS:
                keep.append(s)
                clip = [c for c in clip if c.end_ms <= s.start_ms or c.start_ms >= s.end_ms]
        segs = keep + clip
        notes.append(f"clip {path} (offset {offset_s} s) spliced over {hms(lo)}-{hms(hi)}")
    segs.sort()
    return segs, notes


def is_speech(text):
    return bool(text) and not NOISE.match(text)


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        raise Unusable(f"{cmd[0]} not found on PATH")


def duration_s(audio):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).stdout.strip()
    try:
        return float(out)
    except ValueError:
        raise Unusable(f"{audio}: ffprobe reports no duration")


def audio_filter(audio, start_s, dur_s, af):
    """Run one ffmpeg audio filter over a window and return its log."""
    return run(["ffmpeg", "-nostdin", "-hide_banner", "-ss", f"{start_s:.3f}", "-t", f"{dur_s:.3f}",
                "-i", audio, "-vn", "-af", af, "-f", "null", "-"]).stderr


def mean_volume(audio, start_s, dur_s):
    """Mean volume in dB over the window, or None if unreadable."""
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", audio_filter(audio, start_s, dur_s, "volumedetect"))
    if not m:
        return None
    return -120.0 if m.group(1) == "-inf" else float(m.group(1))


def silent_share(audio, start_s, dur_s):
    """Share of the window that ffmpeg silencedetect calls silent."""
    log = audio_filter(audio, start_s, dur_s, f"silencedetect=noise={SILENCE_DB}dB:d=0.5")
    silent = sum(float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", log))
    starts = re.findall(r"silence_start:\s*(-?[\d.]+)", log)
    if len(starts) > len(re.findall(r"silence_end:", log)):  # silence running to the window's end
        silent += max(0.0, dur_s - float(starts[-1]))
    return min(1.0, silent / dur_s) if dur_s > 0 else 1.0


def level_text(db):
    return "LEVEL UNREADABLE" if db is None else f"{db:6.1f} dB"


def report_loops(segs):
    """Print loops and heavy repeats; return flag strings."""
    flags, looped = [], set()
    print("\nloops and repeated lines:")
    i = 0
    while i < len(segs):
        j = i
        while j + 1 < len(segs) and segs[j + 1].text == segs[i].text:
            j += 1
        run_len, text = j - i + 1, segs[i].text
        if is_speech(text) and ((run_len >= 3 and len(text) > 15) or run_len >= 10):
            print(f"  LOOP x{run_len} {hms(segs[i].start_ms)}-{hms(segs[j].end_ms)}: {text[:70]}")
            flags.append(f"loop at {hms(segs[i].start_ms)}")
            looped.add(text)
        i = j + 1
    counts = collections.Counter(s.text for s in segs if is_speech(s.text) and len(s.text) > 15 and s.text not in looped)
    for text, n in counts.most_common():
        if n < 5:
            break
        first = next(s.start_ms for s in segs if s.text == text)
        print(f"  REPEATED x{n}, not consecutive, first at {hms(first)}: {text[:70]}")
        flags.append(f"repeated line from {hms(first)}")
    if not flags:
        print("  none")
    return flags


def holes_in(segs, total_ms, min_ms):
    """Gaps between segments, the lead-in and tail, and runs of non-speech markers."""
    found = []
    if segs:
        found.append(Hole(0, segs[0].start_ms, "lead-in"))
        found.append(Hole(segs[-1].end_ms, total_ms, "tail"))
    found += [Hole(a.end_ms, b.start_ms, "gap") for a, b in zip(segs, segs[1:])]
    span = None
    for s in segs + [Segment(total_ms, total_ms, "end")]:
        if is_speech(s.text):
            if span:
                found.append(Hole(span[0], span[1], "non-speech"))
            span = None
        elif span and s.start_ms - span[1] <= 2000:
            span[1] = max(span[1], s.end_ms)
        else:
            if span:
                found.append(Hole(span[0], span[1], "non-speech"))
            span = [s.start_ms, s.end_ms]
    return sorted(h for h in found if h.end_ms - h.start_ms >= min_ms)


def report_holes(args, segs, total_s):
    """Measure every hole; flag the ones that are mostly sound at speech level."""
    flags = []
    holes = holes_in(segs, round(total_s * 1000), args.gap * 1000)
    print(f"\ngaps and blank spans of {args.gap} s or more (level, silent share):")
    for h in holes:
        start_s, dur_s = h.start_ms / 1000, (h.end_ms - h.start_ms) / 1000
        db = mean_volume(args.audio, start_s, dur_s)
        share = silent_share(args.audio, start_s, dur_s)
        if db is None:
            status = "unreadable"
            flags.append(f"unreadable level {hms(h.start_ms)}")
        elif db > args.speech_db and share < 0.5:
            status = "SUSPECT: mostly sound at speech level"
            flags.append(f"loud {h.kind} {hms(h.start_ms)}")
        else:
            status = "quiet"
        print(f"  {h.kind:10} {hms(h.start_ms)}-{hms(h.end_ms)} ({dur_s:.0f} s)  {level_text(db)}  {share:4.0%} silent  {status}")
    if not holes:
        print("  none")
    return flags


def report_windows(args, segs, total_s):
    """Words per window against the window's measured level."""
    flags = []
    window_s = args.window
    print(f"\ncoverage by {window_s // 60}-minute window (words vs measured mean level):")
    words = collections.Counter()
    for s in segs:
        if is_speech(s.text):
            words[s.start_ms // 1000 // window_s] += len(s.text.split())
    count = max(1, int(-(-(total_s - 10) // window_s)))  # ceiling; a tail under 10 s joins nothing
    for k in range(count):
        length_s = min(window_s, total_s - k * window_s)
        db = mean_volume(args.audio, k * window_s, length_s)
        per_min = words[k] / (length_s / 60)
        if db is None:
            status = "unreadable"
            flags.append(f"unreadable level {hms(k * window_s * 1000)}")
        elif db <= args.silent_db:
            status = "silent (measured)"
        elif per_min < args.min_wpm:
            status = "SUSPECT: audio at speech level but almost no words"
            flags.append(f"wordless window {hms(k * window_s * 1000)}")
        else:
            status = "ok"
        print(f"  {hms(k * window_s * 1000)}  {words[k]:5d} words  {per_min:5.0f}/min  {level_text(db)}  {status}")
    return flags


def cmd_check(args):
    if not os.path.isfile(args.audio):
        raise Unusable(f"{args.audio}: no such audio file")
    segs, notes = spliced(args.full, args.clip or [])
    total_s = duration_s(args.audio)
    end_ms = max((s.end_ms for s in segs), default=0)
    if end_ms / 1000 > total_s + AUDIO_SLACK_S:
        raise Unusable(f"{args.audio} lasts {hms(total_s * 1000)} but the transcript runs to {hms(end_ms)}; "
                       "pass the audio the transcript was made from")
    words = sum(len(s.text.split()) for s in segs if is_speech(s.text))
    print(f"segments {len(segs)}, last end {hms(end_ms)}, words {words}, audio {hms(total_s * 1000)}")
    for n in notes:
        print(f"  {n}")

    flags = [] if segs else ["empty transcript"]
    flags += report_loops(segs)
    flags += report_holes(args, segs, total_s)
    flags += report_windows(args, segs, total_s)
    print(f"\n{len(flags)} flagged" + (": " + "; ".join(flags) if flags else ", transcript proved"))
    return 1 if flags else 0


def cmd_reading_copy(args):
    if os.path.exists(args.out) and not args.force:
        raise Unusable(f"{args.out} exists; pass --force to overwrite")
    segs, notes = spliced(args.full, args.clip or [])
    for n in notes:
        print(n, file=sys.stderr)
    paras, current, start_ms = [], [], None
    for s in segs:
        if not is_speech(s.text):
            continue
        if start_ms is None:
            start_ms = s.start_ms
        elif s.start_ms - start_ms >= args.para * 1000:
            paras.append((start_ms, " ".join(current)))
            current, start_ms = [], s.start_ms
        current.append(s.text)
    if current:
        paras.append((start_ms, " ".join(current)))
    if not paras:
        print("no speech segments; nothing written", file=sys.stderr)
        return 1
    with open(args.out, "w", encoding="utf-8") as f:
        for para_start, text in paras:
            f.write(f"[{hms(para_start)}] {text}\n")
    print(f"{len(paras)} paragraphs, {sum(len(p[1].split()) for p in paras)} words -> {args.out}",
          file=sys.stderr)
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("full", help="whisper.cpp JSON of the whole file")
    common.add_argument("--clip", nargs=2, action="append", metavar=("JSON", "OFFSET"),
                        help="re-transcribed clip and its offset in seconds; repeatable, applied in order")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", parents=[common], help="loops, measured gaps and blanks, coverage by window")
    c.add_argument("--audio", required=True, help="source audio the transcript was made from (any format ffmpeg reads)")
    c.add_argument("--window", type=int, default=300, help="window length in seconds (default 300)")
    c.add_argument("--min-wpm", type=float, default=20, help="words/min below which a loud window is suspect (default 20)")
    c.add_argument("--silent-db", type=float, default=-60, help="window mean dB at or below which it counts as silent (default -60)")
    c.add_argument("--speech-db", type=float, default=-40, help="gap or blank mean dB above which it is suspect, unless half of it is silent (default -40)")
    c.add_argument("--gap", type=int, default=10, help="measure gaps and blank spans at least this long, seconds (default 10)")
    c.set_defaults(func=cmd_check)

    r = sub.add_parser("reading-copy", parents=[common], help="timed paragraphs for reading, clips spliced in")
    r.add_argument("out", help="output text file, one [H:MM:SS] paragraph per line")
    r.add_argument("--para", type=int, default=60, help="paragraph length in seconds (default 60)")
    r.add_argument("--force", action="store_true", help="overwrite OUT if it exists")
    r.set_defaults(func=cmd_reading_copy)

    args = p.parse_args()
    try:
        sys.exit(args.func(args))
    except Unusable as e:
        print(f"transcript.py: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
