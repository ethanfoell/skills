---
name: workbook-onboarding
description: Open a workbook for the first time and make it understandable — read the full structure, lay down an Instructions sheet (humans), an Audit Log (history), and an Agent sheet (standing guidance), and surface findings. The workbook loop's first-visit mode.
disable-model-invocation: true
---

# /workbook-onboarding

Open an Excel finance workbook for the first time and make it understandable — to humans and agents — so any later session orients instead of re-deriving structure. The first-visit counterpart to `/workbook-pickup`, and the Onboard route `/workbook-explore` names.

The skill adds four meta-sheets a workbook didn't have, each with a distinct audience — defined once in the [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md) reference:

- **Instructions** — the human-facing user guide: what the workbook does, how it's built, how to use it.
- **Audit Log** — the dated, append-only record of what was done per task (continuity across sessions).
- **Agent** — the standing operating manual synthesized across sessions: conventions, gotchas, risks, decisions.
- **Handoff** — an in-flight task paused for a future session (transient; created by `/workbook-handoff`, not here).

Two more sheet contracts live in this hub without an onboarding step: [`SPEC-SHEET.md`](SPEC-SHEET.md) and [`TICKETS-SHEET.md`](TICKETS-SHEET.md) define the conditional **Spec** and **Tickets** sheets a multi-session effort adds via the `/to-spec` and `/to-tickets` runs — the Tickets sheet doubling as the home of a wayfinder map, per its contract's Wayfinding operations section. A third, [`BASELINE-SHEET.md`](BASELINE-SHEET.md), defines the transient **Baseline** sheets a destructive `/workbook-build` captures and `/workbook-log` clears. This skill owns their contracts — the sheet-layer hub owns the specs of the workbook's contract sheets — but never creates the sheets.

**Self-format at creation.** This skill leaves every sheet it creates fully formatted to the sheet contract — typography, geometry, autofit with the floor, alignment, tab color — and stamps each with the template-version cell note on its title cell (per [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md)). The loop splits formatting by phase: this skill and `/workbook-handoff` self-format the sheets they create; `/workbook-build` defers formatting mid-task; `/workbook-log` runs the finalization pass at close.

**Write every output sheet as a knowledgeable analyst would.** These sheets are the workbook's documentation, read by colleagues, auditors, and future maintainers long after the session that wrote them. Record the work, not the worker: "documented", "reviewed", "analyzed" — never AI, automation, Claude, or "this tool".

## When to use

Use when opening a workbook you'll work in again and want it understandable — or someone hands you one and says "figure out what this does." Skip it for:
- A workbook you'll touch once → just look at it; don't lay down scaffolding.
- An already-onboarded workbook (has an Instructions sheet) → `/workbook-pickup` or `/workbook-explore`.
- A folder or filing system → `/folder-onboarding`.
- Formula-error or logic auditing → `/formula-audit`, `/logic-audit`. Refactoring structure → `/excel-finance-workbooks`.

## Prerequisites

Run `/excel-finance-workbooks` first — follow its "Opening an existing workbook" workflow and intake checklist. (Model-invoked; it loads the resilient-architecture knowledge this pass leans on.)

## Step 1: Read every sheet

Read structure, values, formulas, and formatting. For each sheet, capture:

| Question | What to capture |
|---|---|
| **Purpose** | Its role — raw data, calculations, config, output, reference |
| **Layout** | What's in each section; where headers end and data begins |
| **Formulas vs hardcodes** | Which cells are formula-driven vs manually entered; are derived values actually formulas? |
| **Config/input cells** | Which cells a user changes to update the workbook (period selectors, assumptions, toggles) |
| **Cross-sheet dependencies** | Which sheets reference which; what breaks on a rename or row insert |
| **Data sources** | ERP, CSV import, manual entry, API/plugin (Velixo) |
| **Plugin connections** | Hidden/utility sheets configuring external connections (VelixoReportsConnections, Power Query) — easy to miss, critical: they name the system, tenant/environment, and last refresh |
| **Stale data** | Are display values current? Compare formula-driven columns against any "display" column |
| **Frozen panes/filters** | What's frozen, filtered, or hidden — it reveals the author's intended view |

