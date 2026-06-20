# Threat And Privacy Model

Agent Working Ledger is designed to improve resumability without turning a
repository into uncontrolled shared memory.

## Primary Risks

- Silent adoption of an unrelated ledger.
- Multiple agents writing into the same scope without explicit assignment.
- Treating `working-ledger/` as a shared scratchpad.
- Recording aspirational progress as actual progress.
- Marking validation as passed after later changes make it stale.
- Storing secrets, credentials, private keys, tokens, or unnecessary personal
  data in task-state files.
- Copying large logs or proprietary material that is not needed for resumption.
- Letting wrapper instructions redefine the core ledger schema.

## Controls

- Each thread writes to exactly one active ledger scope.
- `OWNER.md` is the write-boundary authority for a scope.
- Existing ledgers are discoverable artifacts, not automatically adoptable
  memory.
- `ledger.md` is the human-readable authority; optional machine state only
  mirrors it.
- Validation entries use the approved status set and record evidence.
- Large evidence is referenced from `evidence/` instead of pasted into the main
  ledger.
- Shared cross-ledger files are created only when the user explicitly asks for
  them, and they must be marked as human-requested shared state.

## Publication Assumption

Ledgers are not automatically safe to publish. Treat them as task-local working
state that may contain repository details or private operational context. Redact
or summarize sensitive material before committing, sharing, or handing off.
