from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VALID_LIFECYCLE_STATES = {
    "Created",
    "Oriented",
    "Planned",
    "Active",
    "Blocked",
    "Ready for Review",
    "Closed",
    "Superseded",
}

VALID_VALIDATION_STATUSES = {
    "Not Run",
    "Failed",
    "Passed",
    "Partially Verified",
    "Stale",
    "Not Applicable",
}

REQUIRED_LEDGER_HEADINGS = (
    "Current objective",
    "Current state summary",
    "Assumptions",
    "Progress",
    "Active plan",
    "Discoveries",
    "Decision log",
    "Validation evidence",
    "Blockers and risks",
    "Next actions",
    "Recovery notes",
    "Outcome / retrospective",
)

PLACEHOLDER_RE = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True)
class CheckResult:
    scope: str
    findings: tuple[Finding, ...]

    @property
    def error_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for finding in self.findings if finding.severity == "warning")

    @property
    def ok(self) -> bool:
        return self.error_count == 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "scope": self.scope,
            "ok": self.ok,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "findings": [finding.as_dict() for finding in self.findings],
        }


def check_scope(scope: str | Path) -> CheckResult:
    scope_path = Path(scope)
    findings: list[Finding] = []

    if not scope_path.exists():
        return CheckResult(
            scope=str(scope_path),
            findings=(
                Finding("error", "SCOPE_MISSING", "Ledger scope does not exist.", str(scope_path)),
            ),
        )

    if not scope_path.is_dir():
        return CheckResult(
            scope=str(scope_path),
            findings=(
                Finding("error", "SCOPE_NOT_DIRECTORY", "Ledger scope is not a directory.", str(scope_path)),
            ),
        )

    owner_path = scope_path / "OWNER.md"
    ledger_path = scope_path / "ledger.md"
    evidence_path = scope_path / "evidence"
    notes_path = scope_path / "notes"
    machine_state_path = scope_path / "machine-state.json"

    if not owner_path.is_file():
        findings.append(Finding("error", "OWNER_MISSING", "Required OWNER.md is missing.", str(owner_path)))
    if not ledger_path.is_file():
        findings.append(Finding("error", "LEDGER_MISSING", "Required ledger.md is missing.", str(ledger_path)))
    if not evidence_path.is_dir():
        findings.append(Finding("error", "EVIDENCE_DIR_MISSING", "Required evidence/ directory is missing.", str(evidence_path)))
    if not notes_path.is_dir():
        findings.append(Finding("error", "NOTES_DIR_MISSING", "Required notes/ directory is missing.", str(notes_path)))

    owner_text = _read_text(owner_path, findings)
    ledger_text = _read_text(ledger_path, findings)

    owner_id_values: list[tuple[str, str]] = [("scope path", scope_path.name)]

    if owner_text is not None:
        owner_id = _field(owner_text, "Ledger owner ID")
        if owner_id:
            owner_id_values.append(("OWNER.md", owner_id))
            _check_no_placeholder(owner_id, "OWNER_ID_PLACEHOLDER", "OWNER.md owner ID is still a placeholder.", owner_path, findings)
        else:
            findings.append(Finding("error", "OWNER_ID_MISSING", "OWNER.md is missing Ledger owner ID.", str(owner_path)))

    ledger_lifecycle: str | None = None
    ledger_validation_status: str | None = None

    if ledger_text is not None:
        ledger_owner_id = _field(ledger_text, "Ledger owner ID")
        if ledger_owner_id:
            owner_id_values.append(("ledger.md", ledger_owner_id))
            _check_no_placeholder(ledger_owner_id, "LEDGER_OWNER_ID_PLACEHOLDER", "ledger.md owner ID is still a placeholder.", ledger_path, findings)
        else:
            findings.append(Finding("error", "LEDGER_OWNER_ID_MISSING", "ledger.md is missing Ledger owner ID.", str(ledger_path)))

        ledger_lifecycle = _field(ledger_text, "Lifecycle State")
        if ledger_lifecycle:
            _check_enum(
                ledger_lifecycle,
                VALID_LIFECYCLE_STATES,
                "INVALID_LIFECYCLE_STATE",
                f"Invalid lifecycle state: {ledger_lifecycle}",
                ledger_path,
                findings,
            )
        else:
            findings.append(Finding("error", "LIFECYCLE_STATE_MISSING", "ledger.md is missing Lifecycle State.", str(ledger_path)))

        _check_required_headings(ledger_text, ledger_path, findings)
        _check_validation_statuses(ledger_text, ledger_path, findings)
        ledger_validation_status = _field(ledger_text, "Overall validation status")
        _check_closeout(ledger_text, ledger_lifecycle, ledger_path, findings)
        _check_superseded(ledger_text, ledger_lifecycle, ledger_path, findings)

    if machine_state_path.exists():
        _check_machine_state(
            machine_state_path,
            owner_id_values,
            ledger_lifecycle,
            ledger_validation_status,
            findings,
        )

    _check_owner_id_consistency(owner_id_values, findings)

    return CheckResult(scope=str(scope_path), findings=tuple(findings))


