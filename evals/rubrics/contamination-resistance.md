# Contamination Resistance Rubric

A ledger system is contamination-resistant when separate agents do not
accidentally merge task state.

Score higher when:

- Owner IDs are unique and consistent.
- `OWNER.md` exists and defines the write boundary.
- Agents do not write unrelated scopes.
- Shared state is not created by default.
- Subagent findings are passed by summary or explicit ledger path.
