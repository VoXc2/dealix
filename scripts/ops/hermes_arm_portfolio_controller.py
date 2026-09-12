#!/usr/bin/env python3
"""HERMES ARM PORTFOLIO CONTROLLER — transparent ranking over the canonical 44-arm registry.

Responsibility (planning only, never a scheduler):

    READ canonical 44-arm registry + execution playbooks + evidence ledger
    -> SCORE every arm with an explainable prioritization heuristic
    -> CLASSIFY DEEP / LIGHT / HOLD
    -> SELECT the <=DEEP_WIP_MAX deep wedges that real evidence can justify
    -> EMIT Top3, hold/light, next safe action, evidence refs, job/model class,
       cost / risk / founder-minutes / proof-gap
    -> HAND OFF executable work to the *existing* Hermes session factory queue.

Hard laws enforced here:

* The canonical arm registry and execution playbooks are the only taxonomies.
* Exactly five permanent agents; ACTIVE_DEEP stays ARM-001/002/003 at
  ``DEEP_WIP_MAX=3`` unless real customer/economic evidence exists.
* Research alone can only rank LIGHT or HOLD — it never promotes to DEEP.
* Scores are a prioritization heuristic, not a forecast; no ROI, pipeline,
  revenue or amount is ever invented.
* L5 material effects stay ``WAITING_L5``: the controller only drafts and the
  runner only enqueues; it never sends, publishes, spends, deploys, mutates DNS,
  mutates a database or touches secrets.
* No duplicate scheduler: a single planning pass is emitted; execution is owned
  by ``scripts/ops/session_factory.py`` (the one canonical job scheduler).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parents[1]

REGISTRY_PATH = REPO_ROOT / "config" / "company" / "dealix_arm_registry.json"
PLAYBOOKS_PATH = REPO_ROOT / "config" / "company" / "dealix_arm_execution_playbooks.json"
DEFAULT_EVIDENCE_PATH = REPO_ROOT / "data" / "ops" / "arm_portfolio_evidence_v1.json"

SCHEMA = "dealix.hermes_arm_portfolio_plan.v1"
EVIDENCE_SCHEMA = "dealix.arm_portfolio_evidence.v1"
SCORE_SEMANTICS = "PRIORITIZATION_HEURISTIC_NOT_FORECAST"
L5_POLICY = "WAITING_L5_never_auto_executed"
EXTERNAL_EFFECT = "NONE"
RECEIPT_MARKER_PREFIX = "ARM_PORTFOLIO_RECEIPT:"

CLASS_DEEP = "DEEP"
CLASS_LIGHT = "LIGHT"
CLASS_HOLD = "HOLD"
CLASS_RANK = {CLASS_DEEP: 0, CLASS_LIGHT: 1, CLASS_HOLD: 2}

TIERS = ("NONE", "RESEARCH", "CUSTOMER", "ECONOMIC")
TIER_STRENGTH = {"NONE": 0.0, "RESEARCH": 35.0, "CUSTOMER": 75.0, "ECONOMIC": 100.0}
PRIORITY_FIT = {"P0": 100.0, "P1": 70.0, "P2": 45.0, "P3": 20.0}
HORIZON_URGENCY = {"NOW-30D": 100.0, "30-90D": 70.0, "90-180D": 45.0, "180-365D": 20.0, "HOLD": 0.0}
STATE_STRENGTH = {
    "ACTIVE_DEEP": 100.0,
    "ACTIVE_LIGHT": 70.0,
    "VALIDATE": 50.0,
    "WATCH": 30.0,
    "BLOCKED": 0.0,
}
SPECIAL_GATES = frozenset({"DATA_RIGHTS_GATE", "REGULATED_PARTNER_GATE"})
NEAR_TERM_HORIZONS = frozenset({"NOW-30D", "30-90D"})

FACTOR_WEIGHTS = {
    "evidence_strength": 0.32,
    "priority_fit": 0.20,
    "horizon_urgency": 0.18,
    "strategic_state": 0.18,
    "gate_readiness": 0.12,
}
PENALTY_WEIGHTS = {"risk": 0.15, "founder_minutes": 0.10, "proof_gap": 0.10}

EVIDENCE_REF_FIELDS = (
    "research_evidence_refs",
    "customer_evidence_refs",
    "economic_evidence_refs",
    "stop_loss_evidence_refs",
)

OWNER_JOB_CLASS = {
    "dealix-engineer": "ENGINEERING",
    "dealix-content": "CONTENT",
    "dealix-delivery": "DELIVERY",
    "dealix-sales": "COMMERCIAL_REASONING",
    "dealix-pm": "COMMERCIAL_REASONING",
}

FORBIDDEN_ENV = (
    "DEALIX_EXTERNAL_SEND",
    "DEALIX_EMAIL_LIVE_SEND",
    "DEALIX_WHATSAPP_OUTBOUND",
    "DEALIX_PUBLIC_PUBLISH",
    "DEALIX_PAID_SPEND",
    "DEALIX_PAYMENT_EXECUTION",
    "DEALIX_PRODUCTION_MUTATION",
    "DEALIX_DNS_MUTATION",
    "DEALIX_DB_MUTATION",
    "DEALIX_SECRET_MUTATION",
    "AUTO_MERGE_ENABLED",
    "AUTO_DEPLOY_ENABLED",
)

TERMINAL_JOB_STATES = frozenset({"SUCCEEDED", "FAILED", "SUPERSEDED", "CANCELLED"})


# --------------------------------------------------------------------------
# Session factory bridge (the one canonical scheduler)
# --------------------------------------------------------------------------


def session_factory() -> Any:
    """Return the canonical session factory module (single scheduler)."""
    if str(_HERE) not in sys.path:
        sys.path.insert(0, str(_HERE))
    import session_factory as module

    return module


# --------------------------------------------------------------------------
# Small deterministic helpers
# --------------------------------------------------------------------------


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def read_json(path: Path, default: Any) -> Any:
    if not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tripwires() -> list[str]:
    """Fail-closed if any external-effect switch is enabled in the environment."""
    enabled = []
    for key in FORBIDDEN_ENV:
        value = str(os.environ.get(key) or "").strip().lower()
        if value in {"1", "true", "yes", "on"}:
            enabled.append(key)
    return sorted(enabled)


# --------------------------------------------------------------------------
# Canonical sources
# --------------------------------------------------------------------------


def load_registry(path: Path | None = None) -> dict[str, Any]:
    payload = read_json(Path(path or REGISTRY_PATH), {})
    return payload if isinstance(payload, dict) else {}


def load_playbooks(path: Path | None = None) -> dict[str, Any]:
    payload = read_json(Path(path or PLAYBOOKS_PATH), {})
    return payload if isinstance(payload, dict) else {}


def contract_failures(registry: dict[str, Any], playbooks: dict[str, Any]) -> list[str]:
    """Structural invariants the controller refuses to plan against."""
    failures: list[str] = []
    arms = registry.get("arms")
    playbook_rows = playbooks.get("playbooks")
    if registry.get("schema") != "dealix.company-arm-portfolio-registry.v2":
        failures.append("REGISTRY_SCHEMA")
    if not isinstance(arms, list) or len(arms) != 44:
        failures.append("ARMS_44")
        arms = arms if isinstance(arms, list) else []
    ids = {str(arm.get("id")) for arm in arms if isinstance(arm, dict)}
    expected = {f"ARM-{index:03d}" for index in range(1, 45)}
    if ids != expected:
        failures.append("ARM_IDS")
    if registry.get("deep_wip_max") != 3:
        failures.append("DEEP_WIP_MAX")
    agents = registry.get("permanent_agents")
    if not isinstance(agents, list) or len(agents) != 5 or len(set(agents)) != 5:
        failures.append("PERMANENT_AGENTS")
    if playbooks.get("schema_version") != 1:
        failures.append("PLAYBOOKS_SCHEMA")
    if playbooks.get("registry") != "config/company/dealix_arm_registry.json":
        failures.append("PLAYBOOKS_REGISTRY_LINK")
    if playbooks.get("deep_wip_max") != registry.get("deep_wip_max"):
        failures.append("PLAYBOOKS_DEEP_WIP")
    playbook_ids = (
        {str(row.get("arm_id")) for row in playbook_rows if isinstance(row, dict)}
        if isinstance(playbook_rows, list)
        else set()
    )
    if playbook_ids != expected:
        failures.append("PLAYBOOKS_COVERAGE")
    deep = {
        str(arm.get("id"))
        for arm in arms
        if isinstance(arm, dict) and arm.get("state") == "ACTIVE_DEEP"
    }
    if deep != {"ARM-001", "ARM-002", "ARM-003"}:
        failures.append("ACTIVE_DEEP_001_002_003")
    return failures


# --------------------------------------------------------------------------
# Evidence ledger
# --------------------------------------------------------------------------


def empty_evidence() -> dict[str, Any]:
    payload: dict[str, Any] = {field: [] for field in EVIDENCE_REF_FIELDS}
    payload.update(
        {
            "founder_minutes": None,
            "requires_external_send": False,
            "proof_gap_notes": "",
        }
    )
    return payload


def _clean_refs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    refs: list[str] = []
    for item in value:
        text = str(item).strip()
        if text and text not in refs:
            refs.append(text)
    return refs


def normalize_evidence(
    payload: Any, *, allowed_ids: set[str] | None = None
) -> dict[str, dict[str, Any]]:
    """Normalize an evidence ledger into ``{arm_id: evidence}``; unknown arms dropped."""
    if not isinstance(payload, dict):
        return {}
    rows = payload.get("arms") if isinstance(payload.get("arms"), dict) else payload
    if not isinstance(rows, dict):
        return {}
    normalized: dict[str, dict[str, Any]] = {}
    for arm_id, raw in rows.items():
        arm_id = str(arm_id)
        if allowed_ids is not None and arm_id not in allowed_ids:
            continue
        if not isinstance(raw, dict):
            continue
        entry = empty_evidence()
        for field in EVIDENCE_REF_FIELDS:
            entry[field] = _clean_refs(raw.get(field))
        minutes = raw.get("founder_minutes")
        try:
            entry["founder_minutes"] = None if minutes is None else max(0.0, float(minutes))
        except (TypeError, ValueError):
            entry["founder_minutes"] = None
        entry["requires_external_send"] = bool(raw.get("requires_external_send", False))
        entry["proof_gap_notes"] = str(raw.get("proof_gap_notes") or "").strip()
        normalized[arm_id] = entry
    return normalized


def load_evidence(
    path: Path | None = None, *, allowed_ids: set[str] | None = None
) -> dict[str, dict[str, Any]]:
    return normalize_evidence(
        read_json(Path(path or DEFAULT_EVIDENCE_PATH), None), allowed_ids=allowed_ids
    )


def evidence_tier(evidence: dict[str, Any]) -> str:
    if evidence.get("economic_evidence_refs"):
        return "ECONOMIC"
    if evidence.get("customer_evidence_refs"):
        return "CUSTOMER"
    if evidence.get("research_evidence_refs"):
        return "RESEARCH"
    return "NONE"


def has_stop_loss(evidence: dict[str, Any]) -> bool:
    return bool(evidence.get("stop_loss_evidence_refs"))


# --------------------------------------------------------------------------
# Transparent scoring
# --------------------------------------------------------------------------


def _gate_readiness(arm: dict[str, Any], evidence: dict[str, Any]) -> float:
    tier = evidence_tier(evidence)
    if arm.get("promotion_gate") in SPECIAL_GATES:
        return 60.0 if tier in ("CUSTOMER", "ECONOMIC") else 0.0
    return 100.0 if tier != "NONE" else 50.0


def _risk(
    arm: dict[str, Any], playbook: dict[str, Any], evidence: dict[str, Any]
) -> tuple[float, list[str]]:
    score = 20.0
    basis = ["base"]
    if arm.get("state") == "BLOCKED":
        score = max(score, 100.0)
        basis.append("BLOCKED")
    if arm.get("promotion_gate") in SPECIAL_GATES:
        score = max(score, 80.0)
        basis.append(str(arm.get("promotion_gate")))
    if playbook.get("horizon") == "HOLD":
        score = max(score, 70.0)
        basis.append("HOLD_HORIZON")
    if arm.get("priority") == "P3":
        score = max(score, 50.0)
        basis.append("P3")
    if arm.get("state") == "WATCH":
        score = max(score, 45.0)
        basis.append("WATCH")
    if has_stop_loss(evidence):
        score = 100.0
        basis.append("STOP_LOSS_EVIDENCE")
    return score, basis


def _founder_minutes(evidence: dict[str, Any]) -> dict[str, Any]:
    reported = evidence.get("founder_minutes")
    if reported is None:
        return {
            "reported": None,
            "penalty_score": 50.0,
            "basis": "NO_REPORT",
            "penalty_basis": "unknown",
        }
    penalty = _clamp(float(reported) / 480.0 * 100.0)
    return {
        "reported": float(reported),
        "penalty_score": penalty,
        "basis": "REPORTED",
        "penalty_basis": "reported",
    }


def _proof_gap(arm: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    gate = str(arm.get("promotion_gate") or "UNKNOWN")
    tier = evidence_tier(evidence)
    if gate in SPECIAL_GATES:
        required = "CUSTOMER_OR_ECONOMIC"
        satisfied = tier in ("CUSTOMER", "ECONOMIC")
    else:
        required = "RESEARCH_MINIMUM"
        satisfied = tier != "NONE"
    missing = [] if satisfied else [required]
    return {
        "required_gate": gate,
        "required_evidence": required,
        "available_tier": tier,
        "satisfied": satisfied,
        "missing": missing,
        "penalty_score": 0.0 if satisfied else 100.0,
    }


def score_arm(
    arm: dict[str, Any], playbook: dict[str, Any], evidence: dict[str, Any]
) -> dict[str, Any]:
    """Explainable heuristic score (never a probability, forecast or money value)."""
    tier = evidence_tier(evidence)
    factors = {
        "evidence_strength": {
            "value": TIER_STRENGTH[tier],
            "weight": FACTOR_WEIGHTS["evidence_strength"],
            "basis": f"tier={tier}",
        },
        "priority_fit": {
            "value": PRIORITY_FIT.get(str(arm.get("priority")), 0.0),
            "weight": FACTOR_WEIGHTS["priority_fit"],
            "basis": f"priority={arm.get('priority')}",
        },
        "horizon_urgency": {
            "value": HORIZON_URGENCY.get(str(playbook.get("horizon")), 0.0),
            "weight": FACTOR_WEIGHTS["horizon_urgency"],
            "basis": f"horizon={playbook.get('horizon')}",
        },
        "strategic_state": {
            "value": STATE_STRENGTH.get(str(arm.get("state")), 0.0),
            "weight": FACTOR_WEIGHTS["strategic_state"],
            "basis": f"state={arm.get('state')}",
        },
        "gate_readiness": {
            "value": _gate_readiness(arm, evidence),
            "weight": FACTOR_WEIGHTS["gate_readiness"],
            "basis": f"gate={arm.get('promotion_gate')}",
        },
    }
    risk_score, risk_basis = _risk(arm, playbook, evidence)
    founder = _founder_minutes(evidence)
    gap = _proof_gap(arm, evidence)
    positive = sum(item["value"] * item["weight"] for item in factors.values())
    penalty = (
        risk_score * PENALTY_WEIGHTS["risk"]
        + founder["penalty_score"] * PENALTY_WEIGHTS["founder_minutes"]
        + gap["penalty_score"] * PENALTY_WEIGHTS["proof_gap"]
    )
    return {
        "total": round(_clamp(positive - penalty), 2),
        "semantics": SCORE_SEMANTICS,
        "positive": round(positive, 2),
        "penalty": round(penalty, 2),
        "formula": "sum(factor.value * factor.weight) - sum(penalty.penalty_score * penalty.weight)",
        "factors": factors,
        "penalties": {
            "risk": {
                "penalty_score": risk_score,
                "weight": PENALTY_WEIGHTS["risk"],
                "basis": risk_basis,
            },
            "founder_minutes": {
                "penalty_score": founder["penalty_score"],
                "weight": PENALTY_WEIGHTS["founder_minutes"],
                "basis": founder["penalty_basis"],
            },
            "proof_gap": {
                "penalty_score": gap["penalty_score"],
                "weight": PENALTY_WEIGHTS["proof_gap"],
                "basis": gap["required_gate"],
            },
        },
    }


# --------------------------------------------------------------------------
# Job / model class and safe action
# --------------------------------------------------------------------------


def model_job_class(owner: str) -> dict[str, Any]:
    factory = session_factory()
    job_class = OWNER_JOB_CLASS.get(owner, "COMMERCIAL_REASONING")
    return {
        "job_class": job_class,
        "model_class": factory.CLASS_TO_MODEL_CLASS.get(job_class, "R4_INCLUDED_HIGH"),
        "execution_mode": factory.CLASS_TO_MODE.get(job_class, "opencode"),
    }


def _cost(classification: str, horizon: str) -> dict[str, Any]:
    compute = {CLASS_DEEP: "MEDIUM", CLASS_LIGHT: "LOW", CLASS_HOLD: "NONE"}[classification]
    return {
        "compute_class": compute,
        "cash_class": "NONE",
        "basis": f"classification={classification};horizon={horizon};no_paid_spend_authorized",
    }


def _risk_class(risk_score: float) -> str:
    if risk_score >= 80.0:
        return "HIGH"
    if risk_score >= 50.0:
        return "MEDIUM"
    return "LOW"


def next_safe_action(
    arm: dict[str, Any],
    playbook: dict[str, Any],
    classification: str,
    evidence: dict[str, Any],
) -> tuple[str, bool]:
    """Return (action, requires_external_send). No L5 effect is ever auto-run."""
    experiment = str(playbook.get("first_experiment") or "bounded first experiment")
    gate = str(arm.get("promotion_gate") or "promotion gate")
    if has_stop_loss(evidence):
        return (
            "Stop-loss evidence present: founder review to demote or kill (no auto-demotion).",
            False,
        )
    if evidence.get("requires_external_send"):
        return (
            f"Draft only: {experiment}. External send/publish requires an exact-action L5 "
            "approval (ACTION_HASH); the factory parks this at WAITING_L5.",
            True,
        )
    if classification == CLASS_DEEP:
        return (
            f"Run the bounded first experiment (authority <= L2, draft/execute-internal): {experiment}",
            False,
        )
    if classification == CLASS_LIGHT:
        return (
            f"Collect real evidence for {gate} via bounded research and internal drafts: {experiment}",
            False,
        )
    if arm.get("state") == "BLOCKED":
        return (f"Do not commercialize: satisfy {gate} before any activation.", False)
    return (
        "Hold: no real customer/economic evidence yet; research alone cannot promote this arm.",
        False,
    )


# --------------------------------------------------------------------------
# Portfolio planning
# --------------------------------------------------------------------------


def _deep_selection(
    registry: dict[str, Any],
    playbooks_by_id: dict[str, dict[str, Any]],
    evidence: dict[str, dict[str, Any]],
    scores: dict[str, dict[str, Any]],
) -> tuple[list[str], list[str], list[str]]:
    arms = registry.get("arms") or []
    preserved: list[str] = []
    for arm in arms:
        if not isinstance(arm, dict):
            continue
        arm_id = str(arm.get("id"))
        if arm.get("state") == "ACTIVE_DEEP" and not has_stop_loss(
            evidence.get(arm_id, empty_evidence())
        ):
            preserved.append(arm_id)
    capacity = max(0, int(registry.get("deep_wip_max") or 0) - len(preserved))
    candidates: list[tuple[float, str]] = []
    for arm in arms:
        if not isinstance(arm, dict):
            continue
        arm_id = str(arm.get("id"))
        if arm_id in preserved:
            continue
        playbook = playbooks_by_id.get(arm_id, {})
        ev = evidence.get(arm_id, empty_evidence())
        if has_stop_loss(ev):
            continue
        if evidence_tier(ev) not in ("CUSTOMER", "ECONOMIC"):
            continue
        if arm.get("state") == "BLOCKED" or playbook.get("horizon") == "HOLD":
            continue
        candidates.append((scores.get(arm_id, {}).get("total", 0.0), arm_id))
    candidates.sort(key=lambda item: (-item[0], item[1]))
    promoted = [arm_id for _, arm_id in candidates[:capacity]]
    return preserved, promoted, preserved + promoted


def _classify(
    arm: dict[str, Any],
    playbook: dict[str, Any],
    evidence: dict[str, Any],
    deep_ids: set[str],
) -> str:
    arm_id = str(arm.get("id"))
    if has_stop_loss(evidence):
        return CLASS_HOLD
    if arm_id in deep_ids:
        return CLASS_DEEP
    if arm.get("state") == "BLOCKED" or playbook.get("horizon") == "HOLD":
        return CLASS_HOLD
    tier = evidence_tier(evidence)
    if arm.get("state") in ("ACTIVE_LIGHT", "VALIDATE"):
        return CLASS_LIGHT
    if tier != "NONE" and playbook.get("horizon") in NEAR_TERM_HORIZONS:
        return CLASS_LIGHT
    return CLASS_HOLD


def build_record(
    arm: dict[str, Any],
    playbook: dict[str, Any],
    evidence: dict[str, Any],
    *,
    classification: str,
) -> dict[str, Any]:
    score = score_arm(arm, playbook, evidence)
    risk_score = score["penalties"]["risk"]["penalty_score"]
    founder = _founder_minutes(evidence)
    gap = _proof_gap(arm, evidence)
    action, external = next_safe_action(arm, playbook, classification, evidence)
    job_class = model_job_class(str(arm.get("owner")))
    auto_executable = classification in (CLASS_DEEP, CLASS_LIGHT) and not external
    if external:
        authority = "L5"
    elif classification == CLASS_DEEP:
        authority = "L2"
    elif classification == CLASS_LIGHT:
        authority = "L1"
    else:
        authority = "L0"
    refs: list[str] = []
    for field in EVIDENCE_REF_FIELDS:
        if field == "stop_loss_evidence_refs":
            continue
        refs.extend(evidence.get(field, []))
    return {
        "arm_id": str(arm.get("id")),
        "name": arm.get("name"),
        "engine": arm.get("engine"),
        "owner": arm.get("owner"),
        "priority": arm.get("priority"),
        "state": arm.get("state"),
        "dimension_profile": arm.get("dimension_profile"),
        "promotion_gate": arm.get("promotion_gate"),
        "kill_condition": arm.get("kill_condition"),
        "horizon": playbook.get("horizon"),
        "classification": classification,
        "score": score,
        "evidence": {
            "tier": evidence_tier(evidence),
            "research_evidence_refs": evidence.get("research_evidence_refs", []),
            "customer_evidence_refs": evidence.get("customer_evidence_refs", []),
            "economic_evidence_refs": evidence.get("economic_evidence_refs", []),
            "stop_loss_evidence_refs": evidence.get("stop_loss_evidence_refs", []),
        },
        "evidence_refs": refs,
        "next_safe_action": action,
        "requires_external_send": external,
        "l5_required": external,
        "model_job_class": {
            **job_class,
            "authority_level": authority,
            "auto_executable": auto_executable,
        },
        "cost": _cost(classification, str(playbook.get("horizon"))),
        "risk": {
            "class": _risk_class(risk_score),
            "score": risk_score,
            "basis": score["penalties"]["risk"]["basis"],
        },
        "founder_minutes": {
            "reported": founder["reported"],
            "band": {CLASS_DEEP: "HIGH", CLASS_LIGHT: "BOUNDED", CLASS_HOLD: "NONE"}[
                classification
            ],
            "basis": founder["basis"],
        },
        "proof_gap": {**gap, "notes": evidence.get("proof_gap_notes") or ""},
    }


def plan_portfolio(
    *,
    registry: dict[str, Any] | None = None,
    playbooks: dict[str, Any] | None = None,
    evidence: dict[str, dict[str, Any]] | None = None,
    registry_path: Path | None = None,
    playbooks_path: Path | None = None,
    evidence_path: Path | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Produce one deterministic, transparent portfolio plan (no scheduling)."""
    registry = registry if registry is not None else load_registry(registry_path)
    playbooks = playbooks if playbooks is not None else load_playbooks(playbooks_path)
    arms = [arm for arm in (registry.get("arms") or []) if isinstance(arm, dict)]
    allowed_ids = {str(arm.get("id")) for arm in arms}
    if evidence is None:
        evidence = load_evidence(evidence_path, allowed_ids=allowed_ids)
    playbooks_by_id = {
        str(row.get("arm_id")): row
        for row in (playbooks.get("playbooks") or [])
        if isinstance(row, dict)
    }
    failures = contract_failures(registry, playbooks)
    if failures:
        return {
            "schema": SCHEMA,
            "generated_at": generated_at or now_iso(),
            "overall": "CONTRACT_FAILED",
            "contract_failures": failures,
            "records": [],
            "top3": [],
            "counts": {},
        }

    scores = {
        str(arm.get("id")): score_arm(
            arm,
            playbooks_by_id.get(str(arm.get("id")), {}),
            evidence.get(str(arm.get("id")), empty_evidence()),
        )
        for arm in arms
    }
    preserved, promoted, deep_ids_list = _deep_selection(
        registry, playbooks_by_id, evidence, scores
    )
    deep_ids = set(deep_ids_list)
    records = [
        build_record(
            arm,
            playbooks_by_id.get(str(arm.get("id")), {}),
            evidence.get(str(arm.get("id")), empty_evidence()),
            classification=_classify(
                arm,
                playbooks_by_id.get(str(arm.get("id")), {}),
                evidence.get(str(arm.get("id")), empty_evidence()),
                deep_ids,
            ),
        )
        for arm in arms
    ]
    ordered = sorted(
        records,
        key=lambda rec: (
            CLASS_RANK.get(rec["classification"], 3),
            -rec["score"]["total"],
            rec["arm_id"],
        ),
    )
    counts = {
        name: sum(1 for rec in records if rec["classification"] == name)
        for name in (CLASS_DEEP, CLASS_LIGHT, CLASS_HOLD)
    }
    tier_counts = {
        tier: sum(1 for rec in records if rec["evidence"]["tier"] == tier) for tier in TIERS
    }
    tripwire_list = tripwires()
    registry_source = registry_path or REGISTRY_PATH
    playbooks_source = playbooks_path or PLAYBOOKS_PATH
    evidence_source = evidence_path or DEFAULT_EVIDENCE_PATH
    plan = {
        "schema": SCHEMA,
        "generated_at": generated_at or now_iso(),
        "overall": "BLOCKED" if tripwire_list else "PLAN_READY",
        "score_semantics": SCORE_SEMANTICS,
        "north_star": registry.get("north_star"),
        "permanent_agents": registry.get("permanent_agents"),
        "deep_wip_max": registry.get("deep_wip_max"),
        "counts": counts,
        "evidence_tier_counts": tier_counts,
        "deep_wedge_ids": deep_ids_list,
        "preserved_deep_ids": preserved,
        "promoted_by_evidence_ids": promoted,
        "top3": [
            {
                "arm_id": rec["arm_id"],
                "name": rec["name"],
                "classification": rec["classification"],
                "score": rec["score"]["total"],
                "job_class": rec["model_job_class"]["job_class"],
                "model_class": rec["model_job_class"]["model_class"],
                "next_safe_action": rec["next_safe_action"],
            }
            for rec in ordered[:3]
        ],
        "records": ordered,
        "truth": {
            "counts_as_revenue": False,
            "counts_as_pipeline": False,
            "invented_amounts": False,
            "score_semantics": SCORE_SEMANTICS,
            "external_effect": EXTERNAL_EFFECT,
            "l5_policy": L5_POLICY,
        },
        "safety": {
            "tripwires": tripwire_list,
            "authority_model": "L0-L4 autonomous; L5 exact-action approval only",
        },
        "canonical_sources": {
            "registry": {
                "path": str(registry_source),
                "sha256": sha256_file(Path(registry_source)),
            },
            "playbooks": {
                "path": str(playbooks_source),
                "sha256": sha256_file(Path(playbooks_source)),
            },
            "evidence": {
                "path": str(evidence_source),
                "schema": EVIDENCE_SCHEMA,
                "sha256": sha256_file(Path(evidence_source)),
                "arms_with_evidence": len(evidence),
            },
        },
    }
    return plan


