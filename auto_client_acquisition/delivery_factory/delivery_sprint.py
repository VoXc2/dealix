"""Sprint delivery orchestrator — the 10-step productized runbook.

Walks a customer through the 7-Day Revenue Intelligence Sprint, invoking
the canonical modules at each step. Records to value_ledger,
capital_ledger, friction_log. Builds the Proof Pack at the end.

Every step is a pure-function invocation; the orchestrator collects
intermediate results and surfaces them so the founder reviews before
proceeding to the next step. NO external sends.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SprintStep:
    name: str
    status: str  # pending | ran | review_required | blocked | skipped
    output: dict[str, Any] = field(default_factory=dict)
    governance_decision: str = ""
    notes: str = ""


@dataclass
class SprintRun:
    engagement_id: str
    customer_id: str
    started_at: str
    steps: list[SprintStep] = field(default_factory=list)
    proof_pack: dict[str, Any] | None = None
    proof_score: float = 0.0
    proof_tier: str = ""
    capital_assets_registered: list[str] = field(default_factory=list)
    retainer_eligible: bool = False
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "engagement_id": self.engagement_id,
            "customer_id": self.customer_id,
            "started_at": self.started_at,
            "steps": [asdict(s) for s in self.steps],
            "proof_pack": self.proof_pack,
            "proof_score": self.proof_score,
            "proof_tier": self.proof_tier,
            "capital_assets_registered": list(self.capital_assets_registered),
            "retainer_eligible": self.retainer_eligible,
            "governance_decision": self.governance_decision,
        }


def _safe(step_name: str, fn, **kwargs) -> SprintStep:
    """Run a step; capture exceptions as friction events."""
    try:
        out = fn(**kwargs)
        return SprintStep(
            name=step_name,
            status="ran",
            output=out if isinstance(out, dict) else {"value": out},
        )
    except Exception as exc:  # noqa: BLE001
        try:
            from auto_client_acquisition.friction_log.store import emit
            emit(
                customer_id=kwargs.get("customer_id", "_unknown"),
                kind="schema_failure",
                severity="med",
                workflow_id="delivery_sprint",
                notes=f"step:{step_name}:exception:{type(exc).__name__}",
            )
        except Exception:
            pass
        return SprintStep(
            name=step_name,
            status="blocked",
            output={"error": f"{type(exc).__name__}: {exc}"},
        )


def step1_kickoff(*, customer_id: str, engagement_id: str, source_passport: dict | None) -> dict:
    """Day 1: Source Passport agreement."""
    from auto_client_acquisition.data_os.source_passport import (
        SourcePassport,
        validate,
    )
    if not source_passport:
        return {
            "passport_provided": False,
            "validation": {"is_valid": False, "reasons": ("no_passport",)},
        }
    sp = SourcePassport(**source_passport)
    result = validate(sp)
    return {
        "passport_provided": True,
        "validation": {
            "is_valid": result.is_valid,
            "reasons": list(result.reasons),
            "missing": list(result.missing),
        },
    }


def step2_data_quality(*, customer_id: str, engagement_id: str, raw_csv: str | bytes = b"") -> dict:
    """Day 2: Import preview + DQ score."""
    from auto_client_acquisition.data_os.data_quality_score import compute_dq_from_preview
    from auto_client_acquisition.data_os.import_preview import preview
    raw = raw_csv.encode("utf-8") if isinstance(raw_csv, str) else raw_csv
    if not raw:
        return {"row_count": 0, "dq": 0, "skipped": "no_csv_provided"}
    p = preview(raw)
    dq = compute_dq_from_preview(preview=p, duplicates_found=0)
    return {
        "row_count": p.row_count,
        "columns": list(p.columns),
        "pii_columns": list(p.pii_columns),
        "dq_overall": dq.overall,
        "dq_breakdown": {
            "completeness": dq.completeness,
            "duplicate_inverse": dq.duplicate_inverse,
            "format_consistency": dq.format_consistency,
            "source_clarity": dq.source_clarity,
        },
    }


def step3_account_scoring(*, customer_id: str, engagement_id: str, accounts: list[dict] | None = None) -> dict:
    """Day 3: Account scoring → top 10. Heuristic if revenue_os.account_scoring
    is not available in this environment.
    """
    accounts = accounts or []
    scored: list[dict] = []
    for i, acc in enumerate(accounts):
        score = 0
        if acc.get("relationship_status") in ("warm", "active"):
            score += 30
        if acc.get("sector"):
            score += 15
        if acc.get("city") in ("Riyadh", "Jeddah", "Dammam", "Khobar", "Mecca", "Medina"):
            score += 15
        if acc.get("last_interaction"):
            score += 20
        if acc.get("notes"):
            score += 10
        if acc.get("company_name"):
            score += 10
        scored.append({
            "rank": 0,
            "company_name": acc.get("company_name", f"acct_{i}"),
            "score": score,
            "reasons": _score_reasons(acc, score),
        })
    scored.sort(key=lambda x: x["score"], reverse=True)
    for i, s in enumerate(scored, start=1):
        s["rank"] = i
    return {"top_10": scored[:10], "total_scored": len(scored)}


def _score_reasons(acc: dict, score: int) -> list[str]:
    reasons = []
    if acc.get("relationship_status") in ("warm", "active"):
        reasons.append("warm_relationship")
    if acc.get("last_interaction"):
        reasons.append("recent_interaction")
    if score < 50:
        reasons.append("low_signal_overall")
    return reasons


def step4_draft_pack(*, customer_id: str, engagement_id: str, top_accounts: list[dict]) -> dict:
    """Day 4: Generate AR + EN draft outline. Real LLM call deferred to
    the founder review step — this orchestrator only structures the brief.
    """
    return {
        "ar_drafts_outlined": [
            {
                "account": acc["company_name"],
                "outline_ar": (
                    f"رسالة افتتاحية لـ{acc['company_name']} — تركز على القيمة "
                    "وتترك القرار للعميل بدون أي ادعاءات مضمونة."
                ),
                "outline_en": (
                    f"Opening note for {acc['company_name']} — value-led, decision "
                    "left to the customer, no guaranteed claims."
                ),
                "governance_decision": "draft_only",
            }
            for acc in top_accounts[:10]
        ],
        "total_outlines": min(10, len(top_accounts)),
    }


def step5_governance_review(*, customer_id: str, engagement_id: str, drafts: list[dict]) -> dict:
    """Day 4 cont'd: Run governance_os.decide on every draft."""
    from auto_client_acquisition.governance_os.runtime_decision import decide

    reviews = []
    for d in drafts:
        outline_text = " ".join([d.get("outline_ar", ""), d.get("outline_en", "")])
        result = decide(
            action="generate_draft",
            context={
                "text": outline_text,
                "channel": "email",
                "is_cold": False,
            },
        )
        reviews.append({
            "account": d.get("account", "?"),
            "decision": result.decision.value,
            "reasons": list(result.reasons),
        })
    return {
        "reviews": reviews,
        "summary": _governance_summary(reviews),
    }


