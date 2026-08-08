# Shared contract — Four-sheet model, sheet identities & color palette

Canonical definition of the four meta-sheets this framework adds to a workbook — their exact
names, audiences, purposes, title rows, typography and geometry, tab colors, the Agent sheet's
sections, the Handoff lifecycle, and the workbook color palette. **Canonical home: this file in
`workbook-onboarding/`.** This is the contract's only copy: the other skills that write these
sheets (`/workbook-log`, `/workbook-handoff`) reach this spec via **contract pointer** — a prose
reference naming this skill and this file; `/workbook-explore` reads the same sheets
and relies on these definitions. This contract is **self-contained** — it does not depend on any
other contract being present alongside it.

**Contract version:** sheet-contracts v2

## The four sheets (exact names — other skills match on these strings)

| Sheet | Exact name | Audience | Purpose |
|---|---|---|---|
| Instructions | `Instructions` | Humans (colleagues, auditors, future-self) | How to USE the workbook |
| Agent | `Agent` | AI + any reader | Standing operating guidance, synthesized across sessions |
| Audit Log | `Audit Log` | History | Dated, append-only record of what was done per task |
| Handoff | `Handoff` | Active task state | In-flight task paused for a future session (transient) |

**Dividing lines:** Audit Log = journal (chronological, append-only). Agent = manual (current
operating context, synthesized). Instructions = human user guide. Handoff = in-flight task state
(transient, cleared on completion).

**Overlap rule:** a design decision's *event* goes in the Audit Log (dated); its *implication*
(the standing rule) goes in the Agent sheet. A known risk lives in the Agent sheet; the
originating context stays in the Audit Log entry that first surfaced it.

**Conditional effort sheets.** Two more sheets exist only in a workbook whose effort went up the
stairs to a multi-session climb: **`Spec`** and **`Tickets`**, created by the `/to-spec` and
`/to-tickets` runs — or, for `Tickets`, by a wayfinder charting session, since that sheet
doubles as the wayfinder map's home — never by onboarding. Their contracts are the siblings
[`SPEC-SHEET.md`](SPEC-SHEET.md) and [`TICKETS-SHEET.md`](TICKETS-SHEET.md) in this folder; the
four-sheet model above is unchanged by them.

**Conditional task sheets.** One more family is transient at the task grain: the
**`Baseline — [sheet]`** sheets — a formula-text before-image created by `/workbook-build` when
its destructive-op scan fires, cleared by `/workbook-log` at close (Handoff-mirror lifecycle,
never a second history layer). They carry no title rows and no template stamp — the grid
mirrors the source sheet. Contract: the sibling [`BASELINE-SHEET.md`](BASELINE-SHEET.md).

## Typography

All four meta-sheets set **Aptos**, with **Calibri as the fallback** where Aptos is unavailable —
name the fallback explicitly rather than letting Excel substitute silently, so the sheets render
consistently across machines.

## Sheet title rows (rows 1–2 of each sheet)

Row 1 is the title, row 2 the subtitle (10pt, subtitle gray `#6B7280`). The three accent sheets
carry a **medium accent-navy bottom rule across the title row (both columns)**; the Handoff title
is the one **filled** title — an alert banner, not an accent.

