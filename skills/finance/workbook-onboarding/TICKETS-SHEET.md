# Shared contract — Tickets sheet

Canonical definition of the **Tickets sheet** — the workbook substrate's recorded tracker
backend: sheet identity, the ticket table's columns, the T-id grammar, the status grammar with
claim-by-flip, the lifecycle division of labor across the loop, and the sheet's expression of
`/wayfinder` (the Wayfinding operations section below). **Canonical home: this file
in `workbook-onboarding/`**, beside the sibling sheet contracts — the sheet-layer hub owns the
specs of the workbook's contract sheets. This is the contract's only copy: the
`/to-tickets` run that creates the sheet, the loop skills that read and flip it
(`/workbook-build`, `/workbook-log`, `/workbook-explore`), and the wayfinder session that charts
or works a map here, reach this spec via **contract pointer** — a prose reference naming this
skill and this file.

**Contract version:** tickets-sheet v1

## What the sheet is

A multi-session workbook effort's tickets live **inside the workbook**: a dedicated sheet named
exactly **`Tickets`**, the substrate's tracker backend **on every surface**. The same sheet
serves whether the session runs in the Excel add-in, desktop Excel, or Excel on the web — never
split one effort's queue across backends, and never route a workbook effort's tickets to an
external tracker just because one is reachable: the backend is chosen by contract, not probed at
runtime. Nothing in this contract requires a shell, `gh`, or a filesystem — creating, claiming,
and closing tickets all run as cell operations, so the full climb works in the add-in.

The sheet is **conditional ceremony**: it exists only in a workbook whose effort went up the
stairs to a multi-session climb (a spec on the `Spec` sheet, tickets here) — or whose owner is
charting a **wayfinder map**, which lives on this same sheet and may precede the climb (see
Wayfinding operations below). The common single-session path never creates it.

## Sheet identity

- Named exactly **`Tickets`**, positioned beside the **`Spec`** sheet — the pair reads as one
  unit of the climb.
- Title rows per the sheet-contracts pattern: A1 `Tickets — [Effort name]`, bold 18pt accent
  navy `#1E3A8A` on white with a navy rule under the title row; A2 subtitle 10pt subtitle gray
  `#6B7280`: "Work queue for the current effort. Rows flip status; they are never deleted."
- Aptos, Calibri fallback; tab color accent navy `#1E3A8A`; the creating run stamps the A1 cell
  note `template v2` per the sheet-contracts convention.

## The ticket table

One row per ticket, under a bold header row. Locate the header row by the **`ID`** header string
in column A, not by a fixed row number — readers keyed to the header string never break if
content sits between the title rows and the table. The wide-table exception from the sheet
contracts applies: the
table sets its own column widths, with autofit-with-floor and top-aligned content rows.

Exact header strings — other skills match on these:

| Header | Holds |
|---|---|
| `ID` | Stable short id — `T1`, `T2`, … — assigned once at creation, in dependency order. Never renumbered, never reused: Audit Log blocks, the Handoff sheet, and Blocked-by cells name these ids, so they must stay durable. |
| `Title` | Short descriptive name for the slice. |
| `What it delivers` | The end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list. |
| `Acceptance criteria` | One criterion per line within the cell. |
| `Blocked by` | The T-ids that must complete before this one can start, or blank — a blank cell means the ticket can start immediately. |
| `Status` | One word from the status grammar below, colored per its token. |
| `Status date` | Date of the most recent status flip. |
| `Gist` | One-line outcome plus pointer, written at close. A Done W-row: its one-line answer plus the Audit Log block pointer (the map's Decisions-so-far index — see Wayfinding operations). A Graduated fog row: the W-id(s) it graduated into. An Out of scope row: the one-line why. Blank for open rows and most build T-rows. |

**Rows sit in dependency order** — blockers first, so the queue reads as a glanceable
top-to-bottom walking order; the `Blocked by` column carries the non-linear edges that row order
alone can't express.

## Ticket grammar — from `/to-tickets`

The `/to-tickets` run authors tickets to its own tracer-bullet rules; restated here so readers
of the sheet know what a row promises:

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) —
  vertical, NOT a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice is sized to fit in a single fresh context window.
- Any prefactoring should be done first.

The workbook reading of "every layer": data → formulas → outputs → tie-outs.

The real-tracker form's `ready-for-agent` label is a **no-op on this backend** — the `Status`
column is the state grammar that governs.

## Status grammar and the claim-by-flip rule

