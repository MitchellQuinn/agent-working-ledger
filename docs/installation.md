# Installation

Agent Working Ledger `0.1.0` includes the core skill, wrapper instructions, and
optional helper tooling.

The source specification iteration is `v0.3`; optional `machine-state.json`
files should use `schema_version: "0.3"`.

## Canonical Skill

Copy:

```text
skills/agent-working-ledger/SKILL.md
```

to the skill location expected by the target runtime.

## Claude Code

Recommended paths:

```text
.claude/skills/agent-working-ledger/SKILL.md
~/.claude/skills/agent-working-ledger/SKILL.md
```

Use wrapper material from:

```text
wrappers/claude-code/
```

Claude Code should use `claude-code-${CLAUDE_SESSION_ID}` as the owner ID when
that environment variable is available.

## Codex

Use wrapper material from:

```text
wrappers/codex/
```

Codex should use a stable Codex session or conversation ID when one is available.
Otherwise it should mint:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

## Generic CLI Agents

Use:

```text
wrappers/generic-cli-agent/prompt-wrapper.md
```

The wrapper should be included in the agent prompt or project instructions for
long-running, multi-step, exploratory, validation-heavy, or handoff-prone work.

## Repository Use

Task-local ledgers are normally created under:

```text
working-ledger/<ledger-owner-id>/
```

This repository ignores `working-ledger/` so development ledgers are not
committed by accident. Projects that want to commit ledgers can change that
policy locally.

## Optional Tooling

Create a ledger without installing:

```bash
python -m tools.awl new "Task title" --slug task-title
```

Run the checker without installing:

```bash
python -m tools.awl check working-ledger/<ledger-owner-id>/
```

Install the package in editable mode to expose the `awl` console script:

```bash
python -m pip install -e .
awl new "Task title" --slug task-title
awl check working-ledger/<ledger-owner-id>/
```

`awl new` creates a fresh scope and refuses to overwrite existing scopes.
`awl check` is read-only. It reports errors and warnings but does not create,
repair, close, supersede, or otherwise mutate ledger scopes.
