---
name: retitle-sessions
description: Batch-improve the titles of past Claude Code sessions so you can tell at a glance what each old chat did. Proposes better names and helps you apply them. CCD/Cowork only.
disable-model-invocation: true
argument-hint: "(optional) a project path to deep-check, e.g. ~/dev/foo"
---

Walk a **backlog** of badly-titled past sessions and propose a better name for each, so your session list tells you at a glance what each old chat did. The app already shows each session's Project and date on their own axes — the title's job is the work.

**Proposal-only.** No tool renames a past session, so you apply the names — this skill's job is to make that fast. It runs only in **CCD / Cowork**: it reaches other sessions through the session-mgmt tools and on-disk transcripts, which the plain website and Excel surfaces don't have.

## Steps

1. **Scope the backlog.** Call `mcp__ccd_session_mgmt__list_sessions` (it has no project filter — it returns every project's recent sessions) and **keep only entries whose returned `cwd` is the current project**. Widen only when asked — *all projects* or *include archived*, or **deep-check a project** when a path argument is passed (investigate that one project harder). Never sweep all of `~/.claude/projects` by default — another machine may hold a huge history. See [FINDING-SESSIONS.md](FINDING-SESSIONS.md).

2. **Flag candidates.** Keep only the **badly-titled**: title missing, all-lowercase or ungrammatical, generic ("New session", a first-message fragment), or over-granular (numbers/IDs with no codebase). Leave already-good titles alone. Show the flagged set and get a nod before reading transcripts. If nothing is flagged, say so plainly and stop — don't produce an empty table; offer to widen scope or deep-check a named project.

3. **Read each candidate.** Pull the **opening user turn** (and a few early turns) from its on-disk transcript to learn the codebase and the work — that turn is also how you *confirm* you found the right session, since the session→file join is heuristic. Read opening turns only, not whole files. For a large backlog, offer to fan the reads out across parallel subagents (or a Workflow). See [FINDING-SESSIONS.md](FINDING-SESSIONS.md).

4. **Propose a name** per session by reusing the `chat-title` grammar — subject-first, the high-level work outcome; omit the repo/date, translate ADR/PRD/slice numbers up to what they refer to. Because this skill sees the whole backlog, also make each title distinct from its neighbours. See [TITLE-GRAMMAR.md](TITLE-GRAMMAR.md).

5. **Present the proposal** as one table:

   | Old title | Proposed title | Why | Find it by |
   |---|---|---|---|

   *Find it by* = the old title and its date — or, for an untitled session, its `cwd` plus date/time — so every row is locatable, even with no old title. Mark **archived** rows (from `isArchived`); their rename lives in the app's separate Archived list.

6. **Hand over an apply path** (you pick):
   - **Paste from the table** — rename each session yourself in the app.
   - **Worklist** — the same set as a copy-paste-ready list (find-by → new title), if you'd rather work a checklist.
   - **Computer-use auto-apply** — *only when you explicitly ask.* The skill drives the app UI to set the titles for you. It's usage-heavy — say so before starting. See [APPLY-WITH-COMPUTER-USE.md](APPLY-WITH-COMPUTER-USE.md).

**Done when** every flagged session has a proposed title in the table (or is explicitly left as-is) and you've been handed an apply path. The skill never renames, archives, or deletes a session itself.
