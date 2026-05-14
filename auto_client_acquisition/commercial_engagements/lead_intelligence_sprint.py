"""Lead Intelligence Sprint — deterministic bundle: data quality, dedupe, score, drafts audit."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from auto_client_acquisition.commercial_engagements.schemas import (
    LeadIntelligenceSprintInput,
    LeadIntelligenceSprintReport,
)
from auto_client_acquisition.data_os.data_quality_score import (
    account_row_completeness,
    summarize_table_quality,
)
from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from auto_client_acquisition.revenue_os.dedupe import suggest_dedupe_fingerprint


def _normalize_row(raw: dict[str, Any]) -> dict[str, Any]:
    row = dict(raw)
    name = (row.get("company_name") or row.get("company") or "").strip()
    row["company_name"] = name
    return row


def score_lead_row(
    row: dict[str, Any],
    *,
    sector_weight: float,
    city_weight: float,
) -> float:
    """Completeness over core keys plus small bonuses for sector/city."""
    keys = ("company_name", "sector", "city", "phone", "email")
    base = account_row_completeness(row, keys)
    bonus = 0.0
    if str(row.get("sector") or "").strip():
        bonus += sector_weight
    if str(row.get("city") or "").strip():
        bonus += city_weight
    return min(1.0, round(base + bonus, 4))


def _draft_intro_ar(company: str) -> str:
    """Short internal outreach draft — audited; no forbidden automation phrases."""
    safe = company or "العميل"
    return (
        f"مسودّة داخلية — مراجعة قبل الإرسال: نرحّب بـ{safe} ونقترح "
        "جلسة تعرّف قصيرة لمناقشة احتياجات التشغيل والامتثال."
    )


def run_lead_intelligence_sprint(
    inp: LeadIntelligenceSprintInput | dict[str, Any],
) -> LeadIntelligenceSprintReport:
    if isinstance(inp, dict):
        inp = LeadIntelligenceSprintInput.model_validate(inp)

    raw_rows = inp.accounts[:500]
    normalized = [_normalize_row(r) for r in raw_rows]

    required = ("company_name", "sector", "city")
    data_quality = summarize_table_quality(normalized, required_keys=required)

    enriched: list[dict[str, Any]] = []
    dedupe_full: list[dict[str, Any]] = []
    for row in normalized:
        company = str(row.get("company_name") or "")
        hint = suggest_dedupe_fingerprint(
            company_name=company or "unknown",
            domain=row.get("domain") if isinstance(row.get("domain"), str) else None,
            phone=row.get("phone") if row.get("phone") is not None else None,
            email=row.get("email") if isinstance(row.get("email"), str) else None,
            external_crm_id=row.get("external_crm_id")
            if isinstance(row.get("external_crm_id"), str)
            else None,
        )
        dedupe_full.append(asdict(hint))
        score = score_lead_row(
            row,
            sector_weight=inp.sector_weight,
            city_weight=inp.city_weight,
        )
        item = {
            **row,
            "score": score,
            "dedupe_fingerprint_key": hint.fingerprint_key,
            "dedupe_merge_safe": hint.merge_safe,
        }
        enriched.append(item)

    enriched.sort(key=lambda x: x["score"], reverse=True)
    top = enriched[: inp.top_n]

    action_plan = [
        "تثبيت الحقول الإلزامية: الاسم التجاري، القطاع، المدينة، هاتف، بريد.",
        "مراجعة يدوية لمجموعات dedupe ذات merge_safe قبل أي دمج في CRM.",
        "ترتيب الحسابات حسب درجة الاكتمال ثم النداء الدافئ المعتمد فقط.",
        "ربط كل مسودّة خارجية ببوابة موافقة مؤسس قبل الإرسال.",
        "توثيق مصدر كل صف (Tier1) وفق سجل المصادر في Revenue OS.",
    ]

    draft_audits: list[dict[str, Any]] = []
    for row in top[:5]:
        text = _draft_intro_ar(str(row.get("company_name") or ""))
        issues = audit_draft_text(text)
        draft_audits.append({"company_name": row.get("company_name"), "issues": issues, "sample_draft": text})

    gov_notes: list[str] = []
    low_complete = [r for r in enriched if r["score"] < 0.35]
    if low_complete:
        gov_notes.append(f"rows_low_score:{len(low_complete)}")

    proof_pack_suggestions = [
        ProofEventType.LEAD_INTAKE.value,
        ProofEventType.DELIVERY_STARTED.value,
        ProofEventType.DELIVERY_TASK_COMPLETED.value,
        ProofEventType.PROOF_PACK_ASSEMBLED.value,
        ProofEventType.DIAGNOSTIC_DELIVERED.value,
    ]

    return LeadIntelligenceSprintReport(
        data_quality=data_quality,
        accounts_ranked=top,
        dedupe_hints=dedupe_full[: min(50, len(dedupe_full))],
        action_plan=action_plan,
        draft_audits=draft_audits,
        governance_notes=gov_notes,
        proof_pack_suggestions=proof_pack_suggestions,
    )
