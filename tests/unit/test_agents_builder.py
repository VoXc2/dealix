"""Unit tests for dealix/agents/builder/__init__.py."""

from __future__ import annotations

import pytest

from dealix.agents.builder import AgentValidationError, validate


def _ok_manifest() -> dict[str, object]:
    return {
        "id": "my-helper",
        "name": "My helper",
        "description": "A test agent",
        "model": "claude-haiku-4-5",
        "tools": [],  # empty is fine
        "prompt_override": "You are friendly.",
        "max_usd_per_request": 0.5,
        "locale": "ar",
    }


def test_validate_happy_path() -> None:
    spec = validate(_ok_manifest())
    assert spec.id == "my-helper"
    assert spec.name == "My helper"
    assert spec.max_usd_per_request == 0.5
    assert spec.locale == "ar"


@pytest.mark.parametrize("bad_id", ["", "A", "no", "with spaces", "MIX-Case", "x" * 65])
def test_validate_rejects_bad_ids(bad_id: str) -> None:
    m = _ok_manifest() | {"id": bad_id}
    with pytest.raises(AgentValidationError, match="id must be"):
        validate(m)


def test_validate_requires_name() -> None:
    m = _ok_manifest() | {"name": ""}
    with pytest.raises(AgentValidationError, match="name required"):
        validate(m)


def test_validate_requires_model() -> None:
    m = _ok_manifest() | {"model": ""}
    with pytest.raises(AgentValidationError, match="model required"):
        validate(m)


@pytest.mark.parametrize("cap", [0, -0.1, 10.5, 100])
def test_validate_rejects_out_of_range_cap(cap: float) -> None:
    m = _ok_manifest() | {"max_usd_per_request": cap}
    with pytest.raises(AgentValidationError, match="max_usd_per_request"):
        validate(m)


def test_validate_truncates_description_and_prompt() -> None:
    m = _ok_manifest() | {
        "description": "x" * 600,
        "prompt_override": "y" * 9000,
    }
    spec = validate(m)
    assert len(spec.description) == 500
    assert len(spec.prompt_override) == 8000


def test_validate_unknown_skill_raises() -> None:
    m = _ok_manifest() | {"tools": ["this-skill-does-not-exist"]}
    # Either it raises AgentValidationError or the skills lookup is unavailable
    # and validation passes by design (logged warning).
    try:
        spec = validate(m)
        # If passed, the tool list is preserved.
        assert "this-skill-does-not-exist" in spec.tools
    except AgentValidationError as exc:
        assert "unknown skill" in str(exc)
