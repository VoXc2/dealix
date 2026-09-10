"""Customer portal public-surface regression tests.

Wave-13-era static dashboard assertions are historical. The canonical public
posture now retires ``landing/customer-portal.html`` and redirects visitors to
the proof methodology so synthetic/demo dashboard material cannot be confused
with live customer evidence.
"""
from __future__ import annotations

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_PORTAL = _REPO_ROOT / "landing" / "customer-portal.html"


def test_historical_customer_dashboard_is_explicitly_retired() -> None:
    html = _PORTAL.read_text(encoding="utf-8")
    assert "DEALIX_RETIRED_PUBLIC_SURFACE" in html
    assert "retired customer demo" in html.lower()


def test_retired_dashboard_redirects_to_current_proof_surface() -> None:
    html = _PORTAL.read_text(encoding="utf-8")
    assert 'content="0; url=/proof.html"' in html
    assert 'href="https://dealix.me/proof.html"' in html


def test_retired_dashboard_cannot_expose_old_full_ops_cards() -> None:
    html = _PORTAL.read_text(encoding="utf-8")
    for marker in (
        'class="w13-fourcards"',
        'data-test="w13-card-current-status"',
        'data-test="w13-card-today-decision"',
        'data-test="w13-card-pending-approvals"',
        'data-test="w13-card-proof-progress"',
        'id="w13-degraded-banner"',
    ):
        assert marker not in html


def test_retired_dashboard_contains_no_success_or_guarantee_claim() -> None:
    html = _PORTAL.read_text(encoding="utf-8").lower()
    for token in ("guaranteed", "نضمن", "customer success", "revenue increased"):
        assert token not in html
