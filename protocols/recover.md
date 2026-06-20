# Protocol: Recover

Use this protocol at the start of a resumed work segment.

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
12. Repair the active ledger before proceeding if inconsistencies are found.

## Boundary

Do not repair ledgers outside the active ledger scope unless the user explicitly
asks for an audit or repair.

