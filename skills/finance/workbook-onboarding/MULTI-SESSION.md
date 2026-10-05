# Multi-session efforts on a workbook

The human-in-the-loop pipeline's machinery on the workbook substrate: the `Spec` and `Tickets` sheets, the wayfinder map that lives on `Tickets`, and `/triage` running over the Agent sheet. All of it is opt-in: the common single-session path never creates these sheets, and onboarding never does; they appear only when an effort climbs the stairs (`/to-spec` writes `Spec`, `/to-tickets` writes `Tickets`) or a `/wayfinder` charting session opens a map. The `/to-spec` and `/to-tickets` runs, `/wayfinder`, `/triage`, and the loop skills that detect, flip, or hide these sheets reach it by contract pointer ("the `/workbook-onboarding` skill's `MULTI-SESSION.md`"). Multi-session orchestration runs on Claude Code and Cowork; the Excel add-in treats existing `Spec` and `Tickets` sheets as inert (present, never acted on).

Both effort sheets follow the accent-sheet pattern in the hub's [`SKILL.md`](SKILL.md), Sheet conventions; only their A1 literals and subtitles are specific to them.

## Detection at session start

`/workbook-explore` performs one bounded, detection-level read of the effort sheets, never a ticket body or an acceptance criterion: a status tally of the `Tickets` sheet (Open and In progress counts; Done and the three wayfinding statuses ignored), the id and title of the first unblocked Open ticket in row order (rows sit in dependency order, so first-unblocked is a glance), and the `Map status` cell. A visible `Spec` sheet with no `Tickets` sheet beside it means, by construction, an interrupted spec-to-tickets climb; it earns a note beneath the menu ("resume with `/to-tickets`"), no menu slot.

Menu precedence is **Resume > open map > ticket queue**. Resume (a Handoff sheet or an In-progress stub) wins because mid-effort the next slice usually isn't actionable until the in-flight one closes, so Continue fires only with no Resume signal. When `Map status` reads Open, the slot becomes "Continue charting" with the next map ticket's title: the build queue doesn't exist until the frontier empties and the spec-to-tickets climb runs.

## The Spec sheet

Named exactly **`Spec`**, beside `Tickets`. A1 `Spec — [Effort name]`; A2 "Specification for the current effort. This sheet is the canonical copy; any exported file is a snapshot."

The sheet is the spec; every later session reads it here. A sibling `.md` beside the workbook is an opt-in snapshot, never canonical.

Content is `/to-spec`'s own output sections, unmodified, one bold 12pt accent-navy header row per section (Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes) with the section's content in col B rows beneath, numbered user stories one per row, hairline `#E5E7EB` row separators, no fills. `/to-tickets` reads these rows as its source.

Visibility is the effort's coarse state, readable from the tab strip: visible beside a live `Tickets` sheet, a climb in progress; visible with no `Tickets` sheet, an interrupted climb; hidden, the effort completed and closed out.

Lifecycle: written by `/to-spec`, the sole author of spec content. When every ticket on `Tickets` is Done, the close-out graduates anything of lasting value to the Agent sheet, then hides the sheet. Deletion is the workbook owner's later call, never made in-session.

## The Tickets sheet

Named exactly **`Tickets`**, beside `Spec`. A1 `Tickets — [Effort name]`; A2 "Work queue for the current effort. Rows flip status; they are never deleted." The sheet is the substrate's tracker backend, chosen by contract, never probed at runtime: an effort's queue never routes to an external tracker because one is reachable.

**The ticket table.** One row per ticket under a bold header row, located by the `ID` header string in column A rather than a fixed row number (content may sit between the title rows and the table). The table sets its own column widths, rows autofit with floor and top-aligned. Rows sit in dependency order, blockers first, so the queue reads top to bottom as walking order; `Blocked by` carries the edges row order can't express. Exact header strings, which other skills match on:

| Header | Holds |
|---|---|
| `ID` | `T1`, `T2`, … assigned once at creation, in dependency order; never renumbered, never reused, because Audit Log blocks, the Handoff sheet, and `Blocked by` cells name them. |
| `Title` | Short descriptive name for the slice. |
| `What it delivers` | The end-to-end behaviour the ticket makes work, from the user's perspective. |
| `Acceptance criteria` | One criterion per line within the cell. |
| `Blocked by` | The T-ids that must be Done before this one starts; blank means it can start now. |
| `Status` | One word from the status grammar below, in its color. |
| `Status date` | Date of the most recent flip. |
| `Gist` | One line written at close: outcome plus pointer. Blank for open rows and most build T-rows; the wayfinding statuses below give it its uses. |

