---
name: agent-working-ledger
description: Maintain a task-local working ledger for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone Codex work. Creates or adopts one ledger scope under working-ledger/ and keeps progress, discoveries, decisions, validation evidence, blockers, next actions, and recovery notes current. Do not write to unrelated ledger scopes unless the user explicitly provides one.
---

# Codex Wrapper

Use the core Agent Working Ledger standard without changing the schema or
ownership model.

Use a Codex-provided session or conversation ID if one is available. If no stable
ID is available, mint an owner ID:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

Create:

```text
working-ledger/<owner-id>/
  OWNER.md
  ledger.md
  evidence/
  notes/
```

Optional files are `handoff.md` and `machine-state.json` when useful. Use
`schema_version: "0.3"` for optional machine state because it tracks the ledger
schema/spec iteration, not the package release.

Record whether the owner ID came from a session ID or was generated. Treat
project instructions such as `AGENTS.md` as wrapper-level invocation material,
not a replacement for the core standard.

Do not update other ledger scopes unless the user explicitly names one.
