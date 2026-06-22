# Supersede Command

`awl supersede` marks one explicitly supplied ledger scope as replaced by another
ledger, plan, issue, or execution path. It refuses schema-invalid ledgers and
updates only the specified scope.

```bash
python -m tools.awl supersede working-ledger/<ledger-owner-id>/ \
  --by working-ledger/<replacement-owner-id>/ \
  --reason "Replacement scope has clearer ownership."
```

The command records the replacement target, reason, useful remaining work or
evidence, and continuation location. It updates `machine-state.json` when that
sidecar exists. Its output includes the standalone scope ID as well as the
updated paths.
