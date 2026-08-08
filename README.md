# ethanfoell-skills

> **⚠️ Early release.** This is an early public cut of the skill framework I use daily. The skills work — I run them on real finance and filing work — but polish, docs, and coverage are uneven, and things will change without notice as it evolves.

My agent skills for Claude — engineering discipline applied to a financial analyst's work, and the general-purpose tools that grew around it.

I'm a financial analyst, not a career programmer. This framework exists because the disciplines that make software reliable — plan before you build, validate against an independent target, leave an audit trail, hand off cleanly — turn out to be exactly what Excel workbooks and shared-drive folders need too. Three arms carry that idea:

- **Substrate loops** take a piece of real work from first look to finished, audited change. The **finance loop** runs Excel workbooks through explore → plan → build → log, with tie-outs as the keystone, Velixo/Acumatica reporting knowledge on tap, and formula/logic audits to escalate to. The **folders loop** does the same for filing systems — same shape, different substrate.
- **A planning pipeline** grills rough ideas into agent-ready work: relentless interviewing (`/grilling`), specs (`/to-spec`), tracer-bullet tickets (`/to-tickets`), triage, and shared maps for efforts too big and foggy for one session (`/wayfinder`).
- **A code-craft arm** builds the small finance tools alongside: TDD, disciplined implementation, design vocabulary, debugging, prototyping, and review.

Around those sit genuinely cross-domain tools (handoffs, meeting notes, work comms, teaching) and the framework's own machinery.

## What's inside

Skills live under `skills/<bucket>/<skill>/SKILL.md`; each bucket's README lists its skills in full.

| Bucket | What lives here |
|---|---|
| [`finance/`](./skills/finance/README.md) | the Excel workbook loop, Velixo/Acumatica reporting, the audits |
| [`folders/`](./skills/folders/README.md) | the filing-system loop — same discipline, different substrate |
| [`engineering/`](./skills/engineering/README.md) | the code-craft arm: TDD, implement, design, debugging, review |
| [`productivity/`](./skills/productivity/README.md) | cross-domain tools: grilling, handoff, meeting notes, teach |
| [`meta/`](./skills/meta/README.md) | the framework's own machinery: the planning pipeline, the router, the style guide |
| [`misc/`](./skills/misc/README.md) | cross-cutting utilities |

An interactive guide to the whole framework lives at **<https://ethanfoell.github.io/skills-ef-guide/>** (its source ships in this repo under [`docs/site/`](./docs/site)).

## Install

Three ways in, depending on where you work with Claude. After installing, `/ask-ef` tells you which skill fits your situation, and `/setup-skills-ef` configures a repo once before you use the planning-pipeline skills there.

### claude.ai, Cowork, and Excel — plugin upload

This path runs on a built `.plugin` file, which I build from this repo and hand out directly — there's nothing for you to build.

1. Get the `.plugin` file from me.
2. In claude.ai, open **Settings → Customize → Personal plugins → Upload plugin** and pick the file.
3. The skills then surface everywhere your account reaches: the website, Cowork, Claude Code, and the **Claude for Excel** add-in — Excel reads installed-plugin skills natively, so the finance loop runs right inside the workbook.

### Claude Code — marketplace

This repo is its own plugin marketplace. A managed bundle that updates when I ship:

```bash
claude plugin marketplace add ethanfoell/skills
claude plugin install ethanfoell-skills@ethanfoell
```

(Or from inside a session: `/plugin install ethanfoell-skills@ethanfoell`.) Pull updates with `claude plugin marketplace update ethanfoell`.

### Copy the files — npx

The hack-on-them path: copies editable skill files into your own project instead of subscribing to mine.

```bash
npx skills add ethanfoell/skills
```

Pick the skills you want from the list. Needs Node. Once copied, the files are yours to adapt.

## How this repo works

This repo is a **generated snapshot** of a private authoring repo, scrubbed and exported release by release — each release lands here as a single commit naming the version and source, so the history is a release ledger, not a working log. Version numbers continue the private release line: pre-1.0 is the early-release signal, and 1.0 is reserved for the mature-release moment. [`CHANGELOG.md`](./CHANGELOG.md) tracks the public releases.

## Lineage

This framework is a fork of [`mattpocock/skills`](https://github.com/mattpocock/skills) by Matt Pocock — a documented fork: cloned and rebuilt in my own conventions rather than GitHub-forked, with the lineage carried here and in [`NOTICE`](./NOTICE). His grilling, handoff, and teach skills, the `to-spec → to-tickets → triage` pipeline, domain modeling, and `writing-great-skills` are the scaffold this builds on, and the engineering bucket keeps his code-craft skills wholesale, worked examples intact. MIT licensed, both copyrights in [`LICENSE`](./LICENSE).