Statuses are exact words in colored text, no fills (semantic — keep them mapped):

- **Open** — ink **#111827** — created, not yet claimed.
- **In progress** — amber **#D97706** — claimed by the session working it.
- **Done** — green **#16A34A** — closed; acceptance criteria met.

In progress and Done reuse the audit-log-format token values (In-progress amber, Complete
green) — keep those two in sync with that contract; Open renders in plain ink. The wayfinding
extension adds three more status words — **Fog**, **Graduated**, **Out of scope** — defined in
Wayfinding operations below; a status tally must recognize all six.

**The status flip is the claim.** A session takes a ticket by flipping its `Status` from Open to
In progress and setting the `Status date` **as its first write** — the sheet-native assignee
mark, so a concurrent session reading the sheet skips the row.

**Work the frontier:** pick the topmost Open ticket whose blockers are all Done. For a purely
linear chain that means top to bottom.

## Lifecycle — the division of labor

Mirrors the tracker backend's division of labor:

- **Created** by the `/to-tickets` run — the sole author of build-ticket content (titles,
  deliverables, acceptance criteria, blocking edges); W-row content is the wayfinder session's,
  below. Loop skills flip state; they never write ticket content.
- **Claimed** by the build session — the status flip + date above, before any other write.
- **Closed** by `/workbook-log`'s issue-traced close — it reads the ticket's acceptance criteria
  here and flips the `Status` to Done.
- **Detected** by `/workbook-explore` with a bounded read — a status tally plus the first
  unblocked ticket, never ticket bodies.

For the map's W-rows the same division holds in wayfinder terms — charted by the charting
session, claimed by flip, resolved by the resolving session, detected via the map-status cell —
see Wayfinding operations below.

## Flip, don't delete

Done rows are queue **state**; the work's **narrative** stays in the Audit Log — one history
layer, grains distinct, with the Audit Log's issue-traced blocks keeping each `T-id` as a
durable referent. Never delete or renumber a row, whatever its status. The sheet outlives the
effort as its queue record; deleting it is the workbook owner's later call, never made
in-session.

## Wayfinding operations

How this backend expresses `/wayfinder` — the section that skill's intake consults for how this
substrate expresses maps, tickets, blocking, and frontier queries. **One table, one grammar**:
the workbook map is the Tickets sheet's own machinery extended — no second store, no second
layout contract.

**Map home.** The map lives on this same sheet: a compact **map header block** between the title
rows and the ticket table (the locate-by-`ID`-header rule above absorbs it), plus the map's
tickets as **W-rows** in the one ticket table. When the map precedes the climb — the usual
case — the **charting session creates the sheet** to this contract's identity rules; the
post-map climb (`/to-spec → /to-tickets`) then appends the build queue to the same sheet. One
table, rows appended in effort order: the map's W-rows read above the build's T-rows,
top-to-bottom as the effort's history.

### The map header block

Label/detail rows — label in col A, bold 10pt subtitle gray `#6B7280`; content in col B, normal
10pt ink, text-wrap; hairline `#E5E7EB` bottom rules — with a blank row before the table's
header row:

| Label | Holds |
|---|---|
| `Map` | The map's name. |
| `Destination` | What reaching the end of the map looks like — the spec, decision, or change the effort is finding its way to. One or two lines; every session orients to it before choosing a ticket. On close, updated to name where the effort landed (typically the `Spec` sheet). |
| `Notes` | Compact standing context: domain, skills every session should consult, standing preferences for the effort. Lasting context graduates to the Agent sheet rather than accreting here. |
| `Map status` | **The detection discriminator** — exact word `Open` (amber `#D97706`) or `Closed` (green `#16A34A`). A glance answers "is a map open?" with no body reads; open W-rows corroborate, but this cell is primary. |

A session's map at low resolution = the header block plus the table — one bounded read. There is
no prose Decisions-so-far section: **the index is the Done W-rows read in order**, via the `Gist`
column — structural, so it cannot drift from the tickets.

### W-rows — the map's tickets

Wayfinder tickets take **W-prefixed ids** (`W1`, `W2`, …) with the same durability rules as
T-ids — assigned once in charting order, never renumbered, never reused — and no collision with
the build queue's T-ids on the shared table. The columns read in wayfinder terms:

- `Title` — the ticket's **name** (refer to it by name in narration, never a bare id), prefixed
  with its type word — `Research:`, `Prototype:`, `Grilling:`, or `Task:` — the sheet-native
  form of the `wayfinder:<type>` label.
