# Protocol: Update Ledger

Use this protocol after meaningful checkpoints in the active task.

## Inputs

- Active ledger scope
- New progress, discovery, decision, validation result, blocker, risk, or
  recovery information

## Preconditions

- A single active ledger scope exists.
- The agent has confirmed it may write to that scope.
- The update reflects actual task state, not aspirational progress.

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

## Required Updates

Update every affected section, not only the section where the new fact first
appears. Keep `Last updated` current.

## Steps

1. Read the current `ledger.md`.
2. Identify all sections affected by the new information.
3. Update lifecycle state when task state changed.
4. Update progress, active plan, discoveries, decisions, validation, blockers,
   next actions, and recovery notes as applicable.
5. Mark stale validation when later changes may have invalidated previous
   evidence.
6. Re-read the changed ledger for internal consistency.

## Consistency Rules

- If a decision changes the plan, update both `Decision log` and `Active plan`.
- If a test fails, update both `Validation evidence` and `Next actions`.
- If an assumption is invalidated, update `Assumptions`, `Discoveries`, and
  possibly `Active plan`.
- If work is partially complete, split progress items rather than marking them
  complete.
- If validation becomes stale, mark it `Stale`.
- If blocked, set lifecycle state to `Blocked` and record the recovery path.
- If the agent changes ledger scope, record why and who directed the change.

## Failure Behaviour

If the ledger appears inconsistent with actual repository state, repair the
active ledger before proceeding. Do not repair unrelated ledgers unless the user
explicitly asks for an audit or repair.

## Postconditions

- `ledger.md` remains internally consistent.
- Progress, next actions, and validation status reflect actual state.
- Another agent can safely resume from the ledger.
