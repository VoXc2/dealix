"""V12 — Full-Ops umbrella router.

Single ``GET /api/v1/full-ops/daily-command-center`` rolling up every
Full Ops 2.0 subsystem — the work queues (growth / sales / support /
customer-success / delivery / compliance), the Partner/Affiliate OS,
the Evidence Ledger and the Learning loops — plus top-3 decisions,
blocked actions, revenue truth and the hard gates.

Read-only. No external calls. Returns 200 always; degraded sections
are reported in ``degraded_sections`` rather than raising 5xx.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.full_ops import (
    WorkItem,
    get_default_queue,
    prioritize,
)

router = APIRouter(prefix="/api/v1/full-ops", tags=["full-ops"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "no_linkedin_automation": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


def _safe(name: str, fn, default, degraded: list[str]) -> Any:
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001 — never crash command center
        degraded.append(name)
        return {
            "_error": True,
            "_type": type(exc).__name__,
            "_default": default,
        }


def _growth_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("growth")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _sales_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("sales")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _support_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("support")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _cs_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("customer_success")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _delivery_queue() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("delivery")
    return {
        "count": len(items),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _compliance_alerts() -> dict[str, Any]:
    queue = get_default_queue()
    items = queue.list_by_os("compliance")
    escalated = [it for it in items if it.status == "escalated"]
    return {
        "count": len(items),
        "escalated": len(escalated),
        "top_3": [it.model_dump(mode="json") for it in prioritize(items)[:3]],
    }


def _executive_summary() -> dict[str, Any]:
    queue = get_default_queue()
    all_items = queue.list_all()
    by_priority = {p: len(queue.list_by_priority(p)) for p in ("p0", "p1", "p2", "p3")}
    return {
        "total_items": len(all_items),
        "by_priority": by_priority,
    }


def _blocked_actions() -> dict[str, Any]:
    queue = get_default_queue()
    blocked = queue.list_by_status("blocked")
    return {
        "count": len(blocked),
        "first_3": [b.model_dump(mode="json") for b in prioritize(blocked)[:3]],
    }


def _today_top_3() -> list[dict[str, Any]]:
    queue = get_default_queue()
    return [it.model_dump(mode="json") for it in prioritize(queue.list_all())[:3]]


def _count_proof_events() -> int:
    """Count real proof-event files under the proof-events dir.

    Templates / schema examples / readme placeholders are excluded so
    the count reflects genuine customer evidence only.
    """
    from auto_client_acquisition.runtime_paths import resolve_proof_events_dir

    proof_dir = resolve_proof_events_dir()
    if not proof_dir.exists():
        return 0
    return sum(
        1 for f in proof_dir.iterdir()
        if f.is_file()
        and f.suffix.lower() in (".json", ".jsonl", ".md")
        and not any(s in f.name.lower() for s in (
            ".gitkeep", "readme", "schema.example", ".example.", "template",
        ))
    )


def _revenue_truth_summary() -> dict[str, Any]:
    """RX — single revenue-truth snapshot for the founder.

    Imported lazily so the daily-command-center stays operational
    even if revenue_pipeline ships with a bug.
    """
    from auto_client_acquisition.revenue_pipeline import snapshot_revenue_truth
    from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
    from auto_client_acquisition.revenue_pipeline.revenue_truth import to_dict

    pipeline = get_default_pipeline()
    p_summary = pipeline.summary()

    truth = snapshot_revenue_truth(
        pipeline_summary=p_summary,
        proof_event_files_count=_count_proof_events(),
    )
    return to_dict(truth)


def _partner_queue() -> dict[str, Any]:
    """Partner/Affiliate OS rollup — referral pipeline + payout-safety flags.

    Imported lazily so the command center survives a partnership-OS bug.
    """
    from auto_client_acquisition.partnership_os.referral_store import (
        ReferralStatus,
        list_referrals,
    )

    referrals = list_referrals()
    by_status: dict[str, int] = {}
    for ref in referrals:
        by_status[ref.status] = by_status.get(ref.status, 0) + 1
    return {
        "total_referrals": len(referrals),
        "by_status": by_status,
        # Awaiting the doctrine gate: redeemed but invoice not yet paid.
        "awaiting_invoice_paid": by_status.get(ReferralStatus.REDEEMED.value, 0),
        "credit_issued": by_status.get(ReferralStatus.CREDIT_ISSUED.value, 0),
        "clawed_back": by_status.get(ReferralStatus.CLAWED_BACK.value, 0),
    }


def _evidence_ledger() -> dict[str, Any]:
    """Evidence Ledger rollup — count of recorded customer proof events."""
    return {
        "proof_events_recorded": _count_proof_events(),
        "note_ar": "أدلة العميل توثَّق في docs/proof-events/ عند توفّرها",
        "note_en": "Customer proof events are recorded under docs/proof-events/ when available.",
    }


def _learning_loops() -> dict[str, Any]:
    """Learning OS rollup — objection library + KB-gap candidates.

    Both loops are read-only and report empty rather than failing when
    their JSONL stores have not been populated yet.
    """
    from auto_client_acquisition.learning_loops import (
        build_kb_candidates,
        build_objection_library,
        load_classified_replies,
        load_ticket_categories,
    )

    objections = build_objection_library(load_classified_replies())
    kb_candidates = build_kb_candidates(load_ticket_categories())
    return {
        "objection_library_size": len(objections),
        "top_objections": [
            {"category": o.category, "count": o.count} for o in objections[:3]
        ],
        "kb_gap_candidates": len(kb_candidates),
        "top_kb_gaps": [
            {"category": c.category, "ticket_count": c.ticket_count}
            for c in kb_candidates[:3]
        ],
    }


def _revenue_execution_next_step() -> dict[str, str]:
    """RX — single string telling the founder the next revenue action."""
    truth = _revenue_truth_summary()
    return {
        "ar": truth["next_action_ar"],
        "en": truth["next_action_en"],
    }


@router.get("/status")
async def full_ops_status() -> dict[str, Any]:
    return {
        "service": "full_ops",
        "module": "full_ops",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {"work_queue": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "افتح /daily-command-center للحصول على القرارات اليومية",
        "next_action_en": "Open /daily-command-center for today's decisions.",
    }


@router.get("/daily-command-center")
async def daily_command_center() -> dict[str, Any]:
    """Single bilingual snapshot across all 9 OSes.

    Read-only. 200 always. Degraded sections reported in
    ``degraded_sections`` rather than 5xx.
    """
    degraded: list[str] = []
    growth = _safe("growth_queue", _growth_queue, {"count": 0, "top_3": []}, degraded)
    sales = _safe("sales_queue", _sales_queue, {"count": 0, "top_3": []}, degraded)
    support = _safe("support_queue", _support_queue, {"count": 0, "top_3": []}, degraded)
    cs = _safe("cs_queue", _cs_queue, {"count": 0, "top_3": []}, degraded)
    delivery = _safe("delivery_queue", _delivery_queue, {"count": 0, "top_3": []}, degraded)
    compliance = _safe(
        "compliance_alerts",
        _compliance_alerts,
        {"count": 0, "escalated": 0, "top_3": []},
        degraded,
    )
    executive = _safe(
        "executive_summary",
        _executive_summary,
        {"total_items": 0, "by_priority": {}},
        degraded,
    )
    blocked = _safe(
        "blocked_actions", _blocked_actions, {"count": 0, "first_3": []}, degraded
    )
    top_3 = _safe("today_top_3", _today_top_3, [], degraded)
    partner = _safe(
        "partner_queue",
        _partner_queue,
        {"total_referrals": 0, "by_status": {}, "awaiting_invoice_paid": 0,
         "credit_issued": 0, "clawed_back": 0},
        degraded,
    )
    evidence = _safe(
        "evidence_ledger",
        _evidence_ledger,
        {"proof_events_recorded": 0},
        degraded,
    )
    learning = _safe(
        "learning_loops",
        _learning_loops,
        {"objection_library_size": 0, "top_objections": [],
         "kb_gap_candidates": 0, "top_kb_gaps": []},
        degraded,
    )
    revenue_truth = _safe(
        "revenue_truth",
        _revenue_truth_summary,
        {"revenue_live": False, "v12_1_unlocked": False, "blockers": ["unavailable"]},
        degraded,
    )
    revenue_next_step = _safe(
        "revenue_execution_next_step",
        _revenue_execution_next_step,
        {"ar": "نفّذ 14_DAY_FIRST_REVENUE_PLAYBOOK", "en": "Run 14_DAY_FIRST_REVENUE_PLAYBOOK"},
        degraded,
    )

    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "مركز الأوامر اليومي — Dealix Full-Ops",
        "title_en": "Daily Command Center — Dealix Full-Ops",
        "today_top_3_decisions": top_3,
        "growth_queue": growth,
        "sales_queue": sales,
        "support_queue": support,
        "cs_queue": cs,
        "delivery_queue": delivery,
        "compliance_alerts": compliance,
        "partner_queue": partner,
        "evidence_ledger": evidence,
        "learning_loops": learning,
        "executive_summary": executive,
        "blocked_actions": blocked,
        "revenue_truth": revenue_truth,
        "revenue_execution_next_step": revenue_next_step,
        "next_best_actions": {
            "ar": "ابدأ بأعلى p0/p1 في كل قائمة، وتجاهل المحظور",
            "en": "Start with the highest p0/p1 in each queue; skip blocked items.",
        },
        "hard_gates": _HARD_GATES,
        "degraded": bool(degraded),
        "degraded_sections": degraded,
    }
