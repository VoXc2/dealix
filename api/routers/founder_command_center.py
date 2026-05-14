"""Founder Command Center — Wave 18.

Single-pane-of-glass aggregate the founder hits ONE URL from their phone
to see everything: deploy health, doctrine health, daily-routine state,
commercial-ladder commitments, anchor-partner pipeline state, SAR
pacing toward the Day-90 100K ARR gate, and the 3-decision next-action
recommendation.

This endpoint COMPOSES the existing Wave 14-17 modules. It is admin-gated
because some signals (renewal SAR, anchor partner pipeline) are commercial-
sensitive. A read-only PUBLIC view is exposed at `/public` showing only
the doctrine surface (number of commitments, all-green status, manifesto
URL) — what a procurement reviewer needs.

Endpoints:
  GET /api/v1/founder/command-center           → admin-gated full aggregate
  GET /api/v1/founder/command-center/public    → public (doctrine + offer count)
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends

from api.security.api_key import require_admin_key

router = APIRouter(prefix="/api/v1/founder/command-center", tags=["founder"])

_REPO = Path(__file__).resolve().parent.parent.parent


def _deploy_health() -> dict[str, Any]:
    """In-process production smoke: do the canonical Wave 14-17 modules import?"""
    targets = (
        "auto_client_acquisition.service_catalog.registry",
        "auto_client_acquisition.governance_os.non_negotiables",
        "auto_client_acquisition.proof_os.proof_pack",
        "auto_client_acquisition.capital_os.capital_ledger",
        "auto_client_acquisition.payment_ops.renewal_scheduler",
    )
    failures: list[str] = []
    for path in targets:
        try:
            __import__(path, fromlist=["*"])
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path}: {type(exc).__name__}")
    return {
        "checked": len(targets),
        "failed": failures,
        "all_green": not failures,
    }


def _doctrine_health() -> dict[str, Any]:
    """Wave 17 manifesto count + (in-process) test-file existence check."""
    try:
        from auto_client_acquisition.governance_os.non_negotiables import (
            NON_NEGOTIABLES,
        )
    except Exception:  # noqa: BLE001
        return {"commitments_count": 0, "all_enforcers_exist": False}
    missing: list[str] = []
    for n in NON_NEGOTIABLES:
        for rel in n.enforced_by:
            if not (_REPO / rel).exists():
                missing.append(f"{n.id}::{rel}")
    return {
        "commitments_count": len(NON_NEGOTIABLES),
        "missing_enforcers": missing,
        "all_enforcers_exist": not missing,
    }


def _offer_ladder_summary() -> dict[str, Any]:
    """2026-Q2 reframe ladder summary — 3 offers, lowest paid SAR, highest one-time SAR."""
    try:
        from auto_client_acquisition.service_catalog.registry import OFFERINGS
    except Exception:  # noqa: BLE001
        return {"offer_count": 0}
    paid = [o for o in OFFERINGS if o.price_sar > 0]
    monthly = [o for o in paid if o.price_unit == "per_month"]
    one_time = [o for o in paid if o.price_unit == "one_time"]
    return {
        "offer_count": len(OFFERINGS),
        "paid_floor_sar_per_month": min((o.price_sar for o in monthly), default=0),
        "flagship_sar_one_time": max((o.price_sar for o in one_time), default=0),
        "offer_ids": [o.id for o in OFFERINGS],
    }


def _daily_routine_state() -> dict[str, Any]:
    """Whether today's consolidated daily routine markdown exists."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    p = _REPO / "data" / "daily_routine" / f"{today}.md"
    return {
        "today": today,
        "consolidated_brief_exists": p.exists(),
        "path": str(p.relative_to(_REPO)) if p.exists() else None,
    }


def _anchor_partner_pipeline() -> dict[str, Any]:
    p = _REPO / "data" / "anchor_partner_pipeline.json"
    if not p.exists():
        return {"seeded": False, "partner_count": 0}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"seeded": False, "partner_count": 0}
    partners = data.get("partners", [])
    by_status: dict[str, int] = {}
    for p_ in partners:
        s = p_.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    return {
        "seeded": True,
        "partner_count": len(partners),
        "by_status": by_status,
    }


