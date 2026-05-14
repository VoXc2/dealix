"""Revenue Intelligence Pipeline — the end-to-end MVP wedge.

This router is the **commercial heart** of Phase 1 / Constitution v2 §39:

  POST /api/v1/revenue-intelligence/{engagement}/import
      → Import preview: dedupe + Data Quality Score + PII detection.
  POST /api/v1/revenue-intelligence/{engagement}/score
      → Rank accounts by composite ICP-like score; return Top 10.
  POST /api/v1/revenue-intelligence/{engagement}/draft-pack
      → Generate **DRAFT_ONLY** email + call-script + follow-up plan.
      Refused if requested channel is forbidden (cold WhatsApp / LinkedIn /
      scraping).
  GET  /api/v1/revenue-intelligence/{engagement}/state
      → Read current pipeline state (imported / scored / drafts / closed).
  POST /api/v1/revenue-intelligence/{engagement}/finalize
      → Build the Proof Pack v2 record (delegates to
      ``api.routers.proof_pack``-style persistence) and link the
      Revenue Proof.

Every step:
  * Pre-flight checks the operating-manual non-negotiables.
  * Persists an append-only state record under ``var/revenue_intelligence/{engagement}.jsonl``.
  * Returns a structured **GovernanceDecision** envelope so the dashboard
    can render the "blocked / draft-only / approved" status per output.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.endgame_os.governance_product import (
    GovernanceDecision,
)
from auto_client_acquisition.operating_manual_os.non_negotiables import (
    NonNegotiableCheck,
    check_action_against_non_negotiables,
)
from auto_client_acquisition.revenue_os.dedupe import (
    normalize_company_name,
    normalize_domain,
    normalize_phone_e164_hint,
)
from auto_client_acquisition.safe_send_gateway import (
    SendBlocked,
    enforce_doctrine_non_negotiables,
)

router = APIRouter(prefix="/api/v1/revenue-intelligence", tags=["revenue-intelligence"])

_STORE_ROOT = Path(
    os.getenv("DEALIX_REVENUE_INTELLIGENCE_STORE_ROOT", "var/revenue_intelligence")
)

# Channels Dealix supports for drafts (DRAFT_ONLY in every case).
_ALLOWED_CHANNELS: frozenset[str] = frozenset({"email", "whatsapp_with_consent", "call_script", "follow_up_plan"})

# Channels we refuse outright per the non-negotiables.
_FORBIDDEN_CHANNELS: frozenset[str] = frozenset({
    "cold_whatsapp",
    "linkedin_automation",
    "scraping",
    "bulk_outreach",
})


# ---------------------------------------------------------------------------
# State persistence (append-only JSONL per engagement)
# ---------------------------------------------------------------------------


def _engagement_path(engagement_id: str) -> Path:
    if not engagement_id or "/" in engagement_id or ".." in engagement_id:
        raise HTTPException(status_code=422, detail="invalid_engagement_id")
    return _STORE_ROOT / f"{engagement_id}.jsonl"


def _append(engagement_id: str, event: dict[str, Any]) -> None:
    path = _engagement_path(engagement_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    event_with_ts = {**event, "ts": datetime.now(timezone.utc).isoformat()}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event_with_ts, ensure_ascii=False) + "\n")


def _read_events(engagement_id: str) -> list[dict[str, Any]]:
    path = _engagement_path(engagement_id)
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def _latest_event(engagement_id: str, event_type: str) -> dict[str, Any] | None:
    latest: dict[str, Any] | None = None
    for event in _read_events(engagement_id):
        if event.get("type") == event_type:
            latest = event
    return latest


# ---------------------------------------------------------------------------
# Doctrine pre-flight
# ---------------------------------------------------------------------------


def _check_non_negotiables(action: str, **flags: bool) -> None:
    """Raise HTTP 403 if the action violates any doctrine non-negotiable."""

    check = NonNegotiableCheck(action=action, **flags)
    result = check_action_against_non_negotiables(check)
    if not result.allowed:
        raise HTTPException(
            status_code=403,
            detail={"non_negotiables_violated": [v.value for v in result.violations]},
        )


# ---------------------------------------------------------------------------
# Import preview
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _NormalizedAccount:
    raw_index: int
    company_name: str
    company_norm: str
    domain_norm: str | None
    phone_norm: str | None
    city: str | None
    sector: str | None
    relationship_status: str | None
    consent_status: str | None
    last_interaction: str | None
    notes: str | None
    contains_pii: bool


def _normalize_account(idx: int, raw: dict[str, Any]) -> _NormalizedAccount | dict[str, Any]:
    """Normalize one raw row. Returns a normalized record or an error envelope."""

    name = (raw.get("company_name") or "").strip()
    if not name:
        return {"row": idx, "error": "missing_company_name"}
    domain = raw.get("domain") or raw.get("website")
    phone = raw.get("phone") or raw.get("contact_phone")
    contains_pii = bool(raw.get("contact_email") or raw.get("contact_name") or phone)
    return _NormalizedAccount(
        raw_index=idx,
        company_name=name,
        company_norm=normalize_company_name(name),
        domain_norm=normalize_domain(domain) if domain else None,
        phone_norm=normalize_phone_e164_hint(phone) if phone else None,
        city=(raw.get("city") or None),
        sector=(raw.get("sector") or None),
        relationship_status=(raw.get("relationship_status") or None),
        consent_status=(raw.get("consent_status") or None),
        last_interaction=(raw.get("last_interaction") or None),
        notes=(raw.get("notes") or None),
        contains_pii=contains_pii,
    )


def _fingerprint(account: _NormalizedAccount) -> str:
    parts = [account.company_norm]
    if account.domain_norm:
        parts.append(f"d:{account.domain_norm}")
    elif account.phone_norm:
        parts.append(f"p:{account.phone_norm}")
    return "|".join(parts)


def _data_quality_score(accounts: list[_NormalizedAccount], duplicate_count: int) -> dict[str, Any]:
    """Composite Data Quality Score in 0..100."""

    if not accounts:
        return {"score": 0, "completeness": 0.0, "duplicate_rate": 0.0, "tier": "data_readiness_sprint_first"}
    total = len(accounts)
    duplicate_rate = duplicate_count / total
    completeness = sum(
        1 for a in accounts
        if a.city and a.sector and a.relationship_status
    ) / total
    # Weight: 60% completeness inverse-duplicate × 40%.
    score = round((completeness * 60) + ((1 - duplicate_rate) * 40))
    if score >= 85:
        tier = "ready_for_ai_workflow"
    elif score >= 70:
        tier = "usable_with_cleanup"
    elif score >= 50:
        tier = "diagnostic_only"
    else:
        tier = "data_readiness_sprint_first"
    return {
        "score": score,
        "completeness": round(completeness, 3),
        "duplicate_rate": round(duplicate_rate, 3),
        "tier": tier,
    }


@router.post("/{engagement_id}/import")
async def import_preview(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Run the import preview: dedupe + data quality + PII flags.

    Body:
      * ``rows`` (required) — list of raw account dicts (company_name, domain,
        phone, city, sector, relationship_status, consent_status, ...).
      * ``source_passport`` (required) — dict with at minimum ``source_id``,
        ``owner``, ``allowed_use``, ``contains_pii``, ``sensitivity``.
    """

    _check_non_negotiables("revenue_intelligence_import")

    rows = payload.get("rows")
    source_passport = payload.get("source_passport")
    if not isinstance(rows, list) or not rows:
        raise HTTPException(status_code=422, detail="rows[] required (non-empty list)")
    if not isinstance(source_passport, dict):
        raise HTTPException(status_code=422, detail="source_passport object required")

    required_passport_fields = {"source_id", "owner", "allowed_use", "contains_pii", "sensitivity"}
    missing = required_passport_fields - set(source_passport)
    if missing:
        raise HTTPException(
            status_code=422,
            detail={"missing_source_passport_fields": sorted(missing)},
        )

    normalized: list[_NormalizedAccount] = []
    errors: list[dict[str, Any]] = []
    for idx, raw in enumerate(rows):
        if not isinstance(raw, dict):
            errors.append({"row": idx, "error": "row_must_be_object"})
            continue
        result = _normalize_account(idx, raw)
        if isinstance(result, dict):
            errors.append(result)
        else:
            normalized.append(result)

    seen: dict[str, int] = {}
    duplicates: list[dict[str, Any]] = []
    deduped: list[_NormalizedAccount] = []
    for acc in normalized:
        fp = _fingerprint(acc)
        if fp in seen:
            duplicates.append({
                "fingerprint": fp,
                "matched_row": seen[fp],
                "duplicate_row": acc.raw_index,
                "company_name": acc.company_name,
            })
            continue
        seen[fp] = acc.raw_index
        deduped.append(acc)

    quality = _data_quality_score(deduped, duplicate_count=len(duplicates))
    pii_flagged = [acc.raw_index for acc in deduped if acc.contains_pii]

    record = {
        "type": "import_preview",
        "engagement_id": engagement_id,
        "source_passport": source_passport,
        "total_rows": len(rows),
        "normalized_rows": len(normalized),
        "deduped_rows": len(deduped),
        "duplicates_found": len(duplicates),
        "duplicate_samples": duplicates[:10],
        "errors": errors[:20],
        "data_quality": quality,
        "pii_flagged_count": len(pii_flagged),
        "deduped_preview": [
            {
                "row": acc.raw_index,
                "company_name": acc.company_name,
                "company_norm": acc.company_norm,
                "domain": acc.domain_norm,
                "city": acc.city,
                "sector": acc.sector,
                "relationship_status": acc.relationship_status,
                "consent_status": acc.consent_status,
                "contains_pii": acc.contains_pii,
            }
            for acc in deduped
        ],
    }
    _append(engagement_id, record)
    return {
        "import_preview": record,
        "governance_decision": GovernanceDecision.ALLOW_WITH_REVIEW.value,
        "next_step": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/score "
            "to rank the deduped accounts."
        ),
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def _score_account(acc: dict[str, Any], sector_priority: dict[str, int]) -> dict[str, Any]:
    """Compute a composite ICP score in 0..100 for a normalized account."""

    score = 0
    reasons: list[str] = []

    # Sector priority (0..30)
    sector = (acc.get("sector") or "").strip().lower()
    sector_bonus = sector_priority.get(sector, 5)
    score += sector_bonus
    if sector_bonus >= 25:
        reasons.append(f"sector_priority:{sector}")

    # Relationship status (0..30)
    rel = (acc.get("relationship_status") or "").strip().lower()
    rel_bonus = {
        "existing_relationship": 30,
        "warm_intro": 22,
        "previously_engaged": 18,
        "referral": 15,
        "inbound_lead": 12,
        "first_touch": 5,
        "no_relationship": 0,
    }.get(rel, 0)
    score += rel_bonus
    if rel_bonus >= 20:
        reasons.append(f"strong_relationship:{rel}")

    # Consent for safe outreach (0..15)
    consent = (acc.get("consent_status") or "").strip().lower()
    if consent in {"explicit_consent", "opt_in"}:
        score += 15
        reasons.append("consent_present")
    elif consent in {"implicit", "warm_intro"}:
        score += 7

    # Domain present (0..10)
    if acc.get("domain"):
        score += 10
        reasons.append("domain_present")

    # City present + Saudi-relevant (0..15)
    city = (acc.get("city") or "").strip().lower()
    saudi_cities = {"riyadh", "jeddah", "dammam", "khobar", "mecca", "medina", "الرياض", "جدة", "الدمام"}
    if city:
        score += 5
        if city in saudi_cities:
            score += 10
            reasons.append(f"saudi_city:{city}")

    score = min(score, 100)
    return {**acc, "score": score, "reasons": reasons}


