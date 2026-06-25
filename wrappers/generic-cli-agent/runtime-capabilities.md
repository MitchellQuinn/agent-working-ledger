# Generic CLI Agent Runtime Capabilities

This document describes wrapper assumptions. It does not redefine the core
Agent Working Ledger schema or ownership model.

Status for this release: this is generic prompt material for runtimes that can
read and write project files. Runtime-specific compatibility is not claimed.

| Capability | Status |
| --- | --- |
| Exposes session/thread ID | Unknown; use one when the runtime provides it. |
| Can create files | Required for this wrapper to be useful. |
| Can read project files | Required for create, adopt, recover, and handoff workflows. |
| Can run shell commands | Runtime-dependent. |
| Can run tests | Runtime-dependent. |
| Supports native skills | No assumption. |
| Supports project rules | Runtime-dependent. |
| Supports subagents | Runtime-dependent. |
| Supports hooks | Runtime-dependent. |
| Persists state across sessions | Unknown; ledger files provide durable state. |

## Owner ID Pattern

Use a real session or thread ID when one exists. Otherwise mint:

```text
<UTC timestamp>-generic-agent-<short-random-nonce>
```

## Safety Constraints

The prompt wrapper must tell the agent to create or adopt exactly one active
ledger scope, update only that scope, and avoid unrelated ledgers unless the
user explicitly assigns one.
