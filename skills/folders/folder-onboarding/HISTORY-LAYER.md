# History layer — the folder's record of its own past

Canonical definition of the folder loop's **history layer**: the four obligations every
implementation must meet, the implementation menu, the named-reason gate, and the CLAUDE.md
standing-line templates. **Canonical home: this file in `folder-onboarding/`** — the skill that
chooses and records the layer (Step 6). The other loop phases (`/folder-log`, `/folder-explore`,
`/folder-pickup`) carry one-line dispatch text and defer to this spec — no sibling copies.

The layer is a **contract, not a tool**: chosen once at onboarding, recorded as a CLAUDE.md
standing line, and read — never re-probed — by every later loop phase. Which layer a folder uses
is a decision with a named reason, not a runtime detection.

## The four obligations

Every implementation MUST meet all four, each at its stated floor:

1. **Dated record** — one dated entry per closed task. Floor: the entry exists and is dated;
   tasks, not sessions, are the unit.
2. **What-changed answerability** — the record says what changed and why. Floor: prose-level —
   a returning session can answer "what happened here?" from the records alone. Line-level
   diffs are **above** the floor: Git-only, never promised by the contract.
3. **Explicit in-flight signal** — a returning session can detect open work without being told.
   Floor: the signal is explicit and detectable (`git status` on Git; the open `LOG.md` stub on
   the file-based layer).
4. **Recoverability** — prior state is captured before a destructive operation. Floor: a dated
   copy into `_archive/` first. Git's checkpoint commit is the stronger form of the same
   obligation.

## The implementation menu

**Git — the default.** Exceeds every floor: commits are the dated record, diffs answer
what-changed down to the line, `git status` is the in-flight signal, and a checkpoint commit is
recoverability. Choose it unless a named reason below applies.

**File-based — `LOG.md` at the folder root.** For folders where Git is wrong or its operators
won't use it. Newest entry first; **one entry per closed task** (never per session, never per
save), under a `## YYYY-MM-DD — <task title>` heading. `/folder-log` owns the entry format and
writes the entries — the same adaptive task record it writes as a commit message on Git. The
explicit in-flight signal is an **open stub**: `/folder-build`'s first act at execution start is
writing the task's entry header at the top of `LOG.md` with an **In progress** status marker, and
`/folder-log` completes that stub **in place** at close — never a second entry for the same task.
This is the one exception to one-entry-per-closed-task: the top entry may be the open stub of the
task in flight, and a stub that lingers is the abandonment signal the orientation skills surface.
Recoverability is the `_archive/` dated-copy floor.

## The named-reason gate

Git is the default; the file-based layer is chosen only **for a named reason**, recorded in the
standing line:

- **Binary-heavy folder** — the content doesn't diff, so Git's above-floor strengths are dead
  weight.
- **Shared / synced drive** — Git and sync engines fight over `.git/`.
- **Non-Git operators** — the folder's day-to-day users won't read `git log` or run Git.

No named reason → Git. An ordinary folder never drifts onto the weaker layer by reflex.

## The CLAUDE.md standing line

Record the choice where every later session reads it. Templates (adapt the wording, keep the
parts):

Git:

> History layer: **Git**. One close-out commit per task (`/folder-log`); checkpoint before any
> destructive operation. Single-source history — no separate log file.

File-based:

> History layer: **`LOG.md`** (file-based — <named reason>). One dated entry per closed task,
> newest first (`/folder-log`); dated copy into `_archive/` before any destructive operation.
> Single-source history — Git deliberately not used here.

## Single-source history

One history layer per folder — **never two records of the same events**; parallel records drift,
and each casts doubt on the other. On a Git-backed folder that means **no separate log file** (it
would duplicate the commits). On a file-based folder, `LOG.md` *is* the layer — not a duplicate
of anything. And on every folder, the README `Status` section is **only the current-state
snapshot, never the history** — Status accumulating history is how a second, driftable record is
born.
