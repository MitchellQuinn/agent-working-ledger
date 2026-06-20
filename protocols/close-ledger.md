# Protocol: Close Ledger

Use this protocol when the task or milestone is complete, abandoned, or
intentionally stopped.

## Inputs

- Active ledger scope
- Final outcome or reason for stopping
- Final validation status and known remaining risks

## Preconditions

- The task or milestone is actually complete, abandoned, or intentionally
  stopped.
- Temporary pausing is handled through recovery notes, not closure.

Closing a ledger requires updating:

- Lifecycle state
- Current state summary
- Progress
- Validation evidence
- Blockers and risks
- Next actions
- Recovery notes
- Outcome / retrospective

## Steps

1. Confirm the closeout reason: completed, abandoned, partially completed, or
   intentionally stopped.
2. Set lifecycle state to `Closed`.
3. Update `Current state summary`.
4. Make progress items accurately reflect completed and remaining work.
5. Record final validation evidence or explicit non-run status.
6. Record remaining blockers, risks, and follow-up work.
7. Update `Next actions` so they do not imply hidden continuation in the closed
   ledger.
8. Update `Recovery notes`.
9. Write `Outcome / retrospective`.

## Closeout Questions

A closed ledger should answer:

- What changed?
- What now works?
- How was it verified?
- What remains?
- What risks remain?
- Does follow-up work need a new ledger?
- Was the ledger completed, abandoned, or partially completed?

## Failure Behaviour

Do not mark a ledger `Closed` merely because the agent is stopping temporarily.
Temporary stopping requires updated recovery notes, not closure.

If validation was not run, record `Not Run` with a reason and follow-up rather
than implying success. If work continues elsewhere, consider superseding instead
of closing.

## Postconditions

- Lifecycle state is `Closed`.
- Outcome or retrospective is present.
- Remaining risks and follow-up work are visible.
- No next action implies hidden continuation in the closed ledger.
