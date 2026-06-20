# Anti-Patterns

Avoid these behaviours:

- Silently adopting the most recent ledger.
- Updating multiple ledger scopes in one task.
- Treating `working-ledger/` as shared memory.
- Treating `working-ledger/INDEX.md` as shared memory by default.
- Recording aspirational progress instead of actual progress.
- Marking work complete without validation evidence or an explicit non-run
  status.
- Leaving stale validation marked as passed.
- Hiding meaningful decisions in prose-only notes.
- Keeping an obsolete active plan after discoveries changed the approach.
- Using the ledger as a dumping ground for long logs.
- Storing secrets, credentials, private keys, tokens, or unnecessary personal
  data.
- Treating the ledger as a substitute for tests or source control.
- Using one ledger for unrelated tasks.
- Allowing subagents to write into a parent ledger without explicit instruction.
- Closing a ledger merely because the agent is stopping temporarily.
- Reopening closed ledgers without recording why.
- Letting wrappers redefine lifecycle states, validation statuses, or required
  ledger sections.
