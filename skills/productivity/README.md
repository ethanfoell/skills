# Productivity

Genuinely cross-domain workflow tools: not finance-specific, not code-specific.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[chat-title](./chat-title/SKILL.md)**: Propose a short, scannable title for the current chat, naming the high-level work it did rather than the repo or date the app already groups by.
- **[daily-note](./daily-note/SKILL.md)**: Summarize the current session as a manager-facing daily note: one plain line per front of work, ready to paste into one Excel cell, plus a More detail block.
- **[grill-me](./grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[grill-with-docs](./grill-with-docs/SKILL.md)**: Grilling session that also builds your project's domain model, sharpening terminology and updating `GLOSSARY.md` and ADRs inline.
- **[handoff](./handoff/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[retitle-sessions](./retitle-sessions/SKILL.md)**: Batch-improve the titles of past Claude Code sessions: find badly-titled ones, propose better names (reusing the `chat-title` grammar), and help you apply them. CCD/Cowork only.
- **[teach](./teach/SKILL.md)**: Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can, filled in async or together over a meeting. Interviews you about the send (who, what you need back), not the subject.
- **[unslop](./unslop/SKILL.md)**: Cut AI tells from a piece of writing and sharpen its voice without changing what it says. Point it at a draft, a doc, or a message; facts, names, and numbers stay fixed, and it never invents an opinion. Adapted from Cursor's `pstack` plugin (MIT, credited in `NOTICE`).
- **[wait-what](./wait-what/SKILL.md)**: Fire it the moment a message doesn't land: the agent re-pitches what it just said with the context you were missing, in Simplified Technical English, using the `GLOSSARY.md` vocabulary.
- **[wrap-up](./wrap-up/SKILL.md)**: Close out the current session: account for everything that changed, write the summary (Done / Where it stands / Open / Next), and propose the high-value writes (learnings, commits, doc prunes) for approval. Routes loop work to its own close-out first.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grill-with-files](./grill-with-files/SKILL.md)**: Stress-test a plan against the files it touches: open the workbooks, data, PDFs, and folder, resolve what the files can answer by looking, and run a grounded `/grilling` session on what's on disk.
- **[grilling](./grilling/SKILL.md)**: Interview the user relentlessly about a plan or design, a round of questions at a time, until every branch of the design tree is resolved. The reusable loop behind `grill-me`, `grill-with-docs`, and `grill-with-files`.
- **[meeting-notes](./meeting-notes/SKILL.md)**: Turn a raw or messy meeting transcript into a digestible debrief (TL;DR, key discussion, decisions, action items) saved as Markdown, plus an optional cleaned-up transcript when the source is dirty. Corrects transcription noise, never invents content.
- **[video-research](./video-research/SKILL.md)**: Investigate a topic across a recording with explicit transcript, audio, and visual coverage; save timestamped research notes, useful screenshots, and a durable source archive.
- **[work-coms](./work-coms/SKILL.md)**: Draft a polished work message (email, Teams, Slack, Ramp comment, vendor reply) in the user's voice from a rough draft or context dump.