`/to-tickets` authors the rows to its own tracer-bullet rules; the one workbook reading is "every layer": data → formulas → outputs → tie-outs.

**Status grammar.** Exact words in colored text, no fills: **Open** ink `#111827` (created, unclaimed), **In progress** amber `#D97706` (claimed), **Done** green `#16A34A` (acceptance criteria met). With the three wayfinding statuses below, a tally must recognize six words.

**Claim by flip.** A session takes a ticket by flipping `Status` from Open to In progress and setting `Status date`, as its first write; a concurrent session reading the sheet skips the row.

**Work the frontier.** Take the topmost Open ticket whose blockers are all Done (top to bottom for a linear chain).

**Flip, don't delete.** Done rows are queue state; the narrative lives in the Audit Log, whose blocks keep each T-id as a durable referent. No row is ever deleted or renumbered, whatever its status.

**Division of labor.** Created by `/to-tickets`, the sole author of ticket content (titles, deliverables, acceptance criteria, blocking edges); loop skills flip state and never write ticket content. Claimed by the build session. Closed by `/workbook-log`, which reads the row's acceptance criteria into its block and flips the row to Done with date. Detected by `/workbook-explore`.

## Wayfinding operations

How this backend expresses `/wayfinder`, the section that skill's intake consults. One table, one grammar: the map is the `Tickets` sheet's own machinery extended, no second store.

**Map home.** A **map header block** between the title rows and the ticket table (the locate-by-`ID` rule absorbs it), plus the map's tickets as **W-rows** in the one table. When the map precedes the climb, the usual case, the charting session creates the sheet; the post-map climb appends the build queue's T-rows below the W-rows, so the table reads top to bottom as the effort's history. The map at low resolution is the header block plus the table, one bounded read. There is no prose Decisions-so-far: the index of decisions is the Done W-rows read in order via `Gist`, so it cannot drift from the tickets.

**The map header block.** Label rows (label in col A, bold 10pt subtitle gray `#6B7280`; content in col B, 10pt ink, text-wrap; hairline `#E5E7EB` bottom rules), then a blank row before the table's header:

| Label | Holds |
|---|---|
| `Map` | The map's name. |
| `Destination` | The spec, decision, or change the effort is finding its way to, in one or two lines. |
| `Notes` | Compact standing context: domain, skills every session should consult, standing preferences. Lasting context graduates to the Agent sheet rather than accreting here. |
| `Map status` | The detection discriminator: exact word `Open` (amber `#D97706`) or `Closed` (green `#16A34A`). Open W-rows corroborate; this cell is primary. |

**W-rows.** W-prefixed ids (`W1`, `W2`, …) with T-id durability: assigned once in charting order, never renumbered or reused, no collision with the T-rows. `Title` is the ticket's name, prefixed with its type word (`Research:`, `Prototype:`, `Grilling:`, `Task:`). `What it delivers` holds the question. `Acceptance criteria` is usually blank. `Blocked by` is the frontier: the open, unblocked, unclaimed rows are visible from row order plus this column. Claim by flip, work the frontier, and flip-don't-delete apply verbatim.

**The three wayfinding statuses.**

- **Fog**, subtitle gray `#6B7280`: a not-yet-specified patch, loose text in the question cell, no id.
- **Graduated**, blue `#2563EB`: graduate-by-flip. A fog patch that sharpened into tickets flips to Graduated with `Gist` naming the new W-ids, and stays as map history.
- **Out of scope**, gray `#9CA3AF`: work ruled beyond the destination, on a ruled-out ticket row or a standalone row for a ruling that never was a ticket, the one-line why in `Gist`.

A ticket W-row otherwise runs Open → In progress → Done; Done here means resolved.

**Resolving a W-row** is one three-part motion: write the decision-shaped block to the Audit Log (born Complete); flip the row to Done with date; write `Gist` as the one-line answer plus the block pointer, the Audit Log named with the W-id its header carries (`Audit Log · W3`). Then append newly surfaced W-rows, graduate fog the answer made specifiable, and rule mis-scoped rows out of scope. One ticket per session, except research.

