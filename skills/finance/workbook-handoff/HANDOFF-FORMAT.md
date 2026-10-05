# Shared contract — Handoff block format

Canonical definition of the block *inside* the Handoff sheet — the metadata row, the six fields,
and field formatting. **Canonical home: this file in `workbook-handoff/`** — the only skill that
writes a handoff block. `/workbook-explore` reads the Handoff sheet this produces; `/workbook-log`
clears it at task close. The Handoff sheet's name, title banner, position, tab color, and
lifecycle live in the Sheet conventions of the `/workbook-onboarding` skill's
`SKILL.md`; this file defines what goes inside it. This contract is **self-contained** —
it does not depend on any other contract being present alongside it.

**Contract version:** handoff-format v2

## Block metadata row

No fill — the alert fill belongs to the sheet's title banner (per the `/workbook-onboarding`
skill's `SKILL.md`, Sheet conventions); the block itself uses orange text and a rail:

- Col A: `HANDOFF YYYY-MM-DD HH:MM` — bold 10pt in alert orange **#EA580C** (canonical palette in
  the `/workbook-onboarding` skill's `SKILL.md`, Sheet conventions)
- Col B: `Originated in chat ending [date]` — normal 10pt, subtitle gray **#6B7280**
- Metadata row vertically centered.

**Alert rail:** a **thick left border in alert orange #EA580C down every row of the block**
(metadata row and fields alike) — the same rail treatment the Audit Log's task blocks use, in the
Handoff signal color.

## Field rows

Col A = label, Col B = content. One Handoff block per sheet (a single in-flight task).
**Two-column geometry:** Col A = 200px, Col B = 600px with text-wrap; row heights autofit with a
20px minimum floor.

| Label (col A) | Content (col B) |
|---|---|
| Task goal | One-line statement of what done looks like (from `/workbook-plan`) |
| Plan | Full six-section plan, or rough approach if no `/workbook-plan` was made |
| Decisions made in chat | Non-obvious context, decisions, agreements from conversation |
| Progress | What's done, what's in-flight, what's not started — be specific |
| Next action | Specific first step for next session (not "continue the work") |
| Context to preserve | Non-obvious observations that would be expensive to rediscover |

**Field row formatting:** no fills. Col A label bold 10pt in subtitle gray **#6B7280**; Col B
normal 10pt ink **#111827**, text-wrap enabled; a hairline **#E5E7EB** bottom rule per row.
Content rows top-aligned.

## "Context to preserve" — the anti-loss field

The catch-all for context that reads as background but is expensive to rediscover. Litmus: "If a
future session redid this task without knowing this, would it screw up?" Examples: "Velixo
refresh fails silently if Branch filter is blank"; "Detail sheet bounded at row 9055 — don't
extend without checking."

## Overwrite (stale handoff) handling

If a Handoff sheet already exists when `/workbook-handoff` runs (a prior task never closed), clear
content from row 3 onward (preserve title rows 1–2) and write the new block. Detection and
lifecycle are defined in the `/workbook-onboarding` skill's `SKILL.md`, Sheet conventions.
