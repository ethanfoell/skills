---
name: chat-title
description: Propose a short, scannable title for the current chat, sized to survive the sidebar.
argument-hint: "Anything to focus the title on?"
disable-model-invocation: true
---

Read the whole chat (ignoring this skill's own earlier turns), pick the one outcome that headlines it, and propose a single title. The bar is the sidebar-scan test: skimming chats in one Project group, the title alone says which chat did this work.

If the user gave a steer (the argument, or "title it around the Velixo work"), title that instead of picking the dominant outcome. If they supplied a title, polish it to these rules rather than substituting your own.

## The grammar

- **Subject-first, not verb-first.** `Chat-title skill build`, not `Build chat-title skill`: a leading `Build`/`Fix`/`Update` is shared across dozens of chats. The action trails as a word only when the subject alone is ambiguous.
- **One concrete outcome the chat actually landed.**
- **Let the subject carry the area** when that sets the chat apart (`Finance loop close-out`); no separate area prefix.
- **Sentence case;** a colon only when it genuinely reads as scope then detail (`Velixo refresh: speed fix`).
- **Length:** target ~30 characters, ceiling ~50, the load-bearing word inside the first ~25 (roughly where the sidebar truncates). For non-Latin scripts, govern by the skim test, not the count.

## Leave out

A title is a label, not a record:

- **The repo/project name and the date:** the app already groups by Project and sorts by date.
- **App-tracked status:** `(WIP)`, `[review]`, `staging`, PR or environment tags.
- **Machine identifiers:** ADR/PRD numbers, ticket IDs, cell addresses, file paths. Translate up to the human-readable thing (`Payment-retry design spec`, not `RFC 217`).
- **Effort narration, hedges, padding, and em dashes.**

## Title only what landed

Name what the chat did or shipped, never what it merely discussed, an approach it dropped, or the request to title it. This one rule resolves the awkward cases:

- **No real work** (pure Q&A, exploration, planning with no artifact): title the topic or question (`Approval-chain options`); planning-only is titled as planning. This skill only titles the chat: a thin chat gets its topic title or the empty case below, never a handoff to `/daily-note` or any summary skill.
- **Mid-task:** name the underway work by its subject (`Sub-mapping coverage`); a later run upgrades it once work lands.
- **Pivoted topics:** title where the chat landed; drop the abandoned opener.
- **Cancelled or failed:** title the investigation, not a fix that never shipped.
- **Sensitive content** (names with salaries, credentials, health or legal detail): title one level up (`Comp review analysis`) and say you genericised it; the sidebar is shoulder-surfable, and the user can still override.
- **Standing multi-day thread** that accretes many outcomes: keep a stable identity (`Billing system migration`) so it stays findable, rather than churning the title each run.
- **Genuinely empty or all-meta:** say there is not enough to title well and ask what the chat is for, rather than emitting `General chat`.

## Output

Present one title on its own line, ready to copy, with a one-line note to paste it into the chat's rename field; no character count. Offer an alternate only when two outcomes genuinely tie or no dominant one is clear. This skill cannot see sibling titles; when the work is the recurring kind (a second reconciliation, another auth fix), add a discriminator pulled from the chat (the subsystem, the period, the vendor) rather than inventing a date or sequence number.

On a re-run, replace the title outright. If the dominant work shifted, or a mid-task title can now name its landed outcome, emit the new one; if the thrust is unchanged, return the same title and say it still fits.
