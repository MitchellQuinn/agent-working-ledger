## Agent Working Ledger Use Policy

Creating no ledger is the default. The Agent Working Ledger is a recovery, audit, and drift-control tool for complex work; it is not a normal wrapper for every task.

Before creating a ledger, classify the task. Create or adopt a ledger only when losing context would materially harm correctness, safety, auditability, or handoff quality.

Create a ledger if any hard trigger applies:

- The user explicitly asks for a ledger, worklog, recovery file, continuation file, implementation log, or handoff note.
- The task is long-running, exploratory, validation-heavy, interruption-prone, handoff-prone, or multi-agent.
- The task involves debugging, migration, refactor, audit, incident analysis, or broad repository investigation.
- The work depends on accumulated evidence, rejected hypotheses, decisions, or assumptions that must be preserved.
- The task is likely to hit context compaction or resume in a later turn/thread.


Do not create a ledger for:

- Simple answers, explanations, or advice.
- One-shot shell commands.
- Small single-file edits.
- Routine code review unless evidence must be tracked across many files.
- Tasks where the ledger would take longer than the work.
- Work with no meaningful resume, audit, or handoff value.

If uncertain, do not create a ledger at the start. Begin normally and create one later only if the task crosses a complexity threshold.

Use this scoring fallback when the decision is unclear. Score 1 point for each:

- More than 30 minutes expected.
- More than 5 files or 5 meaningful commands expected.
- Requires validation evidence.
- Requires preserving decisions, assumptions, or rejected paths.
- Likely to be resumed later.
- Multiple agents or threads involved.
- User or system asks for durable work state.

Create a ledger at 2+ points, or on any hard trigger. Skip it at 0-1 points.

When a ledger is used:

- Announce briefly why it is being used.
- Keep exactly one active ledger scope for the task.
- Record objective, assumptions, progress, active plan, discoveries, decisions, validation evidence, blockers, next actions, and recovery notes.
- Update it after meaningful checkpoints, plan changes, validation results, blockers, handoffs, and closeout.
- On resume, read the ledger first and reconcile it against the current workspace state before continuing.
- Do not store secrets, credentials, private keys, or unnecessary personal data.
