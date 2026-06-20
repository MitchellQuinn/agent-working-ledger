# Protocol: Update Ledger

Use this protocol after meaningful checkpoints in the active task.

## Required Triggers

Update the active ledger:

- Immediately after creating it.
- Before risky or broad changes.
- After each meaningful checkpoint.
- After discoveries that change the plan.
- After failed validation.
- After successful validation.
- Before stopping, pausing, compacting context, or handing off.
- At completion.

## Consistency Rules

- If a decision changes the plan, update both `Decision log` and `Active plan`.
- If a test fails, update both `Validation evidence` and `Next actions`.
- If an assumption is invalidated, update `Assumptions`, `Discoveries`, and
  possibly `Active plan`.
- If work is partially complete, split progress items rather than marking them
  complete.
- If validation becomes stale, mark it `Stale`.
- If blocked, set lifecycle state to `Blocked` and record the recovery path.

## Postconditions

- `ledger.md` remains internally consistent.
- Progress, next actions, and validation status reflect actual state.
- Another agent can safely resume from the ledger.

