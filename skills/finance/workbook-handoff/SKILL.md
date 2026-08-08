---
name: workbook-handoff
description: Write a Handoff sheet to an Excel finance workbook so a future session can resume a paused task cleanly — capturing the goal, plan, decisions, progress, next action, and the expensive-to-rediscover context. A user-invoked peer to the workbook loop, detected by `/workbook-explore` next session and cleared by `/workbook-log` at close. The workbook counterpart to `/handoff` (which covers non-workbook work).
disable-model-invocation: true
---

# /workbook-handoff

Generate a durable, structured artifact — the **Handoff sheet** — that lets a future session continue the current task with a fresh context window. A **peer** to the `/workbook-explore` → `/workbook-plan` → `/workbook-build` → `/workbook-log` loop, not a phase within it: invoked at any point during an active task when the user wants to pause and pick up later.

`/workbook-handoff` is the **creator** end of the Handoff lifecycle — `/workbook-explore` detects the sheet next session, `/workbook-log` clears it at close. This skill carries [`HANDOFF-FORMAT.md`](HANDOFF-FORMAT.md), the canonical block format it owns; the sheet identities, title rows, Handoff lifecycle, and palette are defined in the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`.

## When to use

Use when the user says `/workbook-handoff`, "hand this off", "set up for next session", "save this for later", "pause and pick up next time", "moving to a fresh chat" — i.e. they want to deliberately pause a task and continue it later, in a new chat, on another machine, or with a collaborator.

This skill is **purely user-invoked.** Don't invoke it speculatively from guesses about chat length, context state, or task complexity — the user decides when a handoff is needed.

Skip it for:
- **Task completion** — that's `/workbook-log`.
- **Non-workbook work** (research, writing, planning) with no Excel file in play — use `/handoff`.
- Quick mental notes with no cross-session continuity (chat or the Agent sheet), or a task finishing this session.

## How this fits

`/workbook-handoff` writes structured task state to the workbook — the plan and the decisions that shaped it, current progress and the specific next step, this task's user-stated preferences, and the non-obvious observations that read as background but are expensive to rediscover. It captures what otherwise lives only in chat and would be lost across the session boundary.

It does **NOT** write the Audit Log. The Handoff sheet is the in-flight record; `/workbook-log` captures the eventual resolution (Complete on resumption, Cancelled on abandonment) and clears the sheet. The full detection and clearing contract lives in the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`.

## Step 1: Confirm the handoff scope

Before writing, briefly check the chat: is there an active task (a `/workbook-plan` invocation, an in-progress `/workbook-build`, or a stub row in the Audit Log)? What was the user doing when they invoked `/workbook-handoff`?

If there's no clear active task — e.g. mid-exploration without a `/workbook-plan` — ask once: "What should I capture — the exploration findings, or are we further along than I'm reading?" A small check, one question, then proceed. When the handoff is for mid-exploration, what you capture is **leads to verify, not conclusions** — write the findings as the open questions and observations they are, so the next session examines them rather than inheriting them as settled.

## Step 2: Check for an existing Handoff sheet

If a Handoff sheet already exists, a prior handoff was never closed by `/workbook-log`. Two cases:

- **Stale handoff (prior task abandoned):** tell the user and ask whether to (a) overwrite and start fresh, (b) close the old one via `/workbook-log` first, or (c) cancel this handoff. Default to (a) with a warning — the alternative is a permanent orphan. Overwriting clears content from row 3 onward and preserves title rows 1–2.
- **Same task continuing:** if this chat is itself a resumption (the user picked up an earlier handoff), updating the same sheet with new progress is normal cross-session work.

## Step 3: Gather content

Read the chat and extract the six fields (per [`HANDOFF-FORMAT.md`](HANDOFF-FORMAT.md)):

- **Task goal** — one line of what "done" looks like, usually from `/workbook-plan`'s Goal.
- **Plan** — the full six-section plan if one exists (Goal, Approach, Steps, Validation/Tie-outs, Open Questions, Out of Scope); otherwise the rough approach communicated.
- **Decisions made in chat** — non-obvious context not in the plan ("User chose Velixo over paste-special"; "Dana approved deferring the refactor"; "Settled on $5k materiality").
- **Progress** — what's done, in-flight, and not started; be specific about which plan Steps, and any partial work needing finishing or rollback.
- **Next action** — the specific first step ("Open Forecast, refresh Velixo, complete Step 4: update assumptions row 47 from April actuals"), not "continue the work".
- **Context to preserve** — the anti-loss catch-all. Litmus: "If a future session redid this task without knowing this, would it screw up?" ("Velixo refresh fails silently if Branch filter is blank"; "Detail sheet bounded at row 9055 — don't extend without checking").

