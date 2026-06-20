# Protocol: Record Discovery

Use this protocol when the agent learns something that affects the task.

## Inputs

- Active ledger scope
- Observation
- Evidence
- Impact on current work

## Preconditions

- A single active ledger scope exists.
- The discovery is relevant to the current task, plan, validation, risk, or
  recovery state.

## Steps

1. Add a concise entry to `Discoveries`.
2. Include evidence such as a file path, command output summary, test result,
   evidence path, or manual observation.
3. State the impact on the task.
4. Update `Assumptions` when the discovery confirms, invalidates, or supersedes
   an assumption.
5. Update `Active plan`, `Next actions`, and `Blockers and risks` when the
   discovery changes the approach.
6. Mark validation as `Stale` when later work may have invalidated it.

## Failure Behaviour

If the evidence includes secrets or sensitive data, redact or summarize before
recording it. If the discovery depends on uncertain interpretation, mark the
related assumption as `Unconfirmed`.

## Postconditions

- The ledger records what changed in the agent's understanding.
- The active plan and next actions do not contradict the discovery.
