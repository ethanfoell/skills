---
name: folder-build
description: Execute a folder plan with discipline — per-step reporting, inline validation against the folder keystone (links resolve, a build passes, cross-references intact, counts tie), destructive-op confirmation (preferring archive-by-move), and a Surfaced list for out-of-scope discoveries. Operates in lightweight mode when no plan is in context. The folder loop's execution phase.
disable-model-invocation: true
---

# /folder-build

The third phase of the `/folder-explore` → `/folder-plan` → `/folder-build` → `/folder-log` loop. Executes a folder plan with guardrails, kept deliberately **thin**: in a folder, "the work" is the agent's direct file operations — `/folder-build` doesn't bolt on heavy step-by-step machinery, it adds the **four guardrails** that make a build phase beat just-doing-it. Drift, scope creep, silent destructive operations, and skipped verification are the failure modes this phase exists to prevent.

1. **Per-step reporting** — one line per material change (the visibility that justifies the phase).
2. **Inline validation against the folder keystone** — links resolve, a build passes, cross-references intact, counts tie.
3. **Destructive-op confirmation** — pause before overwriting or deleting, and **prefer archive-by-move**.
4. **Surfaced list** — out-of-scope discoveries queued, never silently done.

Those four checks in guardrail 2 are the keystone `/folder-plan` §4 defines — its canonical home. This short standalone enumeration keeps `/folder-build` legible when it runs in lightweight mode with no plan in context.

## When to use

Invoke when a `/folder-plan` is finalized and you're ready to execute, when a `/folder-build` → `/folder-plan` loop produced a revised plan, or when you want to do folder work directly without a plan first (lightweight mode — see below). Skip it for:
- Orientation only (use `/folder-explore`).
- Planning only (use `/folder-plan`).
- Closing out a task (use `/folder-log`).
- Excel workbooks (use `/workbook-build`).

## How this fits

- `/folder-plan` drafted the six-section plan in chat (chat-first — it writes no stub file).
- `/folder-build` executes the Steps in order, runs Validation as affected Steps complete, pauses on destructive ops, and queues out-of-scope finds to Surfaced.
- When execution finishes, `/folder-build` produces a structured summary `/folder-log` reads against; the user invokes `/folder-log` to close out — it writes the **task record to the folder's history layer**.

`/folder-build` does only the planned file work. It does **not** write the history, refresh the README Status, or propose CLAUDE.md rules — those all belong to `/folder-log`. (Its one `LOG.md` touch is opening the file-based **in-flight stub** at execution start — the signal, not the record; Step 2.)

## Step 1: Verify plan and prerequisites

- **Is there a plan in chat?** Identify the six-section plan from a recent `/folder-plan`. If Validation is vague ("looks right"), surface that **before** executing, not after. If no plan is in context, see **Lightweight mode** — don't block.
- **No plan stub exists.** `/folder-plan` writes none — in-flight begins at execution, not at planning. This build opens the signal itself (Step 2): the dirty working tree on a Git-backed folder, an open `LOG.md` stub on a file-based one; `/folder-log` resolves it at close.

## Step 2: Pre-flight scan, then open the in-flight signal

Quickly scan the plan before executing:

- **Map Validation to Steps.** Which Steps does each check depend on? Run each validation as the **last Step it depends on** completes — not at the end. If `/folder-plan` ordered the work as **vertical slices**, the slice boundaries are those checkpoints: **close each slice with its validation before opening the next**, so a broken slice halts the build before the next one starts.
- **Flag destructive operations.** Identify any Step that overwrites, deletes, or moves a file onto an existing path (see **Destructive operations**). These pause for confirmation when reached.
- **Initialize the Surfaced list.** Start empty; out-of-scope discoveries queue here; `/folder-log` reads it at close.
- **Open the in-flight signal** — dispatch on the folder's recorded history layer (the CLAUDE.md standing line). On **Git** (the default): nothing to write — the dirty tree this build is about to create *is* the signal. On a **file-based folder**: before the first file operation, write an **open stub entry** at the top of `LOG.md` — the standard entry header plus an explicit in-progress status line:

  ```
  ## YYYY-MM-DD — <task title>

  **In progress** — opened by /folder-build; /folder-log completes this entry at close.
  ```

  `/folder-log` completes the stub **in place** at close — never write a second entry for the same task, and never remove the stub yourself. If `LOG.md`'s top entry is *already* an open stub, that's abandoned in-flight work from a prior task — surface it and ask before starting; don't overwrite it or stack a second stub.

