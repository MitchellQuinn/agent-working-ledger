# Interrupted Refactor

## Setup

An agent starts a multi-file refactor, completes part of the work, updates the
ledger, and stops before completion.

## Expected Ledger Behavior

- Completed and remaining work are distinguishable.
- Files touched are listed in recovery notes.
- Validation that may be stale is marked.
- Next actions are specific enough for another agent.

## Evaluation Questions

- Can a second agent identify what not to redo?
- Does the second agent avoid unrelated ledger scopes?
- Does it rerun or review stale validation before claiming completion?
