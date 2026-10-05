---
name: workbook-explore
description: Orient to a workbook at session start — run a fast state-check, then present an adaptive routing menu (Resume, Continue the ticketed effort, Quick Pickup, Full orientation, Read-only scan, Onboard). The workbook loop's session-start router, with the deep dive folded in as an inline mode.
disable-model-invocation: true
---

# /workbook-explore

The session-start **router** of the `/workbook-explore` → `/workbook-plan` → `/workbook-build` → `/workbook-log` loop (with `/workbook-onboarding` and `/workbook-pickup` as its first-visit and return-visit orientation modes). It orients to an Excel finance workbook, then presents the right routes for what's present and what you need.

`/workbook-explore` is a **router, not a deep reader**: a fast state-check learns what kind of workbook this is and what's in flight, then it **presents** the modes and you invoke the one you want. Two modes are separate skills it names (`/workbook-pickup`, `/workbook-onboarding`); the rest (Resume, Full orientation, Read-only scan) it handles inline. The loop has **no separate deep-dive skill** — the deep pass is the inline **Full orientation** mode below. `/workbook-explore` also detects what those modes don't act on — a **Handoff sheet**, an **in-progress stub** in the Audit Log, **Agent sheet flags**, and a multi-session effort's queue state (a live **Tickets sheet**, a visible **Spec sheet**).

## When to use

Invoke when you land in a workbook at session start and want to orient before deciding what to do. Skip it when:
- You've already stated a task with enough context → just do it, or go to `/workbook-plan`.
- You're mid-task and want a recap → give one from context; don't re-run the state-check (the `/workbook-build` → `/workbook-explore` loop-back territory, handled gently).
- You're closing out work → `/workbook-log`.
- It's a folder or filing system → `/folder-explore`.

## Step 1: State-check

Run a fast, **detection-level** scan — learn what's present, don't analyze. Do NOT read formulas, recompute totals, or audit logic; that's the routed mode's job. Detect:

1. **Onboarding status** — does an Instructions sheet exist? (Yes → onboarded; sheets but no AI scaffolding → not onboarded.)
2. **Audit Log recency** — does an Audit Log exist, and when was it last touched (date of the most recent task block)? Is there an **in-progress stub** (a task block with status In-progress)?
3. **Workbook flavor** — sheet count and what drives it: Velixo-heavy (VelixoReportsConnections sheet or ACCOUNTTURNOVER/ACU functions), Power Query-heavy (query connections), or mostly manual.
4. **Active signals:**
   - **Handoff sheet** — a sheet named exactly "Handoff" (the deliberate cross-session continuation signal).
   - **In-progress stub** — from check 2; a task someone started but didn't close.
   - **Tickets sheet** — a sheet named exactly "Tickets" (a multi-session effort's queue; contract: the `/workbook-onboarding` skill's `MULTI-SESSION.md`). The bounded read: a status tally (N open, M in progress; Done rows ignored, as are the contract's wayfinding statuses — Fog, Graduated, Out of scope) plus the id and title of the **first unblocked open ticket** in row order — rows sit in dependency order by contract, so first-unblocked is a glance, not analysis — plus the map header's **Map status** cell (the open-map discriminator; while a map is open the first unblocked ticket is a W-row). No ticket-body or acceptance-criteria reads — that stays the routed phase's intake.
   - **Visible Spec sheet** — the Spec sheet hides on effort completion (contract: the `/workbook-onboarding` skill's `MULTI-SESSION.md`), so a *visible* Spec sheet with no Tickets sheet beside it means, by construction, an interrupted spec→tickets climb.
   - **Agent sheet flags** — if an Agent sheet exists, read ONLY its **Active risks** and **Open decisions / pending items** (the time-sensitive content). Skip conventions, gotchas, and preferences — those load on demand. While there, note any Open-decisions line carrying no status word — an untriaged item, per the sheet contract's triage mapping; the same bounded read supplies it, no extra cost.
   - **Complex-logic / stale-data flags** noted in the Audit Log's most recent findings.

The only reads beyond detection are these named, bounded ones: the Agent sheet's risk/decision sections, and the Tickets sheet's tally + first-unblocked + Map-status glance.

**Output** (3–4 sentences, no preamble):

```
[Onboarded / Not onboarded / Sheets only — no AI scaffolding]. Audit Log last touched [date or "never"]. [N] sheets, [Velixo-heavy / Power Query-heavy / mostly manual]. [Active signals: Handoff present / In-progress stub from [date] / Tickets sheet: [N] open (next: [T-id] — [title]), [M] in progress / open map on the Tickets sheet / visible Spec sheet — spec/tickets climb looks interrupted / Agent flags: [risk or decision] / Complex logic detected / Stale-data flag / "no flags"].
```

## Step 2: Present the adaptive menu

Tailor the menu to what the state-check found — don't show modes that don't apply.

**If a Handoff sheet OR in-progress stub is present**, prepend **Resume** (it takes precedence — you most likely returned to continue in-flight work):

> 0. **Resume the in-flight task** — [task title from the Handoff or stub]

When both are present, the **Handoff wins** (the more deliberate signal); note the stub secondarily: "There's also an in-progress stub from [date] — likely the same task; resolved by handling the Handoff."

**If a Tickets sheet has open tickets AND no Resume signal exists** (no Handoff sheet, no in-progress stub), prepend **Continue** instead:

> 0. **Continue the ticketed effort** — next: [T-id] — *[title]* ([N] open)

**The map fork:** when the Map status cell reads **Open**, the slot becomes charting — an open map means the way isn't charted, and the build queue doesn't exist until the frontier empties and the spec/tickets climb runs:

> 0. **Continue charting** — next map ticket: *[title]*

Precedence is **Resume > open map > ticket queue**. Continue fires only when no Resume signal exists: tickets sit in dependency order, so mid-effort the next slice usually isn't actionable until the in-flight one closes. Awareness isn't lost — the state-check tally shows whenever the sheet exists.

**If a visible Spec sheet has no Tickets sheet beside it**, the spec was written but never ticketed — an interrupted climb. No menu slot, no precedence change; note it beneath the menu and name the resumption: "Visible Spec sheet — the spec/tickets climb looks interrupted; resume it with `/to-tickets`."

**If onboarded** (an Instructions sheet exists):

> 1. **Quick Pickup** (`/workbook-pickup`) — Instructions + latest Audit Log → the six-line summary, then stop.
> 2. **Full orientation** — pickup plus a deep, evidence-routed read (data flow, Agent sheet, Velixo / logic / formula-health as warranted, companion workbook). For when you'll do real work; ends by offering `/grill-with-files`.
> 3. **Read-only scan** — a quick structural glance, no artifacts. For a coworker's workbook or a one-off look.
> 4. **Re-onboard** (`/workbook-onboarding`) — re-run onboarding if the workbook changed structurally, or to migrate meta-sheets built to an older template version (confirm-gated, content-preserving).

**If not onboarded** (no Instructions sheet), skip Quick Pickup and Full orientation (both need the scaffolding):

> 1. **Read-only scan** — a quick structural glance, no artifacts.
> 2. **Onboard** (`/workbook-onboarding`) — read every sheet, create Instructions / Audit Log / Agent sheets, surface findings.

**If the Open-decisions read found unmarked (untriaged) lines**, add one awareness line under the menu — awareness only, **no route, never one-click**; Resume still wins:

> Also: [N] untriaged item(s) on the Agent sheet — `/triage` runs the inbox-level pass when you want it.

End with "Which fits?" — don't pad. Your selection is the next message.

## Step 3: Route

- **Resume** → read the Handoff (or stub) fully. If it shows a plan ready to execute, name **`/workbook-build`**; if it's mid-planning or has open questions, name **`/workbook-plan`** (which updates the existing stub in place). Surface the Handoff's "Context to preserve" notes so they carry into the phase you name — a **named route**, not a silent compose.
- **Continue** → name **`/workbook-plan`** with the ticket's id — its down-the-stairs intake reads the ticket's acceptance criteria from the sheet; don't read them here. On the map fork, name **`/wayfinder`** instead. Named routes, user-invoked.
- **Quick Pickup / Onboard / Re-onboard** → these are separate skills. **Name the route** — "Run `/workbook-pickup`" / "Run `/workbook-onboarding`" — and let the user invoke it. Don't perform their work inline; they own it.
- **Full orientation** / **Read-only scan** → handle inline (see below).

## Full orientation mode (inline) — the folded deep dive

Deeper than pickup, still orientation (no changes) — the loop has no separate deep-dive skill. The deep read is the **grounding for the work you're about to do**: it ends by offering to hand that context to `/grill-with-files`. **Scan, don't fix.** **Route by evidence** — only read deeper or reach for a skill the workbook calls for.

**1. Inline the pickup read.** Instructions A+B + the latest Audit Log block → the six-line summary; present it before going deeper. If a Handoff sheet or unclosed stub surfaced, don't resume here (that's Resume) — note it and let the user choose.

**2. Triage — decide what to read deeper.** From the Instructions inventory and Audit Log findings:
- **Data flow** — which sheets are sources (raw, imports), which derived (formulas, rollups), which structural (mappings, config); skim 2–3 to confirm the flow. Share it in 2–3 sentences.
- **Operating context** — if an Agent sheet is present, read it now (conventions, gotchas, active risks, open decisions, preferences) and fold it into the map and the risk areas below. No Agent sheet is a normal case.
- **Complexity signals** — VelixoReportsConnections / ACCOUNTTURNOVER → reach for `/velixo-formulas`; cross-sheet SUMIFS / XLOOKUP / INDEX-MATCH chains → note dependencies; an Audit Log noting unresolved overlaps or gaps → targeted checks.
- **Risk areas** — sheets dense with cross-sheet formulas; ones the Audit Log or Agent sheet flags as fragile, recently modified, or policy-protected; anything in open findings.

**3. Route by evidence — only what the workbook needs:**
- **Live-data formulas** (Velixo / ACU) → load `/velixo-formulas` for syntax + patterns; note the connection, which sheets use it, what it pulls, any anti-patterns. (Model-invoked — composed here.)
- **Complex cross-sheet logic** → name **`/logic-audit`** for the user — "this looks like it needs `/logic-audit` to check overlaps and gaps — want to run it?" Don't auto-run it; it's user-invoked.
- **Formula-health concerns** (errors spotted, or Audit Log flags) → name **`/formula-audit`** the same way (scan-only; no fixes).
- **None of the above** → skip; the triage already gave you what you need.

**4. Companion workbook (`<connected_peers>`).** If a peer Excel agent is present — the same-workbook Excel add-on collaboration — ask it to run `/workbook-pickup` and return its summary, plan the cross-workbook reads, and compare structure (same line items? same filters? same taxonomy?), documenting where the two agree and diverge.

**5. Compile the deep-dive summary** (adapt — drop any line with nothing to say):

```
Deep orientation — [Workbook Name]
Data flow: [source → derived → output, 2–3 sentences]
Formula environment: [what drives it — Velixo / Tables / manual]
Health: [clean, or issues found with counts]
Open items: [unresolved findings or human-decision items, or omit]
Companion: [1 line if a peer workbook, or omit]
```

**6. Close — offer the grill.** The deep read just loaded the context a plan needs, so hand it forward: offer **`/grill-with-files`** to pressure-test the plan against the workbook you just read — its Audit Log decisions, the Agent-sheet DO-NOTs, and what each number ties out to. *(If you're stopping here and the dive surfaced something durable — a DO NOT EDIT, a risk, an open decision — `/workbook-log` can record it.)* Otherwise create no artifacts; orientation writes nothing.

## Read-only scan mode (inline)

The lightest mode — glancing without committing to document (a coworker's file, "just tell me what this is").

- List the sheets and their obvious roles (data / config / output / reference).
- Note the formula flavor (Velixo / Power Query / manual / mixed).
- Surface anything immediately odd (a broken-looking sheet, obvious stale data, a hidden connection sheet).
- **Create no artifacts** — read-only; this mode writes nothing.

Output: three to five sentences, structural orientation only.

```
[N] sheets: [brief roles — e.g. "2 data tabs, 1 config, 3 output dashboards"]. Driven by [flavor]. [Anything odd, or "nothing jumps out"]. [If they'll be back: "Worth onboarding if you'll work in it repeatedly."]
```

Don't read formulas in depth, audit, or recompute. If the user wants more, they'll route to a heavier mode.

## Once-per-session

`/workbook-explore` runs once per session by default. If it already ran (its state-check is earlier in chat) and you invoke it again, don't silently re-run — surface:

> Already oriented this session ([mode] on [workbook]). Re-run, or jump to `/workbook-plan` / `/workbook-build`?

A soft check, not a hard block — re-run if the workbook changed or you want a different mode.

## Agent sheet handling

No Agent sheet is a normal case — proceed without one. When one is present, the state-check reads ONLY **Active risks** and **Open decisions / pending items** (the bounded read in Step 1); the Full-orientation mode reads it in full into operating context. Don't dump the whole Agent sheet at session start — it's reference, not a summary.

## What `/workbook-explore` does NOT do

- **Modify workbook content.** Orientation only; it writes nothing. (A routed Onboard may create sheets — but the user invokes that.)
- **Read formulas or recompute during the state-check** — detection-level only, except the named bounded Agent-sheet and Tickets-sheet reads.
- **Read ticket bodies or acceptance criteria.** Detection stops at the tally, the first unblocked ticket's id + title, and the Map status cell; the routed phase's intake owns the rest.
- **Re-audit settled findings** — the Audit Log's prior findings are trusted, not re-derived.
- **Resume work itself.** It surfaces in-flight state and names the route; it doesn't reconcile or commit.
- **Propose work you didn't ask for.**

## Edge cases

**No workbook open / no finance workbook present:** say so plainly and ask what to work on — there's nothing to orient to.

**Instructions present, no Audit Log (or vice versa):** partial scaffolding — note it ("Instructions present, no Audit Log"); Quick Pickup flags the gap and proceeds against Instructions alone, or a light Re-onboard fills it. Don't block.

**In-progress stub from weeks ago, no Handoff:** surface it in Resume but note the staleness — "In-progress stub from [old date] — still active, or should it be cancelled?" Let the user decide; a cancel gets recorded next `/workbook-log`.

**Handoff sheet references a different workbook:** a Handoff sheet got copied into the wrong file — flag it ("references [other workbook] — looks misplaced; ignore it?"); don't resume against the wrong context.

**Workbook is clearly simple (1–2 sheets, no scaffolding) and the user wants a glance:** Read-only scan. Don't push onboarding on a throwaway file — mention it only if they signal they'll be back.

**Tickets sheet present but nothing open** (every row Done, Graduated, or Out of scope): a completed effort's queue record — flip-don't-delete means the sheet outlives the effort. Report the tally; no Continue slot, and don't propose deleting the sheet (the owner's later call).

**Velixo flavor detected but the user picks Quick Pickup:** Quick Pickup is deliberately shallow — it won't load `/velixo-formulas`. That's correct; the reference loads at `/workbook-plan` / `/workbook-build` time, or in Full orientation, when there's actual Velixo work.

## Quality checklist

- [ ] State-check is detection-level — no formula reading, no recompute, no re-audit (only the named bounded Agent-sheet and Tickets-sheet reads)
- [ ] Tickets-sheet read is bounded — status tally, first unblocked ticket's id + title, Map status cell; never ticket bodies or acceptance criteria
- [ ] Output is 3–4 sentences in the locked format
- [ ] Menu is adaptive — only modes that apply
- [ ] Resume prepended + prioritized when a Handoff or stub exists; Handoff wins over stub when both present
- [ ] Continue slot fires only with no Resume signal; an open map flips it to `/wayfinder` (Resume > open map > ticket queue); a visible Spec sheet with no Tickets sheet names `/to-tickets` as a note, not a slot
- [ ] Quick Pickup / Onboard named for the user to invoke, not performed inline; Resume names `/workbook-plan` vs `/workbook-build`, not a silent compose
- [ ] Full orientation and Read-only scan create no artifacts (Full orientation may offer `/workbook-log`, which writes only if accepted)
- [ ] Full orientation routes by evidence — composes `/velixo-formulas`, present-and-names the audits, preserves the `<connected_peers>` companion read — and ends by offering `/grill-with-files`
- [ ] Once-per-session surfaced if already run
- [ ] Absence of an Agent sheet handled as a normal case
