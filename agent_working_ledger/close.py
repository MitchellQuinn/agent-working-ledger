from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .check import check_scope
from .markdown import VALID_VALIDATION_STATUSES, replace_field, replace_section, section


class CloseLedgerError(Exception):
    """Raised when a ledger cannot be safely closed."""


@dataclass(frozen=True)
class CloseLedgerResult:
    scope_id: str
    scope: str
    ledger: str
    machine_state: str | None
    lifecycle_state: str = "Closed"

    def as_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "scope": self.scope,
            "ledger": self.ledger,
            "machine_state": self.machine_state,
            "lifecycle_state": self.lifecycle_state,
        }


def close_ledger(
    scope: str | Path,
    *,
    outcome: str,
    validation_status: str,
    remaining_risks: str,
    follow_up: str,
    now: datetime | None = None,
) -> CloseLedgerResult:
    scope_path = Path(scope)
    ledger_path = scope_path / "ledger.md"
    machine_state_path = scope_path / "machine-state.json"

    _require_text("outcome", outcome)
    _require_text("remaining risks", remaining_risks)
    _require_text("follow-up", follow_up)
    if validation_status not in VALID_VALIDATION_STATUSES:
        raise CloseLedgerError(f"Invalid validation status: {validation_status}")

    check = check_scope(scope_path)
    if check.error_count:
        raise CloseLedgerError(f"Refusing to close schema-invalid ledger: {check.error_count} error(s)")
    if not ledger_path.is_file():
        raise CloseLedgerError(f"ledger.md is missing: {ledger_path}")

    timestamp = _utc_timestamp(now)
    ledger_text = ledger_path.read_text(encoding="utf-8")
    ledger_text = replace_field(ledger_text, "Lifecycle State", "Closed")
    ledger_text = replace_field(ledger_text, "Last updated", timestamp)
    try:
        ledger_text = replace_field(ledger_text, "Overall validation status", validation_status)
    except ValueError:
        pass
    existing_validation = section(ledger_text, "Validation evidence")
    ledger_text = replace_section(
        ledger_text,
        "Current state summary",
        f"Closed at {timestamp}.\n\n{outcome}",
    )
    ledger_text = replace_section(
        ledger_text,
        "Validation evidence",
        f"""{existing_validation}

- Command/check: Closeout validation status
  Result: {validation_status}
  Evidence: {outcome}
  Follow-up: {follow_up}

Overall validation status: {validation_status}""",
    )
    ledger_text = replace_section(
        ledger_text,
        "Blockers and risks",
        f"""- Blocker/risk: {remaining_risks}
  Impact: Remaining closeout risk or follow-up.
  Next action: {follow_up}""",
    )
    ledger_text = replace_section(ledger_text, "Next actions", f"1. {follow_up}")
    ledger_text = replace_section(
        ledger_text,
        "Recovery notes",
        f"""This ledger was closed at {timestamp}.

To resume safely:
1. Read this ledger.
2. Review remaining risks: {remaining_risks}
3. Follow up: {follow_up}
4. Create or adopt a new explicitly supplied ledger before continuing task-state writes.""",
    )
    ledger_text = replace_section(
        ledger_text,
        "Outcome / retrospective",
        f"""Outcome: {outcome}

Final validation status: {validation_status}

Remaining risks: {remaining_risks}

Follow-up: {follow_up}

Closed: {timestamp}""",
    )
    ledger_path.write_text(ledger_text, encoding="utf-8")

    updated_machine_state: str | None = None
    if machine_state_path.is_file():
        _update_machine_state(machine_state_path, timestamp, "Closed", validation_status)
        updated_machine_state = str(machine_state_path)

    return CloseLedgerResult(
        scope_id=scope_path.name,
        scope=str(scope_path),
        ledger=str(ledger_path),
        machine_state=updated_machine_state,
    )


def format_close_text(result: CloseLedgerResult) -> str:
    lines = [
        f"Ledger scope ID: {result.scope_id}",
        f"Closed ledger scope: {result.scope}",
        f"ledger.md: {result.ledger}",
    ]
    if result.machine_state:
        lines.append(f"machine-state.json: {result.machine_state}")
    return "\n".join(lines)


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise CloseLedgerError(f"{name} must not be empty.")


def _utc_timestamp(now: datetime | None) -> str:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _update_machine_state(path: Path, timestamp: str, lifecycle: str, validation_status: str) -> None:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CloseLedgerError(f"machine-state.json is not valid JSON: {exc}") from exc
    if not isinstance(state, dict):
        raise CloseLedgerError("machine-state.json must contain a JSON object.")

    state["lifecycle_state"] = lifecycle
    state["last_updated"] = timestamp
    state["validation_status"] = validation_status
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
