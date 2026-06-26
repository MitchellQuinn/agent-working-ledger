# Assets Command

`awl assets` locates the Agent Working Ledger release assets available to the
current CLI.

Run from a source checkout:

```bash
python -m agent_working_ledger assets
```

Run after installing the package:

```bash
awl assets
```

JSON output is available:

```bash
awl assets --format json
```

The command reports the asset root and key subpaths for the specification,
protocols, templates, skill package, wrappers, documentation, examples, and
evaluation material. It exits nonzero if required release assets are missing.

