"""Phase 3 — unified_operating_graph tests.

Asserts:
- status returns 200 + node/edge type lists
- empty customer returns insufficient_data + only company node
- graph reflects leadops + service_session + ticket + proof events
- no internal terms in customer-facing summary
- no 500 on any failure (degraded section instead)
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.unified_operating_graph import (
    build_graph_for_customer,
    list_known_node_types,
    summarize_graph_for_customer,
)


def test_list_known_node_types_returns_12() -> None:
    types = list_known_node_types()
    assert len(types) == 12
    assert "company" in types
    assert "case_study_candidate" in types
    assert "partner" in types


def test_empty_customer_returns_insufficient_data() -> None:
    g = build_graph_for_customer(customer_handle="never-seen-customer")
    # Always has at least the company node
    assert len(g.nodes) >= 1
    company_nodes = [n for n in g.nodes if n.node_type == "company"]
    assert len(company_nodes) == 1
    # Status reflects no real data
    assert g.data_status == "insufficient_data"


def test_summary_for_empty_graph() -> None:
    g = build_graph_for_customer(customer_handle="empty-summary-test")
    summary = summarize_graph_for_customer(g)
    assert "بيانات" in summary["headline_ar"]
    assert "data" in summary["headline_en"].lower() or "items" in summary["headline_en"].lower()


@pytest.mark.asyncio
async def test_status_endpoint_returns_hard_gates() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/unified-operating-graph/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "unified_operating_graph"
    assert len(body["node_types"]) == 12
    assert body["hard_gates"]["read_only"] is True


@pytest.mark.asyncio
async def test_graph_endpoint_for_unknown_customer() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/unified-operating-graph/uog-unknown-test")
    assert r.status_code == 200  # NEVER 500 for missing data
    body = r.json()
    assert body["graph"]["data_status"] == "insufficient_data"
    assert body["summary"]["data_status"] == "insufficient_data"


@pytest.mark.asyncio
async def test_graph_reflects_leadops_records() -> None:
    """After creating leadops + service session, graph nodes appear."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create leadops record
        await c.post("/api/v1/leadops/run", json={
            "raw_payload": {
                "company": "UOG Test Co",
                "email": "uog@test.sa",
                "sector": "real_estate",
                "region": "Riyadh",
            },
            "source": "manual",
            "customer_handle": "uog-graph-test",
        })
        # Create service session
        await c.post("/api/v1/service-sessions/start", json={
            "customer_handle": "uog-graph-test",
            "service_type": "diagnostic",
        })
        # Build graph
        r = await c.get("/api/v1/unified-operating-graph/uog-graph-test")
    body = r.json()
    nodes = body["graph"]["nodes"]
    node_types = {n["node_type"] for n in nodes}
    assert "company" in node_types
    assert "lead" in node_types
    assert "service_session" in node_types


@pytest.mark.asyncio
async def test_graph_summary_no_internal_terms() -> None:
    """Customer-facing summary must not leak internal terms."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/unified-operating-graph/leak-check-test")
    summary = r.json()["summary"]
    blob = " ".join([
        summary["headline_ar"], summary["headline_en"],
        " ".join(c["label_ar"] for c in summary["counts_by_type"]),
        " ".join(c["label_en"] for c in summary["counts_by_type"]),
    ]).lower()
    forbidden = ["v11", "v12", "v13", "v14", "router", "verifier",
                 "growth_beast", "stacktrace", "pytest"]
    for f in forbidden:
        assert f not in blob, f"summary leaks internal term: {f}"


def test_builder_never_raises_on_unexpected_input() -> None:
    """Even with weird customer handle inputs, never raises."""
    g = build_graph_for_customer(customer_handle="x")
    assert g is not None
    assert g.customer_handle == "x"
