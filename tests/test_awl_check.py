from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from tools.awl.check import check_scope
from tools.awl.cli import main as cli_main


class CheckScopeTests(unittest.TestCase):
    def test_valid_scope_has_no_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "valid-scope", machine_state=True)

            result = check_scope(scope)

            self.assertTrue(result.ok)
            self.assertEqual(result.scope_id, "valid-scope")
            self.assertEqual(result.findings, ())

    def test_missing_required_files_and_directories_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "missing-files", owner=False, directories=False)

            result = check_scope(scope)

            self.assertFalse(result.ok)
            self.assertIn("OWNER_MISSING", _codes(result))
            self.assertIn("EVIDENCE_DIR_MISSING", _codes(result))
            self.assertIn("NOTES_DIR_MISSING", _codes(result))

    def test_invalid_lifecycle_state_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "invalid-state", lifecycle="Reviewing")

            result = check_scope(scope)

            self.assertFalse(result.ok)
            self.assertIn("INVALID_LIFECYCLE_STATE", _codes(result))

    def test_stale_validation_status_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "stale-validation", validation="Stale")

            result = check_scope(scope)

            self.assertTrue(result.ok)

    def test_closed_ledger_requires_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "closed-without-outcome", lifecycle="Closed", outcome="")

            result = check_scope(scope)

            self.assertFalse(result.ok)
            self.assertIn("CLOSED_OUTCOME_MISSING", _codes(result))

    def test_conflicting_machine_state_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(
                Path(tmp),
                "conflicting-machine-state",
                machine_state={
                    "schema_version": "0.3",
                    "ledger_owner_id": "other-owner",
                    "owner_source": "generated-id",
                    "agent_runtime": "test",
                    "lifecycle_state": "Closed",
                    "created": "2026-06-20T00:00:00Z",
                    "last_updated": "2026-06-20T00:00:00Z",
                    "active_plan_version": 1,
                    "validation_status": "Failed",
                    "touched_files": [],
                    "evidence_files": [],
                },
            )

            result = check_scope(scope)

            self.assertFalse(result.ok)
            codes = _codes(result)
            self.assertIn("OWNER_ID_MISMATCH", codes)
            self.assertIn("MACHINE_STATE_LIFECYCLE_CONFLICT", codes)
            self.assertIn("MACHINE_STATE_VALIDATION_CONFLICT", codes)

    def test_missing_last_updated_is_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "missing-last-updated")
            ledger_path = scope / "ledger.md"
            text = ledger_path.read_text(encoding="utf-8")
            ledger_path.write_text(text.replace("Last updated: 2026-06-20T00:00:00Z\n", ""), encoding="utf-8")

            result = check_scope(scope)

            self.assertFalse(result.ok)
            self.assertIn("LAST_UPDATED_MISSING", _codes(result))

    def test_progress_requires_checkbox(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "no-progress-checkbox")
            ledger_path = scope / "ledger.md"
            text = ledger_path.read_text(encoding="utf-8")
            ledger_path.write_text(text.replace("- [x] Fixture created.", "- Fixture created."), encoding="utf-8")

            result = check_scope(scope)

            self.assertFalse(result.ok)
            self.assertIn("PROGRESS_CHECKBOX_MISSING", _codes(result))

    def test_empty_next_actions_and_decision_log_are_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "empty-sections")
            ledger_path = scope / "ledger.md"
            text = ledger_path.read_text(encoding="utf-8")
            text = text.replace(
                """## Decision log

- Decision: Use unittest fixtures.
  Rationale: Avoid external dependencies.
  Alternatives considered: pytest fixtures.
  Consequences: Tests run with stdlib.
  Date/Author: 2026-06-20T00:00:00Z / test

## Validation evidence""",
                """## Decision log

## Validation evidence""",
            )
            text = text.replace(
                """## Next actions

1. Continue.

## Recovery notes""",
                """## Next actions

## Recovery notes""",
            )
            ledger_path.write_text(text, encoding="utf-8")

            result = check_scope(scope)

            self.assertTrue(result.ok)
            self.assertIn("LEDGER_SECTION_EMPTY", _codes(result))

    def test_validation_entry_missing_evidence_is_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "missing-validation-evidence")
            ledger_path = scope / "ledger.md"
            text = ledger_path.read_text(encoding="utf-8")
            ledger_path.write_text(text.replace("  Evidence: Static fixture content.\n", ""), encoding="utf-8")

            result = check_scope(scope)

            self.assertTrue(result.ok)
            self.assertIn("VALIDATION_EVIDENCE_MISSING", _codes(result))

    def test_cli_returns_nonzero_for_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scope = _write_scope(Path(tmp), "invalid-state", lifecycle="Reviewing")
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(["check", str(scope), "--format", "json"])

            payload = json.loads(stdout.getvalue())

            self.assertEqual(exit_code, 1)
            self.assertEqual(payload["scope_id"], "invalid-state")