def _governance_summary(reviews: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for r in reviews:
        d = r["decision"]
        out[d] = out.get(d, 0) + 1
    return out


def step6_proof_pack(
    *,
    customer_id: str,
    engagement_id: str,
    passport: dict | None,
    dq_score: float,
    governance_summary: dict[str, int],
    work_completed_summary: str,
    outputs_summary: str = "",
    problem_summary: str = "",
) -> dict:
    """Day 5: Proof Pack assembly."""
    from auto_client_acquisition.data_os.source_passport import SourcePassport
    from auto_client_acquisition.proof_os.proof_pack import assemble

    governance_events = [
        {"decision": d, "count": n} for d, n in governance_summary.items()
    ]
    sp = SourcePassport(**passport) if passport else None
    pack = assemble(
        engagement_id=engagement_id,
        customer_id=customer_id,
        source_passport=sp,
        dq_score=dq_score,
        value_events=[],
        governance_events=governance_events,
        work_completed=work_completed_summary or "10-step sprint executed",
        problem=problem_summary or "(provided in kickoff)",
        outputs_summary=outputs_summary or "ranked top 10 + governance-reviewed drafts",
        next_step="founder review and handoff",
    )
    return pack.to_dict()


def step7_capital_assets(
    *, customer_id: str, engagement_id: str, asset_specs: list[dict] | None = None
) -> dict:
    """Day 7: Register capital assets — at least 1 reusable artifact."""
    from auto_client_acquisition.capital_os.capital_ledger import add_asset

    specs = asset_specs or [
        {
            "asset_type": "scoring_rule",
            "owner": customer_id,
            "asset_ref": f"sprint_{engagement_id}_scoring_v1",
            "notes": "Default sector + relationship-status scoring rule used in this sprint.",
        }
    ]
    registered = []
    for s in specs:
        try:
            a = add_asset(
                engagement_id=engagement_id,
                customer_id=customer_id,
                asset_type=s["asset_type"],
                owner=s.get("owner", customer_id),
                reusable=s.get("reusable", True),
                asset_ref=s.get("asset_ref", ""),
                notes=s.get("notes", ""),
            )
            registered.append(a.asset_id)
        except Exception:  # noqa: BLE001
            continue
    return {"registered": registered, "count": len(registered)}


def step8_retainer_check(
    *,
    customer_id: str,
    engagement_id: str,
    proof_score: float,
    workflow_owner_present: bool = True,
    governance_risk_controlled: bool = True,
) -> dict:
    """Day 7: Check retainer eligibility."""
    from auto_client_acquisition.adoption_os.adoption_score import compute as compute_adoption
    from auto_client_acquisition.adoption_os.retainer_readiness import evaluate

    adoption = compute_adoption(customer_id=customer_id)
    readiness = evaluate(
        customer_id=customer_id,
        adoption_score=adoption.score,
        proof_score=proof_score,
        workflow_owner_present=workflow_owner_present,
        governance_risk_controlled=governance_risk_controlled,
    )
    return {
        "adoption_score": adoption.to_dict(),
        "retainer_readiness": readiness.to_dict(),
        "eligible": readiness.eligible,
        "recommended_offer": readiness.recommended_offer,
    }


def run_sprint(
    *,
    engagement_id: str,
    customer_id: str,
    source_passport: dict | None = None,
    raw_csv: str | bytes = b"",
    accounts: list[dict] | None = None,
    problem_summary: str = "",
    workflow_owner_present: bool = True,
) -> SprintRun:
    """End-to-end orchestrated run. Each step's output is captured.

    NOTE: this is a DRY orchestrator — it composes pure-function steps.
    The founder reviews intermediate outputs before proceeding in
    production. For tests, all steps run sequentially.
    """
    started = datetime.now(timezone.utc).isoformat()
    run = SprintRun(
        engagement_id=engagement_id,
        customer_id=customer_id,
        started_at=started,
    )

    # Step 1
    s1 = _safe("kickoff_source_passport", step1_kickoff,
               customer_id=customer_id, engagement_id=engagement_id,
               source_passport=source_passport)
    run.steps.append(s1)

    # Step 2
    s2 = _safe("data_quality", step2_data_quality,
               customer_id=customer_id, engagement_id=engagement_id, raw_csv=raw_csv)
    run.steps.append(s2)
    dq_score = float(s2.output.get("dq_overall", 0.0)) if s2.status == "ran" else 0.0

    # Step 3
    s3 = _safe("account_scoring", step3_account_scoring,
               customer_id=customer_id, engagement_id=engagement_id, accounts=accounts)
    run.steps.append(s3)
    top10 = s3.output.get("top_10", [])

    # Step 4 — outline drafts
    s4 = _safe("draft_pack_outline", step4_draft_pack,
               customer_id=customer_id, engagement_id=engagement_id, top_accounts=top10)
    run.steps.append(s4)
    drafts = s4.output.get("ar_drafts_outlined", [])

    # Step 5 — governance review
    s5 = _safe("governance_review", step5_governance_review,
               customer_id=customer_id, engagement_id=engagement_id, drafts=drafts)
    run.steps.append(s5)
    gov_summary = s5.output.get("summary", {})

    # Step 6 — proof pack
    s6 = _safe("proof_pack", step6_proof_pack,
               customer_id=customer_id, engagement_id=engagement_id,
               passport=source_passport, dq_score=dq_score,
               governance_summary=gov_summary,
               work_completed_summary=f"Imported {s2.output.get('row_count', 0)} rows; scored {s3.output.get('total_scored', 0)} accounts; reviewed {len(drafts)} draft outlines.",
               problem_summary=problem_summary)
    run.steps.append(s6)
    pack = s6.output if s6.status == "ran" else {}
    run.proof_pack = pack
    run.proof_score = float(pack.get("score", 0.0))
    run.proof_tier = pack.get("tier", "weak")

    # Step 7 — capital assets
    s7 = _safe("capital_assets", step7_capital_assets,
               customer_id=customer_id, engagement_id=engagement_id)
    run.steps.append(s7)
    run.capital_assets_registered = list(s7.output.get("registered", []))

    # Step 8 — retainer check
    s8 = _safe("retainer_check", step8_retainer_check,
               customer_id=customer_id, engagement_id=engagement_id,
               proof_score=run.proof_score,
               workflow_owner_present=workflow_owner_present)
    run.steps.append(s8)
    run.retainer_eligible = bool(s8.output.get("eligible", False))

    # Governance envelope on the whole sprint
    if any(s.status == "blocked" for s in run.steps):
        run.governance_decision = "needs_review"
    return run


__all__ = [
    "SprintRun",
    "SprintStep",
    "run_sprint",
    "step1_kickoff",
    "step2_data_quality",
    "step3_account_scoring",
    "step4_draft_pack",
    "step5_governance_review",
    "step6_proof_pack",
    "step7_capital_assets",
    "step8_retainer_check",
]
