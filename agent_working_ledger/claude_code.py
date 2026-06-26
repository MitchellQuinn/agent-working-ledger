from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from .assets import find_assets


class ClaudeCodeSkillError(Exception):
    """Raised when a Claude Code skill package cannot be created."""


@dataclass(frozen=True)
class ClaudeCodeSkillResult:
    target: str
    skill: str
    templates: str
    support_files: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "skill": self.skill,
            "templates": self.templates,
            "support_files": list(self.support_files),
        }


def create_claude_code_skill(target: str | Path = ".claude/skills/agent-working-ledger") -> ClaudeCodeSkillResult:
    """Create a Claude Code-ready Agent Working Ledger skill directory."""

    assets = find_assets()
    if not assets.exists:
        missing = ", ".join(assets.missing) or "unknown release assets"
        raise ClaudeCodeSkillError(f"Agent Working Ledger assets are incomplete: {missing}")

    target_path = Path(target)
    if target_path.exists():
        raise ClaudeCodeSkillError(f"Target already exists: {target_path}")

    skill_root = Path(str(assets.paths["skills"])) / "agent-working-ledger"
    wrapper_root = Path(str(assets.paths["wrappers"])) / "claude-code"
    canonical_skill_path = skill_root / "SKILL.md"
    wrapper_skill_path = wrapper_root / "SKILL.md"
    source_templates = skill_root / "templates"

    _require_file(canonical_skill_path)
    _require_file(wrapper_skill_path)
    _require_dir(source_templates)

    parent = target_path.parent
    parent.mkdir(parents=True, exist_ok=True)
    target_path.mkdir()

    try:
        skill_text = _build_skill_text(
            canonical_skill_path.read_text(encoding="utf-8"),
            wrapper_skill_path.read_text(encoding="utf-8"),
        )
        skill_path = target_path / "SKILL.md"
        skill_path.write_text(skill_text, encoding="utf-8")

        templates_path = target_path / "templates"
        shutil.copytree(source_templates, templates_path)

        support_files: list[str] = []
        for name in ("runtime-capabilities.md", "CLAUDE.md-snippet.md"):
            source = wrapper_root / name
            if source.is_file():
                destination = target_path / name
                shutil.copy2(source, destination)
                support_files.append(str(destination))
    except Exception:
        shutil.rmtree(target_path, ignore_errors=True)
        raise

    return ClaudeCodeSkillResult(
        target=str(target_path),
        skill=str(skill_path),
        templates=str(templates_path),
        support_files=tuple(support_files),
    )


def format_claude_code_skill_text(result: ClaudeCodeSkillResult) -> str:
    lines = [
        f"Created Claude Code skill: {result.target}",
        f"SKILL.md: {result.skill}",
        f"templates/: {result.templates}",
    ]
    if result.support_files:
        lines.append("support files:")
        lines.extend(f"- {path}" for path in result.support_files)
    lines.extend(
        [
            "",
            "Next steps:",
            "1. Start Claude Code from the project root with `claude`.",
            "2. Invoke `/agent-working-ledger \"Smoke test ledger\"`.",
            "3. Confirm a `working-ledger/claude-code-.../` scope is created.",
        ]
    )
    return "\n".join(lines)


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise ClaudeCodeSkillError(f"Required file is missing: {path}")


def _require_dir(path: Path) -> None:
    if not path.is_dir():
        raise ClaudeCodeSkillError(f"Required directory is missing: {path}")


def _build_skill_text(canonical_skill: str, wrapper_skill: str) -> str:
    wrapper_frontmatter, _wrapper_body = _split_frontmatter(wrapper_skill)
    _canonical_frontmatter, canonical_body = _split_frontmatter(canonical_skill)

    wrapper_frontmatter = wrapper_frontmatter.strip()
    canonical_body = canonical_body.strip()

    return f"""{wrapper_frontmatter}

# Agent Working Ledger For Claude Code

This is the Claude Code adapter for the canonical Agent Working Ledger skill.
Apply the canonical instructions below with these Claude Code runtime bindings.

## Claude Code Runtime Binding

- Treat `$ARGUMENTS` as either an explicitly supplied existing ledger scope or a
  human-readable task title. If no argument is supplied, infer the task title
  from the current user request.
- Use `claude-code-${{CLAUDE_SESSION_ID}}` as the ledger owner ID when
  `${{CLAUDE_SESSION_ID}}` is available.
- If a human-readable slug is useful, append it:
  `claude-code-${{CLAUDE_SESSION_ID}}-<task-slug>`.
- If `${{CLAUDE_SESSION_ID}}` is unavailable, fall back to
  `<UTC timestamp>-claude-code-<short-random-nonce>`.
- Bundled templates live under `${{CLAUDE_SKILL_DIR}}/templates/`.
- Supporting Claude Code notes are available in
  `${{CLAUDE_SKILL_DIR}}/runtime-capabilities.md` and
  `${{CLAUDE_SKILL_DIR}}/CLAUDE.md-snippet.md`.
- Do not treat this adapter as a fork of the core schema. If there is any
  ambiguity, preserve the canonical Agent Working Ledger schema and apply only
  the owner-ID and runtime bindings above.

{canonical_body}
"""


def _split_frontmatter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return "", normalized

    marker = "\n---\n"
    end = normalized.find(marker, 4)
    if end == -1:
        raise ClaudeCodeSkillError("Invalid SKILL.md frontmatter: closing marker not found.")

    frontmatter = normalized[: end + len(marker)]
    body = normalized[end + len(marker) :]
    return frontmatter, body
