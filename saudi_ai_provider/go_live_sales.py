"""Go-live sales runbook planner and signature readiness evaluator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .catalog import load_final_service_stack, load_go_live_sales_runbook

SEGMENTS = {"smb", "mid_market", "enterprise"}
BUYER_COMMITMENT_SCORE = {"low": 20, "medium": 60, "high": 100}
PROOF_LEVEL_SCORE = {"L0": 0, "L1": 20, "L2": 45, "L3": 70, "L4": 85, "L5": 100}
RISK_STATUS_SCORE = {"low": 100, "medium": 60, "high": 20}
STAGE_SCORE = {
    "diagnostic_complete": 25,
    "proposal_sent": 45,
    "risk_review_passed": 65,
    "executive_alignment": 85,
    "contract_ready": 100,
}


@dataclass(frozen=True)
class SignatureReadiness:
    score: float
    ready_to_ask_signature: bool
    recommendation: str
    blockers: list[str]


def _service_ids() -> set[str]:
    stack = load_final_service_stack()
    return {service["service_id"] for service in stack.get("services", [])}


def _validate_segment(segment: str) -> str:
    normalized = segment.strip().lower()
    if normalized not in SEGMENTS:
        raise ValueError(f"Unknown segment '{segment}'. Expected one of: {sorted(SEGMENTS)}")
    return normalized


def _runbook() -> dict[str, Any]:
    return load_go_live_sales_runbook()


def build_go_live_sales_plan(segment: str, max_plays: int = 5) -> dict[str, Any]:
    seg = _validate_segment(segment)
    data = _runbook()
    stack_services = _service_ids()
    plays = [
        play
        for play in data.get("target_plays", [])
        if seg in play.get("segments", [])
        and play.get("primary_service") in stack_services
    ][:max_plays]
    priorities = data.get("segment_priorities", {}).get(seg, [])
    return {
        "segment": seg,
        "thesis": data.get("thesis", ""),
        "daily_execution_blocks": data.get("daily_execution_blocks", {}),
        "priority_services": priorities,
        "target_plays": plays,
        "weekly_exec_review": data.get("weekly_exec_review", []),
        "monthly_board_pack": data.get("monthly_board_pack", []),
        "signature_policy": data.get("signature_policy", {}),
    }


def render_go_live_sales_plan(segment: str, lang: str = "ar", max_plays: int = 5) -> str:
    plan = build_go_live_sales_plan(segment=segment, max_plays=max_plays)
    lines: list[str] = []
    if lang == "ar":
        lines.append(f"Go-Live Sales Runbook — الشريحة: {plan['segment']}")
        lines.append(f"الفرضية: {plan['thesis']}")
        lines.append("")
        lines.append("## التشغيل اليومي")
    else:
        lines.append(f"Go-Live Sales Runbook — Segment: {plan['segment']}")
        lines.append(f"Thesis: {plan['thesis']}")
        lines.append("")
        lines.append("## Daily Execution")

    for block_name, actions in plan["daily_execution_blocks"].items():
        lines.append(f"- {block_name}")
        for action in actions:
            lines.append(f"  - {action}")

    lines.append("")
    lines.append("## Priority Services")
    for service_id in plan["priority_services"]:
        lines.append(f"- {service_id}")

    lines.append("")
    lines.append("## Target Plays")
    for play in plan["target_plays"]:
        lines.append(
            f"- {play['play_id']} | industry={play['industry']} | buyer={play['buyer']} | "
            f"primary_service={play['primary_service']} | sku_offer={play['sku_offer']}"
        )
        lines.append(f"  - pain: {play['pain']}")
        lines.append("  - KPI promise:")
        for item in play["kpi_promise"]:
            lines.append(f"    - {item}")
        lines.append(f"  - proof_target: {play['proof_target']}")
        lines.append(f"  - signature_trigger: {play['signature_trigger']}")

    lines.append("")
    lines.append("## Weekly Executive Review")
    for item in plan["weekly_exec_review"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Monthly Board Pack")
    for item in plan["monthly_board_pack"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


def evaluate_signature_readiness(
    *,
    stage: str,
    buyer_commitment: str,
    proof_level: str,
    risk_status: str,
    governance_contract_accepted: bool,
) -> SignatureReadiness:
    stage_key = stage.strip().lower()
    if stage_key not in STAGE_SCORE:
        raise ValueError(f"Unknown stage '{stage}'.")
    commitment = buyer_commitment.strip().lower()
    if commitment not in BUYER_COMMITMENT_SCORE:
        raise ValueError(f"Unknown buyer_commitment '{buyer_commitment}'.")
    proof = proof_level.strip().upper()
    if proof not in PROOF_LEVEL_SCORE:
        raise ValueError(f"Unknown proof_level '{proof_level}'.")
    risk = risk_status.strip().lower()
    if risk not in RISK_STATUS_SCORE:
        raise ValueError(f"Unknown risk_status '{risk_status}'.")

    score = round(
        (
            STAGE_SCORE[stage_key] * 0.30
            + BUYER_COMMITMENT_SCORE[commitment] * 0.25
            + PROOF_LEVEL_SCORE[proof] * 0.25
            + RISK_STATUS_SCORE[risk] * 0.20
        ),
        2,
    )

    blockers: list[str] = []
    if stage_key not in {"executive_alignment", "contract_ready"}:
        blockers.append("stage not mature enough for signature ask")
    if commitment == "low":
        blockers.append("buyer commitment still low")
    if PROOF_LEVEL_SCORE[proof] < PROOF_LEVEL_SCORE["L3"]:
        blockers.append("proof level below L3")
    if risk == "high":
        blockers.append("risk status is high")
    if not governance_contract_accepted:
        blockers.append("governance contract not yet accepted")

    ready = len(blockers) == 0
    recommendation = (
        "Ask for signature now with KPI + governance summary."
        if ready
        else "Do not ask for signature yet; close blockers first."
    )
    return SignatureReadiness(
        score=score,
        ready_to_ask_signature=ready,
        recommendation=recommendation,
        blockers=blockers,
    )


def render_signature_readiness(
    *,
    stage: str,
    buyer_commitment: str,
    proof_level: str,
    risk_status: str,
    governance_contract_accepted: bool,
) -> str:
    verdict = evaluate_signature_readiness(
        stage=stage,
        buyer_commitment=buyer_commitment,
        proof_level=proof_level,
        risk_status=risk_status,
        governance_contract_accepted=governance_contract_accepted,
    )
    lines = [
        "Signature Readiness",
        f"- score: {verdict.score}",
        f"- ready_to_ask_signature: {'yes' if verdict.ready_to_ask_signature else 'no'}",
        f"- recommendation: {verdict.recommendation}",
        "- blockers:",
    ]
    if verdict.blockers:
        for blocker in verdict.blockers:
            lines.append(f"  - {blocker}")
    else:
        lines.append("  - none")
    return "\n".join(lines)
