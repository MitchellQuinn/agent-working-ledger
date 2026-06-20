from __future__ import annotations

import unittest
from pathlib import Path

from tools.awl.check import check_scope


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


if __name__ == "__main__":
    unittest.main()
