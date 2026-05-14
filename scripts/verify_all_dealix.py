#!/usr/bin/env python3
"""Wave 19 Recovery — Master CEO Completion Verifier.

Single command the founder runs to know the honest CEO-completion state of
Dealix. Distinct from `scripts/pr235_merge_readiness.sh` (which checks the
*build* is merge-ready). This verifier checks the *company* is moving:

  - build-complete = code + tests + docs ship
  - company-complete = market motion + invoice motion + partner motion

A PASS on every system + ceo_complete=true requires the founder to have
actually sent one anchor partner outreach AND prepared first-invoice
unlock motion. Marker files NEVER lie about market state.

Usage:
    python scripts/verify_all_dealix.py
    python scripts/verify_all_dealix.py --json
    python scripts/verify_all_dealix.py --strict   # exit 1 if any FAIL

Honors the 11 non-negotiables. Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))


# ── System checks ────────────────────────────────────────────────────


def _exists(path: str) -> bool:
    return (REPO / path).exists()


def _check_doctrine() -> dict[str, Any]:
    """Public Dealix Promise + canonical 11 non-negotiables."""
    try:
        from auto_client_acquisition.governance_os.non_negotiables import (
            NON_NEGOTIABLES,
        )
        nn_count = len(NON_NEGOTIABLES)
    except Exception:
        nn_count = 0
    ok = (
        nn_count == 11
        and _exists("docs/THE_DEALIX_PROMISE.md")
        and _exists("api/routers/dealix_promise.py")
        and _exists("docs/00_constitution/NON_NEGOTIABLES.md")
    )
    return {
        "name": "Doctrine (Dealix Promise + 11 Non-Negotiables)",
        "score": 5 if ok else 2,
        "ok": ok,
        "detail": f"{nn_count} non-negotiables registered",
    }


def _check_offer_ladder() -> dict[str, Any]:
    """3-offer ladder + INVESTOR_ONE_PAGER artifact present + commercial-map endpoint."""
    try:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS
        offer_count = len(OFFERINGS)
        floor = min(
            (o.price_sar for o in OFFERINGS if o.price_unit == "per_month"),
            default=0,
        )
    except Exception:
        offer_count, floor = 0, 0
    one_pager = _exists("docs/sales-kit/INVESTOR_ONE_PAGER.md")
    pricing = _exists("docs/sales-kit/PRICING_REFRAME_2026Q2.md")
    ok = offer_count == 3 and floor >= 4999 and one_pager and pricing
    return {
        "name": "Offer Ladder (3 offers + INVESTOR_ONE_PAGER + pricing reframe)",
        "score": 5 if ok else 3,
        "ok": ok,
        "detail": f"{offer_count} offers, floor={floor} SAR/mo, one-pager={one_pager}",
    }


def _check_gcc_standardization() -> dict[str, Any]:
    """GCC pack + thesis + partner archetypes + country priority map."""
    expected = [
        "docs/gcc-expansion/GCC_EXPANSION_THESIS.md",
        "docs/gcc-expansion/GCC_COUNTRY_PRIORITY_MAP.md",
        "docs/gcc-expansion/GCC_PARTNER_ARCHETYPES.md",
        "docs/gcc-expansion/GCC_GO_TO_MARKET_SEQUENCE.md",
        "auto_client_acquisition/governance_os/gcc_markets.py",
        "api/routers/gcc_market_intel.py",
    ]
    missing = [p for p in expected if not _exists(p)]
    ok = not missing
    return {
        "name": "GCC Standardization Pack",
        "score": 5 if ok else (3 if len(missing) <= 1 else 2),
        "ok": ok,
        "detail": f"{len(expected) - len(missing)}/{len(expected)} files present",
        "missing": missing,
    }


def _check_capital_asset_library() -> dict[str, Any]:
    """Capital Asset registry + index + library docs."""
    try:
        from auto_client_acquisition.capital_os.capital_asset_registry import (
            CAPITAL_ASSETS,
        )
        count = len(CAPITAL_ASSETS)
        public_count = sum(1 for a in CAPITAL_ASSETS if a.public)
    except Exception:
        count, public_count = 0, 0
    has_index = _exists("capital-assets/CAPITAL_ASSET_INDEX.json")
    has_library = _exists("capital-assets/CAPITAL_ASSET_LIBRARY.md")
    ok = count >= 10 and has_index and has_library
    return {
        "name": "Capital Asset Library",
        "score": 5 if ok else 3,
        "ok": ok,
        "detail": f"{count} assets ({public_count} public), index={has_index}, library={has_library}",
    }


def _check_open_doctrine() -> dict[str, Any]:
    """Open-doctrine framework files."""
    expected = [
        "open-doctrine/README.md",
        "open-doctrine/GOVERNED_AI_OPS_DOCTRINE.md",
        "open-doctrine/11_NON_NEGOTIABLES.md",
        "open-doctrine/CONTROL_MAPPING.md",
        "open-doctrine/LICENSE.md",
        "open-doctrine/ADOPTION_GUIDE.md",
    ]
    missing = [p for p in expected if not _exists(p)]
    ok = not missing
    return {
        "name": "Open Governed AI Ops Doctrine",
        "score": 5 if ok else 3,
        "ok": ok,
        "detail": f"{len(expected) - len(missing)}/{len(expected)} core files present",
        "missing": missing,
    }


def _check_funding_pack() -> dict[str, Any]:
    """Funding memo + use of funds + hiring scorecards + first 3 hires."""
    expected = [
        "docs/funding/FUNDING_MEMO.md",
        "docs/funding/USE_OF_FUNDS.md",
        "docs/funding/WHY_NOW_GCC_AI_OPS.md",
        "docs/funding/DEALIX_MOAT_STACK.md",
    ]
    optional = [
        "docs/funding/FIRST_3_HIRES.md",
        "docs/funding/HIRING_SCORECARDS.md",
        "docs/funding/HIRING_PLAN.md",
        "docs/funding/INVESTOR_QA.md",
    ]
    missing = [p for p in expected if not _exists(p)]
    optional_present = [p for p in optional if _exists(p)]
    ok = not missing and len(optional_present) >= 2
    return {
        "name": "Funding + Hiring Pack",
        "score": 5 if ok else (4 if not missing else 3),
        "ok": ok,
        "detail": (
            f"required: {len(expected) - len(missing)}/{len(expected)}, "
            f"optional: {len(optional_present)}/{len(optional)}"
        ),
        "missing": missing,
    }


def _check_founder_command_center() -> dict[str, Any]:
    """Page + status marker + Wave 19 cards wired."""
    page = _exists("landing/founder-command-center.html")
    marker_path = REPO / "data" / "founder_command_center_status.json"
    marker_ok = False
    if marker_path.exists():
        try:
            data = json.loads(marker_path.read_text(encoding="utf-8"))
            marker_ok = bool(data.get("deployment_marker"))
        except Exception:
            marker_ok = False
    api = _exists("api/routers/founder_command_center.py")
    ok = page and marker_ok and api
    return {
        "name": "Founder Command Center",
        "score": 5 if ok else 3,
        "ok": ok,
        "detail": f"page={page}, marker={marker_ok}, api={api}",
    }


def _check_partner_motion() -> dict[str, Any]:
    """Partner pipeline JSON + outreach doc + outreach log JSON."""
    pipeline = REPO / "data" / "anchor_partner_pipeline.json"
    log = REPO / "data" / "partner_outreach_log.json"
    doc = _exists("docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md")
    sent_count = 0
    if log.exists():
        try:
            data = json.loads(log.read_text(encoding="utf-8"))
            sent_count = int(data.get("outreach_sent_count", 0))
        except Exception:
            sent_count = 0
    artifacts_ready = pipeline.exists() and log.exists() and doc
    # Score 3 = artifacts ready, 5 = at least one outreach actually sent.
    if not artifacts_ready:
        score, ok = 1, False
    elif sent_count >= 1:
        score, ok = 5, True
    else:
        score, ok = 3, False  # ready but no outreach yet — NOT CEO-complete
    return {
        "name": "Partner Motion",
        "score": score,
        "ok": ok,
        "detail": (
            f"pipeline={pipeline.exists()}, log={log.exists()}, doc={doc}, "
            f"outreach_sent={sent_count} (need >= 1 for score 5)"
        ),
    }


def _check_first_invoice_motion() -> dict[str, Any]:
    """First invoice runbook + log + Moyasar cutover script + ZATCA preflight."""
    runbook = _exists("docs/ops/FIRST_INVOICE_UNLOCK.md")
    log = REPO / "data" / "first_invoice_log.json"
    moyasar = _exists("scripts/moyasar_live_cutover.py")
    zatca = _exists("scripts/zatca_preflight.py")
    sent_count = 0
    if log.exists():
        try:
            data = json.loads(log.read_text(encoding="utf-8"))
            sent_count = int(data.get("invoice_sent_count", 0))
        except Exception:
            sent_count = 0
    artifacts_ready = runbook and log.exists() and moyasar and zatca
    if not artifacts_ready:
        score, ok = 1, False
    elif sent_count >= 1:
        score, ok = 5, True
    else:
        score, ok = 3, False
    return {
        "name": "First Invoice Motion",
        "score": score,
        "ok": ok,
        "detail": (
            f"runbook={runbook}, log={log.exists()}, moyasar={moyasar}, "
            f"zatca={zatca}, invoices_sent={sent_count} (need >= 1 for score 5)"
        ),
    }


# ── Aggregator ───────────────────────────────────────────────────────


SYSTEMS = (
    _check_doctrine,
    _check_offer_ladder,
    _check_gcc_standardization,
    _check_capital_asset_library,
    _check_open_doctrine,
    _check_funding_pack,
    _check_founder_command_center,
    _check_partner_motion,
    _check_first_invoice_motion,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 if any system scores < 5")
    args = parser.parse_args()

    results = [check() for check in SYSTEMS]
    total_systems = len(results)
    passed = sum(1 for r in results if r["score"] >= 4)
    perfect = sum(1 for r in results if r["score"] == 5)
    ceo_complete = perfect == total_systems

    payload = {
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "systems_count": total_systems,
        "systems_passed_at_4_plus": passed,
        "systems_at_5_perfect": perfect,
        "ceo_complete": ceo_complete,
        "ceo_complete_blocker": None if ceo_complete else (
            "company-complete requires score 5 on every system. Build-complete is necessary "
            "but not sufficient — Partner Motion and First Invoice Motion reach score 5 only "
            "after the founder actually sends and an invoice is actually issued."
        ),
        "systems": results,
        "doctrine_link": "docs/THE_DEALIX_PROMISE.md",
        "is_estimate": False,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return (0 if ceo_complete or not args.strict else 1)

    print("━━ Dealix Master Verifier (Wave 19 Recovery) ━━")
    print()
    for r in results:
        emoji = "✅" if r["score"] == 5 else ("🟡" if r["score"] >= 3 else "❌")
        print(f"  {emoji} {r['name']}  →  {r['score']}/5")
        print(f"       {r['detail']}")
        if r.get("missing"):
            for m in r["missing"]:
                print(f"       missing: {m}")
        print()

    print(f"Systems: {total_systems}  ·  Passed at ≥4: {passed}  ·  Perfect (5/5): {perfect}")
    print()
    if ceo_complete:
        print("✅ CEO-complete = YES.")
        print("   Every system at 5/5. The company is moving, not just the build.")
    else:
        print("🟡 CEO-complete = NO (this is expected — the marker files honestly")
        print("   refuse to claim outreach or invoices that have not happened).")
        print()
        print(f"   {payload['ceo_complete_blocker']}")
    return 0 if (ceo_complete or not args.strict) else 1


if __name__ == "__main__":
    raise SystemExit(main())
