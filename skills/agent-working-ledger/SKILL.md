---
name: agent-working-ledger
description: Use for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone agentic work. Creates or adopts exactly one task-local working-ledger scope, then maintains a Markdown ledger recording progress, discoveries, decisions, validation evidence, blockers, next actions, and recovery state. Each agent thread must write only to its active ledger scope unless the user explicitly directs it to use an existing one. Do not use for simple one-shot tasks.
---

# Agent Working Ledger

Use this skill when work is complex enough that durable execution state is more
valuable than the overhead of maintaining it.

## Core Rule

Each agent thread works inside exactly one active ledger scope. Write only inside
that scope unless the user explicitly directs you to use another one.

Default root:

```text
working-ledger/
```

Default scope shape:

```text
working-ledger/<ledger-owner-id>/
  OWNER.md
  ledger.md
  evidence/
  notes/
```

## Create

When no existing scope is supplied:

1. Create a unique ledger owner ID.
2. Create `working-ledger/<ledger-owner-id>/`.
3. Create `OWNER.md` from the owner template.
4. Create `ledger.md` from the ledger template.
5. Create `evidence/` and `notes/`.
6. Tell the user which scope is active.

Use a runtime session ID when available. Otherwise use:

```text
<UTC timestamp>-<agent-slug>-<short-random-nonce>
```

## Adopt

When the user provides an existing scope:

1. Treat that exact scope as active.
2. Read `OWNER.md`, `ledger.md`, and `handoff.md` if present.
3. Summarize current state before making changes.
4. Continue from `Next actions` and `Recovery notes`.

Do not silently adopt the newest or most plausible existing scope.

## Maintain

Update `ledger.md` after meaningful checkpoints, plan-changing discoveries,
validation results, pauses, handoffs, and closeout.

Keep these sections current:

- Current objective
- Current state summary
- Assumptions
- Progress
- Active plan
- Discoveries
- Decision log
- Validation evidence
- Blockers and risks
- Next actions
- Recovery notes
- Outcome / retrospective

Validation results must use one of:

- Not Run
- Failed
- Passed
- Partially Verified
- Stale
- Not Applicable

## Safety

Do not write secrets, credentials, tokens, private keys, or unnecessary personal
data into a ledger. Summarize or redact risky evidence before recording it.

Do not treat `working-ledger/` as shared memory. It is a container for isolated
ledger scopes.

