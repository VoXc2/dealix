"""Contracts for the repo-governed Hermes skill pack (skills/hermes).

Skills are bounded procedures: exact commands, truth-safe outputs, no external
send, no secrets, no destructive operations.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills" / "hermes"

SCRIPT_REF_RE = re.compile(r"scripts/[A-Za-z0-9_./-]+\.(?:py|sh)")
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")
DANGEROUS_RE = re.compile(
    r"git push|gh pr merge|curl\s+-X\s+(?:POST|PUT|DELETE|PATCH)|MOYASAR_LIVE_MODE=1|rm -rf"
)


def _skill_files() -> list[Path]:
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


def test_skill_pack_exists_and_frontmatter_matches_directory() -> None:
    files = _skill_files()
    assert len(files) >= 5, [path.parent.name for path in files]
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n"), path
        frontmatter = text.split("---", 2)[1]
        name_match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.M)
        assert name_match, path
        assert name_match.group(1) == path.parent.name, path
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        assert description and len(description.group(1)) >= 40, path


def test_referenced_repo_scripts_exist() -> None:
    for path in _skill_files():
        text = path.read_text(encoding="utf-8")
        for relative in SCRIPT_REF_RE.findall(text):
            assert (ROOT / relative).is_file(), f"{path}: missing {relative}"


def test_skill_pack_has_no_secrets_or_dangerous_commands() -> None:
    for path in _skill_files():
        text = path.read_text(encoding="utf-8")
        assert not SECRET_RE.search(text), path
        assert not DANGEROUS_RE.search(text), path


def test_skill_pack_covers_five_agents_and_approval_first() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in _skill_files())
    for agent in ("dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"):
        assert agent in text
    lowered = text.lower()
    assert "l5" in lowered or "approval" in lowered
    assert "estimate" in lowered
