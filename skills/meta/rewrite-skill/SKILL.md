---
name: rewrite-skill
description: "Rewrite one skill under writing-for-agents: gather its facts, grill the per-skill decisions, find its one rule, then ship the PR in this repo's shape."
argument-hint: "Which skill?"
disable-model-invocation: true
---

Rewrite one shipping skill of this repo, end to end, in one attended session. A rewrite reproduces three things, all required: the mechanical writing-for-agents pass, the grill where the user speaks for themselves, and the **reframe**, the skill's one rule and the leading word that carries it. The pass alone leaves a shorter skill that still reads badly.

## 1. Facts

Fill the skill's **facts block** (below) from the tree. A block cut into a ticket earlier is checked line by line against the tree now, since the tree moves. Done when every line of the block is current and the kind is named.

## 2. Grill

Call the Skill tool with "grilling". Open on the frontier already pre-answered from the facts and the standing rules; two questions are always the user's and stay open: what's bothering them about this skill, and the invocation call. Round two carries the proposed reframe for their yes: the one rule the sections keep restating, named, with its leading word. A skill with no such rule (the reference skills) says so and relaxes to cut-and-structure. The user answers their own two questions; the agent never fills them in. Done when the user has answered both and the reframe has their yes, or has been replaced by theirs.

## 3. Rewrite

Call the Skill tool with "writing-for-agents" and run the mechanical pass over `SKILL.md` and every sibling: ladder sort (steps, then in-file reference, then disclosed reference), the branching test (inline what every run needs, disclose what some runs reach), no-ops and duplication hunted, rules stated positively. Then write the reframe in: the rule stated once where its sections used to restate it, the leading word repeated as a token. The standing rules below govern. Done when the skill states its rule once, every standing rule holds, and every step ends on a checkable bound.

## 4. Ripple

Search the live tree for the skill's name and for any sibling file renamed or deleted, and fix every reference in the same PR; frozen records stay as they are. Read the guide card in `docs/site/content.json` and edit it only when it no longer fits the skill, flagging the edit in the PR body as public copy for the user's eyeball. Done when the search returns only the skill's own folder and current references.

## 5. Ship

This repo's shipping motion, all in one PR:

- `agents/openai.yaml` paired with the invocation: the policy block present iff user-invoked.
- The README triple, wording touched only on an invocation flip, when the entry moves between the User-invoked and Model-invoked groups.
- The guide rebuilt (`python3 scripts/build-guide.py`), and rebuilt again after any rebase, since the generated HTML conflicts rather than merges.
- The skill's `DASH_DIRTY` entry in `scripts/repo-facts.mjs` removed.
- A minor changeset.
- The four gates green: lint, the test suite, the guide build with its identifier gate, and the dash gate on the touched paths (`node scripts/dash-gate.mjs <path>`).
- The PR body in the fixed shape below, pushed and opened without asking.

Done when the PR is open and green.

## The facts block

One markdown list, cut into the ticket and refreshed in step 1:

- **Kind**: standalone, loop hub, loop phase, peer, audit, reference, or router. A loop kind also reads `docs/loop-authoring.md` and names the obligations the skill carries.
- **Words**: `SKILL.md`, and each sibling with its own count.
- **Invocation**: user- or model-invoked, and whether `agents/openai.yaml` agrees.
- **Siblings**: every file in the folder besides `SKILL.md` and `agents/`, with the `SKILL.md` sentence that points at it.
- **References out**: every skill the body names (plain `/name` labels, Skill-tool calls, contract pointers), with the sentence's job.
- **References in**: every live-tree file outside the folder that names the skill or a sibling (READMEs, `plugin.json`, `content.json`, other skills, `GLOSSARY.md`).
- **Examples**: the worked examples inline, counted, with the branch each covers.
- **README entries**: the top-level and bucket lines, quoted.
- **Guide card**: the `content.json` group, gist, example, and reach line.
- **Dash gate**: whether `DASH_DIRTY` still grandfathers the skill.
- **Prior tickets and grills**: links, with the decisions that still bind.

## Standing rules

Written once here; a ticket says nothing about method.

- A standalone skill names no other skill; loops and routers keep their routing redirects.
- At most two worked examples inline, chosen to cover the branches; the rest cut.
- Rules stated positively; the em-dash rule is the only paired ban.
- Invocation leans user-invoked unless the model or another skill must reach it, decided per skill in the grill.
- Every-run Excel contracts stay inline in the skill that writes them; siblings hold some-runs material only.
- AI-agnostic wording: "the agent", with a vendor name only for a real surface (the Excel add-in, the Skill tool).
- The checklist, "does NOT do", and "how this fits" sections are deleted; only routing redirects survive.
- Operative `/name` call sites become Skill-tool calls; router prose keeps plain `/name` labels.
- Every prose em dash hand-rewritten in the same edit; sheet-title and stamp literals keep theirs.

## The PR body

A fixed block, then the smoke run:

- The one rule and its leading word, or "none".
- What was cut and why.
- Invocation before and after.
- Words before and after, `SKILL.md` and siblings.
- Guide copy: touched or not.

Smoke run: a standalone skill, and an audit when a small fixture workbook is cheap to make, runs the rewritten skill on a synthetic, fictional input with the output pasted in. Loop skills, the router, and the reference skills ship without one.
