# Agent Working Ledger

[![CI](https://github.com/MitchellQuinn/agent-working-ledger/actions/workflows/ci.yml/badge.svg)](https://github.com/MitchellQuinn/agent-working-ledger/actions/workflows/ci.yml)

**Make AI coding agents resumable.**

Agent Working Ledger gives long-running software-agent work a durable,
human-readable execution record. When an agent session is interrupted, handed
off, reviewed, or resumed, the next worker can see what was done, why decisions
were made, what evidence exists, what is blocked, and what should happen next.

It is not a planner, issue tracker, test runner, or source-control replacement.
It is task-local execution state for agentic software work.

## Status

Agent Working Ledger is a public alpha `v0.1.0` source release: usable,
documented, and tested, but intentionally conservative in scope.

It is intended to be inspected as a small, honest portfolio project with
installable helper tooling and documented runtime wrapper material. It does not
claim production adoption, PyPI publication, or universal agent-runtime
compatibility.

The source specification is currently on iteration `v0.3`. The specification
version describes the ledger schema and expected behaviour. It is not the
package release number.

Manual GitHub tag and Release creation are tracked in
`docs/release-checklist.md`.

## Quick start

Install from source:

```bash
python -m pip install git+https://github.com/MitchellQuinn/agent-working-ledger.git@v0.1.0
```

Create a task-local scope with the optional continuation sidecars, then inspect
it:

```bash
awl new "OAuth refresh fix" --owner-id oauth-refresh-fix --handoff --machine-state
awl check working-ledger/oauth-refresh-fix
awl summarize working-ledger/oauth-refresh-fix
```

That creates:

```text
working-ledger/oauth-refresh-fix/
  OWNER.md
  ledger.md
  handoff.md
  machine-state.json
  evidence/
  notes/
```

`OWNER.md` identifies the task scope and owning agent/session. `ledger.md`
records actual progress, decisions, evidence, blockers, validation, and recovery
notes. `handoff.md` gives the next agent or person enough state to continue.
`machine-state.json` mirrors structured continuation state; the Markdown ledger
remains the authority.

> Generated ledgers may contain private paths, debugging notes, snippets,
> decisions, and handoff context. `working-ledger/` is ignored by default;
> review carefully before committing any ledger content.

See `docs/quickstart.md` for the fuller create, resume, handoff, and closeout
workflow. See `spec/SPEC.md` for the canonical behavior.

## Why this exists

Agentic coding work often fails at the boundaries: context resets, agent
handoffs, stale assumptions, and unclear validation state. Evidence and
decisions get scattered across chat, commits, logs, and memory.

Agent Working Ledger gives each substantial task a small, explicit,
human-readable record of actual work, evidence, blockers, and continuation
state.

Use it when you want an agent to leave behind a clear record of:

- what it is trying to do
- what it has already done
- what it discovered
- what decisions it made
- what validation evidence exists
- what is blocked
- what the next agent or human should do

## When not to use this

Creating no ledger is the default. Ledgers are for work where context loss,
handoff, auditability, safety, or validation drift would matter.

Do not create a ledger for:

- simple Q&A
- tiny one-shot edits
- trivial refactors
- work where the ledger would be longer than the work
- exploratory thoughts that are not yet a task
- anything that would tempt the agent to record guesses as progress

Use a ledger when:

- work spans multiple steps or sessions
- another agent or person may need to continue
- evidence, blockers, validation, or decisions need to survive context loss
- stale or aspirational progress would be harmful

## What this is / is not

Agent Working Ledger is:

- a task-local continuity record
- human-readable and agent-readable
- evidence-oriented
- explicit about ownership, scope, blockers, and validation
- safe to close, abandon, or supersede
- designed to help future agents avoid treating stale state as truth

Agent Working Ledger is not:

- a planner
- a project-management system
- hidden long-term memory
- a cryptographic execution log
- a replacement for commits, tests, issues, or review
- a place to record guesses as completed work

## The core idea

Each agent thread writes to exactly one active ledger scope under
`working-ledger/`, unless the user explicitly directs it to use an existing
scope.

A ledger scope is a task-local working record. It belongs to a specific agent
thread or adopted task context. Existing ledgers are discoverable artifacts, not
automatically adoptable memory.

The human-readable `ledger.md` remains the authority.

## Example ledger excerpt

A committed illustrative example in `examples/feature-implementation/ledger.md`
shows the shape of the artifact:

```text
# Feature Implementation Example

Ledger scope: examples/feature-implementation
Lifecycle State: Ready for Review

## Progress

- [x] Inspect existing feature entry point.
- [x] Implement the requested behavior.
- [x] Run targeted validation.
- [ ] Reviewer acceptance.

## Validation evidence

- Command/check: `python -m unittest discover -s tests`
  Result: Passed
  Evidence: See `evidence/test-run.txt`.
  Follow-up: Reviewer may run broader integration checks.

Overall validation status: Passed

## Blockers and risks

- Blocker/risk: Broader integration path was not exercised.
  Impact: Review should confirm the full workflow.
  Next action: Run integration checks if review requests them.

## Next actions

1. Reviewer inspects the implementation.
2. Run broader checks if requested.
```

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
agent_working_ledger/        Optional helper tooling package
tests/                       Unit tests for helper tooling
```

## Detailed setup

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
python -m agent_working_ledger new "OAuth refresh fix" --owner-id oauth-refresh-fix
```

Alternatively, create optional sidecars at creation time:

```bash
python -m agent_working_ledger new "OAuth refresh fix" --owner-id oauth-refresh-fix --handoff --machine-state
```

### 5. Check or summarise a ledger scope

```bash
python -m agent_working_ledger check working-ledger/<ledger-owner-id>/
python -m agent_working_ledger summarize working-ledger/<ledger-owner-id>/
python -m agent_working_ledger list --root working-ledger
```

When installed as a package, the console script is:

```bash
awl new "OAuth refresh fix" --owner-id oauth-refresh-fix
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
It reports the standalone scope ID as well as the created paths. Use
`--owner-id` when you need a deterministic scope path, or `--slug` when you want
the generated timestamp/runtime/nonce ID to include a readable suffix.

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

`awl list` is read-only. It lists ledger scopes under the selected root. If a
child directory is only a grouping folder, nested ledger scopes are reported
instead.

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

For release validation, use `docs/release-checklist.md`. Core local checks
include:

Build wheels from a clean checkout, or remove ignored `build/`, `dist/`, and
`*.egg-info/` artifacts first.

```bash
python -m pytest
python -m compileall -q agent_working_ledger tests
python -m agent_working_ledger --version
python -m agent_working_ledger assets
python -m agent_working_ledger check <example-scope>
python -m build
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
