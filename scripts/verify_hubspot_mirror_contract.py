#!/usr/bin/env python3
"""Verify that HubSpot remains a CRM mirror, never a commercial truth owner."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/hubspot_mirror_contract.json"
DOC = ROOT / "docs/ops/HUBSPOT_FULL_AUTO_COMMERCIAL_OS.md"
CRM = ROOT / "auto_client_acquisition/agents/crm.py"
FACADE = ROOT / "integrations/hubspot.py"
PIPELINE = ROOT / "auto_client_acquisition/pipeline.py"
POLICY = ROOT / "auto_client_acquisition/revenue_os/crm_mirror_policy.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(data["truth_owner"] == "DEALIX_COMPANY_OS", "truth owner drift")
    require(data["hubspot_role"] == "CRM_MIRROR", "HubSpot role drift")
    require(data["contact_mirror"]["default_allowed"] is False, "contact mirror must fail closed")
    require(data["deal_mirror"]["default_allowed"] is False, "deal mirror must fail closed")
    require(data["amount_semantics"]["crm_amount_is_verified_revenue"] is False, "CRM amount cannot equal revenue")

    doc = DOC.read_text(encoding="utf-8")
    crm = CRM.read_text(encoding="utf-8")
    facade = FACADE.read_text(encoding="utf-8")
    pipeline = PIPELINE.read_text(encoding="utf-8")
    policy = POLICY.read_text(encoding="utf-8")

    require("Dealix Company OS / Revenue Mesh as the commercial source of truth" in doc, "doc authority missing")
    require("HubSpot as an operational **CRM mirror**" in doc, "CRM mirror wording missing")
    require("Use HubSpot as the commercial source of truth" not in doc, "legacy HubSpot truth wording returned")

    require("create_deal: bool = False" in crm, "CRMAgent deal default must remain false")
    require("noemail+" not in crm, "fabricated placeholder email returned")

    # Comments/docstrings are allowed to explain that lead.budget must never become
    # HubSpot amount. Reject executable-looking assignments or payload mappings that
    # actually source CRM amount from lead.budget instead of verified quote authority.
    budget_to_amount_patterns = (
        r'properties\s*\[\s*["\']amount["\']\s*\]\s*=\s*(?:str\s*\(\s*)?lead\.budget',
        r'["\']amount["\']\s*:\s*(?:str\s*\(\s*)?lead\.budget',
        r'amount\s*=\s*(?:str\s*\(\s*)?lead\.budget',
    )
    require(
        not any(re.search(pattern, crm) for pattern in budget_to_amount_patterns),
        "lead budget must not become HubSpot amount",
    )
    require("approved_quote_amount_sar" in crm, "verified quote amount mirror authority missing")
    require("evaluate_hubspot_mirror" in crm, "CRM truth gate missing")
    require("closedwon requires verified payment evidence" in crm, "closedwon payment guard missing")

    require("create_deal: bool = False" in facade, "HubSpot facade deal default must remain false")
    require("evaluate_hubspot_mirror" in pipeline, "legacy pipeline truth gate missing")
    require("auto_book: bool = False" in pipeline, "legacy auto-book must remain fail closed")
    require("distribution_blocked_unverified_relationship" in pipeline, "legacy distribution evidence gate missing")

    for token in (
        "AUTHORITY_NOT_VERIFIED",
        "TRUTH_CLASS_NOT_REAL",
        "NO_EVIDENCE_ID",
        "RELATIONSHIP_NOT_VERIFIED",
        "NO_REAL_CONTACT_IDENTIFIER",
        "NO_OPPORTUNITY_ID",
        "WON_WITHOUT_PAYMENT_EVIDENCE",
    ):
        require(token in policy, f"policy reason missing: {token}")

    print("HUBSPOT_MIRROR_CONTRACT=PASS")
    print("TRUTH_OWNER=DEALIX_COMPANY_OS")
    print("HUBSPOT_ROLE=CRM_MIRROR")
    print("DEFAULT_DEAL_CREATION=BLOCKED")
    print("PLACEHOLDER_EMAIL=BLOCKED")
    print("FIT_SCORE_TO_PIPELINE_TRUTH=BLOCKED")
    print("CLOSEDWON_WITHOUT_PAYMENT_EVIDENCE=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())