# Meta

The framework's own machinery — the skills that build, model, and maintain this repo. Neither finance work nor general productivity; repo-maintenance tooling.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[ask-ef](./ask-ef/SKILL.md)** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[setup-skills-ef](./setup-skills-ef/SKILL.md)** — Configure a repo for these skills (issue tracker, triage labels, domain doc layout). Run once before first use.
- **[to-spec](./to-spec/SKILL.md)** — Turn the current conversation into a spec (you may know it as a PRD) and publish it to the issue tracker. No interview — just synthesis.
- **[to-tickets](./to-tickets/SKILL.md)** — Break a plan, spec, or conversation into tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker.
- **[triage](./triage/SKILL.md)** — Move issues and external PRs through a state machine of triage roles.
- **[wayfinder](./wayfinder/SKILL.md)** — Plan a huge chunk of work — more than one session can hold — as a shared map of investigation tickets on the issue tracker, resolved one at a time until the way is clear.
- **[writing-great-skills](./writing-great-skills/SKILL.md)** — Reference for writing and editing skills well: the vocabulary and principles that make a skill predictable. The style guide for this repo.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[domain-modeling](./domain-modeling/SKILL.md)** — Actively build and sharpen a project's domain model — challenge terms against the glossary, stress-test with scenarios, and update `CONTEXT.md` and ADRs inline.
