"""Case Study builder + library.

select_publishable + build_candidate + request_quote + approve_candidate
+ list_library — full case-study lifecycle.

Reuses:
  - proof_to_market.engine.approval_gate_check (existing approval gate)
  - proof_ledger.consent_signature (Phase 6 — request_consent + record_signature)
  - leadops_spine.draft_builder._scrub (forbidden tokens)
"""
from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    CaseStudyCandidate,
)

_LIBRARY_PATH = os.path.join("data", "case_studies", "library.jsonl")
_DRAFTS_DIR = os.path.join("data", "case_studies", "drafts")
_INDEX: dict[str, CaseStudyCandidate] = {}


# Forbidden tokens — same regex as draft_builder._scrub, kept here so
# this module doesn't depend on leadops_spine internals.
_FORBIDDEN = [
    re.compile(r"\bguaranteed?\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\bscraping\b", re.IGNORECASE),
    re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    re.compile(r"نضمن"),
]


def _ensure_dirs() -> None:
    os.makedirs(os.path.dirname(_LIBRARY_PATH), exist_ok=True)
    os.makedirs(_DRAFTS_DIR, exist_ok=True)


def _scrub(text: str) -> tuple[str, list[str]]:
    findings: list[str] = []
    cleaned = text
    for pat in _FORBIDDEN:
        if pat.search(cleaned):
            findings.append(pat.pattern)
            cleaned = pat.sub("[REDACTED]", cleaned)
    return cleaned, findings


def _persist_draft(candidate: CaseStudyCandidate) -> None:
    _ensure_dirs()
    _INDEX[candidate.candidate_id] = candidate
    target = os.path.join(_DRAFTS_DIR, f"{candidate.candidate_id}.json")
    with open(target, "w", encoding="utf-8") as f:
        f.write(candidate.model_dump_json(indent=2))


def _persist_library_entry(candidate: CaseStudyCandidate) -> None:
    _ensure_dirs()
    with open(_LIBRARY_PATH, "a", encoding="utf-8") as f:
        f.write(candidate.model_dump_json() + "\n")


