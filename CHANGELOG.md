# ethanfoell-skills

The public changelog. Version numbers continue the private authoring repo's release line, which reached 0.24.2 before the first public cut; this file starts there rather than reconstructing the pre-public history. Each public release lands as one export snapshot, and the private releases it rolls up are summarized under their own numbers here.

## 0.36.0

`daily-note` is rewritten for long sessions and for pasting into a spreadsheet.

- The write-up goes to a fresh subagent that reads the session's stored transcript, so a long chat that has been compacted still gets every piece of its work into the note. In T3 Code the subagent runs on Opus 5.5 or GPT-6.1-Sol at high effort, matching the chat's provider; elsewhere it uses the surface's own subagent tool. With no subagent, a failed one, or a transcript from the wrong session, the main agent writes the note itself, from its stored transcript when it can reach one.
- The output is plain text built to paste into one Excel cell: the dated header as an ordinary chat line, then the note with one line per piece of work, then a `More detail:` block of `Label: sentence` lines, now on every note rather than only when it earns its place.
- The voice reports what the work produced rather than claiming it was checked. Words like "confirmed" and "tied out" are kept for checks the user made, and the note leaves the worker unnamed: the user appears only as "I", for what they still have to do, and other people by name or role.

## 0.35.0

`video-research` proves a fresh transcript before reading it, and ships the tools that do it.

- `scripts/transcript.py check` flags loops, heavily repeated lines, and stretches where the audio carries speech but the transcript has almost no words, and refuses audio shorter than the transcript. `scripts/transcript.py reading-copy` splices re-transcribed clips in by offset and writes the timed reading copy. `scripts/flatten_chat.py` turns a YouTube chat replay into Markdown.
- Transcription runs whisper.cpp with `-mc 0`, which cleared both the looping and the blank-through-speech failures in tests. `MEDIA.md` records why `--vad` and `--prompt` are left out. Livestream polling and chat replay move to a new `LIVESTREAM.md`.
- Download guidance from the first livestream run covers downloading a finished stream at `post_live`, the fragment 401 error and its fix, size and caption caveats, why to skip `--write-info-json`, checking yt-dlp's own exit status in background chains, format pairs that fetch audio twice, and updating yt-dlp before a run.
- The skill adds a digest scope, a dated log that doubles as the provenance note, and an option to have subagents read ranges of a very long recording; a corrected reading copy lists its substitutions in its header.

## 0.34.1

`video-research` gains the livestream chat replay as an optional fourth channel: when to fetch it, how to check which chat the speaker reads, and how to pair a paid question with its spoken answer.

## 0.34.0

Upstream sync with Matt Pocock's skills repo (his v1.3.1), in four parts, plus an attribution cleanup.

