"""Schema + safety tests for docs/registry/SERVICE_READINESS_MATRIX.yaml.

These run in CI on every push and protect the invariants the
Service Activation Console relies on:
  - 32 services exactly (the matrix is the source of truth)
  - 0 Live, 1 Pilot, 7 Partial, 24 Target, 0 Blocked (current honest state)
  - All required fields present per service
  - No forbidden marketing claims in customer-visible copy
  - All bundles defined; every service maps to an allowed bundle
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs" / "registry" / "SERVICE_READINESS_MATRIX.yaml"

ALLOWED_STATUSES = {"live", "pilot", "partial", "target", "blocked", "backlog"}
ALLOWED_BUNDLES = {
    "growth_starter",
    "data_to_revenue",
    "executive_growth_os",
    "partnership_growth",
    "full_control_tower",
    "internal",
}
REQUIRED_FIELDS = [
    "service_id", "name_ar", "name_en", "bundle", "capability_group",
    "status", "customer_value_ar", "customer_value_en",
    "target_customer_ar", "target_customer_en",
    "what_it_does_ar", "what_it_does_en",
    "required_inputs", "workflow_steps", "channels",
    "safe_action_policy", "approval_required", "blocked_actions",
    "deliverables", "proof_metrics", "api_endpoints",
    "frontend_surfaces", "data_dependencies",
    "integration_dependencies", "owner",
    "next_activation_step_ar", "next_activation_step_en",
    "definition_of_live", "tests_required", "risks",
    "sla", "last_verified_at", "evidence",
]
ALLOWED_CONTEXT_FIELDS = {
    "blocked_actions", "safe_action_policy", "risks",
    "next_activation_step_ar", "next_activation_step_en",
}
FORBIDDEN_AR = [r"نضمن", r"مضمون"]
FORBIDDEN_EN = [
    r"\bguaranteed?\b",
    r"\bblast\b",
    r"\bscrape\b",
    r"\bscraping\b",
    r"\bcold\s+(whatsapp|outreach|email|messaging)\b",
]


@pytest.fixture(scope="module")
def matrix() -> dict:
    with MATRIX.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_matrix_loads(matrix):
    assert isinstance(matrix, dict)
    assert "services" in matrix and matrix["services"]


def test_total_services_is_32(matrix):
    assert len(matrix["services"]) == 32


def test_status_distribution(matrix):
    """After Phase K1+K2+K3 (PR #165 + PR #166), 3 services flipped to
    live: qualification, audit_trail, lead_intake_whatsapp. Each has
    its full 8 quality gates set true and a tests_required: file that
    exists on disk — verify_service_readiness_matrix.py enforces this.
    """
    counts = {s: 0 for s in ALLOWED_STATUSES}
    for svc in matrix["services"]:
        counts[svc["status"]] += 1
    assert counts["live"] == 3, "3 services flipped to live after Phase K1+K2+K3"
    assert counts["pilot"] == 0
    assert counts["partial"] == 5
    assert counts["target"] == 24
    assert counts["blocked"] == 0


def test_required_fields_present(matrix):
    missing = []
    for svc in matrix["services"]:
        sid = svc.get("service_id", "<unknown>")
        for f in REQUIRED_FIELDS:
            if f not in svc:
                missing.append(f"{sid}.{f}")
    assert not missing, f"missing fields: {missing}"


def test_status_enum(matrix):
    for svc in matrix["services"]:
        assert svc["status"] in ALLOWED_STATUSES


def test_bundle_enum(matrix):
    for svc in matrix["services"]:
        assert svc["bundle"] in ALLOWED_BUNDLES


def test_bundles_block_complete(matrix):
    bundles = {b["id"] for b in matrix.get("bundles", [])}
    assert ALLOWED_BUNDLES.issubset(bundles)


def test_unique_service_ids(matrix):
    ids = [s["service_id"] for s in matrix["services"]]
    assert len(ids) == len(set(ids))


def test_no_forbidden_claims_in_visible_copy(matrix):
    """Customer-visible copy must not contain forbidden marketing claims.
    blocked_actions / safe_action_policy / risks / next_activation_step_*
    are allowed to *describe* what we don't do.
    """
    violations: list[str] = []
    for svc in matrix["services"]:
        sid = svc["service_id"]
        for field, value in svc.items():
            if field in ALLOWED_CONTEXT_FIELDS:
                continue
            texts: list[str] = []
            if isinstance(value, str):
                texts.append(value)
            elif isinstance(value, list):
                texts.extend([str(v) for v in value])
            for t in texts:
                for pat in FORBIDDEN_AR + FORBIDDEN_EN:
                    if re.search(pat, t, flags=re.IGNORECASE):
                        violations.append(f"{sid}.{field}: {pat!r}")
    assert not violations, f"forbidden claims found: {violations}"


def test_live_status_requires_gates(matrix):
    """If any service is marked live, it must have a gates: block with all 8 gates true."""
    for svc in matrix["services"]:
        if svc["status"] != "live":
            continue
        gates = svc.get("gates", {})
        for g in [
            "inputs", "workflow", "agent_role", "human_approval",
            "safe_tool_gateway", "deliverable", "proof_metric", "test_or_evidence",
        ]:
            assert gates.get(g), f"{svc['service_id']}: missing gate.{g}"


def test_evidence_paths_exist(matrix):
    missing = []
    for svc in matrix["services"]:
        for ev in svc.get("evidence", []) or []:
            if not isinstance(ev, str):
                continue
            if not (REPO / ev).exists():
                missing.append(f"{svc['service_id']}: {ev}")
    assert not missing, f"missing evidence files: {missing}"
