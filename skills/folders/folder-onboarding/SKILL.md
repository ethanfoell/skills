---
name: folder-onboarding
description: Open a folder for the first time and make it understandable — lay down a README (for humans) and CLAUDE.md (for agents), choose and record the folder's history layer (Git by default), and surface findings. The folder loop's first-visit mode.
disable-model-invocation: true
---

# /folder-onboarding

Open a folder for the first time and make it understandable — to humans and agents — so any later session orients instead of re-deriving structure. The first-visit counterpart to `/folder-pickup`, and the Onboard route `/folder-explore` names.

## The design

Markdown files are cheap to open but expensive to clutter, so onboarding lays down a small set of **earned** surfaces — a human surface, an agent surface, a history layer, and — only when earned — a glossary:

- **`README.md`** — the human-facing orientation doc: what this folder is, how it's organized, how to use it, current status.
- **`CLAUDE.md`** — the terse standing rulebook an agent follows here: conventions, guardrails, gotchas. (It auto-loads into agent context, which is why standing rules live here, not the README.)
- **The history layer** — the folder's dated record of its own past: a contract with four obligations (dated record, what-changed answerability, in-flight signal, recoverability), chosen once in Step 6 — **Git by default**, `LOG.md` for a named reason — and recorded as a CLAUDE.md standing line every later phase reads. **Single-source history: one layer per folder, never two records of the same events.** Full spec: [HISTORY-LAYER.md](./HISTORY-LAYER.md).
- **`GLOSSARY.md`** *(lazy — only when earned)* — the folder's glossary: the canonical noun for each folder-specific concept the docs and skills reuse. Seeded by composing `/domain-modeling` (Step 5), and only when a real domain term surfaces during onboarding. A self-evident-names folder earns none, and that absence is never a gap to flag.
- **`docs/adr/`** *(lazy — only when earned)* — the home for a **settled, hard-to-reverse structural** decision's rationale (why the layout deliberately deviates from the obvious). Offered by composing `/domain-modeling` (Step 5) only when a layout choice clears the three-prong gate; the ordinary *why* stays the README why-aside. Most folders earn none.

Two further surfaces are **opt-in, never default**, added only when a folder earns them: an inbox/staging convention for cross-session proposed work (Step 7) and a living HTML overview for a complex folder (Step 8).

### Where a multi-session effort's pipeline artifacts live

Some work outgrows one session — a multi-session effort with a spec and independent tickets, shaped up the **stairs** (`/grill-with-docs → /to-spec → /to-tickets`; `/folder-plan` names the door). This section is the folder loop's standing record of where those artifacts live, so every session finds one convention. They land at the **effort's folder root** — the folder playing the role a code repo's `.scratch/<feature-slug>/` plays — in exactly the form the pipeline skills already write, so `/to-spec`, `/to-tickets`, and `/wayfinder` run over a folder unmodified:

- **Tickets** — one file per ticket in an `issues/` subfolder: `issues/<NN>-<slug>.md`, numbered from `01` in dependency order (blockers first), each file carrying its own "Blocked by" and Status lines — `/to-tickets`' local-files form verbatim, never a single combined file. The subfolder keeps `/to-tickets`' own name deliberately: a future upstream change to the layout flows through that skill, not through this record.
- **The spec** — `/to-spec`'s output `.md`, beside the `issues/` subfolder.
- **A wayfinder map** — when an effort is too big *and* foggy to spec directly, `/wayfinder`'s local-markdown fallback is the folder-side map, its files at the same root. The folder side needs no map machinery of its own.

`/folder-onboarding` never creates any of these — the pipeline skills write them when an effort earns them. A record to read, not a scaffolding step.

## When to use

