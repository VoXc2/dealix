from scripts.ops.software_acquisition_factory import LEGACY_SCHEMA, SCHEMA, SCORE_FIELDS, decide

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
        "installation_tiers": {"dependency_sandbox": "L3_INTERNAL"},
        "deep_wip_max": 3,
    }


def base_candidate(schema: str = SCHEMA) -> dict:
    return {
        "schema": schema,
        "candidate_id": "edge-tool",
        "name": "Edge Tool",
        "source": "official",
        "official_url": "https://example.invalid/tool",
        "repo": "https://example.invalid/repo",
        "version": "1.0.0",
        "commit_sha": "abc123",
        "image_digest": "sha256:123",
        "artifact_type": "executable",
        "license": "Apache-2.0",
        "purpose": "edge coverage",
        "dealix_gap": "safe acquisition",
        "scores": dict.fromkeys(SCORE_FIELDS, 90),
        "duplicate_of_existing": "",
        "replacement_of_existing": "",
        "rollback_method": "discard sandbox",
        "sbom_path": "sbom.cdx.json",
        "vulnerability_status": "CLEAR",
        "cisa_kev_match": False,
        "signature_status": "UNKNOWN",
        "provenance_status": "NOT_APPLICABLE",
        "requires_secret_dump": False,
        "capability_map": dict.fromkeys(CAPABILITY_FIELDS, False),
        "install_surface": "dependency_sandbox",
        "evidence_refs": ["evidence://official"],
    }


def test_high_risk_not_applicable_provenance_is_not_accepted() -> None:
    decision = decide(base_candidate(), policy())
    assert decision.decision == "HOLD_PROVENANCE"


def test_legacy_high_risk_candidate_without_capability_map_is_not_auto_sandboxed() -> None:
    item = base_candidate(schema=LEGACY_SCHEMA)
    item["signature_status"] = "VERIFIED"
    item["provenance_status"] = "VERIFIED"
    item.pop("capability_map")
    decision = decide(item, policy())
    assert decision.decision == "HOLD_CAPABILITY_RISK"
    assert "unknown_capability_scope" in decision.capability_risks
