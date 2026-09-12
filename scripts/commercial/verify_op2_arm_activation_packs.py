#!/usr/bin/env python3
"""Verify OP2 arm activation packs are truth-safe and bound to existing arms.

Enforces the OP2 activation truth laws:
  * exactly 44 canonical arms referenced (no new arms, no new agents)
  * every pack arm exists in the canonical registry
  * ACTIVE_DEEP Top-3 unchanged (ARM-001/002/003) and state changes = 0
  * D0-D2 free, no card, no ROI promise
  * no public fixed price (quote after qualified discovery)
  * no certification / licensed-provider / government-access claims
  * all external effects false; authority flags false; L5_EXECUTED=NONE

Prints: DEALIX_OP2_ARM_PACKS_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKS_PATH = REPO_ROOT / "data" / "commercial" / "op2_arm_activation_packs_v1.json"
ARM_REGISTRY = REPO_ROOT / "config" / "company" / "dealix_arm_registry.json"
VERDICT_PASS = "DEALIX_OP2_ARM_PACKS_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_ARM_PACKS_VERDICT=FAIL"

REQUIRED_ACTIVE_DEEP = ["ARM-001", "ARM-002", "ARM-003"]
FREE_DEPTHS = {"D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"}
REQUIRED_PACK_FIELDS = (
    "icp",
    "free_diagnostic",
    "qualification_gates",
    "proposal_skeleton",
    "acceptance_criteria",
    "proof_requirements",
    "delivery_runbook",
    "stop_loss",
    "partner_regulatory_boundary",
    "content_seo_drafts",
    "next_evidence_required",
)
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}")


def main() -> int:
    errors: list[str] = []
    for path in (PACKS_PATH, ARM_REGISTRY):
        if not path.exists():
            print(VERDICT_FAIL)
            print(f"  - missing {path}")
            return 1
    try:
        payload = json.loads(PACKS_PATH.read_text(encoding="utf-8"))
        registry = json.loads(ARM_REGISTRY.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-arm-activation-packs.v1":
        errors.append("unexpected schema")
    if payload.get("new_arms_created") != 0:
        errors.append("new_arms_created must be 0")
    if payload.get("new_permanent_agents_created") != 0:
        errors.append("new_permanent_agents_created must be 0")
    if payload.get("l5_executed") != "NONE":
        errors.append("l5_executed must be NONE")

    registry_ids = {arm["id"] for arm in registry["arms"]}
    if len(registry_ids) != 44:
        errors.append(f"canonical registry must have exactly 44 arms, got {len(registry_ids)}")

    for pack in payload.get("packs") or []:
        pid = pack.get("pack_id")
        for arm in pack.get("arms") or []:
            if arm not in registry_ids:
                errors.append(f"{pid}: arm {arm} not in canonical registry")
        for field in REQUIRED_PACK_FIELDS:
            if not pack.get(field):
                errors.append(f"{pid}: missing required field {field}")
        diag = pack.get("free_diagnostic") or {}
        if set(diag.get("depths") or []) - FREE_DEPTHS:
            errors.append(f"{pid}: diagnostic depths must be D0-D2 only")
        if diag.get("card_required") is not False:
            errors.append(f"{pid}: diagnostic must not require a card")
        if diag.get("roi_promised") is not False:
            errors.append(f"{pid}: must not promise ROI")
        if (pack.get("proposal_skeleton") or {}).get("public_fixed_price") is not False:
            errors.append(f"{pid}: public_fixed_price must be false")
        if (pack.get("proposal_skeleton") or {}).get("pricing_basis") != "QUOTE_AFTER_QUALIFIED_DISCOVERY":
            errors.append(f"{pid}: pricing_basis must be QUOTE_AFTER_QUALIFIED_DISCOVERY")
        if pack.get("certification_claim") is not False:
            errors.append(f"{pid}: certification_claim must be false")
        if not pack.get("authority_all_false"):
            errors.append(f"{pid}: official signals must have all-false authority")
        effects = pack.get("external_effects") or {}
        if any(bool(v) for v in effects.values()):
            errors.append(f"{pid}: external effects must all be false")
        if pack.get("truth_class") != "PATTERN_RESEARCH_PACK":
            errors.append(f"{pid}: truth_class must be PATTERN_RESEARCH_PACK")
        for key in ("counts_as_pipeline", "counts_as_revenue", "counts_as_relationship"):
            if pack.get(key) is not False:
                errors.append(f"{pid}: {key} must be false")
        drafts = pack.get("content_seo_drafts") or {}
        if drafts.get("publish_authority") is not False:
            errors.append(f"{pid}: content drafts must not have publish authority")

    # Open-banking pack must never claim a licensed provider.
    pack_d = next((p for p in payload.get("packs") or [] if p["pack_id"].endswith("OPEN-BANKING")), None)
    if pack_d is None:
        errors.append("missing open-banking pack")
    else:
        boundary = (pack_d.get("partner_regulatory_boundary") or {}).get("licensed_provider_claim")
        if boundary != "NONE_NEVER":
            errors.append("open-banking pack must set licensed_provider_claim=NONE_NEVER")

    ranking = payload.get("ranking") or {}
    if ranking.get("arm_count") != 44:
        errors.append(f"ranking must cover 44 arms, got {ranking.get('arm_count')}")
    if ranking.get("state_changes_applied") != 0:
        errors.append("ranking must apply 0 state changes")
    locked = [row.get("arm_id") for row in ranking.get("active_deep_locked_top3") or []]
    if locked != REQUIRED_ACTIVE_DEEP:
        errors.append(f"ACTIVE_DEEP locked top3 must be {REQUIRED_ACTIVE_DEEP}, got {locked}")
    if ranking.get("deep_wip_max") != 3:
        errors.append("deep_wip_max must be 3")
    for row in ranking.get("rows") or []:
        if row.get("state_change_allowed") is not False:
            errors.append(f"{row.get('arm_id')}: state_change_allowed must be false")
        if row.get("disposition") != "RESEARCH_ONLY_NO_STATE_CHANGE":
            errors.append(f"{row.get('arm_id')}: disposition must be RESEARCH_ONLY_NO_STATE_CHANGE")

    if SECRET_RE.search(PACKS_PATH.read_text(encoding="utf-8")):
        errors.append("secret-like content detected")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
