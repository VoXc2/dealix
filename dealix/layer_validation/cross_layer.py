"""Cross-layer validation — invariants that span more than one layer.

These checks answer the enterprise question: do the layers hold together?
Each check returns the gate shape plus ``severity`` and ``owner_layer`` so a
critical failure can cap the owning layer's status.
"""

from __future__ import annotations

from typing import Any

from dealix.layer_validation.spec import ENTERPRISE_LAYERS
from dealix.layer_validation.validation_engine import PARTIAL, READY, LayerResult


def _layer_text(manifest: dict[str, Any]) -> str:
    """Flatten every string in a manifest into one lowercase blob."""
    parts: list[str] = []

    def _walk(value: Any) -> None:
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, dict):
            for item in value.values():
                _walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                _walk(item)

    _walk(manifest)
    return " ".join(parts).lower()


def _check(
    gate: str,
    owner_layer: str,
    severity: str,
    blockers: list[str],
) -> dict[str, Any]:
    return {
        "gate": gate,
        "owner_layer": owner_layer,
        "severity": severity,
        "passed": not blockers,
        "blockers": blockers,
    }


def run_cross_layer_checks(manifests: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Run every cross-layer invariant. Returns a list of gate dicts."""
    checks: list[dict[str, Any]] = []

    # 1. Agents must operate under governance.
    agent_text = _layer_text(manifests.get("agent_runtime", {}))
    blockers = [] if "governance" in agent_text else ["agent_runtime_no_governance_reference"]
    checks.append(_check("agents_respect_governance", "agent_runtime", "critical", blockers))

    # 2. Workflows must respect Foundation permissions / RBAC.
    wf_text = _layer_text(manifests.get("workflow_engine", {}))
    blockers = (
        []
        if any(token in wf_text for token in ("permission", "rbac", "auth"))
        else ["workflow_engine_no_permission_reference"]
    )
    checks.append(_check("workflows_respect_permissions", "workflow_engine", "high", blockers))

    # 3. Memory must respect tenant isolation.
    mem_text = _layer_text(manifests.get("memory_knowledge", {}))
    blockers = [] if "tenant" in mem_text else ["memory_knowledge_no_tenant_isolation_reference"]
    checks.append(
        _check("memory_respects_tenant_isolation", "memory_knowledge", "critical", blockers)
    )

    # 4. Every layer's KPIs must be tied to evaluation.
    blockers = []
    for spec in ENTERPRISE_LAYERS:
        layer = manifests.get(spec.id, {}).get("layer", {})
        if not (layer.get("kpis") or []):
            blockers.append(f"layer_without_kpis:{spec.id}")
    eval_text = _layer_text(manifests.get("evaluation", {}))
    if "business_kpis_tracked" not in eval_text:
        blockers.append("evaluation_layer_missing_business_kpis_tracked")
    checks.append(_check("evals_tied_to_business_kpis", "evaluation", "high", blockers))

    # 5. Observability must cover all 8 layers.
    blockers = []
    for spec in ENTERPRISE_LAYERS:
        layer = manifests.get(spec.id, {}).get("layer", {})
        if not (layer.get("observability_signals") or []):
            blockers.append(f"layer_without_observability:{spec.id}")
    checks.append(_check("observability_covers_all_layers", "observability", "critical", blockers))

    return checks


def apply_cross_layer_caps(
    results: dict[str, LayerResult],
    cross_checks: list[dict[str, Any]],
) -> None:
    """A failed ``critical`` cross-layer check caps its owning layer at PARTIAL."""
    for check in cross_checks:
        if check["passed"] or check["severity"] != "critical":
            continue
        owner = results.get(check["owner_layer"])
        if owner is not None and owner.status == READY:
            owner.status = PARTIAL
            owner.capped_by = f"cross_layer:{check['gate']}"


def cross_layer_passed(cross_checks: list[dict[str, Any]]) -> bool:
    """True only when every cross-layer check passed."""
    return all(check["passed"] for check in cross_checks)
