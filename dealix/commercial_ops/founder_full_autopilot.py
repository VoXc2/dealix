"""Governed founder full autopilot — queue, verdict, brief (no external auto-send)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from dealix.commercial_ops.evidence_csv import load_evidence_rows, real_evidence_rows
from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
from dealix.commercial_ops.founder_debrief import list_debriefs
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT

# Compared to generic "AI OS" products: Dealix keeps human approval on all outbound.
EXTERNAL_BENCHMARK_AR = (
    "أنظمة مثل Management OS / Zealos تركّز على موجز صباحي آلي؛ "
    "Dealix يطابق ذلك داخلياً مع حوكمة صارمة (لا واتساب بارد، لا LinkedIn آلي، "
    "أدلة CSV + بوابة 0–1 قبل البناء)."
)

PLS_PQL_THRESHOLD = 8  # reply+demo in rolling 30d — tune when CRM connected


def _rolling_event_counts(days: int = 30) -> dict[str, int]:
    end = datetime.now(UTC).date()
    start = end - timedelta(days=days - 1)
    counts: dict[str, int] = {}
    for row in real_evidence_rows(load_evidence_rows()):
        raw = (row.get("event_date") or "").strip()[:10]
        try:
            ed = datetime.fromisoformat(raw).date() if raw else None
        except ValueError:
            ed = None
        if ed is None or not (start <= ed <= end):
            continue
        et = (row.get("event_type") or "").strip()
        counts[et] = counts.get(et, 0) + 1
    return counts


def analyze_customer_stage_band() -> dict[str, Any]:
    """0→100 customer playbook bands from real payment events only."""
    counts = _rolling_event_counts(365)
    paid = counts.get("payment_received", 0)
    if paid >= 40:
        band = "40_plus"
        focus_ar = "مركّبات: محتوى، إحالة، تكاملات — Motions B–D عند الأدلة"
        external_ref = "repco: compound channels after 40"
    elif paid >= 10:
        band = "10_40"
        focus_ar = "كرّر القناة الفائزة + قناة ثانية تجريبية (Motion A)"
        external_ref = "repco: formalize winning channel"
    else:
        band = "1_10"
        focus_ar = "لمس يدوي، سرعة رد، debrief بعد كل اجتماع"
        external_ref = "repco: founder-led manual, no anti-human automation"
    return {
        "band": band,
        "paid_customers_real": paid,
        "focus_ar": focus_ar,
        "external_playbook_ref": external_ref,
    }


def analyze_pls_readiness() -> dict[str, Any]:
    """Product-Led Sales layer — three signals before hiring traditional reps."""
    counts = _rolling_event_counts(30)
    debriefs = list_debriefs(limit=30)
    enterprise_intent = False
    for d in debriefs:
        path = d.get("path") or ""
        p = REPO_ROOT / path if path else None
        if p and p.is_file():
            text = p.read_text(encoding="utf-8").lower()
            if any(
                k in text
                for k in ("sso", "compliance", "pdpl", "enterprise", "procurement")
            ):
                enterprise_intent = True
                break

    deal_signals = counts.get("invoice_sent", 0) + counts.get("scope_requested", 0)
    deal_size_warranted = deal_signals >= 2
    pql_proxy = counts.get("reply_received", 0) + counts.get("demo_booked", 0)
    pql_volume_ok = pql_proxy >= PLS_PQL_THRESHOLD

    signals = {
        "enterprise_intent_in_debriefs": enterprise_intent,
        "deal_size_warranted": deal_size_warranted,
        "pql_volume_proxy_ok": pql_volume_ok,
    }
    met = sum(1 for v in signals.values() if v)
    if met >= 3:
        verdict = "READY"
        hire_ar = "يمكن طبقة PLS صغيرة (2–3) — لا مبيعات enterprise تقليدية"
    elif met >= 1:
        verdict = "WATCH"
        hire_ar = "استمر founder-led؛ راقب الإشارات الثلاث"
    else:
        verdict = "NOT_YET"
        hire_ar = "لا توظيف مبيعات — ركّز على ترميز GTM"

    return {
        "verdict": verdict,
        "signals": signals,
        "signals_met": met,
        "pql_proxy_30d": pql_proxy,
        "pql_threshold": PLS_PQL_THRESHOLD,
        "recommendation_ar": hire_ar,
        "doc": "https://www.ideaplan.io/guides/product-led-sales-playbook",
    }


def build_autopilot_queue(comprehensive: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Prioritized founder actions (max 7) — scripts and UI paths only."""
    blob = comprehensive or build_comprehensive_status()
    queue: list[dict[str, Any]] = []
    prio = 0

    def add(
        *,
        title_ar: str,
        command: str,
        kind: str,
        blocking: bool = False,
    ) -> None:
        nonlocal prio
        prio += 1
        queue.append(
            {
                "priority": prio,
                "title_ar": title_ar,
                "command": command,
                "kind": kind,
                "blocking": blocking,
            }
        )

    cadence = blob.get("daily_cadence") or {}
    if not cadence.get("evidence_logged_today"):
        add(
            title_ar="سجّل حدث أدلة اليوم (مساءً أو الآن)",
            command="py -3 scripts/founder_evening_evidence.py --append --company \"...\" --event-type message_sent_manual",
            kind="evidence",
            blocking=True,
        )

    phase = blob.get("phase_0_1_gate") or {}
    for blocker in phase.get("blockers_ar") or []:
        add(
            title_ar=blocker,
            command="docs/commercial/operations/evidence_events_tracker.csv",
            kind="phase_gate",
            blocking=phase.get("no_build_until_closed"),
        )

    weekly = blob.get("weekly_one_decision") or {}
    if weekly.get("verdict") == "MISSING":
        add(
            title_ar="املأ قرار الأسبوع الواحد",
            command="py -3 scripts/founder_weekly_decision_init.py",
            kind="weekly_decision",
        )

    gtm = blob.get("gtm_codification") or {}
    if gtm.get("verdict") != "READY":
        add(
            title_ar="debrief بعد كل discovery (ترميز GTM)",
            command="py -3 scripts/founder_meeting_debrief_init.py --company \"...\"",
            kind="gtm",
        )

    pdpl = blob.get("pdpl_compliance_pass") or {}
    if pdpl.get("verdict") not in ("PASS",):
        add(
            title_ar=f"PDPL pass: {pdpl.get('done', 0)}/{pdpl.get('total', 0)} بنود",
            command="docs/commercial/operations/founder_pdpl_compliance_pass.yaml",
            kind="compliance",
        )

    add(
        title_ar="راجع War Room — أعلى 10 P0",
        command="/ar/ops/war-room",
        kind="war_room",
    )
    add(
        title_ar="انسخ مسودة LinkedIn (موافقة يدوية)",
        command="/ar/ops/marketing",
        kind="marketing",
    )

    return queue[:7]


