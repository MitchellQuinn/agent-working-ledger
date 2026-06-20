# Stale Assumption

## Setup

An agent records an assumption, later discovers it is invalid, and must update
the ledger.

## Expected Ledger Behavior

- The assumption is marked `Invalidated` or `Superseded`.
- The discovery records evidence and impact.
- The active plan and next actions are revised.

## Evaluation Questions

- Can another agent see why the approach changed?
- Does stale validation remain marked as current?
- Are recovery notes updated with what to re-check?
