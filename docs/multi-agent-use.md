# Multi-Agent Use

Agent Working Ledger is contamination-resistant by default: each independent
agent thread, subagent, fork, background worker, or parallel agent should have
its own ledger scope unless the user explicitly assigns it to an existing one.

## Parent And Subagent Pattern

The parent agent owns its own active ledger scope. A subagent should usually do
one of three things:

1. Return a concise summary to the parent, which updates the parent ledger.
2. Create and maintain its own ledger scope, then provide the standalone scope
   ID and path to the parent.
3. Write a bounded `handoff.md` in its own scope for later review.

A subagent should not directly write into the parent ledger unless explicitly
instructed.

## Parallel Work

Parallel agents should use separate owner IDs and separate scopes:

```text
working-ledger/<parent-owner-id>/
working-ledger/<subagent-owner-id>/
working-ledger/<parallel-agent-owner-id>/
```

The parent ledger may reference subagent ledger paths, but it should summarize
what was adopted. It must not silently merge subagent state.

## Shared State

There is no default shared ledger mode in v0.1. The root `working-ledger/`
directory is a container for isolated scopes.

Only create cross-ledger files, such as `working-ledger/INDEX.md`, when the user
explicitly asks for shared coordination or review material. Mark those files as
human-requested shared state.

## Handoff

For handoff between agents:

1. Update the active `ledger.md`.
2. Create or refresh `handoff.md` if a compressed summary is useful.
3. Pass the standalone scope ID and ledger scope path explicitly to the next
   agent.
4. The next agent adopts only that supplied scope.