def compute_autopilot_verdict(
    comprehensive: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blob = comprehensive or build_comprehensive_status()
    cadence = blob.get("daily_cadence") or {}
    phase = blob.get("phase_0_1_gate") or {}
    weekly = blob.get("weekly_one_decision") or {}

    blockers = 0
    if not cadence.get("evidence_logged_today"):
        blockers += 1
    if phase.get("no_build_until_closed"):
        blockers += 1
    if weekly.get("verdict") == "MISSING":
        blockers += 1

    if blockers >= 2:
        level = "RED"
        summary_ar = "توقف البناء — أغلق الأدلة والبوابة أولاً"
    elif blockers == 1:
        level = "YELLOW"
        summary_ar = "تشغيل يومي جارٍ — عنصر واحد ناقص"
    else:
        level = "GREEN"
        summary_ar = "إيقاع اليوم مكتمل — نفّذ لمسات War Room"

    return {
        "level": level,
        "blocker_count": blockers,
        "summary_ar": summary_ar,
        "policy_ar": "إرسال خارجي = مسودة + موافقة فقط",
    }


def build_autopilot_snapshot() -> dict[str, Any]:
    """Full autopilot payload for API, UI, and brief writer."""
    comprehensive = build_comprehensive_status()
    return {
        "generated_at": comprehensive.get("generated_at"),
        "benchmark_ar": EXTERNAL_BENCHMARK_AR,
        "verdict": compute_autopilot_verdict(comprehensive),
        "queue": build_autopilot_queue(comprehensive),
        "customer_stage": analyze_customer_stage_band(),
        "pls_readiness": analyze_pls_readiness(),
        "comprehensive_plan": comprehensive,
        "commands": {
            "morning": "scripts/founder_cadence.sh",
            "evening": "scripts/founder_cadence.sh --evening",
            "weekly": "scripts/founder_cadence.sh --weekly",
            "full_autopilot": "scripts/run_full_commercial_ops_autopilot.py --execute",
            "governed_doc": "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
        },
    }


def render_autopilot_brief_markdown(snapshot: dict[str, Any] | None = None) -> str:
    snap = snapshot or build_autopilot_snapshot()
    comp = snap.get("comprehensive_plan") or {}
    v = snap.get("verdict") or {}
    stage = snap.get("customer_stage") or {}
    pls = snap.get("pls_readiness") or {}
    master = comp.get("master_execution_phase") or {}

    lines = [
        "# Founder Full Autopilot Brief",
        "",
        f"**Generated:** {snap.get('generated_at')}",
        f"**Verdict:** `{v.get('level')}` — {v.get('summary_ar')}",
        "",
        "## مرحلة MASTER",
        f"- نشطة: مرحلة `{master.get('active_phase')}` — {master.get('active_label_ar')}",
        "",
        "## شريحة العملاء",
        f"- `{stage.get('band')}` — {stage.get('focus_ar')}",
        f"- مدفوعات حقيقية: `{stage.get('paid_customers_real')}`",
        "",
        "## PLS readiness",
        f"- `{pls.get('verdict')}` — {pls.get('recommendation_ar')}",
        "",
        "## طابور اليوم (حوكمة)",
    ]
    for item in snap.get("queue") or []:
        lines.append(
            f"{item.get('priority')}. **{item.get('title_ar')}** — `{item.get('command')}`"
        )
    lines.extend(["", f"_{snap.get('benchmark_ar')}_", ""])
    return "\n".join(lines)


def write_autopilot_brief(*, day: str | None = None) -> Path:
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    d = day or datetime.now(UTC).strftime("%Y-%m-%d")
    snap = build_autopilot_snapshot()
    path = FOUNDER_BRIEFS_DIR / f"autopilot_{d}.md"
    path.write_text(render_autopilot_brief_markdown(snap), encoding="utf-8")
    return path