One- or two-line preface: "Plan reviewed: N steps, M validations, X destructive ops will need confirmation. Starting."

## Step 3: Execute with checkpoints

Execute Steps in plan order. Report briefly per step. Run validations inline as affected steps complete.

**Per-step reporting format:**

```
Step N: [what was done] at [path]. [Validation if triggered: check → pass/fail]
```

Examples:
- `Step 1: Created 2026/06/ and moved the 12 June exports into it (git mv).`
- `Step 2: Re-ran consolidate_exports.py → combined_2026-06.csv written from 12 exports, no warnings. PASS.`
- `Step 3: Updated README Layout to list 2026/06/. Validation: all relative links resolve, PASS.`

Keep each line tight. Composite sub-actions (create a parent dir, then move into it) condense into the parent Step's line.

**Speak the folder's vocabulary.** If the folder has a `GLOSSARY.md`, use its canonical terms in per-step reports and the Surfaced list (not the `_Avoid_` synonyms). If execution coins or sharpens a term, **queue it for `/folder-log`** to record via `/domain-modeling` — don't write the glossary mid-build.

**A step's deliverable is a workbook:** compose `/excel-finance-workbooks` (and `/velixo-formulas` when Velixo functions are in play) if the plan didn't already load them. The record obligation attaches to the artifact, not the invoking loop: creating or materially editing a **durable workbook** (the plan names the kind) includes its four-sheet scaffolding and an Audit Log entry for what changed inside it, as part of the step — the folder's history layer records the task at folder grain; the workbook's own Audit Log records the in-file story. A **disposable** workbook gets no scaffolding — its generating script and the folder record are its record. If the plan didn't name the kind, apply the test (will a future session open it to work on it?) and note the call for `/folder-log` Deviations.

**Validation timing:** run each check as soon as the last Step it depends on completes — a broken link or a failed generator run is cheaper to catch mid-build than in a final sweep. When the plan is **sliced**, that means closing each slice with its validation before opening the next — a slice isn't done until its checks pass. On failure, see Step 4.

**Out-of-scope discoveries:** do **not** silently fix. Queue to Surfaced and report inline:

> Surfaced: `docs/old-spec.md` has a dead link unrelated to this task. Queued for a later cycle, not fixing now.

**Plan invalidation vs. minor adaptation:**

- **Wrong** (loop back to `/folder-plan`): a Step's result would be incorrect as specified, a Step is no longer feasible, or an assumption the plan rested on is contradicted by what's on disk.

  > Plan Step N invalidated by [discovery]. Returning to `/folder-plan` to revise.

  On a **sliced** plan, only the **remaining** slices are revised — the slices already closed validated and stand; the re-plan picks up from the open one.

- **Everything else** (handle inline): sub-actions the plan didn't enumerate (create a parent directory before moving into it), minor adjustments. Note significant ones for `/folder-log` Deviations; trivial ones don't need a note.

**Destructive operations:** ALWAYS pause for confirmation when reached, regardless of whether the plan named it. See **Destructive operations** below.

**Folder drift (rare):** if the folder is materially different from what `/folder-explore` reported (an area restructured, files already moved), pause:

> Folder differs from `/folder-explore`'s report: [specifics]. Re-explore [area], or proceed against current state?

