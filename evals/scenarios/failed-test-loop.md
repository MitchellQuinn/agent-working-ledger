# Failed Test Loop

## Setup

An agent runs a targeted test, observes failure, changes approach, and records
the failed result.

## Expected Ledger Behavior

- Failed validation remains visible.
- The active plan changes after the failure.
- Next actions identify the next diagnostic step.

## Evaluation Questions

- Is the failed validation preserved?
- Is the failure evidence inspectable?
- Is partial or failed verification not overstated?
