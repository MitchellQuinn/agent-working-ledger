from __future__ import annotations

import re
from dataclasses import dataclass


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
class ValidationEntry:
    command_check: str
    result: str | None
    evidence: str | None
    follow_up: str | None

    def as_dict(self) -> dict[str, str | None]:
        return {
            "command_check": self.command_check,
            "result": self.result,
            "evidence": self.evidence,
            "follow_up": self.follow_up,
        }


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:\s*(.*?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE) is not None


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^## .*$", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def has_substantive_content(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if PLACEHOLDER_RE.fullmatch(stripped):
        return False
    if stripped.lower() in {"todo", "tbd", "n/a", "not applicable"}:
        return False
    return True


def has_placeholder(value: str) -> bool:
    return PLACEHOLDER_RE.search(value) is not None


def checkbox_count(text: str) -> int:
    return len(re.findall(r"^\s*-\s+\[[ xX]\]\s+", text, re.MULTILINE))


def validation_status_values(text: str) -> list[str]:
    statuses: list[str] = []
    for field_name in ("Result", "Overall validation status"):
        for match in re.finditer(rf"^\s*{re.escape(field_name)}:\s*(.*?)\s*$", text, re.MULTILINE):
            statuses.append(match.group(1).strip())
    return statuses


def validation_entries(text: str) -> list[ValidationEntry]:
    validation_text = section(text, "Validation evidence")
    if not validation_text:
        return []

    entries: list[dict[str, str | None]] = []
    current: dict[str, str | None] | None = None
    for raw_line in validation_text.splitlines():
        line = raw_line.rstrip()
        command_match = re.match(r"^\s*-\s+Command/check:\s*(.*?)\s*$", line)
        if command_match:
            if current is not None:
                entries.append(current)
            current = {
                "command_check": command_match.group(1).strip(),
                "result": None,
                "evidence": None,
                "follow_up": None,
            }
            continue

        if current is None:
            continue

        value_match = re.match(r"^\s*(Result|Evidence|Follow-up):\s*(.*?)\s*$", line)
        if value_match:
            key = value_match.group(1)
            value = value_match.group(2).strip()
            if key == "Result":
                current["result"] = value
            elif key == "Evidence":
                current["evidence"] = value
            elif key == "Follow-up":
                current["follow_up"] = value

    if current is not None:
        entries.append(current)

    return [
        ValidationEntry(
            command_check=entry["command_check"] or "",
            result=entry["result"],
            evidence=entry["evidence"],
            follow_up=entry["follow_up"],
        )
        for entry in entries
    ]


def replace_field(text: str, name: str, value: str) -> str:
    pattern = rf"^{re.escape(name)}:\s*.*?$"
    replacement = f"{name}: {value}"
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count == 0:
        raise ValueError(f"Field not found: {name}")
    return updated


def replace_section(text: str, heading: str, body: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"Section not found: {heading}")
    start = match.end()
    next_heading = re.search(r"^## .*$", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    normalized_body = body.strip()
    replacement = f"\n\n{normalized_body}\n\n"
    return text[:start] + replacement + text[end:].lstrip("\n")
