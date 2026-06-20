## Agent Working Ledger

For long-running, multi-step, exploratory, interruptible, validation-heavy, or
handoff-prone tasks, use the Agent Working Ledger skill.

Each agent thread must work inside exactly one active ledger scope under
`working-ledger/`.

If the user gives an existing ledger scope, use that. Otherwise create a new
scope for this thread.

Do not write to unrelated ledger scopes merely because they exist.

Keep the active ledger updated with progress, discoveries, decisions, validation
evidence, blockers, next actions, and recovery notes.

A plan records intended work. The working ledger records actual execution state.

