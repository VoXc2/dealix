"""Tests for the DesignOps skill registry.

Phase 2 (first half) of DesignOps. These tests guard:

- the eight initial SKILL.md files exist and parse
- list_skills() / get_skill() return Skill records
- validate_skill() enforces safety + evidence + approval invariants
- every loaded skill defaults to approval_required (no auto-send).
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.designops import (
    Skill,
    get_skill,
    list_skills,
    validate_skill,
)

EXPECTED_SKILLS = {
    "dealix-mini-diagnostic",
    "dealix-proof-pack",
    "dealix-executive-weekly-pack",
    "dealix-proposal-page",
    "dealix-pricing-page",
    "dealix-customer-room-dashboard",
    "dealix-service-status-console",
    "dealix-partnership-one-pager",
}


def test_list_skills_includes_initial_eight():
    skills = set(list_skills())
    missing = EXPECTED_SKILLS - skills
    assert not missing, f"missing initial skills: {missing}"
    # And we have at least the eight.
    assert len(skills) >= 8


def test_get_skill_returns_skill_object():
    s = get_skill("dealix-mini-diagnostic")
    assert isinstance(s, Skill)
    assert s.name == "dealix-mini-diagnostic"
    assert s.mode == "document"
    assert s.scenario == "sales"
    assert s.approval_mode == "approval_required"
    assert s.arabic_first is True
    assert s.english_secondary is True
    assert s.safety_rules
    assert s.evidence_requirements


def test_get_skill_unknown_name_raises_keyerror():
    with pytest.raises(KeyError):
        get_skill("does-not-exist")


def test_validate_skill_rejects_empty_safety_rules():
    s = get_skill("dealix-proof-pack").model_copy(
        update={"safety_rules": []}
    )
    with pytest.raises(AssertionError, match="safety rule"):
        validate_skill(s)


def test_validate_skill_rejects_empty_evidence_requirements():
    s = get_skill("dealix-proof-pack").model_copy(
        update={"evidence_requirements": []}
    )
    with pytest.raises(AssertionError, match="evidence requirement"):
        validate_skill(s)


def test_validate_skill_passes_for_all_initial_skills():
    """Every shipped skill must satisfy validate_skill out of the box."""
    for name in sorted(EXPECTED_SKILLS):
        s = get_skill(name)
        validate_skill(s)


def test_every_loaded_skill_is_approval_required():
    """Hard rule: no SKILL.md ships with auto-send."""
    for name in list_skills():
        s = get_skill(name)
        assert s.approval_mode == "approval_required", (
            f"skill {name!r} declares approval_mode={s.approval_mode!r}; "
            "all initial skills must default to 'approval_required'."
        )


def test_skills_use_the_dealix_design_system():
    for name in sorted(EXPECTED_SKILLS):
        assert get_skill(name).design_system == "dealix"


def test_skills_declare_arabic_first_and_english_secondary():
    for name in sorted(EXPECTED_SKILLS):
        s = get_skill(name)
        assert s.arabic_first is True
        assert s.english_secondary is True


def test_skills_forbidden_claims_overlap_with_design_system_list():
    """Each SKILL's forbidden_claims must be a subset of the
    design-system forbidden copy list. We assert at least one shared
    token to catch typos and stale enumerations.
    """
    from auto_client_acquisition.designops import load_design_system

    ds_forbidden = set(load_design_system()["forbidden_copy"])
    for name in sorted(EXPECTED_SKILLS):
        s = get_skill(name)
        assert s.forbidden_claims, (
            f"{name!r} declares an empty forbidden_claims list"
        )
        overlap = set(s.forbidden_claims) & ds_forbidden
        assert overlap, (
            f"{name!r} forbidden_claims {s.forbidden_claims!r} "
            f"share nothing with design system list {ds_forbidden!r}"
        )