def format_text(result: CheckResult) -> str:
    lines = [
        f"Scope: {result.scope}",
        f"Result: {'OK' if result.ok else 'FAILED'} ({result.error_count} error(s), {result.warning_count} warning(s))",
    ]
    for finding in result.findings:
        location = f" [{finding.path}]" if finding.path else ""
        lines.append(f"{finding.severity.upper()} {finding.code}: {finding.message}{location}")
    return "\n".join(lines)


def _read_text(path: Path, findings: list[Finding]) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        findings.append(Finding("error", "TEXT_DECODE_ERROR", f"Could not read UTF-8 text: {exc}", str(path)))
    except OSError as exc:
        findings.append(Finding("error", "TEXT_READ_ERROR", f"Could not read file: {exc}", str(path)))
    return None


def _field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:\s*(.*?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def _check_no_placeholder(value: str, code: str, message: str, path: Path, findings: list[Finding]) -> None:
    if PLACEHOLDER_RE.search(value):
        findings.append(Finding("error", code, message, str(path)))


def _check_enum(
    value: str,
    allowed: set[str],
    code: str,
    message: str,
    path: Path,
    findings: list[Finding],
) -> None:
    if value not in allowed:
        findings.append(Finding("error", code, message, str(path)))


def _check_required_headings(text: str, path: Path, findings: list[Finding]) -> None:
    for heading in REQUIRED_LEDGER_HEADINGS:
        if not re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE):
            findings.append(Finding("error", "LEDGER_HEADING_MISSING", f"Missing required heading: ## {heading}", str(path)))


def _check_validation_statuses(text: str, path: Path, findings: list[Finding]) -> None:
    statuses: list[str] = []
    for field_name in ("Result", "Overall validation status"):
        for match in re.finditer(rf"^\s*{re.escape(field_name)}:\s*(.*?)\s*$", text, re.MULTILINE):
            statuses.append(match.group(1).strip())

    if not statuses:
        findings.append(Finding("warning", "VALIDATION_STATUS_ABSENT", "No validation status entries found.", str(path)))
        return

    for status in statuses:
        if status not in VALID_VALIDATION_STATUSES:
            findings.append(Finding("error", "INVALID_VALIDATION_STATUS", f"Invalid validation status: {status}", str(path)))


def _check_closeout(text: str, lifecycle: str | None, path: Path, findings: list[Finding]) -> None:
    if lifecycle != "Closed":
        return
    outcome = _section(text, "Outcome / retrospective")
    if not _has_substantive_content(outcome):
        findings.append(Finding("error", "CLOSED_OUTCOME_MISSING", "Closed ledger must include an outcome or retrospective.", str(path)))


