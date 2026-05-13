"""Revenue Intelligence Sprint — 10-minute end-to-end demo.

Usage:
    python -m demos.revenue_intelligence_demo

Walks through: intake -> SOW -> data quality -> scoring -> top 10
recommendations -> QA gates -> proof pack -> handoff -> renewal.
"""
from __future__ import annotations

import json
from typing import Any

from auto_client_acquisition.customer_data_plane.data_quality_score import score_batch
from auto_client_acquisition.customer_data_plane.pii_detection import scan_batch
from auto_client_acquisition.delivery_factory.client_handoff import build_handoff
from auto_client_acquisition.delivery_factory.client_intake import (
    CustomerTier,
    IntakeRequest,
    StartingOffer,
    Vertical,
    process_intake,
)
from auto_client_acquisition.delivery_factory.delivery_checklist import (
    Stage,
    checklist_for,
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
from auto_client_acquisition.revenue_os.icp_builder import from_answers
from auto_client_acquisition.revenue_os.lead_scoring import rank_top_k


SAMPLE_RECORDS: list[dict[str, Any]] = [
    {
        "company_name_ar": "بنك الرياض الافتراضي",
        "vertical": "bfsi",
        "region": "riyadh",
        "headcount": 250,
        "annual_revenue_sar": 350_000_000,
        "triggers": ["funding", "hire"],
        "commercial_registration": "1010001111",
        "vat_number": "300000000000003",
        "email": "biz@example-bank.sa",
        "phone": "+966500001111",
        "domain": "example-bank.sa",
        "source": "maroof",
        "updated_at": "2026-04-01T00:00:00+00:00",
    },
    {
        "company_name_ar": "شركة الاتصالات الإقليمية",
        "vertical": "telco",
        "region": "jeddah",
        "headcount": 180,
        "annual_revenue_sar": 180_000_000,
        "triggers": ["tender"],
        "commercial_registration": "4030002222",
        "email": "ops@example-telco.sa",
        "phone": "+966500002222",
        "domain": "example-telco.sa",
        "source": "etimad",
        "updated_at": "2026-04-15T00:00:00+00:00",
    },
    {
        "company_name_ar": "مستشفى الرعاية المتقدّمة",
        "vertical": "healthcare",
        "region": "riyadh",
        "headcount": 320,
        "annual_revenue_sar": 220_000_000,
        "triggers": ["tender", "cr_amendment"],
        "commercial_registration": "1010003333",
        "vat_number": "300000000000004",
        "email": "procurement@example-hospital.sa",
        "phone": "+966500003333",
        "domain": "example-hospital.sa",
        "source": "sfda",
        "updated_at": "2026-05-01T00:00:00+00:00",
    },
    {
        "company_name_ar": "متجر التجزئة الذكي",
        "vertical": "retail_ecomm",
        "region": "khobar",
        "headcount": 80,
        "annual_revenue_sar": 65_000_000,
        "triggers": ["expansion"],
        "commercial_registration": "2050004444",
        "email": "ceo@example-retail.sa",
        "phone": "+966500004444",
        "domain": "example-retail.sa",
        "source": "maroof",
        "updated_at": "2026-04-22T00:00:00+00:00",
    },
    {
        "company_name_ar": "شركة الخدمات اللوجستية",
        "vertical": "logistics",
        "region": "dammam",
        "headcount": 60,
        "annual_revenue_sar": 45_000_000,
        "triggers": [],
        "commercial_registration": "2050005555",
        "email": "info@example-logistics.sa",
        "phone": "+966500005555",
        "domain": "example-logistics.sa",
        "source": "chamber",
        "updated_at": "2025-12-01T00:00:00+00:00",
    },
]


def run() -> dict[str, Any]:
    # 1. Intake
    intake = IntakeRequest(
        company_name_ar="مجموعة الديلوكس التجريبية",
        company_name_en="Demo Group",
        commercial_registration="1010099999",
        vat_number="300000000099003",
        vertical=Vertical.BFSI,
        tier=CustomerTier.MID_MARKET,
        region="riyadh",
        headcount=120,
        annual_revenue_sar=80_000_000,
        primary_pain_ar="بيانات الحسابات مبعثرة ولا توجد أولوية واضحة في المبيعات.",
        primary_pain_en="Accounts data is fragmented; no clear sales priority.",
        requested_offer=StartingOffer.REVENUE_INTELLIGENCE,
        contact_name="مدير المبيعات",
        contact_role="Head of Sales",
        contact_email="sales@demo-group.sa",
        contact_phone="+966500000000",
        pdpl_acknowledged=True,
    )
    res = process_intake(intake)
    assert res.accepted

    # 2. ICP + SOW
    icp = from_answers(sector="bfsi", region="riyadh", target_size="mid_market")
    sow = build_scope(intake, res)

    # 3. Data Quality + PII
    pii = scan_batch(SAMPLE_RECORDS)
    quality = score_batch(SAMPLE_RECORDS, has_pii=pii.has_pii, redacted=True)

    # 4. Score + rank top 50 (here we have 5; demo)
    ranked = rank_top_k(SAMPLE_RECORDS, k=10)

    # 5. Stage machine: Discover -> Diagnose -> Design -> Build -> Validate
    state = start_project(project_id=res.project_id, actor="ceo")
    for next_stage in (MachineStage.DIAGNOSE, MachineStage.DESIGN, MachineStage.BUILD, MachineStage.VALIDATE):
        state = transition(state, next_stage, actor="ceo")

    # 6. QA gates
    gates = build_blank_gates()
    for g in gates:
        for c in g.checks:
            c.passed = True
    score = QualityScore(
        business_impact=18,
        data_quality=14,
        output_quality_ar_en=13,
        customer_usability=9,
        safety_compliance=14,
        productization=12,
        retainer_upgradeability=8,
    )
    qa = evaluate(state.project_id, gates, score, reviewer="ceo")

    # 7. Validate -> Deliver -> Prove -> Expand
    state = transition(state, MachineStage.DELIVER, actor="ceo", ships=qa.ships)
    state = transition(state, MachineStage.PROVE, actor="ceo")
    state = transition(state, MachineStage.EXPAND, actor="ceo")

    # 8. Handoff + renewal
    handoff = build_handoff(
        project_id=state.project_id,
        title_ar="تسليم Revenue Intelligence Sprint",
        title_en="Revenue Intelligence Sprint Handoff",
        next_step_summary_ar="Retainer شهري للمحافظة على المخرجات.",
        next_step_summary_en="Monthly retainer to sustain the outputs.",
    )
    rec = recommend(
        project_id=state.project_id,
        completed_offer=StartingOffer.REVENUE_INTELLIGENCE,
        quality_score=qa.score.total,
        ships=qa.ships,
        customer_signaled_volume=False,
    )

    return {
        "demo": "Revenue Intelligence Sprint",
        "intake": res.to_dict(),
        "icp": icp.to_dict(),
        "sow_summary": {
            "title_en": sow.title_en,
            "price_sar": sow.price_sar,
            "total_sar": sow.total_sar,
            "duration_days": sow.duration_days,
            "deliverables_count": len(sow.deliverables),
        },
        "data_quality": quality.to_dict(),
        "pii_summary": {"has_pii": pii.has_pii, "hits": len(pii.hits)},
        "top_5_ranked": [
            {
                "company": rec_in["company_name_ar"],
                "score": round(sc.score, 1),
                "band": sc.band,
                "why_now_en": sc.why_now_en,
            }
            for rec_in, sc in ranked[:5]
        ],
        "qa": {"ships": qa.ships, "score": qa.score.total},
        "stage_progression": [t.to_stage for t in state.transitions if t.from_stage],
        "handoff_id": handoff.handoff_id,
        "renewal_proposal": rec.to_dict(),
        "checklist_items_total": len(checklist_for(StartingOffer.REVENUE_INTELLIGENCE)),
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
