# Changelog

## 0.1.0 - 2026-06-26

- Preparing the first Agent Working Ledger release from source specification
  iteration `v0.3`.
- Added the canonical standard at `spec/SPEC.md` plus focused reference docs for
  invariants, ownership, lifecycle, ledger scopes, validation/evidence, and
  security/privacy.
- Added operation protocols for create, adopt, orient, update, record discovery,
  record decision, record validation, recover, handoff, close, and supersede.
- Added reusable templates for `OWNER.md`, `ledger.md`, `handoff.md`, optional
  evidence README material, and optional `machine-state.json`.
- Added the canonical installable skill package plus thin Claude Code, Codex,
  and generic CLI wrapper material.
- Added practical documentation for quickstart, installation, multi-agent use,
  plan boundaries, and anti-patterns.
- Added optional read-only `awl check` tooling for validating a specified ledger
  scope without creating, repairing, closing, or mutating ledgers.
- Added optional `awl new` tooling for creating a fresh ledger scope that passes
  `awl check` immediately and refuses to overwrite existing scopes.
- Added read-only `awl summarize` and `awl list` commands.
- Added read-only `awl assets` command for locating packaged release assets.
- Added bounded mutating `awl close` and `awl supersede` commands for explicitly
  supplied scopes.
- Added `awl install-claude-code-skill` to materialize a Claude Code-ready
  project or personal skill directory from the canonical skill and wrapper
  assets.
- Bundled templates with the canonical skill package and packaged release
  assets under `share/agent-working-ledger/`.
- Added example ledger scopes under `examples/`.
- Added manual evaluation scenario docs and rubrics under `evals/`, with the
  procedure in `docs/manual-evals.md`.
- Added GitHub Actions CI in `.github/workflows/ci.yml`.
- Added release asset inspection coverage through CI and `docs/assets-command.md`.
