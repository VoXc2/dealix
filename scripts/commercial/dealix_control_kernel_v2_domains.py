#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
KERNEL_PATH = ROOT / "config" / "company" / "dealix_control_kernel_v2.json"


class DomainContractError(ValueError):
    pass


def load_kernel(path: Path = KERNEL_PATH) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise DomainContractError("kernel_root_not_object")
    return data


def _required(record: dict[str, Any], fields: list[str], code: str) -> None:
    missing = [field for field in fields if field not in record or record[field] in (None, "", [], {})]
    if missing:
        raise DomainContractError(f"{code}:" + ",".join(sorted(missing)))


def _bounded01(name: str, value: Any) -> float:
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise DomainContractError(f"{name}_outside_0_1")
    return number


def validate_workload_binding(binding: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    fields = [str(x) for x in kernel["identity"]["material_binding_fields"]]
    _required(binding, fields, "WORKLOAD_BINDING_MISSING")
    if str(binding.get("agent_id", "")) == str(binding.get("workload_id", "")):
        raise DomainContractError("AGENT_IDENTITY_MUST_DIFFER_FROM_WORKLOAD_IDENTITY")


def validate_durable_task(task: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    cfg = kernel["long_running_tasks"]
    _required(task, [str(x) for x in cfg["fields"]], "TASK_FIELD_MISSING")
    if task["state"] not in cfg["states"]:
        raise DomainContractError("INVALID_TASK_STATE")


def validate_customer_memory(record: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    fields = [str(x) for x in kernel["customer_memory"]["record_fields"]]
    _required(record, fields, "CUSTOMER_MEMORY_FIELD_MISSING")
    if str(record["tenant"]).strip().upper() in {"GLOBAL", "ALL", "*"}:
        raise DomainContractError("GLOBAL_CUSTOMER_MEMORY_FORBIDDEN")
    if str(record["purpose"]).strip().upper() in {"ANY", "UNBOUNDED", "*"}:
        raise DomainContractError("UNBOUNDED_CUSTOMER_MEMORY_PURPOSE_FORBIDDEN")


def validate_relationship_change(
    *,
    from_state: str,
    to_state: str,
    evidence: list[str] | None,
    kernel: dict[str, Any] | None = None,
) -> None:
    kernel = kernel or load_kernel()
    states = [str(x) for x in kernel["relationship_graph"]["states"]]
    if from_state not in states or to_state not in states:
        raise DomainContractError("INVALID_RELATIONSHIP_STATE")
    if states.index(to_state) > states.index(from_state) and not evidence:
        raise DomainContractError("RELATIONSHIP_PROMOTION_REQUIRES_EVIDENCE")


def validate_model_change(
    *,
    from_state: str,
    to_state: str,
    evidence: dict[str, Any] | None,
    kernel: dict[str, Any] | None = None,
) -> None:
    kernel = kernel or load_kernel()
    cfg = kernel["model_change"]
    lifecycle = [str(x) for x in cfg["lifecycle"]]
    if from_state not in lifecycle or to_state not in lifecycle:
        raise DomainContractError("INVALID_MODEL_LIFECYCLE_STATE")
    if from_state == to_state:
        return
    evidence = evidence or {}
    required_dimensions = [str(x) for x in cfg["evidence_dimensions"]]
    missing = [name for name in required_dimensions if name not in evidence or evidence[name] in (None, "", [], {})]
    if missing:
        raise DomainContractError("MODEL_CHANGE_EVIDENCE_MISSING:" + ",".join(sorted(missing)))


def validate_canary_transition(
    *,
    from_state: str,
    to_state: str,
    rollback_defined: bool,
    kernel: dict[str, Any] | None = None,
) -> None:
    kernel = kernel or load_kernel()
    progression = [str(x) for x in kernel["canary_autonomy"]["progression"]]
    if from_state not in progression or to_state not in progression:
        raise DomainContractError("INVALID_CANARY_STATE")
    from_index = progression.index(from_state)
    to_index = progression.index(to_state)
    if to_index > from_index:
        if to_index != from_index + 1:
            raise DomainContractError("CANARY_PROMOTION_MUST_BE_INCREMENTAL")
        if not rollback_defined:
            raise DomainContractError("CANARY_ROLLBACK_REQUIRED_BEFORE_PROMOTION")


def autonomy_degradation_response(trigger: str, kernel: dict[str, Any] | None = None) -> list[str]:
    kernel = kernel or load_kernel()
    cfg = kernel["autonomy_degradation"]
    if trigger not in cfg["triggers"]:
        raise DomainContractError("UNKNOWN_AUTONOMY_DEGRADATION_TRIGGER")
    return [str(x) for x in cfg["response"]]


def validate_external_a2a(request: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    fields = [str(x).lower() for x in kernel["a2a_boundary"]["requirements"]]
    normalized = {str(k).lower(): v for k, v in request.items()}
    _required(normalized, fields, "EXTERNAL_A2A_REQUIREMENT_MISSING")
    if normalized.get("verified_agent_card") is not True:
        raise DomainContractError("EXTERNAL_AGENT_CARD_NOT_VERIFIED")
    if normalized.get("policy_evaluation") not in {"ALLOW", "REQUIRE_APPROVAL"}:
        raise DomainContractError("EXTERNAL_A2A_POLICY_NOT_ACCEPTABLE")


def validate_regulatory_signal(signal: dict[str, Any], *, authoritative_source: bool, kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    cfg = kernel["regulatory_radar"]
    if cfg["sources_must_be_authoritative"] and not authoritative_source:
        raise DomainContractError("REGULATORY_SOURCE_NOT_AUTHORITATIVE")
    _required(signal, [str(x) for x in cfg["signal_fields"]], "REGULATORY_SIGNAL_FIELD_MISSING")
    if signal.get("classification") not in cfg["classifications"]:
        raise DomainContractError("INVALID_REGULATORY_CLASSIFICATION")


def classify_demand_evidence(evidence_types: list[str], kernel: dict[str, Any] | None = None) -> str:
    kernel = kernel or load_kernel()
    allowed = set(str(x) for x in kernel["demand_radar"]["purchase_evidence"])
    found = allowed.intersection(str(x) for x in evidence_types)
    return "PURCHASE_SIGNAL" if found else "MARKET_HYPE_OR_UNPROVEN_DEMAND"


def validate_company_twin(twin: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    _required(twin, [str(x) for x in kernel["company_twin"]["fields"]], "COMPANY_TWIN_FIELD_MISSING")
    if twin.get("source_system") == "INDEPENDENT_COMPANY_BRAIN":
        raise DomainContractError("COMPANY_TWIN_CANNOT_BECOME_SECOND_BRAIN")


def derive_company_twin(canonical_state: dict[str, Any], kernel: dict[str, Any] | None = None) -> dict[str, Any]:
    """Create a derived projection only; never create independent authority or storage."""
    kernel = kernel or load_kernel()
    fields = [str(x) for x in kernel["company_twin"]["fields"]]
    twin = {field: canonical_state.get(field) for field in fields}
    twin["source_system"] = "DERIVED_PROJECTION"
    validate_company_twin(twin, kernel=kernel)
    return twin


def validate_proof_dimensions(dimensions: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    required = [str(x) for x in kernel["proof_compounding_index"]["dimensions"]]
    _required(dimensions, required, "PROOF_DIMENSION_MISSING")
    for name in required:
        _bounded01(name, dimensions[name])


def validate_repeatability_dimensions(dimensions: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    required = [str(x) for x in kernel["repeatability_index"]["dimensions"]]
    _required(dimensions, required, "REPEATABILITY_DIMENSION_MISSING")
    for name in required:
        _bounded01(name, dimensions[name])


def validate_automation_roi_inputs(record: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    """Validate inputs without inventing the missing aggregation formula."""
    kernel = kernel or load_kernel()
    cfg = kernel["automation_roi"]
    _required(record, [str(x) for x in cfg["record"]], "AUTOMATION_ROI_RECORD_FIELD_MISSING")
    _required(record, [str(x) for x in cfg["required_components"]], "AUTOMATION_ROI_COMPONENT_MISSING")
    if cfg.get("operator_relationship") != "UNSPECIFIED_IN_FOUNDER_TEXT":
        raise DomainContractError("AUTOMATION_ROI_OPERATOR_DRIFT")
    if cfg.get("aggregation_requires_explicit_policy") is not True:
        raise DomainContractError("AUTOMATION_ROI_AGGREGATION_MUST_BE_EXPLICIT")


def validate_agent_scorecard(scorecard: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    cfg = kernel["agent_scorecard"]
    _required(scorecard, [str(x) for x in cfg["metrics"]], "AGENT_SCORECARD_METRIC_MISSING")
    rewarded = set(str(x) for x in scorecard.get("rewarded_metrics", []))
    forbidden = set(str(x) for x in cfg["do_not_reward"])
    if rewarded.intersection(forbidden):
        raise DomainContractError("AGENT_ACTIVITY_METRIC_CANNOT_BE_REWARDED")


def validate_founder_request(packet: dict[str, Any], kernel: dict[str, Any] | None = None) -> None:
    kernel = kernel or load_kernel()
    cfg = kernel["minimum_founder_surface"]
    if packet.get("action") not in cfg["founder_actions"]:
        raise DomainContractError("FOUNDER_SURFACE_VIOLATION")
    _required(packet, [str(x) for x in cfg["request_packet_fields"]], "FOUNDER_PACKET_FIELD_MISSING")


def self_healing_decision(action: str, kernel: dict[str, Any] | None = None) -> str:
    kernel = kernel or load_kernel()
    cfg = kernel["self_healing"]
    if action in cfg["forbidden"]:
        return "DENY"
    if action in cfg["allowed"]:
        return "ALLOW_BOUNDED"
    return "REQUIRE_POLICY_REVIEW"
