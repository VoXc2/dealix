from __future__ import annotations

import json
from pathlib import Path

from scripts.ops.software_acquisition_factory import (
    DECISION_SCHEMA,
    SCHEMA,
    SCORE_FIELDS,
    build_job,
    decide,
    process_candidates,
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
        "thresholds": {"auto_sandbox_min": 80, "research_more_min": 65},
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
        "license": "Apache-2.0",
        "purpose": "reduce repetitive engineering toil",
        "dealix_gap": "automate safe maintenance",
        "scores": {field: 90 for field in SCORE_FIELDS},
        "monthly_cost": 0,
        "resource_cost": "LOW",
        "alternatives": [],
        "duplicate_of_existing": "",
        "rollback_method": "remove isolated worktree/container",
        "sbom_path": "sbom.cdx.json",
        "vulnerability_status": "CLEAR",
        "signature_status": "VERIFIED",
        "requires_secret_dump": False,
        "install_surface": "dependency_sandbox",
        "sandbox_result": "NOT_RUN",
        "benchmark_result": "NOT_RUN",
        "evidence_refs": ["evidence://official"],
    }
    item.update(overrides)
    return item


def test_high_score_candidate_goes_to_auto_sandbox() -> None:
    decision = decide(candidate(), policy())
    assert decision.decision == "AUTO_SANDBOX"
    assert decision.score == 90.0
    assert decision.auto_executable is True
    assert decision.as_dict()["schema"] == DECISION_SCHEMA


def test_unknown_license_fails_closed() -> None:
    decision = decide(candidate(license="UNKNOWN"), policy())
    assert decision.decision == "HOLD_LICENSE"
    assert decision.auto_executable is False


def test_duplicate_is_rejected_before_score_can_promote() -> None:
    decision = decide(candidate(duplicate_of_existing="existing://tool"), policy())
    assert decision.decision == "REJECT_DUPLICATE"


def test_critical_vulnerability_is_rejected() -> None:
    decision = decide(candidate(vulnerability_status="CRITICAL"), policy())
    assert decision.decision == "REJECT_SECURITY"


def test_l5_surface_is_identified_but_sandbox_job_stays_l4() -> None:
    item = candidate(install_surface="production")
    decision = decide(item, policy())
    assert decision.required_authority == "L5_REQUIRED"
    job = build_job(item, decision, base_sha="deadbeef")
    assert job is not None
    assert job["AUTHORITY_LEVEL"] == "L4"
    assert "Do not merge, deploy" in job["EXECUTOR"]["prompt"]


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
