# Ledger Scope

A ledger scope is the isolated task-state directory owned by one agent thread or
one explicitly assigned continuation.

## Default Shape

```text
working-ledger/
  <ledger-owner-id>/
    OWNER.md
    ledger.md
    evidence/
    notes/
```

Optional files:

```text
working-ledger/
  <ledger-owner-id>/
    handoff.md
    machine-state.json
```

The root `working-ledger/` directory is only a container. It is not shared
working memory and must not become a coordination file by accident.

## Owner ID

When the runtime exposes a stable session or thread ID, include it in the owner
ID. Otherwise mint:

```text
<UTC timestamp>-<agent-slug>-<short-random-nonce>
```

The owner ID must appear in the scope path, `OWNER.md`, `ledger.md`, and optional
handoff or machine-readable state files when those files exist.

## File Responsibilities

`OWNER.md` records identity and write permission. It must not contain progress,
plans, discoveries, or validation detail.

`ledger.md` is the durable human-readable execution-state authority. It records
objective, progress, discoveries, decisions, evidence, blockers, next actions,
and recovery state.

`evidence/` stores bulky or external proof such as logs, command output,
screenshots, benchmark output, reports, or diffs. The ledger should summarize
and reference evidence rather than copy excessive output.

`notes/` stores supporting material. Important discoveries from notes must be
reflected in `ledger.md`.

`handoff.md` is an optional compressed continuation artifact. It does not
replace `ledger.md`.

`machine-state.json` is optional non-authoritative metadata mirrored from
`ledger.md`. If the files conflict, `ledger.md` wins.

## Write Boundary

An agent may write to a scope only when it created the scope, the user explicitly
supplied it, or a wrapper/project instruction explicitly assigned it. Existing
ledgers are discoverable artifacts, not automatically adoptable memory.
