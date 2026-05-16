from __future__ import annotations

import asyncio

from api.routers import service_catalog
from auto_client_acquisition.service_catalog.governed_revenue_ai_ops import (
    build_governed_revenue_ai_ops_blueprint,
)


def test_blueprint_exposes_positioning_and_north_star() -> None:
    payload = build_governed_revenue_ai_ops_blueprint()

    assert payload["positioning"]["name_en"] == (
        "Dealix — Governed Revenue & AI Operations"
    )
    assert payload["north_star_metric"]["id"] == "governed_value_decisions_created"


def test_blueprint_sales_order_starts_with_diagnostic_sprint_retainer() -> None:
    payload = build_governed_revenue_ai_ops_blueprint()
    assert payload["recommended_sales_order"][:3] == [
        "governed_revenue_ops_diagnostic",
        "revenue_intelligence_sprint",
        "governed_ops_retainer",
    ]


def test_blueprint_state_machine_includes_founder_approval_rule() -> None:
    payload = build_governed_revenue_ai_ops_blueprint()
    assert payload["state_machine"]["levels"]["sent"] == "L4"
    assert (
        "no_sent_without_founder_confirmed"
        in payload["state_machine"]["rules"]
    )


def test_router_endpoint_returns_same_blueprint() -> None:
    payload = asyncio.run(service_catalog.governed_operating_model())
    assert payload["core_kpis"] == [
        "sent_count",
        "reply_count",
        "meeting_count",
        "scope_requested_count",
        "invoice_sent_count",
        "invoice_paid_count",
        "retainer_opportunity_count",
    ]
