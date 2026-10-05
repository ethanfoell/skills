---
name: workbook-onboarding
description: Open a workbook for the first time and make it understandable. Reads the full structure, surfaces findings, then lays down an Instructions sheet (for humans), an Audit Log (history), and an Agent sheet when there is standing guidance to record. The workbook loop's first-visit mode.
disable-model-invocation: true
---

# /workbook-onboarding

Open an Excel finance workbook for the first time and leave it understandable to humans and agents, so any later session orients instead of re-deriving structure. Onboarding adds documentation sheets; the workbook's own formulas and data stay as found.

## When to use

Use when opening a workbook you will work in again, or when someone hands you one and says "figure out what this does." Skip it for:

- A workbook you will touch once: just read it; lay down no scaffolding.
- An already-onboarded workbook (it has an Instructions sheet): `/workbook-pickup` or `/workbook-explore`. To refresh its meta-sheets, see Re-onboarding below.
- A folder or filing system: `/folder-onboarding`.
- Formula-error or logic auditing: `/formula-audit`, `/logic-audit`. Refactoring structure: `/excel-finance-workbooks`.

## Prerequisites

Call the Skill tool with "excel-finance-workbooks" and follow its "Opening an existing workbook" workflow and intake checklist; it loads the resilient-architecture knowledge this pass leans on.

## Step 1: Read every sheet

Read structure, values, formulas, and formatting. On the Excel add-in, use `get_cell_ranges` with `includeStyles: true` where formatting carries meaning (headers, input cells, conditional formatting) and `get_range_as_csv` for large value-only ranges; on a standalone `.xlsx`, the same reads via openpyxl. Either way, read formulas explicitly for any range that drives calculations. Capture per sheet:

| Question | Capture |
|---|---|
| Purpose | Raw data, calculations, config, output, or reference |
| Layout | What each section holds; where headers end and data begins |
| Formulas vs hardcodes | Which cells are formula-driven vs typed; whether derived values are actually formulas |
| Config/input cells | What a user changes to update the workbook (period selectors, assumptions, toggles) |
| Cross-sheet dependencies | Which sheets reference which; what breaks on a rename or row insert |
| Data sources | ERP, CSV import, manual entry, plugin (Velixo) |
| Plugin connections | Hidden or utility sheets (VelixoReportsConnections, Power Query) naming the system, tenant/environment, and last refresh; easy to miss |
| Stale data | Are display values current? Compare formula-driven columns against any "display" column |
| Frozen panes, filters, hidden | The author's intended view |

Done when you can explain what every sheet does, how data flows between them, and what a user changes in normal use.

## Step 2: Map the architecture

Synthesize:

1. **Data flow**: source, import/staging, config/assumptions, calculations, outputs, and each sheet's place in the chain.
2. **Nerve centers**: the cells everything depends on (a period selector feeding 200 formulas, a mapping table driving every lookup).
3. **Formula patterns**: positional (fragile) or name-based (resilient) lookups; bounded or full-column ranges; circular references; the dominant functions.
4. **Business logic** the labels do not reveal: sign conventions, classification rules, aggregation hierarchies, variance definitions, allocation methods.
5. **Structural risks**: what breaks when rows are inserted, categories added, or data arrives in a different shape.
6. **Complexity**: a simple reporting workbook, or logic encoded in filter combinations and multi-dimensional lookups? If complex, `/logic-audit` is the follow-up to recommend.

Done when you could explain the architecture to a colleague in two minutes.

## Step 3: Surface findings before writing anything

Tell the user what you found and get it confirmed before creating any sheet. Lead with what needs confirmation: business logic embedded in formulas, stale or inconsistent data, structural risks, missing checks or reconciliation, assumptions to validate. Ask:

- Which sheets must not be modified? Establish a **DO NOT EDIT** policy; critical in someone else's workbook.
- What business context is invisible in the formulas: why it is built this way, who else uses it?
- What is the update cadence (monthly, weekly, ad hoc)?

Done when the user has confirmed or corrected your model and any edit restrictions are established.

Steps 4 to 6 write sheets. Format each fully at creation to Sheet conventions (below) and stamp it. Write for the colleagues and auditors who read it long after this session: record the work, not the worker ("documented", "reviewed", "analyzed", with no actor named).

