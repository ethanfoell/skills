---
name: folder-log
description: Close out a unit of folder work — write the task record to the folder's history layer (a Git commit by default; on a file-based folder, completing the LOG.md stub in place), refresh the README Status snapshot if the task changed it, and propose CLAUDE.md standing-rule updates when the work surfaced a new convention, gotcha, or risk. The folder loop's close-out phase.
disable-model-invocation: true
---

# /folder-log

The fourth, **close-out** phase of the `/folder-explore` → `/folder-plan` → `/folder-build` → `/folder-log` loop. Closes a unit of work by writing the task record to the folder's **history layer** (the choice its CLAUDE.md standing line records — a Git commit by default; on a file-based folder, completing the `LOG.md` stub in place), refreshing the README `Status` snapshot, and proposing CLAUDE.md updates — the gate on each spelled out below. Tasks, not sessions, are the unit of record: each `/folder-log` closes one task with one record, and multiple per session is normal.

## The design

A close-out touches at most three surfaces, each with its own gate:

- **The history-layer record** — the task record, written to whichever layer the folder's CLAUDE.md standing line records: the **commit message** on Git (files touched ride for free in the diff), the **`LOG.md` entry** on a file-based folder — the stub `/folder-build` opened, completed in place. One format (Step 4), two destinations. **Single-source history** — never two records of the same events, so no log file beside Git.
- **The README `Status` section** — the current-state snapshot. Refresh only when the task materially changed what it reports.
- **CLAUDE.md** — the standing rules. Propose an update only when the task surfaced a convention, gotcha, risk, or open decision; the user accepts / edits / skips.

Keep the surfaces complementary, never duplicated: **README** = what's here / current state (and the ordinary *why*) · **CLAUDE.md** = standing rules · **GLOSSARY.md** = the canonical nouns (when present) · **docs/adr/** = a settled hard-to-reverse structural decision's rationale (when earned) · **the history layer** (Git, or `LOG.md`) = the dated history. README `Status` is only ever the snapshot, never the history.

`/folder-plan` is chat-first and writes **no durable stub** — in-flight begins at execution. On a Git-backed folder the **dirty working tree** `/folder-build` leaves *is* the in-flight state `/folder-log` resolves (the same signal `/folder-explore` and `/folder-pickup` flag), and the record is written fresh as the close-out commit. On a file-based folder, `/folder-build` opened an **In-progress stub** at the top of `LOG.md` at execution start — `/folder-log` **completes that stub in place** at close (Step 4); a stub that lingers is the abandonment signal the orientation skills surface.

## When to use

Use when:
- The user says `/folder-log`, "log this", "close this task", "wrap this up", "commit the work".
- A unit of folder work is done (files added / moved / edited / reorganized) and should be recorded.
- The user did a quick standalone fix (no `/folder-explore` first) and wants it committed cleanly.
- A task was cancelled and the decision should be recorded.

**Do NOT use** for:
- **Mid-task checkpoint commits** — those follow the folder's own commit-cadence rule; `/folder-log` is the deliberate close-out, not every save.
- **Excel workbooks** → `/workbook-log`.
- **The file work itself** — reorganizing or building is the task; `/folder-log` records it afterward, it doesn't do it.

## Step 1: Gather context

Read the chat and working tree for the task and extract:

- **Task** — a one-line title (becomes the commit subject).
- **What changed & why** — files or areas added, moved, edited, deleted, and the reason. `git status` / `git diff --stat` show the *what*; the chat shows the *why*.
- **Validation** — any check that the work is sound (links resolve, a build passes, counts tie); pass/fail with the specific thing checked. Omit if none.
- **Deviations** — where the work went off the stated intent, with the reason. Omit if none.
- **Surfaced** — out-of-scope things noticed but **not** done, stated concretely ("file the 2025 exports still loose at the root", not "look into the old exports"). Omit if none.
- **Status** — Complete (default), Cancelled, or Partial. After a `/folder-build`, its summary states `Complete | Partial` directly; `Cancelled` is `/folder-log`'s own determination.

For a standalone quick fix most of these are empty — expected; you'll have just Task plus what changed.

