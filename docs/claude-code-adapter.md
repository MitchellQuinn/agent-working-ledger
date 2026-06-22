# Claude Code Adapter

The Claude Code adapter is a generated skill directory that combines the
canonical Agent Working Ledger skill with Claude Code runtime bindings.

Claude Code discovers project skills from:

```text
.claude/skills/<skill-name>/SKILL.md
```

and personal skills from:

```text
~/.claude/skills/<skill-name>/SKILL.md
```

## Create The Project Skill

From the repository root:

```bash
python -m tools.awl install-claude-code-skill
```

This creates:

```text
.claude/skills/agent-working-ledger/
  SKILL.md
  templates/
  runtime-capabilities.md
  CLAUDE.md-snippet.md
```

The command refuses to overwrite an existing target. To write somewhere else,
pass an explicit target:

```bash
python -m tools.awl install-claude-code-skill --target path/to/agent-working-ledger
```

For a personal Windows PowerShell install:

```powershell
python -m tools.awl install-claude-code-skill --target "$HOME\.claude\skills\agent-working-ledger"
```

For a personal macOS, Linux, or WSL install:

```bash
python -m tools.awl install-claude-code-skill --target ~/.claude/skills/agent-working-ledger
```

## Install Claude Code

Install Claude Code using Anthropic's current installer for your platform, then
start it once and log in:

```bash
claude
```

On native Windows, Anthropic recommends Git for Windows so Claude Code can use a
Bash tool. Without it, Claude Code falls back to PowerShell.

## Smoke Test

Start Claude Code in the repository root:

```bash
claude
```

Invoke the skill:

```text
/agent-working-ledger "Claude Code adapter smoke test"
```

Approve file creation if Claude Code asks. Expected result:

- Claude Code creates exactly one scope under `working-ledger/`.
- The scope owner starts with `claude-code-` when `${CLAUDE_SESSION_ID}` is
  available.
- The scope contains `OWNER.md`, `ledger.md`, `evidence/`, and `notes/`.
- Claude Code reports the active scope ID as a standalone, copyable fragment,
  may also report the active scope path, and continues using only that scope.

Validate the generated scope from a normal shell:

```bash
python -m tools.awl check working-ledger/<ledger-owner-id>
```

## Troubleshooting

If `/agent-working-ledger` does not appear in Claude Code, restart Claude Code.
Creating a top-level skills directory after a session has already started may
require a restart before it is watched.

If the generated owner does not start with `claude-code-`, check whether Claude
Code exposed `${CLAUDE_SESSION_ID}` in that run. The adapter falls back to:

```text
<UTC timestamp>-claude-code-<short-random-nonce>
```

If the install command says the target already exists, inspect the existing
directory and either remove it manually or choose another `--target`.
