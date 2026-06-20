# Working Ledger Owner

Ledger owner ID: parallel-subagent
Owner source: generated-id
Agent runtime: example-subagent
Created: 20260620T160500Z
Created by: example-subagent
Scope path: examples/parallel-subagents/parallel-subagent
Primary ledger: ledger.md

## Ownership rule

This ledger scope belongs to the agent thread or assigned continuation
explicitly identified above.

Agents must not update this scope unless:

1. They created it.
2. The user explicitly directed them to use it.
3. A wrapper or project instruction explicitly assigned it.

Agents must not update unrelated working-ledger scopes merely because they
exist.
