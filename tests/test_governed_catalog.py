"""Governed-tier service catalog — added alongside the 7 canonical offerings."""

from __future__ import annotations

from auto_client_acquisition.service_catalog import (
    OFFERINGS,
    get_governed_service,
    list_governed_services,
    list_headline_services,
)

_FORBIDDEN_MODES = {"live_send", "live_charge"}
_GUARANTEE_TOKENS = ("نضمن", "guarantee", "guaranteed")


def test_seven_governed_services() -> None:
    services = list_governed_services()
    assert len(services) == 7
    ids = {s.id for s in services}
    assert "governed_revenue_ops_diagnostic" in ids
    assert "revenue_intelligence_sprint_25000" in ids
    assert "governed_ops_retainer" in ids


def test_canonical_offerings_untouched() -> None:
    # The original 7 offerings still exist alongside the governed tier.
    assert len(OFFERINGS) == 7


def test_three_headline_services() -> None:
    headline = list_headline_services()
    assert len(headline) == 3
    assert [s.id for s in headline] == [
        "governed_revenue_ops_diagnostic",
        "revenue_intelligence_sprint_25000",
        "governed_ops_retainer",
    ]


def test_headline_pricing_matches_doctrine() -> None:
    diag = get_governed_service("governed_revenue_ops_diagnostic")
    assert diag is not None
    assert diag.price_min_sar == 4999.0
    assert diag.price_max_sar == 25000.0
    sprint = get_governed_service("revenue_intelligence_sprint_25000")
    assert sprint.price_min_sar == sprint.price_max_sar == 25000.0
    retainer = get_governed_service("governed_ops_retainer")
    assert retainer.price_unit == "per_month"
    assert retainer.price_max_sar == 35000.0


def test_price_ranges_are_ordered() -> None:
    for s in list_governed_services():
        assert s.price_max_sar >= s.price_min_sar >= 0


def test_no_live_action_modes() -> None:
    for s in list_governed_services():
        assert _FORBIDDEN_MODES.isdisjoint(set(s.action_modes_used))


def test_no_guarantee_language() -> None:
    for s in list_governed_services():
        blob = " ".join(
            [
                s.name_ar,
                s.name_en,
                s.summary_ar,
                s.summary_en,
                s.kpi_commitment_ar,
                s.kpi_commitment_en,
            ]
        ).lower()
        for token in _GUARANTEE_TOKENS:
            assert token.lower() not in blob, f"{s.id} contains forbidden token {token!r}"


def test_every_service_has_evidence_level_and_next_action() -> None:
    for s in list_governed_services():
        assert s.evidence_level_required
        assert s.allowed_next_action_ar and s.allowed_next_action_en
        assert s.forbidden_actions
        assert s.is_estimate is True


def test_unknown_service_returns_none() -> None:
    assert get_governed_service("does_not_exist") is None
