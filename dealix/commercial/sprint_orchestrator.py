"""Revenue Intelligence Sprint Orchestrator — 7-day commercial engagement.

Orchestrates the 499 SAR Revenue Intelligence Sprint. Each day calls the
appropriate canonical module and returns a structured :class:`SprintDayResult`
with bilingual (ar/en) output.

Day 1: Source Passport — audit lead sources
Day 2: Data Quality Score (DQ 0-100 per source)
Day 3: Account scoring (top 10 by revenue potential)
Day 4: Draft Pack (3 WhatsApp drafts, 1 email sequence, 1 proposal)
Day 5: Governance review (founder approval gate)
Day 6: Proof Pack assembly
Day 7: Capital asset registration + retainer eligibility

Each day output is a plain JSON-serialisable dict so it can be stored
in the operational stream without extra marshalling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

# ---------------------------------------------------------------------------
# Context / Result schemas
# ---------------------------------------------------------------------------


@dataclass
class SprintContext:
    """Input context for a single sprint run."""

    engagement_id: str
    customer_id: str
    customer_name: str = ""
    customer_name_ar: str = ""
    sector: str = ""
    city: str = ""
    # Day-1 source audit data: list of {source_type, row_count, ...} dicts
    sources: list[dict[str, Any]] = field(default_factory=list)
    # Day-2/3 rows for DQ computation and account scoring
    rows: list[dict[str, Any]] = field(default_factory=list)
    # Day-4 context for draft generation
    pain_summary: str = ""
    pain_summary_ar: str = ""
    # Day-5 governance state
    founder_approved: bool = False
    # Day-6 proof evidence
    proof_evidence: dict[str, str] = field(default_factory=dict)
    # Day-7 capital/retainer signals
    workflow_owner_present: bool = False
    proof_score_override: float | None = None
    adoption_score_override: float | None = None


@dataclass
class SprintDayResult:
    """Output from a single sprint day execution."""

    day: int
    title_en: str
    title_ar: str
    status: str  # complete | pending | blocked
    output: dict[str, Any] = field(default_factory=dict)
    governance_decision: str = "ALLOW_WITH_REVIEW"
    errors: list[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "day": self.day,
            "title_en": self.title_en,
            "title_ar": self.title_ar,
            "status": self.status,
            "output": self.output,
            "governance_decision": self.governance_decision,
            "errors": self.errors,
            "generated_at": self.generated_at,
        }


# ---------------------------------------------------------------------------
# Day runners — one pure function per day
# ---------------------------------------------------------------------------

_REQUIRED_KEYS: tuple[str, ...] = ("company_name", "sector", "city")


def _run_day_1(ctx: SprintContext) -> SprintDayResult:
    """Source Passport — audit all declared lead sources."""
    from auto_client_acquisition.data_os import SourcePassport, source_passport_valid_for_ai
    from auto_client_acquisition.governance_os import GovernanceDecision

    source_audits: list[dict[str, Any]] = []
    has_any_error = False

    for src in ctx.sources or []:
        passport = SourcePassport(
            source_id=str(src.get("source_id") or src.get("source_type", "")),
            source_type=str(src.get("source_type", "unknown")),
            owner=str(src.get("owner", ctx.customer_id)),
            allowed_use=frozenset(src.get("allowed_use", ["internal_analysis"])),
            contains_pii=bool(src.get("contains_pii", False)),
            sensitivity=str(src.get("sensitivity", "medium")),
            retention_policy=str(src.get("retention_policy", "project_duration")),
            ai_access_allowed=bool(src.get("ai_access_allowed", True)),
            external_use_allowed=bool(src.get("external_use_allowed", False)),
        )
        is_valid, errors = source_passport_valid_for_ai(passport)
        audit: dict[str, Any] = {
            "source_type": src.get("source_type", "unknown"),
            "source_id": passport.source_id,
            "valid": is_valid,
            "errors": list(errors),
        }
        if not is_valid:
            has_any_error = True
        source_audits.append(audit)

    gov = GovernanceDecision.ALLOW if not has_any_error else GovernanceDecision.REQUIRE_APPROVAL

    output: dict[str, Any] = {
        "sources_audited": len(source_audits),
        "all_passports_valid": not has_any_error,
        "source_audits": source_audits,
        "summary_en": (
            f"Audited {len(source_audits)} sources. "
            + ("All passports valid." if not has_any_error else "Some passports require approval.")
        ),
        "summary_ar": (
            f"تم تدقيق {len(source_audits)} مصدر. "
            + ("جميع جوازات المصدر صالحة." if not has_any_error else "بعض جوازات المصدر تحتاج موافقة.")
        ),
    }
    return SprintDayResult(
        day=1,
        title_en="Source Passport Audit",
        title_ar="تدقيق جواز المصدر",
        status="complete" if not has_any_error else "pending",
        output=output,
        governance_decision=gov.value,
    )


def _run_day_2(ctx: SprintContext) -> SprintDayResult:
    """Data Quality Score — compute DQ per source."""
    from auto_client_acquisition.data_os import compute_dq

    rows = ctx.rows or []
    columns = list({k for row in rows for k in row}) if rows else list(_REQUIRED_KEYS)

    # One source passport per source type observed in rows.
    source_types: list[str] = list(
        {str(row.get("source", "unknown")) for row in rows} or ["unknown"]
    )

    dq_by_source: list[dict[str, Any]] = []
    for src_type in source_types:
        src_rows = [r for r in rows if str(r.get("source", "unknown")) == src_type] or rows
        dq = compute_dq(
            src_rows,
            columns=columns,
            has_valid_passport=bool(ctx.sources),
            required_keys=_REQUIRED_KEYS,
        )
        dq_by_source.append(
            {
                "source_type": src_type,
                "row_count": len(src_rows),
                "dq_score": dq.overall,
                "completeness": dq.completeness,
                "duplicate_inverse": dq.duplicate_inverse,
                "format_consistency": dq.format_consistency,
                "source_clarity": dq.source_clarity,
            }
        )

    overall_dq = (
        sum(d["dq_score"] for d in dq_by_source) / len(dq_by_source) if dq_by_source else 0.0
    )

    output: dict[str, Any] = {
        "total_rows": len(rows),
        "sources_scored": len(dq_by_source),
        "overall_dq": round(overall_dq, 1),
        "dq_by_source": dq_by_source,
        "summary_en": f"Overall Data Quality Score: {overall_dq:.0f}/100 across {len(rows)} rows.",
        "summary_ar": f"درجة جودة البيانات الإجمالية: {overall_dq:.0f}/100 عبر {len(rows)} سجل.",
    }
    return SprintDayResult(
        day=2,
        title_en="Data Quality Score",
        title_ar="درجة جودة البيانات",
        status="complete",
        output=output,
        governance_decision="ALLOW",
    )


def _run_day_3(ctx: SprintContext) -> SprintDayResult:
    """Account scoring — rank top 10 accounts by revenue potential."""
    from auto_client_acquisition.sales_os import ICPDimensions, icp_score

    rows = ctx.rows or []
    scored: list[dict[str, Any]] = []

    for row in rows:
        sector_val = str(row.get("sector", ctx.sector or ""))
        # ICPDimensions expects 0-100 int signals.
        dims = ICPDimensions(
            b2b_service_fit=int(row.get("b2b_service_fit", int(float(row.get("sector_fit", 0.5)) * 100))),
            data_maturity=int(row.get("data_maturity", 50)),
            governance_posture=int(row.get("governance_posture", 50)),
            budget_signal=int(row.get("budget_signal", int(bool(row.get("has_budget", False))) * 70)),
            decision_velocity=int(row.get("decision_velocity", int(float(row.get("urgency", 0.5)) * 100))),
        )
        s = icp_score(dims)
        scored.append(
            {
                "company_name": str(row.get("company_name", "")),
                "sector": sector_val,
                "icp_score": s,
                "row": row,
            }
        )

    top_10 = sorted(scored, key=lambda x: x["icp_score"], reverse=True)[:10]

    output: dict[str, Any] = {
        "total_accounts": len(rows),
        "top_10": [
            {
                "rank": i + 1,
                "company_name": a["company_name"],
                "sector": a["sector"],
                "icp_score": a["icp_score"],
            }
            for i, a in enumerate(top_10)
        ],
        "summary_en": f"Ranked {len(rows)} accounts. Top 10 by ICP score selected.",
        "summary_ar": f"تم تصنيف {len(rows)} حساب. تم اختيار أعلى 10 بمعيار ICP.",
    }
    return SprintDayResult(
        day=3,
        title_en="Account Scoring",
        title_ar="تصنيف الحسابات",
        status="complete",
        output=output,
        governance_decision="ALLOW",
    )


def _run_day_4(ctx: SprintContext) -> SprintDayResult:
    """Draft Pack — generate 3 WhatsApp drafts, 1 email sequence, 1 proposal."""
    from auto_client_acquisition.governance_os import (
        GovernanceDecision,
        audit_draft_text,
        policy_check_draft,
    )
    from auto_client_acquisition.sales_os.proposal_renderer import ProposalContext, render_proposal

    customer = ctx.customer_name or "العميل"
    customer_ar = ctx.customer_name_ar or customer
    pain = ctx.pain_summary or "revenue growth challenges"
    pain_ar = ctx.pain_summary_ar or "تحديات نمو الإيراد"
    sector = ctx.sector or "b2b"

    whatsapp_drafts = [
        {
            "draft_id": f"wa_draft_1_{ctx.engagement_id}",
            "lang": "ar",
            "body": (
                f"مرحباً {customer_ar}، هل تواجهون {pain_ar}؟ "
                f"لدينا Sprint تشخيصي يساعدكم خلال 7 أيام."
            ),
            "channel": "whatsapp",
            "status": "draft_only",
        },
        {
            "draft_id": f"wa_draft_2_{ctx.engagement_id}",
            "lang": "ar",
            "body": (
                f"فريق {customer_ar}، نخصص Sprint تشخيصي لقطاع {sector} يُنتج "
                f"Proof Pack كاملاً في 7 أيام بـ 499 ريال."
            ),
            "channel": "whatsapp",
            "status": "draft_only",
        },
        {
            "draft_id": f"wa_draft_3_{ctx.engagement_id}",
            "lang": "en",
            "body": (
                f"Hi {customer}, we run a 7-day Revenue Intelligence Sprint for {sector} "
                f"businesses — complete with a Proof Pack at 499 SAR."
            ),
            "channel": "whatsapp",
            "status": "draft_only",
        },
    ]

    email_sequence = {
        "sequence_id": f"email_seq_{ctx.engagement_id}",
        "emails": [
            {
                "step": 1,
                "subject_en": f"Revenue Intelligence Sprint for {customer}",
                "subject_ar": f"Sprint ذكاء الإيراد لـ {customer_ar}",
                "body_en": (
                    f"We've identified {pain}. "
                    f"Our 7-day sprint delivers measurable results with full Proof Pack."
                ),
                "body_ar": (
                    f"رصدنا {pain_ar}. "
                    f"Sprint الـ7 أيام يُنتج نتائج قابلة للقياس مع Proof Pack كامل."
                ),
            },
        ],
        "status": "draft_only",
    }

    proposal_ctx = ProposalContext(
        customer_name=customer,
        customer_handle=ctx.customer_id,
        sector=sector,
        city=ctx.city or "Riyadh",
        engagement_id=ctx.engagement_id,
        price_sar=499,
        delivery_days=7,
    )
    proposal_md = render_proposal(proposal_ctx)

    # Governance gate on draft content.
    all_texts = [d["body"] for d in whatsapp_drafts] + [proposal_md]
    governance_checks = [policy_check_draft(t) for t in all_texts]
    all_allowed = all(r.allowed for r in governance_checks)
    gov = GovernanceDecision.ALLOW if all_allowed else GovernanceDecision.DRAFT_ONLY

    output: dict[str, Any] = {
        "whatsapp_drafts": whatsapp_drafts,
        "email_sequence": email_sequence,
        "proposal_preview_md": proposal_md[:500] + "..." if len(proposal_md) > 500 else proposal_md,
        "all_drafts_passed_governance": all_allowed,
        "summary_en": (
            f"Generated {len(whatsapp_drafts)} WhatsApp drafts + 1 email sequence + 1 proposal. "
            + ("All passed governance." if all_allowed else "Some items flagged for review.")
        ),
        "summary_ar": (
            f"تم إنشاء {len(whatsapp_drafts)} مسودة WhatsApp + تسلسل إيميل + مقترح. "
            + ("جميعها اجتازت الحوكمة." if all_allowed else "بعض العناصر تحتاج مراجعة.")
        ),
    }
    return SprintDayResult(
        day=4,
        title_en="Draft Pack",
        title_ar="حزمة المسوّدات",
        status="complete" if all_allowed else "pending",
        output=output,
        governance_decision=gov.value,
    )


def _run_day_5(ctx: SprintContext) -> SprintDayResult:
    """Governance review — founder approval gate."""
    from auto_client_acquisition.governance_os import GovernanceDecision

    if not ctx.founder_approved:
        return SprintDayResult(
            day=5,
            title_en="Governance Review",
            title_ar="مراجعة الحوكمة",
            status="blocked",
            output={
                "approved": False,
                "summary_en": "Awaiting founder approval. No output will be sent until confirmed.",
                "summary_ar": "في انتظار موافقة المؤسس. لن يُرسَل أي مخرج حتى التأكيد.",
            },
            governance_decision=GovernanceDecision.REQUIRE_APPROVAL.value,
            errors=["founder_approval_required"],
        )

    output: dict[str, Any] = {
        "approved": True,
        "approved_by": "founder",
        "approved_at": datetime.now(UTC).isoformat(),
        "summary_en": "Founder approval confirmed. Sprint outputs cleared for client delivery.",
        "summary_ar": "تم تأكيد موافقة المؤسس. مخرجات Sprint جاهزة للتسليم للعميل.",
    }
    return SprintDayResult(
        day=5,
        title_en="Governance Review",
        title_ar="مراجعة الحوكمة",
        status="complete",
        output=output,
        governance_decision=GovernanceDecision.ALLOW.value,
    )


def _run_day_6(ctx: SprintContext) -> SprintDayResult:
    """Proof Pack assembly — collect L0-L4 evidence and compute score."""
    from auto_client_acquisition.proof_os import (
        build_empty_proof_pack_v2,
        merge_proof_pack_v2,
        proof_pack_completeness_score,
        proof_strength_band,
    )

    base_pack = build_empty_proof_pack_v2()
    # Merge user-supplied evidence (keys must match PROOF_PACK_V2_SECTIONS).
    evidence = ctx.proof_evidence or {}
    merged = merge_proof_pack_v2(base_pack, evidence)

    score = proof_pack_completeness_score(merged)
    band = proof_strength_band(score)

    output: dict[str, Any] = {
        "proof_pack": merged,
        "completeness_score": score,
        "strength_band": band,
        "summary_en": f"Proof Pack assembled. Completeness: {score}/100 ({band}).",
        "summary_ar": f"تم تجميع Proof Pack. الاكتمال: {score}/100 ({band}).",
    }
    return SprintDayResult(
        day=6,
        title_en="Proof Pack Assembly",
        title_ar="تجميع حزمة الإثبات",
        status="complete",
        output=output,
        governance_decision="ALLOW",
    )


def _run_day_7(ctx: SprintContext) -> SprintDayResult:
    """Capital asset registration + retainer eligibility check."""
    from auto_client_acquisition.adoption_os.adoption_score import compute
    from auto_client_acquisition.adoption_os.retainer_readiness import evaluate
    from auto_client_acquisition.capital_os import CapitalAssetType, add_asset, list_assets

    # Register capital assets produced during the sprint.
    asset = add_asset(
        customer_id=ctx.customer_id,
        engagement_id=ctx.engagement_id,
        asset_type=CapitalAssetType.PROOF_EXAMPLE,
        owner="founder",
        reusable=True,
        asset_ref=f"sprint_{ctx.engagement_id}",
        notes=f"Revenue Intelligence Sprint assets for {ctx.customer_name or ctx.customer_id}",
    )

    assets = list_assets(customer_id=ctx.customer_id)

    # Adoption score
    adoption_result = compute(
        customer_id=ctx.customer_id,
        channels_enabled=1,
        integrations_connected=1,
        sectors_targeted=1,
        total_drafts_lifetime=4,
        logins_last_30d=5,
        drafts_approved_last_30d=1,
        replies_acted_on_last_30d=1,
    )
    adoption_s = ctx.adoption_score_override if ctx.adoption_score_override is not None else adoption_result.score
    proof_s = ctx.proof_score_override if ctx.proof_score_override is not None else 60.0

    # Retainer eligibility
    retainer = evaluate(
        customer_id=ctx.customer_id,
        adoption_score=adoption_s,
        proof_score=proof_s,
        workflow_owner_present=ctx.workflow_owner_present,
        governance_risk_controlled=True,
    )

    output: dict[str, Any] = {
        "capital_asset_id": asset.asset_id,
        "total_assets_registered": len(assets),
        "adoption_score": adoption_s,
        "proof_score": proof_s,
        "retainer_eligible": retainer.eligible,
        "recommended_offer": retainer.recommended_offer,
        "retainer_gaps": retainer.gaps,
        "summary_en": (
            f"Capital asset registered. Adoption: {adoption_s:.0f}, Proof: {proof_s:.0f}. "
            + (
                f"Retainer eligible — recommended: {retainer.recommended_offer}."
                if retainer.eligible
                else f"Not yet eligible. Gaps: {', '.join(retainer.gaps)}."
            )
        ),
        "summary_ar": (
            f"تم تسجيل الأصل الرأسمالي. Adoption: {adoption_s:.0f}, Proof: {proof_s:.0f}. "
            + (
                f"مؤهَّل للـRetainer — المقترح: {retainer.recommended_offer}."
                if retainer.eligible
                else f"غير مؤهَّل بعد. الثغرات: {', '.join(retainer.gaps)}."
            )
        ),
    }
    return SprintDayResult(
        day=7,
        title_en="Capital Asset Registration & Retainer Eligibility",
        title_ar="تسجيل الأصل الرأسمالي وأهلية الـRetainer",
        status="complete",
        output=output,
        governance_decision="ALLOW",
    )


_DAY_RUNNERS = {
    1: _run_day_1,
    2: _run_day_2,
    3: _run_day_3,
    4: _run_day_4,
    5: _run_day_5,
    6: _run_day_6,
    7: _run_day_7,
}

# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


class SprintOrchestrator:
    """Orchestrates the 7-day Revenue Intelligence Sprint (499 SAR offer).

    Usage::

        ctx = SprintContext(
            engagement_id="eng_001",
            customer_id="acme",
            sources=[{"source_type": "crm", ...}],
            rows=[...],
        )
        orchestrator = SprintOrchestrator()
        result = orchestrator.run_day(1, ctx)
        # result.to_dict() → JSON-serialisable output
    """

    def run_day(self, day: int, context: SprintContext) -> SprintDayResult:
        """Execute a single sprint day.

        :param day: Day number 1-7.
        :param context: Full sprint context (may not be fully populated for early days).
        :raises ValueError: If day is outside 1-7.
        """
        if day not in _DAY_RUNNERS:
            raise ValueError(f"Sprint day must be 1-7, got {day!r}")
        runner = _DAY_RUNNERS[day]
        try:
            return runner(context)
        except Exception as exc:  # noqa: BLE001
            return SprintDayResult(
                day=day,
                title_en=f"Day {day}",
                title_ar=f"اليوم {day}",
                status="blocked",
                output={},
                governance_decision="BLOCK",
                errors=[str(exc)],
            )

    def run_all(self, context: SprintContext) -> list[SprintDayResult]:
        """Run all 7 days sequentially. Day 5 blocks if founder_approved is False."""
        return [self.run_day(d, context) for d in range(1, 8)]


__all__ = [
    "SprintContext",
    "SprintDayResult",
    "SprintOrchestrator",
]