| Sheet | A1 title | A1 treatment |
|---|---|---|
| Instructions | `Instructions` (or a name fitting the workbook's convention) | bold 18pt accent navy `#1E3A8A` on white, navy rule under the row |
| Agent | `Agent — [Workbook Name]` | bold 18pt accent navy `#1E3A8A` on white, navy rule under the row |
| Audit Log | `Audit Log — [Workbook Name]` | bold 18pt accent navy `#1E3A8A` on white, navy rule under the row |
| Handoff | `HANDOFF — [Workbook Name]` | bold 16pt **white on alert-orange `#EA580C` fill**, across both columns |

Subtitles: Agent — "Standing operating guidance for maintaining this workbook." Audit Log —
"Running record of changes per task. See Agent sheet for current operating guidance." Handoff —
"Active handoff. If you're picking up this task in a new session, read this first." Instructions
has no fixed subtitle.

## Two-column geometry & row behavior

- **Columns:** Col A (labels) = 200px (150pt); Col B (content) = 600px (450pt), text-wrap on Col B.
- **Row heights:** autofit with a **20px minimum floor** — short fields collapse, long fields
  grow. The **title row is held fixed at 28px**.
- **Vertical alignment:** content rows top-aligned (labels align to the first line of multi-line
  content); title and block-header rows vertically centered.
- **Wide-table exception:** a genuinely multi-column table sets its own column widths but follows
  the same autofit-with-floor and alignment rules. Merged narrative rows keep manual heights —
  Excel can't autofit merged cells reliably.

(The block contracts — `audit-log-format`, `handoff-format` — and the effort-sheet contract
`spec-sheet` restate the column widths, floor, and field-row treatment so each stays
self-contained; keep those restatements in sync with this section, same as the shared palette
values below.)

## Tab colors

The meta-sheet tabs carry the palette, so a maintained workbook is recognizable from the tab
strip alone: **Instructions, Agent, and Audit Log tabs in accent navy `#1E3A8A`; the Handoff tab
in alert orange `#EA580C`**.

## Template-version stamp

Each meta-sheet carries a discreet template-version marker: a **cell note on its A1 title cell
reading `template v2`**. The creating skill writes the note — `/workbook-onboarding` for the
three sheets it lays down (and any sheet it migrates), `/workbook-handoff` for the Handoff sheet —
and `/workbook-onboarding`'s Re-onboard migration reads it to detect sheets built to an older
standard; an absent note reads as pre-v2. The conditional effort sheets (`Spec`, `Tickets`) are
stamped by the runs that create them — see the sibling `SPEC-SHEET.md` and `TICKETS-SHEET.md`
contracts.

## Agent sheet sections (exact names — `/workbook-log`, `/workbook-explore`, and `/triage` read these)

1. **Operating conventions**
2. **Workbook-specific gotchas**
3. **Active risks**
4. **Open decisions / pending items**
5. **User preferences for this workbook**
6. **Out of scope**

`/workbook-explore` reads only **Active risks** and **Open decisions / pending items** at session
start (the time-sensitive content) — **the session-start read does not grow with section 6**:
"Out of scope" is rejection memory, read by `/triage` on demand and never at session start. On
first creation, seed a section only when verifiable from the workbook or confirmed by the user;
otherwise placeholder: "None recorded yet — added by `/workbook-log` as they surface." (Section 6
has a different writer — its placeholder reads "None recorded yet — added by `/triage` as
rejections land.") Keep section headers stable even when empty. Neutral operator voice — record
the work, not the worker; these sheets outlive the sessions that write them.

## Triage on the Agent sheet (the `/triage` mapping)

How this substrate expresses `/triage` — the record that skill's intake expects ("the mapping
should have been provided"): the substrate's onboarding is its setup motion, so the mapping lives
here in the hub, and `/setup-skills-ef`'s front door routes a workbook to `/workbook-onboarding`.
`/triage` itself runs byte-untouched, and everything below is cell operations — the full pass
runs in the Excel add-in with no shell, no `gh`, no filesystem.

- **The surface is section 4, Open decisions / pending items** — the workbook's idea inbox. The
  `Tickets` and `Spec` sheets are **never triaged**: the queue is downstream of triage, never a
  triage surface.
- **States are one status word on the line.** An unmarked line *is* `needs-triage`; triage marks
  `ready-for-agent` / `ready-for-human` or closes the line out — the close-out *is* `wontfix`
  (and a rejected enhancement additionally lands in section 6, below). No new sheet, no
  status-column ceremony. `needs-info` is vestigial-but-mapped on this solo substrate — an open
  question stays on the line awaiting its trigger, which is exactly what section 4 already
  holds. The category roles (`bug` / `enhancement`) carry no marker; a rejection's disposition
  applies the distinction (below).
- **Documents are triage-shaped Audit Log blocks.** The overlap rule above decides the split: the
  *event* (the triage session — notes + brief) goes to the Audit Log as a dated block; the
  *implication* (current status) stays on the Agent-sheet line as status word + gist + block
  pointer. Format: the sibling [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md) — the decision-shaped
  grammar's second use. Single-source holds: the Audit Log stays the workbook's one narrative
  layer.
- **Graduation is one-directional.** The never-triage-tickets rule bars *re-triaging the queue*,
  not *feeding it*: a `ready-for-agent` item with a live `Tickets`-sheet effort is **offered** as
  a W-row — the human approves the append; with no live effort it stays marked-ready on its line
  for `/workbook-plan`'s normal intake. Nothing flows queue → triage, and queue and inbox never
  cycle.
- **Rejection memory is section 6, "Out of scope"** — one line per rejected concept plus its
  Audit Log block pointer: `/triage`'s concept-file knowledge base in sheet form, read by its
  prior-rejection check on demand and extended on a rejected-enhancement close (the section-4
  line closes out; already-implemented and rejected-bug closes take no entry). The first
  extension of the pinned five sections — and `/workbook-explore`'s session-start read does not
  grow.

(An accepted zero-edits consequence: `/triage`'s grill step runs `/grilling`, not
`/grill-with-files` — triage's earlier steps already did the file-grounded looking.)

## Handoff sheet detection & lifecycle (contract among `/workbook-handoff`, `/workbook-explore`, `/workbook-log`)

- Named exactly **`Handoff`**, positioned as the **last** sheet for discovery.
- **Created** by `/workbook-handoff` when pausing a task. **Read** by `/workbook-explore` next
  session — it surfaces the handoff and offers Resume (→ `/workbook-build`) or close-out
  (→ `/workbook-log` with Cancelled). **Cleared** (the entire sheet deleted) by `/workbook-log`
  at task close.
- The block format *inside* the Handoff sheet is defined in the `handoff-format` contract — the
  `/workbook-handoff` skill's `HANDOFF-FORMAT.md`.

## Color palette

The workbook's design tokens. **Alert orange**, **ink**, **subtitle gray**, and **hairline** also
appear in the other contracts that use them (`audit-log-format`, `handoff-format`, and the
effort-sheet contracts `spec-sheet`/`tickets-sheet`) so each contract stays self-contained —
keep those values in sync across every contract that restates them. Status/tag colors are
defined and owned in the `audit-log-format` contract — the sibling
[`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md) in this folder.

| Token | Hex | Used for |
|---|---|---|
| Accent navy | `#1E3A8A` | Sheet titles + title rules, section headers, the Workbook Snapshot label — text and rules only, never a fill; also the Instructions/Agent/Audit Log tab color |
| Alert orange | `#EA580C` | Handoff title banner (the one fill — it signals "active, read me"); the Handoff tab; handoff block metadata + rail |
| Ink | `#111827` | Content text; task titles |
| Subtitle gray | `#6B7280` | A2 subtitles; field-row labels |
| Hairline | `#E5E7EB` | Field-row and section separators (thin bottom rules) — replaces alternating row shading |

(Status/tag tokens — Complete green `#16A34A`, In-progress amber `#D97706`, Cancelled gray
`#9CA3AF`, Partial rose `#E11D48`; tags Verified blue `#2563EB`, Fixed green `#16A34A`, Flagged
amber `#D97706` — live in the sibling [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md) in this folder.)

**Palette overrides.** These tokens are defaults, not law — a workbook may re-theme them to
company branding. Record any override in the Agent sheet's **User preferences for this workbook**
section so later sessions apply the workbook's palette, not the default. Status colors stay
semantic whatever the theme — keep them mapped to the same states.
