"""Offer ladder — 7-rung commercial ladder backed by the service catalog."""
from __future__ import annotations

from auto_client_acquisition.business_ops.offer_ladder import (
    OFFER_LADDER,
    OfferRung,
    get_offer,
    list_offers,
)
from auto_client_acquisition.service_catalog.registry import OFFERINGS


def test_offer_ladder_has_seven_rungs():
    assert len(OFFER_LADDER) == 7
    assert len(OFFERINGS) == 7


def test_offer_ladder_keys_match_catalog():
    assert set(OFFER_LADDER.keys()) == {o.id for o in OFFERINGS}


def test_get_offer_returns_rung():
    rung = get_offer("free_mini_diagnostic")
    assert isinstance(rung, OfferRung)
    assert rung.rung == 1
    assert rung.service_id == "free_mini_diagnostic"


def test_get_offer_unknown_returns_none():
    assert get_offer("does_not_exist") is None


def test_list_offers_ascending_by_rung():
    rungs = list_offers()
    assert [r.rung for r in rungs] == [1, 2, 3, 4, 5, 6, 7]


def test_offer_rung_to_dict_pulls_catalog_pricing():
    rung = get_offer("revenue_proof_sprint_499")
    assert rung is not None
    d = rung.to_dict()
    assert d["price_sar"] == 499.0
    assert d["name_en"] == "499 SAR Revenue Proof Sprint"
