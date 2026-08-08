---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

The temp directory is the default, not a rule: if the user names a destination, or the active work's own convention in this session states one, write the handoff there instead — the stated destination wins. (Example: the folder loop's park step files the handoff into the folder as a `future-work/` item; when that's the work being handed off, honor it.)

If the surface can't write files, output the whole handoff as one self-contained fenced markdown block instead — assume the receiver has none of this chat's history and may be in a different tool.

State as fact only what you confirmed this session; mark a lead as a lead. An unverified guess written as settled fact is the most common way a handoff misleads, so lean the doc to how settled the work is: for decided work, say what to do; for open work, pose the question rather than pre-answering it.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Name those skills as available-if-present, so a receiver in a different tool can use the ones its workspace has.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Flag any files dropped into this chat as attachments — the human needs to re-attach those to the next session alongside the handoff.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
