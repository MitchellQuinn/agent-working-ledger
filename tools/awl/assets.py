from __future__ import annotations

import sysconfig
from dataclasses import dataclass
from pathlib import Path


ASSET_DIR_NAME = "agent-working-ledger"
ASSET_SUBPATHS = {
    "documents": "documents",
    "spec": "spec",
    "protocols": "protocols",
    "templates": "templates",
    "skills": "skills",
    "wrappers": "wrappers",
    "docs": "docs",
    "examples": "examples",
    "evals": "evals",
}
REQUIRED_PATHS = (
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "documents/agent-working-ledger-skill-specification-v0.3.md",
    "spec/SPEC.md",
    "protocols/create-ledger.md",
    "templates/OWNER.md.template",
    "templates/ledger.md.template",
    "skills/agent-working-ledger/SKILL.md",
    "skills/agent-working-ledger/templates/OWNER.md.template",
    "wrappers/claude-code/SKILL.md",
    "wrappers/codex/SKILL.md",
    "wrappers/generic-cli-agent/prompt-wrapper.md",
    "docs/quickstart.md",
    "examples/README.md",
    "evals/README.md",
)


@dataclass(frozen=True)
class AssetsResult:
    asset_root: str
    source: str
    exists: bool
    paths: dict[str, str]
    missing: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "asset_root": self.asset_root,
            "source": self.source,
            "exists": self.exists,
            "missing": list(self.missing),
            **self.paths,
        }


def find_assets() -> AssetsResult:
    source_root = _source_tree_root()
    if _looks_like_asset_root(source_root):
        return _result(source_root, "source-tree")

    installed_root = _installed_asset_root()
    return _result(installed_root, "installed")


def format_assets_text(result: AssetsResult) -> str:
    lines = [
        f"Asset root: {result.asset_root}",
        f"Source: {result.source}",
        f"Exists: {'yes' if result.exists else 'no'}",
    ]
    for name in sorted(result.paths):
        lines.append(f"{name}: {result.paths[name]}")
    if result.missing:
        lines.append("Missing:")
        lines.extend(f"- {path}" for path in result.missing)
    return "\n".join(lines)


def _source_tree_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _installed_asset_root() -> Path:
    return Path(sysconfig.get_path("data")) / "share" / ASSET_DIR_NAME


def _looks_like_asset_root(root: Path) -> bool:
    return (root / "pyproject.toml").is_file() and (root / "tools" / "awl").is_dir()


def _result(root: Path, source: str) -> AssetsResult:
    missing = tuple(path for path in REQUIRED_PATHS if not (root / path).exists())
    paths = {name: str(root / subpath) for name, subpath in ASSET_SUBPATHS.items()}
    return AssetsResult(
        asset_root=str(root),
        source=source,
        exists=root.is_dir() and not missing,
        paths=paths,
        missing=missing,
    )

