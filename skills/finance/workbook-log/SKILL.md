---
name: workbook-log
description: Close out a task in an Excel finance workbook — complete the In-progress stub in place (or append a standalone block), refresh the Workbook Snapshot if the task changed it, clear the Handoff sheet and any Baseline sheets at close, flip a Tickets-sheet ticket to Done when the task traces to one, and propose Agent-sheet updates when the work surfaced standing guidance. The workbook loop's close-out phase.
disable-model-invocation: true
---

# /workbook-log

The fourth, **close-out** phase of the `/workbook-explore` → `/workbook-plan` → `/workbook-build` → `/workbook-log` loop. Closes a task by writing a structured entry to the **Audit Log** sheet — completing the In-progress stub `/workbook-plan` wrote, or appending a fresh block for a standalone fix — then refreshing the Workbook Snapshot, clearing the Handoff sheet and any Baseline sheets, and proposing Agent-sheet updates where the work earned them.

**Tasks, not sessions, are the unit of record.** Each `/workbook-log` writes one task block; multiple per session is normal.

## How this fits

- `/workbook-plan` writes an **In-progress stub** to the Audit Log at task start (Goal + a compressed Plan summary).
- `/workbook-build` executes and reports per step; it never writes to the Audit Log.
- `/workbook-log` either **completes the stub in place** (fills in Done, Validation, Deviations, Surfaced, Sheets touched and flips the status) or **appends a new block** when no stub exists (standalone fix). For completion state it reads `/workbook-build`'s `Status: [Complete | Partial]` summary; **`Cancelled` is `/workbook-log`'s own determination.**

The Audit Log is **history**; the Agent sheet is **the operating manual** synthesized from it. Keep them complementary — a dated event in the Audit Log, the standing rule it implies in the Agent sheet — never duplicated.

Two shared contracts define what this skill writes, both owned by the sheet-layer skill: the block format is the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md`; the sheet identities, Agent sections, Handoff lifecycle, and palette are the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`. On a multi-session effort workbook two more apply, same owner: the Tickets sheet this skill flips is its `TICKETS-SHEET.md`; the Baseline sheets it clears are its `BASELINE-SHEET.md`.

## When to use

Use when:
- The user says `/workbook-log`, "log this", "close this task", "write the audit log".
- A `/workbook-build` cycle finished (validation done, work checked) — complete its stub.
- The user did a quick fix without `/workbook-plan` / `/workbook-build` and wants it recorded.
- A task was cancelled and needs to be marked as such — cancelled tasks still get logged.

Skip it for:
- Orientation (`/workbook-explore`), planning (`/workbook-plan`), or executing (`/workbook-build`).
- A folder or filing system → `/folder-log`.

## Step 1: Gather context

Read the chat and workbook for this task and extract — **auto-omit any field that's empty**:

- **Goal** — what the task aimed at (one line).
- **Plan** — a compressed 2–3-line summary of the `/workbook-plan` six-section output, if a plan was made.
- **Done** — what `/workbook-build` executed: cell references, formulas added/changed, sheets modified, data imported, values updated; before → after for any changed formula.
- **Validation** — tie-outs run, pass/fail with the specific number compared ("Q3 total $4.2M ties to Summary!A1 within $200").
- **Deviations** — where execution went off plan, with the reason; capture any bounded loop-backs (`/workbook-build` → `/workbook-plan` / `/workbook-explore`).
- **Surfaced** — out-of-scope items noticed and queued, concrete enough to become future tasks ("audit the Q4 forecast assumptions", not "look into Q4").
- **Sheets touched** — every sheet modified, plus external artifacts.
- **Status** — **Complete / Cancelled / Partial.** Read `/workbook-build`'s summary for Complete vs Partial; determine Cancelled yourself.

A standalone quick fix (no plan, no build) populates only Date, Task, Goal, Done, and Sheets touched — expected.

## Step 2: Locate or create the Audit Log

**If it exists:** read it, find the last populated row, and check for an **In-progress stub** for this task (from `/workbook-plan`) — if present, you'll complete it in place in Step 3, not append. Note the Workbook Snapshot's current contents for Step 4.

