from __future__ import annotations

import json
from pathlib import Path

from scripts.ops.software_acquisition_factory import (
    DECISION_SCHEMA,
    LEGACY_SCHEMA,
    SCHEMA,
    SCORE_FIELDS,
    build_job,
    decide,
    process_candidates,
)

CAPABILITY_FIELDS = (
    "privileged",
    "host_docker_socket",
    "host_network",
    "unrestricted_egress",
    "broad_filesystem_write",
    "broad_secret_access",
    "kernel_device_access",
    "firewall_mutation",
)


def policy() -> dict:
    return {
        "weights": {
            "business_value": 0.30,
            "security": 0.20,
            "maturity": 0.15,
            "maintenance": 0.10,
            "integration_fit": 0.10,
            "license": 0.05,
            "cost": 0.05,
            "reversibility": 0.05,
        },
        "thresholds": {
            "auto_sandbox_min": 80,
            "research_more_min": 65,
            "auto_sandbox_evidence_min": 80,
        },
        "evidence_confidence_weights": {
            "official_source": 15,
            "immutable_pin": 15,
            "verified_license": 10,
            "vulnerability_evidence": 15,
            "rollback": 10,
            "evidence_refs": 10,
            "sbom": 10,
            "provenance": 10,
            "capability_map": 5,
        },
        "high_risk_artifact_types": [
            "executable",
            "container_image",
            "mcp_server",
            "agent_runtime",
            "installer",
            "system_service",
        ],
        "capability_risk_fields": list(CAPABILITY_FIELDS),
        "installation_tiers": {
            "dependency_sandbox": "L3_INTERNAL",
            "repo_integration": "L4_REPO_EXECUTE",
            "production": "L5_REQUIRED",
        },
        "deep_wip_max": 3,
    }


def candidate(**overrides) -> dict:
    item = {
        "schema": SCHEMA,
        "candidate_id": "tool-1",
        "name": "Useful Tool",
        "source": "official",
        "official_url": "https://example.invalid/tool",
        "repo": "https://example.invalid/repo",
        "version": "1.2.3",
        "commit_sha": "abc123",
        "image_digest": "sha256:123",
        "artifact_type": "source_library",
        "license": "Apache-2.0",
        "purpose": "reduce repetitive engineering toil",
        "dealix_gap": "automate safe maintenance",
        "scores": dict.fromkeys(SCORE_FIELDS, 90),
        "monthly_cost": 0,
        "resource_cost": "LOW",
        "alternatives": [],
        "duplicate_of_existing": "",
        "replacement_of_existing": "",
        "rollback_method": "remove isolated worktree/container",
        "sbom_path": "sbom.cdx.json",
        "sbom_status": "VERIFIED",
        "vulnerability_status": "CLEAR",
        "cisa_kev_match": False,
        "epss_score": 0.001,
        "signature_status": "VERIFIED",
        "provenance_status": "VERIFIED",
        "requires_secret_dump": False,
        "capability_map": dict.fromkeys(CAPABILITY_FIELDS, False),
        "network_allowlist": [],
        "data_egress": "DENY_BY_DEFAULT",
        "install_surface": "dependency_sandbox",
        "sandbox_result": "NOT_RUN",
        "benchmark_result": "NOT_RUN",
        "evidence_refs": ["evidence://official"],
    }
    item.update(overrides)
    return item


def test_high_score_candidate_goes_to_auto_sandbox_only_with_evidence() -> None:
    decision = decide(candidate(), policy())
    assert decision.decision == "AUTO_SANDBOX"
    assert decision.score == 90.0
    assert decision.evidence_confidence == 100.0
    assert decision.auto_executable is True
    assert decision.as_dict()["schema"] == DECISION_SCHEMA


def test_high_value_low_evidence_routes_to_research_more() -> None:
    decision = decide(
        candidate(
            vulnerability_status="UNKNOWN",
            sbom_path="",
            sbom_status="UNKNOWN",
            signature_status="UNKNOWN",
            provenance_status="UNKNOWN",
            evidence_refs=[],
        ),
        policy(),
    )
    assert decision.score == 90.0
    assert decision.evidence_confidence < 80
    assert decision.decision == "RESEARCH_MORE"


def test_unknown_license_fails_closed() -> None:
    decision = decide(candidate(license="UNKNOWN"), policy())
    assert decision.decision == "HOLD_LICENSE"
    assert decision.auto_executable is False


def test_duplicate_is_rejected_before_score_can_promote() -> None:
    decision = decide(candidate(duplicate_of_existing="existing://tool"), policy())
    assert decision.decision == "REJECT_DUPLICATE"


def test_explicit_replacement_is_not_rejected_as_duplicate() -> None:
    decision = decide(
        candidate(duplicate_of_existing="existing://tool", replacement_of_existing="existing://tool"),
        policy(),
    )
    assert decision.decision == "AUTO_SANDBOX"


def test_critical_vulnerability_is_rejected() -> None:
    decision = decide(candidate(vulnerability_status="CRITICAL"), policy())
    assert decision.decision == "REJECT_SECURITY"


def test_cisa_kev_match_quarantines() -> None:
    decision = decide(candidate(cisa_kev_match=True), policy())
    assert decision.decision == "QUARANTINE_KEV"
    assert decision.auto_executable is False


def test_high_risk_executable_missing_provenance_is_held() -> None:
    decision = decide(
        candidate(
            artifact_type="executable",
            signature_status="UNKNOWN",
            provenance_status="UNKNOWN",
        ),
        policy(),
    )
    assert decision.decision == "HOLD_PROVENANCE"


def test_dangerous_capability_does_not_auto_execute() -> None:
    capabilities = dict.fromkeys(CAPABILITY_FIELDS, False)
    capabilities["host_docker_socket"] = True
    decision = decide(candidate(capability_map=capabilities), policy())
    assert decision.decision == "HOLD_CAPABILITY_RISK"
    assert "host_docker_socket" in decision.capability_risks


def test_legacy_v1_candidate_remains_safely_readable() -> None:
    item = candidate(schema=LEGACY_SCHEMA)
    item.pop("capability_map")
    decision = decide(item, policy())
    assert decision.decision == "AUTO_SANDBOX"
    assert decision.evidence_confidence >= 80


def test_l5_surface_is_identified_but_sandbox_job_stays_l4() -> None:
    item = candidate(install_surface="production")
    decision = decide(item, policy())
    assert decision.required_authority == "L5_REQUIRED"
    job = build_job(item, decision, base_sha="deadbeef")
    assert job is not None
    assert job["AUTHORITY_LEVEL"] == "L4"
    prompt = job["EXECUTOR"]["prompt"]
    assert "never privileged" in prompt
    assert "never mount the host Docker socket" in prompt
    assert "deny or allowlist network egress" in prompt
    assert "Do not merge, deploy" in prompt


def test_process_candidates_submits_at_most_three_jobs(tmp_path: Path) -> None:
    items = []
    for index in range(5):
        item = candidate(candidate_id=f"tool-{index}", name=f"Tool {index}")
        items.append(item)
    result = process_candidates(
        items,
        policy=policy(),
        base_sha="deadbeef",
        enqueue=True,
        session_state=tmp_path / "session",
        max_jobs=3,
    )
    assert result["candidate_count"] == 5
    assert len(result["submitted_jobs"]) == 3
    assert result["l5_executed"] == "NONE"
    for receipt in result["submitted_jobs"]:
        assert receipt["ok"] is True
        assert receipt["status"] == "READY"
    queue = json.loads((tmp_path / "session" / "AUTONOMOUS_JOB_QUEUE.json").read_text())
    assert queue["counts"]["READY"] == 3
