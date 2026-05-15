"""Landing ↔ registry drift guard.

The landing pages (services.html, pricing.html, checkout.html) and the
exported services-catalog.json must never drift from the canonical
service catalog registry. This test parses the catalog-bearing bits of
each surface and asserts they match the registry.

Sandbox-safe — reads files + imports the registry only.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
LANDING = REPO_ROOT / "landing"

_OLD_IDS = (
    "free_mini_diagnostic",
    "revenue_proof_sprint_499",
    "data_to_revenue_pack_1500",
    "growth_ops_monthly_2999",
    "support_os_addon_1500",
    "executive_command_center_7500",
    "bespoke_ai_custom",
)


def test_services_html_lists_every_registry_offering() -> None:
    """services.html must carry a card data-service-id for every offering."""
    html = (LANDING / "services.html").read_text(encoding="utf-8")
    for offering in OFFERINGS:
        assert f'data-service-id="{offering.id}"' in html, (
            f"services.html missing card for {offering.id}"
        )


def test_services_html_has_no_stale_offering_ids() -> None:
    """No retired offering id may linger in services.html."""
    html = (LANDING / "services.html").read_text(encoding="utf-8")
    for old in _OLD_IDS:
        assert old not in html, f"services.html still references retired id {old}"


def test_services_catalog_json_matches_registry() -> None:
    """The exported JSON artifact must match the in-code registry."""
    payload = json.loads(
        (LANDING / "assets" / "data" / "services-catalog.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["count"] == len(OFFERINGS)
    json_ids = {o["id"] for o in payload["offerings"]}
    assert json_ids == set(SERVICE_IDS)


def test_checkout_tiers_reference_real_service_ids() -> None:
    """Every checkout.html TIERS service_session_id must be a registry id."""
    html = (LANDING / "checkout.html").read_text(encoding="utf-8")
    session_ids = re.findall(r'service_session_id:\s*"([^"]+)"', html)
    assert session_ids, "no service_session_id entries found in checkout.html"
    for sid in session_ids:
        assert sid in SERVICE_IDS, f"checkout.html tier references unknown id {sid}"


def test_pricing_html_shows_canonical_rung_prices() -> None:
    """pricing.html must show the locked price strings for the paid rungs."""
    html = (LANDING / "pricing.html").read_text(encoding="utf-8")
    for token in ("2,500", "9,500", "6,000–18,000", "45,000–120,000"):
        assert token in html, f"pricing.html missing canonical price token {token}"


def test_paid_rung_amounts_in_checkout_match_registry() -> None:
    """checkout.html charge amounts must match registry price anchors."""
    html = (LANDING / "checkout.html").read_text(encoding="utf-8")
    # Map each TIERS block's service_session_id → amount_sar.
    blocks = re.findall(
        r'amount_sar:\s*(null|\d+),\s*recurring:[^,]+,\s*'
        r'service_session_id:\s*"([^"]+)"',
        html,
    )
    assert blocks, "could not parse TIERS amount/service_session_id pairs"
    for amount, sid in blocks:
        offering = get_offering(sid)
        assert offering is not None, f"checkout tier id {sid} not in registry"
        if amount == "null":
            continue
        # checkout charges the registry anchor (band minimum for banded rungs)
        assert float(amount) == offering.price_sar, (
            f"checkout amount {amount} != registry price_sar "
            f"{offering.price_sar} for {sid}"
        )
