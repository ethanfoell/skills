# Finding and reading sessions

How to enumerate the backlog, flag the badly-titled, and read enough of each to title it. All read-only.

## Enumerate

`mcp__ccd_session_mgmt__list_sessions` takes only `limit` and `include_archived`; there is no project filter. It returns recent sessions across **all** projects, each with `sessionId` (a `local_<uuid>`), `title` (absent when untitled), `cwd`, `isArchived`, `isRunning`, `lastActivityAt`. The current session is excluded.

- **Default scope:** call it, then keep only entries whose returned `cwd` is the current project. The cwd filter is yours, applied after the call.
- **`limit` bounds the cross-project list before you filter,** so raise it whenever the current project's sessions might sit past the most-recent `limit` entries, or they never reach the filter.
- **Widen only on request:** keep all `cwd`s (*all projects*), or set `include_archived: true`.

## Flag the badly-titled

Keep a session as a candidate if its title is:

- **missing** (no `title` field),
- **lowercase / ungrammatical** (`payment retry and webhook backoff stood up in acme - api`),
- **generic** (`New session`, or a verbatim first-message fragment), or
- **over-granular** (mostly numbers/IDs, names a slice/ADR but not the codebase).

Skip titles that already name the work clearly. **Skip `isRunning: true` sessions** by default: their auto-title is still provisional, and their transcript is still being written, which destabilizes the mtime prefilter below. Flag one only if asked.

## Read a candidate's transcript

The strong content source is the **on-disk JSONL**, not `search_session_transcripts` (substring snippets only: fine for a keyword spot-check, weak for titling).

**Location.** `~/.claude/projects/<encoded-cwd>/<internal-uuid>.jsonl`, where `<encoded-cwd>` is the `cwd` with every non-alphanumeric character replaced by `-` (e.g. `/Users/me/dev/foo` → `-Users-me-dev-foo`). Each `<uuid>.jsonl` is one session.

**Titles on disk come in two record shapes:** `{"type":"ai-title","aiTitle":"…"}` (the auto-titler: the common case, and itself a weak-title signal) and `{"type":"custom-title","customTitle":"…"}` (human-set).

**Join by content: title, mtime, and in-record ids all fail as keys.**

- **Title.** The `list_sessions` title comes from the app's own session index and routinely diverges from the on-disk records, or is absent there, so grepping `aiTitle`/`customTitle` for the listed title misses most sessions.
- **Recency.** `lastActivityAt` ≈ file mtime is a coarse prefilter, never a key. Files get rewritten on session *resume* and by occasional batch operations long after a session's last activity, so mtime routinely runs minutes to tens of hours later than `lastActivityAt`. (Measured on a real backlog: **0 of 13** content-confirmed sessions fell within a 2-minute tolerance; deltas reached ~30 h, and five unrelated files shared one batch-rewrite mtime.) Use recency only to order which files to open first, comparing as UTC epoch: `lastActivityAt` is ISO `…Z`; read mtime with `stat -f %m <file>` on macOS/CCD.
- **In-record `sessionId`.** The `sessionId` inside a title record equals the jsonl filename stem, so it pins a file's identity once you're reading it, but it is **not** the `local_<uuid>` from `list_sessions`, so it can't perform the initial join.

So **the opening user turn is the join key.** For each candidate, open the project dir's files (newest mtime first) and read the first `"type":"user"` message, then match it to the `list_sessions` entry by the *work it describes*: that turn is both what you title from and the proof you found the right session. Read the opening turn plus a few early turns only; never load whole transcripts.

- **Expect more files than sessions.** A resumed session writes a fresh `<uuid>.jsonl`, so one `list_sessions` entry can match several files sharing the same opening turn (a resume chain); any of them titles fine.
- **When no file's opening turn matches**, or two unrelated ones do and content can't disambiguate, don't guess a file: propose from the `list_sessions` metadata alone, or flag the session needs-manual.

## Deep-check a named project

Given a project path, scope to that one `<encoded-cwd>` dir and read the opening turns of **all** its sessions (not just title-flagged ones), then surface those whose title underserves the content. Bounded to the one project, never all of `~/.claude/projects`. **If the path has no `<encoded-cwd>` dir or no `.jsonl` sessions, say so and ask the user to confirm it's the project root**; otherwise a wrong path and a clean project look identical.

## Large backlog

When there are many candidates, **offer** to fan the transcript reads out across parallel subagents (the `Agent` tool) or a `Workflow`, both opt-in: one agent reads a slice of candidates' opening turns and returns `{old title, codebase, work}`; synthesize the single proposal table from the results.
