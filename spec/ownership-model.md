# Ownership Model

Agent Working Ledger uses explicit ownership to prevent unrelated agent threads
from contaminating each other's task state.

## Active Scope

Each agent thread owns exactly one active working-ledger scope unless the user
explicitly directs it to use an existing one.

An agent may write to a ledger scope only when:

1. It created the scope in the current thread.
2. The user explicitly directed it to use that scope.
3. A wrapper or project instruction explicitly assigned that scope.

## Scope Path

The default scope path is:

```text
working-ledger/<ledger-owner-id>/
```

The `<ledger-owner-id>` path segment is also the standalone scope ID agents
should reflect back separately from the path.

The root `working-ledger/` directory is a container, not a shared working-memory
file.

## Owner Marker

Every scope must contain `OWNER.md`. It records the ledger owner ID, owner
source, runtime, creation timestamp, scope path, and ownership rule.

Before writing to a scope, an agent should read `OWNER.md` and confirm that the
scope is active for the current work.

## Adoption

Existing ledgers are discoverable artifacts, not automatically adoptable memory.
If multiple ledgers exist and the user has not identified one, the agent must
not guess. It may list candidates and ask the user to choose.
