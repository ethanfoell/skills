---
name: daily-note
description: Summarize the current chat session as a manager-scannable daily note: a maximally dense headline, plus a fuller follow-on cut when there's more worth knowing. Use when the user asks to summarize a session, log the day's work, or invokes /daily-note.
---

Generate a daily note: a concise, manager-facing summary of what a chat session accomplished. It works across **any** kind of work — spreadsheet builds, analysis, research, writing, planning, modeling, messaging — not just Excel.

This is **not** an audit trail. Forensic detail belongs in the Audit Log via the `/workbook-log` skill, not here.

## The two notes

A daily note is, by default, **two parts for one reader** — the same skimming manager:

1. **The note** — a maximally dense headline that passes the 15-second test on its own.
2. **`More detail:`** — a fuller cut beneath it, carrying the genuinely valuable nuance the dense headline had to leave out.

Produce both by default; don't ask. But the second part earns its place by value, never volume: when the dense note already says everything that matters, **drop `More detail:` entirely** and show only the note. The fuller cut is *standing*, not *forced* — it has more to say on a busy day and nothing at all on a light one.

## The 15-second test

The reader is a **manager, or someone above them, glancing at notes between meetings**. They are skimming to confirm the work is real and to flag anything they must act on.

The dense note must pass this: in a 15-second skim, does the reader come away with (a) what got done, (b) why it mattered, and (c) anything they need to know or act on? If yes, the note is doing its job. `More detail:` is for the reader who wants to go one level deeper — never required reading.

## Length

**The note: default to maximally dense.** Compress every line until each word earns its place; never pad up to look substantial. Its *length* is still decided by the work, not the chat: a two-hour chat of drafting iterations on one email might be a single sentence; a 30-minute structural decision affecting future work might be a tight paragraph; a genuine three-front day names all three fronts. But it always sits at the compressed floor.

**Note vs. More detail — the division of labor.** The note names *what happened* (the outcome on each front). `More detail:` carries *why and how much*: the reasoning behind a structural decision, itemized numbers, the context an open item needs. They do not overlap.

**`More detail:` carries genuine value when** one or more holds:
- A structural decision was made that affects future work, and the reasoning isn't self-evident from the outcome.
- Significant quantitative outcomes are worth itemizing (totals, deltas, coverage, dollar amounts, a per-component breakdown).
- Open items exist that the manager needs context on to act (one brief sentence each).
- Two or more genuinely distinct workstreams each produced outcomes worth expanding beyond the headline.

When none holds, **suppress `More detail:`** — the note alone is the daily note.

**Never expand — in either part — for** drafting-and-redrafting (one task, one mention), step-by-step replay (collapse to the outcome), repeated iterations of one analysis (state the final answer), showing your work, or listing every component of a build when the headline tells the story.

### The drafting-session trap

Sessions spent drafting a message are the most common cause of over-long notes — the chat fills with register experiments and wording trials, none of which matter to a manager. For a drafting session, the note includes only the task and recipient, the structural point or recommendation the message made, and the follow-up (meeting set, awaiting reply, sent and closed); `More detail:` almost always suppresses.

**Too long:**
> Drafted and refined a response to Sam's counter-proposal on Ramp approval chains. Worked through several iterations to find the right register, firm on the existing structure but open to a meeting. The final version acknowledged his cost-asymmetry point specifically, named the precedent risk if customizations stack per department, and framed the meeting as a pressure test of his proposal rather than open-ended deliberation. The message has been sent.

**Right length:**
> Responded to Sam's counter-proposal on the Ramp approval chain restructure. Held the line on the existing principle (vendor owners must report to a C-suite exec) while accepting a meeting to walk through both approaches. Sent.

## Show value without claiming it

A daily note should justify the time spent without ever saying so.

**Do:**
- Lead with the task in plain terms ("Audited X", not "Spent time reviewing X").
- State the problem the work addressed when the significance isn't obvious from the task alone.
- Name the outcome concretely: a metric, a delta, a decision, a recommendation sent, a deliverable produced.
- Use proper nouns liberally (workbooks, sheets, tools, people, vendors) for orientation.

**Don't:**
- Explain your thought process ("I noticed that…", "after considering…").
- Defend the time spent ("this was a significant build", "took careful work").
- Hedge the outcome ("hopefully this will help…", "this should make things easier…").
- Pad with connective filler ("Additionally", "Furthermore", "It's worth noting that").

## Output format

**Header:** `**Daily Note [M.D.YYYY]**`, using the current date.

**The note:** directly under the header, unlabeled — connective prose, no bullets. One paragraph, or one short paragraph per distinct front on a genuine multi-front day.

**`More detail:`** after a blank line, introduced by a bold **`More detail:`** label, when it carries genuine value (see **Length**). Prose in the same voice; a tight bullet list is allowed *only* for genuinely list-shaped content (open items to act on, a run of itemized numbers). Suppress the whole block — label and all — when the note already says everything that matters.

