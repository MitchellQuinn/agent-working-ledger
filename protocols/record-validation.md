# Protocol: Record Validation

Use this protocol whenever the agent runs, reviews, intentionally skips, or
invalidates a validation check.

## Inputs

- Active ledger scope
- Command or manual check
- Result status
- Evidence
- Follow-up, if needed

## Preconditions

- A single active ledger scope exists.
- The result status is one of `Not Run`, `Failed`, `Passed`,
  `Partially Verified`, `Stale`, or `Not Applicable`.

## Steps

1. Add an entry to `Validation evidence`.
2. Record the command/check exactly enough to repeat or understand it.
3. Record the approved result status.
4. Include concise evidence or a path under `evidence/`.
5. Record follow-up for failed, partial, stale, or not-run checks.
6. Update `Current state summary`, `Progress`, `Blockers and risks`, and
   `Next actions` when validation changes task state.

## Failure Behaviour

If output is large, write a concise summary to the ledger and store the full
redacted output in `evidence/`. If output contains secrets or sensitive data,
redact before recording or store only a safe summary.

If later changes may invalidate a previous pass, add or update an entry with
`Stale` rather than leaving the old result as the current validation claim.

## Postconditions

- Validation claims are backed by evidence or an explicit non-run status.
- Failed and stale validation results remain visible.