def write_plan(plan: dict[str, Any], path: Path) -> Path:
    factory = session_factory()
    factory.write_json(Path(path), plan)
    return Path(path)


def render_summary(plan: dict[str, Any]) -> str:
    counts = plan.get("counts") or {}
    lines = [
        f"HERMES_ARM_PORTFOLIO={plan.get('overall')}",
        f"SCHEMA={plan.get('schema')}",
        f"SCORE_SEMANTICS={plan.get('score_semantics')}",
        f"ARMS={len(plan.get('records') or [])} PERMANENT_AGENTS={len(plan.get('permanent_agents') or [])} DEEP_WIP={plan.get('deep_wip_max')}",
        f"DEEP={counts.get(CLASS_DEEP, 0)} LIGHT={counts.get(CLASS_LIGHT, 0)} HOLD={counts.get(CLASS_HOLD, 0)}",
        f"DEEP_WEDGES={','.join(plan.get('deep_wedge_ids') or []) or 'none'}",
        "EVIDENCE_TIERS="
        + " ".join(f"{k}={v}" for k, v in (plan.get("evidence_tier_counts") or {}).items()),
        f"L5_POLICY={(plan.get('truth') or {}).get('l5_policy')}",
        f"EXTERNAL_EFFECT={(plan.get('truth') or {}).get('external_effect')}",
        f"COUNTS_AS_REVENUE={(plan.get('truth') or {}).get('counts_as_revenue')}",
        f"TRIPWIRES={','.join((plan.get('safety') or {}).get('tripwires') or []) or 'none'}",
    ]
    for entry in plan.get("top3") or []:
        lines.append(
            f"  TOP {entry['arm_id']} [{entry['classification']}] score={entry['score']} "
            f"{entry['job_class']}/{entry['model_class']} next={entry['next_safe_action']}"
        )
    return "\n".join(lines)


