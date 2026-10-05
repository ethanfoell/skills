---
name: daily-note
description: "Summarize the current session as a manager-facing daily note: one dense mention per front of work, plus a More detail cut only when it earns it."
disable-model-invocation: true
---

Write a daily note: a manager-facing summary of what this chat session accomplished, across any kind of work (workbook builds, analysis, research, writing, planning, messaging).

## The reader

A manager, or someone above them, glancing between meetings to confirm the work is real and to catch anything they must act on. The note passes the **15-second test**: one skim leaves the reader with what got done, why it mattered, and what they need to know or do.

## Fronts

A **front** is a piece of work the manager would name separately, and its test is that it has its own outcome. A two-hour drafting session on one email is one front. Ten iterations of one analysis are one front. A build with twelve components is one front. Each front carries three slots:

- **Task**, in plain terms, leading with the verb ("Audited the Sub Mapping sheet"). Add the problem it addressed when the task alone doesn't show why it mattered.
- **Outcome**, concrete: a metric, a delta, a decision, a recommendation sent, a deliverable produced, the final answer.
- **Follow-up**, only when the manager needs it: a meeting set, a reply awaited, a blocker, an item they must act on.

Everything else in the chat is **process** and stays in the chat: cell addresses and formula identifiers, tie-outs and intermediate numbers, wording trials, tool mechanics, clarifications between the user and the agent, approaches abandoned without lasting effect.

## Workflow

1. **Inventory the fronts.** Read every message and list each front with its three slots filled. If the chat already holds a daily note, inventory only the work after it, for a standalone note. Done when every piece of work in the chat sits under a front and no front lacks an outcome.
2. **Write the note, dense.** One mention per front, largest outcome first, and a mention is its three slots and nothing more. The slots decide the length: a one-front day may be a single sentence, a three-front day names all three. An empty inventory writes "No new work to log since the last daily note" under the header. Done when every front from the inventory appears exactly once and the note passes the 15-second test.
3. **Decide `More detail:` yourself, from the bar below.** When it clears, add the block; when it doesn't, the note alone is the daily note.

## The More detail: bar

`More detail:` carries a front's *why* and *how much* when its three slots can't: the reasoning behind a structural decision, the itemized numbers, the context an open item needs. It clears the bar when at least one holds:

- A structural decision affects future work and its reasoning isn't self-evident from the outcome.
- Quantitative outcomes are worth itemizing (totals, deltas, coverage, dollar amounts, a per-component breakdown).
- An open item needs context before the manager can act (one sentence each).
- Two or more fronts each have an outcome worth expanding past their mention.

When none holds, the block and its label are absent.

## Register

A competent colleague giving a brief status update: confident, plain, matter-of-fact. Value shows through the task and the outcome, so the note states both and stops. Proper nouns (workbooks, sheets, tools, people, vendors) orient the reader; meaningful numbers (totals, deltas, percentages, dollar amounts) tell the story. Punctuate with commas, periods, parentheses, colons, and semicolons; the note carries no em dashes, since the user doesn't write with them.

## Format

- Header: `**Daily Note 5.11.2026**`, today's date as M.D.YYYY.
- The note directly under the header, unlabeled, flowing prose without bullets: one paragraph, or one short paragraph per front on a multi-front day.
- `More detail:` after a blank line, opened by the bold label **`More detail:`**, in the same voice; a tight bullet list only for list-shaped content (open items, a run of itemized numbers).

## Examples

**One front, a drafting session.** The chat is full of register experiments and wording trials; the front's slots are the task and recipient, the point the message made, and the send status.

Too long:
> Drafted and refined a response to Sam's counter-proposal on Ramp approval chains. Worked through several iterations to find the right register, firm on the existing structure but open to a meeting. The final version acknowledged his cost-asymmetry point specifically, named the precedent risk if customizations stack per department, and framed the meeting as a pressure test of his proposal rather than open-ended deliberation. The message has been sent.

Right length:
> Responded to Sam's counter-proposal on the Ramp approval chain restructure. Held the line on the existing principle (vendor owners must report to a C-suite exec) while accepting a meeting to walk through both approaches. Sent.

**Two fronts, `More detail:` clears the bar:**
> **Daily Note 5.12.2026**
>
> Aligned the CFO P&L on Budget vs Actuals v15 against the CFO's original blueprint and built a formal P&L Comparison sheet to present for structural buy-in. Three structural questions and the Acumatica payroll permissions blocker remain open for the CFO conversation.
>
> **More detail:** The comparison ran all 148 of my line items against his 139 side-by-side (90 identical, 44 modified, 14 only in mine, 5 only in his). Executed five fixes with clear CFO precedent, the biggest moving $1.4M YTD from a misclassified Amortization line to Interest Expense. Open for the CFO: the Returns-reserve breakout, the Fulfillment/Logistics sub overlap, and Software-subscriptions placement; the payroll permissions blocker (~$520K/month across 5 GLs) has a Teams message drafted but not sent.

**Light session, `More detail:` absent:**
> **Daily Note 5.6.2026**
>
> Pulled Q1 2026 revenue from Amazon Seller Central for the 4/22 to 5/6 settlement period and tied the $48,500 deposit to the bank statement cleanly. Also fixed a stale Dashboard lookup pointing at a deleted column.
