# Shared contract — Spec sheet

Canonical definition of the **Spec sheet** — where a multi-session workbook effort's spec lives:
sheet identity, the content layout (the `/to-spec` template as rows), the canonical-copy rule,
visibility-as-state, and the hide-on-complete lifecycle. **Canonical home: this file in
`workbook-onboarding/`**, beside the sibling sheet contracts — the sheet-layer hub owns the
specs of the workbook's contract sheets. This is the contract's only copy: the
`/to-spec` run that writes the sheet, and the loop skills that read or hide it
(`/workbook-explore`, `/workbook-log`), reach this spec via **contract pointer** — a prose
reference naming this skill and this file.

**Contract version:** spec-sheet v1

## What the sheet is

When a workbook effort goes up the stairs to a multi-session climb, its spec lands in a
dedicated sheet named exactly **`Spec`**, written by the `/to-spec` run on whichever surface it
runs. The workbook is the effort's only durable surface, so **the Spec sheet is the canonical
copy of the spec** — every later session reads the spec here, on any surface. Nothing in this
contract requires a shell, `gh`, or a filesystem: writing and reading the spec are cell
operations, so the full climb — grill → spec → tickets → build — runs in the Excel add-in.
Desktop surfaces are an **enhancement, never a prerequisite**: on a surface with a filesystem, a
run may additionally export a sibling `.md` beside the workbook — an **opt-in snapshot, never
the canonical copy**.

Like its sibling `Tickets` sheet, the Spec sheet is **conditional ceremony**: the common
single-session path never creates it.

## Sheet identity

- Named exactly **`Spec`**, positioned beside the **`Tickets`** sheet — the pair reads as one
  unit of the climb.
- Title rows per the sheet-contracts pattern: A1 `Spec — [Effort name]`, bold 18pt accent navy
  `#1E3A8A` on white with a navy rule under the title row; A2 subtitle 10pt subtitle gray
  `#6B7280`: "Specification for the current effort. This sheet is the canonical copy; any
  exported file is a snapshot."
- Aptos, Calibri fallback; tab color accent navy `#1E3A8A`; the creating run stamps the A1 cell
  note `template v2` per the sheet-contracts convention.
- Two-column geometry per the sheet contracts: col A labels 200px, col B content 600px with
  text-wrap, autofit rows with the 20px floor, content rows top-aligned.

## Content — the `/to-spec` template, as rows

The sheet holds `/to-spec`'s own output sections, unmodified, one bold 12pt accent-navy section
header row per section — **Problem Statement**, **Solution**, **User Stories**, **Implementation
Decisions**, **Testing Decisions**, **Out of Scope**, **Further Notes** — with the section's
content in col B rows beneath it (numbered user stories one per row), hairline `#E5E7EB` row
separators, no fills. The `/to-tickets` run reads these rows as its source when it builds the
`Tickets` sheet.

## Visibility is state

The sheet's visibility carries the effort's coarse state — readable from the tab strip without
opening a single cell:

- **Visible beside a live `Tickets` sheet** — a climb in progress.
- **Visible with no `Tickets` sheet** — an interrupted climb, paused between spec and tickets.
- **Hidden** — the effort completed and was closed out.

## Lifecycle

- **Written** by the `/to-spec` run — the sole author of spec content.
- **Effort complete** (every ticket on the `Tickets` sheet is Done) — the close-out first
  graduates anything of lasting value to the Agent sheet, then **hides** the Spec sheet.
- **Deletion is the workbook owner's later call, never made in-session** — hiding is as far as
  any close-out goes.