Use when opening a folder you'll work in again and want it understandable — or someone hands you a directory and says "figure out what's in here." Skip it for:
- A folder you'll touch once → just look at it; don't lay down scaffolding.
- An already-onboarded folder (has README + CLAUDE.md) → `/folder-pickup` or `/folder-explore`.
- Excel workbooks → `/workbook-onboarding`.
- Reorganizing or moving files → this documents structure; it doesn't change it.

## Prerequisites

- You'll **choose and record the history layer** in Step 6 — Git by default; if the folder isn't a repo, you'll offer to init.
- If a `README.md` or `CLAUDE.md` already exists, you're **updating, not creating** — read it first, treat it as the owner's source of truth (the merge rule in Steps 4–5).

## Step 1: Read the folder structure

Walk the tree and build a mental model. Use `ls`/`find`/`tree` for shape, read the entry-point files (existing `README`, `CLAUDE.md`, `AGENTS.md`, top-level docs), and **sample** representative files in each area — don't read every file in a large folder. For each top-level area, capture: its **purpose** (source / working / output / archive / docs / config); the **organizing scheme** (how things are named and filed); the **entry points**; **source-of-truth vs generated** (editing a generated file is a trap); **cross-references** that depend on paths staying put; **stable vs volatile**; **existing conventions** (archiving, versioning, naming); and **smells** (stale, duplicated, misfiled, orphaned).

Done when: you can explain what every top-level area is for, how things are organized, and what someone would create or change in normal use.

## Step 2: Map the structure

Synthesize into a model you could explain in two minutes:

1. **Purpose** — what this folder is, in a sentence or two.
2. **Organizing principle** — the one rule that explains the layout ("one folder per plugin"; "by case then date"; "source / working / output / archive").
3. **Nerve centers** — the few files or dirs that matter most: source-of-truth locations, entry-point docs, the thing everything depends on.
4. **Conventions in force** — naming, filing, archiving, versioning.
5. **Generated vs authored** — what's safe to edit vs regenerated.
6. **Structural risks** — what breaks on a rename/move; brittle relative paths; areas with no archive or version-control safety net.

## Step 3: Surface findings — before writing anything

Tell the user what you found and confirm it before laying down surfaces. Prioritize: structure/conventions that need confirmation (the inferred organizing principle, what's canonical); stale/duplicated/misfiled material; **"do not touch" areas** (generated dirs, source-of-truth files) → propose a **DO NOT EDIT** policy; missing safety nets (no archive, not under Git, no entry-point doc). Ask:
- Are there areas that should **not** be modified?
- Context invisible from the structure — **why** it's organized this way, the outcome it serves, who else uses it?
- The intended workflow and cadence?
- Which history layer fits — Git (the default), or is there a named reason for the file-based `LOG.md` (binary-heavy, synced drive, non-Git operators)? (Step 6)

Done when: the user has confirmed or corrected your model, and any edit restrictions are established.

## Step 4: Write (or update) the README — the human surface

`README.md` lets any colleague open the folder cold and understand it.

**Merge rule — don't clobber.** If a README exists, read it, treat the owner's content as canonical, and propose **additions and corrections** — show a diff or summary before saving. Only write fresh when none exists.

**Required sections** (adapt; trim hard for simple folders):

- **A. Purpose & Overview** (2–3 sentences) — what this folder is, who it's for, how it's used, **and why it exists** — the reason-for-being / outcome it serves, when the user gave it in Step 3. (Capturing the *why*, not just the *what*, gives a later session the standard to judge what to do next.)
- **B. Layout / Inventory** — one line per top-level area: name, role, and whether it's **authored** (edit freely), **canonical** (source of truth — change with care), or **generated** (don't hand-edit). Every area, even utility ones.
- **C. How it's organized** — the organizing principle and the filing conventions (naming, archiving, versioning): the rules to file something new in the right place.
- **D. How to use it** — the routine workflow for common tasks, in sequence ("To do X: 1… 2… 3…").
- **E. Status** — the current-state snapshot: what's live, in flight, needs attention, and the date. The one section expected to change often; keep it near the top and date-stamp it.
- **F. Known issues & limitations** *(optional)* — user-facing limitations and workarounds. Agent-editing traps go in CLAUDE.md's Gotchas, not here. Omit if nothing user-facing.

