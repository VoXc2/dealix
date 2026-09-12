#!/usr/bin/env python3
"""Verify that Dealix Agentic Holding policy, contract and constitution agree."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "config/company/fresh_market_execution_policy.json"
CONTRACT_PATH = ROOT / "config/company/agentic_holding_canonical_contract.json"
CONSTITUTION_PATH = ROOT / "docs/architecture/DEALIX_AGENTIC_HOLDING_CANONICAL_2026_09_12.md"


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected object: {path}")
    return value


def verify() -> dict[str, object]:
    failures: list[str] = []
    for path in (POLICY_PATH, CONTRACT_PATH, CONSTITUTION_PATH):
        if not path.is_file():
            failures.append(f"missing:{path.relative_to(ROOT)}")
    if failures:
        return {"verdict": "FAIL", "failures": failures}

    policy = _load_json(POLICY_PATH)
    contract = _load_json(CONTRACT_PATH)
    constitution = CONSTITUTION_PATH.read_text(encoding="utf-8")

    architecture = policy.get("architecture", {})
    execution = policy.get("execution", {})
    security = policy.get("connector_security", {})
    observability = policy.get("observability", {})
    authority = policy.get("authority", {})

    if architecture.get("model") != "agentic_holding_sector_company_mesh":
        failures.append("architecture_model_drift")
    if architecture.get("status") != "CANONICAL":
        failures.append("architecture_not_canonical")
    if architecture.get("canonical_source") != str(CONSTITUTION_PATH.relative_to(ROOT)).replace("\\", "/"):
        failures.append("canonical_source_mismatch")
    if architecture.get("canonical_contract") != str(CONTRACT_PATH.relative_to(ROOT)).replace("\\", "/"):
        failures.append("canonical_contract_mismatch")

    if contract.get("status") != "CANONICAL":
        failures.append("contract_not_canonical")
    if contract.get("architecture") != architecture.get("model"):
        failures.append("contract_architecture_mismatch")
    if contract.get("architecture_source") != architecture.get("canonical_source"):
        failures.append("contract_source_mismatch")

    one_company = contract.get("one_company_law", {})
    for field in (
        "single_company_machine",
        "single_company_brain",
        "single_economic_truth",
        "single_approval_path",
        "single_proof_path",
        "single_scheduler",
        "single_model_routing_policy",
        "parallel_sector_businesses_forbidden",
    ):
        if one_company.get(field) is not True:
            failures.append(f"one_company_law:{field}")

    agent_model = contract.get("agent_model", {})
    if agent_model.get("logical_agents") != "dynamic_hierarchical_registry":
        failures.append("logical_agent_registry_drift")
    if agent_model.get("runtime_workers") != "lazy_resource_governed":
        failures.append("runtime_worker_model_drift")
    if agent_model.get("orphan_agents_allowed") is not False:
        failures.append("orphan_agents_enabled")
    if agent_model.get("process_per_logical_agent_forbidden") is not True:
        failures.append("process_per_agent_not_forbidden")

    coordination = contract.get("coordination", {})
    if coordination.get("implicit_authority_transfer_forbidden") is not True:
        failures.append("implicit_authority_transfer_enabled")
    if coordination.get("handoff_pattern", {}).get("authorization_before_side_effects") is not True:
        failures.append("handoff_authorization_not_pre_side_effect")
    if coordination.get("handoff_pattern", {}).get("receiving_agent_context_is_filtered") is not True:
        failures.append("handoff_context_not_filtered")

    guardrails = contract.get("guardrails", {})
    if guardrails.get("blocking_before_side_effects") is not True:
        failures.append("blocking_guardrails_disabled")
    if guardrails.get("self_approval_forbidden") is not True:
        failures.append("self_approval_enabled")
    if guardrails.get("model_output_is_authority") is not False:
        failures.append("model_output_authority_enabled")

    traces = contract.get("tracing_and_receipts", {})
    required_trace_events = {"model_call", "tool_call", "handoff", "guardrail", "approval_check", "acceptance_check", "receipt"}
    if traces.get("end_to_end_trace_required") is not True:
        failures.append("end_to_end_trace_disabled")
    if not required_trace_events <= set(traces.get("trace_events", [])):
        failures.append("trace_event_coverage_incomplete")
    if traces.get("acceptance_receipt_required") is not True:
        failures.append("acceptance_receipt_disabled")

    mcp = contract.get("mcp_and_connector_security", {})
    for field in (
        "issuer_validation_required",
        "credentials_issuer_bound",
        "resource_bound_tokens_required",
        "token_passthrough_forbidden",
        "agent_identity_and_delegated_scope_must_be_explicit",
        "ssrf_protection_for_remote_metadata_fetch",
        "credentials_never_enter_prompt_context",
    ):
        if mcp.get(field) is not True:
            failures.append(f"mcp_security:{field}")

    if execution.get("handoff_contract_required") is not True:
        failures.append("policy_handoff_contract_disabled")
    if execution.get("blocking_guardrails_before_material_side_effects") is not True:
        failures.append("policy_blocking_guardrails_disabled")
    if execution.get("paid_spill_default") is not False:
        failures.append("paid_spill_enabled")
    if execution.get("verifier_required_for_material_outputs") is not True:
        failures.append("material_verifier_disabled")
    if security.get("token_passthrough_forbidden") is not True:
        failures.append("policy_token_passthrough_enabled")
    if observability.get("end_to_end_trace_required") is not True:
        failures.append("policy_trace_disabled")
    if authority.get("implicit_authority_transfer_forbidden") is not True:
        failures.append("policy_implicit_authority_enabled")
    if authority.get("self_approval_forbidden") is not True:
        failures.append("policy_self_approval_enabled")

    if "**Status:** CANONICAL" not in constitution:
        failures.append("constitution_not_canonical")
    if "config/company/agentic_holding_canonical_contract.json" not in constitution:
        failures.append("constitution_contract_link_missing")

    basis = contract.get("research_basis", [])
    if len(basis) < 6:
        failures.append("research_basis_incomplete")
    if any(not str(row.get("url", "")).startswith("https://") for row in basis if isinstance(row, dict)):
        failures.append("research_basis_url_invalid")

    return {
        "verdict": "FAIL" if failures else "PASS",
        "architecture": architecture.get("model"),
        "status": architecture.get("status"),
        "logical_agents": agent_model.get("logical_agents"),
        "runtime_workers": agent_model.get("runtime_workers"),
        "coordination": coordination.get("default_pattern"),
        "blocking_guardrails": guardrails.get("blocking_before_side_effects"),
        "end_to_end_trace": traces.get("end_to_end_trace_required"),
        "token_passthrough_forbidden": mcp.get("token_passthrough_forbidden"),
        "issuer_validation_required": mcp.get("issuer_validation_required"),
        "paid_spill_default": execution.get("paid_spill_default"),
        "external_authority": authority.get("material_external_actions"),
        "research_sources": len(basis),
        "failures": failures,
    }


def main() -> int:
    receipt = verify()
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(f"DEALIX_AGENTIC_HOLDING_CANONICAL={receipt['verdict']}")
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
