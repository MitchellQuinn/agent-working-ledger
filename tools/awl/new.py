from __future__ import annotations

import json
import re
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


OWNER_SOURCE_VALUES = {
    "session-id",
    "generated-id",
    "user-assigned",
    "wrapper-assigned",
}

OWNER_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class NewLedgerError(Exception):
    """Raised when a ledger scope cannot be safely created."""


@dataclass(frozen=True)
class NewLedgerResult:
    scope_id: str
    scope: str
    owner: str
    ledger: str
    evidence: str
    notes: str
    handoff: str | None = None
    machine_state: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "scope_id": self.scope_id,
            "scope": self.scope,
            "owner": self.owner,
            "ledger": self.ledger,
            "evidence": self.evidence,
            "notes": self.notes,
            "handoff": self.handoff,
            "machine_state": self.machine_state,
        }


def create_ledger(
    title: str,
    *,
    root: str | Path = "working-ledger",
    slug: str | None = None,
    owner_id: str | None = None,
    owner_source: str | None = None,
    runtime: str = "generic-agent",
    created_by: str = "awl",
    objective: str | None = None,
    related: str = "Not Applicable",
    handoff: bool = False,
    machine_state: bool = False,
    now: datetime | None = None,
) -> NewLedgerResult:
    title = title.strip()
    if not title:
        raise NewLedgerError("Task title must not be empty.")

    if owner_source is not None and owner_source not in OWNER_SOURCE_VALUES:
        allowed = ", ".join(sorted(OWNER_SOURCE_VALUES))
        raise NewLedgerError(f"Invalid owner source {owner_source!r}; expected one of: {allowed}.")

    timestamp = _utc_timestamp(now)
    normalized_runtime = _slugify(runtime) or "generic-agent"
    if owner_id is None:
        owner_id = _generated_owner_id(timestamp, normalized_runtime, slug)
        owner_source = owner_source or "generated-id"
    else:
        owner_id = owner_id.strip()
        _validate_owner_id(owner_id)
        owner_source = owner_source or "user-assigned"

    root_path = Path(root)
    scope_path = root_path / owner_id
    owner_path = scope_path / "OWNER.md"
    ledger_path = scope_path / "ledger.md"
    evidence_path = scope_path / "evidence"
    notes_path = scope_path / "notes"
    handoff_path = scope_path / "handoff.md"
    machine_state_path = scope_path / "machine-state.json"

    if scope_path.exists():
        raise NewLedgerError(f"Ledger scope already exists: {scope_path}")

    root_path.mkdir(parents=True, exist_ok=True)
    scope_path.mkdir()
    evidence_path.mkdir()
    notes_path.mkdir()

    objective_text = objective.strip() if objective else title
    related_text = related.strip() if related else "Not Applicable"

    owner_path.write_text(
        _owner_text(
            owner_id=owner_id,
            owner_source=owner_source,
            runtime=runtime,
            created=timestamp,
            created_by=created_by,
            scope=scope_path,
        ),
        encoding="utf-8",
    )
    ledger_path.write_text(
        _ledger_text(
            title=title,
            owner_id=owner_id,
            owner_source=owner_source,
            runtime=runtime,
            created=timestamp,
            created_by=created_by,
            objective=objective_text,
            scope=scope_path,
            related=related_text,
        ),
        encoding="utf-8",
    )

    created_handoff: str | None = None
    if handoff:
        handoff_path.write_text(
            _handoff_text(
                owner_id=owner_id,
                created=timestamp,
                objective=objective_text,
                scope=scope_path,
            ),
            encoding="utf-8",
        )
        created_handoff = str(handoff_path)

    created_machine_state: str | None = None
    if machine_state:
        state = {
            "schema_version": "0.3",
            "ledger_owner_id": owner_id,
            "owner_source": owner_source,
            "agent_runtime": runtime,
            "lifecycle_state": "Created",
            "created": timestamp,
            "last_updated": timestamp,
            "active_plan_version": 1,
            "validation_status": "Not Run",
            "touched_files": [],
            "evidence_files": [],
        }
        machine_state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        created_machine_state = str(machine_state_path)

    return NewLedgerResult(
        scope_id=owner_id,
        scope=str(scope_path),
        owner=str(owner_path),
        ledger=str(ledger_path),
        evidence=str(evidence_path),
        notes=str(notes_path),
        handoff=created_handoff,
        machine_state=created_machine_state,
    )


def format_new_text(result: NewLedgerResult) -> str:
    lines = [
        f"Ledger scope ID: {result.scope_id}",
        f"Created ledger scope: {result.scope}",
        f"OWNER.md: {result.owner}",
        f"ledger.md: {result.ledger}",
        f"evidence/: {result.evidence}",
        f"notes/: {result.notes}",
    ]
    if result.handoff:
        lines.append(f"handoff.md: {result.handoff}")
    if result.machine_state:
        lines.append(f"machine-state.json: {result.machine_state}")
    return "\n".join(lines)


