# Protocol: Recover

Use this protocol at the start of a resumed work segment.

## Inputs

- Explicitly supplied, created, or wrapper-assigned active ledger scope
- Current repository state

## Preconditions

- The agent knows which ledger scope is active.
- The agent is not guessing from unrelated ledgers.

## Steps

1. Confirm the active ledger scope.
2. Read `OWNER.md`.
3. Read `ledger.md`.
4. Read `handoff.md` if present.
5. Check whether lifecycle state matches actual repository state.
6. Check whether listed next actions are still valid.
7. Check whether the active plan conflicts with newer discoveries.
8. Check whether validation evidence is stale.
9. Check whether progress overstates completion.
10. Check whether files mentioned in the ledger still exist.
11. Check whether files changed unexpectedly.
12. Reflect the active scope ID as a standalone, copyable fragment; also report
    the scope path when useful.
13. Repair the active ledger before proceeding if inconsistencies are found.

## Failure Behaviour

Do not repair ledgers outside the active ledger scope unless the user explicitly
asks for an audit or repair.

If multiple ledgers are plausible and none was explicitly supplied, stop and ask
the user to choose. Listing candidates is not adoption.

## Postconditions

- The agent understands current objective, progress, validation status,
  blockers, next actions, and recovery notes.
- The active scope ID has been reflected as a standalone fragment.
- Any repair is recorded in the active ledger.
- The active plan is safe to continue or the blocker is explicit.
