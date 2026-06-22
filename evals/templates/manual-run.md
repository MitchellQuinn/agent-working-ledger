# Manual Eval Run Template

Use this template for one handoff/resume evaluation run. Copy it into
`evals/runs/` or another task-local review location, then fill it out during the
run.

## Run Metadata

- Run ID:
- Date:
- Evaluator:
- Scenario:
- Repository or fixture:
- Agent A runtime:
- Agent B runtime:
- Active ledger scope ID created by Agent A:
- Active ledger scope path created by Agent A:
- Handoff artifact:

## Scenario Setup

- Scenario file:
- Starting branch or commit:
- Files or fixtures prepared:
- Constraints given to Agent A:
- Intended interruption point:

## Agent A Prompt

```text
<Prompt given to the first agent.>
```

## Agent A Result At Interruption

- Files changed:
- Ledger scope ID:
- Ledger scope path:
- Ledger lifecycle state:
- Validation recorded:
- Work completed:
- Work remaining:
- Known stale assumptions or validation:

## Handoff Prompt For Agent B

```text
<Prompt given to the second agent, including the exact ledger scope ID and path to adopt.>
```

## Agent B Resume Result

- Did Agent B adopt only the supplied scope?
- Did Agent B identify completed work without redoing it?
- Did Agent B identify remaining work?
- Did Agent B rerun or review stale validation before claiming completion?
- Did Agent B preserve or update validation evidence accurately?
- Final lifecycle state:
- Final validation status:

## Scoring Summary

Use `evals/templates/scoring-sheet.md`.

| Quality | Score | Notes |
| --- | ---: | --- |
| Resumability |  |  |
| Auditability |  |  |
| Validation quality |  |  |
| Contamination resistance |  |  |

Total score:

## Evidence

- Ledger scope ID inspected:
- Ledger scope path inspected:
- Commands run:
- Screenshots, transcripts, or notes:
- Relevant diffs:

## Outcome

- Pass, partial pass, or fail:
- Main reason:
- Follow-up changes:
