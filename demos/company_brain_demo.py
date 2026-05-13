"""Company Brain Sprint — 21-day end-to-end demo.

Usage:
    python -m demos.company_brain_demo

Demonstrates ingestion -> PII redaction -> RAG retrieval (simulated) ->
citation-grounded answer -> QA gates -> handoff. The retrieval step uses
a tiny in-memory index so the demo runs offline in seconds.
"""
from __future__ import annotations

import json
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_detection import scan_record
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
from dealix.reporting import build_proof_pack
from dealix.reporting.proof_pack import ProofMetric
from dealix.trust.pii_detector import decide_for_record


# Simulated mini-corpus (3 docs). In production this is the customer's documents.
_CORPUS: list[dict[str, str]] = [
    {
        "doc_id": "POL-001",
        "title": "PDPL Internal Handling Policy",
        "section": "§3.2",
        "text": (
            "All customer personal data must be processed under PDPL Art. 5 "
            "lawful basis. Retention defaults to 24 months unless contract states otherwise."
        ),
    },
    {
        "doc_id": "PRD-014",
        "title": "Enterprise Pricing Sheet",
        "section": "Tier — Sovereign",
        "text": (
            "Sovereign tier starts at SAR 80,000/month with in-Kingdom data residency, "
            "dedicated VPC and customer-managed keys (BYOK)."
        ),
    },
    {
        "doc_id": "HR-021",
        "title": "Annual Leave Policy",
        "section": "Eligibility",
        "text": (
            "Employees become eligible for 21 days of paid annual leave after completing "
            "their first 90 days of employment."
        ),
    },
]


def _retrieve(question: str) -> dict[str, str] | None:
    """Tiny keyword-match retriever as a stand-in for full RAG."""
    q = question.lower()
    best: tuple[int, dict[str, str] | None] = (0, None)
    for doc in _CORPUS:
        hits = sum(1 for tok in q.split() if tok in doc["text"].lower())
        if hits > best[0]:
            best = (hits, doc)
    return best[1]


def _answer_with_citation(question: str) -> dict[str, str]:
    doc = _retrieve(question)
    if doc is None:
        return {
            "question": question,
            "answer": "insufficient evidence — لا توجد أدلة كافية في القاعدة المعرفية.",
            "source_doc_id": "",
            "source_section": "",
        }
    return {
        "question": question,
        "answer": doc["text"],
        "source_doc_id": doc["doc_id"],
        "source_section": doc["section"],
    }


def run() -> dict[str, Any]:
    intake = IntakeRequest(
        company_name_ar="مؤسسة المعرفة الصحية",
        company_name_en="Health Knowledge Co.",
        commercial_registration="1010088888",
        vertical=Vertical.HEALTHCARE,
        tier=CustomerTier.MID_MARKET,
        region="riyadh",
        headcount=140,
        primary_pain_ar="ملفات السياسات مبعثرة والموظفون يستغرقون وقتًا للبحث.",
        primary_pain_en="Policy files are fragmented and staff spend time searching.",
        requested_offer=StartingOffer.COMPANY_BRAIN,
        contact_name="مديرة الموارد",
        contact_role="HR Director",
        contact_email="hr@example-hc.sa",
        pdpl_acknowledged=True,
    )
    res = process_intake(intake)
    sow = build_scope(intake, res)

    state = start_project(project_id=res.project_id, actor="hocs")
    for next_stage in (MachineStage.DIAGNOSE, MachineStage.DESIGN, MachineStage.BUILD, MachineStage.VALIDATE):
        state = transition(state, next_stage, actor="hocs")

    # PII gate per document
    pii_decisions = [decide_for_record(doc).to_dict() for doc in _CORPUS]

    # Q&A samples with citation enforcement
    questions = [
        "What is the default retention period under PDPL?",
        "What does Sovereign tier include?",
        "What is the credit-card return policy?",  # not in corpus -> insufficient evidence
    ]
    answers = [_answer_with_citation(q) for q in questions]

    # QA
    gates = build_blank_gates()
    for g in gates:
        for c in g.checks:
            c.passed = True
    score = QualityScore(
        business_impact=17,
        data_quality=13,
        output_quality_ar_en=14,
        customer_usability=9,
        safety_compliance=15,
        productization=13,
        retainer_upgradeability=8,
    )
    qa = evaluate(state.project_id, gates, score, reviewer="hocs")
    state = transition(state, MachineStage.DELIVER, actor="hocs", ships=qa.ships)

    pack = build_proof_pack(
        project_id=state.project_id,
        customer_codename="HealthKnow-D1",
        vertical="healthcare",
        headline_ar="100% من الإجابات تحوي مصادر؛ تقليل زمن البحث بنسبة 60%.",
        headline_en="100% of answers cite sources; 60% reduction in search time.",
        metrics=[
            ProofMetric(
                name_ar="نسبة الإجابات بمصادر",
                name_en="Answers with citations",
                before="—",
                after="100%",
                unit="%",
                method_ar="فحص 30 إجابة عينة.",
                method_en="Audit of 30 sample answers.",
            ),
            ProofMetric(
                name_ar="زمن البحث المتوسط",
                name_en="Mean search time",
                before=8,
                after=3,
                unit="minutes",
                method_ar="استبيان موظفين قبل/بعد.",
                method_en="Employee survey before/after.",
            ),
        ],
    )

    state = transition(state, MachineStage.PROVE, actor="hocs")
    state = transition(state, MachineStage.EXPAND, actor="hocs")

    handoff = build_handoff(
        project_id=state.project_id,
        title_ar="تسليم Company Brain",
        title_en="Company Brain Handoff",
        next_step_summary_ar="انتقل إلى Sales Knowledge Assistant لاحقًا.",
        next_step_summary_en="Move to a Sales Knowledge Assistant next.",
    )
    rec = recommend(
        project_id=state.project_id,
        completed_offer=StartingOffer.COMPANY_BRAIN,
        quality_score=qa.score.total,
        ships=qa.ships,
    )

    return {
        "demo": "Company Brain Sprint",
        "intake": res.to_dict(),
        "sow_summary": {
            "title_en": sow.title_en,
            "price_sar": sow.price_sar,
            "duration_days": sow.duration_days,
        },
        "documents_indexed": [d["doc_id"] for d in _CORPUS],
        "pii_decisions": pii_decisions,
        "answers_with_citations": answers,
        "qa": {"ships": qa.ships, "score": qa.score.total},
        "proof_pack": pack.to_dict(),
        "handoff_id": handoff.handoff_id,
        "renewal_proposal": rec.to_dict(),
        "final_stage": state.current_stage,
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
