# Codex Runtime Capabilities

This document describes wrapper assumptions. It does not redefine the core
Agent Working Ledger schema or ownership model.

| Capability | Status |
| --- | --- |
| Exposes session/thread ID | Use a Codex-provided session or conversation ID if available. |
| Can create files | Yes, subject to workspace permissions. |
| Can read project files | Yes. |
| Can run shell commands | Yes, subject to tool permissions. |
| Can run tests | Yes, when project tooling is available. |
| Supports native skills | Environment-dependent. |
| Supports project rules | Yes, through project instruction files such as `AGENTS.md`. |
| Supports subagents | Environment-dependent. |
| Supports hooks | Environment-dependent. |
| Persists state across sessions | Chat context may not persist; ledger files do. |

## Owner ID Pattern

Use `codex-<session-id>` when a stable session or conversation ID is available.
Otherwise mint:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

Record whether the owner ID came from a session ID or was generated.

## Safety Constraints

Codex wrappers must treat project instructions as invocation material, not as a
replacement for the core standard. Write only to the active ledger scope unless
the user explicitly provides another one.
