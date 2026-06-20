# Summarize Command

`awl summarize` reads one explicitly supplied ledger scope and emits a compact
continuation summary. It does not adopt, repair, close, supersede, or mutate
ledgers.

```bash
python -m tools.awl summarize working-ledger/<ledger-owner-id>/
python -m tools.awl summarize working-ledger/<ledger-owner-id>/ --format json
```

The summary includes owner ID, lifecycle state, last updated time, objective,
current state, next actions, blockers and risks, validation status, validation
evidence, recovery notes, and whether a handoff note is present.
