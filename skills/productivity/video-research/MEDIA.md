# Media acquisition and timing

Examples of a local workflow with `yt-dlp`, `ffmpeg`, and whisper.cpp; any equivalent backend works. For flags beyond these, read the installed tool's `--help` or its docs: [yt-dlp](https://github.com/yt-dlp/yt-dlp#usage-and-options), [FFmpeg](https://ffmpeg.org/ffmpeg.html), [whisper.cpp](https://github.com/ggml-org/whisper.cpp#quick-start).

## Captions

```sh
yt-dlp --ignore-config --no-playlist --list-subs "$video_url"
yt-dlp --ignore-config --no-playlist --skip-download --write-auto-subs \
  --sub-langs 'en-orig' --sub-format json3 \
  -o "$archive_dir/%(id)s.%(ext)s" "$video_url"
```

- `--ignore-config --no-playlist` keeps the user's config and the surrounding playlist out of the run. Quote the URL.
- List tracks first and pick the real source-language one. On YouTube the untranslated automatic track is usually `<lang>-orig` (`en-orig` above); other listed languages are machine translations. Use `--write-subs` for authored subtitles.
- Prefer `json3` for YouTube automatic captions: each event carries only its new words, with timing. Flatten it by joining each event's `segs` and skipping `aAppend` events, which hold only line breaks. The VTT form of the same track repeats every line across rolling cues.

## Audio and video downloads

```sh
yt-dlp --ignore-config --no-playlist --list-formats "$video_url"
yt-dlp --ignore-config --no-playlist -f "$format_id" \
  -o "$archive_dir/%(id)s.%(ext)s" "$video_url"
```

- Pick a video format whose resolution makes small on-screen text readable. For audio, select an audio format; the `bestaudio/best` fallback may bring video along.
- `HTTP Error 403: Forbidden` on the media download usually means the default player client is blocked. Switch clients with `--extractor-args "youtube:player_client=web_embedded"` (worked in September 2026), on the format listing too, since format ids differ per client.
- Run `yt-dlp` unpiped, or check its own exit status: piped into `tail`, a failed download reports the pipe's success. The same goes for a background chain, which reports its last command: capture `$?` right after `yt-dlp`.
- Skip `--write-info-json`: the file holds every fragment URL, signed, and ran to 83 MB on one DASH VOD in October 2026. Take metadata with `--print` instead. If the file already exists, copy the fields you need into a small file and delete it.
- A `video+audio` format pair fetches the audio again even when the audio file already exists. Download the audio once, then the video, and merge locally; or accept the second fetch.
- `--download-sections '*HH:MM:SS-HH:MM:SS'` fetches a window cut at keyframes, so the clip's true start can differ from the request. Verify the offset (next section) before trusting it.
- yt-dlp ships fixes for YouTube changes every few weeks. Update it before a run, through whatever installed it (`brew upgrade yt-dlp`, `pipx upgrade yt-dlp`). When an extractor fails some other way, check `yt-dlp --version` and the error text, and retry only after changing something the error points at.

## Audio and transcription

```sh
ffmpeg -n -i "$audio_path" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$archive_dir/full.16k.wav"
whisper-cli -m "$model_path" -l "$lang" -mc 0 -f "$archive_dir/full.16k.wav" \
  -oj -osrt -otxt -of "$archive_dir/full.$model_name"
python3 -I "$skill_dir/scripts/transcript.py" check "$archive_dir/full.$model_name.json" --audio "$audio_path"
```

- whisper.cpp reads 16 kHz mono PCM WAV, which this produces. `-n` refuses to overwrite, so give every file its own name. Match the model to the language: `.en` models handle English only. Look in the usual model folders, such as `~/.cache/whisper-cpp/`, before searching the disk. The scripts read whisper.cpp's `-oj` JSON only.
- whisper.cpp fails two ways under normal-looking timestamps: it loops (one sentence repeated for minutes), or it emits `[BLANK_AUDIO]` straight through speech (an hour of it once, after an 11-minute silent lead-in). `-mc 0` stops the decoder carrying text from one window to the next, and on the recording that showed both failures it cleared both, with timestamps that matched a short reference clip (October 2026). It can still loop briefly on silence (ten `>>` markers once), which `check` catches. It also makes `--prompt` inert, so leave the prompt out and fix names in proofreading. `--vad` cleared both failures too but shifted later timestamps by the length of the silence it cut, 20 seconds in one place, so it is a poor fit wherever source time is cited.
- `scripts/transcript.py check` is the coverage proof, measured against the audio the transcript was made from. It flags a line repeated back to back or five times over; a gap, lead-in, tail, or blank span of 10 seconds or more whose mean level is above -40 dB and less than half of which is silent; and a five-minute window above -60 dB with under 20 words a minute. Those defaults, the options that change them, and the exit codes are in its `--help`. Resolve each flag by looking at a frame or listening: log music, a holding screen, or a played clip as irrelevant with that reason, or re-transcribe the window as a clip.
- A clip's **offset** is its start in the source: source time = offset + clip time. Store the offset with the clip. Exit status says nothing about timing, so check the clip's duration with `ffprobe` and spot-check a known line against the source. Cut from the full WAV, or from the source audio when there is none (a targeted excerpt):
  ```sh
  ffmpeg -n -ss "$offset_seconds" -t "$duration_seconds" -i "$archive_dir/full.16k.wav" \
    -c copy "$archive_dir/clip-$offset_seconds.wav"
  ffmpeg -n -ss "$offset_seconds" -t "$duration_seconds" -i "$audio_path" \
    -vn -ar 16000 -ac 1 -c:a pcm_s16le "$archive_dir/excerpt-$offset_seconds.wav"
  ```
- Rerun `check` with each clip as `--clip CLIP.json OFFSET`, later clips winning where they overlap, until every remaining flag is resolved, since a clip can loop too. `scripts/transcript.py reading-copy` takes the same arguments and writes the timed reading copy, one `[H:MM:SS]` paragraph per minute, leaving the raw outputs untouched.
- Silence, music, and poor audio still produce confident invented text. Check consequential passages against captions or the video.

## Frames

```sh
ffmpeg -n -ss "$clip_seconds" -i "$video_clip" -frames:v 1 "$frame_path"
ffmpeg -n -i "$video_clip" -vf "fps=1/10,scale=480:-1,tile=6x5" "$archive_dir/sheet-%03d.png"
```

- `-ss` before `-i` seeks straight to the frame; after `-i` it decodes the whole file up to that point.
- `$clip_seconds` is clip time, which equals source time only for a whole-file download. Otherwise derive source time from the clip's verified offset before naming or citing the image; nearby speech and recognizable visual transitions confirm alignment. Label a timestamp approximate when alignment is uncertain.
- Sample several frames around the moment and pick one after scrolling or transitions settle.
- Read frames with vision; confirm OCR output by eye for commands, filenames, and numbers.
- Keep enough context in the frame to identify the application or document, and keep the original beside any crop.
- The second command builds contact sheets for navigation: one tile per 10 seconds, 30 per sheet, read left to right. Homebrew's ffmpeg often lacks `drawtext`, so find a tile's time by counting. Tiles are candidates.
