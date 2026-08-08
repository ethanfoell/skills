---
name: folder-plan
description: Draft a structured, chat-first plan before real, multi-file work in a folder — a six-section plan (Goal, Approach, Steps, Validation, Open Questions, Out of Scope) to review before `/folder-build` runs. Validation is the keystone: the folder checks that prove the work sound (links resolve, a build passes, cross-references intact, counts tie). Ends by offering to park the plan (`/handoff`) or run it (`/folder-build`); routes unsettled shaping decisions to `/grill-with-files`, not an inline interview. The folder loop's planning phase.
disable-model-invocation: true
---

# /folder-plan

The second phase of the `/folder-explore` → `/folder-plan` → `/folder-build` → `/folder-log` loop. Produces a structured six-section plan in chat the user reviews before `/folder-build` executes. **Chat-first**: it writes no durable stub. A plan changes nothing on disk, so there's nothing for the folder's history layer to record yet (single-source history — one layer per folder, and the plan isn't an event in it); the durable in-flight signal is delegated instead (Step 4).

`/folder-plan` is **opt-in**: trivial or one-file tasks skip it and go straight to `/folder-build` (lightweight mode) or just get done. It earns its keep on multi-file reorganizations, structural changes, and cross-tree doc/skill edits — anywhere going the wrong direction costs more than the plan does.

## When to use

Invoke when the task is multi-file, structural, or non-obvious enough that the wrong direction wastes real time, or when you want to think through an approach before editing — including when a `/folder-build` cycle flagged its plan as invalidated and looped back here. Skip it for:
- One-file or one-line fixes (use `/folder-build` lightweight mode, or just do the work).
- Pure orientation (use `/folder-explore`).
- Closing out work (use `/folder-log`).
- Excel workbooks (use `/workbook-plan`).

## How this fits

- `/folder-explore` has typically oriented the folder earlier this session — but `/folder-plan` can proceed without it (flag the gap, let the user decide).
- `/folder-plan` drafts the plan, takes revisions, then **offers two branches**: park it (`/handoff`) or run it (`/folder-build`). Readiness is signaled by invoking `/folder-build` — there's no separate approval gate.
- `/folder-build` executes against the plan; `/folder-log` writes the task record to the folder's history layer at task close.

## Step 1: Quick checks before drafting

Three fast checks — signals to surface, not gates:

1. **Did `/folder-explore` run this session?** Look for a state-check earlier in chat. If not, note it briefly ("No `/folder-explore` this session — proceeding from current context; say if you want a state-check first") and proceed. Don't block.
2. **Are the shaping decisions settled?** If the task rests on unresolved design choices — *which* way to reorganize, what the canonical structure should be, whether two areas should merge — point upstream rather than deciding inline:

   > These shaping decisions aren't settled yet. `/grill-with-files` is the place to resolve them against what's actually in the folder, then come back to plan.

   The interrogation is externalized to `/grill-with-files` (or `/grill-me`) — **a pointer, not a copy.** Don't run a decision-interview inside `/folder-plan`. If the decisions are settled (or the user says proceed anyway), go straight to drafting.
3. **Is this one unit of work, or a multi-session feature?** If the task is actually a multi-session feature — many units, spanning sessions, the kind of thing that wants a spec and independent tickets — it's bigger than one plan. Point up the stairs rather than planning it all here:

   > This looks like a multi-session feature, not one unit of work. Shape it up the stairs — `/grill-with-docs → /to-spec → /to-tickets` — then run the folder loop (`/folder-explore → /folder-plan → /folder-build → /folder-log`) per ticket. If the way to the destination isn't visible yet — too big **and** foggy — chart it first with `/wayfinder`.

   A pointer, not a takeover: `/folder-plan` stays the lighter sibling that plans a single unit; it **never writes the spec itself.** If it really is one unit (or the user says plan it here anyway), go straight to drafting.

## Step 2: Draft the six-section plan

Draft in chat. Sections can collapse to one line for light work, but **always include every header** — the structure is the contract `/folder-build` reads against.

If the folder has a `CONTEXT.md`, use its **canonical terms** in the plan — not the `_Avoid_` synonyms — so the plan, the build, and the commit speak one vocabulary. If the work coins or sharpens a term, don't author the glossary inline: **note it for `/folder-log`** to record via `/domain-modeling`.

**1. Goal** — one or two lines: what "done" looks like, concrete enough to recognize completion.
- Good: "The twelve loose June exports live under `2026/06/`; the README Layout lists them; `consolidate_exports.py` still runs clean."
- Bad: "Clean up the folder."

**2. Approach** — the strategy in plain language: the overall direction and key choices, not a step list.
- Good: "File the loose exports into `2026/06/`, re-tag the two PRs to `proposed-change`, touch no script inputs so `consolidate_exports.py` output is unchanged."
- Bad: "Reorganize the files and fix the tags."

**Order a large reorg as vertical slices.** When the reorg is big enough to have intermediate states — a move-everything-first pass would leave references broken across many files at once — prefer slicing it into thin end-to-end units (a *tracer bullet* through the folder's layers: **move + reference-rewire + validation**), each closed by its own validation before the next opens — so a wrong direction surfaces after the first slice, not after all of them. For an irreducible few-file move with no meaningful intermediate state, the horizontal **move-all-then-fix-all-then-build-once** shape is the named default — don't slice flat work. Prefactor either way: do `/folder-build`'s setup moves first (create the parent dirs, stage the `_archive/` landing zone, checkpoint before a destructive step) — make the change easy, then make the easy change.

**3. Steps** — ordered, numbered file operations, each with a **path as its target**. No composite steps that bury sub-actions.
- Good: 1. Create `2026/06/` and move the 12 loose exports in. 2. Re-tag `PR_x.md`/`PR_y.md` headers to `Rung: proposed-change`. 3. Update the README Layout to list `2026/06/`. 4. Re-run `consolidate_exports.py` from the folder root.
- Bad: 1. Reorganize everything, fix the tags, and rebuild.

When sliced (per the Approach), group the numbered steps into slices, ordered so each slice's validation closes before the next opens. For flat work the plain numbered list stands; don't group.

**A step that creates or materially edits a workbook names its kind: durable or disposable.** The test: will a future session open this workbook to *work on* it, or only to read it? **Durable** takes the four-sheet contract — `/folder-build` scaffolds it and writes its Audit Log entry as part of the step. **Disposable** (a one-shot output, a script-regenerated intermediate) takes none — the generating script and the folder's record are its record; scaffolding a regenerated file wipes its Audit Log every run. A wrong guess is cheap: `/workbook-onboarding` retrofits. Compose `/excel-finance-workbooks` for the design knowledge behind such a step (and `/velixo-formulas` when Velixo functions are in play). If a workbook sub-deliverable earns its own plan/build/log cycle, name the route — "run `/workbook-plan`" — rather than burying a workbook project inside one folder step.

**4. Validation — the keystone.** Without it, `/folder-build` pattern-matches to "done" and skips verification. This section is the **single canonical** statement of the folder checks that prove the work sound:

- **Links resolve** — relative links in the docs still point at real files after the moves.
- **A build passes** — if the folder has a build or generator script, it runs and emits the expected outputs, no errors or warnings.
- **Cross-references intact** — scripts with hardcoded paths, workbook external links, and inter-doc references still find their targets.
- **Counts tie** — files in == files out (N moved, 0 lost); skill count unchanged unless the task adds/removes one.

A workbook-creating step's validation is additionally **tie-out-shaped**: an explicit this-equals-X / sums-to-Y / ties-within-$Z check on the numbers inside the deliverable — not only that the file exists and the counts tie.

When the plan is sliced (per the Approach), these same checks run at **each slice boundary** — a slice isn't closed until its validation passes — not only in a final sweep. Slicing changes *when* they run, not *what* they are.

State the specific checks, not "check it looks right":
- Good: "All relative links in `README.md` resolve — no dead links after the moves." / "`consolidate_exports.py` emits `combined_2026-06.csv` clean, no warnings." / "File count before/after matches: 3 moved, 0 lost."

For a non-mechanical task (a pure reorganization with nothing to build), Validation is **still required** — make it structural: "Every moved file lands in the documented area; no orphaned references; the README Layout matches the tree." Never drop the section.

When the task traces to a ticket (it came down the stairs from `/to-tickets`), seed this section from the ticket's **acceptance criteria** — the spec flows into the keystone at plan time, and `/folder-log` checks Done against the same criteria at close. A task with no issue gets no extra ceremony.

**5. Open questions** — anything to resolve before `/folder-build`, or assumptions flagged as known unknowns. If unresolved after one prompt, note that `/folder-build` proceeds on the assumption ("defaulting to `docs/` if no response"). If genuinely none, write "Open questions: none."

**6. Out of scope** — the explicit list of what `/folder-build` will **not** do this cycle: the stop signal against the "while you're in there…" creep that's constant in folder work ("Not touching `account-snapshots/`. Not renaming any skill. Not hand-editing `dist/`"). Write "none" only in the rare case nothing could creep — tight scoping is the norm.

## Step 3: Present and invite revisions

Surface the plan in chat. End with an open invitation, not an approval gate:

> Anything to adjust before `/folder-build`?

Iterate on revisions and re-present as needed — no "type YES to approve" friction. When the user signals readiness (by invoking `/folder-build`, or saying "looks good" / "proceed"), move to Step 4.

## Step 4: Offer to park or run (the in-flight signal)

A plan changes no files, so the working tree stays clean between plan and build — there is **no durable in-flight signal yet**. Don't invent a stub file to fix that; **delegate the signal** by offering two branches:

- **Park for later → `/handoff`** — write a durable handoff into the folder as a `future-work/` item carrying the rung header (idea/task), which `/folder-explore` and `/folder-pickup` detect next session. Write it **open**: a parked plan is unsettled work, so pose the question and point at the files — leads to verify, not a conclusion to inherit. (A top-level `HANDOFF.md` works for a one-off pause.)
- **Run now → `/folder-build`** — executes the plan and dirties the working tree, and **a dirty tree is itself the in-flight signal** `/folder-explore` and `/folder-pickup` already hunt for.

Either way the in-flight state lands as a signal those skills already detect — no new detection is invented. If the user is ready to run:

> Ready for `/folder-build`?

## Bounded loop-back to `/folder-explore`

If during planning you hit context you can't fill in ("I need to see what's actually in `docs/` before I can specify Step 3"), pause for a targeted re-explore, then resume:

> Plan needs more context on [specific area]. Doing a targeted re-explore of [area], then resuming `/folder-plan`.

Bounded, visible in chat, and captured in the eventual `/folder-log` Deviations. More than one loop-back in a single `/folder-plan` means upstream exploration was insufficient — surface that.

## Content quality checklist

- [ ] Goal is concrete enough to recognize completion
- [ ] Approach is a strategy, not a step list
- [ ] Steps are numbered, atomic, each with a **path** target
- [ ] A large reorg *with intermediate states* is ordered as vertical slices (each closed by its validation before the next); flat work stays horizontal
- [ ] Validation names the keystone's specific checks (Step 2 §4), not "looks right"
- [ ] A step whose deliverable is a workbook names it durable or disposable; durable carries the four-sheet obligation and a tie-out-shaped validation; a workbook earning its own cycle routed to `/workbook-plan`, not folded into one step
- [ ] Issue-traced task: Validation seeded from the issue's acceptance criteria (no issue → nothing extra)
- [ ] Open questions are answered, or flagged as proceeding-on-assumption
- [ ] Out of scope lists at least one item if the task could creep
- [ ] No durable stub file written — the plan lives in chat (Step 4)
- [ ] Ended by offering to park (`/handoff`) or run (`/folder-build`)
- [ ] Unsettled shaping decisions routed to `/grill-with-files`, not interviewed inline
- [ ] A multi-session feature is routed up the stairs (`/grill-with-docs → /to-spec → /to-tickets`), not planned here as one unit
- [ ] Uses the folder's `CONTEXT.md` canonical terms (not `_Avoid_` synonyms); any coined term queued for `/folder-log`, not authored inline

## Edge cases

**No `/folder-explore` ran this session:** flag it; proceed if the user wants. Some tasks don't need it (a folder you already know, a one-off).

**Task is already mid-execution:** the user has been working ad-hoc and wants to formalize, or a `/folder-build` → `/folder-plan` loop-back is happening. Capture work already done as Steps marked "Already done," then plan the remainder.

**User describes a task but doesn't clearly want a plan:** ask once — "Write this up as a `/folder-plan`, or just do it with `/folder-build`?" Trivial tasks benefit from skipping. Don't force the workflow.

**Non-mechanical task with nothing to build or link-check:** Validation becomes structural (Step 2 §4's non-mechanical case) — still a check, never dropped.

**Open questions go unanswered after one prompt:** don't keep asking. Note the assumption ("defaulting to X if no response by build time") and proceed; the user can revise at the invitation step.

**Parking the plan for later:** Step 4's park branch — a `future-work/` item (rung-tagged idea/task) via `/handoff`, written **open**. The offer to run `/folder-build` now is unaffected.

## What NOT to include in the plan

- AI deliberation ("I considered X then chose Y") — capture decisions, not the path to them.
- Procedural file-manager mechanics ("drag this into that folder") — Steps are conceptual operations with path targets.
- Padding sections — say "none" per the section's rule.
- Speculation about future tasks — those belong in the Surfaced list at `/folder-log` time.
- A durable `PLAN.md` stub — the plan is chat-first by design (Step 4).