def _write_scope(
    root: Path,
    name: str,
    *,
    lifecycle: str = "Active",
    validation: str = "Passed",
    outcome: str = "Task is still active; no closeout yet.",
    owner: bool = True,
    directories: bool = True,
    machine_state: bool | dict[str, object] = False,
) -> Path:
    scope = root / name
    scope.mkdir()
    if directories:
        (scope / "evidence").mkdir()
        (scope / "notes").mkdir()

    if owner:
        (scope / "OWNER.md").write_text(_owner_text(name), encoding="utf-8")

    (scope / "ledger.md").write_text(
        _ledger_text(name, lifecycle=lifecycle, validation=validation, outcome=outcome),
        encoding="utf-8",
    )

    if machine_state:
        if isinstance(machine_state, dict):
            state = machine_state
        else:
            state = {
                "schema_version": "0.3",
                "ledger_owner_id": name,
                "owner_source": "generated-id",
                "agent_runtime": "test",
                "lifecycle_state": lifecycle,
                "created": "2026-06-20T00:00:00Z",
                "last_updated": "2026-06-20T00:00:00Z",
                "active_plan_version": 1,
                "validation_status": validation,
                "touched_files": [],
                "evidence_files": [],
            }
        (scope / "machine-state.json").write_text(json.dumps(state), encoding="utf-8")

    return scope


def _owner_text(owner_id: str) -> str:
    return f"""# Working Ledger Owner

Ledger owner ID: {owner_id}
Owner source: generated-id
Agent runtime: test
Created: 2026-06-20T00:00:00Z
Created by: test
Scope path: working-ledger/{owner_id}
Primary ledger: ledger.md

## Ownership rule

This ledger scope belongs to the agent thread or assigned continuation
explicitly identified above.
"""


def _ledger_text(owner_id: str, *, lifecycle: str, validation: str, outcome: str) -> str:
    return f"""# Test Ledger

Ledger schema version: 0.3
Lifecycle State: {lifecycle}
Created: 2026-06-20T00:00:00Z
Last updated: 2026-06-20T00:00:00Z
Ledger owner ID: {owner_id}
Owner source: generated-id
Agent/runtime: test
User objective: Validate checker behavior.
Ledger scope: working-ledger/{owner_id}
Primary ledger: working-ledger/{owner_id}/ledger.md
Related branch/issue/plan/ledger: Not Applicable

## Current objective

Validate checker behavior.

## Current state summary

Fixture scope for tests.

## Assumptions

- [Confirmed] Tests create temporary scopes.

## Progress

- [x] Fixture created.

## Active plan

Run the checker.

## Discoveries

- Observation: Fixture exists.
  Evidence: Test helper wrote files.
  Impact: Checker can inspect them.

## Decision log

- Decision: Use unittest fixtures.
  Rationale: Avoid external dependencies.
  Alternatives considered: pytest fixtures.
  Consequences: Tests run with stdlib.
  Date/Author: 2026-06-20T00:00:00Z / test

## Validation evidence

- Command/check: Fixture validation
  Result: {validation}
  Evidence: Static fixture content.
  Follow-up: None.

Overall validation status: {validation}

## Blockers and risks

- Blocker/risk: None known.
  Impact: None.
  Next action: Continue.

## Next actions

1. Continue.

## Recovery notes

To resume safely:
1. Read this ledger.
2. Run the checker.

## Outcome / retrospective

{outcome}
"""


def _codes(result: object) -> set[str]:
    return {finding.code for finding in result.findings}


if __name__ == "__main__":
    unittest.main()
