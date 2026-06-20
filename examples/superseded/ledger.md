# Superseded Ledger Example

Ledger schema version: 0.3
Lifecycle State: Superseded
Created: 20260620T150000Z
Last updated: 20260620T151500Z
Ledger owner ID: superseded
Owner source: generated-id
Agent/runtime: example
User objective: Demonstrate a replaced execution path.
Ledger scope: examples/superseded
Primary ledger: examples/superseded/ledger.md
Related branch/issue/plan/ledger: examples/feature-implementation

## Current objective

Demonstrate how a ledger records supersession.

## Current state summary

Superseded by: examples/feature-implementation

Reason: The replacement ledger has the current execution path.

## Assumptions

- [Superseded] This ledger is no longer the active continuation path.

## Progress

- [x] Record supersession reason.
- [x] Name the replacement path.

## Active plan

Do not continue task-state writes here unless the user explicitly reactivates
this scope.

## Discoveries

- Observation: Another scope replaced this one.
  Evidence: User-selected continuation path.
  Impact: Future writes should happen elsewhere.

## Decision log

- Decision: Mark this ledger superseded.
  Rationale: Prevent stale continuation.
  Alternatives considered: Leave both scopes active.
  Consequences: Agents should continue in the replacement path.
  Date/Author: 20260620T151500Z / example

## Validation evidence

- Command/check: Supersession review
  Result: Not Applicable
  Evidence: This example records workflow state rather than implementation.
  Follow-up: Continue in the replacement path.

Overall validation status: Not Applicable

## Blockers and risks

- Blocker/risk: Agents may accidentally continue here.
  Impact: Task state could fragment.
  Next action: Continue in examples/feature-implementation.

## Next actions

1. Continue in examples/feature-implementation.

## Recovery notes

This ledger was superseded.

Superseded by: examples/feature-implementation

Reason: The replacement ledger has the current execution path.

## Outcome / retrospective

Superseded by: examples/feature-implementation

Useful remaining work or evidence: Decision log explains why this scope stopped.

Continuation: examples/feature-implementation
