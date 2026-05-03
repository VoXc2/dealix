"""
Service Excellence Score — gates each service contract before it ships.

Scoring scheme (0-100):
  +10  has target_customer + pain + promise (not empty)
  +10  required_inputs >= 2
  +10  workflow_steps >= 3
  +10  agents_used >= 1
  +10  human_approvals >= 1
  +10  safe_tool_policy >= 1
  +10  deliverables >= 2
  +10  proof_metrics >= 3
  +10  sla_hours > 0
  +5   upgrade_path set (or explicitly None for top tier)
  +5   risks list has content
  -20  promise contains forbidden claim
  -10  forbidden_claims tuple is empty (must declare its own anti-claims)

Gates:
  >= 80   sellable (public marketing OK)
  70-79   beta-only (private beta only — needs improvement)
  < 70    internal-only (do NOT publish)
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.service_tower.contracts import (
    CONTRACTS,
    ServiceContract,
    contract_to_dict,
)


_GLOBAL_FORBIDDEN = (
    "نضمن", "guaranteed", "ضمان نتائج",
    "auto-dm", "cold whatsapp", "scrape", "scraping",
)


def _has_forbidden_in_promise(promise: str) -> bool:
    p = (promise or "").lower()
    return any(claim.lower() in p for claim in _GLOBAL_FORBIDDEN)


def compute_excellence(contract: ServiceContract) -> dict[str, Any]:
    score = 0
    breakdown: list[tuple[str, int, str]] = []  # (rule, points, note)

    if contract.target_customer and contract.pain and contract.promise:
        score += 10
        breakdown.append(("essentials", 10, "target/pain/promise present"))
    else:
        breakdown.append(("essentials", 0, "missing target/pain/promise"))

    if len(contract.required_inputs) >= 2:
        score += 10
        breakdown.append(("inputs", 10, f"{len(contract.required_inputs)} inputs"))
    else:
        breakdown.append(("inputs", 0, f"only {len(contract.required_inputs)} inputs"))

    if len(contract.workflow_steps) >= 3:
        score += 10
        breakdown.append(("workflow", 10, f"{len(contract.workflow_steps)} steps"))
    else:
        breakdown.append(("workflow", 0, f"only {len(contract.workflow_steps)} steps"))

    if len(contract.agents_used) >= 1:
        score += 10
        breakdown.append(("agents", 10, f"{len(contract.agents_used)} agents"))
    else:
        breakdown.append(("agents", 0, "no agents"))

    if len(contract.human_approvals) >= 1:
        score += 10
        breakdown.append(("approvals", 10, f"{len(contract.human_approvals)} approval gates"))
    else:
        breakdown.append(("approvals", 0, "no approval gate"))

    if len(contract.safe_tool_policy) >= 1:
        score += 10
        breakdown.append(("safe_tools", 10, "safe tool policy declared"))
    else:
        breakdown.append(("safe_tools", 0, "missing safe tool policy"))

    if len(contract.deliverables) >= 2:
        score += 10
        breakdown.append(("deliverables", 10, f"{len(contract.deliverables)} deliverables"))
    else:
        breakdown.append(("deliverables", 0, f"only {len(contract.deliverables)} deliverables"))

    if len(contract.proof_metrics) >= 3:
        score += 10
        breakdown.append(("proof_metrics", 10, f"{len(contract.proof_metrics)} metrics"))
    else:
        breakdown.append(("proof_metrics", 0, f"only {len(contract.proof_metrics)} metrics"))

    if contract.sla_hours and contract.sla_hours > 0:
        score += 10
        breakdown.append(("sla", 10, f"{contract.sla_hours}h"))
    else:
        breakdown.append(("sla", 0, "sla missing"))

    # upgrade_path explicitly None is OK for top-tier
    if contract.upgrade_path is not None or contract.bundle_tier == "control_tower":
        score += 5
        breakdown.append(("upgrade_path", 5, contract.upgrade_path or "top tier (no upgrade)"))
    else:
        breakdown.append(("upgrade_path", 0, "missing upgrade_path"))

    if contract.risks:
        score += 5
        breakdown.append(("risks", 5, f"{len(contract.risks)} risks declared"))
    else:
        breakdown.append(("risks", 0, "no risks declared"))

    if _has_forbidden_in_promise(contract.promise):
        score -= 20
        breakdown.append(("forbidden_in_promise", -20, "promise contains forbidden claim"))

    if not contract.forbidden_claims:
        score -= 10
        breakdown.append(("no_anti_claims", -10, "must declare own forbidden_claims"))

    # Clamp 0..100
    score = max(0, min(100, score))
    gate = "sellable" if score >= 80 else ("beta_only" if score >= 70 else "internal_only")

    return {
        "service_id": contract.service_id,
        "score": score,
        "gate": gate,
        "breakdown": breakdown,
    }


def all_excellence() -> dict[str, Any]:
    rows = [compute_excellence(c) for c in CONTRACTS]
    summary = {
        "total": len(rows),
        "sellable": sum(1 for r in rows if r["gate"] == "sellable"),
        "beta_only": sum(1 for r in rows if r["gate"] == "beta_only"),
        "internal_only": sum(1 for r in rows if r["gate"] == "internal_only"),
        "average_score": round(sum(r["score"] for r in rows) / max(len(rows), 1), 1),
    }
    return {"summary": summary, "services": rows}
