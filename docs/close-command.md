# Close Command

`awl close` closes one explicitly supplied ledger scope. It refuses to close a
schema-invalid ledger and updates only that scope.

```bash
python -m tools.awl close working-ledger/<ledger-owner-id>/ \
  --outcome "Implementation complete." \
  --validation-status Passed \
  --remaining-risks "None known." \
  --follow-up "No follow-up needed."
```

The command updates `ledger.md` and mirrors lifecycle, timestamp, and validation
status to `machine-state.json` when that sidecar exists. It must not be used for
temporary pauses; update recovery notes instead. Its output includes the
standalone scope ID as well as the updated paths.
