# Shared contract — Audit Log block format

Canonical definition of the Audit Log block formats — the task block (layout, status indicators,
field set, formatting, inline tags, two-column geometry, the stub lifecycle) and the wayfinding
**decision-shaped block**, with its **triage-shaped** second use. **Canonical home: this file in `workbook-onboarding/`**, beside its
sibling `SHEET-CONTRACTS.md` — the sheet-layer creator owns the specs of the sheets it lays
down, so both sheet-shaped contracts live in one place (while a sole-consumer contract like
`handoff-format` stays with its consumer).
This is the contract's only copy: the other skills that write Audit Log blocks
(`/workbook-plan`, `/workbook-log`, the wayfinder session resolving on the Tickets sheet, and
the `/triage` session working the Agent sheet)
reach this spec via **contract pointer** — a prose reference naming this skill and this file;
`/workbook-build` reads the stub it defines but never writes it.

**Contract version:** audit-log-format v2

## Task-block layout

A task block is one header row plus field rows, with **no fills** — status is carried by colored
text and a rail, so it stays the loudest signal on the page:

- **Header row** — Col A: the **status indicator**, a colored dot + word (`● Complete`), bold
  10pt in the status color. Col B: `TASK YYYY-MM-DD HH:MM — [Task title]` in ink `#111827`, bold
  12pt — the title sits in the wide column so it never truncates. Header row vertically centered.
- **Status rail** — a **thick left border in the status color down every row of the block**
  (header and fields alike). The rail makes in-flight and finished work scannable from across
  the sheet.

## Status indicators (semantic — keep them mapped)

- **Complete** — green **#16A34A**
- **In-progress** — amber **#D97706** (stub state set by `/workbook-plan`; replaced by `/workbook-log` at close)
- **Cancelled** — gray **#9CA3AF**
- **Partial** — rose **#E11D48** (rare)

Each renders as a bold dot + word in the status color, no fill; the block's rail takes the same
color. When a status changes (completing a stub), recolor **both** the indicator and the rail.

## Field rows

Col A = label, Col B = content. **Skip any field whose content is empty** (auto-omit rule).

| Label (col A) | Content (col B) |
|---|---|
| Goal | One-line statement of what done looks like |
| Plan | Compressed 2-3 line plan summary. Skip if no plan. |
| Done | What was actually executed, with cell references and before/after where applicable |
| Validation | Tie-outs and checks run, with pass/fail and specific numbers |
| Deviations | Where execution went off plan, with reasons. Skip if none. |
| Surfaced | Out-of-scope items noticed and queued for future. Skip if none. |
| Sheets touched | Every sheet modified, plus external artifacts |
| Cancel reason | Only for Cancelled status |

**Field row formatting:** no fills. Col A label bold 10pt in subtitle gray **#6B7280**; Col B
normal 10pt ink **#111827**, text-wrap enabled; a hairline **#E5E7EB** bottom rule per row.
Content rows top-aligned.

## Inline tags within Done content

Bracketed, bold, colored text — no fills:

- **Fixed** (green #16A34A) — something broken got fixed
- **Verified** (blue #2563EB) — something checked and confirmed correct
- **Flagged** (amber #D97706) — needs attention, not resolved this cycle

## Stub lifecycle (contract between `/workbook-plan` and `/workbook-log`)

- `/workbook-plan` writes a **stub** at task start: block header with status **In-progress**
  (amber #D97706 dot + word, amber rail), plus Goal and a compressed 2-3 line Plan summary.
- `/workbook-build` reads the stub but never writes it.
- `/workbook-log` **completes the stub in place**: flips the status to Complete / Cancelled /
  Partial — recoloring the dot + word and the rail — and appends Done, Validation, Deviations,
  Surfaced, and Sheets touched below the existing rows.
- A lingering In-progress stub is the abandonment signal `/workbook-explore` detects in the next session.

## Decision-shaped blocks (wayfinding)

The Audit Log's second block type — the resolution record for a wayfinder map's W-rows. The
Tickets-sheet contract (the sibling [`TICKETS-SHEET.md`](TICKETS-SHEET.md), Wayfinding
operations) names when one is written. A resolved decision is a completed, past-tense unit of
work — the grain this log already holds — and blocks are id-addressable, so a decision block is
the durable target the Tickets sheet's `Gist` pointers name: the sheet-native form of a
tracker's resolution comment. The resolving session writes the block **whole, at resolution** —
born **Complete** (green dot + word, green rail), no stub lifecycle.

- **Header row** — Col A: the status indicator (`● Complete`). Col B:
  `DECISION YYYY-MM-DD HH:MM — [W-id] · [Ticket name]` in ink `#111827`, bold 12pt — the
  `DECISION` keyword distinguishes it from task blocks, and the W-id is the string pointer
  lookups match on.
- **Field rows** — same formatting and auto-omit rule as task blocks:

| Label (col A) | Content (col B) |
|---|---|
| Question | The decision or investigation as charted on the W-row |
| Decision | The answer, stated as the settled rule |
| Rationale | The why — key reasoning and trade-offs weighed |
| Rejected | Alternatives ruled out, with a one-line why each. Skip if none. |
| Research digest | For research rows: the findings with named sources — the canonical record (a cited sibling `.md` is opt-in export, never canonical). Skip if none. |
| Assets | In-workbook objects the resolution produced — prototype/scratch sheets or mocked-up regions, by name. Skip if none. |
| Surfaced | New W-rows added or fog graduated as a result. Skip if none. |

Decision blocks ride the same two-column geometry, status rail, and blank-row separation as task
blocks, appended in chronological order among them — one history layer, grains distinct: queue
state stays on the Tickets sheet; the narrative and the full answers live here.

## Triage-shaped blocks (the decision-shaped grammar, second use)

The triage record for an Agent-sheet inbox item — the same grammar as a decision-shaped block
(born **Complete**, no stub lifecycle; same field formatting, auto-omit rule, rail, and
geometry), written by the `/triage` session working the Agent sheet's Open decisions / pending
items. A sheet line can't hold a 30–50-line brief, so the block holds the *event* — the triage
notes and any agent brief — while the line keeps the *implication*: status word + gist + block
pointer. When one is written, and how graduation works, is the Triage-on-the-Agent-sheet section
of the sibling [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md).

- **Header row** — Col A: the status indicator (`● Complete`). Col B:
  `TRIAGE YYYY-MM-DD HH:MM — [Item gist]` in ink `#111827`, bold 12pt — the `TRIAGE` keyword
  distinguishes it from task and decision blocks, and the Agent-sheet line's pointer names the
  block by keyword and date (e.g. `Audit Log · TRIAGE 2026-08-02`). One block per item triaged.
- **Field rows** — the decision-block field set read in triage terms, same auto-omit rule:

| Label (col A) | Content (col B) |
|---|---|
| Question | The item as it stood on the Agent-sheet line |
| Decision | The state applied — ready-for-agent / ready-for-human / closed out — with the outcome stated |
| Rationale | The why — key reasoning, verification results, the redundancy and prior-rejection checks |
| Rejected | For an out-of-scope close: the concept ruled out, with the one-line why. Skip if none. |
| Agent brief | For ready-for-agent items: the brief (the `/triage` skill's `AGENT-BRIEF.md` structure, disclaimer line included). Skip if none. |
| Surfaced | Follow-on items added to the inbox, or the W-row a graduation appended. Skip if none. |

## Two-column block geometry

Used across both the Audit Log and the Handoff sheet. Col A = 200px, Col B = 600px with text-wrap;
row heights autofit with a 20px minimum floor. A blank row separates one block from the next.