**Tone — human-neutral.** Write for a colleague; be specific (name folders, describe conventions). **No references to AI, automation, Claude, or "this tool"** — the README is a human document. (Agent-directed language belongs in CLAUDE.md.)

Done when: a colleague who's never seen the folder could read the README and know what it is, how it's organized, how to use it, and its current state.

## Step 5: Write (or update) the CLAUDE.md — the agent surface

`CLAUDE.md` is the terse standing rulebook for an agent working here — the operating contract that keeps a session from breaking something. Keep it **complementary** to the README, never duplicated: a fact about *what's here* belongs in the README; a *rule for working here* belongs in CLAUDE.md. **Same merge rule** — if one exists, respect it as canonical and propose changes.

**Suggested sections:** **Operating conventions** (the standing rules — "edit the source in `skills/`, never the generated `dist/`"); **Gotchas** (easy-to-miss facts that cause silent breakage); **Filing & version-control discipline** (archive don't delete, park unfinished work, commit cadence — Step 6); **Active risks** *(optional)*; **Open decisions / pending items** *(optional)*.

**The confidence line — seed only what's earned.** Seed CLAUDE.md only with facts **verifiable from the folder** or **confirmed by the user** in Step 3 (conventions, gotchas, the filing/Git discipline, any DO NOT EDIT policy). **Leave for `/folder-log`** what's earned through working here — Active risks and Open decisions. Don't infer them from a cold first read, and **don't stub empty sections**: markdown has no fixed schema to keep stable, so an absent section is fine.

**Voice — agent-directed is correct here** (second-person, terse standing rules — "don't edit the installed cache"). The narrative belongs in the README or a `docs/` guide.

**Keep the surfaces honest.** Add one CLAUDE.md rule plus a **last-verified date**: when a convention, tool, or the structure changes, update `README.md` and `CLAUDE.md` in the same task — docs that contradict the folder are worse than none, because agents trust them over what they observe.

**Seed `GLOSSARY.md` — the glossary, only if a real term surfaced.** A further complementary surface holds the folder's *canonical nouns* — the term the docs and skills should use for each folder-specific concept (an area's role, a file-kind, a coined name). If a real domain term surfaced in Steps 1–3 — a noun whose meaning isn't self-evident and that the folder's material will reuse — **seed `GLOSSARY.md` by running `/domain-modeling`**, which owns the glossary format and the lazy-creation rules. Lazy is the default: a folder whose names already explain themselves earns **no** `GLOSSARY.md`, and that absence is never a gap to flag. The split, stated once for the whole loop: a **noun** → `GLOSSARY.md` · a **rule** → `CLAUDE.md` · **what's here** (and an ordinary *why*) → `README` · a **settled hard-to-reverse structural decision's rationale** → `docs/adr/`.

**Offer a structural ADR — only when a settled layout rationale clears the gate.** If the owner explained in Steps 1–3 *why* the layout deliberately deviates from the obvious — a hard-to-reverse structural choice made for a real trade-off — that rationale can earn an ADR. **Default: no offer** — almost nothing qualifies, and the plain *why* already has a home in the README (Section A). Offer **in addition to** the README why-aside when the decision clears `/domain-modeling`'s three prongs — **hard to reverse · surprising without context · the result of a real trade-off** — and record it by running `/domain-modeling`, which owns the ADR format, numbering, and placement (the folder's **own** `docs/adr/`). The README keeps the one-line *why*; the ADR holds the full rationale and the rejected alternatives — complementary, not duplicated. When a folder earns its **first** ADR, also seed one CLAUDE.md standing line — the **`docs/adr` read-habit**: _"Structural decisions are recorded in `docs/adr/` — read the ones touching your area before changing the layout."_ — the folder's port of "read the ADRs in the area you touch", so the ADR is read, never write-only.

