# Read-Only Checker

`awl check` validates one explicitly supplied ledger scope and reports the
standalone scope ID with the scope path. It is intentionally read-only and must
not adopt, repair, close, supersede, or mutate ledgers.

Run without installing:

```bash
python -m agent_working_ledger check working-ledger/<ledger-owner-id>/
```

Run after installing the package:

```bash
awl check working-ledger/<ledger-owner-id>/
```

JSON output is available:

```bash
python -m agent_working_ledger check working-ledger/<ledger-owner-id>/ --format json
```

## Checks

- Required `OWNER.md`, `ledger.md`, `evidence/`, and `notes/`.
- Owner ID consistency across scope path, `OWNER.md`, `ledger.md`, and optional
  `machine-state.json`.
- Required `ledger.md` headings.
- `Last updated` is present and concrete.
- `Progress` contains checkbox items.
- `Next actions` and `Decision log` are not empty.
- Valid lifecycle state.
- Valid validation statuses.
- Validation evidence entries include command/check, result, evidence, and
  follow-up structure.
- Closed ledgers include an outcome or retrospective.
- Superseded ledgers name what replaced them where possible.
- Optional `machine-state.json` parses and does not obviously conflict with
  `ledger.md`.

## Exit Codes

- `0`: no errors.
- `1`: one or more errors.
- `2`: command-line usage error from `argparse`.

Warnings do not make the command fail. They identify issues that may be
acceptable but should be reviewed.
