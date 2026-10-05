---
name: folder-explore
description: Orient to a folder at session start — run a fast state-check, then present an adaptive routing menu (Resume, Integrate, Continue, Quick Pickup, Full orientation, Read-only scan, Onboard). The folder loop's session-start router.
disable-model-invocation: true
---

# /folder-explore

The session-start **router** of the `/folder-explore` → `/folder-plan` → `/folder-build` → `/folder-log` loop (with `/folder-onboarding` and `/folder-pickup` as its first-visit and return-visit orientation modes). It orients to a folder, then presents the right routes for what's present and what you need.

`/folder-explore` is a **router, not a deep reader**: a fast state-check learns what kind of folder this is and what's in flight, then it **presents** the modes and you invoke the one you want. Two modes are separate skills it names (`/folder-pickup`, `/folder-onboarding`); the rest (Resume, Integrate, Full orientation, Read-only scan) it handles inline. It also detects what those modes don't act on — **in-flight work** (a dirty Git tree, or an open `LOG.md` stub on a file-based folder), a **parked handoff**, and a **ticketed effort's queue** (an `issues/` folder of per-ticket files at the folder root, with any wayfinder map beside it).

## When to use

Invoke when you land in a folder at session start and want to orient before deciding what to do. Skip it when:
- You've already stated a task with enough context — just do it.
- You're mid-task and want a recap — give one from context; don't re-run the state-check.
- You're closing out work — use `/folder-log`.
- It's an Excel workbook → `/workbook-explore`.

## Step 1: State-check

