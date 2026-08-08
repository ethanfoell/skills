---
name: excel-finance-workbooks
description: Build, audit, maintain, and refactor Excel finance workbooks — budget vs. actuals, forecasts, reconciliations, and reporting models. Use when creating a new finance workbook, opening an existing one for the first time, reviewing whether its structure supports reliable ongoing use, refactoring fragile formulas or sheet dependencies, or maintaining a workbook across multiple AI sessions.
---

# Excel Finance Workbooks

Principles, patterns, and failure modes for building and maintaining Excel finance workbooks that are resilient, auditable, and maintainable by both a financial analyst and an AI across multiple sessions.

## Intake before intervention

**Always inspect before changing.** Before modifying any workbook — even if the user describes what they want — read it and understand its current state. This applies whether you built it or not.

### What to examine

1. **Purpose and audience.** What decisions does this workbook support? Who uses it? How often?
2. **Sheet inventory.** Name, role, and rough content of every sheet. Identify which hold raw data, assumptions, calculations, checks, and outputs.
3. **Data flow.** Trace how data moves: source → import → categorization → aggregation → output. Identify cross-sheet references.
4. **Formula architecture.** Are lookups positional or name-based? Ranges bounded or full-column? Derived values formulas or hardcoded? Any circular references?
5. **Manual inputs.** Which cells does the user edit directly? Are they visually distinguished (blue text, yellow fill)?
6. **Hardcoded values.** Assumptions, thresholds, mappings, or constants embedded in formulas rather than in dedicated cells.
7. **Checks and reconciliation.** Does anything verify the workbook is internally consistent?
8. **Existing audit trail.** Is there an Audit Log, change history, or documentation sheet?
9. **Known fragility.** What breaks if a row is inserted, a category added, a new period starts, or data arrives in a slightly different format?

### What to surface

After intake, tell the user what you found — especially:
- Business logic embedded in formulas that the user should confirm (classification rules, sign conventions, aggregation choices)
- Assumptions you'd need the user to validate before proceeding
- Structural risks (positional dependencies, duplicated lists, undocumented ceilings)
- Missing checks or reconciliation

**Never silently decide business logic.** Category structures, classification rules, sign conventions, forecast assumptions, allocation methods — propose them and get confirmation. These are business decisions, not implementation details.

## Core design principles

### 1. Separate concerns across sheets

Organize sheets by role, keeping these layers distinct:

- **Raw data** — imported transactions, journal entries, trial balances, ERP extracts. Preserved as-is or normalized through a documented staging process; never manually edited ad hoc.
- **Assumptions and mappings** — budget targets, growth rates, category master lists, account mappings, period definitions. Clearly marked as user-editable inputs.
- **Calculations** — formulas that aggregate, classify, compare, or derive. No manual edits.
- **Checks** — reconciliation, validation, and health checks. Automated formulas that flag problems.
- **Outputs** — dashboards, summaries, variance reports. Read-only views driven by formulas.
- **Audit Log** — session history, design decisions, known risks. Append-only.

Not every workbook needs all six layers — a simple reconciliation might have three sheets. But when layers mix — assumptions buried in formula sheets, manual overrides scattered across output tabs — fragility follows.

### 2. Establish intentional sources of truth

Any value that appears in more than one place needs a single authoritative source: category lists, account lists, period definitions, mappings (source→reporting category, account→group rollups), and assumptions (growth rates, allocation percentages, exchange rates, thresholds).

Create a dedicated reference sheet (or section) where these are defined once. Every other sheet pulls via formula, Named Range, or data validation — never by retyping the same list. When a user adds a category, renames a department, or updates an assumption, it should propagate everywhere automatically. Duplicated lists drift silently.

### 3. Name-based lookups over positional references

This is the single most important structural principle for resilient finance workbooks.

**The failure mode:** Formula `=Budget!C5` assumes row 5 on Budget is the same category as row 5 on Dashboard. Insert a row, reorder categories, or add a new one on either sheet, and the variance math silently compares wrong categories. No error. No warning. Wrong numbers.

**The fix:** Use name-based lookups — XLOOKUP, SUMIFS, INDEX/MATCH, SUMPRODUCT with criteria arrays, or FILTER — to find values by matching on the category (or account, or period) name:

```
=XLOOKUP(A5, Budget!$A$5:$A$25, Budget!C$5:C$25, 0)
=SUMIFS(Budget!C$5:C$25, Budget!$A$5:$A$25, A5)
```

