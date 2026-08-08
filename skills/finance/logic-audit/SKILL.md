---
name: logic-audit
description: Decode and audit the business logic in a spreadsheet — the classification scheme that sorts source records (GL transactions, detail rows) into reporting buckets (P&L lines, KPIs) via filters and rules. Verifies the scheme is complete (no gaps), non-overlapping (no double-counts), correctly classified, consistent across sheets and periods, and reconciled to a control total. Runs as a lightweight Scan (findings in chat) or a full Decode (writes a reference sheet). The business-logic sibling of `/formula-audit`; run `/formula-audit` first if formulas may be broken.
disable-model-invocation: true
---

# /logic-audit

`/formula-audit` answers *"are the formulas mechanically correct?"* This skill answers a different question: *"is the logic right?"* — does the workbook classify and aggregate data the way it's supposed to, with nothing missed, nothing double-counted, and everything in the right place?

## How this fits

The two audits pair. `/formula-audit` is the **mechanical** sibling — error values, broken links, off-by-one ranges, buried hardcodes. `/logic-audit` is the **business-logic** one — what the formulas *mean*, decoded and checked. If a workbook might have broken formulas, run `/formula-audit` first; decode the logic once the formulas are known to be sound. Both are user-invoked escalation targets — `/workbook-explore`'s Full-orientation mode present-and-names them when its scan warrants a deeper look.

## The core discipline

**Scan-only. Report first; fix only on explicit request, and show the fix before applying it.** This skill decodes and audits — it never edits live logic. In Decode mode it writes a *reference* sheet, not changes to the formulas it documents. This rule governs every step below.

## When to use

Use when business logic hides in formulas the row labels don't reveal — SUMIFS/SUMPRODUCT filters, wildcard account ranges, mapping tables, aggregation hierarchies — or when someone wants the scheme decoded, overlaps and gaps found, or a tie-out checked.

## The core idea: logic is a classification scheme

Almost all finance and reporting logic is a **classification scheme**. It takes a universe of *source records* — GL transactions, detail rows, line items — and sorts them into *reporting buckets* — P&L lines, categories, KPIs, rollups — using filters and rules (SUMIFS criteria, wildcard account ranges, mapping tables, Power Query steps, Velixo filter strings).

Seen this way, "auditing the logic" stops being a grab-bag of checks and becomes a small set of properties the classification either has or doesn't: **decode the scheme, then verify five invariants.**

## What a logic audit checks: the five invariants

A sound classification scheme is **MECE, correct, consistent, and reconciled.** Each invariant has a characteristic way it gets violated in real finance workbooks — the failure mode matters more than the name, so lead with it.

**1. Exhaustive — no gaps.** Every source record lands in *at least one* bucket. Nothing falls through all the filters.
- *How it breaks:* The dangerous version isn't a gap that exists today — it's a gap that *opens later*. These workbooks get refreshed every period, and the dominant failure is "someone adds GL 615999 next month and it silently drops out of every bucket." So check current coverage **and** future robustness: is there a residual / catch-all bucket, or a standing reconciliation that would *catch* a new code rather than let it vanish? A scheme that's MECE today but has no catch-all is a latent gap.

**2. Exclusive — no double-counts.** No source record lands in *more than one* bucket.
- *How it breaks:* The obvious version is two filter sets that intersect (row A captures account 6015, row B captures 60??, both grab 6015). The sneakier and more common version is **hierarchy double-counting** — a subtotal or total row getting swept into a sum alongside its own components. When you check for overlaps, check for level mix-ups too, not just filter-set intersections.

**3. Correct — the right bucket, not just *a* bucket.** Each record lands where it actually belongs.
- *How it breaks:* You can be perfectly exhaustive and exclusive and still have everything misfiled. This is the least mechanical invariant and the one where judgment earns its keep, because it requires knowing what a code *means*, not just where it's pointed. Watch especially for **sign / direction** errors — contra accounts, credits, account-type sign conventions — where a bucket is right in *what* it selects but wrong in *direction* (negative when it should be positive). A misclassification is invisible to a tie-out if two errors offset.