**Research.** The session researches itself; the digest is the decision block's Research digest field. Research W-rows may resolve inline alongside the session's one real ticket, and charting's fire-the-subagents step reads: resolve what you can inline, leave the rest on the frontier. A `/research` subagent landing a sibling `.md` is opt-in export, never canonical.

**Assets.** A prototype, mock, or scratch work created while resolving is a prototype or scratch sheet (or mocked-up region) in the workbook, named in the block's Assets field.

**Map close.** When the destination is reached (typically a spec on `Spec` with the build queue appended below the W-rows), flip `Map status` to Closed and point `Destination` at where the effort landed. W-rows end Done, Graduated, or Out of scope; the Done rows remain the effort's permanent rationale index.

## Triage on the Agent sheet

How this substrate expresses `/triage`, the mapping that skill's intake expects; it lives here because onboarding is the substrate's setup motion (`/setup-skills-ef`'s front door routes a workbook to `/workbook-onboarding`). `/triage` itself runs unmodified.

- **The surface is Agent-sheet section 4, Open decisions / pending items**, the workbook's idea inbox. `Tickets` and `Spec` are never triaged: the queue is downstream of triage. A workbook with no Agent sheet yet gets one, built to Sheet conventions, before the first triage write.
- **States are one status word on the line.** An unmarked line is `needs-triage`; triage marks `ready-for-agent` / `ready-for-human` or closes the line out, and the close-out is `wontfix`. `needs-info` is the line waiting on its trigger, which is what section 4 already holds. The category roles (`bug` / `enhancement`) carry no marker; a rejection's disposition applies the distinction.
- **The record is a triage-shaped Audit Log block** (the event: notes plus any brief), while the line keeps the implication: status word + gist + block pointer.
- **Graduation is one-directional.** A `ready-for-agent` item with a live `Tickets` effort is offered as a W-row, the human approving the append; with no live effort it stays marked on its line for `/workbook-plan`'s intake. Nothing flows queue → inbox.
- **Rejection memory is section 6, Out of scope**: one line per rejected concept plus its block pointer, `/triage`'s `.out-of-scope/` knowledge base in sheet form, read by its prior-rejection check on demand and extended only on a rejected-enhancement close (already-implemented and rejected-bug closes take no entry).

`/triage`'s grill step runs `/grilling`, not `/grill-with-files`: its earlier steps already did the file-grounded looking.

## Decision and triage blocks

The Audit Log's second block grammar, shared by W-row resolutions and triage records. Same two-column geometry, status rail, field-row formatting, auto-omit rule, and blank-row separation as the task block in [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md); written whole, born **Complete** (green dot plus word, green rail), no stub lifecycle. Blocks append in chronological order among task blocks.

Header row: col A `● Complete`; col B `DECISION YYYY-MM-DD HH:MM — [W-id] · [Ticket name]` or `TRIAGE YYYY-MM-DD HH:MM — [Item gist]`, ink bold 12pt. The keyword distinguishes the block from task blocks, and pointers match on the W-id or the date (`Audit Log · W3`, `Audit Log · TRIAGE 2026-08-02`). One triage block per item triaged.

| Label (col A) | Content (col B) |
|---|---|
| Question | Decision: the question as charted on the W-row. Triage: the item as it stood on the line. |
| Decision | Decision: the answer as the settled rule. Triage: the state applied (ready-for-agent / ready-for-human / closed out) with the outcome. |
| Rationale | Key reasoning and trade-offs; for triage, also verification results and the redundancy and prior-rejection checks. |
| Rejected | Alternatives ruled out with a one-line why each; for an out-of-scope close, the concept ruled out. Skip if none. |
| Research digest | Decision only, research rows: findings with named sources, the canonical record. Skip if none. |
| Assets | Decision only: in-workbook objects the resolution produced, by name. Skip if none. |
| Agent brief | Triage only, ready-for-agent items: the `/triage` skill's `AGENT-BRIEF.md` structure, disclaimer line included. Skip if none. |
| Surfaced | New W-rows or graduated fog; follow-on inbox items; the W-row a graduation appended. Skip if none. |
