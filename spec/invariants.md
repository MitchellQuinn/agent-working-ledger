# Architectural Invariants

These invariants are the core safety properties of Agent Working Ledger.

1. An agent may write to only one active ledger scope at a time.
2. A ledger scope is active only if it was created by the current thread,
   explicitly supplied by the user, or explicitly assigned by a wrapper or
   project instruction.
3. `working-ledger/` is a container for isolated scopes, not shared memory.
4. `OWNER.md` is the authority for scope identity and write permission.
5. `ledger.md` is the durable human-readable execution-state authority.
6. Optional machine-readable state mirrors the ledger and is never more
   authoritative than `ledger.md`.
7. Validation claims must be backed by command output, manual check notes,
   evidence references, or an explicit non-run status.
8. A ledger must be accurate enough for another agent or human to resume from it
   without the original chat.
9. Agents must not silently adopt the newest, nearest, or most plausible
   existing ledger.
10. Ledgers must not contain secrets, credentials, private keys, tokens, or
    unnecessary personal data.
11. Discoveries that change the approach must be reflected in the active plan.
12. Decisions must record rationale and consequences.
13. Closed ledgers must contain an outcome or retrospective.
14. Superseded ledgers must name what superseded them where possible.
15. Ledger updates must keep the document internally consistent.

See [SPEC.md](SPEC.md) for the normative specification.