**4. Consistent — the same data classified the same way everywhere.** A given record is treated identically across sheets, across periods, and across a companion workbook.
- *How it breaks:* Account 6015 is "Meals" on the summary sheet but rolled into "Travel" on the detail sheet; this month's scheme silently differs from last month's; the budget workbook uses a different taxonomy than actuals. The *test* is different from the others — you're diffing two surfaces against each other, not checking one against reality — which is why it's its own invariant.

**5. Reconciled — it ties to a control total.** The buckets sum to an independent number: GL total, trial balance, an unfiltered pull.
- *How it breaks:* Exhaustive and Exclusive are *structural* claims about the filters; reconciliation is the *empirical proof* in dollars. If the sum of the parts doesn't equal the control total, you have a gap, an overlap, or a sign error — the variance tells you how much, and which invariant to go hunting in. No control total means none of the other four can be proven, only argued.

Decoding the scheme is the prerequisite that makes all five checkable — you can't judge coverage or correctness until you know what each filter actually selects.

## Two modes

This skill runs at two depths. Pick based on how it was invoked; if it's ambiguous, ask which the user wants.

**Scan mode** — lightweight, reports findings in chat, creates no artifacts. This is what `/workbook-explore`'s Full-orientation mode calls for ("a targeted scan of the highest-risk areas") and the right default for a pre-trust check. Decode the high-risk filters, run the invariant checks against them, report a findings table, stop. Don't build decoder sheets.

**Decode mode** — the full treatment. Decode the *entire* scheme, document it in a reference sheet (decoder tables + line-by-line map + a findings section), and optionally produce a Blueprint for reproducing the logic elsewhere. Use when the goal is to make tribal knowledge explicit and durable ("the CFO built this and only they understand it"), or to reproduce the structure in another workbook or system.

Both modes sit on the same spine: decode, then check the five invariants. Scan reports; Decode documents.

## Step 1: Decode the scheme

Find where the logic lives and make it explicit.

| Where logic hides | What to look for |
|---|---|
| Filter-based formulas | SUMIFS, SUMPRODUCT, Velixo `ACCOUNTTURNOVER`, Power Query filters — anything selecting data by criteria |
| Classification columns | Codes/categories that drive formulas (GL accounts, subaccounts, department or channel codes) |
| Mapping tables | Reference sheets translating source codes into reporting categories |
| Aggregation hierarchies | How detail rolls up into subtotals, sections, grand totals |
| Config-driven formulas | Behavior that changes with input cells (period selectors, company codes, toggles) |

For each filter dimension, build a **decoder** that maps codes to business meaning. The skill is the *method of inference*, not a lookup table: read the row labels, section headers, and formula placement around each code — those tell you what it represents. Note the filter syntax as you go (wildcards, ranges, OR-lists, negation).

A decoder entry looks like this (the codes below are illustrative placeholders — yours come from the workbook in front of you):

| Code | Meaning | Type | Notes |
|---|---|---|---|
| `1??` | *(example)* a channel group | Channel | Wildcard expands to 100–199 |
| `920` | *(example)* a department | Department | Exact match |

Group by type (channels vs departments vs brands vs special codes). In Scan mode this lives in chat; in Decode mode it becomes a decoder table on the reference sheet.

## Step 2: Check the invariants

Work through the five. The two that benefit most from code are Exclusive (overlaps) and Exhaustive (gaps), because enumerating filter coverage by hand is error-prone. The utility below is a **starting point you adapt to the workbook's code system** — it is not specific to any one workbook.

The key design choice is how to expand a filter string into the set of values it captures. Two common cases:
- **Numeric codes** (Acumatica/Velixo and similar): wildcards are digit positions (`1??` → 100–199), `:` is a range, `;` is OR. Enumerate directly.
- **Alphanumeric / mixed codes** (`AMZ?`, `US-W`, `EU-FR`): convert wildcards to regex and match against the *universe of codes actually present in the data*, rather than trying to enumerate.

