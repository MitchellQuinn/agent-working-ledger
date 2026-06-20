# Handoff Example

Ledger schema version: 0.3
Lifecycle State: Blocked
Created: 20260620T140000Z
Last updated: 20260620T143000Z
Ledger owner ID: handoff
Owner source: generated-id
Agent/runtime: example
User objective: Pause safely after partial implementation.
Ledger scope: examples/handoff
Primary ledger: examples/handoff/ledger.md
Related branch/issue/plan/ledger: Not Applicable

## Current objective

Pause the task with enough state for a later agent to continue.

## Current state summary

Implementation started but is blocked on a missing environment detail.

## Assumptions

- [Unconfirmed] The missing detail is available from the user.

## Progress

- [x] Inspect the target files.
- [x] Start implementation.
- [ ] Confirm environment detail.
- [ ] Complete implementation.

## Active plan

Ask for the missing environment detail, then resume implementation from the
listed next actions.

## Discoveries

- Observation: The implementation depends on an environment detail not present
  in the repo.
  Evidence: Manual inspection notes.
  Impact: The task is blocked.

## Decision log

- Decision: Stop and write a handoff note.
  Rationale: Continuing would require guessing.
  Alternatives considered: Continue with a guessed value.
  Consequences: Future work resumes from explicit next actions.
  Date/Author: 20260620T142500Z / example

## Validation evidence

- Command/check: Manual review of partial implementation
  Result: Partially Verified
  Evidence: Partial implementation inspected.
  Follow-up: Run task-specific tests after the blocker is resolved.

Overall validation status: Partially Verified

## Blockers and risks

- Blocker/risk: Missing environment detail.
  Impact: Implementation cannot safely continue.
  Next action: Ask user for the value.

## Next actions

1. Ask user for the missing environment detail.
2. Resume implementation after the value is known.

## Recovery notes

To resume safely:
1. Read this ledger.
2. Read `handoff.md`.
3. Do not guess the missing environment detail.
4. Re-run validation after implementation resumes.

## Outcome / retrospective

Not completed yet.