Run a fast, **detection-level** scan — learn what's present, don't analyze. Do NOT crawl the tree, read file contents, or re-derive structure; that's the routed mode's job (and the real task's). Detect:

1. **Onboarding status** — do `README.md` and `CLAUDE.md` exist at top level? (Both → onboarded; one → partial; neither → not onboarded.) Note a `GLOSSARY.md` glossary if one sits alongside — but it's **not part of this test**: a folder earns a glossary only when it has terms worth pinning, so README+CLAUDE.md with no `GLOSSARY.md` is still fully onboarded. A legacy `CONTEXT.md` is the same glossary under its old name: read it as the glossary, and flag renaming it to `GLOSSARY.md`.
2. **History recency** — dispatch on the folder's **recorded history layer** (the standing line in its CLAUDE.md): on Git, the most recent commit date (`git log`); on a file-based folder, the top `LOG.md` entry's date. No recorded choice → fall back to README `Status` / file mtimes, and note that `/folder-onboarding` would record one. A `git log`/`status` that only emits `unable to unlink … lock` warnings has still reported correctly — trust it; that warning is the ungranted Cowork file-delete permission (`/folder-onboarding` and `/folder-log` handle it), not a dead repo.
3. **Folder flavor** — one line, from names and extensions only: code/plugin, document store, data, media, workbook-heavy (mostly `.xlsx`), mixed.
4. **Active signals:**
   - **In-flight work** — on Git, `git status` shows uncommitted changes (work started, not committed); on a file-based folder, an **open stub** at the top of `LOG.md` — an entry still marked **In progress** (`/folder-build` opens it at execution start; `/folder-log` completes it at close). An old-dated stub is likely abandoned work — note the staleness.
   - **Parked handoff** — a top-level `HANDOFF.md` or a `future-work/` entry that reads as an active paused task.
   - **Inbox queue** — if the folder uses the inbox convention (items with `Target`/`Rung` headers, e.g. `future-work/`), read **only those item headers** (not bodies) and tally open items by rung. No-op if there's no inbox.
   - **Ticket queue** — if the folder is a multi-session effort's root, a top-level `issues/` folder of per-ticket files (`issues/<NN>-<slug>.md` — `/to-tickets`' local form; `/folder-onboarding` records the convention). Detection is a bounded per-file read: count ticket files **open vs done by each file's one-line `Status:`**, and note the **first unblocked** open ticket — files are numbered in dependency order, so the lowest-numbered open ticket whose `Blocked by:` line names no still-open ticket is a glance, not analysis. No acceptance-criteria or body reads (that's the routed phase's intake), and **never a `gh` or network query** — the queue detected here is the file-shaped one; a repo-configured tracker is owned by the repo's tracker doc and `/folder-plan`'s stairs pointer. No-op if there's no `issues/` folder.
   - **Wayfinder map** — a `map.md` at the folder root (`/wayfinder`'s local-markdown form): a **presence check only**. Present means the effort is still being charted.
   - **CLAUDE.md flags** — if a CLAUDE.md exists, read ONLY its **Active risks**, **Open decisions**, and any **DO NOT EDIT** policy. Skip conventions and gotchas (they load on demand).
   - **README Status flags** — a "needs attention / in-progress" note.

The only reads beyond detection are these named, bounded ones: CLAUDE.md's risk/decision/DO-NOT-EDIT sections, inbox item *headers*, and ticket files' `Status:`/`Blocked by:` lines.

**Output** (3–4 sentences, no preamble):

```
[Onboarded / Partially onboarded / Not onboarded]. [History: last commit <date> / top LOG.md entry <date> / none recorded → README+mtime fallback]. [Folder flavor]. [Active signals: dirty working tree (N files) / open LOG.md stub (<date> — <task title>) / parked handoff / inbox: N open (e.g. 2 proposed-change, 2 task, 2 idea) / tickets: N open (next: <NN> — <title>) / open wayfinder map / CLAUDE.md risk: <one line> / DO NOT EDIT: <area> / "no flags"].
```

## Step 2: Present the adaptive menu

Tailor the menu to what the state-check found — don't show modes that don't apply.

**If in-flight work (a dirty tree or an open `LOG.md` stub) OR a parked handoff is present**, prepend **Resume** (it takes precedence — you most likely returned to continue in-flight work):

> 0. **Resume in-flight work** — [the handoff's task title, the open stub's task title, or "uncommitted changes in N files"]

When both are present, the **parked handoff wins** (it's the deliberate signal); note the in-flight state secondarily.

**If the inbox has `proposed-change` items** (decided, ready to land), prepend **Integrate**:

> 0. **Integrate inbox proposed-change(s)** — [N ready: short titles]

Lower rungs (idea/task) are surfaced for awareness but get **no route** — acting on them is deliberate, never one-click: `/triage` for the inbox-level pass (the sweep, the rejection-memory check, the state machine), `/grill-with-files` for promoting a single item. When both apply, list Resume before Integrate.

**If the ticket queue has open tickets AND no Resume signal is present**, prepend **Continue** — present-and-naming `/folder-plan`, whose down-the-stairs intake reads the ticket's acceptance criteria into its Validation section:

> 0. **Continue the ticketed effort** — next: <NN> — *<title>* (N open) → run `/folder-plan`

**The map fork — an open map wins:** if `map.md` is present, the way isn't charted yet and the build queue isn't the next move; the slot becomes:

> 0. **Continue charting** — next map ticket: *<title>* → run `/wayfinder`

(A map's child tickets are the same `issues/` files, so the tally's first-unblocked pick already supplies the title — no `map.md` read.)

Continue **coexists with Integrate** (inbox items are independent of the effort — both shown when both apply); the 0-slot order is **Resume > Integrate > Continue**. Any Resume signal suppresses Continue entirely: tickets sit in dependency order, so mid-effort the next slice usually isn't actionable until the in-flight one closes. Awareness isn't lost — the state-check tally shows whenever the queue exists.

**If onboarded** (README + CLAUDE.md exist):

> 1. **Quick Pickup** (`/folder-pickup`) — the two surfaces + recent history → the six-line summary, then stop.
> 2. **Full orientation** — pickup plus a deeper read (full README + CLAUDE.md, sample the key areas). For when you'll do real work.
> 3. **Read-only scan** — a quick structural glance, no artifacts. For someone else's folder or a one-off look.
> 4. **Re-onboard** (`/folder-onboarding`) — re-run onboarding if the folder changed structurally.

**If not onboarded** (surfaces missing), skip Pickup and Full orientation (both need the surfaces):

> 1. **Read-only scan** — a quick structural glance, no artifacts.
> 2. **Onboard** (`/folder-onboarding`) — read the structure, lay down README + CLAUDE.md, choose and record the history layer, surface findings.

**If the flavor is workbook-heavy**, add one route line after the menu — this loop stays at folder grain; orienting *inside* a workbook is the workbook loop's:

> To orient inside a specific workbook, open it and run `/workbook-explore`.

End with "Which fits?" — don't pad. Your selection is the next message.

## Step 3: Route

- **Resume** → read the parked handoff in full (or, for a dirty tree, `git status` / `git diff --stat`; for an open `LOG.md` stub, the stub entry). Re-establish the in-flight context, hand back to continue the work, and point to `/folder-log` to close out. Carry any "context to preserve" notes forward.
- **Integrate** → read the named `proposed-change` item(s) in full, integrate per each item's target, self-check, then surface the result for **human approval** before `/folder-log` records and archives it — don't auto-merge. If an item isn't a decided change yet, `/grill-with-files` is the promote step, not integration.
- **Continue** → a separate skill's lane: name the route — "Run `/folder-plan`" on the named next ticket, or "Run `/wayfinder`" on the open map — and let the user invoke it. Don't read the ticket body or start planning inline.
- **Quick Pickup / Onboard / Re-onboard** → these are separate skills. **Name the route** — "Run `/folder-pickup`" / "Run `/folder-onboarding`" — and let the user invoke it. Don't perform their work inline; they own it.
- **Full orientation** / **Read-only scan** → handle inline (see below).

## Full orientation mode (inline)

Deeper than pickup, still orientation (no changes) — the suite has no separate deep-dive skill.

- Start from the `/folder-pickup` summary (the two surfaces + recent history).
- Read the rest of the README (Layout, conventions, how-to, known issues) and CLAUDE.md (conventions, gotchas).
- Sample the key areas the README names as nerve centers — enough to confirm the docs match reality, not a full crawl.
- **Create no artifacts.**

Output: the six-line summary, then a short **Full context** addendum (3–6 lines) — organizing principle, nerve centers, conventions in force, and any drift between docs and disk.

## Read-only scan mode (inline)

The lightest mode — glancing without committing to document (someone else's folder, "just tell me what this is").

- List the top-level areas and their obvious roles (source / working / output / docs / archive).
- Note the folder flavor.
- Surface anything immediately odd (a stale area, an unexplained dump, a missing entry point).
- **Create no artifacts** — read-only; this mode writes nothing.

Output: three to five sentences, structural orientation only. If the user will be back repeatedly, mention onboarding is worth it; otherwise don't push it.

## Once-per-session

`/folder-explore` runs once per session by default. If it already ran (its state-check is earlier in chat) and you invoke it again, don't silently re-run — surface:

> Already oriented this session ([mode] on [folder]). Re-run, or get to work?

A soft check, not a hard block — re-run if the folder changed or you want a different mode.

## CLAUDE.md handling

The state-check's read of a present CLAUDE.md is the bounded one named in Step 1 (risks / decisions / DO NOT EDIT). Don't dump the full file at session start — it's reference, not a summary. (In Cowork / Claude Code it may already be auto-loaded; consult it in place.) No CLAUDE.md is a normal case — the not-onboarded menu handles it.

## What `/folder-explore` does NOT do

- **Modify folder content.** Orientation only; it writes nothing. (A routed Onboard may create surfaces — but the user invokes that.)
- **Crawl the tree or read file contents during the state-check** — detection-level only, except the named bounded reads.
- **Resume work itself.** It surfaces in-flight state and routes; it doesn't reconcile or commit.
- **Query a remote tracker.** Ticket detection is file-shaped only — `Status:`/`Blocked by:` lines of local files; never a `gh` or network call.
- **Propose work you didn't ask for.**

## Edge cases

**No folder context:** say so plainly and ask what to work on.

**README but no CLAUDE.md (or vice versa):** partial scaffolding — note it; a light `/folder-onboarding` pass fills the gap. Don't block.

**Dirty tree from long ago, no handoff:** surface it in Resume but note the staleness — "uncommitted changes from <old date> — resume, or commit/discard first?" Let the user decide. (File-based analog: an open `LOG.md` stub dated long ago — same question, with `/folder-log` as the close-or-cancel path.)

**Parked handoff references a different folder:** a `HANDOFF.md` got copied in — flag it; don't resume against the wrong context.

**No recorded history layer** (and no repo): note it; recency falls back to README Status / mtimes. Onboard would choose and record one; don't init or seed a `LOG.md` during explore. (A lock warning isn't "no Git" — it's the ungranted file-delete permission.)

**`/folder-explore` mid-task to mean "remind me where we are":** brief recap from chat context, not a full re-run.

**Simple folder, user wants a glance:** Read-only scan. Don't push onboarding on a throwaway folder.

## Quality checklist

- [ ] State-check is detection-level — no tree crawl, no file-content reads, no structure re-derivation (only the named bounded reads)
- [ ] Output is 3–4 sentences in the locked format
- [ ] Menu is adaptive — only modes that apply
- [ ] Workbook-heavy flavor judged from names/extensions only (no file opened); its `/workbook-explore` route line offered; no cross-workbook aggregation
- [ ] Resume prepended + prioritized on in-flight work or a parked handoff; handoff wins over the in-flight signal
- [ ] Integrate prepended for proposed-change only; idea/task surfaced with no route; no-op when no inbox
- [ ] Ticket detection bounded — per-file `Status:`/`Blocked by:` lines only, no acceptance-criteria or body reads, never a `gh`/network query
- [ ] Continue prepended only with no Resume signal; coexists with Integrate; 0-slot order Resume > Integrate > Continue
- [ ] Open map wins — Continue charting → `/wayfinder`; otherwise the next ticket → `/folder-plan`
- [ ] Read-only scan and Full orientation create no artifacts
- [ ] Quick Pickup / Onboard named for the user to invoke, not performed inline
- [ ] Once-per-session surfaced if already run
- [ ] Absence of a CLAUDE.md or a recorded history layer handled as normal
