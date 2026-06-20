# Handoff

Active ledger: examples/handoff
Ledger owner ID: handoff
Lifecycle state: Blocked
Last updated: 20260620T143000Z

## Current objective

Pause the task with enough state for a later agent to continue.

## Current state

Implementation is blocked on a missing environment detail.

## Files touched

- Example files only.

## Do next

1. Ask user for the missing environment detail.
2. Resume implementation after the value is known.

## Do not redo

- Do not redo the initial target-file inspection.

## Known traps

- Do not guess the missing environment detail.

## Validation status

- Partially Verified.

## Resume command/checks

- `python -m tools.awl check examples/handoff`