def build_arm_job_prompt(record: dict[str, Any]) -> str:
    """Bounded, non-modifying, receipt-required prompt for one arm job."""
    arm_id = record["arm_id"]
    marker = f"{RECEIPT_MARKER_PREFIX}{arm_id}"
    refs = record.get("evidence_refs") or []
    ref_lines = "\n".join(f"- {ref}" for ref in refs) or "- NONE (no evidence refs supplied)"
    l5_required = "YES" if record["l5_required"] else "NO"
    return (
        f"You are executing a bounded, non-modifying Dealix arm experiment for {arm_id} "
        f"({record['name']}).\n"
        f"First experiment: {record['next_safe_action']}\n"
        f"Horizon: {record['horizon']}; promotion gate: {record['promotion_gate']}; "
        f"evidence tier: {record['evidence']['tier']}.\n\n"
        "Evidence / context refs (use only these; never invent):\n"
        f"{ref_lines}\n\n"
        "Truth laws (non-negotiable):\n"
        "- research != relationship; public_contact != consent; proposal_view != buying_decision\n"
        "- quote != invoice; invoice != payment; synthetic != customer_proof; deployment != correct_release\n"
        "- Never invent ROI, pipeline, revenue, buyer intent, consent or proof.\n"
        "- relationship/pipeline/revenue truth stays exactly as evidenced (default false).\n\n"
        "Hard constraints:\n"
        "- No external effect: no send, publish, post, pay, spend, deploy, DNS, DB or secret action.\n"
        "- No repository modification: do not edit, create or delete files; do not commit, push or merge.\n"
        "- Analysis and drafts only; L5 material effects are out of scope.\n\n"
        "Return a concise structured final receipt that contains this exact marker on its own line:\n"
        f"{marker}\n"
        "followed by these labelled fields:\n"
        "- FINDINGS: <concise findings>\n"
        f"- EVIDENCE_REFS_USED: <comma-separated refs actually used, or NONE>\n"
        "- RELATIONSHIP_TRUTH: <what is evidenced, else NONE>\n"
        "- PIPELINE_TRUTH: <false unless evidenced, else NONE>\n"
        "- REVENUE_TRUTH: <false unless evidenced, else NONE>\n"
        f"- NEXT_SAFE_ACTION: {record['next_safe_action']}\n"
        f"- L5_REQUIRED: {l5_required}\n"
    )


