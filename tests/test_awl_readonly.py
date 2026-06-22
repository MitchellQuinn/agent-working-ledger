from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from tools.awl.cli import main as cli_main
from tools.awl.list import list_ledgers
from tools.awl.new import create_ledger
from tools.awl.summarize import SummarizeError, summarize_scope


class SummarizeTests(unittest.TestCase):
    def test_summarize_valid_ledger_without_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Summarize task", root=Path(tmp), owner_id="summary-owner")

            summary = summarize_scope(result.scope)

            self.assertEqual(summary.scope_id, "summary-owner")
            self.assertEqual(summary.owner_id, "summary-owner")
            self.assertEqual(summary.lifecycle_state, "Created")
            self.assertIn("Summarize task", summary.objective)
            self.assertIsNone(summary.handoff)

    def test_summarize_includes_handoff_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("Handoff task", root=Path(tmp), owner_id="handoff-owner", handoff=True)

            summary = summarize_scope(result.scope)

            self.assertIsNotNone(summary.handoff)
            self.assertIn("# Handoff", summary.handoff)

    def test_summarize_reports_stale_blocked_and_closed_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stale = create_ledger("Stale task", root=Path(tmp), owner_id="stale-owner")
            _replace_in_ledger(stale.scope, "Overall validation status: Not Run", "Overall validation status: Stale")
            _replace_in_ledger(stale.scope, "Lifecycle State: Created", "Lifecycle State: Blocked")
            summary = summarize_scope(stale.scope)

            self.assertEqual(summary.validation_status, "Stale")
            self.assertEqual(summary.lifecycle_state, "Blocked")

            closed = create_ledger("Closed task", root=Path(tmp), owner_id="closed-owner")
            _replace_in_ledger(closed.scope, "Lifecycle State: Created", "Lifecycle State: Closed")
            summary = summarize_scope(closed.scope)
            self.assertEqual(summary.lifecycle_state, "Closed")

    def test_summarize_malformed_scope_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            malformed = Path(tmp) / "malformed"
            malformed.mkdir()

            with self.assertRaises(SummarizeError):
                summarize_scope(malformed)

    def test_cli_summarize_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = create_ledger("CLI summarize", root=Path(tmp), owner_id="cli-summary")
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(["summarize", result.scope, "--format", "json"])

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["scope_id"], "cli-summary")
            self.assertEqual(payload["owner_id"], "cli-summary")

    def test_cli_summarize_missing_scope_returns_nonzero(self) -> None:
        stderr = StringIO()
        with redirect_stderr(stderr):
            exit_code = cli_main(["summarize", "does-not-exist"])

        self.assertEqual(exit_code, 1)
        self.assertIn("does-not-exist", stderr.getvalue())


class ListTests(unittest.TestCase):
    def test_list_empty_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = list_ledgers(Path(tmp) / "missing-root")

            self.assertEqual(result.entries, ())

    def test_list_multiple_valid_and_malformed_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "working-ledger"
            active = create_ledger("Active task", root=root, owner_id="active-owner")
            closed = create_ledger("Closed task", root=root, owner_id="closed-owner")
            _replace_in_ledger(closed.scope, "Lifecycle State: Created", "Lifecycle State: Closed")
            superseded = create_ledger("Superseded task", root=root, owner_id="superseded-owner")
            _replace_in_ledger(superseded.scope, "Lifecycle State: Created", "Lifecycle State: Superseded")
            _replace_in_ledger(
                superseded.scope,
                "Not completed yet. This ledger is newly created and remains open.",
                "Superseded by working-ledger/replacement-owner.",
            )
            malformed = root / "malformed-owner"
            malformed.mkdir()

            result = list_ledgers(root)

            by_name = {Path(entry.scope).name: entry for entry in result.entries}
            self.assertEqual(len(result.entries), 4)
            self.assertEqual(by_name["active-owner"].scope_id, "active-owner")
            self.assertTrue(by_name["active-owner"].ok)
            self.assertEqual(by_name["closed-owner"].lifecycle_state, "Closed")
            self.assertEqual(by_name["superseded-owner"].lifecycle_state, "Superseded")
            self.assertFalse(by_name["malformed-owner"].ok)

    def test_cli_list_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "working-ledger"
            create_ledger("List task", root=root, owner_id="list-owner")
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(["list", "--root", str(root), "--format", "json"])

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(payload["entries"][0]["scope_id"], "list-owner")
            self.assertEqual(payload["entries"][0]["owner_id"], "list-owner")


def _replace_in_ledger(scope: str, old: str, new: str) -> None:
    ledger_path = Path(scope) / "ledger.md"
    text = ledger_path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"Expected text not found: {old}")
    ledger_path.write_text(text.replace(old, new), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
