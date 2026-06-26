# Installation

Agent Working Ledger `0.1.0` includes the core skill, wrapper instructions,
release documentation, templates, examples, evaluation material, and optional
helper tooling.

The source specification iteration is `v0.3`; optional `machine-state.json`
files should use `schema_version: "0.3"`.

## Locate Installed Assets

After installing the package, locate the installed release assets with:

```bash
awl assets
```

JSON output is available:

```bash
awl assets --format json
```

The installed asset root is:

```text
share/agent-working-ledger/
```

## Canonical Skill

Copy the whole skill package directory:

```text
skills/agent-working-ledger/
```

to the skill location expected by the target runtime.

The skill package includes `SKILL.md` and bundled templates under
`skills/agent-working-ledger/templates/`.

## Claude Code

Recommended paths:

```text
.claude/skills/agent-working-ledger/SKILL.md
~/.claude/skills/agent-working-ledger/SKILL.md
```

Create a Claude Code-ready skill directory from the repository root with:

```bash
python -m agent_working_ledger install-claude-code-skill
```

By default this writes:

```text
.claude/skills/agent-working-ledger/
```

Use wrapper material from:

```text
wrappers/claude-code/
```

Claude Code should use `claude-code-${CLAUDE_SESSION_ID}` as the owner ID when
that environment variable is available.

See `docs/claude-code-adapter.md` for personal install targets, Claude Code
installation notes, and smoke-test steps.

## Codex

Create a Codex-ready user skill directory from the repository root with:

```bash
python -m agent_working_ledger install-codex-skill
```

By default this writes to `$CODEX_HOME/skills/agent-working-ledger/`, or
`~/.codex/skills/agent-working-ledger/` when `CODEX_HOME` is unset.

For a repository-scoped Codex skill, pass an explicit target:

```bash
python -m agent_working_ledger install-codex-skill --target .agents/skills/agent-working-ledger
```

Codex should use `codex-<session-id>` when a stable Codex session or
conversation ID is available. Otherwise it should mint:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

The installer copies `wrappers/codex/AGENTS.md-snippet.md` for reference but
does not modify `AGENTS.md`.

See `docs/codex-adapter.md` for install, invocation, smoke-test, and
troubleshooting steps.

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
python -m agent_working_ledger new "Task title" --slug task-title
```

Run the checker without installing:

```bash
python -m agent_working_ledger check working-ledger/<ledger-owner-id>/
```

Install the package in editable mode to expose the `awl` console script:

```bash
python -m pip install -e .
awl new "Task title" --slug task-title
awl check working-ledger/<ledger-owner-id>/
awl summarize working-ledger/<ledger-owner-id>/
awl list --root working-ledger
awl assets
awl install-claude-code-skill
awl install-codex-skill
```

`awl new` creates a fresh scope and refuses to overwrite existing scopes. Scope
commands report the standalone scope ID separately from any path when they
reflect a ledger back to the user. `awl check` is read-only. It reports errors
and warnings but does not create, repair, close, supersede, or otherwise mutate
ledger scopes.
