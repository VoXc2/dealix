"""Delivery cost accounting — hours × blended rate + AI."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.offer_unit_economics import OfferUnitEconomics


def delivery_cost_usd(econ: OfferUnitEconomics) -> float:
    return round(econ.delivery_cost, 2)


__all__ = ["delivery_cost_usd"]
