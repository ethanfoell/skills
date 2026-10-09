---
name: daily-note
description: "Summarize the current session as a manager-facing daily note: one plain line per front of work, ready to paste into one Excel cell, plus a More detail block."
disable-model-invocation: true
---

Write a daily note: a manager-facing summary of what this chat session produced, across any kind of work. The reader is a manager glancing between meetings, so the note passes the **15-second test**: one skim leaves them with what got done, why it mattered, and what they need to know or do.

## Workflow

1. **Delegate the run.** Compaction drops work from a long chat's context, and dropped work drops out of the note; a fresh subagent reads the session's stored transcript, which compaction leaves whole. The parent locates its own transcript, since the subagent starts from the brief alone: in T3 Code, the thread ID `orchestrator_capabilities` returns as `parentThreadId`, read with `t3_thread_read`; in Claude Code, the `.jsonl` named by `$CLAUDE_CODE_SESSION_ID`; elsewhere, wherever the surface stores the session. Then it starts the subagent on the first route the surface offers:
   - **T3 Code:** `delegate_task` in `wait` mode, on the parent's provider: Claude gets `claude-opus-5-5` with `effort: high`, Codex gets `gpt-6.1-sol` with `reasoningEffort: high`.
   - **Elsewhere:** the surface's own subagent tool, starting a fresh agent at high effort on its strongest model family (`opus` in Claude Code's Agent tool); a fresh agent reads the transcript clean, where a fork carries the compacted context.

   The brief carries this file's path with the instruction to follow it from step 2, the transcript's location (in T3 Code, the parent's thread ID), today's date, and "return only the output in Format". The parent prints the returned output as it stands, correcting only a wrong date. With no subagent route, a failed one, or a subagent reporting the wrong session, the parent runs step 2 onward itself, from its stored transcript when it can reach one. Done when the subagent's output is printed or the parent has taken over.
2. **Inventory the fronts from the transcript.** Read it start to finish and confirm it holds this `/daily-note` request; a transcript without it belongs to another session, so the subagent returns "wrong session" in place of a note. List each front with its three slots filled. If the chat already holds a daily note, inventory only the work after it. Done when every piece of work in the transcript sits under a front and no front lacks an outcome.
3. **Write the note.** One line per front, largest outcome first, one to three sentences each: the three slots and nothing more. An empty inventory makes "No new work to log since the last daily note." the whole output, under the header. Done when every front appears exactly once and the note passes the 15-second test.
4. **Write `More detail:`, every time.** One `Label: sentence` line per topic, carrying what a front's line can't: the reasoning behind a structural decision, the figures a decision rests on, the context an open item needs. Done when every front has at least one detail line, and every reasoning, figure, and open item its note line leaves out sits on one.

## Fronts

A **front** is a piece of work the manager would name separately, and its test is that it has its own outcome. A two-hour drafting session on one email is one front. Ten iterations of one analysis are one front. A build with twelve components is one front. Each front carries three slots:

- **Task**, in plain terms, leading with the verb ("Audited the Sub Mapping sheet"). Add the problem it addressed when the task alone doesn't show why it mattered.
- **Outcome**, concrete: what the work produced (a deliverable, a draft, a recommendation sent, a decision taken).
- **Follow-up**, only when the manager needs it: a meeting set, a reply awaited, a blocker, an item they must act on.

Everything else in the chat is **process** and stays in the chat: cell addresses and formula identifiers; tie-outs and intermediate numbers; wording trials; tool mechanics; clarifications between the user and the agent; approaches abandoned without lasting effect; how agents were run (handoffs, prompts, which agent, how many); review rounds, reviewer counts, and test pass counts; internal references (section numbers, issue IDs, PO and receipt numbers, file names besides the deliverable); and non-events, unless the manager needs the reassurance ("approved values unchanged").

## Voice

The note goes out in the user's voice, as a competent colleague's brief status update: plain and matter-of-fact. Sentences lead with the verb and carry no subject, so the note speaks about the work and leaves the worker unnamed. The user appears only as "I", for what they personally still have to do ("I review the carrier lanes before posting"); other people appear by name or role (the manager, AP, a vendor). An agent appears only as "an agent" or "AI agent", and only when an agent is part of the outcome.

The work stays the agent's until the user reviews it, so the note reports what the work **produced**. Produced-words carry it: built, drafted, proposed, flagged, mapped, staged. Checked-words (confirmed, verified, tied out, fixed, resolved, corrected, clean) are reserved for a check the user made in the chat. A figure earns its place as the deliverable or as the number a decision rests on, and reads as the work's figure ("the draft lowers the accrual by about $18,400").

Proper nouns (workbooks, sheets, tools, people, vendors) orient the reader. Punctuate with commas, periods, parentheses, colons, and semicolons; the note carries no em dashes, since the user doesn't write with them.

## Format

The user pastes the note, and often `More detail:` beneath it, into one Excel cell under their own line for the time block, so both blocks are plain text that pastes clean:

1. `**Daily Note 5.11.2026**`, today's date as M.D.YYYY, as an ordinary chat line outside the blocks.
2. The note in a fenced `text` block: plain sentences, one line per front, the lines back to back.
3. `More detail:` in a second fenced `text` block of the same plain, back-to-back lines: first `More detail:`, then the `Label: sentence` lines.

## Examples

**One front, the claim against the product.** The chat rebuilt a freight accrual and ran reviewers over it.

Overstated:
> Rebuilt the Q3 freight accrual and confirmed it ties out cleanly to the carrier statements; three independent reviewers recomputed all 212 lanes and found zero errors. Corrected the regional carrier's $18,400 overbilling. Everything is committed and clean.

Plain:
> Rebuilt the Q3 freight accrual in the Freight Accruals workbook from the carrier statements; the draft lowers the accrual by about $18,400, mostly a billing difference with the regional carrier. Next: I review those lanes before the accrual posts.

**Two fronts, the full output:**

**Daily Note 5.12.2026**

```text
Drafted the FY27 headcount plan in the Staffing Plan workbook from the department requests and current open roles, staged for Thursday's budget review.
Mapped the packaging vendor's three billing entities to one Acumatica vendor record and flagged two duplicate invoices for AP.
```

```text
More detail:
Headcount: the draft adds 14 of the 19 requested roles; the five deferred roles sit on the Deferred tab with each manager's reason.
Cost: the draft puts the new roles at about $1.6M fully loaded for FY27, with eight hires timed to the back half.
Duplicates: the two invoices total $7,250; AP decides whether to void or credit them.
```
