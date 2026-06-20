# Debugging Loop Example

Ledger schema version: 0.3
Lifecycle State: Active
Created: 20260620T130000Z
Last updated: 20260620T133000Z
Ledger owner ID: debugging
Owner source: generated-id
Agent/runtime: example
User objective: Diagnose a failing parser test without losing failed evidence.
Ledger scope: examples/debugging
Primary ledger: examples/debugging/ledger.md
Related branch/issue/plan/ledger: Not Applicable

## Current objective

Find why the parser fixture fails and record the failed validation loop.

## Current state summary

The targeted test fails. The active hypothesis is that fixture normalization
changed.

## Assumptions

- [Unconfirmed] Parser behavior changed after fixture normalization.

## Progress

- [x] Reproduce failing test.
- [x] Capture failure evidence.
- [ ] Inspect fixture normalization.
- [ ] Implement fix.

## Active plan

Inspect fixture normalization, update the parser or fixture expectation, then
rerun the targeted test.

## Discoveries

- Observation: The parser test fails consistently.
  Evidence: See `evidence/parser-failure.txt`.
  Impact: Validation remains failed until the fixture path is fixed.

## Decision log

- Decision: Preserve the failed validation result.
  Rationale: It explains why the task is still active.
  Alternatives considered: Only record the future passing run.
  Consequences: A later agent can avoid repeating reproduction work.
  Date/Author: 20260620T132000Z / example

## Validation evidence

- Command/check: `python -m unittest tests.test_parser`
  Result: Failed
  Evidence: See `evidence/parser-failure.txt`.
  Follow-up: Inspect fixture normalization.

Overall validation status: Failed

## Blockers and risks

- Blocker/risk: Root cause is not confirmed.
  Impact: Fix may target the wrong layer.
  Next action: Inspect fixture normalization.

## Next actions

1. Inspect fixture normalization.
2. Update active plan after root cause is confirmed.

## Recovery notes

To resume safely:
1. Read this ledger.
2. Do not rerun broad tests before inspecting the targeted failure.
3. Review `evidence/parser-failure.txt`.
4. Re-check the unconfirmed assumption.

## Outcome / retrospective

Not completed yet.