## Step 4: Write the Instructions sheet

The human user guide: a colleague opens the workbook cold and can use it. Sections (trim hard for simple workbooks):

- **A. Purpose & Overview** (2 to 3 sentences): what it does, who it is for, how often it updates.
- **B. Sheet Inventory**: one row per sheet, utility and connection sheets included: name, role, user-editable vs formula-driven.
- **C. Data Flow**: sources to processing to outputs; column groups on complex sheets; config/input cells and what they control; external connections (system, environment, refresh method).
- **D. Key Reference Points**: config cells with current values and what they drive; named ranges, tables, anchors; the cross-sheet dependency map.
- **E. Routine Workflow**: the per-period steps in sequence ("1. Update period in R4. 2. Refresh Velixo. 3. Review check rows."), with refresh/recalc requirements (F9, ribbon buttons).
- **F. Known Issues & Limitations** (optional): failure mode and impact, workarounds, range ceilings that grow into problems. Omit if nothing is user-facing; agent-editing traps go in the Agent sheet.

Be specific (name sheets, columns, cells) and explain why, not just what ("Column Q holds GL account codes because the Velixo formulas filter Acumatica data by them").

Done when a colleague who has never seen the workbook could use it, update it, and troubleshoot basic issues from this sheet alone.

## Step 5: Create the Audit Log

Build it to what `/workbook-log` and `/workbook-plan` write and `/workbook-build` reads:

1. **Title rows** (rows 1 to 2) per Sheet conventions.
2. **Workbook Snapshot** (from row 3, before the first task block; defined here, refreshed by `/workbook-log`): a bold 11pt accent-navy section header, then label/detail rows for Source data; Key totals; Sheet list (each sheet plus a one-line purpose, separated by " · "); Critical dependencies (cell/range feeds, hardcoded limits like "SUMPRODUCT ranges end at row 9055"); Status (ready / in-progress / needs-review).
3. **First task block**, in the block shape of [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md): header `TASK YYYY-MM-DD HH:MM — Onboarded workbook`, status Complete, then Goal, Done, and Sheets touched at minimum, with inline Verified / Flagged / Fixed tags in Done where intake confirmed, flagged, or corrected something.

Route findings by type: dated events from this pass go in the task block's Done field; standing guidance goes to the Agent sheet (Step 6), and a DO NOT EDIT policy also into the snapshot Status when it materially constrains work.

Done when the Audit Log has the title rows, a populated Workbook Snapshot, and one Complete task block that a future `/workbook-log` or `/workbook-plan` can extend without reformatting.

## Step 6: Create the Agent sheet, when earned

Create the Agent sheet only when Step 3 surfaced something to record that is verifiable from the workbook or confirmed by the user: a plugin convention or gotcha (refresh method, ledger-name casing, period format, parameter-order quirks), a DO NOT EDIT policy, a stated preference. Otherwise leave it for `/workbook-log`, which creates it on the first standing rule; a cold first read does not earn Active risks or Open decisions.

When you create it, lay down all six sections from Sheet conventions, seeded where earned and placeholdered elsewhere. Write the standing rule, not who follows it: "Refresh Velixo before tie-outs."

Done when the sheet is absent, or exists with all six sections and nothing an auditor would read as guessed.

## Step 7: Report

Summarize what was created (Instructions, Audit Log, Agent if any; merges vs fresh writes), the top 3 to 5 findings ranked by importance, and next steps: `/logic-audit` for complex business logic, `/formula-audit` for formula errors, specific recommendations for structural improvements.

Done when the user knows what was built, what was found, and what to do next.

## Adapting to complexity

- **Simple** (1 to 3 sheets, straightforward formulas): one pass through Steps 1 to 5; a 15 to 20 row Instructions sheet; a brief Audit Log. Manufacture no sections.
- **Complex** (many sheets, cross-sheet dependencies, embedded logic, ERP integrations): multiple read passes per step; a 40+ row Instructions sheet; recommend `/logic-audit`.
- **With plugins** (Velixo, Power Query): document connection details, refresh requirements, case sensitivity, and parameter-order quirks; future sessions need them to avoid silent failures.

## Re-onboarding and template migration

