# Protocol: Record Decision

Use this protocol when the agent chooses between meaningful alternatives.

## Inputs

- Active ledger scope
- Decision
- Rationale
- Alternatives considered
- Consequences
- Date/time and author or agent

## Preconditions

- A single active ledger scope exists.
- Reversing the choice would affect architecture, implementation approach,
  validation strategy, dependency choice, file organization, user-facing
  behavior, project risk, maintainability, or handoff safety.

## Steps

1. Add the decision to `Decision log`.
2. Record why the choice was made.
3. Record meaningful alternatives considered.
4. Record consequences for implementation, validation, or future continuation.
5. Update `Active plan`, `Progress`, `Next actions`, and `Blockers and risks`
   when the decision changes them.

## Failure Behaviour

If a decision was made earlier but only discovered later, record it with the best
available date/author context and note that it is being backfilled.

## Postconditions

- Meaningful decisions are not hidden in prose-only notes.
- The current plan reflects the chosen approach.
