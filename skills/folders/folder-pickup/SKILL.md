---
name: folder-pickup
description: Quick re-orientation for an already-onboarded folder — read its README + CLAUDE.md and its recent history, return a locked six-line summary, flag anything in-flight, then stop. The folder loop's return-visit mode.
disable-model-invocation: true
---

# /folder-pickup

Fast return-visit re-orientation for a folder you've worked in before — the counterpart to `/folder-onboarding`. Where onboarding lays down the orientation surfaces, this reads them back, gets you just-oriented-enough, then stops. The Quick Pickup mode `/folder-explore` names.

## When to use

For quick context on an **already-onboarded** folder (one with a `README.md` + `CLAUDE.md`). Skip it when:
- It's a first encounter (no surfaces) → `/folder-onboarding`.
- You've already stated a task → just do it; don't re-read context.
- It's an Excel workbook → `/workbook-pickup`.

## The core discipline: restraint

This skill exists to enforce **restraint**, not to analyze. The default failure on landing in a folder is to over-helpfully crawl the tree, read everything, and start proposing cleanup. The discipline: read the two surfaces and the recent history, summarize in the locked template, optionally flag, then stop and wait.

- Don't crawl the tree or read file contents beyond the two surfaces (plus a glance at `CONTEXT.md` if present).
- Don't re-derive structure — trust the README and CLAUDE.md.
- Don't "while I'm here…" anything (no reorganizing, cleanup, or audits).
- Don't propose work the user hasn't asked for.

The user knows what's next and will say it. The job is to be oriented enough to help when they do.

## Step 1: Read the surfaces + recent history

- **`README.md`** — **Purpose/Overview** and the dated **Status** only. Glance at the Layout for names; skip how-to-use, conventions, known-issues.
- **`CLAUDE.md`** — only the time-sensitive parts: any **DO NOT EDIT** policy, and **Active risks / Open decisions** if present. Skip standing conventions and gotchas. (If it's already auto-loaded, consult in place — don't re-read.)
- **`CONTEXT.md`** *(if present)* — skim the glossary terms so the summary speaks the folder's canonical vocabulary. A bounded glance like the CLAUDE.md read, not a tree crawl; it feeds the existing lines and **adds no line** — the six-line template stays frozen.
- **The history layer** — dispatch on the folder's recorded choice (the standing line in its CLAUDE.md): on Git, `git log` for the last few commits ("last touched") and `git status` for uncommitted changes (the in-flight signal, Step 3); on a file-based folder, the top `LOG.md` entries for last-touched, with an **open stub** at the top (an entry still marked **In progress**) as the in-flight signal. No recorded choice → fall back to README `Status` / mtimes; don't repair, init, or seed. A lock warning is the ungranted file-delete permission, not a dead repo — trust a `git log` that still reports.

If neither surface exists, stop and recommend `/folder-onboarding`. If only one, note the partial scaffolding and proceed.

## Step 2: Return the locked summary

Exactly six lines, no prose, no extras:

```
Folder: [name]
Purpose: [one line from README Purpose/Overview]
Status: [one line from the README Status section]
Open threads: [2–4 bullets, latest first; "none" if clean]
Edit restrictions: [DO NOT EDIT items from CLAUDE.md, or "none"]
Last touched: [date + summary of the most recent history-layer record]
```

No introduction, no closing question, no emoji.

## Step 3: Surface flags (only if any exist)

Add a **Flags** section only if one of these is present:

- An active **DO NOT EDIT** policy.
- Unresolved **Active risks** in CLAUDE.md.
- **Stale or misfiled material** flagged in README Status / known-issues.
- Anything the last session flagged but didn't resolve.
- **In-flight state** — uncommitted changes (`git status` dirty) or, on a file-based folder, an open `LOG.md` stub (the top entry still marked **In progress**); or a parked handoff (a `HANDOFF.md` or an active `future-work/` entry). These matter most when pickup is invoked directly (no `/folder-explore` first): they're work that must not be silently stepped on.

For in-flight state, surface a one-line flag pointing to `/folder-explore` — do NOT resume, reconcile, or commit. Pickup orients; it does not act. `/folder-explore` owns resuming.

```
Flags:
- [type]: [one line — what it is, where it lives, why it matters]
- Uncommitted changes: working tree dirty (N files) — `/folder-explore` to resume or `/folder-log` to close out
```

If no flags, omit the section. Don't write "No flags" — that's noise.

## Step 4: Stop

Don't ask "what would you like to work on?" — the user opened this session for a reason and will state it. Asking pads the response and signals you're waiting on instructions that will arrive.

## Escalation paths

When the next prompt arrives, route to the right skill (silently — don't pre-announce):
- Resume in-flight work → `/folder-explore`
- Document the session's work → `/folder-log`
- Full re-orientation (more than the two surfaces) → `/folder-explore` (Full orientation mode)
- Re-document a structurally-changed folder → `/folder-onboarding`

## Edge cases

**README but no CLAUDE.md (or vice versa):** note it in the summary ("README present, no CLAUDE.md") and proceed; suggest a light `/folder-onboarding` pass, don't block.

**No recorded history layer** (and no repo): use README Status for "last touched" (mtimes as a rough fallback); note no layer is recorded (`/folder-onboarding` would choose and record one). Don't repair, init, or seed during a pickup.

**User already stated a task:** skip the pickup — just do the task. Re-reading context they didn't ask for is the over-helpfulness this skill restrains.

## Quality checklist

- [ ] Read only README (Purpose + Status) + CLAUDE.md (DO NOT EDIT + risks/decisions) + `CONTEXT.md` terms if present + the recorded history layer's recent records (or the Status/mtime fallback) — no tree crawl, no file-content reads
- [ ] Output is exactly the six-line template (+ optional Flags) — the `CONTEXT.md` glance adds no line
- [ ] No preamble, no closing question, no emoji
- [ ] In-flight state flagged with a pointer to `/folder-explore` — not resumed, committed, or reconciled
- [ ] Flags section omitted entirely if none ("No flags" is noise)
- [ ] No tree crawling, no re-derivation of structure, no proposed cleanup
- [ ] Both surfaces missing → recommended `/folder-onboarding` and stopped
