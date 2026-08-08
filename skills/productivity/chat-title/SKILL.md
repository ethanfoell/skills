---
name: chat-title
description: Propose a short, scannable title for the current chat, sized to survive the sidebar.
argument-hint: "Anything to focus the title on?"
disable-model-invocation: true
---

Propose a single short title for the current chat: the high-level work it did, sized so it survives the sidebar. You are the final filter, so tweak or reject it freely.

## The sidebar-scan test

Skimming chats inside a single Project group, you can tell which chat did what work from its first skim alone. Every rule below serves that test.

This skill reads only the current chat, so it cannot see sibling titles and cannot guarantee yours is distinct from a real neighbour. When the work is the recurring kind (a second reconciliation, another auth fix), offer a discriminator pulled from the chat — the subsystem, the period, the vendor — rather than inventing a date or sequence number.

## Write the outcome, subject-first

- **Lead with the distinctive subject, not a verb.** `Chat-title skill build`, not `Build chat-title skill` — a leading `Build`/`Fix`/`Update` is shared across dozens of chats. The action trails as a word when the subject alone is ambiguous.
- **Name one concrete outcome the chat actually landed.** The work decides which single outcome headlines.
- **Let the subject carry the area** when that is what sets the chat apart (`Finance loop close-out`). No separate area-prefix.
- **Sentence case.** No forced separator; use a colon only when it genuinely reads as scope then detail (`Velixo refresh: speed fix`).

## Leave out

A title is a label, not a record. Omit each of these, for the reason given:

- **The repo/project name and the date** — the app already groups chats by Project and sorts them by Date, so these duplicate an axis and burn the window.
- **App-tracked status** — `(WIP)`, `[review]`, `staging`, PR or environment tags. The app tracks state on its own axes.
- **Machine identifiers** — ADR/PRD numbers, ticket IDs, cell addresses, file paths. Translate up to the human-readable thing (`Payment-retry design spec`, not `RFC 217`).
- **Effort narration, hedges, padding, and em dashes** — strip any em dash before presenting.

## Title only what landed

Name what the chat did or shipped, never what it merely discussed, an approach it dropped, or the request to title it. A chat that built this skill is `Chat-title skill build`, never `Chat title generation`. This one rule resolves the awkward cases:

- **No real work** (pure Q&A, exploration, planning that produced no artifact) → title the topic or question (`Approval-chain options`); do not manufacture a verb. Planning-only is titled as planning. This skill only titles the chat — it does not route a thin chat to `/daily-note` or any summary skill; if there is nothing worth titling, say so (see the empty case) rather than handing off.
- **Mid-task** → name the underway work by its subject (`Sub-mapping coverage`), no `(WIP)` tag. A later run upgrades it once work lands.
- **Pivoted topics** → title where the chat landed; drop the abandoned opener.
- **Cancelled or failed** → title the investigation, not a fix that never shipped.
- **Sensitive content** (names with salaries, credentials, health or legal detail) → title one level up (`Comp review analysis`, not `Jane's $120k package`) and say you genericised it, so you can add a safe discriminator. The sidebar is shoulder-surfable; you can still override.
- **Standing multi-day thread** that accretes many outcomes → keep a stable identity (`Billing system migration`) so you can find it again, rather than churning the title each run. A bounded chat still gets its one outcome.
- **Genuinely empty or all-meta** → say there is not enough to title well and ask what the chat is for. Never emit `General chat`.

## Length

Target ~30 characters, ceiling ~50. The load-bearing word must land in the first ~25 characters — roughly what the sidebar shows before truncating, though it moves with pane width and font, so design to the narrow case. A prose-only skill cannot measure the live cut, so treat this as behaviour, not a gate. For non-Latin scripts, govern by the skim test, not the character count.

## Output

Present one title on its own line, ready to copy, with a one-line note to paste it into the chat's rename field. Offer one or two alternates only when two outcomes genuinely tie or the dominant one is unclear — otherwise a single best title is the answer. Run the quality check silently; never show a character count.

If the user gave a steer (the argument, or "title it around the Velixo work"), title that and skip the dominant-outcome pick. If they supplied a title, polish it to these constraints rather than substituting your own.

## Repeat invocations

On a re-run, re-read the whole conversation (still ignoring this skill's own earlier turns) and **replace** the title — never append, never `(continued)`. If the dominant work shifted, or a mid-task title can now be upgraded to its landed outcome, emit the new one. If the thrust is unchanged, return the same title and say it still fits rather than inventing a gratuitously different one.