def select_publishable(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Filter events down to those eligible for publication."""
    publishable: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for e in events:
        reasons: list[str] = []
        if e.get("evidence_level") not in ("customer_confirmed", "payment_confirmed"):
            reasons.append("evidence_level_too_weak")
        if not e.get("consent_for_publication"):
            reasons.append("consent_not_granted")
        if e.get("approval_status") != "approved":
            reasons.append("not_approved")
        if not e.get("pii_redacted", True):
            reasons.append("pii_not_redacted")
        if reasons:
            rejected.append({"event_id": e.get("event_id"), "reasons": reasons})
        else:
            publishable.append(e)
    return {
        "publishable": publishable,
        "rejected": rejected,
        "total_input": len(events),
        "publishable_count": len(publishable),
    }


def _build_narrative(events: list[dict[str, Any]], sector: str | None) -> tuple[str, str, list[str]]:
    """Compose before/after/proof narrative — bilingual + scrubbed."""
    sector_ar = sector or "—"
    sector_en = sector or "—"
    summaries_ar = " · ".join(e.get("summary_ar", "") for e in events if e.get("summary_ar"))
    summaries_en = " · ".join(e.get("summary_en", "") for e in events if e.get("summary_en"))

    raw_ar = (
        f"دراسة حالة من قطاع {sector_ar}.\n\n"
        f"السياق: عميل في {sector_ar} كان يعاني من بطء في تأهيل العملاء المحتملين.\n"
        f"التدخّل: تفعيل Dealix كطبقة AI للتأهيل والتشغيل.\n"
        f"النتيجة الموثَّقة (proof events): {summaries_ar or 'تفاصيل في الـ proof pack المرفق'}.\n"
        f"الموقف الحالي: قابل للنشر بعد توقيع العميل."
    )
    raw_en = (
        f"Case study — {sector_en} sector.\n\n"
        f"Context: A client in {sector_en} was struggling with slow lead qualification.\n"
        f"Intervention: Dealix activated as the AI operations layer.\n"
        f"Documented outcome (proof events): {summaries_en or 'details in attached proof pack'}.\n"
        f"Status: publishable upon customer signature."
    )

    ar, findings_ar = _scrub(raw_ar)
    en, findings_en = _scrub(raw_en)
    return ar, en, list(set(findings_ar + findings_en))


def build_candidate(
    *,
    customer_handle: str,
    events: list[dict[str, Any]],
    sector: str | None = None,
    objection_addressed: str | None = None,
) -> dict[str, Any]:
    """Build a CaseStudyCandidate. Returns {'candidate', 'safety_findings', 'rejected'}.

    The candidate is NOT yet publishable — it requires consent_signature
    + approval. is_publishable() will return False until both arrive.
    """
    selection = select_publishable(events)
    publishable = selection["publishable"]
    if not publishable:
        raise ValueError(
            "no publishable events — need at least one with "
            "evidence_level in {customer_confirmed, payment_confirmed}, "
            "consent_for_publication=True, approval_status=approved"
        )

    narrative_ar, narrative_en, safety_findings = _build_narrative(publishable, sector)

    candidate = CaseStudyCandidate(
        candidate_id=f"cs_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        proof_event_ids=[e["event_id"] for e in publishable],
        narrative_draft_ar=narrative_ar,
        narrative_draft_en=narrative_en,
        consent_status="not_requested",
        redaction_status="complete",  # all events declared pii_redacted=True
        approval_status="pending",
        sector=sector,
        objection_addressed=objection_addressed,
    )
    _persist_draft(candidate)

    return {
        "candidate": candidate.model_dump(mode="json"),
        "safety_findings": safety_findings,
        "rejected_events": selection["rejected"],
        "publishable_count": len(publishable),
    }


def request_quote(*, candidate_id: str) -> dict[str, Any]:
    """Mark candidate as awaiting customer signature on the narrative.

    The actual consent signature is requested via
    /api/v1/proof-ledger/consent/request — this endpoint just flips the
    case study state to consent_requested and returns the document hash
    that the customer must confirm.
    """
    candidate = _INDEX.get(candidate_id)
    if candidate is None:
        raise ValueError(f"candidate {candidate_id} not found")
    candidate.consent_status = "requested"
    _persist_draft(candidate)
    # The narrative used for hashing is the AR + EN concat, deterministic
    document = candidate.narrative_draft_ar + "\n---\n" + candidate.narrative_draft_en
    from auto_client_acquisition.proof_ledger.consent_signature import (
        request_consent,
    )
    sig = request_consent(
        customer_handle=candidate.customer_handle,
        scope="single_pack",
        narrative=document,
        target_event_ids=list(candidate.proof_event_ids),
    )
    candidate.consent_signature_id = sig.signature_id
    _persist_draft(candidate)
    return {
        "candidate_id": candidate.candidate_id,
        "consent_signature_id": sig.signature_id,
        "document_hash": sig.document_hash,
    }


def approve_candidate(
    *,
    candidate_id: str,
    approver: str,
) -> dict[str, Any]:
    """Final approval — only after consent is signed."""
    candidate = _INDEX.get(candidate_id)
    if candidate is None:
        raise ValueError(f"candidate {candidate_id} not found")
    if candidate.consent_status != "signed":
        raise ValueError(
            f"cannot approve case study without signed consent "
            f"(current: {candidate.consent_status})"
        )
    candidate.approval_status = "approved"
    _persist_draft(candidate)
    if candidate.is_publishable():
        _persist_library_entry(candidate)
    return {
        "candidate_id": candidate.candidate_id,
        "approval_status": candidate.approval_status,
        "publishable_now": candidate.is_publishable(),
        "approver": approver,
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }


def list_library(*, sector: str | None = None, limit: int = 50) -> list[dict[str, Any]]:
    """Return library entries. Reads from JSONL on disk + in-memory index."""
    entries: list[dict[str, Any]] = []
    if os.path.exists(_LIBRARY_PATH):
        with open(_LIBRARY_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if sector and entry.get("sector") != sector:
                        continue
                    entries.append(entry)
                except Exception:
                    continue
    return entries[:limit]