Done when: an agent could read CLAUDE.md and know the rules for working here safely, with risks/decisions either seeded from confirmed facts or left for `/folder-log` — and, if a real term surfaced, the folder's canonical vocabulary seeded into `GLOSSARY.md` via `/domain-modeling` (else none, lazily), plus a settled structural rationale recorded as an ADR only if one cleared the three-prong gate.

## Step 6: Choose and record the history layer

The history layer is the folder's dated record of its own past — a contract with four obligations, each at an explicit floor: a **dated record**, **what-changed answerability**, an **explicit in-flight signal**, and **recoverability**. The obligations with their floors, the implementation menu, the named-reason gate, and the standing-line templates live in [HISTORY-LAYER.md](./HISTORY-LAYER.md) — read it for this step.

**Choose once, here; record the choice as a CLAUDE.md standing line** (templates in the reference file). The later phases (`/folder-log`, `/folder-explore`, `/folder-pickup`) read the recorded choice and dispatch — they never re-probe. **Git is the default**; the file-based `LOG.md` takes a **named reason** (binary-heavy folder, shared/synced drive, non-Git operators), recorded in the standing line — a deliberate choice, never a reflex. Whichever is chosen, history is **single-source**: on Git, no separate log file (it would duplicate the commits); on files, `LOG.md` *is* the layer. The README `Status` section is always and only the current-state snapshot, never the history.

**Git path (the default):**

- **Git works on Cowork mounts — `unlink` (delete) is just gated behind a permission.** The sandbox blocks file *deletion* until the user grants the file-delete permission, and Git needs delete to clear its own lock/temp files. So a `git init`/commit that warns `unable to unlink … Operation not permitted` is almost always that **ungranted permission** — grant it once per session and retry; Git then operates normally. **Don't pre-gate Git behind a delete-probe** — attempt it, and treat the unlink warning as grant-and-retry, not a reason to route onto the file-based layer.
- **Not a repo:** offer to `git init` and make an initial commit ("Onboard folder: add README + CLAUDE.md"). Confirm first.
- **Already a repo:** make the onboarding commit and record the standing line + commit-cadence rule in CLAUDE.md (typically: commit a checkpoint at each meaningful milestone and before any destructive operation, with a descriptive message).
- **Multi-agent resilience — only when concurrent agents are expected:** add one terse CLAUDE.md line — concurrent commits can collide on Git's lock file, so retry rather than force-removing the lock, and recover a desynced index with `git reset` (mixed), never `--hard`. A seed, not a procedure; skip it for solo-use folders.

**File-based path (named reason only):**

- Seed **`LOG.md` at the folder root** — newest entry first, one dated entry per **closed** task; `/folder-log` owns the entry format and writes the entries. Seed it with its first entry recording the onboarding.
- Record the standing line **naming the reason** Git was passed over.
- The explicit in-flight signal is the **open `LOG.md` stub** — written by `/folder-build` at execution start, completed in place by `/folder-log` at close (mechanism in [HISTORY-LAYER.md](./HISTORY-LAYER.md)). Nothing to seed here; a live folder's top `LOG.md` entry may legitimately be the open stub of a task in flight.

**Either path — staleness signal:** for a key living document inside the folder (a generated overview, a spec), a version-stamped filename or in-file version constant is the at-a-glance "is this current?" signal. Point it out where one exists; don't impose it everywhere.

Done when: the history layer is chosen, its standing line is in CLAUDE.md, and the onboarding work is recorded in it — the onboarding commit on Git (plus the resilience seed if concurrent agents are expected), or the seeded `LOG.md` with its named reason on the file-based layer.

## Step 7: Offer the inbox / staging convention — only if the folder will accumulate cross-session proposed work