These find "Groceries" on the Budget sheet by name regardless of its row. Inserting, deleting, or reordering rows on either sheet doesn't break them. **Apply this everywhere:** variance formulas, KPI aggregations, balance lookups, any cross-sheet reference where the join key is a name or label.

### Formula preference: modern Excel 365 functions

Use modern Excel 365 formulas where they improve clarity and resilience: LET (intermediate variables), XLOOKUP (over INDEX/MATCH and VLOOKUP), FILTER, UNIQUE, SORT, TEXTSPLIT, BYROW, CHOOSECOLS, VSTACK/HSTACK, and other dynamic-array functions.

SUMPRODUCT is valid and sometimes ideal — especially for multi-criteria conditional sums against non-Table ranges — but it is not the default for every lookup. Where SUMIFS, XLOOKUP, structured references, or dynamic-array formulas are clearer, prefer those. Choose the formula that most directly expresses the intent.

Provide paste-ready formulas without inline comments; keep them readable through LET naming or clear cell layout rather than comment annotations.

### 4. Use Excel Tables for growing data

Any sheet that accumulates rows over time — transactions, journal entries, balance snapshots, import logs — should be an Excel Table (Insert → Table, or `ListObject` in openpyxl). Benefits: auto-expanding ranges, built-in filtering, structured references, automatic formatting for new rows — eliminating the "new data falls outside the formula range" problem.

**When Tables aren't right:** small reference lists (5–10 rows that rarely change), complex merged-cell layouts, or workbooks where Table behavior conflicts with existing structure. Tables are a strong default, not a universal mandate.

### 5. Manage formula range boundaries deliberately

Full-column references (`F:F`) in array-style formulas like SUMPRODUCT cause #VALUE! errors when the column has mixed types or exceeds calculation limits. Prefer:

- **Excel Tables with structured references** (`Transactions[Amount]`) where possible — these auto-expand.
- **Bounded ranges with documented headroom** (`F$2:F$5000`) when Tables aren't feasible. Choose a ceiling that gives years of growth at the expected data volume.
- **Document the ceiling** in the Audit Log and Instructions sheet so future sessions know to extend it.

Never use unbounded ranges in SUMPRODUCT, SUMIFS across mixed-type columns, or programmatically generated formulas. The failure is silent until it isn't.

### 6. Make derived values formula-driven

If a value can be calculated from other data in the workbook, it should be a formula — not a manually entered value. Common candidates:

- **Period columns** — `=TEXT(A2,"YYYY-MM")` instead of free-text month entry
- **Effective category** — `=IF(Override<>"", Override, AutoCategory)` so overrides flow through without losing the original
- **Running balances** — formula-driven from opening balance + period activity
- **Variance** — always `Actual - Budget` (with a documented sign convention), never manually calculated

Manual entry of derived values risks both staleness and inconsistency with its inputs. Formulas eliminate both.

### 7. Enforce valid inputs with data validation

Dimension columns users edit directly — category, account, department, status, anything that feeds a lookup, aggregation, or filter — should have a validation dropdown restricting entries to the source-of-truth list. Use **Named Ranges** (`=CategoryNames`) pointing to the master list as the validation source — more universally compatible than structured table references, especially in programmatically generated workbooks.

