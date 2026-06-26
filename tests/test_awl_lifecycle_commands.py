from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from agent_working_ledger.check import check_scope
from agent_working_ledger.cli import main as cli_main
from agent_working_ledger.close import CloseLedgerError, close_ledger, format_close_text
from agent_working_ledger.new import create_ledger
from agent_working_ledger.supersede import SupersedeLedgerError, format_supersede_text, supersede_ledger


class CloseLedgerTests(unittest.TestCase):
    def test_close_updates_ledger_and_machine_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Close task", root=Path(tmp), owner_id="close-owner", machine_state=True)

            close_result = close_ledger(
                result.scope,
                outcome="Implementation complete.",
                validation_status="Passed",
                remaining_risks="None known.",
                follow_up="No follow-up needed.",
            )

            ledger_text = Path(close_result.ledger).read_text(encoding="utf-8")
            state = json.loads(Path(close_result.machine_state).read_text(encoding="utf-8"))
            self.assertIn("Lifecycle State: Closed", ledger_text)
            self.assertIn("Overall validation status: Passed", ledger_text)
            self.assertEqual(state["lifecycle_state"], "Closed")
            self.assertEqual(state["validation_status"], "Passed")
            self.assertEqual(close_result.scope_id, "close-owner")
            self.assertIn("Ledger scope ID: close-owner\n", format_close_text(close_result))
            self.assertTrue(check_scope(result.scope).ok)

    def test_close_refuses_schema_invalid_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Invalid close", root=Path(tmp), owner_id="invalid-close")
            ledger_path = Path(result.ledger)
            ledger_path.write_text(ledger_path.read_text(encoding="utf-8").replace("Lifecycle State: Created", "Lifecycle State: Reviewing"), encoding="utf-8")

            with self.assertRaises(CloseLedgerError):
                close_ledger(
                    result.scope,
                    outcome="Done.",
                    validation_status="Passed",
                    remaining_risks="None.",
                    follow_up="None.",
                )

    def test_close_updates_only_specified_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = create_ledger("Target", root=root, owner_id="target")
            other = create_ledger("Other", root=root, owner_id="other")
            other_before = Path(other.ledger).read_text(encoding="utf-8")

            close_ledger(
                target.scope,
                outcome="Done.",
                validation_status="Passed",
                remaining_risks="None.",
                follow_up="None.",
            )

            self.assertEqual(Path(other.ledger).read_text(encoding="utf-8"), other_before)

    def test_cli_close_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("CLI close", root=Path(tmp), owner_id="cli-close")
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "close",
                        result.scope,
                        "--outcome",
                        "Done.",
                        "--validation-status",
                        "Passed",
                        "--remaining-risks",
                        "None.",
                        "--follow-up",
                        "None.",
                        "--format",
                        "json",
                    ]
                )

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["scope_id"], "cli-close")
            self.assertEqual(payload["lifecycle_state"], "Closed")


class SupersedeLedgerTests(unittest.TestCase):
    def test_supersede_updates_ledger_and_machine_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Supersede task", root=Path(tmp), owner_id="supersede-owner", machine_state=True)

            supersede_result = supersede_ledger(
                result.scope,
                superseded_by="working-ledger/replacement-owner",
                reason="Replacement scope has clearer ownership.",
            )

            ledger_text = Path(supersede_result.ledger).read_text(encoding="utf-8")
            state = json.loads(Path(supersede_result.machine_state).read_text(encoding="utf-8"))
            self.assertIn("Lifecycle State: Superseded", ledger_text)
            self.assertIn("Superseded by: working-ledger/replacement-owner", ledger_text)
            self.assertEqual(state["lifecycle_state"], "Superseded")
            self.assertEqual(supersede_result.scope_id, "supersede-owner")
            self.assertIn("Ledger scope ID: supersede-owner\n", format_supersede_text(supersede_result))
            self.assertTrue(check_scope(result.scope).ok)

    def test_supersede_refuses_schema_invalid_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Invalid supersede", root=Path(tmp), owner_id="invalid-supersede")
            ledger_path = Path(result.ledger)
            ledger_path.write_text(ledger_path.read_text(encoding="utf-8").replace("Lifecycle State: Created", "Lifecycle State: Reviewing"), encoding="utf-8")

            with self.assertRaises(SupersedeLedgerError):
                supersede_ledger(
                    result.scope,
                    superseded_by="working-ledger/replacement",
                    reason="Invalid ledger should not be superseded.",
                )

    def test_supersede_updates_only_specified_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = create_ledger("Target", root=root, owner_id="target")
            other = create_ledger("Other", root=root, owner_id="other")
            other_before = Path(other.ledger).read_text(encoding="utf-8")

            supersede_ledger(
                target.scope,
                superseded_by="working-ledger/replacement",
                reason="Use replacement.",
            )

            self.assertEqual(Path(other.ledger).read_text(encoding="utf-8"), other_before)

    def test_cli_supersede_errors_on_missing_scope(self) -> None:
        stderr = StringIO()
        with redirect_stderr(stderr):
            exit_code = cli_main(
                [
                    "supersede",
                    "does-not-exist",
                    "--by",
                    "working-ledger/replacement",
                    "--reason",
                    "Missing scope.",
                ]
            )

        self.assertEqual(exit_code, 1)
        self.assertIn("schema-invalid", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
