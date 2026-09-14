#!/usr/bin/env python3
"""Verify OP2 sector diagnostic routes stay free, truthful and Omega V3 compatible.

The historical five executor names may remain only as backward-compatible aliases.
They are never architecture authority. Fresh artifacts should expose the current
Agentic Holding registry receipt and `fixed_five_authority=false`.

Prints: DEALIX_OP2_DIAGNOSTIC_ROUTER_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = REPO_ROOT / "data" / "commercial" / "op2_sector_diagnostic_routes_v1.json"
VERDICT_PASS = "DEALIX_OP2_DIAGNOSTIC_ROUTER_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_DIAGNOSTIC_ROUTER_VERDICT=FAIL"

LEGACY_EXECUTOR_ALIASES = ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"]
LEGACY_ALIAS_SEMANTICS = "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY"
CURRENT_ARCHITECTURE = "agentic_holding_sector_company_mesh"
FREE_DEPTHS = {"D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"}
BANNED_SUBSTRINGS = ("18% leakage", "guaranteed", "best in market", "fixed price", "roi guaranteed")


def main() -> int:
    errors: list[str] = []
    if not ROUTES_PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {ROUTES_PATH}")
        return 1
    try:
        payload = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-sector-diagnostic-routes.v1":
        errors.append("unexpected schema")
    authority = payload.get("authority") or {}
    if any(bool(v) for v in authority.values()):
        errors.append("authority flags must all be false")
    if payload.get("counts_as_pipeline") is not False or payload.get("counts_as_revenue") is not False:
        errors.append("counts_as_pipeline/counts_as_revenue must be false")

    holding = payload.get("agentic_holding")
    if holding is not None:
        if holding.get("architecture") != CURRENT_ARCHITECTURE:
            errors.append("agentic_holding architecture drift")
        if holding.get("fixed_five_authority") is not False:
            errors.append("fixed-five must never be Agentic Holding authority")
        if holding.get("orphan_failures"):
            errors.append("agentic_holding has orphan failures")
        if holding.get("legacy_executor_aliases") != LEGACY_EXECUTOR_ALIASES:
            errors.append("legacy executor alias compatibility drift")

    routes = payload.get("routes") or []
    if not routes:
        errors.append("no routes produced")
    for route in routes:
        sector = route.get("sector_id")
        entry = route.get("diagnostic_entry") or {}
        if entry.get("route") != "/book":
            errors.append(f"{sector}: diagnostic route must be /book")
        if entry.get("api") != "POST /api/v1/public/execution-diagnostic":
            errors.append(f"{sector}: diagnostic api must be the canonical one")
        if set(entry.get("free_depths") or []) - FREE_DEPTHS:
            errors.append(f"{sector}: only D0-D2 may be free")
        if entry.get("card_required") is not False:
            errors.append(f"{sector}: diagnostic must not require a card")
        if entry.get("roi_promised") is not False:
            errors.append(f"{sector}: must not promise ROI")

        handoff = route.get("crm_handoff") or {}
        # Old stored artifacts are tolerated until exact-head regeneration on V,
        # but the compatibility field may never drift into another authority set.
        if handoff.get("canonical_agents") != LEGACY_EXECUTOR_ALIASES:
            errors.append(f"{sector}: legacy executor alias field drift")
        if handoff.get("fixed_five_authority") is True:
            errors.append(f"{sector}: fixed-five architecture authority is forbidden")
        semantics = handoff.get("canonical_agents_field_semantics")
        if semantics is not None and semantics != LEGACY_ALIAS_SEMANTICS:
            errors.append(f"{sector}: legacy alias semantics drift")
        architecture = handoff.get("architecture")
        if architecture is not None and architecture != CURRENT_ARCHITECTURE:
            errors.append(f"{sector}: Agentic Holding architecture drift")
        if handoff.get("legacy_executor_aliases") is not None and handoff.get("legacy_executor_aliases") != LEGACY_EXECUTOR_ALIASES:
            errors.append(f"{sector}: legacy executor aliases mismatch")

        if route.get("truth_class") != "PATTERN_RESEARCH_ROUTING":
            errors.append(f"{sector}: truth_class must be PATTERN_RESEARCH_ROUTING")
        if route.get("allowed_use") != ["INTERNAL_RESEARCH_ONLY"]:
            errors.append(f"{sector}: allowed_use must be INTERNAL_RESEARCH_ONLY")

    text = ROUTES_PATH.read_text(encoding="utf-8").lower()
    for banned in BANNED_SUBSTRINGS:
        if banned in text:
            errors.append(f"banned claim detected: {banned}")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
