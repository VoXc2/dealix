"""AI Quick Win Sprint — 7-day end-to-end demo.

Usage:
    python -m demos.ai_quick_win_demo

Demonstrates one chosen use case ("CEO weekly report") shipped through the
Delivery Standard: intake -> SOW -> build -> QA -> proof pack -> handoff.
"""
from __future__ import annotations

import json
from typing import Any

from auto_client_acquisition.delivery_factory.client_handoff import build_handoff
from auto_client_acquisition.delivery_factory.client_intake import (
    CustomerTier,
    IntakeRequest,
    StartingOffer,
    Vertical,
    process_intake,
)
from auto_client_acquisition.delivery_factory.qa_review import (
    QualityScore,
    build_blank_gates,
    evaluate,
)
from auto_client_acquisition.delivery_factory.renewal_recommendation import recommend
from auto_client_acquisition.delivery_factory.scope_builder import build_scope
from auto_client_acquisition.delivery_factory.stage_machine import (
    Stage as MachineStage,
    start_project,
    transition,
)
from dealix.reporting import build_executive_report, build_proof_pack
from dealix.reporting.executive_report import KPIRow
from dealix.reporting.proof_pack import ProofMetric


def run() -> dict[str, Any]:
    intake = IntakeRequest(
        company_name_ar="شركة الخدمات اللوجستية الرائدة",
        company_name_en="Lead Logistics Co.",
        commercial_registration="2050000007",
        vertical=Vertical.LOGISTICS,
        tier=CustomerTier.MID_MARKET,
        region="dammam",
        headcount=85,
        primary_pain_ar="التقرير الأسبوعي للرئيس التنفيذي يستهلك 6 ساعات كل أسبوع.",
        primary_pain_en="CEO weekly report takes 6 hours every week.",
        requested_offer=StartingOffer.AI_QUICK_WIN,
        contact_name="رئيس العمليات",
        contact_role="COO",
        contact_email="coo@lead-logistics.sa",
        pdpl_acknowledged=True,
    )
    res = process_intake(intake)
    sow = build_scope(intake, res)

    state = start_project(project_id=res.project_id, actor="cto")
    for next_stage in (MachineStage.DIAGNOSE, MachineStage.DESIGN, MachineStage.BUILD, MachineStage.VALIDATE):
        state = transition(state, next_stage, actor="cto")

    gates = build_blank_gates()
    for g in gates:
        for c in g.checks:
            c.passed = True
    score = QualityScore(
        business_impact=19,
        data_quality=12,
        output_quality_ar_en=14,
        customer_usability=10,
        safety_compliance=14,
        productization=14,
        retainer_upgradeability=9,
    )
    qa = evaluate(state.project_id, gates, score, reviewer="cto")
    state = transition(state, MachineStage.DELIVER, actor="cto", ships=qa.ships)

    pack = build_proof_pack(
        project_id=state.project_id,
        customer_codename="LeadLogistics-D1",
        vertical="logistics",
        headline_ar="توفير 5 ساعات أسبوعيًا في تقرير الرئيس التنفيذي.",
        headline_en="5 hours saved weekly on the CEO report.",
        metrics=[
            ProofMetric(
                name_ar="ساعات الإعداد",
                name_en="Preparation hours",
                before=6,
                after=1,
                unit="hours/week",
                method_ar="قياس قبل/بعد من سجلات الإدارة.",
                method_en="Before/after measurement from manager timesheets.",
            ),
            ProofMetric(
                name_ar="عدد الأخطاء في التقرير",
                name_en="Report errors",
                before=2.3,
                after=0.4,
                unit="errors/week",
                method_ar="عدد التصحيحات بعد المراجعة الأسبوعية.",
                method_en="Count of post-review corrections weekly.",
            ),
        ],
    )

    report = build_executive_report(
        project_id=state.project_id,
        title_ar="تقرير تنفيذي — AI Quick Win Sprint",
        title_en="Executive Report — AI Quick Win Sprint",
        summary_ar="تمت أتمتة تقرير CEO الأسبوعي مع موافقة بشرية وسجل تدقيق.",
        summary_en="Automated CEO weekly report with human approval and audit log.",
        kpis=[
            KPIRow(label_ar="الساعات الموفّرة", label_en="Hours saved", baseline="6", after="1", delta="-5"),
            KPIRow(label_ar="الأخطاء", label_en="Errors", baseline="2.3", after="0.4", delta="-82%"),
        ],
        findings=(
            ["البيانات المصدر متاحة في 3 أنظمة فقط."],
            ["Source data lives in only 3 systems."],
        ),
        recommendations=(
            ["إضافة تقرير المخاطر الأسبوعي في الشهر التالي."],
            ["Add a weekly risks report next month."],
        ),
        next_steps=(
            ["Monthly AI Ops Retainer."],
            ["Monthly AI Ops Retainer."],
        ),
        quality_score=qa.score.total,
        proof_pack_ref=pack.pack_id,
    )

    state = transition(state, MachineStage.PROVE, actor="cto")
    state = transition(state, MachineStage.EXPAND, actor="cto")

    handoff = build_handoff(
        project_id=state.project_id,
        title_ar="تسليم AI Quick Win",
        title_en="AI Quick Win Handoff",
        next_step_summary_ar="انتقل إلى Monthly AI Ops Retainer لإضافة عمليات أخرى.",
        next_step_summary_en="Move to Monthly AI Ops Retainer to add more workflows.",
    )
    rec = recommend(
        project_id=state.project_id,
        completed_offer=StartingOffer.AI_QUICK_WIN,
        quality_score=qa.score.total,
        ships=qa.ships,
    )

    return {
        "demo": "AI Quick Win Sprint",
        "intake": res.to_dict(),
        "sow_summary": {
            "title_en": sow.title_en,
            "price_sar": sow.price_sar,
            "duration_days": sow.duration_days,
        },
        "qa": {"ships": qa.ships, "score": qa.score.total},
        "proof_pack": pack.to_dict(),
        "executive_report_id": report.report_id,
        "handoff_id": handoff.handoff_id,
        "renewal_proposal": rec.to_dict(),
        "final_stage": state.current_stage,
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
