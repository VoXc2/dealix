"""Read-only access to docs/registry/SERVICE_READINESS_MATRIX.yaml.

Wraps the source-of-truth YAML so other modules don't reach into
the file directly. The validator
(``scripts/verify_service_readiness_matrix.py``) remains the
canonical correctness check; this module is purely a reader.
"""
from __future__ import annotations

from pathlib import Path

import yaml

from auto_client_acquisition.self_growth_os.schemas import (
    ApprovalStatus,
    Language,
    RiskLevel,
    ServiceActivationCheck,
    ServiceBundle,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = REPO_ROOT / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"

ALLOWED_STATUSES = {"live", "pilot", "partial", "target", "blocked", "backlog"}

LIVE_GATES = (
    "inputs",
    "workflow",
    "agent_role",
    "human_approval",
    "safe_tool_gateway",
    "deliverable",
    "proof_metric",
    "test_or_evidence",
)


def _load() -> dict:
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"matrix not found at {MATRIX_PATH}")
    with MATRIX_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def _bundle_enum(raw: str) -> ServiceBundle:
    try:
        return ServiceBundle(raw)
    except ValueError:
        return ServiceBundle.UNKNOWN


def _risk_for_status(status: str) -> RiskLevel:
    return {
        "live": RiskLevel.LOW,
        "pilot": RiskLevel.LOW,
        "partial": RiskLevel.MEDIUM,
        "target": RiskLevel.MEDIUM,
        "backlog": RiskLevel.MEDIUM,
        "blocked": RiskLevel.BLOCKED,
    }.get(status, RiskLevel.MEDIUM)


def load_matrix() -> dict:
    """Return the raw YAML payload."""
    return _load()


def counts() -> dict[str, int]:
    """Status histogram + total."""
    out = {s: 0 for s in ALLOWED_STATUSES}
    out["total"] = 0
    for svc in _load().get("services", []) or []:
        s = svc.get("status")
        if s in out:
            out[s] += 1
        out["total"] += 1
    return out


def check_service(service_id: str) -> ServiceActivationCheck:
    """Build a ``ServiceActivationCheck`` for one service.

    Honest signal: ``eight_gate_block_present`` is True only when the
    YAML actually carries a ``gates:`` mapping with all 8 gates true,
    matching the validator's rule.
    """
    data = _load()
    svc = next(
        (s for s in data.get("services", []) or [] if s.get("service_id") == service_id),
        None,
    )
    if svc is None:
        raise KeyError(f"service_id not found: {service_id}")

    gates = svc.get("gates") or {}
    eight_gate = isinstance(gates, dict) and all(bool(gates.get(g)) for g in LIVE_GATES)

    blocking_reasons: list[str] = []
    if svc.get("status") != "live" and not eight_gate:
        for g in LIVE_GATES:
            if not (isinstance(gates, dict) and gates.get(g)):
                blocking_reasons.append(f"gate_missing:{g}")
    if svc.get("status") == "blocked":
        for reason in svc.get("blocked_actions") or []:
            blocking_reasons.append(f"blocked_action:{reason}")

    return ServiceActivationCheck.new(
        language=Language.BILINGUAL,
        source="self_growth_os.service_activation_matrix",
        confidence=0.95,
        risk_level=_risk_for_status(str(svc.get("status", "target"))),
        target_persona="founder",
        service_bundle=_bundle_enum(str(svc.get("bundle", "unknown"))),
        recommended_action=(
            f"promote {service_id} from {svc.get('status')} to live once "
            f"the 8 gates pass"
            if svc.get("status") != "live"
            else f"keep {service_id} live; periodic gate re-verification"
        ),
        approval_status=(
            ApprovalStatus.APPROVED
            if svc.get("status") in {"live", "pilot"}
            else ApprovalStatus.APPROVAL_REQUIRED
        ),
        service_id=str(svc["service_id"]),
        name_ar=str(svc.get("name_ar", "")),
        name_en=str(svc.get("name_en", "")),
        status=str(svc.get("status", "target")),  # type: ignore[arg-type]
        eight_gate_block_present=eight_gate,
        blocking_reasons=blocking_reasons,
        next_activation_step_ar=str(svc.get("next_activation_step_ar", "")).strip(),
        next_activation_step_en=str(svc.get("next_activation_step_en", "")).strip(),
    )


def check_all() -> list[ServiceActivationCheck]:
    """Run check_service over every service in the matrix."""
    return [check_service(s["service_id"]) for s in _load().get("services", []) or []]


def candidates_for_promotion() -> list[ServiceActivationCheck]:
    """Services currently `partial` whose blocking_reasons could be
    closed in the next sprint. Ordered by current status (partial > pilot)."""
    rank = {"partial": 0, "pilot": 1, "target": 2, "blocked": 3, "backlog": 4, "live": 5}
    checks = [c for c in check_all() if c.status in {"partial", "pilot"}]
    checks.sort(key=lambda c: rank.get(str(c.status), 99))
    return checks
