---
name: workbook-review
description: A fresh-eyes, changes-scoped review of what a workbook build actually changed — the workbook substrate's `/code-review` analog. Reads the build's change object (the Audit Log block's footprint, plus the transient formula-text baseline sheets when a destructive build left them), enumerates the real diff against the builder's self-report (unreported changes are findings in themselves), and routes to `/formula-audit` and `/logic-audit` with a scope derived from the changes. Run it in a fresh session, between `/workbook-build`'s close and `/workbook-log`. Offered when a baseline exists; never auto-run.
disable-model-invocation: true
---

# /workbook-review

The workbook substrate's `/code-review` analog: a **changes-scoped, fresh-eyes review** of what a build actually changed — not a whole-workbook audit. It reads the **change object** the loop leaves behind, enumerates the real diff, checks it against the builder's self-report, and points the audits at exactly the cells the build touched. An **orchestrator over the audits**, not a third audit: `/formula-audit` and `/logic-audit` stay the finding engines; this skill decides where they look.

## When to use

Use when:

- A `/workbook-build` just closed with a baseline captured — its summary ended "Ready for `/workbook-review` → `/workbook-log`?" and you want the fresh-eyes pass before close-out.
- `/workbook-log` flagged Baseline sheets about to be cleared and you want the diff reviewed before its raw material goes.
- You want a build's changes verified by a session that didn't do the building.

Skip it for:

- A whole-workbook pre-trust check (before sending to a coworker, auditor, or boss) — run `/formula-audit` then `/logic-audit` directly; this skill reviews *changes*, not the workbook.
- The effort-complete moment (the last Tickets-sheet ticket just closed) — `/workbook-log` names the audits there; that's the whole-workbook grain.
- Reviewing a code branch or working tree → `/code-review`.

## Fresh session first

Run this in a **fresh session** (or a fresh add-in chat) whenever you can. Every input is durable in the workbook — the Audit Log block and the baseline sheets — so a brand-new session runs the review with zero handoff, and freshness is the point: the workbook substrate has no sub-agents to manufacture a second perspective the way `/code-review` does, so its only fresh-eyes mechanism is a session boundary, and only you can cross one. The same reasoning is why this skill is **offered, never auto-run** — a review run inside the build session is the builder's own context grading its own homework.

## The change object — two tiers

**Tier 1 — the footprint (always present).** The task's Audit Log block, read as a spatial object: the cell references in **Done** and the **Sheets touched** field once `/workbook-log` has completed it; the Goal + Plan stub (plus `/workbook-build`'s structured summary, when it's in context) before then. It converts the temporal question — *what changed since the build?* — into the spatial one — *these sheets and ranges* — which is exactly the scope grammar the audits already eat. Honest limit: the footprint is the **builder's self-report**, complete only where the log-writer reported. Block format per the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md`.

**Tier 2 — the baseline sheets (conditional).** When the build's destructive-op scan fired, `/workbook-build` left one `Baseline — [sheet]` sheet per touched sheet: a cell-for-cell **formula-text** before-image, recalc-free and refresh-stable, per the `/workbook-onboarding` skill's `BASELINE-SHEET.md`. The baseline is the diff's raw material — the only record of the build's changes that *isn't* self-reported. It is transient (`/workbook-log` clears it at close), so review while it stands. An additive build leaves none; the review still runs on the footprint alone.

## Step 1: Locate the change object

Find the task's Audit Log block — the most recent In-progress stub (the normal case: review runs between build and close-out) or the completed block the user names. Then inventory the tab strip for `Baseline — …` sheets. Report what the review has to work with:

> Reviewing [task title]. Baseline: [N sheets — full diff available | none — footprint-only, self-report grain].

If neither a block nor a baseline exists, say so and stop — there's no change object to review, and inventing one from a whole-workbook read is the audits' job, not this skill's.

Done when: the block is identified and the baseline inventory is known.

## Step 2: Enumerate the real diff

- **Baseline present:** compare each `Baseline — [sheet]` against its live sheet, cell for cell at the same addresses — formula text against current formula, value against value. The output is the **real diff**: every cell whose content changed since capture, with before → after.
- **No baseline:** the footprint's Done references and Sheets touched *are* the change list. Say plainly that the review is at self-report grain — it can verify what was reported, not discover what wasn't. Those fields exist once `/workbook-log` has completed the block; a fresh session holding only the Goal + Plan stub and no baseline has nothing changes-shaped to read — say so, and recommend re-running after `/workbook-log` completes the block (footprint-only review is the post-close moment).

Keep the diff at content grain, matching the capture: charts, objects, and formatting changes are invisible to a formula-text baseline and are only as visible as the narrative made them.

Done when: the changed cells are listed with before → after (or the self-report scope is fixed).

## Step 3: Compare the diff against the self-report

Set the real diff beside the footprint. Three buckets:

- **Reported and changed** — the expected case; these feed Step 4's scope.
- **Changed but unreported** — a finding in itself, before any audit runs: the build touched cells its record doesn't mention. Flag each with its address and before → after.
- **Reported but unchanged** — rarer; the record claims work the cells don't show. Flag it.

Done when: every diff entry and every self-report claim is in a bucket, and the mismatches are flagged.

## Step 4: Route to the audits with the derived scope

Hand the changed sheets and ranges to the audits as their scope — both fix a scope before reading and use one the user gives them. Name them in order: **`/formula-audit` first** (mechanical faults in the changed cells — broken formulas make logic findings noise), **then `/logic-audit`** (does the changed classification still hold its invariants — scoped to the buckets the changes feed). Both are user-invoked; naming them with the scope is the move, not running the whole workbook through them.

Where the diff is small and mechanical (a handful of formula edits), it's fine to check those cells directly in this pass and say so — routing exists for real surface area, not ceremony.

Done when: the scope is stated and the audits are named (or the small-diff check is done inline).

## Step 5: Report

Lead with a one-line verdict, then the findings:

> **Change review — [task title] — [Clean / Findings] — N changed cells across M sheets, X unreported**

- The diff summary: what actually changed, per sheet.
- Mismatch findings from Step 3 (unreported changes first — they're the fresh-eyes catch).
- The derived audit scope and what came back (or the named next step if the audits haven't run).
- What the review could *not* see: no baseline → self-report grain; formatting/objects → narrative only.

**Read-only throughout.** This skill changes nothing — no fixes, no re-capture, and never the baseline sheets themselves: clearing them is `/workbook-log`'s close-out, and this review is the last reader before that. Offer fixes only as named findings for a follow-up task.

## Quality checklist

- [ ] Run fresh — a new session or add-in chat, not the build session grading itself
- [ ] Baseline inventory reported up front (full diff vs footprint-only, stated plainly)
- [ ] Diff enumerated cell-for-cell against the baseline where one stands, before → after
- [ ] Unreported changes surfaced as findings in their own right
- [ ] Audit scope derived from the changes, not defaulted to the whole workbook
- [ ] `/formula-audit` named before `/logic-audit`
- [ ] Nothing modified — baseline sheets left standing for `/workbook-log` to clear
- [ ] Everything ran as sheet and cell reads — the whole review works in the Excel add-in
