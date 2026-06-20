# Parallel Subagents Example

This example contains two separate ledger scopes:

- `parallel-parent`
- `parallel-subagent`

The parent references the subagent by path, but the subagent maintains its own
ledger. This demonstrates contamination-resistant coordination.
