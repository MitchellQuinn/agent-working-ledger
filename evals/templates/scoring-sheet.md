# Manual Eval Scoring Sheet

Score each quality from 0 to 3. Prefer concrete ledger evidence over evaluator
impressions.

## Score Scale

| Score | Meaning |
| ---: | --- |
| 0 | Missing or actively misleading. |
| 1 | Present but too vague, stale, or incomplete to rely on. |
| 2 | Adequate for a careful agent or human to continue with minor follow-up. |
| 3 | Strong, specific, and easy to verify without the original chat. |

## Resumability

Score how well the next agent can continue from the ledger.

| Check | Notes |
| --- | --- |
| Objective and current state are clear. |  |
| Completed and remaining work are distinguishable. |  |
| Relevant files and touched files are listed. |  |
| Next actions are specific and ordered. |  |
| Recovery notes state what not to redo. |  |

Score:

## Auditability

Score how well a reviewer can understand what happened and why.

| Check | Notes |
| --- | --- |
| Decisions include rationale, alternatives, and consequences. |  |
| Discoveries include evidence and impact. |  |
| Risks and blockers are visible. |  |
| Progress reflects actual work rather than intent. |  |
| Outcome or pause state is explicit. |  |

Score:

## Validation Quality

Score whether correctness claims match recorded evidence.

| Check | Notes |
| --- | --- |
| Commands or manual checks are named. |  |
| Results use approved validation statuses. |  |
| Failures and partial verification are preserved. |  |
| Stale validation is marked stale. |  |
| Follow-up validation is specific. |  |

Score:

## Contamination Resistance

Score whether the run keeps unrelated agent state separated.

| Check | Notes |
| --- | --- |
| Owner ID is unique and consistent. |  |
| `OWNER.md` defines the write boundary. |  |
| Agent B adopts only the supplied scope. |  |
| No unrelated ledger scopes are modified. |  |
| Subagent or parallel findings are passed by summary or explicit path. |  |

Score:

## Overall Result

| Total | Result |
| ---: | --- |
| 10-12 | Pass |
| 7-9 | Partial pass |
| 0-6 | Fail |

- Total score:
- Result:
- Required follow-up before release:
