---
name: agent-working-ledger
description: Maintain a session-specific working ledger for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone work. Uses the active Claude Code session ID when available to create or adopt one ledger scope under working-ledger/. Do not write to unrelated ledger scopes unless the user explicitly provides one.
argument-hint: "[optional-existing-ledger-scope-or-task-title]"
---

# Claude Code Wrapper

Use the core Agent Working Ledger standard without changing the schema or
ownership model.

Recommended owner ID when `${CLAUDE_SESSION_ID}` is available:

```text
claude-code-${CLAUDE_SESSION_ID}
```

If a human-readable slug is useful, append it:

```text
claude-code-${CLAUDE_SESSION_ID}-<task-slug>
```

Create:

```text
working-ledger/<owner-id>/
  OWNER.md
  ledger.md
  evidence/
  notes/
```

Do not update unrelated `working-ledger/*/` scopes unless the user explicitly
names one.

