"""Gross margin summary by offer id (pure)."""

from __future__ import annotations

from collections.abc import Mapping

from auto_client_acquisition.operating_finance_os.offer_unit_economics import OfferUnitEconomics


def margin_percent_by_offer(economics_by_offer: Mapping[str, OfferUnitEconomics]) -> dict[str, float]:
    return {oid: round(100.0 * e.gross_margin, 2) for oid, e in economics_by_offer.items()}


__all__ = ["margin_percent_by_offer"]
