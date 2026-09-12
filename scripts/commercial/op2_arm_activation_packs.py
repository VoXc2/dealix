#!/usr/bin/env python3
"""OP2 commercial activation packs for EXISTING Dealix arms.

Turns fresh, independently-verified Saudi official signals into truth-safe
commercial activation packs bound to arms that already exist in the canonical
44-arm registry. It creates NO new arm, NO new permanent agent, NO parallel
company machine, and NO pipeline. Research is never a relationship.

Packs produced (all bound to existing arms):
  A  ARM-001 + ARM-016  Fatoora / revenue-leakage readiness (ZATCA Wave 25)
  B  ARM-002 + ARM-006 + ARM-008  Governed AI / agent reliability (CST + SDAIA)
  C  ARM-003 + ARM-028  Market access + cybersecurity evidence (NCA)
  D  ARM-023  Open Banking (SAMA) — VALIDATE / partner-first only

It also emits a transparent 44-arm priority VIEW. Research signal strength can
move only LIGHT/HOLD/RADAR prioritisation; it can never silently displace the
current ACTIVE_DEEP Top-3, which remain locked unless real customer/economic
evidence exists.

Prints: DEALIX_OP2_ARM_PACKS=OK plus machine lines.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ARM_REGISTRY = REPO_ROOT / "config" / "company" / "dealix_arm_registry.json"
ARM_PLAYBOOKS = REPO_ROOT / "config" / "company" / "dealix_arm_execution_playbooks.json"
WAVE_PATH = REPO_ROOT / "data" / "commercial" / "op2_market_intelligence_wave_v1.json"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_arm_activation_packs_v1.json"

UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
DEEP_WIP_MAX = 3
LOCKED_STATES = ("ACTIVE_DEEP",)

# ---------------------------------------------------------------------------
# Pack definitions (data only; every external effect flag stays false).
# ---------------------------------------------------------------------------

PACKS: list[dict[str, Any]] = [
    {
        "pack_id": "OP2-PACK-A-FATOORA",
        "title": "Fatoora / Revenue-Leakage Readiness + Integration Operations",
        "arms": ["ARM-001", "ARM-016"],
        "official_signal_ids": ["op2-2026-zatca-wave25-einvoicing"],
        "certification_claim": False,
        "icp": {
            "sectors": ["finance_fintech_insurance", "retail_commerce_ecommerce", "professional_services", "export_import_rhq"],
            "buyer_roles": ["cfo", "finance_manager", "tax_compliance_lead", "operations_director"],
            "size_hypothesis": "SME to mid-market with VAT-subject revenue above SAR 187,500 in any of 2022-2025",
            "problem_hypotheses": [
                "E-invoicing integration not yet mapped to the Fatoora integration phase",
                "Manual reconciliation between invoices, VAT returns and collections",
                "Unknown readiness before the 1 February 2027 integration date",
            ],
        },
        "free_diagnostic": {
            "depths": ["D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"],
            "families": ["A03", "A04", "A14", "A15"],
            "route": "/book",
            "api": "POST /api/v1/public/execution-diagnostic",
            "card_required": False,
            "roi_promised": False,
        },
        "qualification_gates": [
            "VAT-subject revenue in scope of an announced ZATCA wave (self-declared, then evidenced)",
            "Named finance/tax decision owner",
            "Confirmed current invoicing stack and integration status",
            "No request for a tax/legal certification opinion from Dealix",
        ],
        "discovery_questions_ar": [
            "ما تاريخ آخر موجة تكامل تنطبق عليكم ومعايير الاختيار؟",
            "كيف تُربط الفواتير الإلكترونية بإقرار ضريبة القيمة المضافة حالياً؟",
            "أين يحدث التسرّب بين الفاتورة والتحصيل؟",
        ],
        "discovery_questions_en": [
            "Which integration wave applies to you and on what criteria?",
            "How are e-invoices reconciled to the VAT return today?",
            "Where does leakage occur between invoice, collections and reporting?",
        ],
        "proposal_skeleton": {
            "phases": [
                "Readiness assessment (free D0-D2 diagnostic)",
                "Qualified discovery",
                "Customer-specific implementation scope",
                "Managed exception/operations retainer",
            ],
            "pricing_basis": "QUOTE_AFTER_QUALIFIED_DISCOVERY",
            "public_fixed_price": False,
        },
        "acceptance_criteria": [
            "Readiness gaps documented with owner and target date",
            "Integration/reconciliation workflow described end-to-end",
            "Evidence of each agreed control captured and re-verified",
        ],
        "proof_requirements": [
            "Before/after reconciliation evidence (no customer identity without permission)",
            "Control evidence pack",
            "Customer validation statement where permission is granted",
        ],
        "delivery_runbook": [
            "Intake + consent",
            "Free D0-D2 assessment",
            "Discovery call with decision owner",
            "Scope + quote (no public price)",
            "Implementation with human gates",
            "Evidence capture + customer validation",
        ],
        "stop_loss": "Stop if no named owner, if the buyer wants a certification opinion, or if eligibility cannot be evidenced.",
        "partner_regulatory_boundary": {
            "tax_or_legal_certification": "NOT_PROVIDED",
            "licensed_tax_firm_partner": "OPTIONAL_IF_CERTIFICATION_REQUIRED",
            "note": "Dealix provides integration and operations evidence, never tax/legal certification.",
        },
        "content_seo_drafts": {
            "publish_authority": False,
            "ar_title": "الفاتورة الإلكترونية: كيف تستعد لموجة التكامل القادمة بدل الانتظار؟",
            "ar_body": "الموجة 25 من مرحلة التكامل تشمل المكلفين الذين تجاوزت إيراداتهم الخاضعة للضريبة 187,500 ريال في أي من 2022-2025، مع موعد تكامل في 1 فبراير 2027. ابدأ بتشخيص مجاني لتحديد الفجوات — بدون أي ادعاء شهادة ضريبية.",
            "en_title": "E-invoicing: preparing for the next integration wave instead of waiting",
            "en_body": "Wave 25 covers taxpayers with VAT-subject revenue above SAR 187,500 in any of 2022-2025, integrating by 1 February 2027. Start with a free readiness diagnostic — no tax-certification claim.",
        },
        "next_evidence_required": [
            "Confirm ZATCA notification status per prospect",
            "Capture current invoicing stack and integration gaps",
        ],
        "reason_codes": ["OFFICIAL_SIGNAL", "HARD_DEADLINE_2027-02-01", "EXISTING_ARM_ONLY"],
        "truth_class": "PATTERN_RESEARCH_PACK",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "counts_as_relationship": False,
    },
    {
        "pack_id": "OP2-PACK-B-GOVERNED-AI",
        "title": "Governed AI / Agent Reliability Readiness",
        "arms": ["ARM-002", "ARM-006", "ARM-008"],
        "official_signal_ids": [
            "op2-2026-cst-ai-adoption-guide-tech",
            "op2-2026-sdaia-ai-governance-package",
            "op2-2026-pdpl-active-enforcement",
        ],
        "certification_claim": False,
        "icp": {
            "sectors": ["technology_saas_si", "finance_fintech_insurance", "healthcare", "telecom_media_marketing"],
            "buyer_roles": ["cto", "cio", "product_lead", "ai_governance_lead", "ciso"],
            "size_hypothesis": "Saudi technology company shipping AI or AI-agent features to customers",
            "problem_hypotheses": [
                "No inventory of AI/agent systems, tools, data and action boundaries",
                "Missing evaluation, approval, and human-oversight evidence",
                "Unclear readiness against CST/SDAIA guidance and PDPL duties",
            ],
        },
        "free_diagnostic": {
            "depths": ["D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"],
            "families": ["A11", "A12", "A13", "A43"],
            "route": "/book",
            "api": "POST /api/v1/public/execution-diagnostic",
            "card_required": False,
            "roi_promised": False,
        },
        "qualification_gates": [
            "Named AI owner and at least one deployed AI/agent system",
            "Willingness to expose tool/data/action boundaries",
            "No request for a certification or legal opinion from Dealix",
        ],
        "discovery_questions_ar": [
            "ما الأنظمة/الوكلاء العاملون حالياً وأي أدوات وبيانات يلمسون؟",
            "كيف تُقيّم مخرجات النموذج قبل التأثير على العميل؟",
            "أين توجد موافقة بشرية على القرارات الحساسة؟",
        ],
        "discovery_questions_en": [
            "What AI/agent systems run today, and what tools/data can they touch?",
            "How are model outputs evaluated before customer impact?",
            "Where is human oversight enforced on sensitive decisions?",
        ],
        "proposal_skeleton": {
            "phases": [
                "Free readiness diagnostic",
                "AI inventory + risk mapping",
                "Control/eval/approval implementation",
                "Managed AI reliability retainer",
            ],
            "pricing_basis": "QUOTE_AFTER_QUALIFIED_DISCOVERY",
            "public_fixed_price": False,
        },
        "acceptance_criteria": [
            "Complete AI/agent inventory with owners and boundaries",
            "Evaluation and human-oversight evidence per high-risk system",
            "Remediation items closed and re-verified",
        ],
        "proof_requirements": [
            "AI inventory artifact",
            "Eval/control evidence pack",
            "Customer validation of a fixed gap",
        ],
        "delivery_runbook": [
            "Intake + consent",
            "Free readiness diagnostic",
            "AI inventory and gap workshop",
            "Scope + quote",
            "Implement controls/evals",
            "Evidence capture + validation",
        ],
        "stop_loss": "Stop if no named AI owner, if the buyer seeks certification, or if systems cannot be inventoried safely.",
        "partner_regulatory_boundary": {
            "certification_or_audit_opinion": "NOT_PROVIDED",
            "legal_pdpl_opinion": "NOT_PROVIDED",
            "note": "Dealix provides readiness, control and evidence engineering; not certification or legal advice.",
        },
        "content_seo_drafts": {
            "publish_authority": False,
            "ar_title": "الذكاء الاصطناعي المسؤول للشركات التقنية: جاهزية قبل التوسع",
            "ar_body": "دليل تبني الذكاء الاصطناعي من هيئة الاتصالات والفضاء والتقنية يغطي العمليات والمنتجات والوكلاء، ومعه إطار جاهزية بخمسة أبعاد. ابدأ بتشخيص مجاني لفجوات الحوكمة والتقييم — بدون ادعاء شهادة.",
            "en_title": "Responsible AI for tech companies: readiness before scale",
            "en_body": "CST's AI adoption guide covers operations, products and AI agents with a five-dimension readiness frame. Start with a free governance/eval gap diagnostic — no certification claim.",
        },
        "next_evidence_required": [
            "Confirm AI/agent systems per prospect",
            "Capture which official guidance the buyer tracks",
        ],
        "reason_codes": ["OFFICIAL_SIGNAL", "NO_CERTIFICATION_CLAIM", "EXISTING_ARM_ONLY"],
        "truth_class": "PATTERN_RESEARCH_PACK",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "counts_as_relationship": False,
    },
    {
        "pack_id": "OP2-PACK-C-MARKET-ACCESS-CYBER",
        "title": "Market Access + Cybersecurity Evidence Readiness",
        "arms": ["ARM-003", "ARM-028"],
        "official_signal_ids": [
            "op2-2026-nca-ncnicc-private-sector",
            "op2-2026-nca-ecc2-controls",
            "op2-2026-nupco-localization-digital",
        ],
        "certification_claim": False,
        "icp": {
            "sectors": ["government_b2g", "healthcare", "technology_saas_si", "industrial_manufacturing"],
            "buyer_roles": ["ciso", "grc_lead", "procurement_director", "partner_manager"],
            "size_hypothesis": "Private-sector firm or supplier to an in-scope entity with cyber evidence obligations",
            "problem_hypotheses": [
                "No mapped evidence base against NCA controls",
                "Unclear applicability (private non-CNI vs CNI vs supplier)",
                "Tender/partner route requires specialist credentials Dealix does not hold",
            ],
        },
        "free_diagnostic": {
            "depths": ["D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"],
            "families": ["A13", "A15", "A28", "A36"],
            "route": "/book",
            "api": "POST /api/v1/public/execution-diagnostic",
            "card_required": False,
            "roi_promised": False,
        },
        "qualification_gates": [
            "Applicability determined against NCA control families",
            "Named security/compliance owner",
            "Explicit partner/specialist boundary if audit authority is required",
            "No claim of government access or accreditation",
        ],
        "discovery_questions_ar": [
            "هل الجهة ضمن نطاق الضوابط أم مورد لها؟",
            "أين توجد فجوات الأدلة الحالية؟",
            "من الشريك/المدقق المعتمد عند الحاجة لسلطة تخصصية؟",
        ],
        "discovery_questions_en": [
            "Is the entity in-scope, or a supplier to one?",
            "Where are the current evidence gaps?",
            "Which accredited partner/auditor is required where specialist authority applies?",
        ],
        "proposal_skeleton": {
            "phases": [
                "Free applicability/evidence diagnostic",
                "Evidence matrix + gap map",
                "Remediation + evidence operations",
                "Partner-led route where specialist authority required",
            ],
            "pricing_basis": "QUOTE_AFTER_QUALIFIED_DISCOVERY",
            "public_fixed_price": False,
        },
        "acceptance_criteria": [
            "Control applicability matrix completed",
            "Evidence owners and gaps assigned",
            "Partner boundary documented for specialist authority",
        ],
        "proof_requirements": [
            "Evidence matrix artifact",
            "Gap closure evidence",
            "Partner attestation where applicable",
        ],
        "delivery_runbook": [
            "Intake + consent",
            "Free applicability diagnostic",
            "Evidence gap workshop",
            "Scope + quote or partner handoff",
            "Evidence build + verification",
        ],
        "stop_loss": "Default PARTNER_OR_NO_BID when specialist authority or accreditation is required.",
        "partner_regulatory_boundary": {
            "government_access_claim": "NONE",
            "accreditation_claim": "NONE",
            "default_bid_posture": "PARTNER_OR_NO_BID",
            "note": "Dealix prepares evidence and partners for specialist authority; it does not claim accreditation or government access.",
        },
        "content_seo_drafts": {
            "publish_authority": False,
            "ar_title": "ضوابط الأمن السيبراني للقطاع الخاص: جاهزية الأدلة بدل الادعاءات",
            "ar_body": "أصدرت الهيئة الوطنية للأمن السيبراني ضوابط للقطاع الخاص من غير ذوي البنية التحتية الحساسة. ابدأ بتشخيص مجاني لخريطة الأدلة والفجوات — بدون ادعاء اعتماد أو وصول حكومي.",
            "en_title": "Private-sector cybersecurity controls: evidence readiness, not claims",
            "en_body": "NCA issued controls for private-sector entities outside critical infrastructure. Start with a free evidence-matrix diagnostic — no accreditation or government-access claim.",
        },
        "next_evidence_required": [
            "Confirm NCNICC applicability per prospect",
            "Identify accredited partners for specialist authority",
        ],
        "reason_codes": ["OFFICIAL_SIGNAL", "PARTNER_OR_NO_BID_DEFAULT", "EXISTING_ARM_ONLY"],
        "truth_class": "PATTERN_RESEARCH_PACK",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "counts_as_relationship": False,
    },
    {
        "pack_id": "OP2-PACK-D-OPEN-BANKING",
        "title": "Open Banking — VALIDATE / Partner-First",
        "arms": ["ARM-023"],
        "official_signal_ids": ["op2-2026-sama-open-banking-licensing"],
        "certification_claim": False,
        "icp": {
            "sectors": ["finance_fintech_insurance"],
            "buyer_roles": ["coo", "cto", "risk_lead", "compliance_lead"],
            "size_hypothesis": "SAMA-licensed or licence-seeking fintech/bank",
            "problem_hypotheses": [
                "Consent/API governance and operational-resilience evidence under a licensed regime",
                "Need for a non-licensed technical partner rather than a licence holder",
            ],
        },
        "free_diagnostic": {
            "depths": ["D0_SNAPSHOT", "D1_RAPID", "D2_FUNCTIONAL"],
            "families": ["A13", "A14", "A15", "A43"],
            "route": "/book",
            "api": "POST /api/v1/public/execution-diagnostic",
            "card_required": False,
            "roi_promised": False,
        },
        "qualification_gates": [
            "Buyer is a licensed provider or a partner of one",
            "Explicit acknowledgement that Dealix is not a SAMA-licensed provider",
            "Specialist/regulatory boundary agreed before any scope",
        ],
        "discovery_questions_ar": [
            "من الجهة المرخّصة في العلاقة؟",
            "كيف تُدار الموافقات وحدود الوصول إلى بيانات العملاء؟",
            "ما الفجوات في جاهزية التشغيل والأدلة؟",
        ],
        "discovery_questions_en": [
            "Who is the licensed entity in the relationship?",
            "How are consent and customer-data access boundaries managed?",
            "What operational/evidence readiness gaps exist?",
        ],
        "proposal_skeleton": {
            "phases": [
                "Free readiness diagnostic (partner-led)",
                "Licensed-provider boundary agreement",
                "Technical evidence/control work under partner",
                "Managed evidence operations under partner",
            ],
            "pricing_basis": "QUOTE_AFTER_QUALIFIED_DISCOVERY",
            "public_fixed_price": False,
        },
        "acceptance_criteria": [
            "Licensed-provider boundary documented and signed",
            "Consent/API evidence requirements mapped",
            "Deliverables scoped strictly as non-licensed technical support",
        ],
        "proof_requirements": [
            "Boundary agreement",
            "Control/evidence artifacts",
            "Licensed partner validation",
        ],
        "delivery_runbook": [
            "Validate partner/licensed boundary",
            "Free readiness diagnostic",
            "Scope + quote under partner",
            "Deliver technical evidence work",
        ],
        "stop_loss": "HOLD/VALIDATE until a licensed partner is engaged; never represent Dealix as a SAMA-licensed provider.",
        "partner_regulatory_boundary": {
            "licensed_provider_claim": "NONE_NEVER",
            "partner_required": True,
            "note": "Dealix must never represent itself as a SAMA-licensed open-banking provider.",
        },
        "content_seo_drafts": {
            "publish_authority": False,
            "ar_title": "المصرفية المفتوحة في السعودية: حدود الشريك مقابل الجهة المرخّصة",
            "ar_body": "بدأت مؤسسة النقد ترخيص شركات التقنية المالية للمصرفية المفتوحة. Dealix ليست جهة مرخّصة؛ نعمل فقط كشريك تقني خلف الجهة المرخّصة. تشخيص مجاني للجاهزية التقنية.",
            "en_title": "Open banking in Saudi Arabia: partner vs licensed-provider boundary",
            "en_body": "SAMA has begun licensing open-banking providers. Dealix is not a licensed provider; we operate only as a technical partner behind the licensed entity. Free readiness diagnostic.",
        },
        "next_evidence_required": [
            "Identify licensed/partnering providers from SAMA primary announcements",
            "Confirm the specialist/regulatory boundary in writing",
        ],
        "reason_codes": ["OFFICIAL_SIGNAL", "PARTNER_FIRST", "NO_LICENSED_PROVIDER_CLAIM"],
        "truth_class": "PATTERN_RESEARCH_PACK",
        "counts_as_pipeline": False,
        "counts_as_revenue": False,
        "counts_as_relationship": False,
    },
]

# ---------------------------------------------------------------------------
# Transparent 44-arm priority view (research only; ACTIVE_DEEP is locked).
# ---------------------------------------------------------------------------

# Research signal strength per arm from the linked packs (1-5). Defaults to 1.
SIGNAL_STRENGTH: dict[str, int] = {
    "ARM-001": 4, "ARM-016": 4,          # ZATCA Wave 25
    "ARM-002": 5, "ARM-006": 5, "ARM-008": 5,  # CST + SDAIA + PDPL
    "ARM-003": 4, "ARM-028": 5,          # NCA NCNICC/ECC + NUPCO
    "ARM-023": 4,                        # SAMA open banking
    "ARM-011": 4, "ARM-012": 4,          # market radar / Etimad
    "ARM-007": 4,                        # PDPL enforcement
    "ARM-019": 3,                        # cloud residency (CCC)
    "ARM-037": 3,                        # AI eval (CST/SDAIA)
}

# Regulated / higher-risk dimension profiles carry more regulatory risk.
HIGH_RISK_DIMENSIONS = {"GOVERNANCE", "FINTECH", "HEALTHCARE"}
LONG_CASH_DIMENSIONS = {"SOFTWARE", "IP_MEDIA", "VENTURE"}


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _index_arms() -> dict[str, dict[str, Any]]:
    registry = _load_json(ARM_REGISTRY)
    return {arm["id"]: arm for arm in registry["arms"]}


def _wave_evidence() -> dict[str, dict[str, Any]]:
    wave = _load_json(WAVE_PATH)
    return {sig["signal_id"]: sig for sig in wave.get("signals", [])}


def build_packs() -> list[dict[str, Any]]:
    arms = _index_arms()
    wave = _wave_evidence()
    built: list[dict[str, Any]] = []
    for pack in PACKS:
        missing_arms = [arm for arm in pack["arms"] if arm not in arms]
        if missing_arms:
            raise ValueError(f"{pack['pack_id']} references unknown arms: {missing_arms}")
        signals = []
        for signal_id in pack["official_signal_ids"]:
            signal = wave.get(signal_id)
            if signal is None:
                raise ValueError(f"{pack['pack_id']} references unknown signal: {signal_id}")
            signals.append(
                {
                    "signal_id": signal_id,
                    "source_ref": signal["source_ref"],
                    "authority_ref": signal.get("authority_ref", UNKNOWN),
                    "observed_at": signal["observed_at"],
                    "fresh_until": signal["fresh_until"],
                    "deadline": signal.get("deadline", UNKNOWN),
                    "authority": signal["authority"],
                }
            )
        built.append(
            {
                **pack,
                "arm_details": [
                    {"id": arm, "name": arms[arm]["name"], "state": arms[arm]["state"], "owner": arms[arm]["owner"]}
                    for arm in pack["arms"]
                ],
                "official_signals": signals,
                "authority_all_false": all(not v for s in signals for v in s["authority"].values()),
                "external_effects": {
                    "send": False,
                    "publish": False,
                    "spend": False,
                    "payment": False,
                    "merge": False,
                    "deploy": False,
                    "dns": False,
                    "db": False,
                    "secret": False,
                },
            }
        )
    return built


def build_ranking() -> dict[str, Any]:
    arms = _index_arms()
    playbooks = _load_json(ARM_PLAYBOOKS)
    horizon_by_arm = {pb["arm_id"]: pb.get("horizon", UNKNOWN) for pb in playbooks.get("playbooks", [])}

    rows: list[dict[str, Any]] = []
    for arm_id, arm in arms.items():
        dimension = arm.get("dimension_profile", UNKNOWN)
        signal_strength = SIGNAL_STRENGTH.get(arm_id, 1)
        relationship_evidence = 0  # no verified company relationships exist
        time_to_cash = 2 if dimension in LONG_CASH_DIMENSIONS else 4
        delivery_readiness = 5 if arm["state"] in {"ACTIVE_DEEP", "ACTIVE_LIGHT"} else 2
        cost_margin_proxy = 4 if dimension not in LONG_CASH_DIMENSIONS else 2
        founder_minutes = 4 if arm["state"] == "ACTIVE_DEEP" else 3  # higher = cheaper in founder time
        regulatory_risk = 5 if dimension in HIGH_RISK_DIMENSIONS else 3  # higher = more risky

        # Transparent internal research score. Denominator factors are risks.
        numerator = signal_strength * (1 + relationship_evidence) * time_to_cash * delivery_readiness * cost_margin_proxy * founder_minutes
        denominator = max(regulatory_risk, 1)
        score = round(numerator / denominator, 4)
        locked = arm["state"] in LOCKED_STATES
        rows.append(
            {
                "arm_id": arm_id,
                "name": arm["name"],
                "state": arm["state"],
                "priority": arm["priority"],
                "owner": arm["owner"],
                "dimension": dimension,
                "horizon": horizon_by_arm.get(arm_id, UNKNOWN),
                "factors": {
                    "official_signal_strength": signal_strength,
                    "relationship_evidence": relationship_evidence,
                    "time_to_cash": time_to_cash,
                    "delivery_readiness": delivery_readiness,
                    "cost_margin_proxy": cost_margin_proxy,
                    "founder_minutes_factor": founder_minutes,
                    "regulatory_risk": regulatory_risk,
                },
                "research_score": score,
                "locked": locked,
                "locked_reason": "CURRENT_ACTIVE_DEEP_TOP3" if locked else None,
                "disposition": "RESEARCH_ONLY_NO_STATE_CHANGE",
                "state_change_allowed": False,
            }
        )

    # Locked ACTIVE_DEEP arms stay in canonical registry order (never re-sorted).
    locked = [r for r in rows if r["locked"]]
    unlocked = sorted([r for r in rows if not r["locked"]], key=lambda r: r["research_score"], reverse=True)
    return {
        "schema": "dealix.op2-arm-priority-view.v1",
        "truth_policy": "RESEARCH_ONLY_CANNOT_DISPLACE_ACTIVE_DEEP",
        "deep_wip_max": DEEP_WIP_MAX,
        "arm_count": len(rows),
        "active_deep_locked_top3": [{"arm_id": r["arm_id"], "name": r["name"], "state": r["state"]} for r in locked[:DEEP_WIP_MAX]],
        "research_top10": [
            {"arm_id": r["arm_id"], "name": r["name"], "research_score": r["research_score"], "disposition": r["disposition"]}
            for r in unlocked[:10]
        ],
        "rows": rows,
        "state_changes_applied": 0,
    }


def build() -> dict[str, Any]:
    return {
        "schema": "dealix.op2-arm-activation-packs.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "lane": "OP2",
        "truth_policy": "RESEARCH_ONLY_NO_RELATIONSHIP_NO_PIPELINE_NO_FIXED_PUBLIC_PRICE",
        "new_arms_created": 0,
        "new_permanent_agents_created": 0,
        "arm_registry": "config/company/dealix_arm_registry.json",
        "packs": build_packs(),
        "ranking": build_ranking(),
        "l5_executed": "NONE",
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_ARM_PACKS=OK",
        f"PACKS={len(result['packs'])}",
        f"NEW_ARMS={result['new_arms_created']}",
        f"ARM_COUNT={result['ranking']['arm_count']}",
        f"DEEP_WIP_MAX={result['ranking']['deep_wip_max']}",
        f"STATE_CHANGES={result['ranking']['state_changes_applied']}",
        f"L5_EXECUTED={result['l5_executed']}",
    ]
    for pack in result["packs"]:
        lines.append(f"PACK {pack['pack_id']} arms={','.join(pack['arms'])} signals={','.join(pack['official_signal_ids'])}")
    for row in result["ranking"]["active_deep_locked_top3"]:
        lines.append(f"LOCKED {row['arm_id']} {row['state']}")
    for row in result["ranking"]["research_top10"]:
        lines.append(f"RESEARCH_TOP {row['arm_id']} score={row['research_score']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 arm activation packs")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
