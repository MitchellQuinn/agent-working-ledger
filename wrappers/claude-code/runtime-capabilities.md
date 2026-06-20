# Claude Code Runtime Capabilities

This document describes wrapper assumptions. It does not redefine the core
Agent Working Ledger schema or ownership model.

| Capability | Status |
| --- | --- |
| Exposes session/thread ID | Yes, `${CLAUDE_SESSION_ID}` when available. |
| Can create files | Yes, subject to normal workspace permissions. |
| Can read project files | Yes. |
| Can run shell commands | Yes, subject to normal tool permissions. |
| Can run tests | Yes, when project tooling is available. |
| Supports native skills | Yes. |
| Supports project rules | Yes, through project instruction files such as `CLAUDE.md`. |
| Supports subagents | Yes, depending on runtime configuration. |
| Supports hooks | Runtime-dependent. |
| Persists state across sessions | Chat context may not persist; ledger files do. |

## Owner ID Pattern

Use `claude-code-${CLAUDE_SESSION_ID}` when available. If a human-readable task
slug is useful, append `-<task-slug>`.

If no stable session ID is available, fall back to:

```text
<UTC timestamp>-claude-code-<short-random-nonce>
```

## Safety Constraints

Claude Code wrappers must keep the core schema intact, write only to the active
ledger scope, and avoid letting subagents write into a parent ledger unless the
user explicitly instructs that.
