"""LTV from value ledger."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.ltv_from_events import estimate_ltv_sar
from auto_client_acquisition.value_os.value_ledger import add_event, clear_for_test


def test_estimate_ltv() -> None:
    clear_for_test("cust_ltv")
    add_event(
        customer_id="cust_ltv",
        kind="expansion_value",
        amount=1000.0,
        tier="verified",
        source_ref="test:ltv",
    )
    out = estimate_ltv_sar(customer_id="cust_ltv")
    assert out["ltv_sar"] >= 1000.0
