# Workbook grilling

The workbook branch of grill-with-files: read this when the plan touches an Excel workbook.

**Recon:** note the sheets, where tables start, and whether the workbook carries an Instructions, Agent, or Audit Log sheet. The how-to-work-here layer lives in those sheets: the **Instructions sheet** (how the workbook works), the **Agent sheet** (conventions, gotchas, DO-NOT-EDITs, open decisions), and the **Audit Log** (the session log: what prior tasks decided, retired, or flagged stale). Not every workbook has them, but when they exist, read them before grilling; a plan that contradicts them is already broken.

**Pressure a workbook throws:**

- A logged retirement: *"The Audit Log retired that sheet as the source of truth; why is the plan still keying off it?"*
- A live-data pull: *"That Velixo pull may have silently returned blank or stale. Refresh and check first, or build on whatever's cached?"*