Some folders collect proposed changes and parked work one session drops and a later one integrates — a cross-session *propose → integrate → close* layer. When a folder will work that way (a plugin or project workspace touched by multiple sessions, not a static store), offer to seed a lightweight **inbox**. Like the HTML overview, this is **opt-in, not default** — skip it for a folder that won't accumulate such work. When accepted, lay down three things:

- **A README `Inbox` section** — names the inbox area (default `future-work/`; the owner can rename — keep the skills name-agnostic, detect by the header), the item header, and the readiness ladder. Items group into sub-folders by **target** (the stable axis) and are tagged by **rung** (the volatile axis — never folders). The four rungs: **idea** (raw thought; promote it) → **task** (a queued prompt; run it, output re-enters one rung up) → **proposed-change** (decided, ready to integrate) → **merged** (integrated, moved to `_archive/`; terminal). Lower rungs are *promoted*; only a proposed-change is *integrated*; a human approves before anything is *merged*. **Write each item to its rung:** idea/task **open** — pose the question, point at the files, share observations as leads to verify, not verdicts; proposed-change **prescriptive** — what changes and why, ready to integrate. (The stance keeps a parked item from handing the next session a conclusion to inherit.)
- **A CLAUDE.md standing line** — the inbox is surfaced by rung at orientation (`/folder-explore`); proposed-changes are integrated then archived on close (`/folder-log`); the close is an archive-**move** (rename into `_archive/`), never a delete.
- **A copyable item header** — a `_TEMPLATE.md` in the inbox area:

  ```
  **Target:** <which plugin/area this lands in — becomes the sub-folder>
  **Rung:** idea | task | proposed-change | merged
  **Type:** <optional — disambiguates within a rung, e.g. "finding" vs a ready change>
  **Opened:** <YYYY-MM-DD>
  **Status:** open | in-progress | done
  ```

**The `/triage` mapping — recorded in the same README `Inbox` section.** The inbox is the folder's triage surface: `/triage` runs over it unmodified, and its intake expects the folder to have recorded how its canonical roles map here — this section is that record. Scaffold the mapping alongside the ladder:

