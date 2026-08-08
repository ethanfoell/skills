# Folders

The core domain bucket for a different substrate: the filing-system loop (explore → plan → build → log) for directories instead of workbooks.

**The full loop ships** — the orientation trio, the plan/build action arm, and the `folder-log` close-out — woven with a default `CONTEXT.md` glossary discipline: the loop seeds and refreshes the glossary by composing `/domain-modeling` at the active points and reads it for vocabulary at the rest. A large reorg is ordered as vertical slices where applicable — move + reference-rewire + validation, each validated before the next opens. A settled, hard-to-reverse structural decision earns a per-folder `docs/adr/` entry — offered at close-out and onboarding by composing `/domain-modeling`, three-prong-gated and default-off, either/or with the CLAUDE.md open-decision default. The loop is wired into `ask-ef` as its folder-native build-arm, and `folder-plan` points up the stairs (`/grill-with-docs → /to-spec → /to-tickets`) when a task reveals itself as a multi-session feature. The loop is **user-invoked** throughout — `folder-explore` is a present-and-name router that names the next mode for you to invoke.

## User-invoked

Reachable only when you type them (`disable-model-invocation: true`).

- **[folder-explore](./folder-explore/SKILL.md)** — Orient to a folder at session start: a fast state-check, then an adaptive routing menu (Resume, Integrate, Quick Pickup, Full orientation, Read-only scan, Onboard). The loop's session-start router.
- **[folder-onboarding](./folder-onboarding/SKILL.md)** — Open a folder for the first time and make it understandable: lay down a README (humans) and CLAUDE.md (agents), choose and record the history layer (Git by default), surface findings. The first-visit mode.
- **[folder-pickup](./folder-pickup/SKILL.md)** — Quick re-orientation for an already-onboarded folder: read the two surfaces + recent history, return a locked six-line summary, flag anything in-flight, then stop. The return-visit mode.
- **[folder-plan](./folder-plan/SKILL.md)** — Draft a chat-first six-section plan (Goal, Approach, Steps, Validation, Open Questions, Out of Scope) before multi-file folder work; Validation is the keystone. The planning phase.
- **[folder-build](./folder-build/SKILL.md)** — Execute a folder plan with four guardrails: per-step reporting, inline keystone validation, destructive-op confirmation (archive-by-move), and a Surfaced list. The execution phase.
- **[folder-log](./folder-log/SKILL.md)** — Close out a unit of work: write the task record to the folder's history layer (a Git commit by default; a `LOG.md` entry on file-based folders), refresh the README Status snapshot if the task changed it, and propose CLAUDE.md standing-rule updates when the work surfaced a new convention, gotcha, or risk. The close-out phase.
