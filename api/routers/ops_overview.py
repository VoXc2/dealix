"""Unified Ops API — Dealix Full Ops command layer.

A thin aggregator that gives the founder one coherent overview across
the existing OS modules. It reads the persistent JSONL stores directly
(affiliate, approval, referral, evidence) — it never calls LLMs, never
sends anything, and never mutates state. Each endpoint also lists the
canonical deeper endpoints as ``sources`` so the founder can drill in.

Endpoints:
  GET /api/v1/ops/founder/overview
  GET /api/v1/ops/sales/pipeline
  GET /api/v1/ops/partners/dashboard
  GET /api/v1/ops/support/inbox
  GET /api/v1/ops/governance/status
"""
from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/ops", tags=["ops-overview"])

_GUARDRAILS = {
    "no_llm_calls": True,
    "no_external_sends": True,
    "read_only": True,
}


def _now() -> str:
    return datetime.now(UTC).isoformat()


# ── Safe aggregators (each degrades gracefully) ──────────────────────


def _approval_counts() -> dict[str, Any]:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )

        store = get_default_approval_store()
        pending = store.list_pending()
        history = store.list_history(limit=500)
        by_status = Counter(str(r.status) for r in history)
        return {
            "available": True,
            "pending": len(pending),
            "by_status": dict(by_status),
            "blocked": int(by_status.get("blocked", 0)),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _commission_summary() -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os import store as aff_store
        from auto_client_acquisition.affiliate_os.commission import (
            CommissionStatus,
        )

        commissions = aff_store.list_commissions()
        by_status = Counter(c.status for c in commissions)
        owed = sum(
            c.amount_sar
            for c in commissions
            if c.status
            in (
                CommissionStatus.ELIGIBLE.value,
                CommissionStatus.PAYOUT_REQUESTED.value,
            )
        )
        paid = sum(
            c.amount_sar
            for c in commissions
            if c.status == CommissionStatus.PAID.value
        )
        return {
            "available": True,
            "count": len(commissions),
            "by_status": dict(by_status),
            "owed_sar": round(owed, 2),
            "paid_sar": round(paid, 2),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _affiliate_summary() -> dict[str, Any]:
    try:
        from auto_client_acquisition.affiliate_os import store as aff_store

        affiliates = aff_store.list_affiliates()
        by_status = Counter(a.status for a in affiliates)
        return {
            "available": True,
            "count": len(affiliates),
            "by_status": dict(by_status),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _referral_summary() -> dict[str, Any]:
    try:
        from auto_client_acquisition.partnership_os.referral_store import (
            list_referrals,
        )

        referrals = list_referrals()
        by_status = Counter(r.status for r in referrals)
        return {
            "available": True,
            "count": len(referrals),
            "by_status": dict(by_status),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _evidence_count() -> dict[str, Any]:
    try:
        from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
            list_evidence,
        )

        items = list_evidence(customer_id="affiliate_os", limit=500)
        # affiliate_os evidence is customer-scoped per affiliate; the
        # project_id field carries the module name.
        by_project = Counter(i.project_id or "unknown" for i in items)
        return {
            "available": True,
            "affiliate_os_project_events": int(by_project.get("affiliate_os", 0)),
        }
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def _kb_articles() -> dict[str, Any]:
    try:
        from pathlib import Path

        kb_dir = Path(__file__).resolve().parents[2] / "docs" / "knowledge-base"
        if not kb_dir.exists():
            return {"available": False, "error": "knowledge-base dir not found"}
        articles = sorted(p.name for p in kb_dir.glob("*.md"))
        return {"available": True, "count": len(articles), "articles": articles}
    except Exception as exc:
        return {"available": False, "error": str(exc)}


# ── Endpoints ────────────────────────────────────────────────────────


@router.get("/founder/overview")
async def founder_overview() -> dict[str, Any]:
    """One-pane founder overview across leads-to-cash and governance."""
    approvals = _approval_counts()
    commissions = _commission_summary()
    affiliates = _affiliate_summary()
    referrals = _referral_summary()
    return {
        "service": "ops_overview",
        "view": "founder_overview",
        "generated_at": _now(),
        "guardrails": _GUARDRAILS,
        "approvals": approvals,
        "affiliate_commissions": commissions,
        "affiliates": affiliates,
        "referrals": referrals,
        "evidence": _evidence_count(),
        "action_items": {
            "approvals_pending": approvals.get("pending", 0),
            "commission_owed_sar": commissions.get("owed_sar", 0),
            "blocked_actions": approvals.get("blocked", 0),
        },
        "sources": [
            "/api/v1/approvals/pending",
            "/api/v1/affiliate-os/commission/list",
            "/api/v1/ops/sales/pipeline",
            "/api/v1/ops/partners/dashboard",
            "/api/v1/ops/governance/status",
        ],
    }


@router.get("/sales/pipeline")
async def sales_pipeline() -> dict[str, Any]:
    """Pipeline overview — referral and affiliate-commission stages."""
    return {
        "service": "ops_overview",
        "view": "sales_pipeline",
        "generated_at": _now(),
        "guardrails": _GUARDRAILS,
        "referrals": _referral_summary(),
        "affiliate_commissions": _commission_summary(),
        "sources": [
            "/api/v1/revenue-os/status",
            "/api/v1/referrals/_program-terms",
            "/api/v1/affiliate-os/commission/list",
        ],
    }


@router.get("/partners/dashboard")
async def partners_dashboard() -> dict[str, Any]:
    """Partner + affiliate dashboard — registrations, referrals, commissions."""
    commissions = _commission_summary()
    void_count = 0
    if commissions.get("available"):
        void_count = int(commissions.get("by_status", {}).get("void", 0))
    return {
        "service": "ops_overview",
        "view": "partners_dashboard",
        "generated_at": _now(),
        "guardrails": _GUARDRAILS,
        "affiliates": _affiliate_summary(),
        "referrals": _referral_summary(),
        "affiliate_commissions": commissions,
        "compliance_flags": {
            "void_commissions": void_count,
            "note": "void = commission disqualified by lead flags",
        },
        "sources": [
            "/api/v1/affiliate-os/status",
            "/api/v1/partnership-os/status",
        ],
    }


@router.get("/support/inbox")
async def support_inbox() -> dict[str, Any]:
    """Support overview — knowledge-base coverage + module pointers.

    The live ticket queue is owned by support_os; this view reports the
    knowledge-base coverage that auto-answers depend on.
    """
    return {
        "service": "ops_overview",
        "view": "support_inbox",
        "generated_at": _now(),
        "guardrails": _GUARDRAILS,
        "knowledge_base": _kb_articles(),
        "sources": [
            "/api/v1/support-os/status",
            "/api/v1/support-inbox/tickets",
            "/api/v1/support-journey/status",
        ],
    }


@router.get("/governance/status")
async def governance_status() -> dict[str, Any]:
    """Governance overview — approvals, blocked actions, evidence."""
    approvals = _approval_counts()
    return {
        "service": "ops_overview",
        "view": "governance_status",
        "generated_at": _now(),
        "guardrails": _GUARDRAILS,
        "approvals": approvals,
        "evidence": _evidence_count(),
        "doctrine": {
            "no_external_action_without_approval": True,
            "no_payout_before_invoice_paid": True,
            "every_high_risk_action_has_evidence": True,
        },
        "sources": [
            "/api/v1/approvals/pending",
            "/api/v1/approvals/history",
        ],
    }
