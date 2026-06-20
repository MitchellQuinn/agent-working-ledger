# Agent Working Ledger

Agent Working Ledger is an agent-agnostic skill for long-running software-agent work.
It teaches agents to create or adopt one task-local ledger scope under
`working-ledger/`, then maintain a structured Markdown record of progress,
discoveries, decisions, validation evidence, blockers, next actions, and recovery
notes.

The ledger is not a replacement for a plan, tests, issue trackers, or source
control. It is durable execution state for work that may be interrupted,
resumed, reviewed, or handed off.

## Status

This repository is initialized from the v0.3 specification. The current contents
are a minimal release scaffold: core spec, protocol summaries, templates, the
canonical skill package, wrapper snippets, and introductory docs.

## Repository Layout

```text
documents/                  Source specification material
spec/                       Canonical specification and core model docs
protocols/                  Operation protocols for ledger lifecycle actions
templates/                  Reusable ledger file templates
skills/agent-working-ledger/ Canonical distributable skill package
wrappers/                   Runtime-specific wrapper material
docs/                       User-facing documentation
```

## Quick Start

1. Read [spec/SPEC.md](spec/SPEC.md) for the full standard.
2. Install or copy [skills/agent-working-ledger/SKILL.md](skills/agent-working-ledger/SKILL.md)
   into the target agent's skill directory.
3. Use the relevant wrapper material under [wrappers/](wrappers/) when the
   runtime needs agent-specific instructions.
4. Use the templates under [templates/](templates/) when creating a new ledger
   scope manually or from future tooling.

## Core Rule

Each agent thread writes to exactly one active ledger scope unless the user
explicitly directs it to use an existing one. Existing ledgers are discoverable
artifacts, not automatically adoptable memory.

