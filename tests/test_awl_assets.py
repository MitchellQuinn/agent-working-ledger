from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from agent_working_ledger.cli import main as cli_main


class AssetsCommandTests(unittest.TestCase):
    def test_cli_assets_json_reports_source_tree_assets(self) -> None:
        stdout = StringIO()

        with redirect_stdout(stdout):
            exit_code = cli_main(["assets", "--format", "json"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertTrue(payload["exists"])
        self.assertEqual(payload["source"], "source-tree")
        self.assertTrue(Path(payload["asset_root"]).is_dir())
        self.assertTrue(Path(payload["spec"]).is_dir())
        self.assertTrue(Path(payload["templates"]).is_dir())
        self.assertTrue(Path(payload["skills"]).is_dir())
        self.assertEqual(payload["missing"], [])

    def test_cli_assets_returns_nonzero_when_required_assets_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_root = Path(tmp) / "missing-assets"
            stdout = StringIO()

            with (
                patch("agent_working_ledger.assets._source_tree_root", return_value=Path(tmp) / "not-source"),
                patch("agent_working_ledger.assets._installed_asset_root", return_value=missing_root),
                redirect_stdout(stdout),
            ):
                exit_code = cli_main(["assets", "--format", "json"])

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 1)
            self.assertFalse(payload["exists"])
            self.assertEqual(payload["source"], "installed")
            self.assertIn("README.md", payload["missing"])


class SkillTemplateTests(unittest.TestCase):
    def test_bundled_skill_templates_match_top_level_templates(self) -> None:
        top_level = Path("templates")
        bundled = Path("skills") / "agent-working-ledger" / "templates"

        template_names = sorted(path.name for path in top_level.iterdir() if path.is_file())
        self.assertEqual(template_names, sorted(path.name for path in bundled.iterdir() if path.is_file()))

        for name in template_names:
            self.assertEqual(
                (bundled / name).read_text(encoding="utf-8"),
                (top_level / name).read_text(encoding="utf-8"),
                f"Bundled skill template drifted from top-level template: {name}",
            )


if __name__ == "__main__":
    unittest.main()

