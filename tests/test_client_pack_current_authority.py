"""Client-pack runtime must stay minimum-data and current commercial authority."""

from __future__ import annotations

from pathlib import Path

from dealix.commercial_ops.client_pack import build_client_pack_from_row

ROOT = Path(__file__).resolve().parents[1]


def test_client_pack_normalizes_legacy_offer_and_drops_contact_data() -> None:
    row = {
        "company": "ACME Saudi",
        "segment": "b2b_saas",
        "pain_hypothesis": "فرص بلا owner أو next action واضح",
        "offer_id": "growth_starter",
        "contact_name": "Person Name",
        "email": "person@example.com",
        "phone": "+966500000000",
    }

    pack = build_client_pack_from_row(row, write_disk=False)
    blob = (
        pack["proposal"]["markdown"]
        + "\n"
        + pack["deck_notes"]
        + "\n"
        + pack["policy_ar"]
    )

    assert pack["offer_id"] == "revenue_command_pilot_30d"
    assert pack["recommended_service"] == "Revenue Command Pilot"
    assert pack["timeline_days"] is None
    assert pack["price_band_sar"] == "quote_after_discovery"
    assert pack["legacy_offer_id_input"] == "growth_starter"
    assert pack["safe_to_send"] is False
    assert "person@example.com" not in blob
    assert "+966500000000" not in blob
    assert "Person Name" not in blob
    assert "customer-specific quote" in blob.lower()


def test_client_pack_quarantines_unvalidated_legacy_deck() -> None:
    pack = build_client_pack_from_row(
        {
            "company": "ACME Saudi",
            "segment": "b2b_services",
            "pain_hypothesis": "تأخر المتابعة",
        },
        write_disk=False,
    )

    assert pack["deck_template"] is None
    assert pack["deck_template_status"] == (
        "quarantined_until_current_commercial_authority_review"
    )
    assert pack["legacy_deck_reference"].endswith("dealix_ops_sales_kit_ar.pptx")
    assert "QUARANTINED" in pack["deck_notes"]
    assert "Do not attach or send" in pack["deck_notes"]


def test_active_client_pack_runbook_has_no_retired_price_or_offer_path() -> None:
    runbook = (
        ROOT / "docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md"
    ).read_text(encoding="utf-8")

    assert "نطاق ومدة ومعايير قبول خاصة بالعميل" in runbook
    assert "30-day Revenue Command Pilot" not in runbook
    assert "customer-specific quote" in runbook
    assert "STOP / EXPAND / REDESIGN" in runbook
    assert "public fixed price" in runbook

    for token in (
        "4,999",
        "9,999",
        "15,000",
        "Governed Revenue Ops Diagnostic",
        "Recommended Sprint / Retainer",
        "اختر 5 warm contacts",
    ):
        assert token not in runbook
