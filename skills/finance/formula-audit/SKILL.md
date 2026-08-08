---
name: formula-audit
description: A read-only mechanical QA scan of a workbook's formulas — error values, buried hardcodes, broken cross-sheet links, off-by-one ranges, pattern breaks, unit/scale mismatches, stale live-data formulas — returned as a severity-ranked findings table. Changes nothing unless explicitly asked. The mechanical sibling to `/logic-audit`; run it first when formulas may be broken, since broken formulas make logic findings noise.
disable-model-invocation: true
---

# /formula-audit

A fast, read-only pass that answers one question: **is this workbook mechanically correct?** It finds broken formulas, errors, hardcodes, and reference faults, then reports them in a severity-ranked table. It does not decode business logic, check filter coverage, or hunt for double-counts — that is `/logic-audit`'s job.

A user-invoked escalation target, not a loop phase: reach for it when you suspect mechanical faults, or when `/workbook-explore`'s Full-orientation mode names it after spotting formula-health concerns.

## When to use

Use when:
- You need a quick formula-health check before sending a workbook to a coworker, auditor, or boss.
- A model "won't balance" or "something's off" and you need to find mechanical faults first.
- You inherited a workbook and want to know what's broken before trusting it.
- `/workbook-explore`'s Full-orientation mode flagged formula-health concerns and named this skill.

Use `/logic-audit` instead when the question is about *meaning* — whether filters overlap, whether coverage has gaps, whether every dollar flows to exactly one line. Mental model: `/formula-audit` = "are the formulas right?" `/logic-audit` = "is the logic right?" They pair; running both before a major handoff is reasonable, formula-audit first.

## The core discipline

**Read-only. Report first, fix only on explicit request, and show each fix before applying it.** This skill diagnoses; it never edits until the user asks after seeing the findings. The deliverable is a findings table in chat — not edits to the workbook, not a written audit sheet (that's `/logic-audit`'s durable artifact; this is the fast pass). Don't "while I'm here" anything, and don't re-derive prior findings already settled in the Audit Log.

## Step 1: Determine scope

If the user gave a scope, use it. Otherwise ask which of three:

- **selection** — the currently selected range only
- **sheet** — the active sheet only
- **workbook** — every sheet

Default to **sheet** if the user is vague and there's an obvious active sheet. Reserve **workbook** for pre-send QA passes and inherited files.

Done when: scope is fixed and you know which cells you're reading.

## Step 2: Run the mechanical checks

Read formula cells across the scope (`get_cell_ranges` or `code_execution` with openpyxl on a standalone `.xlsx`). Check for:

| Check | What to look for |
|---|---|
| Error values | `#REF!`, `#VALUE!`, `#N/A`, `#DIV/0!`, `#NAME?`, `#NULL!`, `#NUM!` |
| Buried hardcodes | A literal inside a formula that should be a cell reference (`=B5*1.05` where `1.05` belongs in an assumption cell) |
| Pattern breaks | A formula that deviates from its neighbors across a row or column without reason — the single SUM in a row of SUMIFS, the one cell pasted as a value |
| Off-by-one ranges | `SUM`/`AVERAGE`/`SUMIFS` that misses the first or last row, or over-reaches into a total row |
| Pasted-over formulas | A cell that should hold a formula (matches its row/column pattern) but is a static value |
| Broken cross-sheet links | References to sheets/cells that were moved, renamed, or deleted |
| Unit / scale mismatches | Thousands mixed with millions, percentages stored as whole numbers (5 vs 0.05), a hardcode in a different unit than its column |
| Circular references | Note whether intentional (and whether the iterative-calc toggle is on) or accidental |
| Hidden rows / sheets | Could conceal overrides or stale calculations driving visible totals — note their existence, don't assume intent |
| Volatile / fragile patterns | Whole-column references that will silently absorb new rows, `OFFSET`/`INDIRECT` chains that break on insert |

Note whether any logic is locked in VBA — flag that macros exist and that formula-only auditing can't see inside them.

Done when: every formula in scope has been read and each finding is recorded with its exact cell address.

## Step 3: Live-data formula checks (if present)

If the workbook uses a data plugin (Velixo, Bloomberg, FactSet, Power Query), the most common silent fault is a formula that *looks* fine but returns stale or wrong data. Check for:

**Velixo (Acumatica) — the common case here:**
- Stale values: display values that won't match source because the workbook wasn't refreshed. **F9 does NOT refresh Velixo** — a refresh needs desktop Excel (ribbon or Velixo's VBA API). Flag any sign the last refresh predates the latest data change.
- Ledger-name casing: names are case-sensitive — match the ledger's exact casing. `"ACTUAL"` works; a wrong-case variant like `"Actual"` returns `#N/A`. A frequent silent break.
- Period format must be `"MM-YYYY"` (e.g. `"04-2026"`); other formats fail quietly.
- Parameter-order faults in `ACCOUNTTURNOVER` (Connection, Ledger, AccountClass, Account, Subaccount, Branch, FromPeriod, ToPeriod, IncludeUnposted).

**Power Query:** note whether queries have refreshed; flag connections that error or point at a moved source.

**Other plugins:** flag parameter-order, case-sensitivity, and refresh-state faults the same way.

Done when: every live-data formula's freshness and syntax has been checked, or this step is skipped because no plugins are present.

## Step 4: Report

Output a findings table in chat. Lead with a one-line verdict, then the table:

> **[scope] scan — [Clean / Minor issues / Major issues] — N critical, N warnings, N info**

| # | Sheet | Cell/Range | Severity | Category | Issue | Suggested fix |
|---|---|---|---|---|---|---|

Severity:
- **Critical** — produces a wrong output now: error value feeding a total, broken link, pasted-over formula in a live calc, stale Velixo behind a reported number
- **Warning** — risky but not currently wrong: buried hardcode, pattern break, off-by-one that happens to land right, volatile reference
- **Info** — style/robustness: whole-column refs, hidden rows worth noting, unit conventions

Order the table critical-first. If a load-bearing reconciliation or balancing total is itself broken, say so up front — everything downstream of it is suspect until it's fixed, and the rest of the findings may be noise from that one break.

**Do not change anything.** End by offering to fix specific findings if the user wants — show each fix before applying it. This skill only diagnoses; it does not rebuild, clean, or restructure.

## Quality checklist

- [ ] Scope confirmed before reading (selection / sheet / workbook)
- [ ] All error-value types checked, not just `#REF!`
- [ ] Buried hardcodes and pasted-over formulas actively hunted (the top sources of silent bugs)
- [ ] Pattern breaks checked against row/column neighbors
- [ ] Live-data formulas checked for staleness and syntax (Velixo refresh, ledger casing, period format) if plugins present
- [ ] Macros flagged as un-auditable if VBA is present
- [ ] Findings table is severity-ranked, critical-first, with exact cell addresses (not "a cell on Dashboard")
- [ ] A broken load-bearing total is called out up front
- [ ] Nothing was changed without explicit request
- [ ] No business-logic analysis performed — overlaps, gaps, and coverage are a separate `/logic-audit` invocation
