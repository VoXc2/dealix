"""Customer health v2."""

from __future__ import annotations

from auto_client_acquisition.customer_success.health_v2 import compute_health_v2


def test_healthy_band() -> None:
    out = compute_health_v2(
        signals={"proof_pack_opened": True, "nps_promoter": True, "adoption_milestone_met": True}
    )
    assert out["band"] in ("healthy", "expansion_ready")
