from __future__ import annotations

from saudi_ai_provider.kpis import kpis_for_service


def test_kpi_tree_has_customer_portal() -> None:
    data = kpis_for_service("CUSTOMER_PORTAL_GOLD")
    assert data["north_star"] == "ticket_deflection_rate"
    assert "support_cost_reduction_sar" in data["business_kpis"]
