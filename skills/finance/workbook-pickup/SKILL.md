---
name: workbook-pickup
description: Quick re-orientation for an already-onboarded workbook — read the Instructions sheet and latest Audit Log block, return a locked six-line summary, flag anything in-flight, then stop. The workbook loop's return-visit mode.
disable-model-invocation: true
---

# /workbook-pickup

Fast return-visit re-orientation for a workbook you've worked in before — the counterpart to `/workbook-onboarding`. Where onboarding lays down the Instructions sheet and Audit Log, this reads them back, gets you just-oriented-enough, then stops — the Quick Pickup mode `/workbook-explore` names.

## When to use

For quick context on an **already-onboarded** workbook — one with an Instructions sheet and Audit Log. Skip it when:
- It's a first encounter (no scaffolding) → `/workbook-onboarding`.
- You've already stated a task → just do it; don't re-read context.
- It's a folder or filing system → `/folder-pickup`.

## The core discipline: restraint

This skill exists to enforce **restraint**, not to analyze. The default failure on a fresh chat is to over-helpfully scan, recompute, and surface findings the user didn't ask for. The discipline: read two sheets, summarize in the locked template, optionally flag, then stop and wait.

- Don't read formulas, check totals, or re-audit logic.
- Don't validate, question, or re-derive the Audit Log's existing findings — those were settled in a prior session.
- Don't "while I'm here…" anything (no reorganizing, cleanup, or audits).
- Don't propose work the user hasn't asked for.

The user knows what's next and will say it. The job is to be oriented enough to help when they do.

## Step 1: Read the two source sheets

- **Instructions sheet** — Section A (Purpose & Overview) and Section B (Sheet Inventory) only. Skip data flow, reference points, routine workflow, known issues.
- **Audit Log** — the most recent task block only: Workbook Snapshot, the block's Done/Flagged content, any DO NOT EDIT note. Skip older blocks unless the most recent references them.

If either sheet is missing, stop and recommend `/workbook-onboarding`.

## Step 2: Return the locked summary

Exactly six lines, no prose, no extras:

```
Workbook: [name]
Purpose: [one line from Instructions A]
Status: [one line from latest Audit Log task block]
Open threads: [2–4 bullets, latest first; "none" if clean]
Edit restrictions: [DO NOT EDIT items, or "none"]
Last touched: [date and task title from latest Audit Log task block]
```

No introduction, no "let me know what you'd like to work on" closer, no emoji. The user's next prompt provides direction.

## Step 3: Surface flags (only if any exist)

Add a **Flags** section only if one of these is present in the Audit Log or Instructions:

- Unresolved overlaps with material dollar impact (from `/logic-audit` findings).
- An active **DO NOT EDIT** policy on any sheet.
- Stale-data warnings (display values not matching source).
- Flagged findings from the last session that weren't resolved.
- Plugin connection issues (Velixo refresh failure, wrong tenant, expired credentials).
- **In-flight state** — a sheet named exactly "Handoff" (an active paused task), or an in-progress task block in the Audit Log (a `/workbook-plan` stub never closed by `/workbook-log`). These matter most when pickup is invoked directly (no `/workbook-explore` first): they're work that must not be silently stepped on.

For in-flight state, surface a one-line flag pointing to `/workbook-explore` — do NOT read the Handoff sheet in full, resume, route, or reconcile. Pickup orients; it does not act. `/workbook-explore` owns resuming.

```
Flags:
- [type]: [one line — what it is, where it lives, why it matters]
- Active handoff: paused task on "Handoff" sheet — `/workbook-explore` to resume or close it
- In-progress task: unclosed stub in Audit Log from [date] — `/workbook-explore` to resume, cancel, or ignore
```

If no flags, omit the section. Don't write "No flags" — that's noise. (When `/workbook-explore` routed you here, it already surfaced these during its state-check — re-surfacing is harmless but usually redundant; keep it to the one-line flag.)

## Step 4: Stop

Don't ask "what would you like to work on?" — the user opened this chat for a reason and will state it. Asking pads the response and signals you're waiting on instructions that will arrive.

## Escalation paths

When the next prompt arrives, route to the right skill (silently — don't pre-announce):
- Decode formula logic, find overlaps or gaps → `/logic-audit`
- Audit for formula errors or broken references → `/formula-audit`
- Resume in-flight work, a deeper read than two sheets, or the Instructions C–F detail this skipped → `/workbook-explore`
- Document the session's work → `/workbook-log`
- Build a new workbook or major refactor → `/excel-finance-workbooks`

## Edge cases

**Instructions present, no Audit Log (or vice versa):** note the partial scaffolding in the summary and proceed; suggest a light `/workbook-onboarding` pass, don't block.

**User already stated a task:** skip the pickup — just do it. Re-reading context they didn't ask for is the over-helpfulness this skill restrains.

## Quality checklist

- [ ] Read only Instructions A+B and the most recent Audit Log task block — nothing else (checking the sheet-tab list for a "Handoff" sheet is allowed; reading its contents is not)
- [ ] Output is exactly the six-line template (plus optional Flags)
- [ ] No preamble, no closing question, no emoji
- [ ] In-flight Handoff or unclosed stub flagged with a pointer to `/workbook-explore` — not read in full, resumed, or routed
- [ ] Flags section omitted entirely if none ("No flags" is noise)
- [ ] No proactive analysis, formula reading, or re-auditing of prior findings
- [ ] Sheets missing → recommended `/workbook-onboarding` and stopped
