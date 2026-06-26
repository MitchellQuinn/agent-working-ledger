from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from .assets import find_assets


class CodexSkillError(Exception):
    """Raised when a Codex skill package cannot be created."""


@dataclass(frozen=True)
class CodexSkillResult:
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


def create_codex_skill(target: str | Path | None = None) -> CodexSkillResult:
    """Create a Codex-ready Agent Working Ledger skill directory."""

    assets = find_assets()
    if not assets.exists:
        missing = ", ".join(assets.missing) or "unknown release assets"
        raise CodexSkillError(f"Agent Working Ledger assets are incomplete: {missing}")

    target_path = Path(target) if target is not None else _default_target()
    if target_path.exists():
        raise CodexSkillError(f"Target already exists: {target_path}")

    skill_root = Path(str(assets.paths["skills"])) / "agent-working-ledger"
    wrapper_root = Path(str(assets.paths["wrappers"])) / "codex"
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
        for name in ("runtime-capabilities.md", "AGENTS.md-snippet.md"):
            source = wrapper_root / name
            if source.is_file():
                destination = target_path / name
                shutil.copy2(source, destination)
                support_files.append(str(destination))
    except Exception:
        shutil.rmtree(target_path, ignore_errors=True)
        raise

    return CodexSkillResult(
        target=str(target_path),
        skill=str(skill_path),
        templates=str(templates_path),
        support_files=tuple(support_files),
    )


def format_codex_skill_text(result: CodexSkillResult) -> str:
    lines = [
        f"Created Codex skill: {result.target}",
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
            "1. Restart Codex or start a new Codex session if the skill is not visible.",
            "2. Invoke `$agent-working-ledger \"Smoke test ledger\"` or select it with `/skills`.",
            "3. Confirm one scope is created under `working-ledger/` with an owner like `codex-<session-id>` or `<UTC timestamp>-codex-<short-random-nonce>`.",
        ]
    )
    return "\n".join(lines)


def _default_target() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills" / "agent-working-ledger"
    return Path.home() / ".codex" / "skills" / "agent-working-ledger"


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise CodexSkillError(f"Required file is missing: {path}")


def _require_dir(path: Path) -> None:
    if not path.is_dir():
        raise CodexSkillError(f"Required directory is missing: {path}")


def _build_skill_text(canonical_skill: str, wrapper_skill: str) -> str:
    wrapper_frontmatter, _wrapper_body = _split_frontmatter(wrapper_skill)
    _canonical_frontmatter, canonical_body = _split_frontmatter(canonical_skill)

    wrapper_frontmatter = wrapper_frontmatter.strip()
    canonical_body = canonical_body.strip()

    return f"""{wrapper_frontmatter}

# Agent Working Ledger For Codex

This is the Codex adapter for the canonical Agent Working Ledger skill. Apply
the canonical instructions below with these Codex runtime bindings.

## Codex Runtime Binding

- Invoke this skill explicitly with `$agent-working-ledger`, choose it with
  `/skills`, or rely on implicit skill matching when the task matches the skill
  description.
- Use a Codex-provided session or conversation ID as the ledger owner ID when a
  stable ID is available.
- If no stable session or conversation ID is available, fall back to
  `<UTC timestamp>-codex-<short-random-nonce>`.
- Bundled templates live in this skill directory under `templates/`.
- Supporting Codex notes are available in `runtime-capabilities.md` and
  `AGENTS.md-snippet.md` in this skill directory.
- `AGENTS.md` guidance remains manual. The installer copies
  `AGENTS.md-snippet.md` for reference and does not append to or rewrite project
  instruction files.
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
        raise CodexSkillError("Invalid SKILL.md frontmatter: closing marker not found.")

    frontmatter = normalized[: end + len(marker)]
    body = normalized[end + len(marker) :]
    return frontmatter, body