**Read method:** on the Excel add-in, `get_cell_ranges` with `includeStyles: true` where formatting carries meaning (headers, input cells, conditional formatting) and `get_range_as_csv` for large value-only ranges; on a standalone `.xlsx` from the filesystem, the same reads via openpyxl (values, formulas, and styles all reachable). Either way, read formulas explicitly for any range that drives calculations.

Done when: you can explain what every sheet does, how data flows between them, and what a user changes in normal use.

## Step 2: Map the architecture

Synthesize into a model you could explain in two minutes:

1. **Data flow** — source → import/staging → config/assumptions → calculations → outputs; each sheet's position in it.
2. **Nerve centers** — the cells everything depends on (a period selector feeding 200 formulas, a mapping table driving all lookups).
3. **Formula patterns** — lookups positional (fragile) or name-based (resilient); ranges bounded or full-column; circular references; which functions dominate (SUMIFS, XLOOKUP, Velixo, SUMPRODUCT).
4. **Business logic** — decisions encoded in formulas that labels don't reveal: sign conventions, classification rules, aggregation hierarchies, variance definitions, allocation methods.
5. **Structural risks** — what breaks if rows are inserted, categories added, or data arrives in a different format.
6. **Complexity** — a simple reporting workbook, or one encoding complex logic in filter combinations and multi-dimensional lookups? If complex, note `/logic-audit` as a follow-up.

Done when: you could explain the workbook's architecture to a colleague in two minutes.

## Step 3: Surface findings — before writing anything

