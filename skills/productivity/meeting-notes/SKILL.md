---
name: meeting-notes
description: Turn a raw or messy meeting transcript, including the auto-generated punctuation-free kind from Apple Voice Memos or the Notes app, into a rich, digestible meeting debrief (TL;DR, key discussion, decisions, action items, open questions, next steps) saved as a Markdown file, plus an optional cleaned-up readable transcript saved as a second file when the source is dirty. Use whenever the user drops in a meeting transcript, call transcript, recording, or voice memo and wants notes, a debrief, a summary, an action plan, or action items, at any level of transcript cleanliness, or says "turn this into meeting notes", "clean up this transcript", "what were the action items", "debrief this meeting", or invokes /meeting-notes. Corrects transcription noise without inventing content; marks what it cannot hear as [unclear] rather than guessing.
---

Turns an external transcript (a recording of a meeting that happened elsewhere) into a saved meeting debrief. To summarize the current chat session for a manager, route to `/daily-note`; to draft a message, `/work-coms`.

## Workflow

1. **Ingest.** Accept pasted text or a file path. Read the whole transcript; never truncate or sample a long one.
2. **Assess cleanliness.** Dirty means absent or erratic punctuation, run-on sentences, no paragraph breaks, no speaker labels, or visible ASR errors.
3. **Build the debrief** (always, using the format below). Lead with substance: someone who missed the meeting should come away knowing what happened, what was decided, and what they owe.
4. **Offer a cleaned transcript** only if step 2 found the source dirty: *"The transcript is pretty rough. Want me to also save a cleaned-up, readable version?"* A second near-identical copy of a clean source is clutter.
5. **Save and present.** Default location: a `meetings/` subfolder in the working folder. Default names: `YYYY-MM-DD_<topic-slug>_debrief.md` and `YYYY-MM-DD_<topic-slug>_transcript.md`, dated from the transcript when the meeting date is evident, else today. Give a one- or two-line chat summary rather than pasting the debrief back into chat.

## Correct, never author

Clean transcription noise; never invent, infer beyond the evidence, or smooth gaps with plausible-sounding content. In both files:

- Fix punctuation, capitalization, and paragraphing freely.
- Correct a transcription error only when context makes the intended word unambiguous ("charge back" → "chargeback"; "Mat" → "Matt" once the name is established).
- Never invent a number, name, date, decision, or owner that isn't in the source. A debrief that fabricates a figure is worse than one that flags it as unclear.
- Mark anything inaudible, garbled, or ambiguous `[unclear]` (or `[unclear: sounds like "…"]`) rather than guessing.

Attribute speakers with the same light touch: infer a speaker only when the content makes it clear (a direct "Matt, can you take the reconciliation?" handoff, or "I'll own that" next to an established name); otherwise leave the turn unattributed or mark `[speaker?]`. If knowing the participants would materially sharpen attribution, ask once for the names, but never block: proceed on best-effort inference if the user doesn't supply them.

## Debrief format

```
# Debrief: <Meeting title / topic>

**Date:** <meeting date, or "undated">
**Participants:** <names if known, else "not identified in transcript">
**Source:** <voice-memo transcript / call recording / etc.>

## TL;DR
2–4 sentences: what the meeting was about and the single most important outcome.

## Key discussion
The substance, organized by topic (not chronologically, unless the order matters).
Enough detail that someone who missed it is caught up. This is the rich part.

## Decisions
What was actually decided. Omit this section if nothing was decided.

## Action items
- **<owner>**: <task> (<due date if stated, else "no date">)
Always include this section. If the meeting produced none, say "None identified."

## Open questions / parking lot
Unresolved threads, things deferred, questions raised without answers.

## Next steps
Concrete follow-ups and what happens before the next touchpoint.
```

Adapt to the meeting: drop **Decisions** when nothing was decided; fold **Next steps** into **Action items** when they're the same thing. **Action items** always appears, even when sparse; a reader's first question is "what do I owe." Write plain, scannable prose with no em dashes in the saved output, and report what happened without editorializing ("the team should consider…") unless the user asks for advice.

## Cleaned-transcript format

The same words made legible, not a summary: punctuation, capitalization, and sentence and paragraph breaks added; speaker labels where attribution is confident; obvious ASR errors corrected from context, `[unclear]` where not; no content added or removed. Optionally open with a one-line header (`# Cleaned transcript: <topic>`, plus date/source) so the file stands on its own.
