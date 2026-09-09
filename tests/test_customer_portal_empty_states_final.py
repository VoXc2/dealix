"""Current customer-portal public-surface truth tests.

The historical static portal is retired and fail-closed. Empty/degraded runtime
states remain an API/application concern; the retired HTML must not masquerade
as a live customer dashboard.
"""
from __future__ import annotations

from pathlib import Path

import importlib

HTML = Path("landing/customer-portal.html").read_text(encoding="utf-8")


def test_retired_surface_is_noindex_and_redirected() -> None:
    assert 'name="robots" content="noindex,nofollow"' in HTML
    assert 'url=/proof.html' in HTML
    assert 'href="https://dealix.me/proof.html"' in HTML


def test_retired_surface_explains_synthetic_evidence_boundary() -> None:
    low = HTML.lower()
    assert "synthetic" in low
    assert "ليست دليل عميل" in HTML
    assert "kpi" in low


def test_retired_surface_has_no_live_degraded_dashboard_ui() -> None:
    for marker in (
        ".cp-empty-state",
        ".cp-degraded-banner",
        'id="cp-degraded-banner"',
        'id="w13-degraded-banner"',
        'class="w13-fourcards"',
    ):
        assert marker not in HTML


def test_customer_portal_router_still_imports_cleanly() -> None:
    import api.routers.customer_company_portal as ccp

    importlib.reload(ccp)
    assert hasattr(ccp, "router")
