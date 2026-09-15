from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"

def _read(rel: str) -> str:
    return (WEB / rel).read_text(encoding="utf-8")

def test_proven_operator_surfaces_fail_closed_in_production() -> None:
    middleware = _read("middleware.ts")
    robots = _read("app/robots.ts")
    for route in (
        "/growth", "/commercial-intelligence", "/evidence", "/go-to-market",
        "/brain", "/delivery-os", "/client-acquisition",
    ):
        assert route in middleware
        assert route in robots
    assert '"/service-os"' not in middleware

def test_public_partner_page_does_not_publish_standing_partner_economics() -> None:
    partner = _read("app/partner-room/page.tsx")
    for marker in ("Referral fee", "Revenue share", "White-labeled delivery layer"):
        assert marker not in partner
    assert "Customer-specific commercial terms" in partner
    assert "Commercial authority boundary" in partner

def test_public_buyer_pages_do_not_link_to_protected_operator_surfaces() -> None:
    enterprise = _read("app/enterprise-readiness/page.tsx")
    revenue = _read("app/revenue-os/page.tsx")
    for marker in ("/review-queue", "/data-room", "/delivery-os"):
        assert marker not in enterprise
    for marker in ('href="/product-network"', 'href="/go-to-market"'):
        assert marker not in revenue
    assert 'href="/products"' in revenue
    assert 'href="/book"' in revenue
