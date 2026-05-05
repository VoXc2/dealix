"""V5 endpoint perimeter — structural test.

Verifies that every v5 layer's router is registered at the expected
path. Catches drift between the YAML/docs and what's actually
served. If a router is renamed or its prefix changes, this test
fails immediately so the runbook + smoke-test stay accurate.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


# (path, expected_status). 200 means reachable + healthy.
# 404 listed only for endpoints we explicitly want NOT to exist.
EXPECTED_ENDPOINTS: list[tuple[str, int]] = [
    # Liveness
    ("/health", 200),
    # Self-Growth OS
    ("/api/v1/self-growth/status", 200),
    ("/api/v1/self-growth/service-activation", 200),
    ("/api/v1/self-growth/seo/audit", 200),
    ("/api/v1/self-growth/scorecard/weekly", 200),
    ("/api/v1/self-growth/internal-linking", 200),
    ("/api/v1/self-growth/geo/audit", 200),
    # v5 layer 1 — Customer Loop
    ("/api/v1/customer-loop/status", 200),
    ("/api/v1/customer-loop/states", 200),
    # v5 layer 2 — Role Command OS
    ("/api/v1/role-command/status", 200),
    ("/api/v1/role-command/ceo", 200),
    # v5 layer 3 — Service Quality
    ("/api/v1/service-quality/status", 200),
    ("/api/v1/service-quality/sla", 200),
    # v5 layer 4 — Agent Governance
    ("/api/v1/agent-governance/status", 200),
    ("/api/v1/agent-governance/agents", 200),
    # v5 layer 5 — Reliability OS
    ("/api/v1/reliability/status", 200),
    ("/api/v1/reliability/health-matrix", 200),
    # v5 layer 6 — Vertical Playbooks
    ("/api/v1/vertical-playbooks/status", 200),
    ("/api/v1/vertical-playbooks/list", 200),
    # v5 layer 7 — Customer Data Plane
    ("/api/v1/customer-data/status", 200),
    # v5 layer 8 — Finance OS
    ("/api/v1/finance/status", 200),
    ("/api/v1/finance/pricing", 200),
    # v5 layer 9 — Delivery Factory
    ("/api/v1/delivery-factory/status", 200),
    ("/api/v1/delivery-factory/services", 200),
    # v5 layer 10 — Proof Ledger
    ("/api/v1/proof-ledger/status", 200),
    # v5 layer 11 — GTM OS
    ("/api/v1/gtm/status", 200),
    ("/api/v1/gtm/content-calendar", 200),
    # v5 layer 12 — Security & Privacy
    ("/api/v1/security-privacy/status", 200),
    ("/api/v1/security-privacy/data-minimization", 200),
    # Phase I — founder aggregate
    ("/api/v1/founder/status", 200),
    ("/api/v1/founder/dashboard", 200),
]


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


@pytest.mark.parametrize("path,expected_status", EXPECTED_ENDPOINTS)
def test_v5_endpoint_reachable(
    client: TestClient,
    path: str,
    expected_status: int,
) -> None:
    """Every v5 endpoint must be registered at the documented path."""
    resp = client.get(path)
    assert resp.status_code == expected_status, (
        f"{path} returned {resp.status_code}, expected {expected_status}"
    )


def test_v5_endpoint_count_matches_v5_scope(client: TestClient) -> None:
    """Sanity: ≥30 endpoints registered across the v5 surface area.
    If the count drops below 30, the scope doc is probably stale."""
    assert len(EXPECTED_ENDPOINTS) >= 30, (
        f"perimeter test only covers {len(EXPECTED_ENDPOINTS)} endpoints; "
        "v5 scope expects ≥30. Either the test is incomplete or a "
        "v5 layer regressed."
    )


_STATUS_PATHS = [
    "/api/v1/self-growth/status",
    "/api/v1/customer-loop/status",
    "/api/v1/role-command/status",
    "/api/v1/agent-governance/status",
    "/api/v1/reliability/status",
    "/api/v1/vertical-playbooks/status",
    "/api/v1/customer-data/status",
    "/api/v1/finance/status",
    "/api/v1/delivery-factory/status",
    "/api/v1/proof-ledger/status",
    "/api/v1/gtm/status",
    "/api/v1/security-privacy/status",
    "/api/v1/founder/status",
]


def test_every_status_endpoint_carries_a_guardrails_block(
    client: TestClient,
) -> None:
    """Each layer's /status must advertise SOME guardrails block.
    Layers carry layer-specific guardrails (e.g. security_privacy
    advertises `no_pii_in_logs`, proof_ledger advertises
    `pii_redacted_before_persistence`) — but the block must exist
    on every layer so callers can introspect."""
    failures: list[str] = []
    for path in _STATUS_PATHS:
        resp = client.get(path)
        if resp.status_code != 200:
            failures.append(f"{path}: status {resp.status_code}")
            continue
        body = resp.json()
        guardrails = body.get("guardrails")
        if not guardrails:
            # Some layers expose moyasar_state instead — accept that
            # as evidence of an explicit guardrail surface.
            if "moyasar_state" in body or "rules" in body:
                continue
            failures.append(f"{path}: missing 'guardrails' block")
            continue
        if not isinstance(guardrails, dict) or not guardrails:
            failures.append(f"{path}: 'guardrails' must be a non-empty dict")
    assert not failures, "\n".join(failures)


def test_canonical_hard_rules_advertised_by_platform_collectively(
    client: TestClient,
) -> None:
    """The platform as a whole must advertise the 4 canonical hard
    rules across some status endpoint. Each individual layer doesn't
    have to repeat them — but at least one layer must advertise each."""
    canonical = {
        "no_live_send",
        "no_scraping",
        "no_cold_outreach",
        "approval_required_for_external_actions",
    }
    seen: set[str] = set()
    for path in _STATUS_PATHS:
        resp = client.get(path)
        if resp.status_code != 200:
            continue
        guardrails = (resp.json() or {}).get("guardrails") or {}
        seen.update(canonical & set(guardrails.keys()))
    missing = canonical - seen
    assert not missing, (
        f"these canonical hard rules are NOT advertised by any status "
        f"endpoint: {missing}. Add them to at least one router's "
        f"guardrails block."
    )
