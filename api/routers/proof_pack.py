"""Proof Pack — HTTP surface to generate the v2 14-section Proof Pack.

POST /api/v1/proof-pack/{engagement_id}/generate — build the Proof Pack
record from supplied components.

GET /api/v1/proof-pack/{engagement_id} — retrieve the persisted record
+ rendered Markdown.

GET /api/v1/proof-pack/{engagement_id}/render — get just the Markdown.

GET /api/v1/proof-pack/_score — POST a ProofComponentsV2 dict, get the
score and tier classification (used in sales tooling).

Doctrine bindings:
  * ``proof_architecture_os.proof_pack_v2`` — 14-section schema.
  * ``proof_architecture_os.proof_score_v2`` — 8-weight composite.
  * ``proof_architecture_os.value_ledger`` — typed value events.
  * ``proof_architecture_os.roi_discipline`` — Estimated/Observed/Verified.
  * ``operating_manual_os.proof_to_retainer`` — retainer-gate evaluation.
  * ``operating_manual_os.non_negotiables`` — pre-flight check.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.operating_manual_os.non_negotiables import (
    NonNegotiableCheck,
    check_action_against_non_negotiables,
)
from auto_client_acquisition.operating_manual_os.proof_to_retainer import (
    RETAINER_GATE_THRESHOLDS,
    RetainerGateInputs,
    evaluate_retainer_gate,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
    ProofPackV2,
)
from auto_client_acquisition.proof_architecture_os.proof_score_v2 import (
    PROOF_SCORE_V2_WEIGHTS,
    ProofComponentsV2,
    compute_proof_score_v2,
)

router = APIRouter(prefix="/api/v1/proof-pack", tags=["proof-pack"])

_STORE_PATH = Path(os.getenv("DEALIX_PROOF_PACK_STORE", "var/proof_packs.jsonl"))


def _persist(record: dict[str, Any]) -> None:
    _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _STORE_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def _load(engagement_id: str) -> dict[str, Any] | None:
    if not _STORE_PATH.exists():
        return None
    latest: dict[str, Any] | None = None
    with _STORE_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("engagement_id") == engagement_id:
                latest = rec  # last-write-wins for replays
    return latest


def _classify_tier(score: int) -> str:
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    if score >= 55:
        return "internal_learning"
    return "weak_proof"


def _render_markdown(record: dict[str, Any]) -> str:
    """Render a Proof Pack record into a stable Markdown bundle."""

    titles: dict[str, str] = {
        "executive_summary": "1. Executive Summary",
        "problem": "2. Problem",
        "inputs": "3. Inputs",
        "source_passports": "4. Source Passports",
        "work_completed": "5. Work Completed",
        "outputs": "6. Outputs",
        "quality_scores": "7. Quality Scores",
        "governance_decisions": "8. Governance Decisions",
        "blocked_risks": "9. Blocked Risks",
        "value_metrics": "10. Value Metrics",
        "limitations": "11. Limitations",
        "recommended_next_step": "12. Recommended Next Step",
        "retainer_or_expansion_path": "13. Retainer / Expansion Path",
        "capital_assets_created": "14. Capital Assets Created",
    }
    sections = record.get("sections", {})
    parts = [
        f"# Proof Pack — {record['engagement_id']}",
        "",
        f"Generated: {record.get('generated_at', '')}",
        f"Proof Score: **{record.get('proof_score', 'n/a')}** "
        f"({record.get('tier', 'n/a')})",
        "",
    ]
    for key in PROOF_PACK_V2_SECTIONS:
        body = sections.get(key, "").strip() or "_(not provided)_"
        parts.append(f"## {titles[key]}")
        parts.append("")
        parts.append(body)
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _validate_components(raw: dict[str, int]) -> ProofComponentsV2:
    required = set(PROOF_SCORE_V2_WEIGHTS.keys())
    unknown = set(raw) - required
    missing = required - set(raw)
    if unknown or missing:
        raise HTTPException(
            status_code=422,
            detail={
                "unknown_components": sorted(unknown),
                "missing_components": sorted(missing),
                "required": sorted(required),
            },
        )
    try:
        return ProofComponentsV2(
            metric_clarity=raw["metric_clarity"],
            source_clarity=raw["source_clarity"],
            evidence_quality=raw["evidence_quality"],
            governance_confidence=raw["governance_confidence"],
            business_relevance=raw["business_relevance"],
            before_after_comparison=raw["before_after_comparison"],
            retainer_linkage=raw["retainer_linkage"],
            limitations_honesty=raw["limitations_honesty"],
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/{engagement_id}/generate")
async def generate_proof_pack(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Build and persist a Proof Pack v2 record.

    Body shape:
      * ``sections`` (required) — dict mapping each of the 14 sections to
        a string. Empty values are allowed (will render as "_(not provided)_")
        but the schema check still runs to surface missing keys.
      * ``components`` (required) — 8 integer components for proof score
        (see ``proof_score_v2.PROOF_SCORE_V2_WEIGHTS``).
      * ``strongest_proof_type`` (optional) — one of
        ``revenue|knowledge|risk|time|quality`` (used by retainer gate).
    """

    if not engagement_id:
        raise HTTPException(status_code=422, detail="engagement_id_required")

    # Doctrine pre-flight — closing a project without a Proof Pack is
    # a non-negotiable, so by definition generating one is always allowed.
    pre = check_action_against_non_negotiables(
        NonNegotiableCheck(action="generate_proof_pack")
    )
    if not pre.allowed:
        raise HTTPException(
            status_code=403,
            detail={"non_negotiables_violated": [v.value for v in pre.violations]},
        )

    sections_raw = payload.get("sections")
    if not isinstance(sections_raw, dict):
        raise HTTPException(
            status_code=422,
            detail="sections object required (14 keys)",
        )
    sections = {k: str(v) for k, v in sections_raw.items()}

    # Validate pack shape via the typed dataclass (raises on missing sections).
    try:
        pack = ProofPackV2(
            engagement_id=engagement_id,
            sections=frozenset(sections.keys()),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not pack.is_complete():
        # Should not happen because frozen-set validation raises above,
        # but keep an explicit guard for clarity.
        raise HTTPException(
            status_code=422,
            detail={"missing_sections": list(pack.missing_sections())},
        )

    components_raw = payload.get("components")
    if not isinstance(components_raw, dict):
        raise HTTPException(
            status_code=422,
            detail="components object required (8 keys 0..100)",
        )
    components = _validate_components(components_raw)
    proof_score = compute_proof_score_v2(components)
    tier = _classify_tier(proof_score)

    record: dict[str, Any] = {
        "engagement_id": engagement_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": sections,
        "components": {
            "metric_clarity": components.metric_clarity,
            "source_clarity": components.source_clarity,
            "evidence_quality": components.evidence_quality,
            "governance_confidence": components.governance_confidence,
            "business_relevance": components.business_relevance,
            "before_after_comparison": components.before_after_comparison,
            "retainer_linkage": components.retainer_linkage,
            "limitations_honesty": components.limitations_honesty,
        },
        "proof_score": proof_score,
        "tier": tier,
        "strongest_proof_type": payload.get("strongest_proof_type"),
    }
    _persist(record)
    return {
        "proof_pack": record,
        "markdown_excerpt": _render_markdown(record).split("\n", 12)[:12],
        "retainer_eligible_threshold": RETAINER_GATE_THRESHOLDS["proof_score_min"],
    }


@router.get("/{engagement_id}")
async def get_proof_pack(engagement_id: str) -> dict[str, Any]:
    rec = _load(engagement_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="proof_pack_not_found")
    return {"proof_pack": rec, "markdown": _render_markdown(rec)}


@router.get("/{engagement_id}/render", response_model=None)
async def render_proof_pack(engagement_id: str) -> dict[str, str]:
    rec = _load(engagement_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="proof_pack_not_found")
    return {"engagement_id": engagement_id, "markdown": _render_markdown(rec)}


@router.post("/{engagement_id}/retainer-gate")
async def retainer_gate(
    engagement_id: str,
    payload: dict[str, Any] = Body(default_factory=dict),
) -> dict[str, Any]:
    """Evaluate the retainer gate against a stored Proof Pack + client signals.

    Body:
      * ``client_health`` (required) — 0..100.
      * ``workflow_is_recurring`` (required) — bool.
      * ``monthly_value_clear`` (required) — bool.
      * ``stakeholder_engaged`` (required) — bool.
      * ``adjacent_capability_signal`` (optional) — bool, defaults False.
    """

    rec = _load(engagement_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="proof_pack_not_found")

    proof_type = rec.get("strongest_proof_type")
    if not proof_type:
        raise HTTPException(
            status_code=409,
            detail="proof_pack_missing_strongest_proof_type",
        )

    try:
        inputs = RetainerGateInputs(
            engagement_id=engagement_id,
            proof_score=float(rec["proof_score"]),
            client_health=float(payload["client_health"]),
            workflow_is_recurring=bool(payload["workflow_is_recurring"]),
            monthly_value_clear=bool(payload["monthly_value_clear"]),
            stakeholder_engaged=bool(payload["stakeholder_engaged"]),
            strongest_proof_type=proof_type,
            adjacent_capability_signal=bool(
                payload.get("adjacent_capability_signal", False)
            ),
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result = evaluate_retainer_gate(inputs)
    return {
        "engagement_id": engagement_id,
        "motion": result.motion.value,
        "retainer_offer": result.retainer_offer,
        "reasons": list(result.reasons),
        "thresholds": RETAINER_GATE_THRESHOLDS,
    }


@router.get("/_meta/weights")
async def weights() -> dict[str, Any]:
    return {
        "sections": list(PROOF_PACK_V2_SECTIONS),
        "score_weights": PROOF_SCORE_V2_WEIGHTS,
        "retainer_thresholds": RETAINER_GATE_THRESHOLDS,
    }
