"""GTM stack — ABM wave 1, dual-track recommendation, TTV, proof stack."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from functools import lru_cache
from typing import Any

import yaml

from dealix.commercial_ops.evidence_csv import load_evidence_rows, real_evidence_rows
from dealix.commercial_ops.paths import (
    GTM_ABM_WAVE1_YAML,
    REPO_ROOT,
)
from dealix.commercial_ops.targeting_csv import load_targets

FORBIDDEN_CHANNELS = frozenset({"cold_whatsapp", "linkedin_auto_send", "scraping"})
WARM_SEGMENTS = frozenset(
    {
        "agency_wedge",
        "direct_b2b",
        "crm_partner",
        "agency_partner",
        "marketing_agency",
        "consulting_firm",
    }
)
REPLACE_PREFIX = "REPLACE:"


@lru_cache(maxsize=1)
def load_gtm_abm_config() -> dict[str, Any]:
    if not GTM_ABM_WAVE1_YAML.is_file():
        return {}
    data = yaml.safe_load(GTM_ABM_WAVE1_YAML.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def is_placeholder_target(row: dict[str, str]) -> bool:
    company = (row.get("company") or "").strip()
    if not company or company.startswith(REPLACE_PREFIX):
        return True
    notes = (row.get("notes") or "").lower()
    return bool("مثال تدريبي" in notes or "training" in notes)


def score_abm_wave1_row(row: dict[str, str]) -> dict[str, Any]:
    """Score 0–100 for wave-1 fit (warm ABM)."""
    if is_placeholder_target(row):
        return {"score": 0, "eligible": False, "reasons": ["placeholder"]}

    cfg = load_gtm_abm_config()
    weights = cfg.get("scoring_weights") or {}
    w_warm = float(weights.get("warm_relationship", 40))
    w_pain = float(weights.get("pain_fit_agency_wedge", 30))
    w_signal = float(weights.get("buying_signal_recent", 20))
    w_channel = float(weights.get("channel_allowed", 10))

    reasons: list[str] = []
    score = 0.0

    notes = (row.get("notes") or "").lower()
    if "warm" in notes or "inbound" in notes or "partner" in notes:
        score += w_warm
        reasons.append("warm_signal")
    else:
        reasons.append("missing_warm_note")

    segment = (row.get("segment") or "").strip()
    if segment in WARM_SEGMENTS:
        score += w_pain
        reasons.append("segment_fit")
    else:
        reasons.append("segment_weak")

    pain = (row.get("pain_hypothesis") or "").strip()
    if len(pain) >= 12:
        score += w_signal
        reasons.append("pain_hypothesis")

    channel = (row.get("channel") or "").strip()
    allowed = set(cfg.get("channels_allowed") or [])
    if channel in allowed and channel not in FORBIDDEN_CHANNELS:
        score += w_channel
        reasons.append("channel_ok")
    elif channel in FORBIDDEN_CHANNELS:
        reasons.append("channel_forbidden")

    status = (row.get("status") or "").strip()
    if status == "closed_lost":
        return {"score": 0, "eligible": False, "reasons": ["closed_lost"]}

    next_action = (row.get("next_action") or "").strip()
    (row.get("next_action_date") or "").strip()
    if not next_action:
        reasons.append("no_next_action")

    eligible = (
        score >= 50
        and "channel_forbidden" not in reasons
        and bool(next_action)
    )
    return {
        "score": round(score),
        "eligible": eligible,
        "reasons": reasons,
        "priority": (row.get("priority") or "medium").strip().lower(),
    }


def build_abm_wave1_status(*, top_n: int = 15) -> dict[str, Any]:
    cfg = load_gtm_abm_config()
    acct = cfg.get("account_count") or {}
    rows = load_targets()
    active = [r for r in rows if not is_placeholder_target(r)]
    scored: list[dict[str, Any]] = []
    for r in active:
        s = score_abm_wave1_row(r)
        if s["eligible"] or s["score"] >= 40:
            scored.append({**r, "abm_score": s["score"], "abm_eligible": s["eligible"], "abm_reasons": s["reasons"]})
    scored.sort(key=lambda x: (x.get("abm_score", 0), x.get("priority") == "high"), reverse=True)

    high_priority = sum(1 for r in active if (r.get("priority") or "").lower() == "high")
    eligible_count = sum(1 for r in active if score_abm_wave1_row(r)["eligible"])
    min_rows = int(acct.get("min") or 30)
    target_rows = int(acct.get("target") or 50)

    return {
        "wave_id": cfg.get("wave_id", "abm_wave_1"),
        "pool_rows": len(rows),
        "active_rows": len(active),
        "eligible_wave1": eligible_count,
        "high_priority_rows": high_priority,
        "min_required": min_rows,
        "target_required": target_rows,
        "wave1_ready": len(active) >= min_rows and eligible_count >= min_rows,
        "top_targets": scored[:top_n],
        "config_path": str(GTM_ABM_WAVE1_YAML.relative_to(REPO_ROOT)).replace("\\", "/"),
        "doc_path": "docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md",
    }


def recommend_dual_track() -> dict[str, Any]:
    """Path A (promote) vs B (ops) — mirrors GTM_DUAL_TRACK doc."""
    rows = load_targets()
    active = [r for r in rows if not is_placeholder_target(r)]
    high_no_action = [
        r
        for r in active
        if (r.get("priority") or "").lower() == "high"
        and (r.get("status") or "") in {"not_contacted", "message_drafted"}
        and not (r.get("next_action_date") or "").strip()
    ]
    evidence = real_evidence_rows()
    discovery_week = sum(
        1
        for r in evidence
        if (r.get("event_type") or "") in {"demo_booked", "discovery_completed"}
    )

    if high_no_action:
        track = "A"
        reason_ar = (
            f"مسار A (ترويج): {len(high_no_action)} هدف high بلا تاريخ متابعة — "
            "War Room قبل بناء المنتج."
        )
    elif discovery_week >= 3:
        track = "A"
        reason_ar = "مسار A (إغلاق): لديك زخم discovery — ركّز على scope ودفع."
    else:
        track = "B"
        reason_ar = (
            "مسار B (ops): عبّئ موجة ABM 1 أو شغّل verify — "
            "ثم ارجع للمسار A."
        )

    return {
        "recommended_track": track,
        "reason_ar": reason_ar,
        "high_priority_stale": len(high_no_action),
        "discovery_signals_week": discovery_week,
        "doc_path": "docs/commercial/operations/GTM_DUAL_TRACK_CLARIFICATION_AR.md",
    }


def _company_event_dates(rows: list[dict[str, str]]) -> dict[str, dict[str, date]]:
    by_co: dict[str, dict[str, date]] = {}
    for row in rows:
        company = (row.get("company") or "").strip()
        if not company:
            continue
        et = (row.get("event_type") or "").strip()
        raw = (row.get("event_date") or "").strip()[:10]
        try:
            ed = date.fromisoformat(raw)
        except ValueError:
            continue
        by_co.setdefault(company, {})
        prev = by_co[company].get(et)
        if prev is None or ed < prev:
            by_co[company][et] = ed
    return by_co


def compute_ttv_metrics(*, lookback_days: int = 90) -> dict[str, Any]:
    rows = real_evidence_rows()
    cutoff = datetime.now(UTC).date() - timedelta(days=lookback_days)
    by_co = _company_event_dates(
        [
            r
            for r in rows
            if (r.get("event_date") or "")[:10]
            and date.fromisoformat((r.get("event_date") or "")[:10]) >= cutoff
        ]
    )

    discovery_days: list[int] = []
    demo_days: list[int] = []
    paid_days: list[int] = []

    for events in by_co.values():
        lead = events.get("message_sent_manual") or events.get("reply_received")
        disc = events.get("discovery_completed") or events.get("demo_booked")
        demo = events.get("demo_held") or events.get("demo_booked")
        paid = events.get("payment_received")
        if lead and disc:
            discovery_days.append((disc - lead).days)
        if disc and demo:
            demo_days.append((demo - disc).days)
        if demo and paid:
            paid_days.append((paid - demo).days)

    def _avg(vals: list[int]) -> float | None:
        return round(sum(vals) / len(vals), 1) if vals else None

    return {
        "lookback_days": lookback_days,
        "companies_with_events": len(by_co),
        "ttv_discovery_days_avg": _avg(discovery_days),
        "ttv_demo_days_avg": _avg(demo_days),
        "ttv_paid_days_avg": _avg(paid_days),
        "samples_discovery": len(discovery_days),
        "targets_ar": {
            "ttv_discovery_max_days": 14,
            "ttv_demo_max_days": 7,
        },
        "doc_path": "docs/commercial/operations/FOUNDER_SALES_LOOP_AR.md",
    }


def proof_stack_for_status(war_room_status: str) -> dict[str, Any]:
    """Minimum proof tier before advancing stage."""
    st = (war_room_status or "not_contacted").strip().lower()
    tiers = {
        "not_contacted": 2,
        "message_drafted": 2,
        "approved_to_send": 2,
        "sent_manual": 2,
        "replied": 3,
        "meeting_booked": 3,
        "discovery_completed": 3,
        "demo_held": 4,
        "scope_requested": 4,
        "invoice_sent": 4,
        "paid": 5,
    }
    tier = tiers.get(st, 2)
    assets = {
        1: [
            "docs/commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md",
            "docs/commercial/INFRA_HOSTING_REGION_RUBRIC_AR.md",
        ],
        2: ["docs/commercial/POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md"],
        3: [
            "docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md",
            "/ar/proof-pack",
            "/ar/risk-score",
        ],
        4: [
            "docs/commercial/operations/motion_a_agency/SCOPE_AGENCY_AUDIT_AR.md",
            "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
        ],
        5: ["docs/commercial/samples/LEAD_INTELLIGENCE_SPRINT_SAMPLE_REPORT_AR.md"],
    }
    required = []
    for t in range(1, tier + 1):
        required.extend(assets.get(t, []))
    return {
        "war_room_status": st,
        "minimum_tier": tier,
        "required_assets": required,
        "doc_path": "docs/commercial/operations/PROOF_STACK_ORDER_AR.md",
    }


def build_gtm_stack_snapshot(*, abm_top_n: int = 10) -> dict[str, Any]:
    dual = recommend_dual_track()
    abm = build_abm_wave1_status(top_n=abm_top_n)
    ttv = compute_ttv_metrics()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "playbook_path": "docs/commercial/GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md",
        "dual_track": dual,
        "abm_wave1": abm,
        "ttv": ttv,
        "focus_ar": _build_focus_ar(dual, abm, ttv),
        "docs": {
            "dual_track": dual["doc_path"],
            "abm_wave1": abm["doc_path"],
            "founder_loop": ttv["doc_path"],
            "proof_stack": "docs/commercial/operations/PROOF_STACK_ORDER_AR.md",
            "channels": "docs/commercial/operations/GTM_CHANNELS_PLAYBOOK_AR.md",
            "objections": "docs/commercial/operations/GTM_OBJECTION_MATRIX_AR.md",
        },
    }


def _build_focus_ar(
    dual: dict[str, Any],
    abm: dict[str, Any],
    ttv: dict[str, Any],
) -> list[str]:
    out: list[str] = [dual["reason_ar"]]
    if not abm.get("wave1_ready"):
        out.append(
            f"موجة ABM 1: {abm.get('active_rows', 0)}/{abm.get('min_required', 30)} "
            f"صف فعّال — عبّئ warm في agency_accounts_seed.csv."
        )
    disc_avg = ttv.get("ttv_discovery_days_avg")
    if disc_avg is not None and disc_avg > 14:
        out.append(f"TTV discovery متوسط {disc_avg} يوم — ركّز high فقط.")
    return out[:4]
