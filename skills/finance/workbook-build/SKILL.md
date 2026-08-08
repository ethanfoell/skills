---
name: workbook-build
description: Execute a finalized `/workbook-plan` in an Excel finance workbook with discipline — per-step reporting, inline Validation/Tie-outs as affected Steps complete, destructive-op confirmation (with a pre-flight baseline-sheet snapshot when the scan flags destructive work), and a Surfaced list for out-of-scope discoveries. Reads the In-progress stub `/workbook-plan` wrote (never writes it); conditionally composes `/excel-finance-workbooks` and `/velixo-formulas`. Operates in lightweight mode when no plan is in context. The workbook loop's execution phase.
disable-model-invocation: true
---

# /workbook-build

The third phase of the `/workbook-explore` → `/workbook-plan` → `/workbook-build` → `/workbook-log` loop. Executes a finalized plan with discipline, checkpoints, and inline validation. The work is real per-cell step machinery, so this phase runs a full per-step execution structure and adds the **four guardrails** that prevent the failure modes — drift, scope creep, silent destructive operations, and skipped verification.

1. **Per-step reporting** — one line per material change.
2. **Inline Validation/Tie-outs** — run each check as the last Step it depends on completes, not at the end.
3. **Destructive-op confirmation** — pause for explicit confirmation before any destructive operation.
4. **Surfaced list** — out-of-scope discoveries queued, never silently done.

## When to use

Invoke when a `/workbook-plan` is finalized and you're ready to execute, when a `/workbook-build` → `/workbook-plan` loop produced a revised plan, or when you want to do workbook work directly without a plan first (lightweight mode — see below). Skip it for:
- Orientation only (use `/workbook-explore`).
- Planning only (use `/workbook-plan`).
- Closing out a task (use `/workbook-log`).
- Folders or filing systems (use `/folder-build`).

## How this fits

- `/workbook-plan` drafted the six-section plan and wrote an In-progress stub to the Audit Log.
- `/workbook-build` reads the plan from chat (or runs without one in lightweight mode), executes the Steps in order, runs Validation/Tie-outs as affected Steps complete, and pauses on its triggers (destructive ops, plan invalidation, validation failure, workbook drift).
- When execution finishes, `/workbook-build` produces a structured summary `/workbook-log` reads against; the user invokes `/workbook-log` to close out — it completes the stub in place.

`/workbook-build` modifies only user-facing workbook content per the plan. It does **not** touch the stub row, the Workbook Snapshot, or the Agent sheet — those all belong to `/workbook-log`.

**Formatting is deferred.** `/workbook-build` writes content only — values and formulas, with text-wrap left on — and skips polish passes mid-task; `/workbook-log` runs the finalization pass (autofit with floor, alignment, no-clipping check) on the touched sheets at close. The rule defers the finish-line polish, not the task: a plan Step that *is* formatting work still executes.

## Step 1: Verify plan and prerequisites

Three fast checks before executing:

1. **Plan in chat?** Identify the six-section plan from a recent `/workbook-plan`. If Validation is vague ("verify it looks right"), surface that **before** executing, not after. If no plan is in context, see **Lightweight mode** — don't block.
2. **Stub row in the Audit Log?** There should be — `/workbook-plan` writes it. If it's missing, the user may have skipped `/workbook-plan` (lightweight mode) or the stub got lost (rare); note the gap — `/workbook-log` appends a fresh block at close. `/workbook-build` reads the stub but never writes it.
3. **Right reference skills loaded?** Scan chat for prior load announcements within this task. If `/workbook-plan` loaded `/velixo-formulas` or `/excel-finance-workbooks`, skip reload; if not loaded but the triggers fire now (Velixo functions in Steps, structural changes in Approach), compose them and note what loaded.

## Step 2: Pre-flight scan

Quickly scan the plan before executing:

