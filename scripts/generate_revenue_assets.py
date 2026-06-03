from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dealix_product_network.json"
OUT = ROOT / "reports" / "revenue"

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    payload = json.loads(DATA.read_text(encoding="utf-8"))

    lines = [
        "# Dealix Revenue Asset Index",
        "",
        f"Positioning: {payload['positioning']['one_liner']}",
        "",
        "## Product families",
        "",
    ]

    for family in payload["product_families"]:
        lines.extend([
            f"### {family['name']}",
            "",
            f"- Buyer: {family['buyer']}",
            f"- Outcome: {family['outcome']}",
            f"- Offers: {', '.join(family['offers'])}",
            "",
        ])

    lines.extend(["## Pricing", ""])
    for tier in payload["pricing"]:
        lines.extend([
            f"### {tier['tier']} — SAR {tier['price_sar_month']}/month",
            "",
            tier["best_for"],
            "",
        ])

    (OUT / "dealix_revenue_asset_index.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "dealix_revenue_asset_index.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Generated reports/revenue/dealix_revenue_asset_index.md")
    print("Generated reports/revenue/dealix_revenue_asset_index.json")

if __name__ == "__main__":
    main()
