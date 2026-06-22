# Manual Handoff Evaluations

Manual evaluations are Markdown-first checks for Agent Working Ledger behavior.
They are meant to answer one question: can a second agent resume from the
ledger without the original chat and without contaminating unrelated scopes?

## Materials

- Scenario files in `evals/scenarios/`
- Run template in `evals/templates/manual-run.md`
- Scoring sheet in `evals/templates/scoring-sheet.md`
- Filled run examples in `evals/runs/`
- Existing checker command documented in `docs/checker.md`

## Two-Agent Handoff Test

1. Pick one scenario from `evals/scenarios/`.
2. Copy `evals/templates/manual-run.md` into `evals/runs/` with a descriptive
   file name.
3. Prepare the repository or fixture state described by the scenario.
4. Start Agent A with instructions to use Agent Working Ledger and complete only
   the first segment of the scenario.
5. Interrupt Agent A at the planned stopping point.
6. Record Agent A's standalone scope ID, ledger scope path, changed files,
   validation state, and handoff note in the run file.
7. Start Agent B in a fresh chat or runtime context.
8. Give Agent B the exact standalone scope ID and ledger scope path to adopt. Do
   not provide the full Agent A chat unless the scenario explicitly tests chat
   availability.
9. Ask Agent B to recover, continue from the ledger, and update only the adopted
   scope.
10. Score the run with `evals/templates/scoring-sheet.md`.

## Suggested Agent B Prompt

```text
Use Agent Working Ledger. Adopt this existing scope exactly:
<ledger-owner-id>
working-ledger/<ledger-owner-id>/

Recover from the ledger, continue the task, and do not update any unrelated
ledger scope. Before claiming completion, review or rerun validation that the
ledger marks as stale, partial, failed, or not run.
```

## Comparison Notes

Run the same scenario more than once when comparing runtimes or prompt changes.
Keep each run file separate. Compare the score totals, but also compare the
failure modes: a lower score caused by stale validation is different from a
lower score caused by scope contamination.

The evaluation is intentionally manual. Do not add a new harness or runner
unless the Markdown process stops being sufficient.
