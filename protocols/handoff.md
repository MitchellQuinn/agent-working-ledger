# Protocol: Handoff

Use this protocol when another agent or human may need to continue the task.

## Inputs

- Active ledger scope
- Current task state
- Known continuation audience, if any

## Preconditions

- `ledger.md` is current enough to be the task-state authority.
- The handoff note will summarize rather than replace the ledger.

## Steps

1. Update `ledger.md` first.
2. Create or update `handoff.md` when a compressed continuation note is useful.
3. Include the active scope ID as a standalone, copyable fragment, plus the
   active ledger path, lifecycle state, and last updated time.
4. Summarize current objective and current state.
5. List files touched or important files to inspect.
6. List immediate next actions.
7. List work that should not be redone.
8. List known traps, blockers, stale validation, and assumptions to re-check.
9. List resume commands or checks.

## Failure Behaviour

If the ledger is outdated, repair `ledger.md` before writing `handoff.md`. If
the handoff would expose secrets or sensitive details, summarize or redact them.

## Postconditions

- Another agent or human can resume from `ledger.md` and `handoff.md`.
- The continuation audience can copy the scope ID without extracting it from a
  path.
- `handoff.md` does not contain authoritative state absent from `ledger.md`.
