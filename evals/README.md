# Evaluation Scenarios

These evaluation documents describe how to assess Agent Working Ledger behavior.
They are not executable tests yet.

Primary qualities:

- Resumability
- Auditability
- Contamination resistance
- Validation quality

Use:

- `scenarios/` for setup prompts and expected ledger behavior.
- `rubrics/` for quality-specific evaluation notes.
- `runs/` for filled manual run examples.
- `templates/manual-run.md` to record a single handoff/resume run.
- `templates/scoring-sheet.md` to score a completed run.

Use the scenarios to review whether an agent and its ledger can survive
interruption, failed validation, stale assumptions, parallel work, and handoff
after compaction.

For a two-agent handoff procedure, see `docs/manual-evals.md`.
