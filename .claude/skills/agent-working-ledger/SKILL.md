---
name: agent-working-ledger
description: Maintain a session-specific working ledger for long-running, multi-step, exploratory, interruptible, validation-heavy, or handoff-prone work. Uses the active Claude Code session ID when available to create or adopt one ledger scope under working-ledger/. Do not write to unrelated ledger scopes unless the user explicitly provides one.
argument-hint: "[optional-existing-ledger-scope-or-task-title]"
---

# Agent Working Ledger For Claude Code

This is the Claude Code adapter for the canonical Agent Working Ledger skill.
Apply the canonical instructions below with these Claude Code runtime bindings.

## Claude Code Runtime Binding

- Treat `$ARGUMENTS` as either an explicitly supplied existing ledger scope or a
  human-readable task title. If no argument is supplied, infer the task title
  from the current user request.
- Use `claude-code-${CLAUDE_SESSION_ID}` as the ledger owner ID when
  `${CLAUDE_SESSION_ID}` is available.
- If a human-readable slug is useful, append it:
  `claude-code-${CLAUDE_SESSION_ID}-<task-slug>`.
- If `${CLAUDE_SESSION_ID}` is unavailable, fall back to
  `<UTC timestamp>-claude-code-<short-random-nonce>`.
- Bundled templates live under `${CLAUDE_SKILL_DIR}/templates/`.
- Supporting Claude Code notes are available in
  `${CLAUDE_SKILL_DIR}/runtime-capabilities.md` and
  `${CLAUDE_SKILL_DIR}/CLAUDE.md-snippet.md`.
- Do not treat this adapter as a fork of the core schema. If there is any
  ambiguity, preserve the canonical Agent Working Ledger schema and apply only
  the owner-ID and runtime bindings above.

# Agent Working Ledger

Use this skill when work is complex enough that durable execution state is more
valuable than the overhead of maintaining it.

## Trigger

Use this skill for long-running, multi-step, exploratory, interruption-prone,
validation-heavy, handoff-prone, migration, refactor, debugging, eval-loop, or
multi-agent work.

Also use it when the user asks for a working memory, working ledger, task
ledger, worklog, continuation file, implementation log, recovery file, or
handoff note.

Do not use it for simple one-shot answers, small single-file edits, purely
conversational tasks, or when the user explicitly asks not to create files.

## Core Rule

Each agent thread works inside exactly one active ledger scope. Write task-state
files only inside that scope unless the user explicitly directs you to use
another one.

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

Optional files:

```text
working-ledger/<ledger-owner-id>/
  handoff.md
  machine-state.json
```

`ledger.md` is the human-readable authority. Optional machine-readable state only
mirrors it.

Bundled templates live under this skill package:

```text
templates/
  OWNER.md.template
  ledger.md.template
  handoff.md.template
  evidence-README.md.template
  machine-state.json.template
```

## Create

When no existing scope is supplied:

1. Create a unique ledger owner ID.
2. Create `working-ledger/<ledger-owner-id>/`.
3. Create `OWNER.md` from `templates/OWNER.md.template`.
4. Create `ledger.md` from `templates/ledger.md.template`.
5. Create `evidence/` and `notes/`.
6. Tell the user which scope is active.
7. Continue using only that scope.

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

If `OWNER.md` is missing but the user explicitly supplied the scope, create it
only after noting that ownership metadata was missing.

## Lifecycle

Use only these lifecycle states:

- Created
- Oriented
- Planned
- Active
- Blocked
- Ready for Review
- Closed
- Superseded

Keep the lifecycle state visible near the top of `ledger.md`. Closed ledgers
should not be reopened casually; create a new ledger or supersede the old one
unless the user explicitly directs reopening.

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

When a fact affects several sections, update all affected sections. Examples:

- If a decision changes the plan, update `Decision log` and `Active plan`.
- If an assumption is invalidated, update `Assumptions`, `Discoveries`, and
  possibly `Active plan`.
- If validation becomes stale, mark it `Stale`.
- If progress is partial, split the item instead of marking it complete.

Validation results must use one of:

- Not Run
- Failed
- Passed
- Partially Verified
- Stale
- Not Applicable

Each validation entry must include the command or check, result, evidence, and
follow-up. Large evidence belongs in `evidence/` with a concise reference in
`ledger.md`.

## Recover

At the start of a resumed work segment:

1. Confirm the active ledger scope.
2. Read `OWNER.md`, `ledger.md`, and `handoff.md` if present.
3. Check whether lifecycle state, next actions, active plan, progress, files
   mentioned, and validation status still match the repository.
4. Repair only the active ledger before proceeding if inconsistencies are found.

## Handoff, Close, And Supersede

Before handing off, update `ledger.md` and optionally create or update
`handoff.md`. The handoff note is a compressed continuation artifact, not the
authority.

Close a ledger only when the task or milestone is complete, abandoned, or
intentionally stopped. Temporary pauses require recovery notes, not closure.

Supersede a ledger when another ledger, plan, issue, or execution path replaces
it. Record what superseded it, why, whether any work remains useful, and where
continuation should happen.

## Subagents

Each independent subagent, fork, or parallel agent should have its own ledger
scope unless the user explicitly assigns it to an existing one. A subagent
should return a summary to the parent, provide its own ledger path, or write a
bounded handoff note in its own scope.

Do not let subagents write into the parent ledger unless explicitly instructed.

## Safety

Do not write secrets, credentials, tokens, private keys, or unnecessary personal
data into a ledger. Summarize or redact risky evidence before recording it.

Do not treat `working-ledger/` as shared memory. It is a container for isolated
ledger scopes.

Do not use the ledger as a substitute for tests, source control, issue tracking,
or a formal project plan. A plan records intended work. The working ledger
records actual execution state.
