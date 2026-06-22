from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from tools.awl.claude_code import ClaudeCodeSkillError, create_claude_code_skill
from tools.awl.cli import main as cli_main


class ClaudeCodeSkillTests(unittest.TestCase):
    def test_create_claude_code_skill_builds_discoverable_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".claude" / "skills" / "agent-working-ledger"

            result = create_claude_code_skill(target)

            skill_path = Path(result.skill)
            skill_text = skill_path.read_text(encoding="utf-8")

            self.assertEqual(Path(result.target), target)
            self.assertTrue(skill_path.is_file())
            self.assertTrue((target / "templates").is_dir())
            self.assertTrue((target / "runtime-capabilities.md").is_file())
            self.assertTrue((target / "CLAUDE.md-snippet.md").is_file())
            self.assertIn("name: agent-working-ledger", skill_text)
            self.assertIn("## Claude Code Runtime Binding", skill_text)
            self.assertIn("claude-code-${CLAUDE_SESSION_ID}", skill_text)
            self.assertIn("${CLAUDE_SKILL_DIR}/templates/", skill_text)
            self.assertIn("## Core Rule", skill_text)
            self.assertIn("## Maintain", skill_text)

    def test_claude_code_skill_templates_match_canonical_skill_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".claude" / "skills" / "agent-working-ledger"

            create_claude_code_skill(target)

            canonical_templates = Path("skills") / "agent-working-ledger" / "templates"
            generated_templates = target / "templates"
            for source in canonical_templates.iterdir():
                if source.is_file():
                    self.assertEqual(
                        (generated_templates / source.name).read_text(encoding="utf-8"),
                        source.read_text(encoding="utf-8"),
                    )

    def test_create_claude_code_skill_refuses_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".claude" / "skills" / "agent-working-ledger"
            target.mkdir(parents=True)

            with self.assertRaises(ClaudeCodeSkillError):
                create_claude_code_skill(target)

    def test_cli_install_claude_code_skill_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".claude" / "skills" / "agent-working-ledger"
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = cli_main(
                    [
                        "install-claude-code-skill",
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

    def test_cli_install_claude_code_skill_returns_nonzero_for_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / ".claude" / "skills" / "agent-working-ledger"
            target.mkdir(parents=True)
            stderr = StringIO()

            with redirect_stderr(stderr):
                exit_code = cli_main(
                    [
                        "install-claude-code-skill",
                        "--target",
                        str(target),
                    ]
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("Target already exists", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
