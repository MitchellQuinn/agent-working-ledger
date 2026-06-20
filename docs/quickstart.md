# Quickstart

Use Agent Working Ledger for work that may need to be resumed, reviewed, audited,
or handed off.

## Create a New Ledger

1. Decide that the task warrants a ledger.
2. Create a unique owner ID.
3. Create this structure:

```text
working-ledger/<ledger-owner-id>/
  OWNER.md
  ledger.md
  evidence/
  notes/
```

4. Fill `OWNER.md` from [../templates/OWNER.md.template](../templates/OWNER.md.template).
5. Fill `ledger.md` from [../templates/ledger.md.template](../templates/ledger.md.template).
6. Record the active scope path in the agent response.

## Resume From a Ledger

1. Use only the scope explicitly supplied by the user or wrapper.
2. Read `OWNER.md`.
3. Read `ledger.md`.
4. Read `handoff.md` if present.
5. Check validation freshness, blockers, next actions, and recovery notes.
6. Repair inconsistencies in the active ledger before continuing.

## Close a Ledger

Close a ledger only when the task or milestone is actually complete, abandoned,
or intentionally stopped. Update validation status, remaining risks, next
actions, recovery notes, and the outcome / retrospective.

