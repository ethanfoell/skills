---
name: workbook-plan
description: Draft a structured six-section plan (Goal, Approach, Steps, Validation/Tie-outs, Open Questions, Out of Scope) before executing work in an Excel finance workbook, and write the In-progress stub to the Audit Log. The Validation/Tie-outs section is the keystone — every change gets an explicit this-equals-X / sums-to-Y / ties-within-$Z check, not a hand-wave that the numbers look right. Conditionally composes `/excel-finance-workbooks` and `/velixo-formulas`. The workbook loop's planning phase.
disable-model-invocation: true
---

# /workbook-plan

The second phase of the `/workbook-explore` → `/workbook-plan` → `/workbook-build` → `/workbook-log` loop. Drafts a structured strategy the user reviews before `/workbook-build` executes, and writes a **stub row** to the Audit Log — the durable signal a task is in-flight, and the anchor of the stub lifecycle: `/workbook-build` reads it, `/workbook-log` completes it in place.

`/workbook-plan` is **opt-in**: trivial one-line tasks skip it and go straight to `/workbook-build` (lightweight mode) or just get done. It earns its keep on multi-step work, refactors, and structural changes — anywhere going the wrong direction costs more than the plan does.

## When to use

Invoke when the task is multi-step, structural, or non-obvious enough that the wrong direction wastes real time, or when you want to think an approach through before executing — including when a `/workbook-build` cycle flagged its plan as invalidated and looped back here. Skip it for:
- One-line fixes (use `/workbook-build` lightweight mode, or just do the work).
- Pure orientation (use `/workbook-explore`).
- Closing out a task (use `/workbook-log`).
- Folders or filing systems (use `/folder-plan`).

## How this fits

- `/workbook-explore` has typically oriented the workbook earlier this session — but `/workbook-plan` can proceed without it (flag the gap, let the user decide).
- `/workbook-plan` drafts the six-section plan in chat, takes revisions, then writes the In-progress stub when finalized. Readiness for the next phase is signaled by invoking `/workbook-build` — no separate approval gate.
- `/workbook-build` executes against the plan; `/workbook-log` completes the stub at task close.

The plan lives in chat; the stub is the persistent breadcrumb. If the session ends or the task is abandoned, the next `/workbook-explore` detects the lingering In-progress stub and prompts resolution. `/workbook-plan` does **not** touch the Workbook Snapshot — that's `/workbook-log`'s at task close.

## Step 1: Quick checks before drafting

Four fast checks — signals to surface, not gates:

1. **In-progress stub in the Audit Log?** Read it for any In-progress block. If it's **this** task (same goal — e.g. a `/workbook-build` → `/workbook-plan` loop-back), you'll update that stub in Step 5, not append a new one. If it's a **different** task, ask once: "Existing in-progress task: '[title]'. Continue it, start fresh and cancel the old, or defer until it resolves?"
2. **Did `/workbook-explore` run this session?** Look for a state-check earlier in chat. If not, note it briefly ("No `/workbook-explore` this session — proceeding from current context; say if you want one first") and proceed.
3. **Are the shaping decisions settled?** If the task rests on unresolved design choices — *whether* to restructure or patch, which block is the source of truth, whether two sheets should merge — point upstream rather than deciding inline:

   > These shaping decisions aren't settled yet. `/grill-with-files` is the place to resolve them against what's actually in the workbook, then come back to plan.

   The interrogation is externalized to `/grill-with-files` — **a pointer, not a copy.** Don't run a decision-interview inside `/workbook-plan`. If the decisions are settled (or the user says proceed anyway), go straight to drafting.
