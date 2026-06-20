# Protocol: Adopt Ledger

Use this protocol only when the user explicitly points the agent at an existing
ledger scope or a wrapper assigns one.

## Inputs

- Existing ledger scope path

## Preconditions

- The user or wrapper explicitly supplied the scope.
- The agent has permission to read the scope.

## Steps

1. Treat the supplied directory as the active ledger scope.
2. Read `OWNER.md` if present.
3. Read `ledger.md`.
4. Read `handoff.md` if present.
5. Summarize the current state before making changes.
6. Check for obvious inconsistencies.
7. Repair only the active ledger if needed and appropriate.
8. Continue from `Next actions` and `Recovery notes`.

## Failure Behaviour

If multiple ledgers are plausible and none was selected, stop and ask the user
to choose. Discovery is not adoption.

If required files are missing from a user-supplied scope, report what is missing
and repair only that scope.

## Postconditions

- The adopted scope is active.
- Current state, next actions, risks, and validation status are understood.
- Any metadata repair is recorded.

