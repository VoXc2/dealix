"""Motion A/B/C/D pipeline plans — governed, no auto-send."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.motion_a_pipeline import STATUS_NEXT_AR, _stage_for_status
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

MOTION_META: dict[str, dict[str, Any]] = {
    "A": {
        "label_ar": "وكالة (Agency wedge)",
        "gate_ar": "الأولوية — حتى أول Proof Pack مدفوع",
        "active_before_proof": True,
        "doc": "docs/commercial/operations/motion_a_agency/",
    },
    "B": {
        "label_ar": "B2B مباشر",
        "gate_ar": "بعد أول Proof من Motion A — أو inbound قوي",
        "active_before_proof": False,
        "doc": "docs/commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md",
    },
    "C": {
        "label_ar": "شريك / CRM",
        "gate_ar": "co-sell · partner_intro — عميل مشترك موثّق",
        "active_before_proof": False,
        "doc": "docs/commercial/operations/PARTNER_ONBOARDING_KIT_AR.md",
    },
    "D": {
        "label_ar": "تنفيذي / حوكمة AI",
        "gate_ar": "CEO · RevOps Diagnostic — بعد أدلة Motion A",
        "active_before_proof": False,
        "doc": "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md",
    },
}


def select_motion_targets(
    motion: str,
    *,
    top_n: int = 5,
    rows: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    m = (motion or "A").strip().upper()
    pool = rows if rows is not None else load_targets()
    filtered = [r for r in pool if (r.get("motion") or "A").strip().upper() == m]
    return select_daily_p0_targets(filtered, top_n=top_n)


def build_motion_pipeline_plan(*, motion: str, top_n: int = 5) -> dict[str, Any]:
    m = (motion or "A").strip().upper()
    meta = MOTION_META.get(m, MOTION_META["A"])
    pool = select_motion_targets(m, top_n=top_n)
    war_room = attach_outreach_drafts(build_war_room_today(pool, top_n=top_n))
    paid = analyze_first_paid_diagnostic()
    proof_closed = bool(paid.get("first_close_ready"))

    targets_out: list[dict[str, Any]] = []
    for row in (war_room.get("targets") or {}).get("items") or []:
        status = (row.get("status") or "not_contacted").strip().lower()
        targets_out.append(
            {
                "company": row.get("company"),
                "contact": row.get("contact"),
                "priority": row.get("priority"),
                "status": status,
                "stage": _stage_for_status(status, paid),
                "next_action_ar": STATUS_NEXT_AR.get(status, STATUS_NEXT_AR["not_contacted"]),
                "offer_id": row.get("offer_id"),
                "has_draft": bool(row.get("outreach_draft_ar")),
            }
        )

    active = meta.get("active_before_proof") or proof_closed
    focus_ar = [
        f"Motion {m}: {meta['label_ar']}",
        meta["gate_ar"],
        f"بوابة الدفع: {paid['verdict']}",
    ]
    if not active:
        focus_ar.insert(0, "⏸ مؤجّل — أغلق Motion A (Diagnostic + Proof) أولاً")

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "motion": m,
        "motion_active": active,
        "label_ar": meta["label_ar"],
        "first_paid": paid,
        "focus_ar": focus_ar,
        "targets": targets_out,
        "pool_size": len([r for r in load_targets() if (r.get("motion") or "A").upper() == m]),
        "doc_path": meta.get("doc"),
    }


def build_all_motions_summary(*, top_n: int = 5) -> dict[str, Any]:
    paid = analyze_first_paid_diagnostic()
    motions = {
        m: build_motion_pipeline_plan(motion=m, top_n=top_n) for m in ("A", "B", "C", "D")
    }
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "first_paid_verdict": paid.get("verdict"),
        "first_close_ready": paid.get("first_close_ready"),
        "motions": motions,
    }


def render_motion_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# Motion {plan.get('motion')} — {plan.get('label_ar')}",
        "",
        f"**توليد:** {plan.get('generated_at', '')}",
        f"**نشط:** {'نعم' if plan.get('motion_active') else 'مؤجّل'}",
        "",
        "## تركيز",
    ]
    for item in plan.get("focus_ar") or []:
        lines.append(f"- {item}")
    lines.extend(["", f"## أعلى P0 (من {plan.get('pool_size', 0)} في القائمة)", ""])
    for i, t in enumerate(plan.get("targets") or [], start=1):
        lines.append(
            f"{i}. **{t.get('company') or '—'}** · `{t.get('status')}` — {t.get('next_action_ar')}"
        )
    return "\n".join(lines)
