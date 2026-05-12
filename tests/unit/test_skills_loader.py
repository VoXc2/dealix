"""Unit tests for dealix/agents/skills/__init__.py."""

from __future__ import annotations

from pathlib import Path

from dealix.agents.skills import _MANIFEST, Skill, by_id, load, reload


def test_manifest_path_resolves_to_real_file() -> None:
    """Regression: the manifest path was off by one parent (parents[2]
    instead of parents[3]) which made the loader read an empty catalogue
    at runtime even though tests passed by importing in-process."""
    assert _MANIFEST.is_file(), (
        f"Manifest expected at {_MANIFEST}; missing — the loader's "
        "parents[] depth is off relative to skills/MANIFEST.yaml."
    )
    # Belt-and-suspenders: the resolved path must end with the canonical
    # repo-root skills folder, not a nested dealix/skills/ path.
    assert _MANIFEST == Path(_MANIFEST.parents[1]) / "skills" / "MANIFEST.yaml"


def test_load_returns_non_empty_catalog() -> None:
    skills = reload()
    assert len(skills) >= 12, "T6a ships at least 12 skills"
    assert all(isinstance(s, Skill) for s in skills)


def test_load_is_cached() -> None:
    first = load()
    second = load()
    assert first is second  # same list object — cached


def test_every_skill_has_required_fields() -> None:
    for s in reload():
        assert s.id
        assert s.path
        assert s.description
        assert isinstance(s.inputs, list)
        assert s.output_shape


def test_by_id_finds_seeded_skills() -> None:
    skills = reload()
    expected_ids = {
        "sales_qualifier",
        "proposal_writer",
        "meeting_summarizer",
        "crm_syncer",
        "email_triage",
        "compliance_reviewer",
        "contract_analyst",
        "market_researcher",
        "lead_scorer",
        "renewal_forecaster",
        "content_generator_ar",
        "ar_en_translator",
    }
    have_ids = {s.id for s in skills}
    # All 12 catalogue ids must be present.
    assert expected_ids.issubset(have_ids), (
        f"missing: {expected_ids - have_ids}"
    )

    for sid in expected_ids:
        s = by_id(sid)
        assert s is not None
        assert s.id == sid


def test_by_id_returns_none_for_unknown() -> None:
    assert by_id("definitely-not-a-real-skill") is None
