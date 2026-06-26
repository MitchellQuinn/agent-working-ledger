from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from agent_working_ledger.cli import main as cli_main
from agent_working_ledger.codex import CodexSkillError, create_codex_skill, format_codex_skill_text


class CodexSkillTests(unittest.TestCase):
    def test_create_codex_skill_builds_discoverable_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".codex" / "skills" / "agent-working-ledger"

            result = create_codex_skill(target)

            skill_path = Path(result.skill)
            skill_text = skill_path.read_text(encoding="utf-8")

            self.assertEqual(Path(result.target), target)
            self.assertTrue(skill_path.is_file())
            self.assertTrue((target / "templates").is_dir())
            self.assertTrue((target / "runtime-capabilities.md").is_file())
            self.assertTrue((target / "AGENTS.md-snippet.md").is_file())
            self.assertIn("name: agent-working-ledger", skill_text)
            self.assertIn("## Codex Runtime Binding", skill_text)
            self.assertIn("$agent-working-ledger", skill_text)
            self.assertIn("/skills", skill_text)
            self.assertIn("<UTC timestamp>-codex-<short-random-nonce>", skill_text)
            self.assertIn("templates/", skill_text)
            self.assertIn("AGENTS.md-snippet.md", skill_text)
            self.assertIn("does not append to or rewrite project", skill_text)
            self.assertIn("## Core Rule", skill_text)
            self.assertIn("## Maintain", skill_text)

            formatted = format_codex_skill_text(result)
            self.assertIn("codex-<session-id>", formatted)
            self.assertIn("<UTC timestamp>-codex-<short-random-nonce>", formatted)

    def test_codex_skill_templates_match_canonical_skill_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".codex" / "skills" / "agent-working-ledger"

            create_codex_skill(target)

            canonical_templates = Path("skills") / "agent-working-ledger" / "templates"
            generated_templates = target / "templates"
            for source in canonical_templates.iterdir():
                if source.is_file():
                    self.assertEqual(
                        (generated_templates / source.name).read_text(encoding="utf-8"),
                        source.read_text(encoding="utf-8"),
                    )

    def test_create_codex_skill_refuses_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".codex" / "skills" / "agent-working-ledger"
            target.mkdir(parents=True)

            with self.assertRaises(CodexSkillError):
                create_codex_skill(target)

    def test_create_codex_skill_defaults_to_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex-home"
            target = codex_home / "skills" / "agent-working-ledger"

            with patch.dict("os.environ", {"CODEX_HOME": str(codex_home)}):
                result = create_codex_skill()

            self.assertEqual(Path(result.target), target)
            self.assertTrue((target / "SKILL.md").is_file())

    def test_create_codex_skill_defaults_to_home_codex_when_codex_home_unset(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            target = home / ".codex" / "skills" / "agent-working-ledger"

            with (
                patch.dict("os.environ", {}, clear=True),
                patch("agent_working_ledger.codex.Path.home", return_value=home),
            ):
                result = create_codex_skill()

            self.assertEqual(Path(result.target), target)
            self.assertTrue((target / "SKILL.md").is_file())

    def test_cli_install_codex_skill_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".codex" / "skills" / "agent-working-ledger"
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install-codex-skill",
                        "--target",
                        str(target),
                        "--format",
                        "json",
                    ]
                )

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(Path(payload["target"]), target)
            self.assertTrue(Path(payload["skill"]).is_file())
            self.assertTrue(Path(payload["templates"]).is_dir())
            self.assertIn(str(target / "runtime-capabilities.md"), payload["support_files"])
            self.assertIn(str(target / "AGENTS.md-snippet.md"), payload["support_files"])

    def test_cli_install_codex_skill_returns_nonzero_for_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".codex" / "skills" / "agent-working-ledger"
            target.mkdir(parents=True)
            stderr = StringIO()

            with redirect_stderr(stderr):
                exit_code = cli_main(
                    [
                        "install-codex-skill",
                        "--target",
                        str(target),
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("Target already exists", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
