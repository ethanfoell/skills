# Apply with computer use (opt-in, usage-heavy)

The heaviest rung of the apply ladder: drive the app UI to set the proposed titles for the user. **Only run this when the user explicitly asks for it**: it spends real computer-use budget. Before starting, say so and confirm.

## Preconditions

- The proposal table from `retitle-sessions` exists, with a *Find it by* hint per row.
- The user has asked for computer-use apply this session (the gate above).

## Procedure

1. `request_access` for the Claude / Cowork desktop app. The dialog reveals the granted tier. If it's restricted (read/click), typing may be blocked; report that and fall back to the worklist rather than fighting it.
2. For each approved row, **one at a time** (this drives the very app this session runs in):
   - Locate the session in the app's session list: search the *Find it by* hint (old title, or `cwd` + date/time for untitled rows) to disambiguate. For an **archived** row, look in the app's separate Archived list; renaming may require un-archiving first.
   - Open the rename affordance and set the **proposed title** exactly.
   - Screenshot to confirm the new title took before moving on.
   - Batch predictable keystroke/click sequences with `computer_batch`, but keep the per-session screenshot check: a mis-targeted rename is worse than a skipped one.
3. Report a short tally: renamed, skipped (not found / ambiguous), and any the tier couldn't type.

## Guardrails

- **Never** archive or delete a session, and never touch a row the user didn't approve.
- If a target session can't be found from its hint, skip it and list it as needs-manual; don't guess at a different session.
