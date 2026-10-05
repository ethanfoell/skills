---
name: grill-with-files
description: Stress-test a plan against the files it touches. Open the workbooks, data, PDFs, and folder, and resolve every question the files can answer by looking instead of asking. Use when you're about to do real work in your filing system (reorganizing files, building or editing a workbook, extracting from PDFs, transforming data) and want the plan interrogated against what's on disk before you start. Triggers include "grill me on this before I start", "poke holes in my approach to this workbook/folder", "stress-test this plan against what's in the files", "interrogate this against the folder", grill-with-files. Prefer over plain grill-me whenever the plan touches files the agent can open; prefer /folder-explore or /workbook-explore (or the audit skills) when you want the files inspected or reported on rather than a plan interrogated.
---

When the plan is about work in the user's filing system, half the answers are already on disk: the workbook knows its own sheet names, the folder knows its own naming rule, a recording's transcript knows what was said. So the one rule that drives this skill:

> **If the files can answer it, look instead of asking.** Spend your questions only on what the files can't settle: the user's intent, judgment calls, and decisions not yet made.

## Read before you ask

Do a **light recon** first so the opening question lands on something real, then open more as specific questions demand. Skim structure, don't ingest everything: list the folder (naming patterns, version-y duplicates, subfolders); for data, note the headers and row count; for a PDF or recording, whether it's real text or a scan. When the plan touches a workbook, read [WORKBOOK-GRILLING.md](WORKBOOK-GRILLING.md) for the sheet-level recon and the pressure workbooks throw.

Prioritize the layer that says **how to work here**; it's where plans live or die. In a light setup that's a README and the folder's naming convention. In a mature one it's a cluster: a rules/agent doc ("never overwrite the originals"), naming and routing conventions (which kind of file belongs where), task SOPs, an inventory of what's present vs. missing, and a session log of prior decisions ("we deleted that, don't recreate it"). A plan that contradicts any of these is already broken; it just doesn't know yet. Don't assume this layer exists, but when it does, read it first.

## Grill with what you find

Call the Skill tool with "grilling" to interrogate the plan. The recon is what makes it *file-grounded*: each recommended answer **cites what backs it** ("pull from the master timeline; the rules doc names it the source of truth") instead of guessing. Turn what you read into pressure:

- **Conflict with a convention or a logged decision**: surface it and make the user reconcile. *"Everything here is date-prefixed `YYYY-MM-DD`; your plan emits `report_final`. Break the rule or rename?"*
- **Fuzzy file or scope reference**: pin it to reality. *"'The Q3 file': there are three, and `Q3 FINAL v2.xlsx` is newest. That one?"* *"'Clean up the folder': this level only, or recursively into the subfolders?"*
- **Edge case the files will actually throw**: invent the specific one. *"The PDF is scanned, not text. OCR it, or does the plan silently extract nothing?"* *"This download may be a re-export of something already filed; dedupe-check first, or assume it's new?"*
- **Claim vs. contents**: when the user asserts how something works, check the file and surface the gap. *"You said totals are row 50; row 50 is blank and 47 holds the total. Which drives the formula?"*
- **A number with nothing to reconcile against**: make the user name what it ties out to. *"This roll-up feeds the board deck: what control total must it match, and where does that total live?"*

## Finish with a grounded brief

You **read, you don't edit**: getting the plan right before any work starts is the whole point. At shared understanding, write a tight brief and stop:

```
## Grounded plan brief
Goal: <one line>
Resolved: <each decision + the file/convention that grounds it>
Assumptions: <inferred from the files; confirm>
Open / blocked: <what the files couldn't settle>
Scope: <what this won't touch>
```

**Offer the handoff, don't take it**: *"Hand this to /folder-plan or /workbook-plan, save it as a note in the folder, or leave it here?"* Default to leaving it in chat. One exception: when the interrogation surfaced a **multi-session feature** (many units, spanning sessions, the kind that wants a spec and independent tickets), lead the offer with handing the brief to /to-spec now, in this window. /to-spec never interviews; the grilling that just happened *is* its interview, and leaving the brief for a later session breaks the chain.

*Reach for grill-me instead when there are no files to open; for /folder-explore or /workbook-explore (or the audit skills) when the files should be inspected and reported on, not a plan interrogated.*
