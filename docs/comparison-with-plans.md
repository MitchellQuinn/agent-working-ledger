# Comparison With Plans

A plan records intended work.

A working ledger records actual execution state.

Plans are allowed to be wrong. They can be revised, replaced, or discarded as
the task evolves. A ledger must not be knowingly wrong. When discoveries change
the approach, the ledger must update the active plan, assumptions, discoveries,
decisions, validation status, and next actions as needed.

## Boundaries

| Artifact | Purpose |
| --- | --- |
| Plan | Intended approach |
| Working ledger | Actual execution state |
| Evidence | Proof, observations, logs, command output, screenshots, or manual checks |
| Handoff note | Compressed continuation summary |
| Issue tracker | Project-level work item or backlog |
| Source control | History of source changes |

The ledger is task-local and operational. It is not a project-management system,
permanent architecture record, or replacement for tests.

## Practical Rule

Keep the plan and ledger synchronized only where they overlap. If investigation
invalidates the plan, revise the ledger's `Active plan` section and record the
discovery or decision that caused the change.

Do not preserve obsolete intended work in the active plan just because it was the
original plan. Preserve obsolete context in discoveries, decisions, notes, or
handoff material instead.