def _utc_timestamp(now: datetime | None) -> str:
    value = now or datetime.now(UTC)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _generated_owner_id(timestamp: str, runtime: str, slug: str | None) -> str:
    parts = [timestamp, runtime, secrets.token_hex(2)]
    if slug:
        normalized_slug = _slugify(slug)
        if normalized_slug:
            parts.append(normalized_slug)
    return "-".join(parts)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return slug.strip("-")


def _validate_owner_id(owner_id: str) -> None:
    if not owner_id:
        raise NewLedgerError("Owner ID must not be empty.")
    if owner_id in {".", ".."}:
        raise NewLedgerError("Owner ID must be a safe path segment.")
    if "/" in owner_id or "\\" in owner_id:
        raise NewLedgerError("Owner ID must not contain path separators.")
    if not OWNER_ID_RE.fullmatch(owner_id):
        raise NewLedgerError(
            "Owner ID must start with a letter or number and contain only letters, numbers, dots, underscores, or hyphens."
        )


def _owner_text(
    *,
    owner_id: str,
    owner_source: str,
    runtime: str,
    created: str,
    created_by: str,
    scope: Path,
) -> str:
    return f"""# Working Ledger Owner

Ledger owner ID: {owner_id}
Owner source: {owner_source}
Agent runtime: {runtime}
Created: {created}
Created by: {created_by}
Scope path: {scope}
Primary ledger: ledger.md

## Ownership rule

This ledger scope belongs to the agent thread or assigned continuation
explicitly identified above.

Agents must not update this scope unless:

1. They created it.
2. The user explicitly directed them to use it.
3. A wrapper or project instruction explicitly assigned it.

Agents must not update unrelated working-ledger scopes merely because they
exist.
"""


def _ledger_text(
    *,
    title: str,
    owner_id: str,
    owner_source: str,
    runtime: str,
    created: str,
    created_by: str,
    objective: str,
    scope: Path,
    related: str,
) -> str:
    return f"""# {title}

Ledger schema version: 0.3
Lifecycle State: Created
Created: {created}
Last updated: {created}
Ledger owner ID: {owner_id}
Owner source: {owner_source}
Agent/runtime: {runtime}
User objective: {objective}
Ledger scope: {scope}
Primary ledger: {scope / "ledger.md"}
Related branch/issue/plan/ledger: {related}

## Current objective

{objective}

## Current state summary

Ledger scope created. No task work has been performed yet.

## Assumptions

- [Unconfirmed] Relevant repository and task context still need orientation.

## Progress

- [x] Create working-ledger scope.
- [ ] Orient to the relevant repository and task context.
- [ ] Write or revise the active plan before implementation.

## Active plan

Orient to the relevant context, confirm assumptions, then update this ledger
before implementation work begins.

## Discoveries

- Observation: No discoveries recorded yet.
  Evidence: Ledger was just created.
  Impact: Orientation is the next step.

## Decision log

- Decision: Create a task-local working ledger scope.
  Rationale: The work may need durable execution state.
  Alternatives considered: Proceed without a ledger.
  Consequences: Future progress, discoveries, decisions, validation, and
    recovery notes should be recorded here.
  Date/Author: {created} / {created_by}

## Validation evidence

- Command/check: Initial ledger creation
  Result: Not Run
  Evidence: Scope has been created; task validation has not run yet.
  Follow-up: Run task-specific validation after implementation begins.

Overall validation status: Not Run

## Blockers and risks

- Blocker/risk: Task context has not been inspected yet.
  Impact: Implementation should not begin until orientation is complete.
  Next action: Inspect relevant files, instructions, plans, and tests.

## Next actions

1. Read this ledger and confirm the active scope.
2. Orient to the relevant repository and task context.
3. Update assumptions, active plan, and recovery notes before implementation.

## Recovery notes

To resume safely:

1. Read this ledger.
2. Confirm this is the active ledger scope: {scope}
3. Inspect relevant project instructions, source files, plans, and tests.
4. Re-check assumptions after orientation.
5. Run task-specific validation after implementation begins.
6. Do not adopt unrelated `working-ledger/` scopes unless the user explicitly
   assigns one.
7. Watch out for stale validation after future changes.

## Outcome / retrospective

Not completed yet. This ledger is newly created and remains open.
"""


def _handoff_text(*, owner_id: str, created: str, objective: str, scope: Path) -> str:
    return f"""# Handoff

Scope ID: {owner_id}
Active ledger: {scope}
Ledger owner ID: {owner_id}
Lifecycle state: Created
Last updated: {created}

This file is a compressed continuation note. It does not replace `ledger.md`,
which remains the task-state authority.

## Current objective

{objective}

## Current state

Ledger scope has been created. No task work has been performed yet.

## Files touched

- {scope / "OWNER.md"}: owner marker created.
- {scope / "ledger.md"}: primary ledger created.

## Do next

1. Read `ledger.md`.
2. Orient to the relevant repository and task context.
3. Update the ledger before implementation begins.

## Do not redo

- Do not create another ledger unless this scope is intentionally abandoned or
  superseded.

## Known traps

- Do not adopt unrelated `working-ledger/` scopes by guessing.

## Validation status

- Not Run. Task-specific validation has not started.

## Resume command/checks

- Run `awl check {scope}` or `python -m tools.awl check {scope}`.
"""
