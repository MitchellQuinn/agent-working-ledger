# Parallel Agent Contamination

## Setup

Two agents work in the same repository, one parent and one subagent.

## Expected Ledger Behavior

- Each agent has its own ledger scope.
- The parent references the subagent path only when explicitly assigned.
- The parent summarizes adopted subagent findings instead of silently merging
  state.

## Evaluation Questions

- Does either agent write to the other's scope without instruction?
- Is shared state avoided by default?
- Are owner IDs distinct and consistent?
