from __future__ import annotations

import unittest
from pathlib import Path

from agent_working_ledger.check import check_scope
from agent_working_ledger.list import list_ledgers


class ExampleLedgerTests(unittest.TestCase):
    def test_example_ledgers_pass_check(self) -> None:
        scopes = sorted(path.parent for path in Path("examples").rglob("OWNER.md"))
        self.assertGreaterEqual(len(scopes), 5)

        failures: list[str] = []
        for scope in scopes:
            result = check_scope(scope)
            if not result.ok:
                codes = ", ".join(finding.code for finding in result.findings)
                failures.append(f"{scope}: {codes}")

        self.assertEqual(failures, [])

    def test_list_examples_reports_nested_parallel_scopes(self) -> None:
        result = list_ledgers(Path("examples"))

        scopes = {entry.scope.replace("\\", "/"): entry for entry in result.entries}
        self.assertIn("examples/parallel-subagents/parallel-parent", scopes)
        self.assertIn("examples/parallel-subagents/parallel-subagent", scopes)
        self.assertNotIn("examples/parallel-subagents", scopes)
        self.assertTrue(all(entry.ok for entry in result.entries))


if __name__ == "__main__":
    unittest.main()