**If none exists:** create the Audit Log sheet and its title rows the way `/workbook-onboarding` does, then write the Workbook Snapshot (its layout is `/workbook-onboarding`'s — Step 4) and the first block. `/workbook-log` defers sheet-creation layout to the canonical sheet-creator rather than re-spelling it.

## Step 3: Write the task block

Compose one task block per the format in the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md` — block header, status indicator, field rows (auto-omitting empties), inline **Fixed** / **Verified** / **Flagged** tags within Done. Leave a blank row between this block and the next.

- **Completing an In-progress stub:** the stub already carries the header (status In-progress), Goal, and Plan. Flip the status — recolor the dot + word and the block's left rail to the closing status — insert the new field rows (Done, Validation, Deviations, Surfaced, Sheets touched) below the existing Plan row, and apply formatting.
- **Appending a new block (no stub):** find the last populated row, add a blank row, write the header, then the populated field rows.

A standalone fix may be just Goal + Done + Sheets touched; a cancelled task may be Goal + Plan + Cancel reason.

**Issue-traced task:** when the task traces to an issue, the block names the issue and checks Done against its **acceptance criteria** — each criterion stated met or not, inside the existing fields (the criteria seeded the plan's Validation/Tie-outs, so this closes against the issue, not only the plan). A task with no issue gets no extra line.

**Ticket on the Tickets sheet:** when the task traces to a ticket on the workbook's **Tickets sheet** (a multi-session effort — the block names its T-id), read the acceptance criteria from that row, and after writing the block **flip the ticket's `Status` to Done and set the `Status date`** — the lifecycle's **Closed** step, per the `/workbook-onboarding` skill's `TICKETS-SHEET.md`. Flip, don't delete: the row is queue state; this block is the narrative.

**Effort complete — offer the audits, once.** Doubly conditional: the task traces to a Tickets-sheet ticket **and** the flip leaves no ticket on the sheet still Open or In progress. Then the effort's last ticket just closed — many sessions of self-checked work are about to become trusted output — so the close-out report (Step 6) says so: *that was the effort's last ticket; before the workbook goes out or gets trusted, `/formula-audit` then `/logic-audit` are the fresh-eyes pass — they read the cells cold, with none of the build sessions' assumptions.* Offer once, at this close, and **never auto-run** — both audits are user-invoked; naming them is the whole move. Either condition false — a mid-effort close, a ticketless task — no line.

## Step 4: Refresh the Workbook Snapshot — only if the task materially changed it

The Workbook Snapshot sits between the Audit Log header and the first task block; its row layout and formatting are defined by `/workbook-onboarding`, which creates it. `/workbook-log` **reads and refreshes** it — it does not re-author the layout. Update only when this task changed what the snapshot reports:

- New sheet created → **Sheet list**.
- Source data changed (new period, new file) → **Source data**.
- Key totals changed materially → **Key totals**.
- New dependency introduced or a limit changed → **Critical dependencies**.
- Workbook state changed (e.g. now needs review) → **Status**.

If none apply, **leave the snapshot alone.**

## Step 5: Propose an Agent-sheet update — when warranted

**The default is no proposal.** Most tasks change nothing in the Agent sheet — "nothing to propose" is the common, correct outcome, not a step left undone. Propose only when the task produced **standing guidance** a future session needs, that isn't a one-off historical event:

- **A new operating convention** — "Refresh Velixo before all GL tie-outs in this workbook — F9 won't refresh Velixo formulas."
- **A workbook-specific gotcha** — "Hidden assumption row at Forecast!47 — easy to miss when inserting rows."
- **A risk became active** — "Power Query refresh fails intermittently on Mondays — retry."
- **An open decision to persist** — "Revisit the Q4 assumption when April actuals arrive."
- **A user preference / edit policy** — "User vetoed the name-based-lookup refactor here; keep positional refs."

Do **NOT** propose for: one-time events (those live in the block's Done field), trivia (typos, formatting), anything already in the Agent sheet, or human-process docs (those belong in the Instructions sheet). This is the loop's in-place "deepening" — a proposed standing rule, not an architecture scan.

**How to propose** — surface the exact wording in chat under the target section (the five are defined in the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`), and ask:

> Proposing Agent-sheet update under **Operating conventions**:
> "Refresh Velixo before GL tie-outs — F9 alone won't refresh Velixo formulas."
>
> Accept, edit, or skip?

