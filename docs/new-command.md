# New Ledger Command

`awl new` creates one fresh working-ledger scope. It is intentionally narrow:
it does not adopt, repair, close, supersede, or inspect unrelated ledgers.

Run without installing:

```bash
python -m tools.awl new "Task title"
```

Run after installing the package:

```bash
awl new "Task title"
```

Useful options:

```bash
python -m tools.awl new "OAuth refresh fix" --slug oauth-refresh-fix
python -m tools.awl new "OAuth refresh fix" --runtime codex
python -m tools.awl new "OAuth refresh fix" --root working-ledger
python -m tools.awl new "OAuth refresh fix" --handoff --machine-state
python -m tools.awl new "OAuth refresh fix" --owner-id codex-session-123
```

## Behavior

- Creates `OWNER.md`, `ledger.md`, `evidence/`, and `notes/`.
- Optionally creates `handoff.md` and `machine-state.json`.
- Generates an owner ID when one is not supplied.
- Uses `generated-id` owner source for generated IDs.
- Uses `user-assigned` owner source for explicit `--owner-id` unless
  `--owner-source` is supplied.
- Requires explicit owner IDs to be safe single path segments.
- Refuses to overwrite an existing scope.
- Prints the standalone `scope_id` and created paths as text or JSON.

## Invariant

A scope created by `awl new` should pass:

```bash
python -m tools.awl check working-ledger/<ledger-owner-id>/
```
