"""Morning core includes dogfooding step."""

from __future__ import annotations

from dealix.commercial_ops.full_ops_autopilot import run_morning_core


def test_morning_core_includes_dogfooding_step():
    result = run_morning_core(top_n=5, run_optional_scripts=False)
    ids = [s["id"] for s in result.get("steps") or []]
    assert "dogfooding" in ids
    dog = next(s for s in result["steps"] if s["id"] == "dogfooding")
    assert dog.get("ok") is True
