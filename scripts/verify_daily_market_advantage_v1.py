#!/usr/bin/env python3
"""Offline source verifier for Daily Market Advantage V1."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data/commercial/daily_market_advantage_v1.json"
RUNNER = ROOT / "scripts/commercial/run_daily_market_advantage_v1.py"

AUTHORITY = {
    "relationship": False,
    "consent": False,
    "offer": False,
    "price": False,
    "quote": False,
    "contract": False,
    "external_send": False,
    "payment": False,
    "customer_proof": False,
    "execution": False,
    "production": False,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    require(cfg.get("schema") == "dealix.daily-market-advantage.v1", "config schema")
    require(cfg.get("authority") == AUTHORITY, "config authority must be all false")
    require(cfg.get("wip", {}).get("top_actions_per_cycle") == 3, "top-3 WIP")
    require(set(cfg.get("demand_grades", {})) == {"D1", "D2", "D3", "D4"}, "D1-D4 grades")
    require(cfg["demand_grades"]["D3"].get("requires_extra_evidence") is True, "D3 must require evidence")

    radar = {
        "schema": "dealix.universal-market-radar-brief.v1",
        "generated_at": "2026-09-07T00:00:00+00:00",
        "input_signal_count": 3,
        "ranked_research_signals": [
            {
                "signal_id": "tender-1",
                "company_or_subject": "Public tender",
                "source_id": "ETIMAD_PUBLIC_PROCUREMENT",
                "source_ref": "https://example.invalid/tender",
                "signal_family": "TENDER_OR_PROCUREMENT",
                "market": "SA",
                "sector_family": "government_public_sector",
                "priority_score": 15,
                "stale": False,
                "facts": ["explicit tender"],
                "inferences": [],
                "unknowns": ["eligibility"],
                "evidence_refs": ["e1"],
                "next_evidence": ["official docs"],
                "authority": AUTHORITY,
            },
            {
                "signal_id": "reply-1",
                "company_or_subject": "Inbound reply",
                "source_id": "FIRST_PARTY_INBOUND_AND_RELATIONSHIP",
                "source_ref": "mail-thread",
                "signal_family": "EXPLICIT_EMAIL_REPLY",
                "market": "SA",
                "sector_family": "technology_software",
                "priority_score": 10,
                "stale": False,
                "facts": ["reply exists"],
                "inferences": [],
                "unknowns": ["problem not confirmed"],
                "evidence_refs": ["e2"],
                "next_evidence": ["problem confirmation"],
                "authority": AUTHORITY,
            },
            {
                "signal_id": "change-1",
                "company_or_subject": "Company expansion",
                "source_id": "COMPANY_OWNED_WEB",
                "source_ref": "https://example.invalid/news",
                "signal_family": "COMPANY_CHANGE",
                "market": "SA",
                "sector_family": "technology_software",
                "priority_score": 8,
                "stale": False,
                "facts": ["expansion announced"],
                "inferences": [],
                "unknowns": ["buyer intent"],
                "evidence_refs": ["e3"],
                "next_evidence": ["account research"],
                "authority": AUTHORITY,
            },
        ],
        "authority": AUTHORITY,
    }

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        radar_path = tmp / "radar.json"
        out_path = tmp / "out.json"
        radar_path.write_text(json.dumps(radar), encoding="utf-8")
        cp = subprocess.run(
            [sys.executable, str(RUNNER), "--radar", str(radar_path), "--config", str(CONFIG), "--out", str(out_path)],
            check=False,
            text=True,
            capture_output=True,
        )
        require(cp.returncode == 0, cp.stdout + cp.stderr)
        brief = json.loads(out_path.read_text(encoding="utf-8"))

    require(brief.get("authority") == AUTHORITY, "brief authority must be all false")
    by_id = {row["signal_id"]: row for row in brief["ranked_candidates"]}
    require(by_id["tender-1"]["demand_grade"] == "D4", "tender should be D4")
    require(by_id["reply-1"]["demand_grade"] == "D1", "reply without confirmed problem must not become D3")
    require(by_id["change-1"]["demand_grade"] == "D2", "company change should be D2")
    require(len(brief["top_actions"]) <= 3, "top actions WIP")
    require(brief.get("new_scheduler") is False, "no scheduler")
    require(brief.get("external_send_or_spend") is False, "no outbound/spend")

    print("DEALIX_DAILY_MARKET_ADVANTAGE_VERIFY=PASS")
    print("D3_FALSE_PROMOTION_GUARD=PASS")
    print("D4_PROCUREMENT_SIGNAL_CLASSIFICATION=PASS")
    print("AUTHORITY_ALL_FALSE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