4. **Is this one unit of work, or a multi-session feature?** If the task is actually a multi-session feature — many units, spanning sessions, the kind of thing that wants a spec and independent tickets — it's bigger than one plan. Point up the stairs rather than planning it all here:

   > This looks like a multi-session feature, not one unit of work. Shape it up the stairs — `/grill-with-files → /to-spec → /to-tickets` — the spec lands on the workbook's **Spec sheet**, the tickets on its **Tickets sheet** — then run the workbook loop (`/workbook-explore → /workbook-plan → /workbook-build → /workbook-log`) per ticket. If the way to the destination isn't visible yet — too big **and** foggy — chart it first with `/wayfinder` — the map lives on the workbook's **Tickets sheet**.

   A pointer, not a takeover: `/workbook-plan` stays the lighter sibling that plans a single unit; it **never writes the spec itself**, and a task going up the stairs gets **no In-progress stub** — its work lives on the Tickets sheet, not as an Audit Log block. If it really is one unit (or the user says plan it here anyway), go straight to drafting.

## Step 2: Determine reference-skill loads

Conditionally compose the model-invoked references — default is don't-load; loading is opt-in on signals. Announce any load briefly ("Loading `/velixo-formulas` — this plan involves Velixo refreshes"). Transparency, not ceremony.

- **Compose `/velixo-formulas`** when any Velixo/ACU function is in the workbook (ACCOUNTTURNOVER, ACCOUNTSANDSUBACCOUNTSWITHHISTORY, GI, GIFILTER, ACU.QUERY, …), the user mentions Velixo/Acumatica, or the plan touches refresh logic, new VLX/ACU formulas, GI changes, or period parameters.
- **Compose `/excel-finance-workbooks`** when the plan involves structural decisions — new sheets, formula-architecture changes (source-of-truth design, hardcode-to-driver refactors), cross-sheet logic, workbook-wide refactoring.
- **Don't load** for "add a column" / "fix this formula" tasks, coworker workbooks that don't follow the user's standards, or pure formatting.

## Step 3: Draft the six-section plan

Draft in chat. Sections can be brief, but **always include every header** — even when it's "none." The structure is the contract `/workbook-build` reads against.

**1. Goal** — one or two lines: what "done" looks like, concrete enough to recognize completion.
- Good: "Q3 forecast row 47 reflects April actuals; Summary!A1 ties to GL within $500." Bad: "Update the forecast."

**2. Approach** — the strategy in plain language: overall direction and key choices, not a step list.
- Good: "Pull April GL via Velixo into a staging block on Forecast, drive row 47 from that, retire the hardcoded prior estimate." Bad: "Use Velixo and fix the formula."

**Order a multi-unit task as vertical slices.** When the task spans multiple homogeneous units across multiple layers — twelve months, a set of accounts or entities, each needing source data → formulas → presentation — replication-before-validation is the live risk: the horizontal shape (all inputs, then all formulas, then all outputs, one tie-out at the end) copies a wrong formula twelve-months-wide before any check fires. Prefer slicing into thin end-to-end units (a *tracer bullet* through the workbook's layers): **one unit — one month, one account, one entity — through every layer, closed by its own tie-out** before the next opens, so a wrong direction surfaces after the first unit, not after all of them. For work without that replication risk — a two-cell fix, a single-unit change — the horizontal flat step list is the named default; don't slice flat work.

**3. Steps** — ordered, numbered actions `/workbook-build` will execute, each one concrete with a target (sheet/range). No composite steps that bury sub-actions.
- Good: 1. Insert staging block at Forecast!H3:N15 with a Velixo ACCOUNTTURNOVER call for April. 2. Refresh and confirm it populates. 3. Update Forecast!C47 to reference staging. 4. Verify Summary!A1 ties to GL. Bad: 1. Set up Velixo and update the forecast and check totals.

When sliced (per the Approach), group the numbered Steps into slices — one unit end-to-end per slice, ordered so each slice's tie-out closes before the next opens. For flat work the plain numbered list stands; don't group.

**Write a step only a human in desktop Excel can perform as a handback step.** The Velixo data refresh above all: it fires from the ribbon or Velixo's VBA API, in desktop Excel with Velixo loaded — neither reachable from a Claude surface. Lead the step with **Handback**, state the prerequisite at the step (not in a preamble), and name what to confirm: "Handback — requires you in desktop Excel with the licensed Velixo connection: run Refresh, confirm the staging block populates." `/workbook-build` pauses there for the user rather than pretending the step ran.

**4. Validation / Tie-outs — the keystone.** **This is the finance-specific keystone.** Every meaningful change needs an explicit "this should match X / sum to Y / tie within $Z" check. Without it, `/workbook-build` pattern-matches to "task complete" and skips verification. A tie-out's target comes from outside the cells it checks — the GL, a bank statement, a prior close, the issue's acceptance criteria — never recomputed from the same cells the plan populates; a check that can only agree with the formulas it validates isn't a tie-out.
- Good: "Staging block total at H16 must equal April GL net activity from Acumatica (~$1.2M)." / "Forecast!C47 should change from $1.1M to ~$1.2M; full-year Summary!A1 should move by the same delta within rounding." Bad: "Verify the numbers look right."

For non-quantitative tasks (renames, chart additions, formatting), validation is **still required** — just visual: "Chart renders without errors, axis labels read cleanly, no broken references." Don't drop the section.

When the plan is sliced (per the Approach), these checks run at **each slice boundary** — a slice isn't closed until its tie-out passes — not only in a final workbook-wide tie-out. Slicing changes *when* the checks fire, not *what* they are.

When the task traces to a ticket (it came down the stairs from `/to-tickets`), seed this section from the ticket's **acceptance criteria** — the spec flows into the tie-outs at plan time, and `/workbook-log` checks Done against the same criteria at close. A task with no ticket gets no extra ceremony.

**5. Open questions** — anything to resolve before `/workbook-build`, or assumptions flagged as known unknowns. If unresolved after one prompt, note that `/workbook-build` proceeds on the assumption ("defaulting to Branch 'All' if no response"). If genuinely none, write "Open questions: none."

**6. Out of scope** — the explicit list of what `/workbook-build` will **not** do this cycle: the stop signal against the "while you're in there…" creep that's constant in finance work ("Not retiring the old prior-estimate column — only updating row 47"). Write "none" only for very tight tasks — tight scoping is the norm.

## Step 4: Present and invite revisions

Surface the plan in chat. End with an open invitation, not an approval gate:

> Anything to adjust before `/workbook-build`?

Iterate and re-present as needed — no "type YES to approve" friction. When the user signals readiness (by invoking `/workbook-build`, or saying "looks good" / "proceed"), move to Step 5.

If the user wants to pause and pick up later, suggest `/workbook-handoff` to capture the plan durably across sessions. **Optional durable save:** if the user explicitly asks for the plan as a sheet deliverable (rare — the stub + chat is usually enough), write a "Plan-[short-title]" sheet with the six sections and note it for `/workbook-log`'s Sheets touched.

## Step 5: Write the stub row to the Audit Log

The stub is the durable in-flight signal `/workbook-log` completes in place at close. Its format — block header, the In-progress status, the field rows — is defined in the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md`, reached via contract pointer.

**Locate or create the Audit Log.** If none exists, create the title rows (1–2) the way `/workbook-onboarding` does, then leave the Workbook Snapshot for `/workbook-log`; `/workbook-plan` writes header + stub only.

**Handle existing stubs:**
- **This task** (loop-back): update the existing stub's Plan field with the revised summary — don't append a new block.
- **Different task** (orphaned In-progress): should have been resolved in Step 1; if not, mark it Cancelled "Superseded by new task" before writing the new stub.
- **None:** append a new stub block at the end.

**The stub** uses the **In-progress** status with just two field rows: Goal (the plan's Goal, one line) and Plan (a compressed 2–3-line Approach + key-Steps summary — **not** the full plan, which lives in chat). Done, Validation, Deviations, Surfaced, and Sheets touched are added by `/workbook-log` at close. Block layout, status palette (dot + word, the status rail), and field-row formatting all follow the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md`.

## Step 6: Confirm and invite `/workbook-build`

Tell the user briefly: stub written at row N, status In-progress; and which reference skills `/workbook-build` will inherit, if any. Then: "Ready for `/workbook-build`?"

## Bounded loop-back to `/workbook-explore`

If during planning you hit context you can't fill in ("I need to see the Detail tab before I can specify Step 3"), pause for a targeted re-explore, then resume:

> Plan needs more context on [area]. Running a targeted re-explore on [Detail tab], then resuming `/workbook-plan`.

Bounded, visible in chat, captured in the eventual `/workbook-log` Deviations. More than one loop-back in a single `/workbook-plan` means upstream exploration was insufficient — surface it.

**`/logic-audit` for logic-heavy refactors:** if the plan involves refactoring formula logic the user doesn't fully understand (complex SUMPRODUCT, opaque filters, cross-sheet rules), suggest `/logic-audit` before `/workbook-build` — a parallel workflow that decodes existing logic, not a loop phase. `/workbook-explore` is the primary suggester; surface it here too when the need only becomes clear during planning (most often in a `/workbook-build` → `/workbook-plan` loop-back where the refactor scope sharpened).

## Content quality checklist

- [ ] Goal is concrete enough to recognize completion
- [ ] Approach is a strategy, not a step list
- [ ] Steps are numbered, atomic, each with a sheet/range target
- [ ] A multi-unit task *with replication risk* is ordered as vertical slices (each closed by its tie-out before the next); flat work stays horizontal
- [ ] Validation has specific numbers, tolerances, and tie-out targets — not "verify it looks right" — and targets independent of the cells they check
- [ ] A refresh-dependent (or otherwise human-only) step is written as a **Handback** step, its prerequisite stated at the step
- [ ] Ticket-traced task: Validation/Tie-outs seeded from the ticket's acceptance criteria (no ticket → nothing extra)
- [ ] Open questions are answered, or flagged as proceeding-on-assumption
- [ ] Out of scope lists at least one item if the task could creep
- [ ] Reference skills loaded only if their triggers fired — no front-loading
- [ ] Unsettled shaping decisions routed to `/grill-with-files`, not interviewed inline
- [ ] A multi-session feature is routed up the stairs (`/grill-with-files → /to-spec → /to-tickets`), not planned here as one unit
- [ ] Stub Goal matches the plan's Goal exactly; stub Plan is 2–3 lines, not the full plan

## Edge cases

**No `/workbook-explore` ran this session:** flag it; proceed if the user wants (one-time scratch work, a well-known file, or a coworker workbook they've already oriented to don't need it).

**Task already mid-execution:** either a `/workbook-build` → `/workbook-plan` loop-back, or the user worked ad-hoc and wants to formalize. Capture work already done as Steps marked "Already done," then plan the remainder.

**User describes a task but doesn't clearly want a plan:** ask once — "Write this up as a `/workbook-plan`, or just do it with `/workbook-build`?" Trivial tasks benefit from skipping.

**Validation isn't quantitative:** make it visual ("Chart renders without errors and reads cleanly") — still a check, never dropped.

**Open questions unanswered after one prompt:** don't keep asking. Note the assumption ("defaulting to X if no response by build time") and proceed; the user can revise at the invitation step.

**An In-progress stub from days or weeks ago:** the user has probably forgotten it. Surface it ("In-progress task from [date]: '[title]'. Still active, or cancel and start fresh?") and don't proceed without an answer.

## What NOT to include in the plan

- AI deliberation ("I considered X then chose Y") — capture decisions, not the path to them.
- Step-by-step Excel mechanics ("click Insert → Function → SUM") — Steps are conceptual with targets.
- Padding sections — say "none" per the section's rule.
- Speculation about future tasks — those belong in the Surfaced list at `/workbook-log` time.
- Assumed preferences not actually stated — ask once or note as an Open Question.
- The full plan in the stub's Plan field — that's a 2–3-line compressed summary; the full plan stays in chat.