Re-running on an already-onboarded workbook (the Re-onboard route `/workbook-explore` names) re-reads structure and updates the existing meta-sheets: read them first, treat them as the owner's source of truth, and propose additions rather than overwriting.

Check each meta-sheet's template stamp (the `template v2` note on A1; an absent note reads as pre-v2). For a sheet built to an older standard, propose a content-preserving reformat (palette, font, geometry, layout, autofit; every row of content untouched), name what would change, and wait for an explicit yes. Declined: note it and move on. Accepted: reformat, re-stamp each migrated sheet, and log the migration as a Complete task block listing the migrated sheets under Sheets touched.

## Multi-session efforts

A workbook whose effort went up the stairs to a multi-session climb gains `Spec` and `Tickets` sheets, created by the `/to-spec` and `/to-tickets` runs or a wayfinder charting session, never by onboarding. Their sheet contracts, the wayfinder map's home, the session-start detection, and the `/triage` mapping on the Agent sheet are in [`MULTI-SESSION.md`](MULTI-SESSION.md).

## Sheet conventions

The four meta-sheets, by exact name (other skills match on these strings):

| Sheet | A1 title | Position | A1 treatment | A2 subtitle | Tab |
|---|---|---|---|---|---|
| `Instructions` | `Instructions` (or a name fitting the workbook's convention) | unpinned | bold 18pt accent navy on white, navy rule under the row | none fixed | accent navy |
| `Agent` | `Agent — [Workbook Name]` | unpinned | as Instructions | Standing operating guidance for maintaining this workbook. | accent navy |
| `Audit Log` | `Audit Log — [Workbook Name]` | unpinned | as Instructions | Running record of changes per task. See Agent sheet for current operating guidance. | accent navy |
| `Handoff` | `HANDOFF — [Workbook Name]` | last sheet, for discovery | bold 16pt white on alert-orange fill across both columns (the one filled title) | Active handoff. If you're picking up this task in a new session, read this first. | alert orange |

Handoff is created by `/workbook-handoff`, surfaced by `/workbook-explore` next session (Resume, or close-out as Cancelled), and deleted by `/workbook-log` at task close; its block format is the `/workbook-handoff` skill's `HANDOFF-FORMAT.md`.

Shared rules:

- Aptos, with Calibri named explicitly as the fallback. Subtitles 10pt subtitle gray; section headers bold 12pt accent navy.
- Col A labels 200px (bold 10pt subtitle gray); col B content 600px (10pt ink, text-wrap on). Hairline bottom rules separate rows; no fills.
- Rows autofit with a 20px floor; the title row is held at 28px. Content rows top-aligned; title and block-header rows vertically centered.
- Wide-table exception: a genuinely multi-column table sets its own widths and keeps the autofit-with-floor and alignment rules; merged narrative rows keep manual heights, since Excel cannot autofit merged cells reliably.
- Template stamp: a cell note reading `template v2` on A1, written by the creating skill.
- Overlap rule: an event goes in the Audit Log, dated; the standing rule it implies goes in the Agent sheet.

Palette (status and tag colors live in [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md)):

| Token | Hex | Used for |
|---|---|---|
| Accent navy | `#1E3A8A` | Titles and title rules, section headers, the Workbook Snapshot label; text and rules only, never a fill; the Instructions, Agent, and Audit Log tabs |
| Alert orange | `#EA580C` | The Handoff title banner (the one fill), the Handoff tab, handoff block metadata and rail |
| Ink | `#111827` | Content text; task titles |
| Subtitle gray | `#6B7280` | A2 subtitles; field-row labels |
| Hairline | `#E5E7EB` | Field-row and section separators |

A workbook may re-theme these tokens to company branding; record the override in the Agent sheet's User preferences for this workbook, so later sessions apply the workbook's palette. Status colors stay mapped to their states whatever the theme.

**Agent sheet sections**, exact names, headers kept even when empty:

1. Operating conventions
2. Workbook-specific gotchas
3. Active risks
4. Open decisions / pending items
5. User preferences for this workbook
6. Out of scope

An empty section carries one placeholder line: "None recorded yet; added by `/workbook-log` as they surface." Section 6 has a different writer, so its placeholder reads "None recorded yet; added by `/triage` as rejections land." Sections 4 and 6 double as `/triage`'s inbox and rejection memory.