```python
from collections import defaultdict
import re

def expand_numeric(filter_str):
    """(exact_values, has_all) for numeric-code systems (Velixo/Acumatica).
       '' -> matches everything; '920;925' -> OR; '900:905' -> range; '1??' -> 100-199."""
    if not filter_str or not filter_str.strip():
        return set(), True
    out = set()
    for part in (p.strip() for p in filter_str.split(';')):
        if not part:
            continue
        if ':' in part:
            lo, hi = (int(x) for x in part.split(':'))
            out.update(str(i) for i in range(lo, hi + 1))
        elif '?' in part:
            prefix, n = part.replace('?', ''), part.count('?')
            start = int(prefix) * (10 ** n)
            out.update(str(i) for i in range(start, start + 10 ** n))
        else:
            out.add(part)
    return out, False

def expand_regex(filter_str):
    """(compiled_regex, has_all) for alphanumeric/mixed codes. '?' -> any char, '*' -> any run.
       Match the regex against the codes actually present in the data; don't enumerate."""
    if not filter_str or not filter_str.strip():
        return None, True
    parts = [re.escape(p.strip()).replace(r'\?', '.').replace(r'\*', '.*')
             for p in filter_str.split(';') if p.strip()]
    return re.compile('^(?:' + '|'.join(parts) + ')$'), False

# Overlap (Exclusive) — numeric example. mapping = [(row, label, primary, secondary), ...]
groups = defaultdict(list)
for row, label, primary, secondary in mapping:
    vals, has_all = expand_numeric(secondary)
    groups[primary].append({'row': row, 'label': label, 'vals': vals, 'all': has_all})

for primary, rows in groups.items():
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            if a['all'] or b['all']:
                print(f"OVERLAP {primary}: a no-filter row captures everything")
            elif a['vals'] & b['vals']:
                print(f"OVERLAP {primary}: rows {a['row']}/{b['row']} share {a['vals'] & b['vals']}")
```

For **Gaps (Exhaustive)**, build the universe of values that exist in the source for each dimension, then subtract everything the filters cover; what's left is the gap. Apply materiality — the raw gap list is long and most of it is cross-type noise (channel codes will never appear in a department-only account). Focus on same-type gaps and anything with real activity. The cleanest gap proof is the reconciliation in Step 3.

For **Correct** and **Consistent**, there's less to automate — these are read-and-judge. For Correct, spot-check that each filter's decoded meaning matches the label and section it sits under, with extra attention to sign. For Consistent, diff the scheme across the surfaces where the same data appears (other sheets, prior period, companion workbook) and document where they diverge.

## Step 3: Reconcile

If any control total exists — an unfiltered Velixo pull, a GL trial-balance figure, a "total" that should equal the sum of the parts — compare it against the sum of all buckets. The variance is your gap/overlap in dollars and the single most convincing piece of evidence in the audit. Quantify it; don't just say "looks close."

## Step 4: Report or document

**Scan mode** → a findings table in chat, severity-ranked, critical first:

> **[scope] logic scan — [Clean / Minor / Major] — N critical, N warnings**

| # | Invariant | Location | Severity | Finding | $ impact | Suggested fix |
|---|---|---|---|---|---|---|

