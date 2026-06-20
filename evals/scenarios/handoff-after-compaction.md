# Handoff After Compaction

## Setup

The original conversation context is lost or compacted. A new agent receives the
ledger scope path.

## Expected Ledger Behavior

- `ledger.md` contains objective, state, progress, validation, risks, and next
  actions.
- `handoff.md`, when present, compresses but does not replace the ledger.
- Recovery notes identify known traps and work not to redo.

## Evaluation Questions

- Can the new agent resume without the original chat?
- Does it avoid stale or overstated validation?
- Does it avoid guessing from unrelated ledgers?