For raw imported data, dropdowns may not be practical (bulk data shouldn't require manual entry); instead validate imported dimension values with checks — orphan detection, fuzzy-match flagging, or COUNTIF against the master list — so mismatches surface without blocking the import. Free-text in user-editable dimension columns creates orphans: a category typed "Dinning" instead of "Dining" silently falls out of every aggregation.

### 8. Build a Checks sheet

A dedicated Checks or Reconciliation sheet should be the default for any workbook that is recurring, shared, or supports ongoing decisions. Essential checks:

- **Orphan values** — dimensions in the data that don't match the master list
- **Duplicate detection** — COUNTIFS on date + amount + description (or equivalent natural key) to flag double-imports
- **Formula health** — spot-check that derived columns still contain formulas, not overwritten values
- **Completeness** — count of uncategorized, unclassified, or unreviewed items
- **Reconciliation** — monthly totals by account for comparison against statement activity
- **Balance tie-out** — computed ending balance (opening + activity) vs. reported ending balance

Format checks with conditional formatting: green for passing, yellow/red for attention. The goal is a single sheet that answers "is this workbook internally consistent right now?" For a lightweight one-off, a full Checks sheet may be overkill — but at minimum, verify key totals against source data before sharing results.

### 9. Sign convention: decide once, document everywhere

Different sources use different sign conventions — credit cards may show purchases as positive, bank accounts show debits as negative, some systems net everything. **Pick one convention and enforce it at import time:**
- Common choice: money in = positive, money out = negative
- Alternative: follow GAAP/accounting sign conventions for the account type

**Document the convention** in the Instructions sheet, the Audit Log, and any import scripts. If a source requires sign flipping at import (credit-card purchases arriving as positive need negating), document that transformation explicitly. Never leave sign convention for downstream formulas to sort out — that's a breeding ground for double-counted or missing amounts.

### 10. Design for gaps between sessions

Finance workbooks are typically updated periodically — monthly, bi-weekly, quarterly — not daily. The design must let a user (or AI) return after weeks and pick up without loss of context:

- **Instructions sheet** with the routine workflow, column mappings per data source, sign convention, and troubleshooting
- **Audit Log** with session history and design decisions (see below)
- **Clear sheet and table names** that describe their role without explanation
- **Visual conventions** — blue text for inputs, yellow fill for assumptions, consistent header styling
- **No tribal knowledge** — nothing that only works if you "just know" column G matters or the Budget sheet must be sorted a certain way

## Audit log as AI collaboration infrastructure

The Audit Log is not just documentation — it's the mechanism that makes multi-session AI collaboration possible. Without it, every new session starts from scratch: re-reading the workbook, guessing at design intent, risking undoing intentional choices.

### What the Audit Log enables

- A new AI session can read it and understand *why* the workbook is structured this way, not just *how*
- Design decisions are preserved — "we use name-based lookups instead of positional references because…" stops a future session from "simplifying" back to fragile patterns
- Known risks carry forward until resolved, not forgotten between sessions
- The user has one place to check what changed and when

For the block format — the Workbook Snapshot, the per-task blocks, the status tags — follow the Audit Log spec that `/workbook-plan` and `/workbook-log` apply; don't restate it here. The rules that bear on *how you write*, not just the layout:

- **Append only** — never delete or overwrite previous task blocks
- **Carry forward** unresolved risks from prior sessions; mark resolved items with date
- **Document *why*, not just *what*** — "Changed variance formula from positional to SUMPRODUCT name-match because inserting a category row broke the old formula silently" is useful; "Updated formulas" is not
- **Update the Workbook Snapshot** when anything material changes (new sheets, new dimensions, changed dependencies). Standing design decisions and known risks live in the Agent sheet, not repeated in each block.

## Refactoring judgment

### Preserve functional layouts

When a user's existing layout and workflow are functional and low-risk, preserve them. The goal is to make the workbook more resilient, not to refactor it into an idealized architecture. Restructuring a working layout imposes learning costs, breaks muscle memory, and can introduce errors — all for marginal benefit. Reserve architectural changes for cases where the current structure creates material risk of silent errors, blocks a needed capability, or causes compounding maintenance problems across sessions.

### When to refactor vs. patch

**Patch** when the issue is isolated to one cell or formula with no downstream dependents, the fix doesn't change structural assumptions, or the effort to refactor exceeds the risk of the current state.

**Refactor** when:
- The same fragility pattern appears in multiple places (e.g. positional references across 200+ formulas)
- A fix in one place would require matching changes in multiple other sheets
- The user needs to add, remove, or reorder dimensions and the current structure can't accommodate that without breaking
- The workbook will be maintained over multiple sessions and the current architecture creates compounding risk

### How to refactor safely

1. **Audit first.** Map every cross-sheet dependency and formula pattern before changing anything. Identify the full blast radius.
2. **Plan holistically.** If fragility is systemic, don't fix issues one at a time — a coordinated plan that addresses all related issues together. Piecemeal fixes create inconsistent states.
3. **Preserve a backup.** Before a major refactor, save a copy. The user should be able to revert.
4. **Verify after.** Recalculate all formulas and scan for errors (#REF!, #VALUE!, #DIV/0!, #NAME?, #N/A) after any structural change. Compare key totals before and after to confirm no data was lost or altered.
5. **Update the Audit Log.** Document what changed, why, and what the new architecture looks like.

### Materiality judgment

Not every issue is worth fixing. Prioritize by:

- **Risk of silent failure** — problems that produce wrong numbers without any visible error are highest priority
- **Downstream impact** — a broken formula in a KPI cell matters more than a formatting issue on a reference sheet
- **Frequency of exposure** — an issue triggered every time data is added matters more than a rare edge case
- **Effort to fix vs. work around** — a 5-minute formula change, do it; if it requires rebuilding three sheets, weigh that against the actual risk

## Category and dimension design

Category structures should reflect the user's real-world reporting needs, not generic defaults — every user has domain-specific classification requirements.

- **Ask before assuming.** Propose a starting category list based on the data, but confirm before building the workbook around it.
- **Include a catch-all.** Every dimension list needs an "Uncategorized" or "Other" bucket so nothing falls through silently.
- **Design for override.** Users will reclassify items — provide an override column that preserves the original classification while letting the user's judgment take precedence.
- **Type the dimension.** If categories have a natural grouping (Income vs. Expense vs. Transfer; Fixed vs. Variable; Operating vs. Non-operating), add a Type column to the master list. This enables dynamic KPIs that automatically include new categories of the right type.

## Finance model judgment

Finance workbooks encode assumptions beyond formulas and layout. When building or reviewing a budget-vs-actuals, forecast, variance analysis, reconciliation, or reporting model, surface and confirm these domain-level decisions:

- **Actuals sources.** GL export, ERP trial balance, bank feeds, manual entry? Pre- or post-close? Adjusting entries included? Confirm the data represents what the user thinks it does.
- **Budget and forecast versions.** One budget or multiple (original, revised, latest estimate)? Which drives variance? How are forecast updates handled — overwrite, or versioned snapshots?
- **Reporting periods.** Fiscal year start, period boundaries, interim vs. full-year. Calendar months or custom (4-4-5, 13-period)? How are partial periods handled?
- **GL and account mappings.** How do source account codes roll up to reporting line items? Is the mapping in the workbook, the ERP, or both? Who owns changes?
- **Manual adjustments.** Manual journal entries, reclassifications, top-side adjustments — where do they live, and how are they distinguished from system-sourced data?
- **Variance definitions.** Favorable/unfavorable convention — actual minus budget, or budget minus actual? Does it flip for revenue vs. expense? Is percentage variance based on budget, actual, or the larger of the two?
- **Tie-outs to source systems.** Key totals should reconcile to a source-system total (ERP trial balance, bank statement, sub-ledger balance). Identify which totals to tie out and where the control numbers come from.
- **Forecast assumptions.** Growth rates, seasonality, headcount plans, pricing changes — anything driving forward-looking numbers belongs in dedicated, auditable cells, not buried in formulas.

These are business decisions, not implementation details. Propose reasonable defaults based on the data and context, but confirm before building the model around them.

## Data import and normalization

When importing financial data from external sources (CSVs, PDFs, bank exports, ERP extracts):

- **Inspect source format before parsing.** Column names, date formats, sign conventions, and delimiter quirks vary across providers and change without notice. Common issues: trailing delimiters creating phantom columns, inconsistent date formats, amounts with currency symbols or parentheses.
- **Preserve raw data or normalize through a documented process.** Either keep the original import untouched on a staging sheet and transform via formulas or Power Query into a clean working sheet, or normalize at import with documented rules. The transformation from source to working format must be reproducible and traceable, not ad hoc manual editing.
- **Preserve source identification.** Include an Account or Source column so every row traces back to its origin — essential for reconciliation.
- **Document column mappings.** Each source has its own column layout; the Instructions sheet should map source columns to workbook columns per provider.
- **Auto-categorize, then let the user override.** Apply keyword- or rule-based categorization during import, but always provide an override column, and document the rules so the user can adjust them.

## Programmatic workbook generation caveats

When building workbooks with Python (openpyxl, xlsxwriter) or other programmatic tools, compatibility issues arise that don't exist when building by hand.

### Known failure modes

- **Structured table references in data validation.** `=TableName[ColumnName]` in a DataValidation formula produces invalid XML in openpyxl; Excel strips the validation on open (sometimes silently, sometimes with a repair dialog). **Use Named Ranges instead** — same cells, universally compatible.
- **Sheet-level autoFilter + Table autoFilter conflict.** An Excel Table owns its own autoFilter. If the code also sets `ws.auto_filter.ref`, Excel sees two conflicting filters on the same range and may destroy the Table definition. **Let the Table handle filtering; don't set sheet-level autoFilter.**
- **Formula-like text.** Any cell value starting with `=` is interpreted as a formula. If descriptive text happens to start with `=` (e.g. documenting a formula pattern in an audit log), prefix it with an apostrophe (`'`) to force text treatment.
- **Full-column references in SUMPRODUCT.** `SUMPRODUCT(Sheet!A:A*Sheet!B:B)` causes #VALUE! when columns contain mixed types or empties beyond the data range. Use bounded ranges.
- **Unicode special characters.** Subscript/superscript Unicode (₀₁₂, ⁰¹²) render as black boxes in some PDF libraries (ReportLab). Use markup tags instead.

### Testing protocol

Always test programmatically generated workbooks in actual Excel (not just in Python). Check for: a repair dialog on open (invalid XML); data validation dropdowns functioning; Tables intact with correct ranges; formulas calculating (not showing as text); conditional formatting applied as expected.

## Building a new workbook — workflow

1. **Clarify purpose and scope.** What questions should this answer? What data sources feed it? What's the update cadence? Who else uses it?
2. **Surface business logic decisions.** Category structure, sign convention, reporting periods, aggregation rules, variance definitions, any allocation or proration logic. Propose defaults but get confirmation.
3. **Design the sheet architecture.** Map which sheets you need and their roles (raw data, assumptions, calculations, checks, outputs, audit log). Name them clearly.
4. **Build the source-of-truth layer first.** Master lists, mappings, assumptions — before any formulas reference them.
5. **Build data sheets with structure.** Excel Tables for growing data, formula-driven derived columns, data validation on dimension columns.
6. **Build calculations with name-based lookups.** Every cross-sheet reference matches on a name or key, not a row position.
7. **Build the Checks sheet.** Orphan detection, duplicate flags, formula health, reconciliation tie-outs.
8. **Build outputs.** Dashboard, variance report, summary — all formula-driven from the layers below.
9. **Write Instructions.** Routine workflow, column mappings, sign convention, how to add dimensions, troubleshooting.
10. **Write the Audit Log and Agent sheet.** Audit Log: Workbook Snapshot + first task block documenting the build. Agent sheet: standing operating conventions, gotchas, design decisions, and known risks.
11. **Verify.** Recalculate all formulas, scan for errors, spot-check key totals, test in Excel if generated programmatically.

## Opening an existing workbook — workflow

When working with a workbook for the first time (whether the user or a previous AI session built it):

1. **Read the Audit Log first** (if one exists). Understand design intent, known risks, and prior history before touching anything.
2. **Run the intake checklist** ("Intake before intervention" above). Understand sheet roles, data flow, formula patterns, manual inputs, and existing checks.
3. **Identify structural risks** — positional cross-sheet references, duplicated lists, hardcoded assumptions in formulas, missing validation, no checks or reconciliation, undocumented range ceilings.
4. **Report findings.** Tell the user what affects reliability; propose improvements ranked by materiality.
5. **Get confirmation before changing structure.** Small fixes (a formula error, a typo) can proceed; structural changes (refactoring architecture, adding sheets, changing data flow) need the user's go-ahead.
6. **Update or create the Audit Log** after any work.

## Formatting conventions

Use consistent visual conventions so the user can distinguish inputs from calculations at a glance:

- **Blue text** — hardcoded inputs and assumptions the user may change
- **Black text** — formulas and calculations (never edit these)
- **Yellow background** — key assumptions or cells requiring periodic update
- **Green conditional formatting** — passing checks, favorable variances
- **Red conditional formatting** — failing checks, unfavorable variances
- **Headers** — consistent style across all sheets (dark fill, white bold text)
- **Number formats** — currency with parentheses for negatives (`$#,##0;($#,##0);"-"`), percentages to one decimal (`0.0%`), dates consistent throughout

## Checklist: is this workbook resilient?

A quick structural review of any finance workbook:

- [ ] Every dimension list (categories, accounts, etc.) has a single source of truth
- [ ] Cross-sheet lookups use name-based matching, not positional row references
- [ ] Growing data is in Excel Tables or has bounded ranges with documented ceilings
- [ ] Derived values are formulas, not manual entries
- [ ] User-editable dimension columns have data validation; imported dimensions are validated by checks
- [ ] Sign convention is documented and enforced at import
- [ ] Recurring/shared workbooks have a Checks sheet with orphan detection, duplicate flags, and reconciliation; one-offs verify key totals against source data
- [ ] An Instructions sheet documents the routine workflow and data source mappings
- [ ] An Audit Log exists with design decisions and known risks
- [ ] All formulas evaluate without errors (#REF!, #VALUE!, #DIV/0!, #NAME?, #N/A)
- [ ] The workbook has been tested in Excel (not just in the tool that generated it)
- [ ] Manual inputs are visually distinguished from formulas
- [ ] Assumptions and hardcoded values are in dedicated cells, not embedded in formulas
- [ ] Key totals tie out to source-system control numbers where applicable
- [ ] Forecast assumptions are visible and auditable, not buried in formulas