- **Map Validation/Tie-outs to Steps.** Which Steps does each check depend on? Run each as the last Step it depends on completes — not at the end. If `/workbook-plan` ordered the work as **vertical slices**, the slice boundaries are those checkpoints: **close each slice with its tie-out before opening the next**, so a wrong formula halts the build before it replicates into the next unit.
- **Flag destructive operations — and snapshot a baseline when any are flagged.** Identify any Step meeting the destructive criteria (see **Destructive operations**). These pause for confirmation when reached, regardless of plan content. If the scan flagged one or more, capture a **baseline** before executing: for each sheet the plan is about to touch, a `Baseline — [sheet]` formula-text before-image, per the `/workbook-onboarding` skill's `BASELINE-SHEET.md` contract. The scan's verdict is the whole trigger — destructive means pre-existing content will be modified or lost, so there is a "before" worth capturing; an additive build creates nothing, ever. `/workbook-log` clears the baseline at close.
- **Note handback steps.** Steps the plan marked **Handback** (a Velixo refresh above all) are the user's to perform when reached — see Step 3.
- **Initialize the Surfaced list.** Start empty; out-of-scope discoveries queue here; `/workbook-log` reads it at close.

One- or two-line preface: "Plan reviewed: N steps, M validations, X destructive ops will need confirmation — baseline captured for [sheets]. Starting execution." (No destructive ops → no baseline, and the preface drops the clause.)

## Step 3: Execute with checkpoints

Execute Steps in plan order. Report briefly per step. Run validations inline as affected steps complete.

**Per-step reporting format:**

```
Step N: [what was done] at [cell ref / range / sheet]. [Validation if triggered: check → pass/fail with numbers]
```

Examples:
- `Step 1: Inserted staging block at Forecast!H3:N15 with an ACCOUNTTURNOVER call for April.`
- `Step 2: Refreshed Velixo. Staging populated; 47 accounts × 1 period. Validation: H16 total = $1,234,567 → matches April GL ($1,234,567), PASS.`
- `Step 3: Updated Forecast!C47 from hardcoded $1.1M to =H16 (now $1.2M).`

Keep each line under ~150 characters where possible. Composite sub-actions (insert range + write formula + refresh) condense into the parent Step's line; a genuinely complex Step still gets exactly one report regardless of length — the plan's Step count is the contract.

**Validation timing:** run each Validation/Tie-out as soon as the last Step it depends on completes — catching breaks early is cheaper than catching them in the final tie-out. When the plan is **sliced**, that means closing each slice with its tie-out before opening the next — a slice isn't done until its checks pass. On failure, see Step 4.

**Handback steps:** when a Step the plan marked **Handback** is reached, pause and hand it to the user — what to do in desktop Excel and what to confirm ("run Velixo Refresh; tell me when the staging block shows April"). Don't simulate the result or run a dependent tie-out on pre-refresh numbers; resume when the user reports back (`LASTREFRESHDATE` confirms a refresh ran). If they can't get to Excel this session, offer `/workbook-handoff` — the pause point is exactly what it captures.

**Out-of-scope discoveries:** do **not** silently fix. Queue to Surfaced and report inline:

> Surfaced: Row 53 has a stale hardcoded value unrelated to this task. Queueing for a future cycle, not addressing now.

**Plan invalidation vs. minor adaptation:**

- **Wrong** (loop back to `/workbook-plan`): a Step's result would be incorrect as specified, a Step is no longer feasible, or an assumption the plan rested on is contradicted by discovery.

  > Plan Step N invalidated by [discovery]. Returning to `/workbook-plan` to revise.

  On a **sliced** plan, only the **remaining** slices are revised — the slices already closed tied out and stand; the re-plan picks up from the open one.

- **Everything else** (handle inline): sub-actions the plan didn't enumerate (refresh Velixo before a tie-out, expand a range by a row), minor adjustments where the Step is still right in spirit. Note significant ones for `/workbook-log` Deviations; trivial ones don't need a note.

**Destructive operations:** ALWAYS pause for confirmation when reached, regardless of whether the plan named it. See **Destructive operations** below.