- The domain-doc convention is renamed: `CONTEXT.md` becomes `GLOSSARY.md` and `CONTEXT-MAP.md` becomes `GLOSSARY-MAP.md` everywhere the skills read and write it (`domain-modeling`, whose format file is now `GLOSSARY-FORMAT.md`, `setup-skills-ef`, `triage`, `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `codebase-design`, `wait-what`, `ask-ef`, the six folder-loop skills, `wrap-up`, and `rewrite-skill`; this `GLOSSARY.md` is the project glossary, unrelated to the file retired in 0.25.0). If you have an existing `CONTEXT.md` or `CONTEXT-MAP.md`, rename it: the skills only look for the new names going forward. Update the plugin first, then rename. `/folder-explore` and `/folder-pickup` still read a legacy `CONTEXT.md` in a folder and flag the rename.
- Three skills adopted from him into engineering. `/implement-spec` (user-invoked) builds a whole spec in one run: it reads the tickets as a task graph, hands each ready ticket to a subagent in its own worktree, lands everything on one integration branch, and closes with `code-review`. `pr` (model-invoked) is the shape a pull request body takes: a summary as the smallest visual that makes the change clear, before and after evidence, and a merge-danger call (one-way or two-way door, plus blast radius); its summary visuals adapt HumanLayer's `show-me` skill, by Dex Horthy (MIT, credited in `NOTICE` and in the skill's own `CREDITS.md`). `/retro` (user-invoked) looks back at a coding session and suggests changes to the agent's environment rather than the code: navigation pointers, automated checks, coding standards, steering files, tool economy, information access.
- `resolving-merge-conflicts` leaves the shipped set, as it left his: the agent works through a merge or rebase conflict without a dedicated skill.
- `/ask-ef` teaches the updated main flow: tickets are worked one per session with `/implement` or all at once with `/implement-spec`, `pr` shapes the body when the work goes up as a pull request, and `/retro` closes the loop; the folder and workbook loops keep their own log step in its place. After a bug fix it points you at `/retro`.
- `NOTICE` reproduces the copyright line of each work this set adapts.

## 0.33.0

A refresh of this tree's README, CLAUDE.md, and changelog, plus two new skills.

- New `/rewrite-skill` (meta, user-invoked): the procedure for rewriting one skill under `writing-for-agents` in one attended session. It gathers the skill's facts, grills the user on what is bothering them and how the skill should be invoked, rewrites around the skill's one rule, ripples the change through everything that names it, and ships. It assumes the private authoring repo's tooling, which this tree does not include.
- New `video-research` (productivity, model-invoked): research a topic across a video or recording (YouTube, a livestream VOD, a local file). It reads the whole transcript by default, tracks separately what was read from the transcript, heard in freshly transcribed audio, and seen in frames, and saves a timestamped write-up with screenshots plus a durable archive of the sources. The coverage record is built so the write-up claims no more than was reviewed.
- This repo's README, CLAUDE.md, and changelog are brought current with the skills that ship (53 across six buckets), and a few stale lines are trimmed from `workbook-log`, the engineering bucket README, and `NOTICE`.
- Private tooling gains a second package for Codex built from the same skill set; nothing in this tree changed for it.

## 0.32.1

Private tooling only (the `.plugin` build is hardened); nothing in this tree changed.

## 0.32.0

`daily-note` is rewritten around fronts and becomes user-invoked. A front is a piece of work with its own outcome; the note is written per front, each carrying task, outcome, and follow-up, and the old length and leave-out rules collapse into that one rule. The skill now fires only on `/daily-note`, so other chats never summarize in this shape unasked.

## 0.31.0

New `/unslop` (productivity, user-invoked): cut AI tells from a piece of writing and sharpen its voice without changing what it says. It works from an input/output contract, reads the register first so it never invents opinions, and checks itself against completion criteria. Its rules adapt Cursor's `pstack` plugin (MIT, credited in `NOTICE`).

## 0.30.0

`workbook-onboarding` is trimmed to a short operative core. The sheet conventions become a one-screen table inside `SKILL.md`; the Spec and Tickets sheet contracts, the wayfinder map, session-start detection, and the triage mapping move into one opt-in `MULTI-SESSION.md`; `AUDIT-LOG-FORMAT.md` keeps only the task-block shape and the stub lifecycle. Onboarding lays down Instructions and Audit Log by default and creates the Agent sheet only when there is guidance to record. The multi-session and triage machinery runs on Claude Code and Cowork; the Excel add-in treats existing Spec and Tickets sheets as inert.

## 0.29.0

- `workbook-review` and the Baseline-sheet lifecycle leave the shipped set. `workbook-build` drops its pre-flight baseline capture and the review offer at close (the destructive-op confirmation stays); `workbook-log` drops the Baseline-sheet clearing.
- The productivity skills `daily-note`, `work-coms`, `meeting-notes`, `grill-with-files`, `chat-title`, and `retitle-sessions` are trimmed to short operative cores, with restatement deleted and steps sorted first. `grill-with-files` moves its workbook-only depth into a new `WORKBOOK-GRILLING.md` sibling.

## 0.28.0

Style guardrails. Skill prose is now gated for em dashes by the private authoring repo's tooling (the finance and folders skills stay grandfathered until their trim), and each skill's `description` is checked as a single-line YAML scalar, which caught and fixed the `daily-note` and `folder-plan` frontmatter. `writing-for-agents` gains a House-style section, and the `triage` out-of-scope reference's example fence is fixed to render correctly.

## 0.27.0

New `/wrap-up` (productivity, user-invoked): a session close-out ritual. It audits everything the session changed, writes a Done / Where it stands / Open / Next summary, and ends on one Proposals block: learnings worth keeping, a commit if work is uncommitted, doc prunes, an owed loop close-out. Workbook and folder tasks route to `/workbook-log` and `/folder-log`; mid-task pauses route to `/handoff`.

## 0.26.0

Private tooling only (the authoring plugin and marketplace were renamed so they sit beside this public one in Claude Code); nothing in this tree changed.

## 0.25.0

Upstream sync with Matt Pocock's skills repo (his v1.2.3), in four parts:

- Fast-forwards to the carried skills: `diagnosing-bugs` gains a Redact rule (every secret shown as `<REDACTED>`, loops built against env vars); `prototype`'s logic branch produces a single shareable HTML file; `domain-modeling` now triggers on `CONTEXT.md` and ADR editing; `grill-me`, `grill-with-docs`, and `handoff` invoke other skills via the Skill tool; `tdd`, `codebase-design`, `improve-codebase-architecture`, `research`, `resolving-merge-conflicts`, `teach`, and the `triage` and `setup-skills-ef` reference files take his edits verbatim. Every one of these is now free of em dashes.
- `grilling` adopts his rewrite: the interview works a design tree in rounds, asking the whole frontier of settled-prerequisite questions at once, each numbered with a recommended answer, and finishing when the frontier is empty. `grill-me`, `grill-with-docs`, and `grill-with-files` inherit the change.
- `writing-great-skills` is replaced by `writing-for-agents` (meta, model-invoked): the reference for writing any document an agent consumes, with the skill-specific mechanics in a sibling `SKILL-MECHANICS.md`. Its `GLOSSARY.md` sibling (the writing glossary, not a project glossary) is retired with it.
- Three new skills adopted from him: `wizard` (engineering) generates an interactive bash wizard that walks a human through the steps only they can perform; `to-questionnaire` (productivity) turns a decision you can't answer alone into a Markdown questionnaire for the person who can; `wait-what` (productivity) re-pitches the last message in Simplified Technical English with the missing context. `ask-ef` gains a Phase boundaries section (Continue, `/clear`, `/handoff`, subagent, `/compact`), worked as an ordered tree in a new `PHASE-BOUNDARIES.md`.

## 0.24.2

First public release: the framework as it stood, 47 skills across six buckets (finance, folders, engineering, productivity, meta, misc), the plugin and marketplace manifests, and the interactive guide's site. See the [README](./README.md) for what the framework is and how to install it.
