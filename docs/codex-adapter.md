# Codex Adapter

The Codex adapter is a generated skill directory that combines the canonical
Agent Working Ledger skill with Codex runtime bindings.

Codex reads user skills from:

```text
$CODEX_HOME/skills/<skill-name>/SKILL.md
```

When `CODEX_HOME` is not set, the default user location is:

```text
~/.codex/skills/<skill-name>/SKILL.md
```

Codex also supports repository-scoped skills from:

```text
.agents/skills/<skill-name>/SKILL.md
```

## Create The User Skill

From the repository root:

```bash
python -m agent_working_ledger install-codex-skill
```

By default this writes:

```text
$CODEX_HOME/skills/agent-working-ledger/
```

or, when `CODEX_HOME` is unset:

```text
~/.codex/skills/agent-working-ledger/
```

The generated directory contains:

```text
agent-working-ledger/
  SKILL.md
  templates/
  runtime-capabilities.md
  AGENTS.md-snippet.md
```

The command refuses to overwrite an existing target. To write somewhere else,
pass an explicit target:

```bash
python -m agent_working_ledger install-codex-skill --target path/to/agent-working-ledger
```

For a repository-scoped Codex skill:

```bash
python -m agent_working_ledger install-codex-skill --target .agents/skills/agent-working-ledger
```

The installer does not append to or rewrite `AGENTS.md`. If project-level
instructions are useful, review the copied `AGENTS.md-snippet.md` and add the
relevant guidance manually.

## Adapter Status

This repository provides Codex wrapper material and an installer that creates a
Codex-ready skill directory. A live Codex smoke run should be recorded in
release notes or a checked smoke-test log before claiming end-to-end Codex
compatibility.

## Smoke Test

Restart Codex or start a new Codex session after installing the skill.

Invoke the skill explicitly:

```text
$agent-working-ledger "Codex adapter smoke test"
```

You can also select it with `/skills`, or rely on implicit skill matching for a
task that clearly matches the skill description.

Approve file creation if Codex asks. Expected result:

- Codex creates exactly one scope under `working-ledger/`.
- The scope owner is either `codex-<session-id>` when Codex exposes a stable
  session or conversation ID, or `<UTC timestamp>-codex-<short-random-nonce>`
  when no stable ID is available.
- The scope contains `OWNER.md`, `ledger.md`, `evidence/`, and `notes/`.
- Codex reports the active scope ID as a standalone, copyable fragment, may
  also report the active scope path, and continues using only that scope.

Validate the generated scope from a normal shell:

```bash
python -m agent_working_ledger check working-ledger/<ledger-owner-id>
```

## Troubleshooting

If `$agent-working-ledger` does not appear in Codex, restart Codex. Skill
discovery can require a new session after creating a top-level skill directory.

If the generated owner uses the timestamp fallback, Codex did not expose a
stable session or conversation ID to the agent. That fallback is:

```text
<UTC timestamp>-codex-<short-random-nonce>
```

If the install command says the target already exists, inspect the existing
directory and either remove it manually or choose another `--target`.
