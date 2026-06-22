# Generic CLI Agent Prompt Wrapper

Use this wrapper for agents without first-class skill support.

Before beginning long-running, multi-step, exploratory, validation-heavy, or
handoff-prone work, create or adopt exactly one active ledger scope.

Rules:

1. Use a real session or thread ID if available.
2. Otherwise mint `<UTC timestamp>-generic-agent-<short-random-nonce>`.
3. Create `working-ledger/<ledger-owner-id>/`.
4. Maintain `OWNER.md` and `ledger.md`.
5. Create `evidence/` and `notes/`.
6. Write only inside the active ledger scope.
7. Reflect the active scope ID as a standalone, copyable fragment in user
   updates; include the path too when useful.
8. Update the ledger at every meaningful checkpoint.
9. Treat `ledger.md` as the durable task-state authority.
10. Do not adopt unrelated scopes unless the user explicitly assigns one.
11. Distinguish plans, ledgers, evidence, and handoff notes.

Use only these validation statuses:

- Not Run
- Failed
- Passed
- Partially Verified
- Stale
- Not Applicable

Use only these lifecycle states:

- Created
- Oriented
- Planned
- Active
- Blocked
- Ready for Review
- Closed
- Superseded

Optional files are `handoff.md` and `machine-state.json` when useful. Optional
machine state uses `schema_version: "0.3"` because it tracks the ledger
schema/spec iteration, not the package release.
