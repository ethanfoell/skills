# Shared contract — Baseline sheets

Canonical definition of the **Baseline sheets** — the transient, in-workbook, formula-text
before-image a destructive build leaves while its task is open: the trigger, the naming and
content rules, and the Handoff-mirror lifecycle. **Canonical home: this file in
`workbook-onboarding/`**, beside the sibling sheet contracts — the sheet-layer hub owns the
specs of the workbook's contract sheets. This is the contract's only copy: the
skills that create and clear the sheets (`/workbook-build`, `/workbook-log`) reach this spec
via **contract pointer** — a prose reference naming this skill and this file.

**Contract version:** baseline-sheet v1

## What the sheets are

When a build is about to modify or destroy pre-existing content, the workbook briefly holds a
**before-image**: a formula-text copy of the sheets the planned build is about to touch,
captured before execution so "what did this build actually change?" stays answerable — by positional
comparison against the live sheet — for as long as the task is open. The baseline is
**conditional and transient**: an additive build never creates one, and no baseline outlives
its task's close-out.

Nothing in this contract requires a shell or a filesystem — capturing, reading, and clearing a
baseline are sheet and cell operations, so the whole lifecycle runs in the Excel add-in.

## Trigger — mechanical, already computed

Created by `/workbook-build` at pre-flight **exactly when its destructive-op scan flags
operations** — destructive = pre-existing content modified or lost = there is a "before" worth
capturing. The scan's verdict is the whole trigger; zero new judgment:

- **Additive builds create nothing.**
- **Lightweight mode never auto-engages** — its per-op confirmation already shows before/after
  at one-cell grain.
- **Capture happens once, at pre-flight**, covering the sheets the planned build is about to
  touch. A baseline is a before-image; it is never refreshed or re-captured mid-task.

## Sheet identity

- One baseline sheet per captured source sheet, named **`Baseline — [source sheet name]`**
  (truncate the source name where needed — Excel caps sheet names at 31 characters).
- Positioned at the **end of the tab strip**, keeping `Handoff` last when one exists (its own
  contract pins that position); tab color subtitle gray `#6B7280` — machinery, not a working
  surface.
- **No title rows and no template stamp** — the grid must mirror the source cell-for-cell, so
  identity rides the sheet name plus a **cell note on A1**: `Baseline of [sheet], captured
  YYYY-MM-DD`.

## Content rule — formula text, not values

A cell-for-cell mirror of the source sheet at capture time, every entry at its source address:

- **Formula cells hold the formula string as inert text** (leading apostrophe) — never live
  formulas. Inert text is recalc-free, query-free, and refresh-stable.
- **Non-formula cells hold their value.**
- No formatting requirements — the baseline is a comparison substrate, not a presentation
  sheet.

Why formula text and not a values copy: a values copy is refresh-unstable — one Velixo refresh
drowns a comparison in false positives — and blind to a same-value formula replacement, the
change an audit cares most about.

**Honest limit:** the capture is text-grain. Charts, embedded objects, and formatting are not
captured; a change to those surfaces is visible only in the Audit Log narrative.

## Lifecycle — Handoff-mirror

- **Created** by `/workbook-build` at pre-flight, on the trigger above.
- **Consumed** by `/workbook-review` — the changes-scoped fresh-eyes pass enumerates the build's
  real diff by positional comparison against the live sheets, while the baseline stands.
- **Cleared** by `/workbook-log` at task close — every `Baseline — …` sheet deleted, whatever
  the closing status.

A temporary before-image, not a second history layer: the Audit Log stays the workbook's one
history, and accumulating version-numbered copies are explicitly rejected as a parallel
history. An abandoned baseline always accompanies a lingering In-progress stub in the Audit
Log — the stub is the abandonment signal, so no other skill needs to detect baselines.
