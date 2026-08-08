---
name: meeting-notes
description: Turn a raw or messy meeting transcript — including the auto-generated, punctuation-free kind from Apple Voice Memos or the Notes app — into a rich, digestible meeting debrief (TL;DR, key discussion, decisions, action items, open questions, next steps) saved as a Markdown file, and, when the source is dirty, an optional cleaned-up readable transcript saved as a second file. Use whenever the user drops in a meeting transcript, call transcript, recording, or voice memo and wants notes, a debrief, a summary, an action plan, or action items — at any level of transcript cleanliness — or says "turn this into meeting notes", "clean up this transcript", "what were the action items", "debrief this meeting", or invokes /meeting-notes. Corrects transcription noise without inventing content; marks what it cannot hear as [unclear] rather than guessing.
---

Takes a meeting transcript at **any level of cleanliness** — often the auto-generated, punctuation-free, speaker-less blob from Apple Voice Memos or the Notes app — and turns it into a digestible **meeting debrief**. When the source is dirty, it also offers a **cleaned-up transcript** as a separate file. The debrief is always produced; the cleaned transcript is offered only when the source actually needs it.

This is for **external transcripts** — a recording of a meeting that happened elsewhere. It is not `/daily-note` (which summarizes the current chat session for a manager) and not `/work-coms` (which drafts a message). If the user wants a record of *this chat*, route to `/daily-note` instead.

## The cardinal rule: correct, never author

Transcripts — especially auto-generated ones — are full of noise: missing punctuation, run-on speech, mis-heard words, no speaker labels. This skill **cleans that noise**. It does **not** invent, infer beyond the evidence, or smooth over gaps with plausible-sounding content.

- Fix punctuation, capitalization, and paragraphing freely.
- Correct an obvious transcription error **only when context makes the intended word unambiguous** (e.g. "charge back" → "chargeback"; "Mat" → "Matt" once the name is established).
- **Never invent** a number, name, date, decision, or owner that isn't in the source. A debrief that fabricates a figure is worse than one that flags the figure as unclear.
- When something is genuinely inaudible, garbled, or ambiguous, mark it `[unclear]` (or `[unclear: sounds like "…"]`) rather than guessing. This holds for both the debrief and the cleaned transcript.

This rule is the whole point of the skill. A finance meeting about chargebacks is exactly where a confidently-wrong number does damage.

## Speaker attribution

Auto-generated transcripts usually have no speaker labels — just one undifferentiated stream. Attribute with a **light touch**:

- Infer a speaker **only when the content makes it clear** (a direct "Matt, can you take the reconciliation?" handoff, or an "I'll own that" next to an established name).
- Where it isn't clear, leave it unattributed or mark `[speaker?]` — don't assign turns by guesswork.
- If knowing the participants up front would materially sharpen attribution, you may ask **once** for the names, but never block on it. Proceed with best-effort inference if the user doesn't supply them.

## Workflow

### Step 1 — Ingest the transcript

Accept pasted text or a file path. Read the **whole** transcript — never truncate or sample a long one.

### Step 2 — Assess cleanliness

Judge whether the source is **dirty** (absent or erratic punctuation, run-on sentences, no paragraph breaks, no speaker labels, visible ASR errors) or **already clean**. This decides whether to offer a cleaned transcript in Step 4.

### Step 3 — Build the debrief (always)

Produce the debrief using the format below. This is the primary deliverable. Lead with substance: someone who missed the meeting should come away knowing what happened, what was decided, and what they owe.

### Step 4 — Offer the cleaned transcript (only if dirty)

If Step 2 found the source dirty, offer it: *"The transcript is pretty rough — want me to also save a cleaned-up, readable version?"* If the source was already clean, skip the offer; a second near-identical file is just clutter.

### Step 5 — Save and present

Save the chosen file(s) and present them. Default location: a `meetings/` subfolder in the working folder. Default names:

- `YYYY-MM-DD_<topic-slug>_debrief.md`
- `YYYY-MM-DD_<topic-slug>_transcript.md`

Use the meeting date when it's evident from the transcript; otherwise today's date. Give a one- or two-line chat summary — don't paste the whole debrief back into chat.

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

Adapt to the meeting: drop **Decisions** if there were none; fold **Next steps** into **Action items** when they're the same thing. **Action items** always appears, even when sparse — a reader's first question is "what do I owe." Write plain, scannable prose; no em dashes in the saved output. Report what happened, not your own advice — no editorializing ("the team should consider…") unless the user asks for it.

## Cleaned-transcript format

A readable version of the **same words** — not a summary:

- Punctuation, capitalization, sentence and paragraph breaks added.
- Speaker labels where attribution is confident (per the rule above).
- Obvious ASR errors corrected from context; `[unclear]` where not.
- **No content added or removed.** Same meaning, same substance, just legible.

Optionally open with a one-line header (`# Cleaned transcript: <topic>`, plus date/source) so the file stands on its own.
