# Validation And Evidence Model

Validation claims must be proportional to recorded evidence. A ledger must never
claim work is verified without command output, manual check notes, evidence
references, or an explicit non-run status.

## Validation Statuses

| Status | Meaning |
| --- | --- |
| `Not Run` | The check has not been run. |
| `Failed` | The check was run and failed. |
| `Passed` | The check was run and passed for the repository state that existed then. |
| `Partially Verified` | The check gives useful evidence but does not cover the full claim. |
| `Stale` | A previous pass or partial pass may have been invalidated by later changes. |
| `Not Applicable` | The check does not apply. |

Every validation entry should include the command or check, result, evidence,
and follow-up.

## Evidence

Evidence may include command output, test output, linter output, build output,
benchmark results, screenshots, generated diffs, manual inspection notes, local
file links, generated reports, or before/after samples.

Large evidence belongs in `evidence/`. The ledger should contain a short summary
and path.

Example:

```markdown
- Command/check: `pytest`
  Result: Failed
  Evidence: See `evidence/20260620T151233Z-pytest-failure.log`.
  Follow-up: Investigate parser fixture failure.
```

Evidence must not contain secrets, credentials, tokens, private keys, API keys,
passwords, unnecessary personal data, or sensitive production data. Summarize or
redact risky output before recording it.