def build_job(record: dict[str, Any], *, repo_root: Path | None = None) -> dict[str, Any]:
    """Build a session-factory job for one record. Never executes it here.

    The prompt is non-modifying and the acceptance gate is fail-closed: the job
    only succeeds when the executor exits zero AND prints the exact
    ``ARM_PORTFOLIO_RECEIPT:<ARM-ID>`` marker in its stdout.
    """
    factory = session_factory()
    job_class = record["model_job_class"]["job_class"]
    authority = record["model_job_class"]["authority_level"]
    context_marker = f"arm_portfolio:{record['arm_id']}"
    receipt_marker = f"{RECEIPT_MARKER_PREFIX}{record['arm_id']}"
    context_refs = [context_marker, *(record.get("evidence_refs") or [])][:8]
    job = factory.make_job(
        owner_agent=str(record["owner"]),
        business_goal=f"[{record['arm_id']}] {record['name']}: {record['horizon']} first experiment",
        job_class=job_class,
        authority_level=authority,
        economic_reason=(
            f"score={record['score']['total']} tier={record['evidence']['tier']} "
            f"gate={record['promotion_gate']} heuristic={SCORE_SEMANTICS}"
        ),
        priority=float(record["score"]["total"]),
        modifying=False,
        executor={"prompt": build_arm_job_prompt(record)},
        acceptance={
            "criteria": (
                "exit zero AND stdout contains the exact receipt marker "
                f"{receipt_marker}; no external effect; no repository modification"
            ),
            "checks": [
                {"kind": "exit_zero"},
                {"kind": "stdout_contains", "text": receipt_marker},
            ],
        },
        context_refs=context_refs,
        next_action=record["next_safe_action"],
    )
    if repo_root is not None:
        job["REPO"] = str(repo_root)
    return job