**Mark a guess as a guess.** This field freezes observations for the next session, so an unverified hunch written as fact is inherited as fact. Tag what you didn't confirm — *"unverified: Velixo refresh may fail silently if Branch filter is blank — check"* — so the next session verifies it rather than trusting it.

## Step 4: Write the Handoff sheet

Add a sheet named exactly **`Handoff`** at the last position, with its title banner (alert-orange fill, A1/A2 text, tab color, two-column geometry) per the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`, then write the handoff block — metadata row, orange rail, the six fields, field-row formatting — per [`HANDOFF-FORMAT.md`](HANDOFF-FORMAT.md). One handoff block per sheet (a single in-flight task).

**Self-format at creation.** The Handoff sheet leaves this pass fully formatted — geometry, autofit with the floor, alignment, tab color, the template-version cell note on its title cell — so a paused task's surface is complete the moment it's written; nothing waits for a later phase.

If overwriting a stale sheet, clear content from row 3 onward (preserve title rows 1–2) and write the new block.

## Step 5: Optional .md export

Default is the sheet only — **.md export is opt-in.** If the user asks ("also give me a markdown file", "I want to email this to myself", "export as .md"), write `handoff-[YYYY-MM-DD].md` where the user can reach it — on Cowork, the outputs folder plus `present_files` to make it downloadable; on a filesystem, beside the workbook — in addition to the sheet:

```
# Handoff — [Workbook Name]

**Created:** YYYY-MM-DD HH:MM
**Originated in chat ending:** [date]

## Task goal
[One-line goal]

## Plan
[Full six-section plan or rough approach]

## Decisions made in chat
[Non-obvious context]

## Progress
[Done / in-flight / not started]

## Next action
[Specific first step for next session]

## Context to preserve
[Non-obvious observations]

---

**To use this handoff in a new session:**
1. Open the workbook in the new chat
2. Invoke `/workbook-explore` — it detects the Handoff sheet and offers to pick up the task
3. Alternatively, paste this entire file into the new chat for the same effect
```

## Step 6: Verify and report

1. Re-read the Handoff sheet — confirm no truncation or formatting issues.
2. Tell the user briefly: what was captured (task title, key fields populated), and that the next session can run `/workbook-explore` in the same workbook to auto-detect and resume.
3. Flag any field that's sparse or you couldn't fully populate ("Context to preserve has only one item — let me know if there's more").

## Content quality checklist

- [ ] Task goal is one line, concrete enough to recognize "done"
- [ ] Plan captures the full six-section structure if a `/workbook-plan` existed
- [ ] Decisions capture what isn't already in the plan
- [ ] Progress is specific about which steps are done vs. in-flight
- [ ] Next action is a concrete first step, not "continue the work"
- [ ] Context to preserve passes the rediscovery test; unverified items tagged as guesses
- [ ] Cell references use exact sheet names and addresses
- [ ] Originating chat date captured in the metadata row

## Edge cases

**No active task:** ask what to capture — they may want to hand off exploration findings, or invoked the wrong skill. Don't write an empty Handoff sheet.

**Mid-`/workbook-build` with partial work to roll back:** capture the rollback in Next action ("Roll back Forecast!C7:C20 before resuming — made before the plan was revised"). The next session executes it first.

**Existing Handoff for a different task:** warn clearly ("There's a Handoff sheet for [task] dated [date]. Overwriting will lose it.") and default to asking before overwriting; the user may want to `/workbook-log` the prior task first.

**Workbook inaccessible next session:** the sheet won't help if the workbook isn't open in the next chat. If the user may be hopping machines or chats without it, proactively offer the .md export.

**Very long field:** Excel cells hold a lot, but if a field exceeds ~10 lines consider splitting (e.g. a very long Plan → reference rather than inline). Otherwise write it all and let the cell wrap.

## What NOT to put in the Handoff sheet

- Verbatim chat dumps — summarize.
- Information already in the Instructions, Agent, or Audit Log sheets — don't duplicate.
- Tool mechanics or AI deliberation ("considered X then chose Y") — capture decisions, not the path to them.
- Optimistic estimates of remaining work — be honest about scope; the next session discovers the truth quickly anyway.
