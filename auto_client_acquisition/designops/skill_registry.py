"""Loads and validates `design-skills/<name>/SKILL.md` front-matter.

Each SKILL.md begins with a YAML front-matter block delimited by
``---`` lines. The remainder of the file is bilingual narrative
markdown that documents the skill for humans; only the front-matter
is loaded into the registry.

This module is pure: no LLM call, no HTTP, no writes — only reads
from `design-skills/` inside the repo.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.designops.schemas import Skill

# `auto_client_acquisition/designops/skill_registry.py` →
# repo root is parents[2].
_REPO_ROOT = Path(__file__).resolve().parents[2]
_SKILLS_DIR = _REPO_ROOT / "design-skills"


def _parse_front_matter(text: str) -> dict[str, Any]:
    """Extract the YAML front-matter from a SKILL.md file.

    Raises ``ValueError`` if the file does not start with a ``---``
    fence followed by a closing ``---`` fence.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md missing opening '---' front-matter fence")
    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("SKILL.md missing closing '---' front-matter fence")
    block = "\n".join(lines[1:end_idx])
    data = yaml.safe_load(block) or {}
    if not isinstance(data, dict):
        raise ValueError("SKILL.md front-matter must be a YAML mapping")
    return data


def _load_skill_file(path: Path) -> Skill:
    text = path.read_text(encoding="utf-8")
    data = _parse_front_matter(text)
    return Skill.model_validate(data)


@lru_cache(maxsize=1)
def _scan_skills() -> dict[str, Skill]:
    """Scan `design-skills/` once and return name→Skill."""
    skills: dict[str, Skill] = {}
    if not _SKILLS_DIR.exists():
        return skills
    for child in sorted(_SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        skill = _load_skill_file(skill_md)
        # The directory name and the front-matter `name` must agree —
        # a mismatch is a structural bug, not a runtime variant.
        if skill.name != child.name:
            raise ValueError(
                f"SKILL.md name mismatch: dir={child.name!r} "
                f"front-matter name={skill.name!r}"
            )
        skills[skill.name] = skill
    return skills


def list_skills() -> list[str]:
    """Return the sorted list of registered skill names."""
    return sorted(_scan_skills().keys())


def get_skill(name: str) -> Skill:
    """Return the Skill record for *name*. Raises KeyError if absent."""
    skills = _scan_skills()
    if name not in skills:
        raise KeyError(name)
    return skills[name]


def validate_skill(skill: Skill) -> None:
    """Assert the safety/evidence/approval invariants for a skill.

    Raises ``AssertionError`` (with a human-readable message) on
    violation. Used both at load-time tests and in CI.
    """
    if not skill.safety_rules:
        raise AssertionError(
            f"skill {skill.name!r} must declare at least one safety rule"
        )
    if not skill.evidence_requirements:
        raise AssertionError(
            f"skill {skill.name!r} must declare at least one "
            "evidence requirement"
        )
    if skill.approval_mode is None:
        raise AssertionError(
            f"skill {skill.name!r} must declare an approval_mode"
        )
    # Customer-facing scenarios must default to approval_required.
    customer_facing = {"sales", "proof", "executive", "partnership"}
    if (
        skill.scenario in customer_facing
        and skill.approval_mode != "approval_required"
    ):
        raise AssertionError(
            f"skill {skill.name!r} is customer-facing "
            f"(scenario={skill.scenario}) but approval_mode is "
            f"{skill.approval_mode!r}; must be 'approval_required'"
        )
