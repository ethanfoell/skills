---
name: velixo-formulas
description: Reference for Velixo Reports Excel functions that pull live data from Acumatica ERP — the ~80 VLX/ACU worksheet functions and the performance patterns that decide whether a workbook refreshes in seconds or minutes. Use when the user mentions Velixo or Acumatica, references functions like ACCOUNTTURNOVER, ACCOUNTSANDSUBACCOUNTSWITHHISTORY, or GI/Generic Inquiries, or works on any actuals export, budget reconciliation, or ERP-to-Excel reporting pipeline.
---

# Velixo Formulas Reference

Velixo Reports is a commercial Excel add-in (https://velixo.com) that connects Excel to Acumatica ERP via worksheet functions. Each function call goes over the wire to Acumatica, evaluates server-side, and returns a value or array. Performance is dominated by **how many round-trips** the workbook makes per refresh — not by formula complexity. That principle drives almost every design choice below.

Formulas reference a named connection configured in the add-in session; credentials and tenant details are managed outside the workbook.

## Function tiers

There are ~80 Velixo functions across Financial / Project / Query / System / Writeback. Most finance and budget work touches a small subset heavily; the rest are "know it exists, look up syntax when you need it."

### Tier 1 — Workhorses (use these constantly)

These cover ~90% of finance/budget/actuals work. Memorize the syntax.

#### `ACCOUNTTURNOVER` — period activity (the most-used function)

Returns net activity (debits − credits, signed by account type) for a GL/Sub combo over a period range.

```
=ACCOUNTTURNOVER(Connection, Ledger, AccountClass, Account, Subaccount, Branch, FromPeriod, ToPeriod, IncludeUnposted)
```

- `Connection` — connection name (string), usually a named cell like `cfg_Connection`
- `Ledger` — typically `"ACTUAL"` for posted actuals, or a budget ledger name
- `AccountClass` — usually blank; filter by class only when needed
- `Account` — GL account, text. A single value, a range like `"500000-599999"`, or an array reference
- `Subaccount` — sub, text. Same flexibility as Account
- `Branch` — blank for all branches, or a specific branch
- `FromPeriod` / `ToPeriod` — period in `"MM-YYYY"` format (e.g. `"01-2025"`). Some Velixo builds also accept raw dates here
- `IncludeUnposted` — `TRUE`/`FALSE`. `FALSE` for closed/audited periods, `TRUE` if you want WIP

Single-month actual for one GL/Sub:
```
=ACCOUNTTURNOVER(cfg_Connection, "ACTUAL", , "601200", "910", , "03-2025", "03-2025", FALSE)
```

TTM (rolling 12 months) using period offsets:
```
=ACCOUNTTURNOVER(cfg_Connection, "ACTUAL", , $A6, $B6, , cfg_TTM_Start, cfg_TTM_End, FALSE)
```

#### `ACCOUNTSANDSUBACCOUNTSWITHHISTORY` — dynamic GL/Sub enumeration

Spills a 2-column array of every (GL, Sub) combo with non-zero posted activity in a period window — purpose-built for "give me everything that moved" rather than hand-maintaining a list.

```
=ACCOUNTSANDSUBACCOUNTSWITHHISTORY(Connection, Ledger, Branch, Account, Subaccount, FromPeriod, ToPeriod, IncludeInactive, IncludeUnposted, IncludeBranches, UseMasterFinancialCalendar)
```

Critical for actuals exports: prior-year spend may have hit GL/Sub combos that have no current-year budget entry, so a hand-curated list will miss them. The result spills as a dynamic array — reference downstream with `A6#` (spill ref) so other formulas size automatically.

```
=ACCOUNTSANDSUBACCOUNTSWITHHISTORY(cfg_Connection, cfg_Ledger, cfg_Branch, , , cfg_FY_Start, cfg_Enum_End, FALSE, FALSE)
```

#### `ACCOUNTNAME` and `SUBACCOUNTNAME` — name lookups (array-aware)

Both are **array-aware**: pass a spill reference and one call returns names for the whole list. This is the canonical pattern — do not loop with MAP/LAMBDA.

```
=ACCOUNTNAME(Connection, Account)        → text or text array
=SUBACCOUNTNAME(Connection, Subaccount)
```

Paired with the enumeration above, one call each spills down the whole list:
```
C6: =ACCOUNTNAME(cfg_Connection, A6#)
D6: =SUBACCOUNTNAME(cfg_Connection, B6#)
```

#### `ACCOUNTENDINGBALANCE` — point-in-time balance

For balance-sheet positions or any "what's the balance at end of period" question. Use this — not `ACCOUNTTURNOVER` — when you need a balance, not a flow.

```
=ACCOUNTENDINGBALANCE(Connection, Ledger, AccountClass, Account, Subaccount, Branch, Period, IncludeUnposted)
```

#### `EXPANDACCOUNTRANGE` and `EXPANDSUBACCOUNTRANGE` — range expansion

Convert a range expression like `"600000-699999"` into a spilled list of actual account values that exist — useful for building dynamic GL universes by class without hand-listing, or expanding a sub range to map to a summary grouping.

```
=EXPANDACCOUNTRANGE(Connection, RangeExpression)
=EXPANDSUBACCOUNTRANGE(Connection, RangeExpression)
```

#### `FINANCIALPERIODBYDATE` and `FINANCIALPERIODOFFSET` — period math

```
=FINANCIALPERIODBYDATE(Connection, Date)                  → period code like "04-2026"
=FINANCIALPERIODOFFSET(Connection, Period, OffsetMonths)  → e.g. -11 for TTM start
```

These build TTM windows that cross fiscal-year boundaries cleanly. Prefer period codes (consistent with Velixo's other period args) over raw dates when chaining.

### Tier 2 — Use when relevant

#### `ACU.QUERY` — query Acumatica objects directly

Run a query against any Acumatica object (Bill, Journal Transaction, Invoice, etc.) and get rows back as a spill — faster than exporting from the Acumatica UI for ad-hoc analysis.

```
=ACU.QUERY(Connection, ObjectName, Fields, Filter, ...)
```

Pair with `ACU.QUERYFILTER` to build the filter expression; use `ACU.OBJECTDEFINITION` first to discover the field names available on an object.

#### `GI` and `GIFILTER` — Generic Inquiry execution

If a Generic Inquiry already exists in Acumatica that returns the data you need, `GI` is the fastest path — one call, returns the same rows the GI shows in the Acumatica UI. Use these for transaction-level investigations ("what's actually flowing through a specific GL/Sub?") without leaving Excel.

```
=GI(Connection, GIName, Filter, ...)
=GIFILTER(FieldName, Operator, Value, ...)
```

#### `GILOOKUP` / `GILOOKUPF` — single-value GI lookup

For pulling one field from one row of a GI (vs `GI`, which returns many rows). Less common.

#### `WRITEBACKBUDGET` — push budget values back into Acumatica

Don't use lightly — this **writes to the ERP**.

```
=WRITEBACKBUDGET(Connection, Ledger, Account, Subaccount, Branch, Period, Amount, ...)
```

Other writeback functions exist but are less common in budget reconciliation; see Tier 3.

### Tier 3 — Niche (look up at help.velixo.com when needed)

These exist; recognize the families, web-fetch the syntax when a specific one comes up.

- **Other financial:** `ACCOUNTBEGINNINGBALANCE`, `ACCOUNTTYPE`, `ACCOUNTSWITHHISTORY` (account-only enumeration, no sub), `BRANCHLIST`, `FINANCIALPERIODLIST`, and ~25 more — plus the `EXPAND*RANGE` variants for class / group / branch / company / cost-code / project / segment.
- **Query:** the `ACU.EXPAND*RANGE` family (ledger, object, project-task).
- **System:** `TODAYNV` (non-volatile TODAY — see gotchas), `LASTREFRESHDATE` / `WORKBOOKLASTREFRESHDATE`, `TOTABLE`, `UNIQUEBYPATTERN`, and version/refresh helpers like `VELIXOVERSION`.
- **Writeback:** `WRITEBACK`, `WRITEBACKJOURNAL`, `WRITEBACKCOMMIT`, project writebacks, … — all **write to the ERP; use carefully**.
- **Project (~30 functions):** `PROJECTBUDGET`, `PROJECTACTUALAMOUNT`, `PROJECTCOMMITTEDAMOUNT`, `PROJECTFORECAST`, plus cost-code / change-order / cost-to-complete lookups. Relevant for **project-cost-controls and job-costing** (construction, professional services, capital projects). If your work is GL/account-centric rather than project-centric, you won't need these.

## Performance — read this before writing any Velixo formula

This section is the difference between a workbook that refreshes in 10 seconds and one that takes 10 minutes.

### The MAP + LAMBDA anti-pattern

**Do not do this:**
```
=MAP(A6:A200, LAMBDA(acct, ACCOUNTTURNOVER(cfg_Connection, "ACTUAL", , acct, ...)))
```

Each `LAMBDA` iteration fires a separate Velixo API call with full overhead. With ~190 GL/Sub combos × 13 period columns, that's ~2,470 sequential round-trips. Velixo's own performance docs call this out — wrapping Velixo functions in `MAP`/`BYROW`/`REDUCE` defeats the add-in's batching.

### What to use instead

**Pattern A — Native array-aware function (preferred):** pass a spill reference directly to functions that accept arrays.
```
=ACCOUNTNAME(cfg_Connection, A6#)   ← one call, spills the full list
```
`ACCOUNTNAME` and `SUBACCOUNTNAME` are confirmed array-aware; some others are too — when in doubt, pass `A6#` and see if it spills.

**Pattern B — By-row formulas with IF guards (for non-array-aware functions):** pre-fill a safe range (e.g. 500 rows), wrapping each in `IF($A6="","", ...)` so empty rows don't fire calls. Velixo batches by-row formulas internally during refresh — this is the intended pattern, and what to do for `ACCOUNTTURNOVER` since it takes two parallel arrays (Account + Sub) the array-aware path doesn't cleanly handle.
```
E6: =IF($A6="", "", ACCOUNTTURNOVER(cfg_Connection, "ACTUAL", , $A6, $B6, , cfg_FY_Start, cfg_FY_End, FALSE))
```

### Refresh control

Velixo refreshes on its own cycle, not Excel's calc engine. `F9` does **not** refresh Velixo. A refresh requires **desktop Excel with Velixo loaded**, triggered from the ribbon's Refresh button or from Velixo's VBA API (`Velixo.Reports.Vba` — `Refresh`/`RefreshFull`, sync and async; VBA is desktop-only). **Neither trigger is reachable from a Claude surface** — the Excel add-in can't run VBA or macros, and a closed `.xlsx` on disk executes no formulas at all — so a plan written from an agent surface names the refresh as a **handback step** for the user, and the VBA API is the seam for automating refreshes outside Claude (verified 2026-07-07). Confirm a refresh ran with `WORKBOOKLASTREFRESHDATE` / `LASTREFRESHDATE`. For "snapshot" workbooks, paste-values immediately after refresh to lock the numbers.

## Conventions and gotchas

- **Period format is `"MM-YYYY"`** with a dash — `"01-2025"`, not `"2025-01"` or `"Jan 2025"`. Some functions accept dates in period args, but periods are safer for consistency. Build a 12-cell month row at the top of the workbook for the periods you reference repeatedly.
- **Account/Sub args are text**, not numbers. Use `TEXT(601200, "0")` or store as text in the source range. Mixing number/text causes **silent zero returns** when Velixo can't match `601200` (number) against an Acumatica account stored as `"601200"` (text).
- **Defined names use underscores, not dots.** `cfg_Connection` works reliably; `cfg.Connection` is legal Excel but occasionally trips Velixo's parser.
- **openpyxl spill caveat** (only when generating workbooks programmatically): openpyxl writes formulas with plain `<f>` tags, not the dynamic-array-marked variant Excel uses for native spill. On first open, array-returning formulas referencing `A6#` may need a one-time `F2` + `Enter` (click into the master enumeration cell once after first open).
- **`TODAYNV` vs `TODAY`:** `TODAY()` is volatile and recalcs on every change — it can trigger Velixo refreshes you didn't want. `TODAYNV()` is non-volatile and only updates on explicit refresh. Prefer it (or a manually-controlled date cell) for dashboard/snapshot workbooks.
- **Parameterize Connection / Ledger / Branch as named cells.** Even on a one-off, a named-range "Config" sheet means you can re-point to a different tenant/ledger in one place and re-refresh.

## Common patterns

### Pattern 1 — Snapshot actuals export (paste-values workflow)

Three sheets: `Config` (named cells for connection, ledger, branch, periods), `Pull` (Velixo formulas spilling from one master enumeration), `Output` (clean rectangle for paste-values into a downstream file). Key moves:
- `ACCOUNTSANDSUBACCOUNTSWITHHISTORY` in a top cell to spill the GL/Sub universe across the period window (catches combos with no current-year budget entry).
- `ACCOUNTNAME(conn, A6#)` and `SUBACCOUNTNAME(conn, B6#)` for the name columns.
- Pre-filled by-row `ACCOUNTTURNOVER` for monthly columns + TTM, each guarded by `IF($A6="","", ...)`.
- `Output` uses `LET` + `INDEX` to pull exactly the populated block, sized off the enumeration spill.

### Pattern 2 — Live balance check for a clearing/balance-sheet account

```
=ACCOUNTENDINGBALANCE(cfg_Connection, "ACTUAL", , "119900", "965", , cfg_AsOf_Period, FALSE)
```
Combine with a `GI` call against a transaction-detail Generic Inquiry to see what's flowing through.

### Pattern 3 — Transaction-level investigation via GI

When budget variance signals a coding issue and you need the actual line items:
```
=GI(cfg_Connection, "GL-Transactions-by-Account", GIFILTER("Account", "=", "701400"), GIFILTER("Subaccount", "=", "931"))
```
Confirm the GI name with `ACU.OBJECTDEFINITION` or the Acumatica GI screen.

### Pattern 4 — Hand-pasted list vs dynamic enumeration

- **Dynamic (`ACCOUNTSANDSUBACCOUNTSWITHHISTORY`)** wins when completeness matters (every active combo, including unbudgeted ones) or the GL/Sub universe shifts year-to-year. In reconciliation work this is usually preferable — miscoded spend hitting an un-budgeted combo is a finding, not noise to suppress.
- **Hand-pasted list** wins when the budget structure is locked and you report only on those budgeted combos (filter signal vs total spend) — e.g. variance reporting against a fixed budget.

## Authoritative reference

Velixo function docs: https://help.velixo.com/doc/main/acumatica/functions

When syntax here conflicts with the live docs, the live docs win — Velixo updates their function set across releases. If a function isn't behaving as documented, web-fetch the relevant docs page before debugging blindly.