**Privacy — keep everything you write at the structure level.** Do **not** echo file *contents* — names, account numbers, diagnoses, client identifiers, secrets — into the commit message or README Status. Describe what changed ("added the Q3 intake file under `2026/`"), never the sensitive payload. (A folder's standing rules for handling sensitive material live in its CLAUDE.md; this is the line that keeps `/folder-log` itself from leaking.)

## Step 2: Refresh the README Status section (only if materially changed)

The README `Status` section is the current-state snapshot. Update it **only** if this task changed what it reports:

- A new top-level area was added, or an area's role changed.
- The folder's state changed (now in-flight / now clean / now needs review).
- A convention or entry point changed.
- An in-flight item was resolved, or a new one opened.

Date-stamp the section. If none apply, **leave it alone.** Merge, don't clobber — adjust Status, don't rewrite the rest of the README. This edit rides in the close-out commit (Step 4).

## Step 3: Propose CLAUDE.md standing-rule updates (when warranted)

**The default is no proposal.** Most close-outs change nothing in CLAUDE.md — "nothing to propose" is the common, correct outcome, not a step left unfinished. Don't manufacture one. Propose only when the task produced **standing guidance** — something a future session needs that isn't a one-off — **and the convention / gotcha / risk was actually observed or verified this session**, not predicted, theoretical, or environment-documented.

Triggers:
- **A new operating convention emerged** — "regenerate the index with `build.py` after editing any entry."
- **A folder-specific gotcha was discovered** — "the loader reads filenames literally; don't rename the dated files."
- **A risk became active** — "the sync script overwrites silently — commit a checkpoint before running it."
- **An open decision needs to persist** — "revisit the archive cutoff when 2027 files arrive."
- **A DO NOT EDIT or handling policy was established or changed.**

Do **NOT** propose for: one-time events (those live in the commit message), trivia, anything already in CLAUDE.md, human-process docs (those belong in the README), or cautions you didn't actually hit this session / guidance already enforced elsewhere (e.g. a harness-level rule).

**Unverified but plausible? Give it a lighter home.** If something seems worth flagging but you didn't verify it this session, route it to the task handoff or README `Status` as a clearly-unverified note (tag it `[UNVERIFIED]`) — **not** into CLAUDE.md as an asserted standing rule. CLAUDE.md's rules are trusted precisely because they're earned; an untested rule among the dated, verified ones dilutes all of them. It can graduate later, dated and verified, if a session actually hits it.

**How to propose** — surface the exact wording in chat under the target section, and ask:

> Proposing CLAUDE.md update under **[section]**:
> "The sync script overwrites silently — commit a checkpoint before running it."
>
> Accept, edit, or skip?

Accept → write it under that section. Edit → use the user's wording. Skip → don't write; the observation stays in the commit message only. This edit also rides in the close-out commit.

**Refresh `GLOSSARY.md` — only if the work resolved or renamed a term.** Beside the CLAUDE.md proposal, close-out is where the folder's glossary catches up. **The default is no change** — the same restraint as above. But if the work *resolved* a domain term (sharpened a fuzzy word, retired a synonym, settled which of two names is canonical), or a `/folder-plan` / `/folder-build` cycle **queued a coined term** for recording, refresh `GLOSSARY.md` by running `/domain-modeling` (it owns the glossary format and lazy-creation). A term merely *used*, not resolved, earns no edit. The refresh rides this close-out commit (Step 4).

**Offer a structural ADR — only a settled, hard-to-reverse layout decision that clears all three prongs.** **The default is no offer** — the same restraint as above; almost nothing qualifies. Offer only when this session **settled** a decision about the folder's *structure* (a layout split, a boundary, a deliberate deviation from the obvious organization) that clears `/domain-modeling`'s three prongs — **hard to reverse · surprising without context · the result of a real trade-off** — then record it by running `/domain-modeling`, which owns the ADR format, numbering, and placement (the worked-on folder's **own** `docs/adr/`). This is the **either/or** with the open-decision trigger above: an *unsettled* question stays a CLAUDE.md Open-decision; a *settled* gate-clearing structural decision becomes an ADR whose rationale lives in `docs/adr/` **only** — never copied into CLAUDE.md. If it's the folder's **first** ADR, also ensure CLAUDE.md carries the one-line **`docs/adr` read-habit** `/folder-onboarding` establishes, so the ADR is read, not left write-only. The ADR (and any read-habit line) rides this close-out commit (Step 4).

## Step 4: Write the record to the history layer — the record closes the task

Dispatch on the folder's **recorded choice** — the history-layer standing line in its CLAUDE.md; don't probe for Git:

- **Git (the default):** stage the outstanding work plus any README / CLAUDE.md / `GLOSSARY.md` / `docs/adr/` edits from Steps 2–3, and make **one close-out commit**. The commit message *is* the task record.
- **File-based (`LOG.md`):** **complete the stub in place.** `/folder-build` opened this task's entry at the top of `LOG.md` with an **In progress** marker; replace that marker with the record body below (sharpening the title if the task's shape changed) — **never append a second entry for the same task**. Heading `## YYYY-MM-DD — <task title>`; one entry per closed task, newest first. Two edge cases: **no stub at the top** (ad-hoc work that skipped `/folder-build`) — write the entry fresh at the top and note in your report that the task ran unsignalled; **the top stub belongs to a *different*, abandoned task** — surface it and ask, don't silently overwrite another task's in-flight record. The doc edits from Steps 2–3 need no further recording — the entry's what/why names them.

**On Git, attempt then branch on the exit code — don't pre-gate.** A forward commit lands even while the Cowork mount warns about `unlink`:

- **Commit succeeds** (exit 0) → recorded. If it emitted `unable to unlink … Operation not permitted` warnings, Git couldn't clear its own lock file — the **file-delete permission** isn't granted. The commit still landed, but a stranded `.git/*.lock` can jam the *next* git write, so grant the permission (once per session) and remove the stale lock.
- **Commit fails** (non-zero exit) → check why. `Operation not permitted` on `unlink` is that ungranted permission — grant it and retry; the commit then lands. Only a **genuinely repo-less** folder takes the no-usable-Git edge case below (the record goes to `LOG.md`, never README `Status`) — don't route a fixable permission failure onto the file-based layer.

**Format — adaptive, destination-independent** (the commit message and the `LOG.md` entry body are the same record):
- **Subject / entry title** — the one-line Task title, imperative and concise.
- **Body** — present **only when warranted**: the what/why, plus any of Validation / Deviations / Surfaced that are non-empty. A trivial fix is subject-only (a heading-only `LOG.md` entry); a substantive task gets a short structured body. **Omit empty fields** — never write "Validation: none."
- **Issue-traced task** — when the task traces to an issue, the record names the issue and checks Done against its **acceptance criteria** — each criterion stated met or not, in the body (commit message and `LOG.md` entry alike; the criteria seeded the plan's Validation, so the close-out closes against the issue, not only the plan). A task with no issue gets no extra line.

Record the *outcome*, not the process: leave out intermediate debugging, trivial formatting tweaks, attempts immediately undone, tool plumbing, and AI deliberation ("considered X then chose Y" — record the decision, not the path to it).

Substantive example:

```
File the June exports under 2026/06 and refresh the combined CSV

What/why: filed the 12 loose June exports into 2026/06/ and updated the
README Layout to list it — month-end close filing.
Validation: consolidate_exports.py emits combined_2026-06.csv clean;
counts tie (12 in / 12 filed / 0 lost).
Surfaced: the 2025 exports are still loose at the root — queued, not
filed this cycle.
```

Trivial example:

```
Fix broken relative link in README Layout section
```

**Record discipline:**
- **One record per task.** Multiple tasks = multiple commits / entries; don't bundle unrelated work.
- **Respect the target folder's own commit-cadence rule** if its CLAUDE.md states one; otherwise propose the close-out record and make it.
- **Before a destructive step** (deleting or overwriting), confirm — and capture the prior state first so it's recoverable: a checkpoint commit on Git; a dated copy into `_archive/` on a file-based folder (the recoverability floor either way).

## Step 5: Verify and report

1. On Git: confirm the commit landed (`git log -1`) and the working tree is clean (`git status`) — unless work was intentionally left uncommitted, in which case say so. On a file-based folder: confirm the completed entry sits at the top of `LOG.md`, correctly dated, with no **In progress** marker left behind (no commit to verify).
2. Tell the user briefly: the task title, the record's subject line, and whether README Status or CLAUDE.md were touched.
3. If anything was intentionally **not** recorded (trivial debugging, abandoned attempts), note it in one line.

## Cancelled and no-change tasks

The history layer records what happened, so `/folder-log` does **not** force an empty record just to mark a task closed:

- **Cancelled, but it left changes worth keeping** → record them with the reason: subject `Cancelled: <short reason>`, body explaining what was kept and why the task stopped (a commit, or a `LOG.md` entry, per the recorded layer).
- **Cancelled, nothing changed** → nothing for the history layer to record. Report it; and **only if it matters for continuity** (don't-retry-without-X), put a one-line note in README Status or propose a CLAUDE.md open-decision. No empty commit, no empty entry.
- **Cancelled, changes discarded** → the user discards (`git restore` / `git clean` on Git; restoring the `_archive/` copy on a file-based folder); `/folder-log` notes the cancellation in its report. No record.

One file-based exception: a cancelled task that **opened a stub** never leaves it dangling — complete the stub in place as the cancellation record (`Cancelled: <short reason>`; heading-only is fine). Execution started, so the stub already exists; an open stub with no task behind it would read as abandoned work forever.

## Edge cases

**No usable Git and no standing line** (never onboarded, or Git declined without the choice being recorded): no commit to make — write the record as a **`LOG.md` entry** anyway, never into README `Status` (Status is the snapshot, not the history), and flag that `/folder-onboarding` Step 6 should record the folder's history-layer choice properly. If the folder *should* be under Git but `git init` / commit warned `Operation not permitted`, that's the ungranted file-delete permission — grant it once per session; don't route a folder that just needs the permission onto the file-based layer.

**Correcting a previously recorded task:** history is append-only — don't rewrite the prior record. Make a **new** commit stating the correction ("Correct the path recorded in `<short-sha>`"); on a file-based folder, a new `LOG.md` entry stating it — never edit the old entry.

**A parked artifact the task completed — a handoff, or an integrated inbox item:** archive it as part of the close-out (don't delete) and note it in the commit body ("handoff cleared", or "archived `<item>` (merged)" for an integrated `proposed-change`). **Archive by moving into `_archive/`** — `git mv` under Git, a plain rename otherwise — a `rename`, never a `delete`, because delete is what sandboxed/synced environments block. This is the close half of the inbox convention: a proposed-change is integrated, a human approves (the `/folder-log` invocation is that gate), then it moves to `_archive/` and is **merged**. Only archive an item actually integrated or decided — leave open items in the inbox.

**Multiple tasks, one `/folder-log`:** default to one record per task. If asked to bundle, warn that it loses the per-task granularity the loop is built on, and bundle only if the user insists.

**Work already committed mid-task:** the close-out commit covers what's left — the README Status / CLAUDE.md edits and final touches. If literally nothing is outstanding, skip the commit, refresh Status, and report.

## Quality checklist

- [ ] Record written to the layer the folder's standing line records — a commit on Git, a top-of-file `LOG.md` entry on files — never both, and never README `Status` as the record
- [ ] On a file-based folder: the stub `/folder-build` opened was completed **in place** — never a second entry for the same task; a missing stub written fresh and noted, a foreign stub surfaced and asked about (Step 4)
- [ ] Record subject is a one-line task title; body present only when warranted, empty fields omitted
- [ ] Issue-traced task: record names the issue and checks Done against its acceptance criteria (no issue → nothing extra)
- [ ] The record and README Status describe **structure, not sensitive file contents**
- [ ] README Status refreshed only if the task materially changed it; date-stamped; rest of the README untouched
- [ ] CLAUDE.md proposal made only if it clears the verified bar (observed this session, not predicted/theoretical/enforced-elsewhere); proposing nothing is expected — exact wording + accept/edit/skip when one is made
- [ ] `GLOSSARY.md` refreshed via `/domain-modeling` only if the work resolved or renamed a term (or plan/build queued one); default is no change
- [ ] Structural ADR offered via `/domain-modeling` only for a settled, hard-to-reverse, three-prong-clearing **structural** decision (default no offer); its rationale in `docs/adr/` only, not duplicated into CLAUDE.md; first-ADR read-habit line ensured
- [ ] No duplication across README (what's here) / CLAUDE.md (rules) / GLOSSARY.md (canonical nouns) / docs/adr (settled structural rationale) / the history layer (this task)
- [ ] Every durable workbook the task created or materially edited carries its own Audit Log entry for the in-file changes (`/folder-build`'s obligation — flag a gap, the workbook-grain record beside this folder-grain one)
- [ ] One record per task; the close-out record covers the work plus any doc edits
- [ ] Cancelled task handled per the no-empty-record rule; corrections are new records, not history rewrites
- [ ] On Git: commit attempted and branched on exit code (not pre-gated); an `Operation not permitted` failure fixed by granting file-delete + retry — a genuinely repo-less folder's record routed to `LOG.md`, not README Status
- [ ] Parked artifact (handoff, or integrated inbox `proposed-change`) archived by **move** into `_archive/` — rename, never delete — and noted in the record body
- [ ] Verified: working tree clean + `git log -1` on Git (or intentional leftovers called out); completed entry at the top of `LOG.md`, no **In progress** marker left, on a file-based folder
