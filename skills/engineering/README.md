# Engineering

Matt Pocock's code-craft skills — the build-arm for small apps and tools — kept **wholesale on Matt's own stack** (TypeScript/React/vitest/pnpm examples intact, not re-grounded to Python). This is deliberate: the goal is learning to code Matt's way, so his worked examples *are* the teaching material — pruning them would destroy the point, and keeping them byte-faithful makes pulling his future changes trivial.

Nine skills, adopted from Matt's repo and kept current with his changes. The bucket is **mixed-kind**, so entries group **User-invoked** / **Model-invoked**.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[implement](./implement/SKILL.md)** — Implement a piece of work from a PRD or set of issues — composing `/tdd` at pre-agreed seams, typechecking and running tests as it goes, then handing off to `/code-review` when done.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)** — Scan a codebase for **deepening opportunities** (shallow modules → deep ones), present them as a self-contained visual HTML report (Tailwind + Mermaid, before/after diagrams, recommendation badges), then grill the one you pick through `/codebase-design` and `/grilling` — keeping `CONTEXT.md` and `docs/adr/` current via `/domain-modeling` as decisions crystallise. The native code-substrate architecture-review skill. See `HTML-REPORT.md` for the full report scaffold and diagram patterns.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them and other skills can compose them).

- **[code-review](./code-review/SKILL.md)** — Review the changes since a fixed point along two parallel axes: **Standards** (does the code follow the repo's documented coding standards, plus a fixed Fowler smell baseline — always judgement calls, repo docs override) and **Spec** (does it faithfully implement the originating issue/PRD), via parallel sub-agents reported side by side — never merged, so one axis can't mask the other. `/implement`'s hand-off target.
- **[codebase-design](./codebase-design/SKILL.md)** — Shared vocabulary for designing **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface (module, interface, depth, seam, adapter, leverage, locality). Use it when designing or restructuring code, or when another skill needs the deep-module language. See `DEEPENING.md` and `DESIGN-IT-TWICE.md` for the worked extensions.
- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)** — Feedback-loop-first diagnosis for hard bugs and performance regressions: build a tight pass/fail signal that goes red on *this* bug, then bisect → hypothesise → instrument → fix → regression-test. Auto-triggers on "debug this" / "broken" / "slow". See `scripts/hitl-loop.template.sh` for the human-in-the-loop reproduction harness.
- **[prototype](./prototype/SKILL.md)** — Build a **throwaway** prototype to answer a design question, then delete it. Two branches: **LOGIC** — a runnable terminal app that lets you feel a state machine or business-logic flow (printed state + numbered actions); **UI** — several radically different visual variations of one screen, toggleable from a single route. Not production code. See `LOGIC.md` and `UI.md` for the two worked branches.
- **[research](./research/SKILL.md)** — Delegate reading legwork to a **background agent**: it investigates a question against **primary sources** (official docs, source code, specs, first-party APIs — never a secondary write-up), follows every claim back to the source that owns it, and leaves a single cited Markdown file where the repo keeps such notes — while you keep working.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)** — A disciplined procedure for an in-progress git merge/rebase conflict: see the current state, find the primary source and original intent behind each side (commits, PRs, tickets), resolve every hunk (preserve both intents where possible; never invent behaviour, never `--abort`), run the project's automated checks, then finish the merge/rebase. Dependency-free — a noted conceptual overlap with `misc/git-guardrails`, deliberately not cross-referenced.
- **[tdd](./tdd/SKILL.md)** — The reference that makes the red → green loop produce tests worth keeping: what a good test is, **seams as a hard gate** (tests live only at pre-agreed public boundaries, confirmed before any test is written), the anti-patterns (implementation-coupled, tautological, horizontal slicing), and the rules of the loop — vertical slices, tracer bullets, refactoring left to the review stage. See `tests.md` and `mocking.md` for the worked examples.