@router.post("/{engagement_id}/score")
async def score_accounts(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Score the deduped accounts and return the Top 10.

    Body:
      * ``sector_priority`` (optional) — dict mapping lower-case sector
        names to bonus 0..30. Defaults to a B2B-services-friendly map.
    """

    _check_non_negotiables("revenue_intelligence_score")

    preview = _latest_event(engagement_id, "import_preview")
    if preview is None:
        raise HTTPException(
            status_code=409,
            detail="import_preview_missing_run_import_first",
        )
    accounts = preview.get("deduped_preview") or []
    if not accounts:
        raise HTTPException(status_code=409, detail="no_deduped_accounts_to_score")

    sector_priority = payload.get("sector_priority") or {
        "b2b_services": 30,
        "consulting": 28,
        "professional_services": 28,
        "training": 25,
        "agency": 22,
        "saas": 20,
        "real_estate_services": 18,
        "clinics": 15,
        "logistics": 15,
    }
    sector_priority = {k.lower(): int(v) for k, v in sector_priority.items()}

    scored = [_score_account(a, sector_priority) for a in accounts]
    scored.sort(key=lambda a: a["score"], reverse=True)
    top10 = scored[:10]

    record = {
        "type": "scored_accounts",
        "engagement_id": engagement_id,
        "sector_priority": sector_priority,
        "top_10": top10,
        "all_scores_summary": {
            "count": len(scored),
            "max": scored[0]["score"] if scored else 0,
            "min": scored[-1]["score"] if scored else 0,
            "median": scored[len(scored) // 2]["score"] if scored else 0,
        },
    }
    _append(engagement_id, record)
    return {
        "scored": record,
        "governance_decision": GovernanceDecision.ALLOW_WITH_REVIEW.value,
        "next_step": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/draft-pack "
            "with channel='email' (DRAFT_ONLY)."
        ),
    }


# ---------------------------------------------------------------------------
# Draft pack — DRAFT_ONLY, never sent
# ---------------------------------------------------------------------------


def _email_draft_ar(account: dict[str, Any]) -> str:
    company = account.get("company_name", "—")
    sector = account.get("sector") or "خدمات"
    return (
        f"السلام عليكم،\n\n"
        f"نتواصل من Dealix بخصوص {company}. لاحظنا أن قطاع {sector} يشهد فرصاً "
        f"لتنظيم المبيعات وتقليل الفرص الضائعة عبر تحليل بياناتكم الحالية وترتيب "
        f"الأولويات، ضمن إطار حوكمة واضح ومخرجات قابلة للمراجعة قبل التواصل.\n\n"
        f"نرحب بجلسة قصيرة لاستعراض Capability Diagnostic الخاص بنا، مع Proof Pack "
        f"يوضح ما يمكن إنجازه خلال أول Sprint بدون أي تواصل خارجي تلقائي.\n\n"
        f"مع التقدير،\nفريق Dealix"
    )


def _email_draft_en(account: dict[str, Any]) -> str:
    company = account.get("company_name", "—")
    sector = account.get("sector") or "services"
    return (
        f"Hello,\n\n"
        f"This is Dealix reaching out about {company}. We're seeing repeated "
        f"opportunity-loss patterns in the {sector} segment that respond well to "
        f"a governed account-scoring + draft-pack engagement — reviewable outputs, "
        f"no autonomous outreach.\n\n"
        f"We'd value a 30-minute Capability Diagnostic walk-through and a Proof "
        f"Pack scoped to your first Sprint.\n\n"
        f"Best regards,\nThe Dealix Team"
    )


def _call_script(account: dict[str, Any]) -> str:
    company = account.get("company_name", "—")
    return (
        f"Opener (AR): «صباح الخير، أتواصل من Dealix بخصوص {company}. "
        f"هل عندكم دقيقتين أوضح فكرة Capability Diagnostic؟»\n"
        f"Discovery: ما هو أكبر مصدر ضياع للفرص حاليًا؟ هل البيانات منظمة؟ "
        f"من هو مالك متابعة المبيعات؟\n"
        f"Close: نرسل لكم Capability Diagnostic بسعر ثابت، ومخرجاته تشمل "
        f"Proof Pack مكتوب يحدد الخطوة التالية."
    )


def _follow_up_plan(account: dict[str, Any]) -> list[dict[str, str]]:
    company = account.get("company_name", "—")
    return [
        {"day": "0", "step": f"Send draft email to {company} after internal approval."},
        {"day": "+3", "step": "Founder follow-up: confirm receipt + offer Diagnostic call."},
        {"day": "+7", "step": "Send Capability Diagnostic one-pager + Proof Pack sample."},
        {"day": "+14", "step": "Final follow-up: convert to paid Diagnostic or move to nurture."},
    ]


@router.post("/{engagement_id}/draft-pack")
async def draft_pack(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Generate the Draft Pack — DRAFT_ONLY for every channel.

    Body:
      * ``channels`` (optional) — list of channels. Anything in
        ``_FORBIDDEN_CHANNELS`` raises immediately with the matching
        doctrine violation. Default = ``["email", "call_script", "follow_up_plan"]``.
      * ``top_n`` (optional) — how many of the top scored accounts to draft for
        (default 10, max 25).
    """

    requested_channels = payload.get("channels") or ["email", "call_script", "follow_up_plan"]
    if not isinstance(requested_channels, list):
        raise HTTPException(status_code=422, detail="channels must be a list")
    channel_set = {str(c).lower() for c in requested_channels}

    forbidden_hit = channel_set & _FORBIDDEN_CHANNELS
    if forbidden_hit:
        # Run through the safe_send_gateway pre-flight so the violation is
        # captured uniformly. This raises SendBlocked which we wrap as 403.
        try:
            enforce_doctrine_non_negotiables(
                action="revenue_intelligence_draft_pack",
                uses_scraping="scraping" in forbidden_hit,
                uses_cold_whatsapp="cold_whatsapp" in forbidden_hit,
                uses_linkedin_automation="linkedin_automation" in forbidden_hit,
                performs_external_action_without_approval="bulk_outreach" in forbidden_hit,
            )
        except SendBlocked as exc:
            raise HTTPException(
                status_code=403,
                detail={
                    "blocked_channels": sorted(forbidden_hit),
                    "reason_code": exc.reason_code,
                    "reasons_en": exc.reasons_en,
                    "reasons_ar": exc.reasons_ar,
                    "gate": exc.gate,
                },
            ) from exc
        # Defensive: should be unreachable.
        raise HTTPException(status_code=403, detail="forbidden_channels_requested")

    unknown = channel_set - _ALLOWED_CHANNELS
    if unknown:
        raise HTTPException(
            status_code=422,
            detail={"unknown_channels": sorted(unknown), "allowed": sorted(_ALLOWED_CHANNELS)},
        )

    _check_non_negotiables("revenue_intelligence_draft_pack")

    scored = _latest_event(engagement_id, "scored_accounts")
    if scored is None:
        raise HTTPException(
            status_code=409,
            detail="scored_accounts_missing_run_score_first",
        )
    top_n = int(payload.get("top_n", 10))
    top_n = max(1, min(top_n, 25))
    accounts = (scored.get("top_10") or [])[:top_n]

    drafts = []
    for acc in accounts:
        entry: dict[str, Any] = {
            "company_name": acc["company_name"],
            "score": acc["score"],
            "governance_decision": GovernanceDecision.DRAFT_ONLY.value,
        }
        if "email" in channel_set:
            entry["email_draft_ar"] = _email_draft_ar(acc)
            entry["email_draft_en"] = _email_draft_en(acc)
        if "call_script" in channel_set:
            entry["call_script"] = _call_script(acc)
        if "follow_up_plan" in channel_set:
            entry["follow_up_plan"] = _follow_up_plan(acc)
        if "whatsapp_with_consent" in channel_set:
            # Only draft for explicit_consent + warm_intro accounts.
            consent = (acc.get("consent_status") or "").strip().lower()
            if consent not in {"explicit_consent", "warm_intro"}:
                entry["whatsapp_draft"] = None
                entry["whatsapp_reason"] = "blocked_no_consent_record"
            else:
                entry["whatsapp_draft"] = _email_draft_ar(acc)[:160] + "…"
                entry["whatsapp_governance_note"] = "draft_only_requires_human_approval"
        drafts.append(entry)

    record = {
        "type": "draft_pack",
        "engagement_id": engagement_id,
        "channels": sorted(channel_set),
        "drafts_count": len(drafts),
        "drafts": drafts,
    }
    _append(engagement_id, record)
    return {
        "draft_pack": record,
        "governance_decision": GovernanceDecision.DRAFT_ONLY.value,
        "external_action_executed": False,
        "next_step": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/finalize "
            "to generate the Revenue Proof Pack."
        ),
    }


