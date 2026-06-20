# Lifecycle Model

Agent Working Ledger uses explicit lifecycle states so another agent or human can
tell where a task stands without reconstructing the chat.

## States

| State | Meaning |
| --- | --- |
| `Created` | Initial task framing and assumptions are recorded. |
| `Oriented` | Relevant repo context, task context, files, or constraints have been inspected. |
| `Planned` | The current executable approach is written down. |
| `Active` | Progress, findings, decisions, and validation are being updated as work proceeds. |
| `Blocked` | Progress cannot safely continue; blocker and recovery options are recorded. |
| `Ready for Review` | A task milestone appears complete and validation evidence has been recorded. |
| `Closed` | Final outcome, remaining risks, and follow-up work are recorded. |
| `Superseded` | Another ledger, plan, issue, or execution path has replaced this one. |

The lifecycle state must be visible near the top of `ledger.md`.

## Allowed Transitions

```text
Created
  -> Oriented
  -> Planned
  -> Active
       -> Blocked -> Active
       -> Ready for Review -> Active
       -> Ready for Review -> Closed
       -> Closed
       -> Superseded
```

Any non-closed state may move to `Superseded` when another execution path
replaces the ledger.

Agents should avoid skipping states unless the task genuinely moves quickly
through them. A short but still ledger-worthy task may move from `Created` to
`Active`, but orientation and planning detail still belongs in the appropriate
sections.

Closed ledgers should not be reopened casually. If work continues after closure,
create a new ledger that references the closed one, mark the old ledger as
superseded, or continue only when the user explicitly directs reopening.
