from __future__ import annotations


def test_legacy_dominance_proof_pack_is_not_registered() -> None:
    from api.routers import dominance
    from api.routers.domains import sales as sales_domain

    registered = sales_domain.get_routers()
    assert registered
    paths = {route.path for router in registered for route in router.routes}

    assert "/api/v1/customers/{customer_id}/proof-pack" not in paths
    assert "/api/v1/offers/route" in paths
    assert "/api/v1/customers/{customer_id}/proof-pack" in {route.path for route in dominance.router.routes}


def test_governed_proof_pack_remains_available() -> None:
    from api.routers import proof_pack_governed
    from api.routers.domains import sales as sales_domain

    registered = sales_domain.get_routers()
    assert proof_pack_governed.router in registered
    paths = {route.path for route in proof_pack_governed.router.routes}
    assert "/api/v1/proof-pack/{engagement_id}/generate" in paths
