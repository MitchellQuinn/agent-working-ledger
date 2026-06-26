# Agent Working Ledger

[![CI](https://github.com/MitchellQuinn/agent-working-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/MitchellQuinn/agent-working-ledger/actions/workflows/ci.yml)

**Make AI coding agents resumable.**

Agent Working Ledger gives long-running software-agent work a durable,
human-readable execution record. When an agent session is interrupted, handed
off, reviewed, or resumed, the next worker can see what was done, why decisions
were made, what evidence exists, what is blocked, and what should happen next.

It is not a planner, issue tracker, test runner, or source-control replacement.
It is task-local execution state for agentic software work.

## Why this exists

AI coding agents are becoming useful for multi-step software work, but their
working state is fragile.

Plans live in chat history. Decisions get buried. Validation evidence
disappears. A task can be half-finished, the session can end, and the next agent
has to reconstruct the work from scratch.

Agent Working Ledger makes that state explicit, durable, inspectable, and
portable between agent sessions.

Use it when you want an agent to leave behind a clear record of:

- what it is trying to do
- what it has already done
- what it discovered
- what decisions it made
- what validation evidence exists
- what is blocked
- what the next agent or human should do

## The core idea

Each agent thread writes to exactly one active ledger scope under
`working-ledger/`, unless the user explicitly directs it to use an existing
scope.

A ledger scope is a task-local working record. It belongs to a specific agent
thread or adopted task context. Existing ledgers are discoverable artifacts, not
automatically adoptable memory.

The human-readable `ledger.md` remains the authority.

## Example workflow

A developer asks an agent to fix a bug.

```bash
awl new "OAuth refresh fix" --slug oauth-refresh-fix
```

The helper prints the standalone scope ID separately from the created paths so
it can be copied into another thread.

The agent creates:

```text
working-ledger/oauth-refresh-fix/
```

During the task, the agent records progress, discoveries, decisions, validation
evidence, blockers, and next actions.

Later, the session ends.

A new agent or human can inspect the ledger:

```bash
awl summarize working-ledger/oauth-refresh-fix/
awl check working-ledger/oauth-refresh-fix/
```

The next worker can resume from the recorded state instead of guessing what
happened.

## What Agent Working Ledger provides

Agent Working Ledger includes:

* a canonical ledger specification
* operation protocols for ledger lifecycle actions
* reusable ledger templates
* a distributable agent skill package
* runtime wrapper material for agent-specific environments
* example ledger scopes
* evaluation scenarios and rubrics
* optional helper tooling for creating, checking, listing, summarising, closing,
  and superseding ledger scopes

## Repository layout

```text
documents/                   Source specification material
spec/                        Canonical specification and core model docs
protocols/                   Operation protocols for ledger lifecycle actions
templates/                   Reusable ledger file templates
skills/agent-working-ledger/  Canonical distributable skill package with bundled templates
wrappers/                    Runtime-specific wrapper material
docs/                        User-facing documentation
examples/                    Example ledger scopes
evals/                       Evaluation scenarios and rubrics
tools/awl/                   Optional helper tooling
tests/                       Unit tests for helper tooling
```

## Status

This repository is preparing the `0.1.0` release of Agent Working Ledger.

This is an alpha GitHub release candidate. It is intended to be inspected as a
small, honest portfolio project with installable helper tooling and documented
runtime wrapper material. It is not a claim of production adoption or universal
agent-runtime compatibility.

The source specification is currently on iteration `v0.3`. The specification
version describes the ledger schema and expected behaviour. It is not the
package release number.

The `0.1.0` release proves the core architecture with:

* specification docs
* operation protocols
* ledger templates
* the canonical skill package
* thin runtime wrappers
* practical documentation
* example ledger scopes
* small optional helper tooling
* tests for the helper tooling

## Quick start

### 1. Read the specification

Start with:

```text
spec/SPEC.md
```

This is the canonical description of the ledger schema and behaviour.

### 2. Install or copy the skill

Copy the whole skill package directory:

```text
skills/agent-working-ledger/
```

into the target agent's skill directory.

When installed as a package, locate the installed release assets with:

```bash
awl assets
```

### 3. Add runtime wrapper material if needed

Use the relevant wrapper material under:

```text
wrappers/
```

when the target runtime needs agent-specific instructions.

Wrappers should adapt Agent Working Ledger to a runtime. They should not
redefine the core schema.

### 4. Create a ledger scope

From the repository root:

```bash
python -m tools.awl new "OAuth refresh fix" --slug oauth-refresh-fix
```

Create optional sidecars at creation time:

```bash
python -m tools.awl new "OAuth refresh fix" --handoff --machine-state
```

### 5. Check or summarise a ledger scope

```bash
python -m tools.awl check working-ledger/<ledger-owner-id>/
python -m tools.awl summarize working-ledger/<ledger-owner-id>/
python -m tools.awl list --root working-ledger
```

When installed as a package, the console script is:

```bash
awl new "OAuth refresh fix" --slug oauth-refresh-fix
awl check working-ledger/<ledger-owner-id>/
awl summarize working-ledger/<ledger-owner-id>/
awl list --root working-ledger
awl assets
awl install-claude-code-skill
awl install-codex-skill
```

See:

```text
docs/quickstart.md
```

for the create, resume, handoff, and closeout workflow.

## CLI

The helper CLI is intentionally small.

### Create a new scope

```bash
awl new "OAuth refresh fix" --slug oauth-refresh-fix
```

`awl new` creates a fresh ledger scope and refuses to overwrite existing scopes.
It reports the standalone scope ID as well as the created paths.

### Validate a scope

```bash
awl check working-ledger/<ledger-owner-id>/
```

`awl check` is read-only. It validates:

* required files
* owner ID consistency
* lifecycle states
* validation statuses
* closeout requirements
* supersession hints
* optional `machine-state.json` consistency

### Summarise a scope

```bash
awl summarize working-ledger/<ledger-owner-id>/
```

`awl summarize` is read-only. It provides a compact view of the current ledger
state.

### List scopes

```bash
awl list --root working-ledger
```

`awl list` is read-only. It lists ledger scopes under the selected root.

### Locate release assets

```bash
awl assets
awl assets --format json
```

`awl assets` is read-only. It prints the release asset root and key subpaths for
the specification, protocols, templates, skill package, wrappers, documentation,
examples, and evaluation material.

### Create a Claude Code skill

```bash
awl install-claude-code-skill
```

`awl install-claude-code-skill` creates a Claude Code-ready project skill under
`.claude/skills/agent-working-ledger/` by combining the canonical skill package
with the Claude Code wrapper. It refuses to overwrite an existing target.

See:

```text
docs/claude-code-adapter.md
```

for Claude Code install and smoke-test steps.

### Create a Codex skill

```bash
awl install-codex-skill
```

`awl install-codex-skill` creates a Codex-ready user skill under
`$CODEX_HOME/skills/agent-working-ledger/`, or
`~/.codex/skills/agent-working-ledger/` when `CODEX_HOME` is unset, by combining
the canonical skill package with the Codex wrapper. It refuses to overwrite an
existing target.

For a repository-scoped Codex skill, pass an explicit target:

```bash
awl install-codex-skill --target .agents/skills/agent-working-ledger
```

See:

```text
docs/codex-adapter.md
```

for Codex install, invocation, and smoke-test steps.

### Close or supersede a scope

```bash
awl close working-ledger/<ledger-owner-id>/
awl supersede working-ledger/<ledger-owner-id>/
```

`awl close` and `awl supersede` mutate only the explicitly supplied scope.

## Ledger lifecycle

A typical ledger lifecycle is:

1. **Create** a task-local ledger scope.
2. **Record** progress, discoveries, decisions, validation evidence, blockers,
   next actions, and recovery notes.
3. **Check** the scope for structural consistency.
4. **Summarise** the scope for review or handoff.
5. **Resume** from an existing scope only when explicitly directed.
6. **Close** the scope when the task is complete.
7. **Supersede** the scope when the work moves to a new scope.

## Design principles

### Durable over clever

The ledger is plain Markdown first. It should be readable by humans without
special tooling.

### Explicit over magical

Existing ledgers are discoverable artifacts. They are not automatically adopted
as memory.

### Task-local over global

Each agent thread writes to one active ledger scope unless explicitly directed
otherwise.

### Evidence over vibes

The ledger records validation evidence, blockers, recovery notes, and decisions
so future work can be grounded in what actually happened.

### Runtime-agnostic core, thin wrappers

The core specification should remain stable across agent runtimes. Wrappers
exist only to adapt the skill to specific environments.

## What this is not

Agent Working Ledger is not:

* a replacement for source control
* a replacement for tests
* a replacement for issue trackers
* a replacement for planning
* a hidden memory system
* an autonomous project manager
* a general knowledge base
* a correctness, compliance, or authorization certification

It is a durable working record for agentic software tasks. A ledger can preserve
review evidence and decisions, but it does not certify that the work is correct,
compliant, authorized, or complete.

## Release boundary

The `0.1.0` release ships bounded Claude Code and Codex skill materializers:

```bash
awl install-claude-code-skill
awl install-codex-skill
```

Those helpers only create Claude Code-ready or Codex-ready skill directories
from the packaged canonical skill and wrapper assets. The release intentionally
does not ship:

* repair commands
* code generators
* general runtime installers
* issue-tracker integrations
* automatic migration tooling
* autonomous adoption of existing ledgers

Future tooling may automate more operations, but the human-readable `ledger.md`
remains the authority.

## Validation

Before release, run:

```bash
python -m unittest discover -s tests
python -m compileall -q tools tests
python -m tools.awl --version
python -m tools.awl assets
python -m tools.awl check <example-scope>
python -m pip wheel --no-deps --no-build-isolation . -w <wheel-dir>
```

Also confirm that the wheel contains `share/agent-working-ledger/`, that an
installed wheel can run `awl assets`, `awl new`, and `awl check`, and that
runtime wrappers do not redefine the core schema.

## Documentation

Start here:

```text
docs/quickstart.md
docs/assets-command.md
spec/SPEC.md
```

Then inspect:

```text
protocols/
templates/
examples/
evals/
```

## Project goal

Agent Working Ledger exists to make agentic software work easier to interrupt,
review, resume, and hand off.

The goal is not to make agents look smarter.

The goal is to make their work state harder to lose.
