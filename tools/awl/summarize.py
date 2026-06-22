from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .markdown import field, section


class SummarizeError(Exception):
    """Raised when a ledger scope cannot be summarized."""


@dataclass(frozen=True)
class SummaryResult:
    scope_id: str
    scope: str
    owner_id: str | None
    lifecycle_state: str | None
    last_updated: str | None
    objective: str
    current_state: str
    next_actions: str
    blockers_and_risks: str
    validation_status: str | None
    validation_evidence: str
    recovery_notes: str
    handoff: str | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "scope": self.scope,
            "owner_id": self.owner_id,
            "lifecycle_state": self.lifecycle_state,
            "last_updated": self.last_updated,
            "objective": self.objective,
            "current_state": self.current_state,
            "next_actions": self.next_actions,
            "blockers_and_risks": self.blockers_and_risks,
            "validation_status": self.validation_status,
            "validation_evidence": self.validation_evidence,
            "recovery_notes": self.recovery_notes,
            "handoff": self.handoff,
        }


def summarize_scope(scope: str | Path) -> SummaryResult:
    scope_path = Path(scope)
    ledger_path = scope_path / "ledger.md"
    handoff_path = scope_path / "handoff.md"

    if not scope_path.exists():
        raise SummarizeError(f"Ledger scope does not exist: {scope_path}")
    if not scope_path.is_dir():
        raise SummarizeError(f"Ledger scope is not a directory: {scope_path}")
    if not ledger_path.is_file():
        raise SummarizeError(f"ledger.md is missing: {ledger_path}")

    ledger_text = ledger_path.read_text(encoding="utf-8")
    handoff_text = handoff_path.read_text(encoding="utf-8") if handoff_path.is_file() else None
    owner_id = field(ledger_text, "Ledger owner ID")

    return SummaryResult(
        scope_id=owner_id or scope_path.name,
        scope=str(scope_path),
        owner_id=owner_id,
        lifecycle_state=field(ledger_text, "Lifecycle State"),
        last_updated=field(ledger_text, "Last updated"),
        objective=_prefer_section(ledger_text, "Current objective", field(ledger_text, "User objective") or ""),
        current_state=section(ledger_text, "Current state summary"),
        next_actions=section(ledger_text, "Next actions"),
        blockers_and_risks=section(ledger_text, "Blockers and risks"),
        validation_status=field(ledger_text, "Overall validation status"),
        validation_evidence=section(ledger_text, "Validation evidence"),
        recovery_notes=section(ledger_text, "Recovery notes"),
        handoff=handoff_text,
    )


def format_summary_text(result: SummaryResult) -> str:
    lines = [
        f"Scope ID: {result.scope_id}",
        f"Scope: {result.scope}",
        f"Owner ID: {result.owner_id or 'Unknown'}",
        f"Lifecycle state: {result.lifecycle_state or 'Unknown'}",
        f"Last updated: {result.last_updated or 'Unknown'}",
        "",
        "Current objective:",
        _indent_or_placeholder(result.objective),
        "",
        "Current state:",
        _indent_or_placeholder(result.current_state),
        "",
        "Next actions:",
        _indent_or_placeholder(result.next_actions),
        "",
        "Blockers and risks:",
        _indent_or_placeholder(result.blockers_and_risks),
        "",
        f"Validation status: {result.validation_status or 'Unknown'}",
        "Validation evidence:",
        _indent_or_placeholder(result.validation_evidence),
        "",
        "Recovery notes:",
        _indent_or_placeholder(result.recovery_notes),
    ]
    if result.handoff:
        lines.extend(("", "Handoff note present: yes"))
    else:
        lines.extend(("", "Handoff note present: no"))
    return "\n".join(lines)


def _prefer_section(text: str, heading: str, fallback: str) -> str:
    value = section(text, heading)
    return value or fallback


def _indent_or_placeholder(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        return "  Not recorded."
    return "\n".join(f"  {line}" if line else "" for line in stripped.splitlines())
