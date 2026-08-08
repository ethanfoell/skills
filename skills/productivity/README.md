# Productivity

Genuinely cross-domain workflow tools — not finance-specific, not code-specific.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[chat-title](./chat-title/SKILL.md)** — Propose a short, scannable title for the current chat: the high-level work it did, not the repo or date the app already groups by.
- **[grill-me](./grill-me/SKILL.md)** — Get relentlessly interviewed about a plan or design until every branch of the decision tree is resolved.
- **[grill-with-docs](./grill-with-docs/SKILL.md)** — Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[handoff](./handoff/SKILL.md)** — Compact the current conversation into a handoff document so another agent can continue the work.
- **[retitle-sessions](./retitle-sessions/SKILL.md)** — Batch-improve the titles of past Claude Code sessions: find badly-titled ones, propose better names (reusing the `chat-title` grammar), and help you apply them. CCD/Cowork only.
- **[teach](./teach/SKILL.md)** — Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[daily-note](./daily-note/SKILL.md)** — Summarize the current chat session into a manager-scannable daily note: a maximally dense headline plus a fuller cut when warranted, outcomes not process.
- **[grill-with-files](./grill-with-files/SKILL.md)** — Stress-test a plan against the files it touches: open the workbooks, data, PDFs, and folder, resolve what the files can answer by looking, and run a `/grilling` session grounded in what's on disk.
- **[grilling](./grilling/SKILL.md)** — Interview the user relentlessly about a plan or design until every branch of the decision tree is resolved. The reusable loop behind `grill-me`, `grill-with-docs`, and `grill-with-files`.
- **[meeting-notes](./meeting-notes/SKILL.md)** — Turn a raw or messy meeting transcript into a digestible debrief (TL;DR, key discussion, decisions, action items) saved as Markdown, plus an optional cleaned-up transcript when the source is dirty. Corrects transcription noise, never invents content.
- **[work-coms](./work-coms/SKILL.md)** — Draft a polished work message (email, Teams, Slack, Ramp comment, vendor reply) in the user's voice from a rough draft or context dump.
