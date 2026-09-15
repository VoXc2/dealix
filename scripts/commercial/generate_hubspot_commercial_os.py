#!/usr/bin/env python3
"""Generate Dealix HubSpot Commercial OS reports.

Local-only generator based on seed intelligence. It does not call HubSpot and
it does not write to CRM. Use it to prepare founder-reviewed actions.
"""
from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = ROOT / "data" / "commercial" / "hubspot_commercial_os_seed.json"
OUT_DIR = ROOT / "reports" / "hubspot_os"


def load_seed() -> dict:
    return json.loads(SEED_PATH.read_text(encoding="utf-8"))


def build_markdown(seed: dict) -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix HubSpot Commercial OS — {today}",
        "",
        "## Operating verdict",
        "",
        "Dealix Company OS / Revenue Mesh owns commercial truth. HubSpot is an operational CRM mirror only; CRM records, stages and amounts are observations and cannot prove relationship, qualified opportunity, payment, revenue or public pricing authority.",
        "",
        "## CRM write policy",
        "",
        "Baseline is read-only intelligence. Any CRM write-back remains fail-closed behind canonical relationship/evidence gates and the applicable action-bound authority; no write is performed by this generator.",
        "",
        "## Target groups found",
        "",
        "| Target group | Industry | Sector | Offer | Pain angle |",
        "|---|---|---|---|---|",
    ]
    for item in seed["target_groups_found"]:
        lines.append(
            f"| {item['name']} | {item.get('industry', '')} | {item['recommended_sector']} | {item['recommended_offer']} | {item['pain_angle']} |"
        )
    lines += [
        "",
        "## Existing tasks that support launch",
        "",
    ]
    lines.extend(f"- {task}" for task in seed["tasks_found"])
    lines += [
        "",
        "## Next CRM actions to propose",
        "",
        "1. Create one Dealix product catalog inside HubSpot after owner approval.",
        "2. Create tasks for each target group: verify, draft, call, proposal.",
        "3. Create notes on selected companies with Dealix pain hypothesis and recommended offer.",
        "4. Create deals only after a qualified discovery call.",
        "5. Attach line items only after scope is approved.",
        "",
        "## Suggested service catalog",
        "",
        "| Product | Type | Suggested price | Revenue model |",
        "|---|---|---:|---|",
        "| Revenue Command Room Sprint | service | Customer-specific quote | scope/terms after qualified discovery |",
        "| Company Brain Sprint | service | Customer-specific quote | scope/terms after qualified discovery |",
        "| Follow-up Recovery Sprint | service | Customer-specific quote | scope/terms after qualified discovery |",
        "| AI Sales Agent Setup | service | Customer-specific quote | scope/terms after qualified discovery |",
        "| AI Trust and Governance OS | service | Customer-specific quote | scope/terms after qualified discovery |",
        "| Client Delivery OS | service | Customer-specific quote | scope/terms after qualified discovery |",
        "",
        "## Metrics to track in HubSpot",
        "",
        "- target groups verified",
        "- tasks completed",
        "- discovery calls booked",
        "- proposals created",
        "- mirrored deal amount (observational only; not verified revenue)",
        "- mirrored deal stage (observational only; not commercial truth)",
        "- close rate",
        "- monthly retainer conversion",
        "- verified cash only from canonical payment evidence; HubSpot may mirror the evidenced state",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    seed = load_seed()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "read_only_proposal",
        "seed": seed,
        "recommended_next_step": "Review proposed HubSpot write-back before creating tasks, notes, products, or deals.",
    }
    (OUT_DIR / "latest.md").write_text(build_markdown(seed), encoding="utf-8")
    (OUT_DIR / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("HUBSPOT_COMMERCIAL_OS_GENERATED=reports/hubspot_os/latest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