Accept → write it under that section. Edit → use the user's wording. Skip → don't write; note in the block's Done field that the observation was made but not codified.

## Step 6: Finalize formatting, verify, and report

1. **Run the finalization pass** on each sheet this task touched — the formatting `/workbook-build`
   deferred: text-wrap on and content rows top-aligned, row heights autofit with the 20px floor,
   title rows held at 28px, and nothing clipping. Geometry and alignment per the
   `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`. (The loop's formatting-timing rule:
   `/workbook-build` writes content only; the close-out polishes.)
2. **Clear any Baseline sheets** — delete every `Baseline — [sheet]` sheet the build created,
   whatever the closing status, and note "Baseline sheets cleared" in Sheets touched. The close
   half of the baseline lifecycle (Handoff-mirror: a temporary before-image, never a second
   history layer), per the `/workbook-onboarding` skill's `BASELINE-SHEET.md`. If a baseline
   stands at close and `/workbook-review` hasn't run for this task, offer it before clearing —
   the diff's raw material is never silently destroyed. Offered, never auto-run.
3. Re-read the rows you wrote — confirm no truncation or formatting issues.
4. Tell the user briefly: the task title, completion status, and the key items captured — plus
   the effort-complete audits offer when Step 3's doubly-conditional check fired.
5. If anything was intentionally **not** logged (trivial debugging, undone attempts), say so in one line.
6. If you wrote to the Agent sheet, confirm what was added.

## What NOT to log

- Intermediate debugging steps that led to no change; failed attempts immediately undone.
- Trivial formatting tweaks (unless part of a larger restructuring).
- Tool mechanics or API plumbing — log the outcome, not the plumbing.
- Long verbatim chat quotes — summarize for readability.
- AI deliberation ("considered X then chose Y") — log the decision, not the path to it.

## Content quality checklist

- [ ] Block header has the date/time; the task title summarizes the work in one line
- [ ] Cell references are specific ("Dashboard!C14", not "a cell on Dashboard"); sheet names copied exactly
- [ ] Before → after shown for any formula change; dollar amounts and row counts where relevant
- [ ] Validation entries state the actual tie-out — numbers, tolerance, pass/fail
- [ ] Deviations explain *why*, not just *that*; Surfaced items are concrete enough to become tasks
- [ ] Issue-traced task: block names the issue and Done checked against its acceptance criteria (no issue → nothing extra)
- [ ] Tickets-sheet ticket: `Status` flipped to Done with a `Status date` — flip, don't delete
- [ ] Effort-complete audits offer made iff the task traced to a Tickets-sheet ticket AND the flip left none open — offered once, never auto-run
- [ ] Baseline sheets cleared at close — none left behind; `/workbook-review` offered first when one stood unreviewed
- [ ] Empty fields omitted, not left blank; cancelled tasks carry a Cancel reason
- [ ] Workbook Snapshot refreshed only if the task materially changed it
- [ ] Finalization pass run on every sheet the task touched — autofit with floor, alignment, no clipping
- [ ] Agent-sheet update proposed only on standing guidance (default: none), with exact wording + accept/edit/skip

## Edge cases

**Stub from `/workbook-plan` but `/workbook-build` never ran:** mark the block **Cancelled**, reason "Abandoned after planning, work not started."

**No stub and no plan in chat:** standalone-fix mode — write a fresh block with whatever populates; skip Plan, Deviations, Surfaced.

**Multiple tasks in one `/workbook-log`:** rare — `/workbook-log` is per-task. Ask whether to write separate blocks (default) or combine; combining loses the per-task granularity the design exists for.

**Task crossed sessions via `/workbook-handoff`:** **clear the Handoff sheet** — delete the entire sheet — when this `/workbook-log` completes the task, and note "Handoff sheet cleared" in Sheets touched (the Handoff lifecycle's close half, per the `/workbook-onboarding` skill's `SHEET-CONTRACTS.md`). The block's date is the close-out date; mention the originating session in the Plan field if it matters.

**Re-logging or editing a prior task:** modify the block in place rather than appending; add "[Edited YYYY-MM-DD: reason]" in col B of the affected field to preserve the change history.
