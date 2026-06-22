# Protocol: Adopt Ledger

Use this protocol only when the user explicitly points the agent at an existing
ledger scope or a wrapper assigns one.

## Inputs

- Existing ledger scope path

## Preconditions

- The user or wrapper explicitly supplied the scope.
- The scope exists or can reasonably be created at that location because the
  user supplied it.
- The agent has permission to read the scope.
- The agent has not selected the scope merely because it was newest, nearest, or
  plausible.

## Steps

1. Treat the supplied directory as the only active ledger scope.
2. Read `OWNER.md` if present.
3. Read `ledger.md`.
4. Read `handoff.md` if present and relevant.
5. Summarize current objective, lifecycle state, progress, validation status,
   blockers, next actions, and recovery notes before making changes.
6. Check for obvious internal inconsistencies.
7. Repair only the active ledger if needed and appropriate.
8. Report the adopted scope ID as a standalone, copyable fragment; also report
   the scope path when useful.
9. Continue from `Next actions` and `Recovery notes`.

## Failure Behaviour

If multiple ledgers are plausible and none was selected, stop and ask the user
to choose. Discovery is not adoption.

If required files are missing from a user-supplied scope, report what is missing
and repair only that scope.

If `OWNER.md` is missing but the user explicitly supplied the directory, create
one only after noting that ownership metadata was missing.

If the ledger is closed or superseded, do not reopen it casually. Continue only
if the user explicitly directed that, or create a new ledger that references it.

## Postconditions

- The adopted scope is active.
- The adopted scope ID has been reflected as a standalone fragment.
- Current state, next actions, risks, and validation status are understood.
- Any metadata repair is recorded.
- Unrelated ledger scopes remain untouched.