**Workbook drift (rare):** if the workbook is materially different from what `/workbook-explore` reported (a sheet renamed, a range restructured outside the plan's scope), pause:

> Workbook state differs from `/workbook-explore`'s report: [specifics]. Re-explore [area], or proceed against current state?

This is the `/workbook-build` → `/workbook-explore` loop-back. Capture in Deviations.

## Step 4: Handle validation failure (when it happens)

If a validation fails, pause and surface the specific failure:

> Validation FAILED at Step N: [check] expected [target with number], got [actual with number]. Delta [delta].

Then present three options:

1. **Fix in place** — investigate and resolve (formula adjustment, missing data), then re-run the validation. Capture the fix and re-validation in Deviations.
2. **Loop back to `/workbook-plan`** — the failure shows the approach was wrong; revise and re-execute.
3. **Cancel and `/workbook-log` as Partial** — work was done but the tie-out can't resolve this cycle; `/workbook-log` records the partial state with the failure noted.

Wait for the user's choice. Don't decide on your own.

## Step 5: Final summary and invite `/workbook-log`

When all Steps are complete and all Validations have run (passed, failed-and-resolved, or noted as failed-deferred):

```
Build summary:
- Status: [Complete | Partial]
- Steps: N/N complete (or N/M if Partial)
- Validations: X/X passed (note any that failed and how resolved)
- Deviations: [brief list, or "none"]
- Surfaced: [out-of-scope items queued, or "none"]
- Sheets touched: [every sheet modified, plus external artifacts]

Ready for /workbook-log?
```

The `Status` line reads `Complete` when every Step landed and every Validation passed (or failed-and-resolved), `Partial` when work stopped with a check deferred or Steps unfinished. (`Cancelled` is `/workbook-log`'s vocabulary, not `/workbook-build`'s.) This mirrors the fields `/workbook-log` completes in the stub — including the completion state it reads directly — so close-out is mechanical.

**When a baseline exists** — the pre-flight scan flagged destructive ops and captured one — the closing line becomes **"Ready for `/workbook-review` → `/workbook-log`?"** instead: the same trigger that created the baseline arms the offer. `/workbook-review` is the fresh-eyes, changes-scoped review of what this build changed, best run in a fresh session while the baseline still stands; it is offered here, **never auto-run**. No baseline, no extra line.

## Destructive operations

ALWAYS pause for explicit user confirmation before a destructive operation, whether or not the plan named it. Plan-time approval is provisional; execution-time confirmation is the gate.

**Destructive:**
- Deleting rows, columns, or sheets
- Deleting or replacing existing formulas
- Overwriting non-empty cells with materially different content
- Clearing ranges that contain data
- Renaming sheets (breaks formulas referencing them)
- Removing named ranges other formulas may reference

**NOT destructive:**
- Writing to empty cells
- Adding new sheets, columns, or rows
- Refreshing data sources (Velixo, Power Query)
- Formatting changes (colors, fonts, borders, number formats)
- Adding charts, comments, or conditional formatting

**Confirmation format:**

> About to [action] at [target]. [What gets lost, what replaces it, whether reversible.] Confirm to proceed?

Example: "About to overwrite Forecast!C47 formula `=SUM(D47:G47)` with `=H16`. Existing returns $1.1M; new returns $1.2M. Confirm to proceed?"

Wait for an explicit yes. Treat ambiguous responses ("okay" with hesitation, "I think so") as not-yet-confirmed and ask again with sharper specifics. If the user declines, treat it as plan invalidation and loop back to `/workbook-plan`.

## Lightweight mode (no plan)

When `/workbook-build` is invoked without a plan in context, operate in lightweight mode — same discipline, no plan to deviate from.

On invocation with no plan, pause briefly:

> No plan in context. Run `/workbook-plan` first, or proceed without one (lightweight mode)?

If the user chooses lightweight mode:
- The user's request becomes the implicit plan (Goal = what they asked; Steps = what you'll do).
- Per-step reporting still applies — one line per material change.
- Validation discipline still applies — state what you'd verify, then verify it (visual checks count for non-quantitative tasks).
- Out-of-scope discoveries still go to the Surfaced list.
- Destructive operations still require explicit confirmation. Lightweight mode never auto-engages a baseline sheet — the per-op confirmation already shows before/after at one-cell grain.
- Loop-backs are simpler: hit something unanticipated → ask, rather than loop to `/workbook-plan`.

