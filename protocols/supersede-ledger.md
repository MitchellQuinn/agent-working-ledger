# Protocol: Supersede Ledger

Use this protocol when another ledger, plan, issue, or execution path replaces
the current active ledger.

## Inputs

- Active ledger scope
- Superseding ledger, plan, issue, branch, or execution path when known
- Reason for superseding

## Preconditions

- A real replacement exists or continuation in the current ledger is no longer
  appropriate.
- The agent is updating only the active ledger unless explicitly directed
  otherwise.

## Steps

1. Set lifecycle state to `Superseded`.
2. Record what superseded the ledger, where possible.
3. Record why it was superseded.
4. Record whether any work or evidence remains useful.
5. Record where continuation should happen.
6. Update `Current state summary`, `Next actions`, `Recovery notes`, and
   `Outcome / retrospective`.

## Failure Behaviour

If the replacement path is not yet known, record the reason and mark the
continuation location as unknown. Do not keep writing task state to the
superseded ledger unless the user explicitly reactivates it.

## Postconditions

- Lifecycle state is `Superseded`.
- The ledger says what replaced it or why that is unknown.
- Future agents know not to continue writing there by default.
