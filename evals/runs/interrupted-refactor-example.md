# Interrupted Refactor Example Run

This is a worked example for `evals/scenarios/interrupted-refactor.md`. It
shows the expected level of detail for a completed manual handoff/resume
evaluation run.

## Run Metadata

- Run ID: interrupted-refactor-example
- Date: 2026-06-22
- Evaluator: Manual evaluator
- Scenario: `evals/scenarios/interrupted-refactor.md`
- Repository or fixture: sample CLI refactor fixture
- Agent A runtime: Example CLI coding agent
- Agent B runtime: Fresh example CLI coding agent session
- Active ledger scope created by Agent A:
  `working-ledger/20260622T093000Z-agent-a-refactor/`
- Handoff artifact:
  `working-ledger/20260622T093000Z-agent-a-refactor/handoff.md`

## Scenario Setup

- Scenario file: `evals/scenarios/interrupted-refactor.md`
- Starting branch or commit: `sample-cli-before-parser-refactor`
- Files or fixtures prepared:
  - `src/cli.py`
  - `src/commands.py`
  - `tests/test_cli.py`
- Constraints given to Agent A:
  - Use Agent Working Ledger.
  - Refactor only the parser construction and read-only command path.
  - Stop before migrating write commands.
  - Record stale or partial validation explicitly.
- Intended interruption point: after parser extraction and targeted read-only
  command tests, before write-command migration.

## Agent A Prompt

```text
Use Agent Working Ledger for this task. Refactor the sample CLI so argument
parser construction is separated from command execution. Complete the parser
extraction and read-only command migration, then stop before migrating write
commands. Leave a handoff note that makes the next steps recoverable without
this chat.
```

## Agent A Result At Interruption

- Files changed:
  - `src/cli.py`
  - `src/commands.py`
  - `tests/test_cli.py`
  - `working-ledger/20260622T093000Z-agent-a-refactor/ledger.md`
  - `working-ledger/20260622T093000Z-agent-a-refactor/handoff.md`
- Ledger scope: `working-ledger/20260622T093000Z-agent-a-refactor/`
- Ledger lifecycle state: Active
- Validation recorded:
  - `python -m pytest tests/test_cli.py -k "parse or list or show"`
  - Result: Partially Verified
  - Evidence: targeted parser, list, and show command tests passed.
  - Follow-up: run full CLI test suite after write commands are migrated.
- Work completed:
  - Extracted `build_parser()` from `main()`.
  - Moved `list` and `show` command dispatch to `src/commands.py`.
  - Updated targeted tests for parser construction and read-only commands.
- Work remaining:
  - Migrate `create`, `update`, and `delete` command dispatch.
  - Remove temporary compatibility branch in `src/cli.py`.
  - Run full test suite.
- Known stale assumptions or validation:
  - Full validation is stale because write-command dispatch still uses the old
    path.
  - No packaging or install smoke test has been run.

## Handoff Prompt For Agent B

```text
Use Agent Working Ledger. Adopt this existing scope exactly:
working-ledger/20260622T093000Z-agent-a-refactor/

Recover from the ledger, finish the interrupted CLI refactor, and do not update
any unrelated ledger scope. Before claiming completion, review or rerun
validation that the ledger marks as stale, partial, failed, or not run.
```

## Agent B Resume Result

- Did Agent B adopt only the supplied scope? Yes.
- Did Agent B identify completed work without redoing it? Yes. Agent B kept the
  extracted parser and read-only command migration.
- Did Agent B identify remaining work? Yes. Agent B resumed at write-command
  migration and compatibility cleanup.
- Did Agent B rerun or review stale validation before claiming completion? Yes.
  Agent B reran targeted CLI tests and the full suite.
- Did Agent B preserve or update validation evidence accurately? Yes. The
  stale targeted validation entry remained in the ledger, and new full-suite
  validation was added as Passed.
- Final lifecycle state: Ready for Review
- Final validation status: Passed

## Scoring Summary

Use `evals/templates/scoring-sheet.md`.

| Quality | Score | Notes |
| --- | ---: | --- |
| Resumability | 3 | Objective, completed work, remaining work, files, and recovery steps were specific. |
| Auditability | 2 | Decisions and validation were clear, but the fixture did not preserve a full command transcript. |
| Validation quality | 3 | Partial and stale validation were labelled, then full validation was rerun before completion. |
| Contamination resistance | 3 | Agent B adopted only the supplied ledger scope and did not write to unrelated scopes. |

Total score: 11

## Evidence

- Ledger scope inspected: `working-ledger/20260622T093000Z-agent-a-refactor/`
- Commands run:
  - `python -m pytest tests/test_cli.py -k "parse or list or show"`
  - `python -m pytest`
  - `python -m agent_working_ledger check working-ledger/20260622T093000Z-agent-a-refactor`
- Screenshots, transcripts, or notes:
  - Manual evaluator reviewed the final ledger, handoff note, and diff.
  - No screenshots were required for this CLI-only fixture.
- Relevant diffs:
  - `src/cli.py`
  - `src/commands.py`
  - `tests/test_cli.py`

## Outcome

- Pass, partial pass, or fail: Pass
- Main reason: the second agent could resume from the ledger without the
  original chat, avoid unrelated scopes, and update stale validation before
  claiming completion.
- Follow-up changes: preserve a complete command transcript if this example is
  promoted from a worked example into a release-gating benchmark.
