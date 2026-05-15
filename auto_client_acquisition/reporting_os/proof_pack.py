"""Deterministic proof pack outline for delivery QA."""

from __future__ import annotations

from typing import Any

MASTER_SECTION_KEYS: tuple[str, ...] = (
    "client",
    "service",
    "problem",
    "inputs",
    "work_completed",
    "metrics",
    "ai_outputs",
    "governance",
    "business_value",
    "next_step",
)


def build_proof_pack_dict(
    *,
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    impact: dict[str, Any],
    next_actions: list[str],
) -> dict[str, Any]:
    """Structured proof pack; callers render to Markdown/PDF."""
    return {
        "inputs": inputs,
        "outputs": outputs,
        "impact": impact,
        "next_actions": next_actions,
    }


def proof_pack_has_required_sections(payload: dict[str, Any]) -> bool:
    return (
        isinstance(payload.get("inputs"), dict)
        and isinstance(payload.get("outputs"), dict)
        and bool(payload.get("next_actions"))
    )


def build_master_proof_pack_dict(
    *,
    client: dict[str, Any],
    service: dict[str, Any],
    problem: dict[str, Any],
    inputs: dict[str, Any],
    work_completed: dict[str, Any],
    metrics: dict[str, Any],
    ai_outputs: dict[str, Any],
    governance: dict[str, Any],
    business_value: dict[str, Any],
    next_step: dict[str, Any],
) -> dict[str, Any]:
    """Full operating proof shape aligned with docs/templates/PROOF_PACK_TEMPLATE.md."""
    return {
        "client": client,
        "service": service,
        "problem": problem,
        "inputs": inputs,
        "work_completed": work_completed,
        "metrics": metrics,
        "ai_outputs": ai_outputs,
        "governance": governance,
        "business_value": business_value,
        "next_step": next_step,
    }


def proof_pack_master_complete(payload: dict[str, Any]) -> bool:
    if not isinstance(payload, dict):
        return False
    for key in MASTER_SECTION_KEYS:
        block = payload.get(key)
        if not isinstance(block, dict) or not block:
            return False
    return True


def render_proof_pack_markdown(payload: dict[str, Any]) -> str:
    """Minimal deterministic render for CLI / exports."""
    lines: list[str] = ["# Proof Pack", ""]
    for key in MASTER_SECTION_KEYS:
        block = payload.get(key)
        if not isinstance(block, dict):
            continue
        title = key.replace("_", " ").title()
        lines.append(f"## {title}")
        lines.append("")
        for k, v in block.items():
            lines.append(f"- **{k}**: {v}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "MASTER_SECTION_KEYS",
    "build_master_proof_pack_dict",
    "build_proof_pack_dict",
    "proof_pack_has_required_sections",
    "proof_pack_master_complete",
    "render_proof_pack_markdown",
]
