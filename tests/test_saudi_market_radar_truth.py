from pathlib import Path

from dealix.commercial.saudi_market_radar import SaudiMarketRadar


def test_official_watchlist_is_truth_safe() -> None:
    radar = SaudiMarketRadar()
    signals = radar.seed_official_watchlist()

    assert len(signals) >= 8
    for signal in signals:
        assert signal.source_url.startswith("https://")
        assert signal.refresh_policy
        assert signal.counts_as_relationship is False
        assert signal.counts_as_consent is False
        assert signal.counts_as_pipeline is False
        assert signal.counts_as_revenue is False
        assert signal.tender_submission_allowed is False


def test_wave25_record_requires_customer_applicability_verification() -> None:
    signal = SaudiMarketRadar().zatca_wave25_signal()

    assert "187,500" in signal.scope
    assert signal.deadline == "2027-02-01 for notified Wave 25 taxpayers"
    assert "applicability" in signal.scope
    assert "Not tax/legal advice" in signal.compliance_implication


def test_jadeer_is_supplier_readiness_not_privileged_access() -> None:
    signal = SaudiMarketRadar().jadeer_supplier_signal()

    assert signal.problem == "supplier_readiness"
    assert "No privileged access claim" in signal.compliance_implication
    assert signal.counts_as_pipeline is False


def test_etimad_record_cannot_submit_tender() -> None:
    signal = SaudiMarketRadar().etimad_tender_cell(
        tender_ref="T-123",
        issuer="Example Government Buyer",
        sector="government_b2g",
        deadline="2026-10-01",
    )

    assert signal.problem == "tender_readiness"
    assert signal.tender_submission_allowed is False
    assert "L5" in signal.compliance_implication


def test_dynamic_market_counts_are_not_persisted_as_durable_truth() -> None:
    payload = SaudiMarketRadar().misa_invest_saudi_signal().model_dump(mode="json")
    text = str(payload)

    assert "1,865" not in text
    assert "888%" not in text


def test_public_radar_surfaces_jadeer_as_readiness_not_buyer_intent() -> None:
    page = (Path(__file__).resolve().parents[1] / "apps/web/app/saudi-opportunity-radar/page.tsx").read_text(encoding="utf-8")
    assert 'id: "monshaat-jadeer"' in page
    assert "Free supplier-readiness diagnostic" in page
    assert "لا يثبت علاقة أو موافقة" in page
    assert "https://www.monshaat.gov.sa/en/node/12778" in page
