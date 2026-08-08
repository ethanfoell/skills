# Title grammar

Reuse the grammar the **`chat-title`** skill defines (`productivity/chat-title`) — don't restate it. In short: **subject-first and front-loaded**, naming the high-level work *outcome*; **omit the repo/project and the date** (the app's Project chip and Date sort already carry them); omit app-tracked status; **translate machine IDs up** (`Payment-retry design spec`, not `RFC 217`); ~30–50 characters with the load-bearing word in the first ~25.

Two things differ for the retroactive, batch case:

- **Never prefix the codebase.** It's tempting when you're staring at sessions from many repos at once — but the app shows each session's Project as its own chip, so an `acme-api:` prefix just burns the window. The work is the title; the app supplies the repo.
- **Ensure distinctness across the batch.** Unlike `chat-title` (which sees only its own chat and can't guarantee uniqueness), this skill reads the whole backlog at once — so make each proposed title distinguishable from its real neighbours, pulling a discriminator from the chat (subsystem, period, vendor) when several sessions share a theme.

## Examples (backlog → proposed)

| Old title | Proposed |
|---|---|
| `payment retry and webhook backoff stood up in acme - api` | `Payment-retry & webhook backoff stood up` |
| `Slice G: invoice export wiring` | `Invoice-export wiring` |
| `Strip stray </content> tag from RFC 217` | `Stray content-tag fix` |
| `Billing Slice 3: statement close-out` | `Statement close-out` |
| *(untitled, opening turn is about reorganizing Documents)* | `Documents reorg` |

Each drops the repo prefix (the Project chip shows it) and leads with the distinctive subject. Machine IDs get translated **up** to what they name (`Slice 3` → the statement close-out) — or **dropped** when the work is a fix to the file, not the thing numbered (`RFC 217` → a stray-tag fix; the session touched the doc, not the decision).