def _arr_pacing_toward_day90() -> dict[str, Any]:
    """SAR committed in the renewal pipeline within next 90 days +
    pacing vs 100K SAR ARR Day-90 gate from FOUNDER_90_DAY_CADENCE.md.
    """
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import (
            list_due,
        )
        cutoff = datetime.now(timezone.utc) + timedelta(days=90)
        renewals = list_due(on_date=cutoff)
        sar_committed = sum(int(getattr(r, "amount_sar", 0)) for r in renewals)
    except Exception:  # noqa: BLE001
        sar_committed = 0
    target_sar = 100_000
    return {
        "sar_committed_next_90d": sar_committed,
        "target_sar_day90": target_sar,
        "percent_of_target": round(
            (sar_committed / target_sar) * 100, 1
        ) if target_sar > 0 else 0.0,
        "target_doc": "docs/ops/FOUNDER_90_DAY_CADENCE.md",
    }


def _capital_assets_this_week() -> int:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
        assets = list_assets(limit=100)
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        count = 0
        for a in assets:
            try:
                created = datetime.fromisoformat(a.created_at)
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if created >= cutoff:
                count += 1
        return count
    except Exception:  # noqa: BLE001
        return 0


# ── Wave 19: GCC + Capital Asset Library + Open Doctrine + Funding ────


def _gcc_standard_readiness() -> dict[str, Any]:
    """Wave 19: GCC market posture readiness."""
    try:
        from auto_client_acquisition.governance_os.gcc_markets import GCC_MARKETS
        active = sum(1 for m in GCC_MARKETS if m.dealix_status == "active")
        pilot = sum(1 for m in GCC_MARKETS if m.dealix_status == "pilot_ready")
        return {
            "market_count": len(GCC_MARKETS),
            "active": active,
            "pilot_ready": pilot,
            "future": sum(1 for m in GCC_MARKETS if m.dealix_status == "future_market"),
            "endpoint": "GET /api/v1/gcc-markets/markdown",
        }
    except Exception:  # noqa: BLE001
        return {"market_count": 0, "active": 0, "pilot_ready": 0, "future": 0}


def _capital_asset_registry_state() -> dict[str, Any]:
    """Wave 19: strategic Capital Asset registry."""
    try:
        from auto_client_acquisition.capital_os.capital_asset_registry import (
            CAPITAL_ASSETS,
        )
        public = sum(1 for a in CAPITAL_ASSETS if a.public)
        live = sum(1 for a in CAPITAL_ASSETS if a.maturity == "live")
        return {
            "asset_count": len(CAPITAL_ASSETS),
            "public_count": public,
            "live_count": live,
            "endpoint_admin": "GET /api/v1/capital-assets",
            "endpoint_public": "GET /api/v1/capital-assets/public",
        }
    except Exception:  # noqa: BLE001
        return {"asset_count": 0, "public_count": 0, "live_count": 0}


def _open_doctrine_status() -> dict[str, Any]:
    """Wave 19: Open Governed AI Operations Doctrine readiness."""
    open_doctrine_dir = _REPO / "open-doctrine"
    license_path = open_doctrine_dir / "LICENSE.md"
    readme_path = open_doctrine_dir / "README.md"
    return {
        "open_doctrine_dir_exists": open_doctrine_dir.exists(),
        "license_present": license_path.exists(),
        "readme_present": readme_path.exists(),
        "framework_endpoint": "GET /api/v1/doctrine",
        "controls_endpoint": "GET /api/v1/doctrine/controls",
    }


