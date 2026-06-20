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

- The task triggers Agent Working Ledger.
- The user has not directed the agent to use an existing ledger.
- The agent has permission to create files.
- The agent will use only one active ledger scope for task-state writes.

## Steps

1. Create `working-ledger/` if needed.
2. Determine the ledger owner ID from a runtime session/thread ID when
   available, otherwise mint `<UTC timestamp>-<agent-slug>-<short-random-nonce>`.
3. Create `working-ledger/<ledger-owner-id>/`.
4. Create `OWNER.md`.
5. Create `ledger.md` from the template.
6. Create `evidence/`.
7. Create `notes/`.
8. Optionally create `handoff.md`.
9. Optionally create `machine-state.json`.
10. Record the current objective, initial assumptions, first progress items,
    active plan or orientation step, next actions, and recovery notes.
11. Report the active scope path to the user.
12. Continue using only that scope.

## Failure Behaviour

If the scope path already exists for the chosen owner ID, do not overwrite it
blindly. Read `OWNER.md` if present and either adopt only when explicitly safe or
mint a new owner ID.

If file creation fails, report the missing artifact and do not claim the ledger
is active until `OWNER.md`, `ledger.md`, `evidence/`, and `notes/` exist.

## Postconditions

- A valid ledger scope exists.
- Ownership is explicit.
- Lifecycle state is `Created`.
- Required ledger sections exist.
- The next action is clear.
- The active scope path is known to the user.
