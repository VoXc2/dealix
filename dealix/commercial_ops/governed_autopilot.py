"""Governed full-ops autopilot — draft-only execution plan and status (no external send).

Industry alignment (2025–2026 RevOps): autonomous *preparation* + human approval at send/payment
(Tektonic-style governed execution; not cold-outreach bots). Dealix non-negotiables unchanged.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.daily_pack import pack_status
from dealix.commercial_ops.doctrine import doctrine_status
from dealix.commercial_ops.expansion_status import build_expansion_status
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT
from dealix.commercial_ops.value_plan import build_value_plan_snapshot

GOVERNED_POLICY_AR = (
    "تشغيل ذاتي كامل للتحضير: استهداف · مسودات · War Room · سوشال · KPI · أدلة — "
    "الإرسال والدفع والنشر بموافقة المؤسس فقط."
)

PHASES_DAILY = [
    "expand_pool_wave2",
    "dealix_daily_ops",
    "founder_commercial_day",
    "value_plan_snapshot",
    "gates_soft",
]

PHASES_EVENING = [
    "evening_evidence_reminder",
    "log_operating_day_if_empty",
]

PHASES_WEEKLY = [
    "expand_pool_wave4",
    "all_motions_pipeline",
    "weekly_scorecard",
    "weekly_content_drafts",
    "queue_approvals_dry_run",
]

GITHUB_AUTOPILOT_WORKFLOWS = [
    ".github/workflows/founder_commercial_daily.yml",
    ".github/workflows/founder_evening_evidence.yml",
    ".github/workflows/weekly-founder-content.yml",
    ".github/workflows/commercial-expand-weekly.yml",
    ".github/workflows/daily-revenue-machine.yml",
]


def build_governed_autopilot_status(*, motion_top_n: int = 5) -> dict[str, Any]:
    """Machine-readable governed autopilot snapshot for API and founder UI."""
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    expansion = build_expansion_status(abm_top_n=10)
    value_plan = build_value_plan_snapshot(motion_top_n=motion_top_n)
    first_paid = analyze_first_paid_diagnostic()
    doctrine = doctrine_status()

    workflows_ok = [
        w for w in GITHUB_AUTOPILOT_WORKFLOWS if (REPO_ROOT / w).is_file()
    ]
    pool_ready = bool(
        expansion.get("targeting", {}).get("wave2_ready")
        and expansion.get("social", {}).get("queue_ready_20w")
    )
    human_required = [
        "approve_outreach_drafts",
        "manual_send_linkedin_whatsapp_email",
        "log_real_crm_kpi",
        "close_first_paid_diagnostic",
    ]

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "date": day,
        "policy_ar": GOVERNED_POLICY_AR,
        "mode": "draft_only_governed_autopilot",
        "pool_ready": pool_ready,
        "first_paid_verdict": first_paid.get("verdict"),
        "doctrine_ok": doctrine.get("ok"),
        "expansion": expansion,
        "value_plan_summary": {
            "north_star": value_plan.get("north_star"),
            "warnings_ar": value_plan.get("warnings_ar"),
        },
        "pack_status": pack_status(day),
        "phases": {
            "daily_morning": PHASES_DAILY,
            "daily_evening": PHASES_EVENING,
            "weekly": PHASES_WEEKLY,
        },
        "human_required_ar": [
            "مراجعة /ar/ops/approvals قبل أي إرسال خارجي",
            "نسخ مسودة LinkedIn ونشر يدوياً بعد SOAEN",
            "تسجيل أدلة حقيقية في evidence CSV",
            "ملء KPI من CRM (لا أرقام مخترعة)",
        ],
        "human_required": human_required,
        "scripts": {
            "morning": "powershell -File scripts/run_founder_full_autopilot.ps1 -Mode morning",
            "evening": "powershell -File scripts/run_founder_full_autopilot.ps1 -Mode evening",
            "full": "powershell -File scripts/run_founder_full_autopilot.ps1 -Mode full",
            "max_autonomous": "py -3 scripts/run_dealix_full_autonomous_ops.py",
            "unified_day": "py -3 scripts/run_dealix_unified_founder_day.py",
            "founder_morning": "powershell -File scripts/founder_morning.ps1",
            "api_cockpit": "GET /api/v1/ops-autopilot/founder/cockpit",
            "api_full_autonomous": "GET /api/v1/ops-autopilot/founder/full-autonomous-ops",
        },
        "github_workflows": workflows_ok,
        "ops_ui": value_plan.get("ops_ui"),
        "comparison_note_ar": (
            "أفضل ممارسة 2026: أتمتة التحضير + موافقة بشرية عند الإرسال/الدفع — "
            "ليس بوت واتساب/LinkedIn بارد (متوافق مع PDPL وثقة السوق السعودي)."
        ),
    }


def write_autopilot_status_file(*, out_dir: Path | None = None) -> Path:
    d = out_dir or FOUNDER_BRIEFS_DIR
    d.mkdir(parents=True, exist_ok=True)
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    path = d / f"governed_autopilot_{day}.json"
    import json

    blob = build_governed_autopilot_status()
    path.write_text(json.dumps(blob, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
