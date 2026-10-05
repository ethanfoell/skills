---
name: wrap-up
description: "Close out the current session: account for everything that changed, write the summary (Done / Where it stands / Open / Next), and propose the high-value writes (learnings, commits, doc prunes) for approval."
disable-model-invocation: true
---

Close out the current session: one pass, one report, one stop at the end. Works on any substrate: a plain chat, a code repo, anything in between.

**Route first.** A loop close-out owns the task record on its substrate; wrap-up's summary and learnings are its own either way.

- Pausing mid-task to resume later → the user runs `/handoff`.
- A finished workbook task → `/workbook-log` owns the record.
- A finished folder task → `/folder-log` owns the record.

## 1. Audit

Account for everything the session changed. In a repo: working-tree and branch state, plus whatever checks the project itself defines. Read them from the environment (package scripts, CI config) and run those, not a memorized command set. In a plain chat: decisions made, artifacts produced, anything created that lives nowhere yet. Done when nothing the session touched is unaccounted for.

## 2. Summary

Four short headed blocks, written in chat:

- **Done**: what was accomplished.
- **Where it stands**: the state right now (merged or uncommitted, saved or unsaved, working or broken).
- **Open**: unresolved questions, deferred items, anything time-sensitive.
- **Next**: the single most logical next step.

Bound: every change from the audit appears under Done or Where it stands.

## 3. Proposals

End on one Proposals block, the single stop. Each entry is a concrete write awaiting the user's yes; perform none of them unprompted. An empty block is a successful wrap-up: propose nothing over sludge.

- **A learning** that clears the bar below, pointed at its home. The home is whatever the environment names: the repo's `CLAUDE.md` or `GLOSSARY.md` when there is a repo, the surface's memory when it has one, otherwise the report itself is the home.
- **A commit**, when uncommitted work exists: name it; the repo's own contract decides the shape. (Usually the work is already merged before wrap-up runs.)
- **A doc prune**: a doc or instruction the session proved wrong, stale, or bloated. Fixing or deleting it counts as a successful wrap-up on its own.
- **An owed close-out**: the `/workbook-log` or `/folder-log` from Route first, when it hasn't run yet.

## The learning bar

The default is to write nothing. Three kinds survive:

- **A rule this project has settled on**: a convention or taste call the code can't reveal on sight.
- **A fact about the outside world**: how a library actually behaves, an API that contradicts its docs, a gotcha no config confesses.
- **A correction or preference the user voiced** about how the agent should work, with the why.

Skip anything discoverable from the files, git history, or config; anything a linter, type, or test already enforces; narrative of what happened this session; anything that only mattered to this task.