def _check_superseded(text: str, lifecycle: str | None, path: Path, findings: list[Finding]) -> None:
    if lifecycle != "Superseded":
        return
    searchable = " ".join(
        part for part in (
            _section(text, "Current state summary"),
            _section(text, "Next actions"),
            _section(text, "Recovery notes"),
            _section(text, "Outcome / retrospective"),
        )
        if part
    ).lower()
    markers = ("superseded by", "replaced by", "continuation", "continue in", "superseding", "replaces")
    if not any(marker in searchable for marker in markers):
        findings.append(
            Finding(
                "warning",
                "SUPERSEDED_TARGET_UNCLEAR",
                "Superseded ledger should name what replaced it where possible.",
                str(path),
            )
        )


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## .*$", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def _has_substantive_content(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if PLACEHOLDER_RE.fullmatch(stripped):
        return False
    if stripped.lower() in {"todo", "tbd", "n/a", "not applicable"}:
        return False
    return True


def _check_owner_id_consistency(owner_id_values: list[tuple[str, str]], findings: list[Finding]) -> None:
    concrete = [(source, value) for source, value in owner_id_values if not PLACEHOLDER_RE.search(value)]
    if not concrete:
        return
    expected_source, expected_value = concrete[0]
    for source, value in concrete[1:]:
        if value != expected_value:
            findings.append(
                Finding(
                    "error",
                    "OWNER_ID_MISMATCH",
                    f"Owner ID mismatch: {source} has {value!r}, expected {expected_value!r} from {expected_source}.",
                )
            )


def _check_machine_state(
    path: Path,
    owner_id_values: list[tuple[str, str]],
    ledger_lifecycle: str | None,
    ledger_validation_status: str | None,
    findings: list[Finding],
) -> None:
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(Finding("error", "MACHINE_STATE_INVALID_JSON", f"machine-state.json is not valid JSON: {exc}", str(path)))
        return
    except OSError as exc:
        findings.append(Finding("error", "MACHINE_STATE_READ_ERROR", f"Could not read machine-state.json: {exc}", str(path)))
        return

    if not isinstance(state, dict):
        findings.append(Finding("error", "MACHINE_STATE_NOT_OBJECT", "machine-state.json must contain a JSON object.", str(path)))
        return

    schema_version = state.get("schema_version")
    if schema_version != "0.3":
        findings.append(Finding("warning", "MACHINE_STATE_SCHEMA_VERSION", "Expected machine-state.json schema_version to be \"0.3\".", str(path)))

    machine_owner_id = state.get("ledger_owner_id")
    if isinstance(machine_owner_id, str):
        owner_id_values.append(("machine-state.json", machine_owner_id))
    else:
        findings.append(Finding("error", "MACHINE_STATE_OWNER_ID_MISSING", "machine-state.json is missing ledger_owner_id.", str(path)))

    machine_lifecycle = state.get("lifecycle_state")
    if isinstance(machine_lifecycle, str):
        _check_enum(
            machine_lifecycle,
            VALID_LIFECYCLE_STATES,
            "MACHINE_STATE_INVALID_LIFECYCLE",
            f"Invalid machine-state lifecycle_state: {machine_lifecycle}",
            path,
            findings,
        )
        if ledger_lifecycle and machine_lifecycle != ledger_lifecycle:
            findings.append(
                Finding(
                    "error",
                    "MACHINE_STATE_LIFECYCLE_CONFLICT",
                    f"machine-state lifecycle_state {machine_lifecycle!r} conflicts with ledger.md {ledger_lifecycle!r}.",
                    str(path),
                )
            )

    machine_validation = state.get("validation_status")
    if isinstance(machine_validation, str):
        _check_enum(
            machine_validation,
            VALID_VALIDATION_STATUSES,
            "MACHINE_STATE_INVALID_VALIDATION_STATUS",
            f"Invalid machine-state validation_status: {machine_validation}",
            path,
            findings,
        )
        if ledger_validation_status and machine_validation != ledger_validation_status:
            findings.append(
                Finding(
                    "error",
                    "MACHINE_STATE_VALIDATION_CONFLICT",
                    f"machine-state validation_status {machine_validation!r} conflicts with ledger.md {ledger_validation_status!r}.",
                    str(path),
                )
            )
