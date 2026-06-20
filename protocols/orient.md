# Protocol: Orient

Use this protocol after creation or adoption when repository or task context must
be inspected before planning or implementation.

## Inputs

- Active ledger scope
- User objective
- Repository, issue, plan, or task context

## Preconditions

- A single active ledger scope has been created, adopted, or explicitly
  assigned.
- Orientation can be performed without implementation changes.

## Steps

1. Inspect relevant files, instructions, plans, tests, issue descriptions, or
   previous outputs.
2. Record confirmed and unconfirmed assumptions.
3. Record discovered constraints, risks, and repo facts.
4. Update `Current state summary`.
5. Update `Next actions`.
6. Update lifecycle state to `Oriented` when enough context exists to plan.

## Failure Behaviour

If orientation finds conflicting instructions or missing context that materially
changes scope, record the uncertainty in `Assumptions`, `Blockers and risks`,
and `Next actions`, then ask the user only for decisions that cannot be derived
from the repo.

## Postconditions

- Relevant context is captured in `ledger.md`.
- The agent has not made implementation changes without needed orientation.
- The ledger states what is known, what remains uncertain, and what should
  happen next.