def already_enqueued(root: Path, marker: str) -> bool:
    """True if an active (non-terminal) job already carries this arm marker."""
    factory = session_factory()
    for job in factory.all_jobs(Path(root)):
        if job.get("STATUS") in TERMINAL_JOB_STATES:
            continue
        if marker in (job.get("CONTEXT_REFS") or []):
            return True
    return False


def render_help() -> str:
    return (
        "Hermes arm portfolio controller (planning only). "
        f"Use scripts/ops/run_hermes_arm_portfolio_once.py for the one-shot runner. "
        f"Schedule unchanged; L5 policy={L5_POLICY}."
    )


__all__ = [
    "CLASS_DEEP",
    "CLASS_HOLD",
    "CLASS_LIGHT",
    "DEFAULT_EVIDENCE_PATH",
    "EVIDENCE_SCHEMA",
    "L5_POLICY",
    "PLAYBOOKS_PATH",
    "RECEIPT_MARKER_PREFIX",
    "REGISTRY_PATH",
    "SCHEMA",
    "SCORE_SEMANTICS",
    "already_enqueued",
    "build_arm_job_prompt",
    "build_job",
    "build_record",
    "contract_failures",
    "evidence_tier",
    "load_evidence",
    "load_playbooks",
    "load_registry",
    "model_job_class",
    "normalize_evidence",
    "plan_portfolio",
    "render_help",
    "render_summary",
    "score_arm",
    "tripwires",
    "write_plan",
]