def _funding_pack_status() -> dict[str, Any]:
    """Wave 19: funding pack readiness (set of required docs on disk)."""
    funding_dir = _REPO / "docs" / "funding"
    required = (
        "FUNDING_MEMO.md",
        "USE_OF_FUNDS.md",
        "WHY_NOW_GCC_AI_OPS.md",
        "FIRST_3_HIRES.md",
        "HIRING_SCORECARDS.md",
    )
    present = []
    missing = []
    for name in required:
        if (funding_dir / name).exists():
            present.append(name)
        else:
            missing.append(name)
    return {
        "required_count": len(required),
        "present_count": len(present),
        "missing": missing,
        "ready": not missing,
    }


def _top_three_next_actions(state: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    arr = state.get("arr_pacing", {})
    pipeline = state.get("anchor_partners", {})
    routine = state.get("daily_routine", {})
    if not routine.get("consolidated_brief_exists"):
        actions.append(
            "Run `python scripts/daily_routine.py --quick` to generate today's brief."
        )
    if pipeline.get("seeded") and pipeline.get("partner_count", 0) > 0:
        queued = pipeline.get("by_status", {}).get("queued_for_founder_call", 0)
        if queued > 0:
            actions.append(
                f"Book {queued} anchor-partner call(s) from `data/anchor_partner_pipeline.json` "
                "this week (target: 3 calls / 7 days)."
            )
    if arr.get("sar_committed_next_90d", 0) < arr.get("target_sar_day90", 100_000):
        gap = arr["target_sar_day90"] - arr["sar_committed_next_90d"]
        actions.append(
            f"{gap:,.0f} SAR ARR gap to Day-90 target. Close 1 retainer (4,999/mo × 3 = 14,997) "
            "or 1 flagship Sprint (25,000) to compress the gap."
        )
    if not actions:
        actions.append("All KPIs on track. Publish 1 LinkedIn post + 2 warm outreaches.")
    while len(actions) < 3:
        actions.append(
            "Read `docs/THE_DEALIX_PROMISE.md` and pick one paragraph to share with one prospect."
        )
    return actions[:3]


@router.get("", dependencies=[Depends(require_admin_key)])
async def command_center() -> dict[str, Any]:
    """Admin-gated full aggregate — the founder's single-pane-of-glass."""
    state: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "deploy_health": _deploy_health(),
        "doctrine_health": _doctrine_health(),
        "offer_ladder": _offer_ladder_summary(),
        "daily_routine": _daily_routine_state(),
        "anchor_partners": _anchor_partner_pipeline(),
        "arr_pacing": _arr_pacing_toward_day90(),
        "capital_assets_this_week": _capital_assets_this_week(),
        # Wave 19 additions — GCC + Capital + Open Doctrine + Funding
        "gcc_standard_readiness": _gcc_standard_readiness(),
        "capital_asset_registry": _capital_asset_registry_state(),
        "open_doctrine_status": _open_doctrine_status(),
        "funding_pack_status": _funding_pack_status(),
        "manifesto_endpoint": "GET /api/v1/dealix-promise/markdown",
        "commercial_map_endpoint": "GET /api/v1/commercial-map/markdown",
        "doctrine_endpoint": "GET /api/v1/doctrine/markdown",
        "gcc_markets_endpoint": "GET /api/v1/gcc-markets/markdown",
        "capital_assets_public_endpoint": "GET /api/v1/capital-assets/public",
        "post_deploy_check_endpoint": "GET /api/v1/founder/post-deploy-check",
        "governance_decision": "allow",
        "is_estimate": False,
    }
    state["top_three_next_actions"] = _top_three_next_actions(state)
    return state


@router.get("/public")
async def command_center_public() -> dict[str, Any]:
    """Public read-only view — what a procurement reviewer can see.

    No commercial-sensitive numbers: only doctrine surface + offer count
    + manifesto URL. Helps the CISO verify the perimeter from the brand's
    own front door.
    """
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "doctrine_health": _doctrine_health(),
        "offer_ladder": _offer_ladder_summary(),
        "manifesto_endpoint": "GET /api/v1/dealix-promise/markdown",
        "commercial_map_endpoint": "GET /api/v1/commercial-map/markdown",
        "governance_decision": "allow",
        "is_estimate": False,
    }
