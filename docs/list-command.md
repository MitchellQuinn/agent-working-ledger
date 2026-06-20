# List Command

`awl list` discovers candidate ledger scopes under a root directory without
adopting or selecting one.

```bash
python -m tools.awl list --root working-ledger
python -m tools.awl list --root working-ledger --format json
```

For each direct child directory, it reports scope path, owner ID, lifecycle
state, last updated time, objective, and `awl check` status. Malformed scopes are
listed with their check error counts instead of failing the whole command.
