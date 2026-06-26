from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .check import check_scope
from .markdown import field

LEDGER_MARKERS = ("OWNER.md", "ledger.md", "evidence", "notes")


@dataclass(frozen=True)
class LedgerListEntry:
    scope_id: str
    scope: str
    owner_id: str | None
    lifecycle_state: str | None
    last_updated: str | None
    objective: str | None
    ok: bool
    error_count: int
    warning_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "scope": self.scope,
            "owner_id": self.owner_id,
            "lifecycle_state": self.lifecycle_state,
            "last_updated": self.last_updated,
            "objective": self.objective,
            "ok": self.ok,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
        }


@dataclass(frozen=True)
class LedgerListResult:
    root: str
    entries: tuple[LedgerListEntry, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "entries": [entry.as_dict() for entry in self.entries],
        }


def list_ledgers(root: str | Path = "working-ledger") -> LedgerListResult:
    root_path = Path(root)
    if not root_path.exists():
        return LedgerListResult(root=str(root_path), entries=())
    if not root_path.is_dir():
        check = check_scope(root_path)
        return LedgerListResult(
            root=str(root_path),
            entries=(
                LedgerListEntry(
                    scope_id=root_path.name,
                    scope=str(root_path),
                    owner_id=None,
                    lifecycle_state=None,
                    last_updated=None,
                    objective=None,
                    ok=check.ok,
                    error_count=check.error_count,
                    warning_count=check.warning_count,
                ),
            ),
        )

    if _has_ledger_marker(root_path):
        return LedgerListResult(root=str(root_path), entries=(_entry_for_scope(root_path),))

    entries: list[LedgerListEntry] = []
    for candidate in _discover_candidates(root_path):
        entries.append(_entry_for_scope(candidate))
    return LedgerListResult(root=str(root_path), entries=tuple(entries))


def format_list_text(result: LedgerListResult) -> str:
    lines = [f"Root: {result.root}", f"Ledgers: {len(result.entries)}"]
    for entry in result.entries:
        status = "OK" if entry.ok else f"FAILED ({entry.error_count} error(s), {entry.warning_count} warning(s))"
        lines.extend(
            [
                "",
                entry.scope,
                f"  Status: {status}",
                f"  Scope ID: {entry.scope_id}",
                f"  Owner ID: {entry.owner_id or 'Unknown'}",
                f"  Lifecycle state: {entry.lifecycle_state or 'Unknown'}",
                f"  Last updated: {entry.last_updated or 'Unknown'}",
                f"  Objective: {entry.objective or 'Unknown'}",
            ]
        )
    return "\n".join(lines)


def _read_ledger(scope: Path) -> str | None:
    ledger_path = scope / "ledger.md"
    if not ledger_path.is_file():
        return None
    try:
        return ledger_path.read_text(encoding="utf-8")
    except OSError:
        return None


def _entry_for_scope(scope: Path) -> LedgerListEntry:
    check = check_scope(scope)
    ledger_text = _read_ledger(scope)
    owner_id = field(ledger_text, "Ledger owner ID") if ledger_text else None
    return LedgerListEntry(
        scope_id=owner_id or scope.name,
        scope=str(scope),
        owner_id=owner_id,
        lifecycle_state=field(ledger_text, "Lifecycle State") if ledger_text else None,
        last_updated=field(ledger_text, "Last updated") if ledger_text else None,
        objective=field(ledger_text, "User objective") if ledger_text else None,
        ok=check.ok,
        error_count=check.error_count,
        warning_count=check.warning_count,
    )


def _discover_candidates(root: Path) -> tuple[Path, ...]:
    candidates: list[Path] = []
    for child in _child_dirs(root):
        if _has_ledger_marker(child):
            candidates.append(child)
            continue

        nested = _discover_marked_scopes(child)
        if nested:
            candidates.extend(nested)
        else:
            candidates.append(child)
    return tuple(candidates)


def _discover_marked_scopes(root: Path) -> tuple[Path, ...]:
    scopes: list[Path] = []
    for child in _child_dirs(root):
        if _has_ledger_marker(child):
            scopes.append(child)
        else:
            scopes.extend(_discover_marked_scopes(child))
    return tuple(scopes)


def _has_ledger_marker(scope: Path) -> bool:
    return any((scope / marker).exists() for marker in LEDGER_MARKERS)


def _child_dirs(root: Path) -> tuple[Path, ...]:
    return tuple(
        sorted(
            (path for path in root.iterdir() if path.is_dir()),
            key=lambda path: str(path).lower(),
        )
    )
