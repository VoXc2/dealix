"""Value attribution paths."""

from __future__ import annotations

from auto_client_acquisition.value_os.attribution import load_attribution_paths, record_path_attribution
from auto_client_acquisition.value_os.value_ledger import clear_for_test, list_events


def test_record_path_attribution() -> None:
    clear_for_test("cust_attr_test")
    ev = record_path_attribution(
        path_id="discovery_to_pilot",
        customer_id="cust_attr_test",
        amount=1000.0,
        source_ref="test:attribution",
    )
    assert "path_id=discovery_to_pilot" in ev.notes
    rows = list_events(customer_id="cust_attr_test")
    assert any(r.event_id == ev.event_id for r in rows)


def test_load_attribution_paths() -> None:
    data = load_attribution_paths()
    assert len(data.get("paths", [])) >= 1
