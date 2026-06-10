"""Full autonomous commercial ops — governed maximum (drafts + approvals, no cold send)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.expansion_status import build_expansion_status
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT

# Synthesized from founder-led RevOps cadence literature (Gong, Weflow, PMGuru, 2024–2026).
# Dealix deliberately exceeds on governance; does not compete on unsupervised outbound volume.
BENCHMARK_COMPARISON_AR: list[dict[str, str]] = [
    {
        "dimension": "إيقاع يومي",
        "industry_best": "مراجعة pipeline يومية + استثناءات فقط (5–15 دقيقة أرقام)",
        "dealix": "موجز + War Room 10 P0 + مسودات لمسة + SOAEN (≈25 دقيقة نظام + موافقات)",
        "verdict": "مكافئ/أقوى في التركيز",
    },
    {
        "dimension": "اجتماع إيراد أسبوعي",
        "industry_best": "30 دقيقة: 4 KPIs + 3 مخاطر + قرارات موثّقة",
        "dealix": "weekly_scorecard من evidence CSV — لا أرقام CRM مخترعة",
        "verdict": "مكافئ مع امتثال أعلى",
    },
    {
        "dimension": "أتمتة الإرسال",
        "industry_best": "أدوات sequences (خطر امتثال/سمعة)",
        "dealix": "draft_only — مسودة Gmail/LinkedIn + موافقة + إرسال يدوي",
        "verdict": "أفضل لسوق سعودي B2B وPDPL",
    },
    {
        "dimension": "حجم الاستهداف",
        "industry_best": "قوائم كبيرة + تسلسلات",
        "dealix": "250 حساب warm + تدوير P0 + ABM wave gates",
        "verdict": "أعمق استراتيجياً · أقل حجم بارد",
    },
    {
        "dimension": "محتوى/تسويق",
        "industry_best": "تقويم محتوى + إعلانات بعد product-market fit",
        "dealix": "28 أسبوع مسودة LinkedIn + AEO + قمع /ar",
        "verdict": "أقوى في المحتوى المحكوم مسبقاً",
    },
    {
        "dimension": "إغلاق الإيراد",
        "industry_best": "CRM كمصدر حقيقة",
        "dealix": "evidence CSV + first_paid DoD + Diagnostic قبل Growth",
        "verdict": "أقوى في إثبات الدفع/Proof",
    },
    {
        "dimension": "Revenue OS / طوابير يومية",
        "industry_best": "9 smart queues + KPIs (RevOS-style dashboards)",
        "dealix": "cockpit + strongest plan + War Room P0 + HITL approvals",
        "verdict": "مكافئ مع حوكمة أعلى — لا إرسال ذاتي كامل",
    },
]

HUMAN_ONLY_AR: list[str] = [
    "الموافقة على المسودات وإرسالها يدوياً (واتساب/لينكدإن/بريد warm فقط).",
    "حجز وإجراء اجتماعات Discovery وإغلاق Diagnostic.",
    "ملء KPI من CRM الحقيقي (لا اختراع في التقارير).",
    "تفعيل Moyasar/HubSpot/Railway عند Paid Launch.",
]


def _last_run_path() -> Path:
    return FOUNDER_BRIEFS_DIR / "autonomous_ops_last_run.json"


def load_last_autonomous_run() -> dict[str, Any] | None:
    p = _last_run_path()
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def save_last_autonomous_run(payload: dict[str, Any]) -> Path:
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    p = _last_run_path()
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    day = payload.get("date") or datetime.now(UTC).strftime("%Y-%m-%d")
    md = FOUNDER_BRIEFS_DIR / f"autonomous_ops_{day}.md"
    md.write_text(render_autonomous_ops_markdown(payload), encoding="utf-8")
    payload["written_paths"] = {
        "json": str(p.relative_to(REPO_ROOT)).replace("\\", "/"),
        "markdown": str(md.relative_to(REPO_ROOT)).replace("\\", "/"),
    }
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def build_autonomous_ops_status(*, abm_top_n: int = 10) -> dict[str, Any]:
    """Read-only snapshot for API/UI — no subprocess execution."""
    from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot

    expansion = build_expansion_status(abm_top_n=abm_top_n)
    first_paid = analyze_first_paid_diagnostic()
    autopilot = build_autopilot_snapshot()
    tech_ready = bool(
        expansion.get("targeting", {}).get("wave4_prep_ready")
        and expansion.get("social", {}).get("queue_ready_28w")
    )
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "mode": "governed_autonomous_max",
        "policy_ar": (
            "أقصى أتمتة تشغيلية: تجهيز يومي كامل — الإرسال والإغلاق بقرار المؤسس فقط."
        ),
        "technical_expansion_ready": tech_ready,
        "expansion": expansion,
        "first_paid": first_paid,
        "first_paid_verdict": first_paid.get("verdict"),
        "benchmark_comparison_ar": BENCHMARK_COMPARISON_AR,
        "human_only_ar": HUMAN_ONLY_AR,
        "governed_autopilot": {
            "verdict": autopilot.get("verdict"),
            "queue": autopilot.get("queue"),
            "customer_stage": autopilot.get("customer_stage"),
            "pls_readiness": autopilot.get("pls_readiness"),
            "benchmark_ar": autopilot.get("benchmark_ar"),
        },
        "comparison_note_ar": (
            "أقصى أتمتة داخل الريبو مع حوكمة أشد من أدوات الإرسال التلقائي الكامل — "
            "مناسب لـ founder-led B2B السعودي."
        ),
        "last_run": load_last_autonomous_run(),
        "canonical_scripts": {
            "complete_day": "py -3 scripts/run_dealix_complete_autonomous_day.py",
            "unified_day": "py -3 scripts/run_dealix_unified_founder_day.py",
            "full_autonomous": "py -3 scripts/run_dealix_full_autonomous_ops.py",
            "complete_day_ps1": "powershell -File scripts/run_dealix_complete_autonomous_day.ps1",
            "full_local": "powershell -File scripts/run_dealix_full_autonomous_ops.ps1",
            "morning": "powershell -File scripts/founder_morning.ps1",
            "evening": "powershell -File scripts/founder_evening.ps1 -Append -Company '...'",
            "ci_daily": ".github/workflows/founder_commercial_daily.yml",
            "ci_revenue_machine": ".github/workflows/daily-revenue-machine.yml",
            "ci_weekly_expand": ".github/workflows/founder_autonomous_ops_weekly.yml",
        },
        "ops_ui": {
            "founder": "/ar/ops/founder",
            "war_room": "/ar/ops/war-room",
            "approvals": "/ar/ops/approvals",
            "expansion_api": "/api/v1/ops-autopilot/founder/autonomous-ops/status",
        },
    }


def render_autonomous_ops_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Autonomous Ops Report · {payload.get('date', '')}",
        "",
        f"_{payload.get('policy_ar', '')}_",
        "",
        f"**Verdict:** `{payload.get('verdict', 'UNKNOWN')}`",
        "",
        "## مقارنة مع أفضل الممارسات (RevOps)",
        "",
    ]
    for row in payload.get("benchmark_comparison_ar") or BENCHMARK_COMPARISON_AR:
        lines.append(
            f"- **{row['dimension']}** — صناعة: {row['industry_best']} · Dealix: {row['dealix']} · "
            f"_{row['verdict']}_"
        )
    lines.extend(["", "## يدوي فقط (لا يُؤتمت)", ""])
    for h in payload.get("human_only_ar") or HUMAN_ONLY_AR:
        lines.append(f"- {h}")
    phases = payload.get("phases") or []
    if phases:
        lines.extend(["", "## مراحل التشغيل", ""])
        for ph in phases:
            lines.append(
                f"- `{ph.get('id')}` · {ph.get('label')} · exit={ph.get('exit_code')} · {ph.get('verdict')}"
            )
    lines.append("")
    lines.append(f"_Generated: {payload.get('generated_at')}_")
    return "\n".join(lines)
