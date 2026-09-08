#!/usr/bin/env python3
"""Validate and print the canonical Dealix North Star contract without inventing business evidence."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSTITUTION = ROOT / "config/company/dealix_operating_constitution.json"
SCORECARD = ROOT / "docs/ops/DEALIX_PERMANENT_NORTH_STAR_SCORECARD.md"
AGENTS = (
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
)
PORTFOLIOS = ("TRUST", "MONEY_NOW", "COMPOUNDING")


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "UNKNOWN_NOT_EVIDENCE_BACKED"


def fail(reason: str) -> None:
    raise SystemExit(f"FAIL_NORTH_STAR_CONTRACT={reason}")


def main() -> int:
    if not CONSTITUTION.is_file():
        fail("missing_constitution")
    if not SCORECARD.is_file():
        fail("missing_scorecard")

    data = json.loads(CONSTITUTION.read_text(encoding="utf-8"))
    scorecard = SCORECARD.read_text(encoding="utf-8")

    if data.get("north_star") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        fail("north_star")
    if data.get("optimize_for") != "Verified Economic Movement / Founder Minutes / Cost / Risk":
        fail("objective")
    if tuple(data.get("permanent_agents", [])) != AGENTS:
        fail("permanent_agents")
    if tuple(data.get("portfolios", [])) != PORTFOLIOS:
        fail("portfolios")

    allocation = data.get("opportunity_allocation", {})
    if allocation.get("top_active_actions_per_cycle") != 3:
        fail("top_actions")
    if allocation.get("deep_qualified_limit") != 10:
        fail("deep_qualified")
    if allocation.get("diagnostic_wip_limit") != 3:
        fail("diagnostics")
    if allocation.get("live_project_cell_limit") != 2:
        fail("project_cells")
    if allocation.get("capability_benchmark_limit") != 1:
        fail("capability_benchmarks")
    if data.get("active_gtm_wedge_limit") != 3:
        fail("gtm_wedges")

    whatsapp = data.get("channel_policy", {}).get("whatsapp", {})
    if whatsapp.get("cold_blending_or_blasts_allowed") is not False:
        fail("cold_whatsapp")
    if whatsapp.get("discovered_number_is_permission") is not False:
        fail("public_phone_permission")

    material = set(data.get("material_actions_requiring_exact_current_authority", []))
    required_material = {
        "MERGE_MAIN",
        "PRODUCTION_DEPLOY_OR_REDEPLOY",
        "DNS_MUTATION",
        "PRODUCTION_DB_OR_SCHEMA_MUTATION",
        "SECRET_OR_IDENTITY_MUTATION",
        "EXTERNAL_CUSTOMER_SEND",
        "PUBLIC_PUBLISH",
        "PAID_SPEND",
        "PAYMENT_OR_REFUND",
        "BINDING_QUOTE_CONTRACT_OR_TENDER",
        "LIVE_VOICE_ACTIVATION",
    }
    if not required_material <= material:
        fail("material_authority")

    for needle in (
        "VERIFIED_CASH_SAR",
        "MRR_SAR",
        "CUSTOMER_ACCEPTED_PROOF_PACKS",
        "M5 — Q1 Revenue",
        "No stage may be inferred from the stage before it.",
    ):
        if needle not in scorecard:
            fail(f"scorecard::{needle}")

    print("NORTH_STAR=CASH_READY_AUTONOMOUS_DEALIX_COMPANY")
    print("OPTIMIZE_FOR=Verified Economic Movement / Founder Minutes / Cost / Risk")
    print(f"SOURCE_HEAD={git_value('rev-parse', 'HEAD')}")
    print(f"SOURCE_BRANCH={git_value('branch', '--show-current')}")
    print("PERMANENT_AGENT_COUNT=5")
    print("PERMANENT_AGENTS=" + ",".join(AGENTS))
    print("PORTFOLIOS=" + ",".join(PORTFOLIOS))
    print("EXECUTIVE_TOP_ACTIONS_MAX=3")
    print("MATERIAL_APPROVAL_PACKETS_MAX=1")
    print("PUBLIC_PHONE_IS_CONSENT=false")
    print("PRODUCTION_GREEN=NOT_INFERRED")
    print("BUSINESS_EVIDENCE=READ_FROM_CURRENT_RECEIPTS_ONLY")
    print("RESULT=PASS_NORTH_STAR_CONTRACT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