- **Rungs are the states** — no second status vocabulary. `needs-triage` → **idea**; `ready-for-agent` → **task or proposed-change** (the ladder is finer than triage on the ready side — the grill picks the rung); `wontfix` → archive-move into `_archive/` plus, for a rejected enhancement, a concept file in `_out-of-scope/`. `needs-info` and `ready-for-human` are **vestigial-but-mapped** on this solo substrate: open questions already live in the item body per the write-open stance, and every path already ends at a human gate. The category roles (`bug`/`enhancement`) ride the optional `Type:` header.
- **The item file is the thread.** Triage notes and agent briefs (the structure in `/triage`'s `AGENT-BRIEF.md`, disclaimer line included) append into the item body — one artifact per item, no sidecars, no `LOG.md` bleed. Briefs stay compatible with the write-open stance: they specify question, constraints, and acceptance criteria, not verdicts. Items are append-accumulating dossiers — deliberate; that's what the eventual build session wants loaded.
- **Rejection memory lives at `future-work/_out-of-scope/`** (inside the inbox area, whatever name it carries) — `/triage`'s concept-file knowledge base (its `OUT-OF-SCOPE.md` owns the format and the write rules), made **Finder-visible**: the substrate is human-browsed, and a dot-prefix would hide the record exactly where the human looks. It sits beside the `_archive/` its closed items move to; the wontfix flow mirrors the tracker's — the item archive-moves, the concept file is created or appended.

Keep the split honest: *how the inbox works* goes in the README; the *standing rule* in CLAUDE.md. The archive-move close is deliberate — `rename` works in sandboxed/synced environments where `delete` fails, so archiving keeps the close robust there.

## Step 8: Offer the living HTML overview — only if complexity earns it

A self-contained, version-stamped HTML page that visualizes a **complex** folder (structure, relationships, pipeline) is genuinely useful — but an **optional** add-on, not a default deliverable. Most folders are fully served by README + CLAUDE.md + Git. Offer it only when there are enough interrelated moving parts that a visual map beats prose (many components with dependencies, a build pipeline, a large cross-referenced corpus). When accepted, build it self-contained (opens offline, no external dependencies) and version-stamped (a `DOC_VERSION` constant + a version-log comment). Don't build it speculatively — a simple folder with an HTML map it didn't need is exactly the over-engineering this design avoids.

## Step 9: Report

Summarize: **what was laid down** (README / CLAUDE.md created or updated, the history layer chosen and recorded — the onboarding commit, or the seeded `LOG.md` with its named reason — note merges vs fresh writes; a `GLOSSARY.md` or `docs/adr/` entry if one was earned, plus the `docs/adr` read-habit line in CLAUDE.md on a first ADR); **top 3–5 findings** ranked by importance (risks, stale/duplicated material, structural issues, DO NOT EDIT areas); **suggested next steps** ("next session, `/folder-pickup` to re-orient fast"; an HTML overview if the folder's complex; specific cleanup if smells were found).

## Adapting to complexity

- **Simple folder** (a few files, one obvious purpose): a short README (Purpose, Layout, Status) may be all it needs; CLAUDE.md minimal or skipped; Git stays the default layer and is cheap here. Don't manufacture sections.
- **Complex folder** (many areas, conventions, generated outputs, cross-references): full README sections, a real CLAUDE.md, the history layer recorded, and possibly the Step 7 inbox / Step 8 HTML overview.

## What this skill does NOT do

- Move, rename, reorganize, or delete files — it documents structure.
- Overwrite an existing README or CLAUDE.md — it merges and proposes (Steps 4–5).
- Keep two history records — single-source history: one layer per folder; on a Git-backed folder that means no separate log file.
- Seed the inbox or build the HTML overview by default — both are opt-in, gated offers (Steps 7–8).

## Quality checklist

- [ ] Every top-level area is named in the README Layout, marked authored / canonical / generated
- [ ] README has a dated Status section and captures the folder's why (not just its what) when the user gave it
- [ ] README is human-neutral — no AI/automation/Claude language
- [ ] CLAUDE.md holds standing rules + gotchas + filing/Git discipline; risks/decisions seeded only from confirmed facts, else omitted; a keep-current rule + last-verified date
- [ ] No content duplicated between README (what's here + ordinary why), CLAUDE.md (rules), GLOSSARY.md (canonical nouns), and docs/adr (settled structural rationale)
- [ ] `GLOSSARY.md` seeded via `/domain-modeling` only if a real domain term surfaced; a self-evident folder earns none and its absence isn't flagged
- [ ] Structural ADR offered via `/domain-modeling` only when a settled layout rationale clears the three-prong gate (default no offer); README keeps the plain *why*, the ADR the full rationale; first-ADR `docs/adr` read-habit line seeded in CLAUDE.md
- [ ] An existing README/CLAUDE.md was merged, not clobbered (diff shown first)
- [ ] Git attempted directly (no pre-gating probe); an `unlink` / `Operation not permitted` warning treated as grant-the-permission-and-retry, not a reason to route onto the file-based layer
- [ ] History layer chosen and recorded as a CLAUDE.md standing line — Git by default with the onboarding commit + commit-cadence rule (+ the resilience seed if concurrent agents expected), or `LOG.md` seeded with a named reason
- [ ] Inbox seeded only if the folder will accumulate cross-session work — README section (with the `/triage` role mapping) + CLAUDE.md line + name-agnostic `_TEMPLATE.md`
- [ ] Single-source history — one layer, never two records of the same events; README Status kept snapshot-only; HTML overview offered only if complexity warranted it
- [ ] DO NOT EDIT policy recorded in CLAUDE.md if the user established one
