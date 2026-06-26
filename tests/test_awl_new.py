from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

from agent_working_ledger.check import check_scope
from agent_working_ledger.cli import main as cli_main
from agent_working_ledger.new import NewLedgerError, create_ledger, format_new_text


class NewLedgerTests(unittest.TestCase):
    def test_create_ledger_passes_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger(
                "OAuth refresh fix",
                root=Path(tmp) / "working-ledger",
                owner_id="test-owner",
                runtime="codex",
            )

            check = check_scope(result.scope)

            self.assertTrue(check.ok)
            self.assertTrue(Path(result.owner).is_file())
            self.assertTrue(Path(result.ledger).is_file())
            self.assertTrue(Path(result.evidence).is_dir())
            self.assertTrue(Path(result.notes).is_dir())
            self.assertEqual(result.scope_id, "test-owner")

    def test_optional_handoff_and_machine_state_pass_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger(
                "Handoff ready task",
                root=Path(tmp) / "working-ledger",
                owner_id="sidecar-owner",
                handoff=True,
                machine_state=True,
            )

            check = check_scope(result.scope)
            machine_state = json.loads(Path(result.machine_state).read_text(encoding="utf-8"))

            self.assertTrue(check.ok)
            self.assertTrue(Path(result.handoff).is_file())
            self.assertIn("Scope ID: sidecar-owner", Path(result.handoff).read_text(encoding="utf-8"))
            self.assertEqual(machine_state["schema_version"], "0.3")
            self.assertEqual(machine_state["ledger_owner_id"], "sidecar-owner")
            self.assertEqual(machine_state["lifecycle_state"], "Created")
            self.assertEqual(machine_state["validation_status"], "Not Run")

    def test_refuses_to_overwrite_existing_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "working-ledger"
            create_ledger("First task", root=root, owner_id="same-owner")

            with self.assertRaises(NewLedgerError):
                create_ledger("Second task", root=root, owner_id="same-owner")

            ledger_text = (root / "same-owner" / "ledger.md").read_text(encoding="utf-8")
            self.assertIn("# First task", ledger_text)
            self.assertNotIn("# Second task", ledger_text)

    def test_rejects_owner_id_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(NewLedgerError):
                create_ledger("Unsafe task", root=Path(tmp) / "working-ledger", owner_id="../escape")

            self.assertFalse((Path(tmp) / "escape").exists())

    def test_generated_owner_id_uses_runtime_nonce_and_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger(
                "Generated task",
                root=Path(tmp) / "working-ledger",
                slug="OAuth Refresh Fix",
                runtime="Codex Desktop",
                now=datetime(2026, 6, 20, 14, 30, 12, tzinfo=timezone.utc),
            )

            owner_id = Path(result.scope).name
            self.assertRegex(owner_id, r"^20260620T143012Z-codex-desktop-[0-9a-f]{4}-oauth-refresh-fix$")
            self.assertEqual(result.scope_id, owner_id)
            self.assertTrue(check_scope(result.scope).ok)

    def test_text_output_includes_standalone_scope_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger(
                "Text output task",
                root=Path(tmp) / "working-ledger",
                owner_id="copyable-owner",
            )

            text = format_new_text(result)

            self.assertIn("Ledger scope ID: copyable-owner\n", text)
            self.assertIn(f"Created ledger scope: {result.scope}", text)

    def test_cli_new_json_output_and_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "new",
                        "CLI task",
                        "--root",
                        str(Path(tmp) / "working-ledger"),
                        "--owner-id",
                        "cli-owner",
                        "--machine-state",
                        "--format",
                        "json",
                    ]
                )

            payload = json.loads(stdout.getvalue())

            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["scope_id"], "cli-owner")
            self.assertEqual(Path(payload["scope"]).name, "cli-owner")
            self.assertTrue(check_scope(payload["scope"]).ok)

    def test_cli_new_returns_nonzero_for_existing_scope(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "working-ledger"
            create_ledger("First task", root=root, owner_id="existing-owner")
            stderr = StringIO()

            with redirect_stderr(stderr):
                exit_code = cli_main(
                    [
                        "new",
                        "Second task",
                        "--root",
                        str(root),
                        "--owner-id",
                        "existing-owner",
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("already exists", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