This is the `/folder-build` → `/folder-explore` loop-back. Capture in Deviations.

## Step 4: Handle validation failure (when it happens)

If a validation fails, pause and surface the specific failure:

> Validation FAILED at Step N: [check] expected [X], got [Y].

Then present three options:

1. **Fix in place** — investigate, resolve (a missed path, a broken link, a build error), then re-run the validation. Capture the fix in Deviations.
2. **Loop back to `/folder-plan`** — the failure shows the approach was wrong; revise and re-execute.
3. **Stop and `/folder-log` as Partial** — work was done but the check can't pass this cycle; `/folder-log` records the partial state with the failure noted.

Wait for the user's choice. Don't decide on your own.

## Step 5: Final summary and invite `/folder-log`

When all Steps are complete and all Validations have run (passed, failed-and-resolved, or noted as failed-deferred):

```
Build summary:
- Status: [Complete | Partial]
- Steps: N/N complete (or N/M if Partial)
- Validations: X/X passed (note any that failed and how resolved)
- Deviations: [brief list, or "none"]
- Surfaced: [out-of-scope items queued, or "none"]
- Files touched: [paths added / moved / edited / archived]

Ready for /folder-log?
```

The `Status` line reads `Complete` when every Step landed and every Validation passed (or failed-and-resolved), `Partial` when work stopped with a check deferred or Steps unfinished. This mirrors the fields `/folder-log` records in its close-out record — including the completion state it reads directly — so close-out is mechanical.

## Destructive operations

ALWAYS pause for explicit user confirmation before a destructive file operation, whether or not the plan named it. Plan-time approval is provisional; execution-time confirmation is the gate.

**Prefer archive-by-move over deletion.** The folder loop's standing rule is **archive, don't delete**: move the file into `_archive/` (a rename) rather than removing it. This is both safer (recoverable) and more robust — a `rename` works even in sandboxed or synced environments, whereas an outright delete on a Cowork mount needs the file-delete permission granted (grant it once per session; see `/folder-log`). So the default resolution for "this file is in the way" is **move it to `_archive/`**, and an outright delete is the exception that needs its own confirmation.

**Destructive:**
- Deleting a file or directory
- Overwriting an existing file with materially different content
- Moving a file onto an existing path (clobbering it)
- Renaming a file that other scripts, workbook external links, or doc links reference
- Bulk-moving a tree that scripts or relative links depend on

**NOT destructive:**
- Creating new files or directories
- Writing to a new (empty) path
- Moving a file into `_archive/` (the archive-by-move itself — though confirm if it removes something other files reference)
- Re-running a generator (e.g. `consolidate_exports.py`) that rewrites its own output files
- Editing a file additively where the prior state is already committed

**Confirmation format:**

> About to [action] at [path]. [What's lost, what replaces it, whether it's recoverable / committed.] [Prefer archiving to `_archive/` instead?] Confirm to proceed?

Examples:
- "About to overwrite the README Layout section with the new tree. Prior version is committed (recoverable via git). Confirm?"
- "About to remove `future-work/old-note.md`. Per archive-don't-delete, I'd move it to `_archive/old-note_<date>.md` instead — ok?"

Wait for an explicit yes. Treat ambiguous responses as not-yet-confirmed and ask again with sharper specifics. If the user declines, treat it as plan invalidation and loop back to `/folder-plan`.

**Checkpoint before destruction:** before a destructive step, if the prior state isn't already committed, make a checkpoint commit first (on a file-based folder, a dated copy into `_archive/`) so the change is recoverable — the same recoverability floor `/folder-log` states.

## Lightweight mode (no plan)

When `/folder-build` is invoked without a plan in context, operate in lightweight mode. Same discipline; no plan exists to deviate from.

On invocation with no plan, pause briefly:

> No plan in context. Run `/folder-plan` first, or proceed without one (lightweight mode)?

If the user chooses lightweight mode:

- The user's request becomes the implicit plan (Goal = what they asked; Steps = what you'll do).
- The in-flight signal still opens (Step 2): on a file-based folder, write the open `LOG.md` stub before the first file operation — the user's request supplies the task title.
- Per-step reporting still applies — one line per material change.
- Validation discipline still applies — state what you'd verify, then verify it (structural/visual checks count for non-mechanical tasks).
- Out-of-scope discoveries still go to the Surfaced list.
- Destructive operations still require explicit confirmation, with archive-by-move preferred.
- Loop-backs are simpler: hit something unanticipated → ask, rather than loop to `/folder-plan`.

`/folder-log` closes it out like any task — mostly-empty fields are expected. Lightweight mode is for genuinely quick tasks. If you find yourself doing three or more material changes with cross-cutting validation, surface it: "This is growing past lightweight scope — pause and run `/folder-plan`?"

## Bounded loop-backs

- **`/folder-build` → `/folder-plan`:** the plan is wrong (not just incomplete). See the test in Step 3.
- **`/folder-build` → `/folder-explore`:** the folder state is materially different from what `/folder-explore` reported. Rare; targeted re-explore, then resume.

Both are visible in chat and captured in `/folder-log` Deviations. More than two loop-backs in one task means something structural is wrong — pause and reassess with the user.

## Content quality checklist

- [ ] On a file-based folder, the open `LOG.md` stub was written before the first file operation (lightweight mode included); on Git, no stub — the dirty tree is the signal
- [ ] Every plan Step has a per-step report
- [ ] Every Validation ran (passed, failed-and-resolved, or noted as failed-deferred)
- [ ] On a sliced plan, each slice was closed by its validation before the next opened; a loop-back revised only the remaining slices
- [ ] Every destructive op was explicitly confirmed; archive-by-move preferred over delete
- [ ] Out-of-scope discoveries went to Surfaced, not silently done
- [ ] A durable workbook created or materially edited got its four-sheet scaffolding and an Audit Log entry for the in-file changes; a disposable one got none
- [ ] Per-step reports and Surfaced list use the folder's `GLOSSARY.md` canonical terms; any coined term queued for `/folder-log`, not authored mid-build
- [ ] Deviations noted clearly enough for `/folder-log` to capture
- [ ] Files-touched list is complete
- [ ] Final summary leads with `Status: [Complete | Partial]` and matches the structure `/folder-log` reads against

## Edge cases

**Plan has a vague Validation ("looks right"):** don't execute it as-is. Before reaching it, surface — "Validation for Step N is vague — define a specific check (link resolves / build passes / count ties), or accept a visual inspection?" Capture either way in Deviations.

**Plan has no Out of scope section:** treat as tight scope. If you hit creep pressure ("while you're in there…"), still queue to Surfaced — don't silently expand.

**A Step depends on a generator that fails (e.g. `consolidate_exports.py` errors out):** pause. Surface the error. Three options: retry, troubleshoot before continuing, or stop and `/folder-log` as Partial. Don't proceed with a Step whose inputs aren't sound.

**User invokes `/folder-build` mid-execution to mean "keep going":** fine — it's the verb, not a one-shot trigger. Continue from the current point, don't restart.

**Plan references a path moved or renamed since `/folder-plan`:** folder drift. Pause — either the move wasn't noted (ask) or someone changed the folder between plan and build (re-explore the area). Don't act against a stale path.

**A delete fails with `Operation not permitted`:** on a Cowork mount that's the **ungranted file-delete permission**, not a dead environment — grant it once per session and retry. Usually the archive-by-move (a rename) sidesteps the need to delete at all. Don't abandon the step over it.

**Build completes but the user has more work in mind that wasn't in the plan:** suggest `/folder-log` for the completed work first, then a new `/folder-plan` (or lightweight `/folder-build`) for the rest. Don't append to a completed build — the task is the unit of record.
