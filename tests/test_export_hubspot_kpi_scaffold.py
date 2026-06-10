"""HubSpot KPI scaffold export."""

from __future__ import annotations

import csv
from pathlib import Path

from scripts.export_hubspot_kpi_scaffold import _summarize_hubspot_csv, build_import_yaml


def test_summarize_hubspot_csv(tmp_path: Path):
    csv_path = tmp_path / "deals.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["dealname", "amount", "dealstage"])
        w.writeheader()
        w.writerow({"dealname": "Acme", "amount": "5000", "dealstage": "closedwon"})
        w.writerow({"dealname": "Beta", "amount": "1000", "dealstage": "open"})
    summary = _summarize_hubspot_csv(csv_path)
    assert summary["deal_count"] == 2
    assert summary["total_amount_sar"] == 6000.0
    doc = build_import_yaml(hubspot_summary=summary)
    assert doc["entries"]["measured_customer_value_sar"]["value_numeric"] == 6000.0
