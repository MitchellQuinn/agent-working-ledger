from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .check import check_scope
from .markdown import field, replace_field, replace_section


class SupersedeLedgerError(Exception):
    """Raised when a ledger cannot be safely superseded."""


@dataclass(frozen=True)
class SupersedeLedgerResult:
    scope: str
    ledger: str
    superseded_by: str
    machine_state: str | None
    lifecycle_state: str = "Superseded"

    def as_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope,
            "ledger": self.ledger,
            "superseded_by": self.superseded_by,
            "machine_state": self.machine_state,
            "lifecycle_state": self.lifecycle_state,
        }


def supersede_ledger(
    scope: str | Path,
    *,
    superseded_by: str,
    reason: str,
    useful: str = "Review this ledger for potentially useful discoveries, decisions, and validation evidence.",
    continuation: str | None = None,
    now: datetime | None = None,
) -> SupersedeLedgerResult:
    scope_path = Path(scope)
    ledger_path = scope_path / "ledger.md"
    machine_state_path = scope_path / "machine-state.json"

    _require_text("superseded-by target", superseded_by)
    _require_text("reason", reason)
    _require_text("useful work/evidence", useful)
    continuation_text = continuation.strip() if continuation else superseded_by.strip()

    check = check_scope(scope_path)
    if check.error_count:
        raise SupersedeLedgerError(f"Refusing to supersede schema-invalid ledger: {check.error_count} error(s)")
    if not ledger_path.is_file():
        raise SupersedeLedgerError(f"ledger.md is missing: {ledger_path}")

    timestamp = _utc_timestamp(now)
    ledger_text = ledger_path.read_text(encoding="utf-8")
    validation_status = field(ledger_text, "Overall validation status") or "Not Run"
    ledger_text = replace_field(ledger_text, "Lifecycle State", "Superseded")
    ledger_text = replace_field(ledger_text, "Last updated", timestamp)
    ledger_text = replace_section(
        ledger_text,
        "Current state summary",
        f"""Superseded at {timestamp}.

Superseded by: {superseded_by}

Reason: {reason}""",
    )
    ledger_text = replace_section(
        ledger_text,
        "Next actions",
        f"1. Continue in {continuation_text}",
    )
    ledger_text = replace_section(
        ledger_text,
        "Recovery notes",
        f"""This ledger was superseded at {timestamp}.

Superseded by: {superseded_by}

Reason: {reason}

Useful remaining work or evidence: {useful}

Continuation: {continuation_text}""",
    )
    ledger_text = replace_section(
        ledger_text,
        "Outcome / retrospective",
        f"""Superseded by: {superseded_by}

Reason: {reason}

Useful remaining work or evidence: {useful}

Continuation: {continuation_text}

Validation status at supersession: {validation_status}

Superseded: {timestamp}""",
    )
    ledger_path.write_text(ledger_text, encoding="utf-8")

    updated_machine_state: str | None = None
    if machine_state_path.is_file():
        _update_machine_state(machine_state_path, timestamp, "Superseded")
        updated_machine_state = str(machine_state_path)

    return SupersedeLedgerResult(
        scope=str(scope_path),
        ledger=str(ledger_path),
        superseded_by=superseded_by,
        machine_state=updated_machine_state,
    )


def format_supersede_text(result: SupersedeLedgerResult) -> str:
    lines = [
        f"Superseded ledger scope: {result.scope}",
        f"Superseded by: {result.superseded_by}",
        f"ledger.md: {result.ledger}",
    ]
    if result.machine_state:
        lines.append(f"machine-state.json: {result.machine_state}")
    return "\n".join(lines)


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise SupersedeLedgerError(f"{name} must not be empty.")


def _utc_timestamp(now: datetime | None) -> str:
    value = now or datetime.now(UTC)
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _update_machine_state(path: Path, timestamp: str, lifecycle: str) -> None:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SupersedeLedgerError(f"machine-state.json is not valid JSON: {exc}") from exc
    if not isinstance(state, dict):
        raise SupersedeLedgerError("machine-state.json must contain a JSON object.")

    state["lifecycle_state"] = lifecycle
    state["last_updated"] = timestamp
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