Tell the user what you found and confirm it before creating sheets. Prioritize: business logic that needs confirmation (classification rules, sign conventions embedded in formulas); stale or inconsistent data; structural risks (positional dependencies, duplicated lists, undocumented ceilings); missing checks or reconciliation; assumptions you'd need validated. Ask:
- Are there sheets that should **NOT** be modified? (Establish a **DO NOT EDIT** policy — critical in someone else's workbook.)
- Business context invisible in the formulas — *why* it's built this way, who else uses it?
- The intended update cadence (monthly, weekly, ad hoc)?

Done when: the user has confirmed or corrected your model, and any edit restrictions are established.

## Step 4: Write the Instructions sheet — the human surface

Create a sheet called "Instructions" (or a name fitting the workbook's convention) that lets any colleague open the workbook cold and use it.

**Required sections** (adapt; trim hard for simple workbooks):

- **A. Purpose & Overview** (2–3 sentences) — what it does, who it's for, how often it's updated.
- **B. Sheet Inventory** — one row per sheet: name, role, user-editable vs formula-driven. **Every** sheet, even utility/connection ones — a colleague needs to know they exist and why.
- **C. Data Flow** — how data moves (sources → processing → outputs); column groups for complex sheets; config/input cells and what they control; external connections (system, environment, refresh method).
- **D. Key Reference Points** — config cells with current values and what they drive; named ranges, tables, anchors; the cross-sheet dependency map.
- **E. Routine Workflow** — step-by-step for each period ("1. Update period in R4. 2. Refresh Velixo. 3. Review check rows."), in sequence, with refresh/recalc requirements (F9, ribbon buttons).
- **F. Known Issues & Limitations** *(optional)* — anything affecting reliability, workarounds, range ceilings that grow into problems. Omit if nothing user-facing. (Agent-editing traps go in the Agent sheet, not here.)

**Formatting:** Aptos (Calibri fallback); title bold 18pt accent navy `#1E3A8A` with a navy rule under the title row; section headers bold 12pt navy; labels (col A) bold 10pt subtitle gray `#6B7280`, 200px; details (col B) normal 10pt ink, 600px wrap; hairline `#E5E7EB` row separators — no fills. Geometry, alignment, and tab color per [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md).

**Tone — human-neutral.** Write for a colleague; be specific (name sheets, columns, cells); explain *why*, not just *what* ("Column Q holds GL account codes because the Velixo formulas filter Acumatica data by them"). Record the work, not the worker.

Done when: a colleague who's never seen the workbook could read this and know how to use it, update it, and troubleshoot basic issues.

## Step 5: Create the Audit Log

Create the Audit Log sheet. Its sheet identity (title rows, palette) comes from [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md); its task-block format from [`AUDIT-LOG-FORMAT.md`](AUDIT-LOG-FORMAT.md) — both canonicals this skill owns. Build it to match what `/workbook-log` and `/workbook-plan` write and `/workbook-build` reads.

- **Instructions** = how to USE the workbook (for colleagues).
- **Audit Log** = what was DONE to it and why, dated (continuity across sessions).

Populate:

1. **Header (rows 1–2)** — title + subtitle per the sheet contract.
2. **Workbook Snapshot** (starts row 3, between header and the first task block): bold 11pt accent-navy section header, then label/detail rows for — Source data; Key totals; Sheet list (each sheet + one-line purpose, separated by " · "); Critical dependencies (cell/range feeds, hardcoded limits like "SUMPRODUCT ranges end at row 9055"); Status (ready / in-progress / needs-review). This is the snapshot `/workbook-log` reads and refreshes.
3. **First task block** documenting this onboarding pass, in the contract's task-block format: header row `TASK YYYY-MM-DD HH:MM — Onboarded workbook`, status **Complete**, then field rows (Goal, Done, Sheets touched at minimum). Use inline **Verified** / **Flagged** / **Fixed** tags in Done where intake confirmed, flagged, or corrected something.

**Where intake findings go** — route by type, don't dump everything here:
- **Dated events from this pass** (reviewed / Verified / Flagged / Fixed) → the onboarding task block's Done field.
- **Standing conventions, gotchas, risks, decisions, preferences** → the **Agent sheet** (Step 6). The Audit Log is history; the Agent sheet is the standing manual. Don't duplicate.
- **DO NOT EDIT policy**, if the user established one → the Agent sheet under User preferences, and flag it in the snapshot Status if it materially constrains work.

Done when: the Audit Log has the contract header, a populated Workbook Snapshot, and one Complete task block for the onboarding pass — and a future `/workbook-log` or `/workbook-plan` could extend it without reformatting.

## Step 6: Create the Agent sheet

Create a sheet named exactly **"Agent"** — the standing operating manual for whoever maintains the workbook across sessions. The Audit Log is history; the Agent sheet is the lessons distilled from it. Keep them complementary — a dated event in the Audit Log, the standing rule it implies here. Don't duplicate.

**Required sections** (exact names — other skills read these, per the sheet contract):

1. **Operating conventions** — standing rules ("Refresh Velixo before any tie-out; F9 does not refresh Velixo formulas").
2. **Workbook-specific gotchas** — easy-to-miss facts that cause silent errors ("Velixo ledger names are case-sensitive: 'Actual' works, 'ACTUAL' returns #N/A").
3. **Active risks** — persistent risks with status.
4. **Open decisions / pending items** — things awaiting a future trigger ("Revisit Q4 assumption when April actuals arrive").
5. **User preferences for this workbook** — confirmed preferences and edit policies ("DO NOT EDIT the GL_Tie sheet — owned by Dana").
6. **Out of scope** — rejection memory: one line per rejected concept plus its Audit Log block pointer. Written and read by `/triage` on demand — never part of the session-start read.

Sections 4 and 6 double as the workbook's triage surface: section 4 is the idea inbox `/triage` runs over (an unmarked line is untriaged), section 6 its rejection memory. The full role mapping and one-directional graduation rule are recorded in [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md)'s Triage-on-the-Agent-sheet section.

**The confidence line — seed only what's earned.** Seed a section only when the content is **verifiable from the workbook** or **confirmed by the user** in Step 3:
- **Seed now** — plugin conventions and gotchas surfaced in Steps 1–3 (refresh method, ledger-name casing, period format, parameter-order quirks); any DO NOT EDIT policy (→ User preferences); any preference the user stated.
- **Leave for `/workbook-log`** — Active risks and Open decisions, unless the user named one. Don't infer them from a cold first read.

For a section with nothing to seed, write one placeholder line: "None recorded yet — added by `/workbook-log` as they surface." (Out of scope has a different writer — its placeholder reads "None recorded yet — added by `/triage` as rejections land.") Keep the header so the structure stays stable for the skills that read it.

**Voice — neutral operator.** Write the standing rule, not who follows it: "Refresh Velixo before tie-outs," not "Claude should refresh Velixo." Conventions, gotchas, risks, decisions, and preferences all read cleanly in neutral voice. Title row, section-header style, and field-row formatting follow the sheet contract — don't re-spell hexes here.

Done when: the Agent sheet exists with all six sections, seeded only with verifiable/confirmed content, the rest placeholdered, and nothing reading as out of place to an auditor.

## Step 7: Report

Summarize: **what was created** (Instructions / Audit Log / Agent — note merges vs fresh writes); **top 3–5 findings** ranked by importance (risks, stale data, structural issues, DO NOT EDIT areas); **suggested next steps** — `/logic-audit` if complex business logic was detected, `/formula-audit` if formula errors were found, specific recommendations if structural improvements are needed.

Done when: the user knows what was built, what was found, and what to do next.

## Adapting to complexity

- **Simple** (1–3 sheets, straightforward formulas): Steps 1–5 in one pass; a 15–20-row Instructions sheet; a brief Audit Log. Don't manufacture sections.
- **Complex** (many sheets, cross-sheet dependencies, embedded logic, ERP integrations): multiple read passes per step; a 40+-row Instructions sheet; recommend `/logic-audit` as a follow-up — decoding tribal knowledge and finding overlaps/gaps is where the highest value often lies.
- **With plugins** (Velixo, Power Query): document connection details, refresh requirements, case sensitivity, and parameter-order quirks — future sessions need these to avoid silent failures.

## Re-onboarding and template migration

Re-running onboarding on an already-onboarded workbook (the Re-onboard route `/workbook-explore`
names) re-reads structure and updates the existing meta-sheets — read them first and treat them as
the owner's source of truth, per What NOT to do below.

On re-onboard, check each meta-sheet's **template version** — the cell note on its A1 title cell
(per [`SHEET-CONTRACTS.md`](SHEET-CONTRACTS.md); an absent note reads as pre-v2). When a sheet was
built to an older standard, **propose** a content-preserving reformat to the current one: palette,
font, geometry, layout, autofit — every row of content untouched (Audit Log history, Agent
guidance, Instructions prose all preserved). **Never reformat unprompted** — reformatting
someone's sheets without asking is surprising; name what would change and wait for an explicit
yes. Declined means the sheets keep their current look — note it and move on.

On acceptance: reformat, re-stamp the version note on each migrated sheet, and log the migration
as a task block in the Audit Log (status Complete, Sheets touched listing the migrated sheets).

## What `/workbook-onboarding` does NOT do

- Modify the workbook's formulas or data — it only adds documentation sheets.
- Overwrite an existing Instructions / Agent sheet — read it first, treat it as the owner's source of truth, propose additions.
- Formula-error auditing (`/formula-audit`) or business-logic decoding (`/logic-audit`).
- Rebuild or refactor the workbook's structure.

## Quality checklist

- [ ] Every sheet appears in the Instructions Sheet Inventory, marked user-editable or formula-driven
- [ ] Config/input cells documented with current values; routine workflow specific enough to follow without asking
- [ ] Known issues include the failure mode and impact, not just "there's a problem"; external connections documented (system, environment, refresh method)
- [ ] Audit Log built from the two reference contracts: contract header + populated Workbook Snapshot + one Complete onboarding task block
- [ ] Agent sheet has all six sections; seeded only with verifiable/confirmed content, the rest placeholdered for `/workbook-log` (Out of scope for `/triage`)
- [ ] Every output sheet (Agent sheet included) records the work, not the worker — no actor references (AI, automation, Claude, "this tool")
- [ ] DO NOT EDIT policy recorded in the Agent sheet if the user established one
- [ ] Follow-up recommendations included (`/logic-audit`, `/formula-audit`) based on complexity
