# Audit Log block format

The block every Audit Log entry follows. `/workbook-plan` writes the stub, `/workbook-log` completes it in place or appends a standalone block, and `/workbook-build` reads the stub but never writes it; those skills reach this file via contract pointer ("the `/workbook-onboarding` skill's `AUDIT-LOG-FORMAT.md`").

## Task-block layout

One header row plus field rows, with **no fills anywhere**: status is carried by colored text and a rail, so it stays the loudest signal on the page.

- **Header row.** Col A: the **status indicator**, a colored dot plus word (`● Complete`), bold 10pt in the status color. Col B: `TASK YYYY-MM-DD HH:MM — [Task title]` in ink `#111827`, bold 12pt (the wide column keeps the title from truncating). The header row is vertically centered.
- **Status rail.** A thick left border in the status color down every row of the block, header and fields alike.

## Status indicators

| Status | Color | Hex |
|---|---|---|
| Complete | green | `#16A34A` |
| In-progress | amber | `#D97706` |
| Cancelled | gray | `#9CA3AF` |
| Partial (rare) | rose | `#E11D48` |

The indicator and the rail share the status color. On a status change, recolor **both**.

## Field rows

Col A holds the label, col B the content. **Auto-omit rule:** skip any field whose content is empty.

| Label (col A) | Content (col B) |
|---|---|
| Goal | One-line statement of what done looks like |
| Plan | Compressed 2 to 3 line plan summary. Skip if no plan. |
| Done | What was actually executed, with cell references and before/after where applicable |
| Validation | Tie-outs and checks run, with pass/fail and specific numbers |
| Deviations | Where execution went off plan, with reasons. Skip if none. |
| Surfaced | Out-of-scope items noticed and queued for future. Skip if none. |
| Sheets touched | Every sheet modified, plus external artifacts |
| Cancel reason | Only for Cancelled status |

**Formatting:** col A label bold 10pt subtitle gray `#6B7280`; col B normal 10pt ink `#111827` with text-wrap; a hairline `#E5E7EB` bottom rule per row; content rows top-aligned.

**Inline tags within Done:** bracketed, bold, colored text, no fills.

- **Fixed** green `#16A34A`: something broken got fixed
- **Verified** blue `#2563EB`: something checked and confirmed correct
- **Flagged** amber `#D97706`: needs attention, not resolved this cycle

## Stub lifecycle

1. `/workbook-plan` writes the **stub** at task start: the header with status In-progress (amber dot plus word, amber rail), then Goal and a compressed 2 to 3 line Plan.
2. `/workbook-build` reads the stub and never writes it.
3. `/workbook-log` completes the stub in place: flips the status to Complete, Cancelled, or Partial, recolors the dot plus word and the rail, and appends Done, Validation, Deviations, Surfaced, and Sheets touched below the existing rows.
4. A stub still In-progress at the next session is the abandonment signal `/workbook-explore` detects.

## Geometry

Col A 200px; col B 600px with text-wrap; rows autofit with a 20px floor; a blank row separates one block from the next.

The Audit Log's second grammar, the decision-shaped and triage-shaped blocks that record `/wayfinder` resolutions and `/triage` records, is defined in [`MULTI-SESSION.md`](MULTI-SESSION.md) and reuses this file's geometry, rail, field formatting, and auto-omit rule.
