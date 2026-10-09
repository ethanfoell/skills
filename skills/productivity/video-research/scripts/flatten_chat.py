#!/usr/bin/env python3
"""Flatten a YouTube chat replay (yt-dlp `live_chat` JSON lines) into Markdown.

Python 3 standard library only.

  python3 -I flatten_chat.py LIVE_CHAT.json OUT.md [--title TITLE] [--force]

One line per message, sorted by source time:
  - `H:MM:SS` **@author** [owner|mod|verified] (paid $5.00): text
Messages sent before the recording started all carry offset 0. Prints counts
as JSON to stdout so they can go straight into the ledger.
"""
import argparse
import json
import os
import sys

KINDS = {
    "liveChatTextMessageRenderer": "text",
    "liveChatPaidMessageRenderer": "paid",
    "liveChatPaidStickerRenderer": "sticker",
    "liveChatMembershipItemRenderer": "membership",
}
ROLE_BY_ICON = {"OWNER": "owner", "MODERATOR": "mod", "VERIFIED": "verified"}
ROLE_BY_TOOLTIP = {"Owner": "owner", "Moderator": "mod", "Verified": "verified"}


def hms(ms):
    # Same helper as transcript.py: the scripts run with `python3 -I`, which
    # keeps a script's own folder off sys.path, so neither can import the other.
    s = max(0, int(ms) // 1000)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def runs_text(message):
    out = []
    for run in (message or {}).get("runs", []):
        if "text" in run:
            out.append(run["text"])
        elif "emoji" in run:
            emoji = run["emoji"]
            out.append((emoji.get("shortcuts") or [emoji.get("emojiId", "")])[0])
    return "".join(out).replace("\n", " ").strip()


def roles(item):
    found = []
    for badge in item.get("authorBadges", []):
        b = badge.get("liveChatAuthorBadgeRenderer", {})
        role = ROLE_BY_ICON.get(b.get("icon", {}).get("iconType", "")) or ROLE_BY_TOOLTIP.get(b.get("tooltip", ""))
        if role:
            found.append(role)
    return found


def tag_for(kind, item):
    """The parenthesised tag after the author, or "" for a plain message."""
    amount = item.get("purchaseAmountText", {}).get("simpleText", "?")
    if kind == "paid":
        return f"(paid {amount})"
    if kind == "sticker":
        return f"(paid sticker {amount})"
    if kind == "membership":
        header = runs_text(item.get("headerSubtext")) or item.get("headerSubtext", {}).get("simpleText", "")
        return f"(membership: {header})" if header else "(membership)"
    return ""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("src", help="yt-dlp live_chat JSON-lines file")
    p.add_argument("out", help="Markdown file to write")
    p.add_argument("--title", default="Live chat replay", help="heading for the output file")
    p.add_argument("--force", action="store_true", help="overwrite OUT if it exists")
    args = p.parse_args()
    if os.path.exists(args.out) and not args.force:
        print(f"flatten_chat.py: {args.out} exists; pass --force to overwrite", file=sys.stderr)
        sys.exit(2)

    rows = []
    counts = dict.fromkeys(KINDS.values(), 0)
    unparsed = 0
    with open(args.src, encoding="utf-8", errors="replace") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                replay = json.loads(line).get("replayChatItemAction", {})
            except ValueError:
                unparsed += 1  # a truncated or garbled line, usually the last one
                continue
            offset_ms = int(replay.get("videoOffsetTimeMsec", 0))
            for action in replay.get("actions", []):
                for renderer, item in action.get("addChatItemAction", {}).get("item", {}).items():
                    kind = KINDS.get(renderer)
                    if not kind:
                        continue
                    text = "" if kind == "sticker" else runs_text(item.get("message"))
                    author = item.get("authorName", {}).get("simpleText", "?")
                    rows.append((offset_ms, int(item.get("timestampUsec", 0)), author, roles(item), tag_for(kind, item), text))
                    counts[kind] += 1

    rows.sort(key=lambda r: (r[0], r[1]))
    with open(args.out, "w", encoding="utf-8") as out:
        out.write(f"# {args.title}\n\n")
        for offset_ms, _, author, role_tags, tag, text in rows:
            parts = [f"- `{hms(offset_ms)}` **{author}**"] + [f"[{r}]" for r in role_tags] + ([tag] if tag else [])
            out.write(" ".join(parts) + (f": {text}" if text else "") + "\n")

    print(json.dumps({
        "messages": len(rows),
        **counts,
        "at_offset_zero": sum(1 for r in rows if r[0] == 0),
        "last_offset": hms(max((r[0] for r in rows), default=0)),
        "unparsed_lines": unparsed,
    }))


if __name__ == "__main__":
    main()
