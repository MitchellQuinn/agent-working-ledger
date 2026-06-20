# Protocol: Create Ledger

Use this protocol when a task triggers Agent Working Ledger and no existing
active ledger scope was supplied.

## Inputs

- Task title
- User objective
- Optional task slug
- Optional root directory
- Optional owner ID and owner source
- Optional agent runtime
- Optional related branch, issue, plan, or previous ledger

## Preconditions

- The task is long-running, multi-step, exploratory, validation-heavy,
  interruption-prone, or handoff-prone.
- The user has not directed the agent to use an existing ledger.
- The agent has permission to create files.

## Steps

1. Create `working-ledger/` if needed.
2. Determine the ledger owner ID.
3. Create `working-ledger/<ledger-owner-id>/`.
4. Create `OWNER.md`.
5. Create `ledger.md` from the template.
6. Create `evidence/`.
7. Create `notes/`.
8. Optionally create `handoff.md`.
9. Optionally create `machine-state.json`.
10. Report the scope path to the user.
11. Continue using only that scope.

## Postconditions

- A valid ledger scope exists.
- Ownership is explicit.
- Lifecycle state is `Created`.
- Required ledger sections exist.
- The next action is clear.

