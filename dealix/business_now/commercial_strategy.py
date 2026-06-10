"""Unified commercial strategy snapshot — deterministic, no invented CRM numbers."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.business import (
    channel_strategy,
    dealix_differentiators,
    estimate_cac_payback,
    estimate_gross_margin,
    first_10_customers_plan,
    first_100_customers_plan,
    founder_led_sales_script,
    get_pricing_tiers,
    north_star_metrics,
    partner_strategy,
    positioning_statement,
)
from auto_client_acquisition.business.pricing_strategy import recommend_plan
from auto_client_acquisition.business.verticals import get_vertical_playbooks, recommend_vertical
from auto_client_acquisition.value_capture_os import (
    ClientQualityDimensions,
    ProofCommercialSignal,
    RevenueQualityDimensions,
    client_quality_band,
    client_quality_score,
    revenue_quality_band,
    revenue_quality_score,
    upsell_from_proof_signal,
)
from auto_client_acquisition.value_capture_os.expansion_map import (
    TRACK_AI_QUICK_WIN,
    TRACK_COMPANY_BRAIN,
    TRACK_GOVERNANCE,
    TRACK_REVENUE_INTELLIGENCE,
)
from dealix.business_now.integration_truth import build_integration_truth_summary

_REPO = Path(__file__).resolve().parents[2]
_PLAYBOOK_YAML = _REPO / "dealix" / "transformation" / "commercial_offer_playbook.yaml"
_FOCUS_OVERRIDE = _REPO / "dealix" / "transformation" / "commercial_focus_override.yaml"

_PROOF_SIGNAL_LABELS_AR: dict[str, str] = {
    "data_issues": "مشاكل بيانات في التقرير",
    "follow_up_gaps": "فجوات متابعة ليدز",
    "knowledge_gaps": "فجوات معرفة / Company Brain",
    "policy_risks": "مخاطر سياسة أو امتثال",
    "manual_reporting": "تقارير يدوية متكررة",
}

_PRIORITY_VERTICALS = ("clinics", "real_estate", "logistics", "training", "agencies", "b2b_saas")

_GUARDRAILS_AR = [
    "لا واتساب بارد ولا LinkedIn تلقائي",
    "لا إرسال خارجي بدون موافقة صريحة",
    "شغّل anti-waste قبل أي حملة أو رسالة خارجية",
    "لا upsell بدون Proof Pack أو دليل L3+",
    "لا أرقام CRM في الأتمتة — عبّئ kpi_founder_commercial_import.yaml يدوياً",
]


def _load_playbook_yaml() -> dict[str, Any]:
    if not _PLAYBOOK_YAML.exists():
        return {}
    return yaml.safe_load(_PLAYBOOK_YAML.read_text(encoding="utf-8")) or {}


def _offers_from_commercial_map() -> list[dict[str, Any]]:
    from api.routers.commercial_map import _build_payload

    playbook = _load_playbook_yaml().get("offers") or {}
    out: list[dict[str, Any]] = []
    for o in _build_payload().get("offers") or []:
        sid = o.get("service_id")
        w = o.get("wiring") or {}
        pb = playbook.get(sid) or {}
        out.append(
            {
                "service_id": sid,
                "name_ar": o.get("name_ar"),
                "name_en": o.get("name_en"),
                "price_sar": o.get("price_sar"),
                "price_unit": o.get("price_unit"),
                "next_offer": w.get("next_offer"),
                "success_metric_ar": pb.get("success_metric_ar", o.get("kpi_commitment_ar")),
                "first_touch_ar": pb.get("first_touch_ar"),
                "intake_endpoint": w.get("intake_endpoint") or w.get("lead_capture_endpoint"),
                "founder_surface": w.get("founder_surface"),
            }
        )
    return out


def _value_ladder() -> list[dict[str, Any]]:
    raw = _load_playbook_yaml().get("value_ladder") or []
    return list(raw)


def _upsell_matrix() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for sig in ProofCommercialSignal:
        offer = upsell_from_proof_signal(sig.value)
        rows.append(
            {
                "proof_signal": sig.value,
                "recommended_offer": offer or "—",
            }
        )
    return rows


def _verticals_priority() -> list[dict[str, Any]]:
    playbooks = get_vertical_playbooks().get("verticals") or {}
    out: list[dict[str, Any]] = []
    for key in _PRIORITY_VERTICALS:
        pb = playbooks.get(key)
        if not isinstance(pb, dict):
            continue
        out.append(
            {
                "key": key,
                "pain_ar": pb.get("pain_ar"),
                "message_angle_ar": pb.get("message_angle_ar"),
                "buyer": pb.get("buyer"),
            }
        )
    return out


def _north_star_table() -> list[dict[str, str]]:
    ns = north_star_metrics()
    rows: list[dict[str, str]] = [
        {
            "axis": "primary",
            "metric": str(ns.get("primary", "")),
            "mvp_target": "قياس أسبوعي — لا ادّعاء إيراد بدون دفع",
        },
        {
            "axis": "secondary",
            "metric": str(ns.get("secondary", "")),
            "mvp_target": "بعد موافقة على المسودة",
        },
        {
            "axis": "guardrail",
            "metric": str(ns.get("guardrail", "")),
            "mvp_target": "صفر تجاوزات عالية الخطورة",
        },
    ]
    return rows


def _ops_client_pack() -> dict[str, Any]:
    """Founder sales motion pack — repo paths (deck + runbook)."""
    return {
        "runbook_doc": "docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md",
        "sales_kit_deck": "docs/commercial/ops_client_pack/dealix_ops_sales_kit_ar.pptx",
        "ui_demo_path": "/business-now#strategy",
        "primary_offer_pitch_ar": "Governed Revenue Ops Diagnostic",
        "suggested_price_sar_range": [4999, 9999],
        "suggested_price_premium_sar": 15000,
        "conversation_opener_en": (
            "Dealix helps teams turn AI experimentation and revenue operations into "
            "governed, measurable workflows — with source clarity, approval boundaries, "
            "evidence trails, and proof of value."
        ),
        "discovery_question_en": (
            "Where do AI experiments or revenue workflows currently create "
            "ambiguity, risk, or wasted follow-up?"
        ),
        "demo_steps": [
            "افتح /ar/business-now#strategy",
            "شغّل simulate للقطاع/المدينة/الميزانية",
            "اعرض focus الحالي بصدق",
            "GTM أول 10 + Sales Script + Proof demo",
            "اختم بـ Diagnostic Scope",
        ],
        "closing_line_ar": (
            "إذا كان هذا يعكس مشكلة عندكم، التشخيص المدفوع يحولها إلى workflow محكوم "
            "وقابل للقياس خلال أسبوعين."
        ),
        "deliverables_ar": [
            "Revenue Workflow Map",
            "Source Quality Review",
            "Pipeline Risk Map",
            "Follow-up Gap Analysis",
            "Decision Passport",
            "Proof-of-Value Opportunities",
            "Recommended Sprint / Retainer",
        ],
    }


def _weekly_motions() -> list[dict[str, str]]:
    return [
        {"day": "sun", "action_ar": "راجع لقطة Business NOW + KPIs التجارية المعلّقة", "href": "/business-now"},
        {"day": "mon", "action_ar": "حدّث قائمة دافئة (~30) — مسودات فقط", "href": "/pipeline"},
        {"day": "tue", "action_ar": "POST /api/v1/leads لاختبار مسار intake", "href": "/pipeline"},
        {"day": "wed", "action_ar": "anti-waste قبل أي رسالة خارجية", "href": "/trust-check"},
        {"day": "thu", "action_ar": "راجع موافقات اليوم — لا إرسال بدون جواز", "href": "/approvals"},
        {"day": "fri", "action_ar": "Proof / تقرير أسبوعي للعميل النشط", "href": "/trust-check"},
        {"day": "sat", "action_ar": "شغّل run_business_now.sh + حدّث cache", "href": "/business-now"},
    ]


def _load_focus_override() -> dict[str, Any]:
    if not _FOCUS_OVERRIDE.exists():
        return {}
    data = yaml.safe_load(_FOCUS_OVERRIDE.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _apply_focus_override(focus: dict[str, Any]) -> dict[str, Any]:
    ov = _load_focus_override()
    if focus.get("stage") in ("kpi_hygiene", "platform_repair"):
        return focus
    out = dict(focus)
    if ov.get("primary_offer_id"):
        out["primary_offer_id"] = ov["primary_offer_id"]
        out["override_applied"] = True
        out["rationale_ar"] = (
            str(out.get("rationale_ar", ""))
            + " — تعديل: commercial_focus_override.yaml"
        )
    if ov.get("preferred_vertical"):
        out["preferred_vertical"] = ov["preferred_vertical"]
    return out


def _gtm_first_10_summary() -> dict[str, Any]:
    plan = first_10_customers_plan()
    return {
        "who": plan.get("who") or [],
        "how_to_find": plan.get("how_to_find") or [],
        "qualification": plan.get("qualification") or [],
        "success_criteria": plan.get("success_criteria") or [],
        "pilot_offer_ar": plan.get("pilot_offer_ar"),
    }


def _recommended_vertical_default() -> dict[str, Any]:
    verts = _verticals_priority()
    if not verts:
        return {}
    v = verts[0]
    return {"key": v.get("key"), "pain_ar": v.get("pain_ar"), "message_angle_ar": v.get("message_angle_ar")}


def _quality_scores_demo() -> dict[str, Any]:
    rev_dims = RevenueQualityDimensions(
        margin=72,
        repeatability=65,
        retainer_potential=70,
        proof_strength=68,
        governance_safety=85,
        productization_signal=60,
    )
    cli_dims = ClientQualityDimensions(
        clear_pain=75,
        data_readiness=55,
        decision_owner=70,
        willingness_to_pay=65,
        governance_alignment=80,
        retainer_potential=60,
        strategic_logo_or_sector=50,
    )
    rev_score = revenue_quality_score(rev_dims)
    cli_score = client_quality_score(cli_dims)
    return {
        "is_estimate": True,
        "notes_ar": "درجات توضيحية ثابتة — عبّئ من تقييمك الفعلي للعميل",
        "revenue_quality": {
            "score": rev_score,
            "band": revenue_quality_band(rev_score),
        },
        "client_quality": {
            "score": cli_score,
            "band": client_quality_band(cli_score),
        },
    }


def _next_best_actions(focus: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    stage = str(focus.get("stage") or "")

    if stage == "kpi_hygiene":
        actions.append(
            {
                "priority": 1,
                "action_ar": "صدّر KPIs من CRM → kpi_founder_commercial_import.yaml",
                "href": "/business-now#strategy",
                "api_hint": "scripts/apply_kpi_founder_commercial.py",
            }
        )
    elif stage == "platform_repair":
        actions.append(
            {
                "priority": 1,
                "action_ar": "أصلح التحول التقني قبل GTM",
                "href": "/cloud",
                "api_hint": "scripts/verify_global_ai_transformation.py",
            }
        )
    elif stage == "pilot_execution":
        actions.append(
            {
                "priority": 1,
                "action_ar": "نفّذ بايلوت Sprint 499 مع عميل واحد",
                "href": "/clients",
                "api_hint": "docs/transformation/enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md",
            }
        )
    else:
        actions.append(
            {
                "priority": 1,
                "action_ar": "قدّم تشخيصاً مجانياً لعميل دافئ واحد",
                "href": "/pipeline",
                "api_hint": "POST /api/v1/leads",
            }
        )

    actions.extend(
        [
            {
                "priority": 2,
                "action_ar": "محاكاة قطاع + خطة (simulate)",
                "href": "/business-now#strategy",
                "api_hint": "POST /api/v1/business-now/commercial-strategy/simulate",
            },
            {
                "priority": 3,
                "action_ar": "راجع GTM أول 10 عملاء",
                "href": "/business-now#strategy",
                "api_hint": "GET /api/v1/business/gtm/first-10",
            },
            {
                "priority": 4,
                "action_ar": "anti-waste قبل حملة",
                "href": "/trust-check",
                "api_hint": "POST /api/v1/revenue-os/anti-waste/check",
            },
        ]
    )
    actions.sort(key=lambda x: x["priority"])
    return actions[:5]


def resolve_focus(
    *,
    commercial_kpi_pending: int = 0,
    transformation_verdict: str = "SKIP",
    all_pilots_template_ready: bool = False,
) -> dict[str, Any]:
    if commercial_kpi_pending > 0:
        return {
            "primary_offer_id": None,
            "stage": "kpi_hygiene",
            "rationale_ar": (
                f"{commercial_kpi_pending} KPIs تجارية معلّقة — عبّئ "
                "kpi_founder_commercial_import.yaml قبل توسع GTM"
            ),
        }
    if transformation_verdict not in ("PASS",):
        return {
            "primary_offer_id": None,
            "stage": "platform_repair",
            "rationale_ar": "أصلح verify_global_ai_transformation قبل أي توسع مبيعات",
        }
    if all_pilots_template_ready:
        return {
            "primary_offer_id": "revenue_proof_sprint_499",
            "stage": "pilot_execution",
            "rationale_ar": "بايلوتات جاهزة للقالب — ركّز على Sprint 499 + PILOT_EXECUTION_RUNBOOK",
        }
    return {
        "primary_offer_id": "free_mini_diagnostic",
        "secondary_offer_id": "revenue_proof_sprint_499",
        "stage": "founder_led_entry",
        "rationale_ar": "سلم الدخول: تشخيص مجاني ثم Sprint 499 — قائمة دافئة فقط",
    }


def build_commercial_strategy_simulate(
    *,
    industry: str = "clinics",
    city: str = "Riyadh",
    company_size: str = "sme",
    monthly_budget_sar: float = 2500.0,
    goal: str = "pipeline",
) -> dict[str, Any]:
    """Founder-facing bundle — deterministic, not CRM-backed."""
    vertical = recommend_vertical(industry=industry, city=city, goal=goal)
    plan = recommend_plan(
        company_size=company_size,
        monthly_budget_sar=monthly_budget_sar,
        goal=goal,
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "inputs": {
            "industry": industry,
            "city": city,
            "company_size": company_size,
            "monthly_budget_sar": monthly_budget_sar,
            "goal": goal,
        },
        "vertical": vertical,
        "plan_recommendation": plan,
        "positioning": {
            "founder": positioning_statement("founder"),
            "sme": positioning_statement("sme"),
        },
        "is_estimate": True,
        "notes_ar": "محاكاة حتمية من منطق business module — ليست أرقام CRM",
    }


def proof_signal_label_ar(signal: str) -> str:
    return _PROOF_SIGNAL_LABELS_AR.get(signal, signal)


def _business_context() -> tuple[int, str, bool]:
    from dealix.business_now.cache import apply_cache_to_platform
    from dealix.business_now.snapshot_builder import (
        _commercial_registry_status,
        _pilot_sprints,
    )

    pending = _commercial_registry_status()["pending_count"]
    platform = apply_cache_to_platform({"transformation_verdict": "SKIP"})
    verdict = str(platform.get("transformation_verdict") or "SKIP")
    sprints = _pilot_sprints()
    all_tr = bool(sprints) and all(s.get("status") == "template_ready" for s in sprints)
    return pending, verdict, all_tr


def build_commercial_strategy_snapshot(
    *,
    commercial_kpi_pending: int | None = None,
    transformation_verdict: str | None = None,
    all_pilots_template_ready: bool | None = None,
) -> dict[str, Any]:
    """Full commercial strategy JSON for founder decisions."""
    if (
        commercial_kpi_pending is None
        or transformation_verdict is None
        or all_pilots_template_ready is None
    ):
        ctx_pending, ctx_verdict, ctx_pilots = _business_context()
        if commercial_kpi_pending is None:
            commercial_kpi_pending = ctx_pending
        if transformation_verdict is None:
            transformation_verdict = ctx_verdict
        if all_pilots_template_ready is None:
            all_pilots_template_ready = ctx_pilots

    focus = _apply_focus_override(
        resolve_focus(
            commercial_kpi_pending=commercial_kpi_pending,
            transformation_verdict=transformation_verdict or "SKIP",
            all_pilots_template_ready=bool(all_pilots_template_ready),
        )
    )

    upsell = _upsell_matrix()
    for row in upsell:
        row["label_ar"] = proof_signal_label_ar(str(row.get("proof_signal", "")))

    tiers = get_pricing_tiers()
    gross = estimate_gross_margin()
    cac = estimate_cac_payback()

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "focus": focus,
        "next_best_actions": _next_best_actions(focus),
        "gtm_first_10_summary": _gtm_first_10_summary(),
        "sales_playbook": founder_led_sales_script(),
        "channels_partners": {
            "channels": channel_strategy(),
            "partners": partner_strategy(),
        },
        "recommended_vertical_default": _recommended_vertical_default(),
        "quality_scores_demo": _quality_scores_demo(),
        "value_ladder": _value_ladder(),
        "offers_playbook": _offers_from_commercial_map(),
        "gtm_motions": {
            "first_10": first_10_customers_plan(),
            "first_100": first_100_customers_plan(),
            "channels": channel_strategy(),
            "partners": partner_strategy(),
            "founder_script": founder_led_sales_script(),
        },
        "positioning": {
            "differentiators": dealix_differentiators(),
            "segments": {
                "founder": positioning_statement("founder"),
                "sme": positioning_statement("sme"),
                "enterprise": positioning_statement("enterprise"),
            },
        },
        "expansion": {
            "tracks": [
                TRACK_REVENUE_INTELLIGENCE,
                TRACK_COMPANY_BRAIN,
                TRACK_GOVERNANCE,
                TRACK_AI_QUICK_WIN,
            ],
            "upsell_matrix": upsell,
        },
        "unit_economics": {
            "gross_margin_demo": {**gross, "is_estimate": True},
            "cac_payback_demo": {**cac, "is_estimate": True},
            "pricing_tiers_summary": tiers.get("tiers") if isinstance(tiers, dict) else tiers,
        },
        "verticals_priority": _verticals_priority(),
        "north_star": _north_star_table(),
        "weekly_motions": _weekly_motions(),
        "guardrails_ar": list(_GUARDRAILS_AR),
        "ops_client_pack": _ops_client_pack(),
        "integration_truth_summary": build_integration_truth_summary(),
        "doc_refs": {
            "value_ladder": "docs/value_capture/VALUE_CAPTURE_LADDER.md",
            "gtm_playbook": "docs/GTM_PLAYBOOK.md",
            "service_ladder": "docs/strategic/GTM_PLAYBOOK_SERVICE_LADDER_AR.md",
            "north_star_doc": "docs/commercial/NORTH_STAR_METRICS_AR.md",
            "ops_runbook": "docs/commercial/ops_client_pack/dealix_ops_runbook_ar.md",
            "integration_truth_matrix": "docs/ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md",
            "founder_agent_playbook": "docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md",
            "founder_sell_motion": "docs/ops/FOUNDER_SELL_MOTION_AR.md",
            "founder_delivery_ladder": "docs/ops/FOUNDER_DELIVERY_LADDER_AR.md",
        },
    }


def commercial_strategy_summary(
    *,
    commercial_kpi_pending: int | None = None,
    transformation_verdict: str | None = None,
    all_pilots_template_ready: bool | None = None,
) -> dict[str, Any]:
    """Lightweight block for Business NOW /snapshot."""
    full = build_commercial_strategy_snapshot(
        commercial_kpi_pending=commercial_kpi_pending,
        transformation_verdict=transformation_verdict,
        all_pilots_template_ready=all_pilots_template_ready,
    )
    motions = full.get("weekly_motions") or []
    return {
        "focus": full["focus"],
        "guardrails_ar": full["guardrails_ar"][:3],
        "weekly_motions_count": len(motions),
        "weekly_motions_preview": motions[:3],
        "offers_count": len(full.get("offers_playbook") or []),
        "doc_ref": "docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md",
    }


def render_commercial_strategy_markdown(snapshot: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Commercial strategy snapshot — {snapshot['generated_at'][:10]}")
    lines.append("")
    focus = snapshot.get("focus") or {}
    lines.append("## Focus")
    lines.append(f"- stage: {focus.get('stage')}")
    lines.append(f"- primary_offer_id: {focus.get('primary_offer_id')}")
    lines.append(f"- rationale: {focus.get('rationale_ar')}")
    lines.append("")
    lines.append("## Offers")
    for o in snapshot.get("offers_playbook") or []:
        lines.append(
            f"- {o.get('service_id')}: {o.get('price_sar')} SAR — {o.get('success_metric_ar')}"
        )
    lines.append("")
    lines.append("## Weekly motions")
    for m in snapshot.get("weekly_motions") or []:
        lines.append(f"- {m.get('day')}: {m.get('action_ar')}")
    lines.append("")
    lines.append("## Guardrails")
    for g in snapshot.get("guardrails_ar") or []:
        lines.append(f"- {g}")
    return "\n".join(lines) + "\n"