`/workbook-log` captures this as "direct execution, no formal plan" in the Plan field — the auto-omit rule doesn't apply here; the note is the signal that lightweight mode was used. Lightweight mode is for genuinely quick tasks. If you find yourself doing three or more material changes with cross-cutting validation, surface it: "This is growing past lightweight scope — pause and run `/workbook-plan`?"

## Bounded loop-backs

- **`/workbook-build` → `/workbook-plan`:** the plan is wrong (not just incomplete). When invoked, `/workbook-plan` runs against the existing stub (updates the Plan field in place rather than appending). See the test in Step 3.
- **`/workbook-build` → `/workbook-explore`:** the workbook state is materially different from what `/workbook-explore` reported. Rare; targeted re-explore, then resume.

Both are visible in chat and captured in `/workbook-log` Deviations. More than two loop-backs in one task means something structural is wrong — pause and reassess with the user.

## Content quality checklist

- [ ] Every plan Step has a per-step report
- [ ] Every Validation/Tie-out ran (passed, failed-and-resolved, or noted as failed-deferred)
- [ ] On a sliced plan, each slice was closed by its tie-out before the next opened; a loop-back revised only the remaining slices
- [ ] Every destructive op was explicitly confirmed before execution
- [ ] A baseline was captured iff the pre-flight scan flagged destructive ops — every touched sheet snapshotted before execution; none for an additive build
- [ ] Every **Handback** step paused for the user; no tie-out ran on pre-handback data
- [ ] Out-of-scope discoveries went to Surfaced, not silently done
- [ ] Deviations (adaptations, loop-backs) noted clearly enough for `/workbook-log` to capture
- [ ] Sheets touched list is complete
- [ ] Final summary leads with `Status: [Complete | Partial]` and matches the structure `/workbook-log` reads against
- [ ] Closing line named `/workbook-review` iff a baseline was captured — offered, never auto-run

## Edge cases

**Plan has a vague Validation/Tie-out ("verify it looks right"):** don't execute it as-is. Before reaching it, surface — "Plan validation for Step N is vague. Define a specific tie-out now, or accept visual inspection only?" Capture either way in Deviations.

**Plan has no Out of scope section:** treat as tight scope. If you hit creep pressure ("while you're in there…"), still queue to Surfaced — don't silently expand.

**A Step depends on a data refresh that fails (e.g. Velixo errors out):** pause. Surface the error. Three options: retry, troubleshoot before continuing, or cancel and `/workbook-log` as Partial. Don't proceed with a Step whose inputs aren't fresh.

**User invokes `/workbook-build` mid-execution to mean "keep going":** fine — it's the verb, not a one-shot trigger. Continue from the current point, don't restart.

**Plan references a sheet renamed since `/workbook-plan`:** workbook drift. Pause — either the rename wasn't noted (ask) or someone changed the workbook between plan and build (re-explore the area). Don't act against a stale reference.

**Build completes but the user has more work in mind that wasn't in the plan:** suggest `/workbook-log` for the completed work first, then a new `/workbook-plan` (or lightweight `/workbook-build`) for the rest. Don't append to a completed build — the task is the unit of record.

## What NOT to do

- **Silently fix things outside the plan.** Every out-of-scope discovery goes to Surfaced. No exceptions.
- **Skip validations because the work "looks done."** Tie-outs catch what eyeballing misses.
- **Execute destructive ops without confirmation, even if the plan listed them.** Plan-time approval is provisional; execution-time confirmation is the gate.
- **Batch per-step reports until the end.** Per-step reporting catches drift early and lets the user course-correct.
- **Decide on the user's behalf when validation fails.** Surface the failure, present options, wait.
- **Loop back without making the loop visible.** Silent transitions defeat the workflow.
- **Touch the stub row, Workbook Snapshot, or Agent sheet.** Those belong to `/workbook-log`.
- **Treat lightweight mode as license to skip discipline.** Same checkpoints, same Surfaced list, same destructive-op confirmation.