- `What it delivers` — the **question**: the decision or investigation the ticket resolves. (For
  a Fog row, the loose patch text lives here.)
- `Acceptance criteria` — usually blank for W-rows; use it only when what a resolution must
  settle is worth pinning.
- `Blocked by` — W-ids, same rule: blank means takeable now. The **frontier** — the open,
  unblocked, unclaimed tickets — is visible from row order plus this column, no body reads.
- `Gist` — written at close; see the resolve motion below.

Claim, flip-don't-delete, and work-the-frontier apply verbatim: **the claim is the status flip +
date, as the session's first write**; never delete or renumber a row.

### The wayfinding statuses

Three more exact status words, colored text, no fills (semantic — keep them mapped; the tokens
reuse the existing palette — subtitle gray from the sheet-contracts palette, the blue and gray
from the audit-log-format status/tag tokens):

- **Fog** — subtitle gray **#6B7280** — a not-yet-specified patch: loose text in the question
  cell, **no id** — fog is coarser than a ticket, and one patch may graduate into several
  tickets, or none. In scope, just not yet sharp enough to ticket; don't pre-slice it.
- **Graduated** — blue **#2563EB** — **graduate-by-flip**: the sheet's flip-don't-delete grammar
  overrides the real-tracker form's delete-on-graduation. A fog patch that sharpened into
  ticket(s) flips to Graduated, its `Gist` cell pointing at the new W-id(s); it stays on the
  sheet as map history.
- **Out of scope** — gray **#9CA3AF** — work ruled beyond the destination: applied to a
  ruled-out ticket row, or to a standalone row for a ruling that never was a ticket, with the
  one-line why in the `Gist` cell. Out-of-scope rows never graduate — the frontier stops at the
  destination.

A ticket W-row otherwise runs Open → In progress → Done as usual; Done here means **resolved** —
the decision made and recorded.

### Resolving a W-row — the gist and the decision-shaped block

The full answer — the real-tracker form's resolution comment — is a **decision-shaped Audit Log
block**: a resolved decision is a completed, past-tense unit of work, the grain the Audit Log
already holds, and blocks are id-addressable, giving Done rows a durable pointer target — the
sheet-native link. The block's shape is defined in the audit-log-format contract, the sibling
[`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md). Resolving is one three-part motion:

1. Write the decision-shaped block to the Audit Log (born Complete — no stub lifecycle).
2. Flip the W-row's `Status` to **Done** + status date.
3. Write the `Gist` cell: the one-line answer plus the block pointer — the Audit Log sheet named
   with the W-id its block header carries (e.g. `Audit Log · W3`).

Then, as on any tracker: append newly-surfaced W-rows, graduate any fog the answer has made
specifiable, and rule mis-scoped rows out of scope. **Never resolve more than one ticket per
session** — except research rows, below.

### Research — digest-as-canonical

The real-tracker form resolves research tickets via `/research` subagents capturing findings on
throwaway branches — neither subagents nor git exist in the add-in, but the underlying
capability does (web search and live URL fetch run there). The canonical motion: **the session
researches itself**, and the findings digest is the same decision-shaped Audit Log block every
resolution uses. The one-ticket-per-session exemption survives — research W-rows may resolve
inline alongside the session's one real ticket, and charting's fire-the-subagents step reads
**resolve what you can inline, leave the rest on the frontier**. Desktop surfaces may still use
a `/research` subagent and land a full cited `.md` beside the workbook — **opt-in export only**,
never canonical, never prerequisite.

### Assets — in-workbook objects

"Linked, not pasted": an asset created while resolving — a prototype, a mock, scratch work — is
a **prototype/scratch sheet or mocked-up region in the workbook**, named from the resolution
block's Assets field, riding the workbook's existing sheet-lifecycle conventions. No new storage.

### Map close

The map closes when the way is clear — the destination reached, typically a spec on the `Spec`
sheet with the build queue appended below the W-rows. Flip `Map status` to Closed and point the
`Destination` row at where the effort landed. W-rows end all Done, Graduated, or Out of scope —
nothing deleted; the Done rows remain the effort's permanent rationale index.

### Add-in-only completeness

Stated as a requirement, not an accident: every canonical wayfinding motion — charting,
claiming, resolving, research, prototyping, detection, continuation — touches only the workbook
plus capabilities verified live in the Excel add-in. A user who only ever has the add-in runs
the entire wayfinding loop with zero loss of decision-critical capability; subagents and sibling
files are the only absences, and both are enhancements.