**Decode mode** → write a reference sheet to the workbook with: the decoder tables (Step 1), a line-by-line map of every formula row (row #, label, filters, section, notes), and a findings section (confirmed overlaps, coverage gaps, anomalies, and the reconciliation summary). This writes a *reference* sheet, not edits to the live logic. For formatting, follow the workbook's established visual conventions — see `/excel-finance-workbooks` for the canonical style (section headers, status colors, monospace for codes); don't invent a new palette. Keep AI-specific language out of the sheet — it's a reference a human will read.

### Blueprint (Decode mode, optional)

If the goal is to reproduce this logic in another workbook or system, produce a self-contained Blueprint: the design philosophy, the decoder tables, the full line-by-line map, an implementation guide (formula templates, config cells, layout), and the known issues from the audit. Written so a reader can rebuild the structure without the original open. Export it as markdown or CSV if another session will consume it, and run `/formula-audit` on the finished rebuild.

## Live-data syntax notes (worked example: Velixo / Acumatica)

When a workbook pulls from a data plugin, document the syntax quirks that cause *silent* failures — the audit is worthless if it decodes a formula that's quietly returning the wrong data. Velixo is the common case in this environment; treat it as the worked example and apply the same discipline to any plugin (Power Query, Bloomberg, etc.).

- `ACCOUNTTURNOVER` parameter order: Connection, Ledger, AccountClass, Account, Subaccount, Branch, FromPeriod, ToPeriod, IncludeUnposted.
- Ledger names are **case-sensitive** — match the exact casing: `"ACTUAL"` works, a wrong-case variant like `"Actual"` returns `#N/A`.
- Filter syntax: `?` = single-char wildcard, `;` = OR, `:` = range.
- Period format is `"MM-YYYY"` (e.g. `"04-2026"`); other formats fail quietly.
- Velixo does **not** refresh on F9 — a refresh needs desktop Excel (ribbon or Velixo's VBA API). Stale values look fine but won't tie. (See `/velixo-formulas` for the full reference.)

## Adapting to different workbook types

The classification frame holds across domains — only the records and buckets change.

- **P&L / budget vs. actuals:** records are GL transactions; buckets are P&L lines via account × subaccount × department. The audit asks whether every dollar flows to exactly one line.
- **Reconciliation workbooks:** records are source items; buckets are match targets. Overlap = double-matching; gap = unmatched items.
- **ETL / transformation:** records are source rows; buckets are output columns. The invariants apply to mapping completeness.
- **Dashboards / reporting:** records are detail rows; buckets are KPI rollups. Check that every detail row is in exactly one rollup.

## What this does NOT do

- **Does not check mechanical correctness** — error values, broken links, off-by-one ranges, buried hardcodes → that's `/formula-audit`. Run it first if the formulas may be faulty.
- **Does not fix silently.** Report first. In Decode mode it writes a *reference* sheet, not edits to live logic; propose fixes, apply only on request, show before applying.
- **Does not rebuild or restructure** the workbook — it decodes and audits.
- **Cannot see inside VBA** — flag that macros exist and that formula-only auditing can't read their logic.

## Offer to log

At the end, offer to invoke `/workbook-log` (don't write automatically — wait for acceptance): what was analyzed, decoder tables created, overlaps and gaps found with severity and status, the reconciliation variance, and the Blueprint's location if one was made. This is what lets a future session pick up without re-deriving everything.

## Quality checklist

- [ ] The logic is framed as a classification scheme — records sorted into buckets — before any checking starts
- [ ] Every filter code in scope has a decoded business meaning
- [ ] Exhaustive: gaps checked, including future robustness (is there a catch-all for new codes?)
- [ ] Exclusive: overlaps checked, including hierarchy/subtotal double-counting
- [ ] Correct: classifications spot-checked against meaning, with attention to sign/direction
- [ ] Consistent: scheme diffed across sheets/periods/companion workbook where the same data appears
- [ ] Reconciled: variance vs. a control total quantified in dollars (if any control total exists)
- [ ] Mode matched the need — Scan reported in chat, Decode wrote a durable reference sheet
- [ ] Findings are severity-ranked with dollar impact and a suggested fix
- [ ] Formatting follows the workbook's existing conventions; no AI-specific language in output sheets
- [ ] Nothing changed unless asked — fixes proposed, shown before applying, applied only on request
- [ ] Offered `/workbook-log` (written only if accepted)
