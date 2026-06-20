# Quickstart

Use Agent Working Ledger for work that may need to be resumed, reviewed, audited,
or handed off.

This repository is preparing package release `0.1.0`. The ledger schema follows
source specification iteration `v0.3`.

## Create a New Ledger

Using the helper tool:

```bash
python -m tools.awl new "Task title" --slug task-title
```

Using only the templates:

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
6. Optionally add `handoff.md`, `machine-state.json`, or an evidence README
   from the templates when useful.
7. Record the active scope path in the agent response.
8. Continue writing task state only inside that scope.

The helper tool creates `OWNER.md`, `ledger.md`, `evidence/`, and `notes/` and
refuses to overwrite an existing scope. Use `--handoff` or `--machine-state` to
create optional sidecars.

Check or summarize the scope:

```bash
python -m tools.awl check working-ledger/<ledger-owner-id>/
python -m tools.awl summarize working-ledger/<ledger-owner-id>/
```

## Work The Ledger

Update `ledger.md` after meaningful checkpoints:

- progress changes
- discoveries that affect the plan
- decisions between meaningful alternatives
- validation failures or passes
- pauses, handoffs, closeout, or supersession

When a discovery changes the approach, update the active plan as well as the
discovery or decision entry. When validation may have been invalidated by later
changes, mark it `Stale`.

## Resume From a Ledger

1. Use only the scope explicitly supplied by the user or wrapper.
2. Read `OWNER.md`.
3. Read `ledger.md`.
4. Read `handoff.md` if present.
5. Check validation freshness, blockers, next actions, and recovery notes.
6. Repair inconsistencies in the active ledger before continuing.

## Handoff

1. Update `ledger.md` first.
2. Create or refresh `handoff.md` when a compressed continuation note is useful.
3. Include the active ledger path, current objective, current state, files
   touched, next actions, work not to redo, traps, validation status, and resume
   checks.
4. Keep `ledger.md` as the authority; the handoff note is only a summary.

## Close a Ledger

Close a ledger only when the task or milestone is actually complete, abandoned,
or intentionally stopped. Update validation status, remaining risks, next
actions, recovery notes, and the outcome / retrospective.

Do not close a ledger merely because the agent is pausing. For temporary stops,
update recovery notes and leave the lifecycle state accurate.

The helper command can close an explicit scope:

```bash
python -m tools.awl close working-ledger/<ledger-owner-id>/ \
  --outcome "Task complete." \
  --validation-status Passed \
  --remaining-risks "None known." \
  --follow-up "No follow-up needed."
```