**Style** (both parts):
- **No em dashes (—) anywhere in the note.** The user doesn't write with them; use commas, periods, parentheses, colons, or semicolons instead.
- Keep meaningful numbers (totals, deltas, percentages, dollar amounts that tell the story).
- Tone: confident, professional, plain — a competent colleague giving a brief status update.

**Leave out** (a daily note is a summary, not a record; this governs both the note and More detail):
- Cell addresses, ranges, formula identifiers.
- Intermediate verification numbers and tie-outs.
- Drafting iterations, register experiments, wording trials.
- Tool mechanics ("used execute_office_js to…").
- Back-and-forth clarifications between user and assistant.
- Failed approaches abandoned with no lasting impact.
- Preamble and meta-commentary ("Today I worked on…").
- Exhaustive risk lists — name only the open items the manager must act on.

## Workflow

1. **Scan the full conversation.** Read every message. For each piece of work, ask: what was the task in plain terms, what concrete outcome did it produce, and is there a follow-up the manager needs to know about? Apply **Leave out** as you go.
2. **Write the note** — the maximally dense headline, length decided by the work (the **Length** section). Strip any em dashes before presenting.
3. **Add `More detail:` when it carries genuine value**, or suppress it. Pull in the reasoning, itemized numbers, or open-item context the dense note had to cut — "the same kinds of content, more of it," never "now I'll explain how I got there." If nothing clears the value bar (a light or routine session), suppress the block and stop at the note.

## Repeat invocations in the same chat

Before writing, scan for a daily note already produced in this chat. If one exists, summarize only work that occurred after it, and write the new note (with `More detail:` if warranted) as a standalone — no backward reference, no "(continued)" tag. If no new meaningful work occurred, say so ("No new work to log since the last daily note") rather than padding.

## Examples

**Single focus, structural work (note + More detail):**
> **Daily Note 5.11.2026**
>
> Audited the Sub Mapping sheet on Budget vs Actuals v14, which bridges Acumatica actuals to the budget structure, and found it covered only 31% of GL combinations from actual spend, so the majority of actuals were silently bypassing the BvA comparison. Built out the missing mappings, improving coverage from 31% to 64% of actuals rows.
>
> **More detail:** The new mappings spanned three areas: COGS brand rollups (mirroring the existing revenue pattern), expense department gaps across 11 GL accounts, and channel mappings for Foxglove and Driftwood.

**Two distinct workstreams (note + More detail):**
> **Daily Note 5.12.2026**
>
> Aligned the CFO P&L on Budget vs Actuals v15 against the CFO's original blueprint and built a formal P&L Comparison sheet to present for structural buy-in. Three structural questions and the Acumatica payroll permissions blocker remain open for the CFO conversation.
>
> **More detail:** The comparison ran all 148 of my line items against his 139 side-by-side (90 identical, 44 modified, 14 only in mine, 5 only in his). Executed five fixes with clear CFO precedent, the biggest moving $1.4M YTD from a misclassified Amortization line to Interest Expense. Open for the CFO: the Returns-reserve breakout, the Fulfillment/Logistics sub overlap, and Software-subscriptions placement; the payroll permissions blocker (~$520K/month across 5 GLs) has a Teams message drafted but not sent.

**Drafting / messaging session (note only — More detail suppressed):**
> **Daily Note 5.14.2026**
>
> Worked through a Ramp approval chain gap. AP flagged Priya M. missing from Ops invoice approvals; diagnosed the cause (vendor owners report to a mid-level manager beneath Priya, so the chain skips her entirely) and drafted a message to the accounting team proposing a structural fix: require vendor owners to report directly to a C-suite exec. Meeting set to walk through before committing.

**Light session (note only — More detail suppressed):**
> **Daily Note 5.6.2026**
>
> Pulled Q1 2026 revenue from Amazon Seller Central for the 4/22 to 5/6 settlement period and tied the $48,500 deposit to the bank statement cleanly. Also fixed a stale Dashboard lookup pointing at a deleted column.

**Different kind of work — a tooling / skill-authoring session (note + More detail):**
> **Daily Note 5.15.2026**
>
> Revised the Velixo Formulas Claude skill to make it shareable across the finance team and packaged it as a `.skill` file, then shared it with a coworker over Teams who had been briefed in a prior meeting.
>
> **More detail:** Universalized the skill's personal references and generalized its workbook-specific examples so it applies team-wide; the Teams message linked the build chat for context.

**Repeat invocation (later in the same chat, stands on its own):**
> **Daily Note 5.8.2026**
>
> Built out the Audit Log Workbook Snapshot section on the Budget vs Actuals workbook, covering source data, key totals, sheet list, dependencies, and current status. Also created two reusable Claude skills (audit-log and daily-note) to standardize session logging and manager-facing summaries across future workbooks.