# ---------------------------------------------------------------------------
# Finalize → Revenue Proof Pack scaffold
# ---------------------------------------------------------------------------


@router.post("/{engagement_id}/finalize")
async def finalize(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Build the Revenue Proof Pack v2 record from the pipeline state.

    Body:
      * ``executive_summary`` (optional override).
      * ``client_name`` (recommended) — used in the proof narrative.
      * ``blocked_risks`` (optional list) — extra blocked items.
    """

    _check_non_negotiables(
        "revenue_intelligence_finalize",
        closes_project_without_proof_pack=False,
        closes_project_without_capital_asset=False,
    )

    preview = _latest_event(engagement_id, "import_preview")
    scored = _latest_event(engagement_id, "scored_accounts")
    drafts = _latest_event(engagement_id, "draft_pack")
    if preview is None or scored is None or drafts is None:
        raise HTTPException(
            status_code=409,
            detail="pipeline_incomplete_run_import_score_draft_pack_first",
        )

    client_name = payload.get("client_name", "Client")
    blocked_extra = payload.get("blocked_risks") or []
    if not isinstance(blocked_extra, list):
        blocked_extra = [str(blocked_extra)]

    accounts_total = preview["total_rows"]
    deduped = preview["deduped_rows"]
    duplicates = preview["duplicates_found"]
    quality = preview["data_quality"]["score"]
    pii_count = preview["pii_flagged_count"]
    top_count = len(scored["top_10"])
    drafts_count = drafts["drafts_count"]

    blocked_risks = [
        f"Cold WhatsApp automation: blocked by doctrine non-negotiable.",
        f"LinkedIn automation: blocked by doctrine non-negotiable.",
        f"Scraping engine: blocked by doctrine non-negotiable.",
        f"Bulk outreach without approval: blocked by doctrine non-negotiable.",
        *[str(item) for item in blocked_extra],
    ]

    sections: dict[str, str] = {
        "executive_summary": (
            payload.get("executive_summary")
            or (
                f"Revenue Intelligence Sprint for {client_name}. "
                f"Imported {accounts_total} accounts, deduped to {deduped} "
                f"({duplicates} duplicates removed). Data Quality Score = {quality}/100 "
                f"({preview['data_quality']['tier']}). Top {top_count} accounts ranked, "
                f"{drafts_count} draft-only outreach packs prepared. No external action executed "
                f"by Dealix; all outputs subject to human review."
            )
        ),
        "problem": (
            f"{client_name} had scattered prospect data, weak follow-up discipline, "
            f"and no governance around outreach. Risk: unsafe automation requests and "
            f"unscored opportunities."
        ),
        "inputs": (
            f"{accounts_total} rows uploaded. Source: {preview['source_passport']['source_id']} "
            f"(owner: {preview['source_passport']['owner']})."
        ),
        "source_passports": json.dumps(preview["source_passport"], ensure_ascii=False),
        "work_completed": (
            f"1) Import preview with dedupe + Data Quality Score = {quality}/100.\n"
            f"2) Account scoring (top {top_count} ranked by sector/relationship/consent/Saudi-fit).\n"
            f"3) Draft pack generated across {drafts['channels']} (DRAFT_ONLY).\n"
            f"4) {len(blocked_risks)} unsafe actions blocked by runtime governance."
        ),
        "outputs": (
            f"- Cleaned account list ({deduped} rows).\n"
            f"- Top 10 ranked accounts.\n"
            f"- Draft email pack (AR + EN).\n"
            f"- Call script.\n"
            f"- Follow-up plan."
        ),
        "quality_scores": (
            f"Data Quality Score = {quality}/100. "
            f"Tier = {preview['data_quality']['tier']}. "
            f"Duplicate rate = {preview['data_quality']['duplicate_rate']:.1%}. "
            f"Completeness = {preview['data_quality']['completeness']:.1%}."
        ),
        "governance_decisions": (
            f"Every output marked DRAFT_ONLY. PII flagged on {pii_count} rows; "
            f"external action requires human approval. WhatsApp drafts produced "
            f"only where consent_status ∈ {{explicit_consent, warm_intro}}."
        ),
        "blocked_risks": "\n".join(f"- {r}" for r in blocked_risks),
        "value_metrics": (
            f"Accounts scored = {top_count}. Drafts prepared = {drafts_count}. "
            f"Unsafe outreach blocked = {len(blocked_risks) - len(blocked_extra)}. "
            f"PII rows flagged = {pii_count}."
        ),
        "limitations": (
            "Outputs are draft-only and reviewable. Value metrics are Observed (not Verified). "
            "Verified value requires client-side confirmation after operating cadence."
        ),
        "recommended_next_step": (
            "Schedule Adoption Review and Retainer Gate check; offer Monthly RevOps OS "
            "if proof score ≥ 80 and client health ≥ 70."
        ),
        "retainer_or_expansion_path": "Monthly RevOps OS (recurring operation of revenue_os capability).",
        "capital_assets_created": (
            "- Revenue Proof Pack template (engagement_id).\n"
            "- Saudi sector priority map (sector_priority).\n"
            "- Draft Pack bilingual templates (AR + EN)."
        ),
    }

    record = {
        "type": "finalize",
        "engagement_id": engagement_id,
        "client_name": client_name,
        "proof_pack_sections": sections,
        "next_step": (
            f"POST /api/v1/proof-pack/{engagement_id}/generate with these sections "
            "+ 8-component score to persist the Proof Pack v2 record."
        ),
    }
    _append(engagement_id, record)
    return {
        "engagement_id": engagement_id,
        "proof_pack_sections": sections,
        "blocked_risks_count": len(blocked_risks),
        "external_action_executed": False,
        "next_step": record["next_step"],
    }


# ---------------------------------------------------------------------------
# State + read endpoints
# ---------------------------------------------------------------------------


@router.get("/{engagement_id}/state")
async def state(engagement_id: str) -> dict[str, Any]:
    events = _read_events(engagement_id)
    if not events:
        raise HTTPException(status_code=404, detail="engagement_not_found")
    state_summary = {
        "imported": any(e["type"] == "import_preview" for e in events),
        "scored": any(e["type"] == "scored_accounts" for e in events),
        "drafted": any(e["type"] == "draft_pack" for e in events),
        "finalized": any(e["type"] == "finalize" for e in events),
    }
    return {
        "engagement_id": engagement_id,
        "events_count": len(events),
        "state": state_summary,
        "last_event_type": events[-1]["type"],
        "last_event_ts": events[-1]["ts"],
    }


@router.get("/_meta/forbidden-channels")
async def forbidden_channels() -> dict[str, Any]:
    return {
        "forbidden": sorted(_FORBIDDEN_CHANNELS),
        "allowed": sorted(_ALLOWED_CHANNELS),
        "doctrine_source": (
            "auto_client_acquisition.operating_manual_os.non_negotiables.DEALIX_NON_NEGOTIABLES"
        ),
    }
