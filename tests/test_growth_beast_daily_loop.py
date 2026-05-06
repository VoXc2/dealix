"""Growth beast daily loop composition."""
from __future__ import annotations

from auto_client_acquisition.growth_beast.daily_loop import build_daily_growth_beast_loop


def test_daily_loop_has_top10_and_gates() -> None:
    out = build_daily_growth_beast_loop({"sector": "marketing agency", "offer": "ops"})
    assert out["schema_version"] == 1
    assert len(out["top_10_targets"]) <= 10
    assert len(out["top_3_targets"]) <= 3
    assert out["hard_gates"]["no_cold_whatsapp"] is True


def test_weekly_learning_from_loops() -> None:
    from auto_client_acquisition.growth_beast.weekly_learning import build_weekly_learning

    w = build_weekly_learning([build_daily_growth_beast_loop({"sector": "saas"})])
    assert w["schema_version"] == 1
