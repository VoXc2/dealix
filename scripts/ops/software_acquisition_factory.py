#!/usr/bin/env python3
"""Dealix Software Acquisition & Evolution Factory.

Governed intake/planning layer on top of the canonical Hermes Session Factory.
It never installs software directly and never creates another scheduler or
execution plane.

V2 separates three independent questions:
1. Is the candidate valuable?
2. Is the supply-chain evidence trustworthy enough?
3. Is the requested capability/blast radius acceptable?

A high business-value score never overrides failed trust or capability gates.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
OPS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(OPS_DIR))

from session_factory import make_job, submit_job

POLICY_PATH = REPO_ROOT / "config/company/software_acquisition_policy.json"
DEFAULT_REGISTRY = Path(
    os.environ.get(
        "DEALIX_SOFTWARE_ACQUISITION_REGISTRY",
        "/opt/dealix/control/state/software_acquisition/CANDIDATE_REGISTRY.json",
    )
)
DEFAULT_STATE = Path(
    os.environ.get(
        "DEALIX_SOFTWARE_ACQUISITION_STATE",
        "/opt/dealix/control/state/software_acquisition",
    )
)
DEFAULT_SESSION_STATE = Path(
    os.environ.get(
        "DEALIX_SESSION_FACTORY_STATE",
        "/opt/dealix/control/state/session_factory",
    )
)

LEGACY_SCHEMA = "dealix.software_candidate.v1"
SCHEMA = "dealix.software_candidate.v2"
DECISION_SCHEMA = "dealix.software_acquisition_decision.v2"

SCORE_FIELDS = (
    "business_value",
    "security",
    "maturity",
    "maintenance",
    "integration_fit",
    "license",
    "cost",
    "reversibility",
)

DEFAULT_CAPABILITY_FIELDS = (
    "privileged",
    "host_docker_socket",
    "host_network",
    "unrestricted_egress",
    "broad_filesystem_write",
    "broad_secret_access",
    "kernel_device_access",
    "firewall_mutation",
)

HIGH_RISK_ARTIFACT_TYPES = frozenset(
    {"executable", "container_image", "mcp_server", "agent_runtime", "installer", "system_service"}
)
L5_SURFACES = frozenset({"production", "root_system", "dns", "database", "secret", "firewall"})


@dataclass(frozen=True)
class Decision:
    candidate_id: str
    score: float
    evidence_confidence: float
    decision: str
    gate: str | None
    required_authority: str
    auto_executable: bool
    next_safe_action: str
    capability_risks: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": DECISION_SCHEMA,
            "candidate_id": self.candidate_id,
            "score": self.score,
            "evidence_confidence": self.evidence_confidence,
            "decision": self.decision,
            "gate": self.gate,
            "required_authority": self.required_authority,
            "auto_executable": self.auto_executable,
            "next_safe_action": self.next_safe_action,
            "capability_risks": list(self.capability_risks),
        }


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    policy = load_json(path, None)
    if not isinstance(policy, dict):
        raise ValueError(f"policy unavailable or invalid: {path}")
    weights = policy.get("weights") or {}
    if set(weights) != set(SCORE_FIELDS):
        raise ValueError("policy weights must exactly match score fields")
    total = sum(float(weights[name]) for name in SCORE_FIELDS)
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"policy weights must total 1.0, got {total}")
    evidence_weights = policy.get("evidence_confidence_weights") or {}
    if evidence_weights:
        evidence_total = sum(float(value) for value in evidence_weights.values())
        if abs(evidence_total - 100.0) > 1e-9:
            raise ValueError(f"evidence confidence weights must total 100, got {evidence_total}")
    return policy


def blank_candidate(candidate_id: str, name: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "candidate_id": candidate_id,
        "name": name,
        "source": "",
        "official_url": "",
        "repo": "",
        "version": "",
        "commit_sha": "",
        "image_digest": "",
        "artifact_type": "source_library",
        "license": "UNKNOWN",
        "purpose": "",
        "dealix_gap": "",
        "scores": dict.fromkeys(SCORE_FIELDS, 0),
        "monthly_cost": None,
        "resource_cost": "UNKNOWN",
        "alternatives": [],
        "duplicate_of_existing": "",
        "replacement_of_existing": "",
        "rollback_method": "",
        "sbom_path": "",
        "sbom_status": "UNKNOWN",
        "vulnerability_status": "UNKNOWN",
        "cisa_kev_match": False,
        "epss_score": None,
        "signature_status": "UNKNOWN",
        "provenance_status": "UNKNOWN",
        "requires_secret_dump": False,
        "capability_map": dict.fromkeys(DEFAULT_CAPABILITY_FIELDS, False),
        "network_allowlist": [],
        "data_egress": "DENY_BY_DEFAULT",
        "install_surface": "dependency_sandbox",
        "sandbox_result": "NOT_RUN",
        "benchmark_result": "NOT_RUN",
        "evidence_refs": [],
        "observed_at": now_iso(),
    }


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if candidate.get("schema") not in (None, LEGACY_SCHEMA, SCHEMA):
        errors.append("invalid_schema")
    for field in ("candidate_id", "name", "source", "official_url", "purpose", "dealix_gap"):
        if not str(candidate.get(field) or "").strip():
            errors.append(f"missing:{field}")
    scores = candidate.get("scores")
    if not isinstance(scores, dict):
        errors.append("missing:scores")
    else:
        for field in SCORE_FIELDS:
            value = scores.get(field)
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= float(value) <= 100:
                errors.append(f"invalid_score:{field}")
    if not str(candidate.get("install_surface") or ""):
        errors.append("missing:install_surface")
    refs = candidate.get("evidence_refs")
    if refs is not None and not isinstance(refs, list):
        errors.append("invalid:evidence_refs")
    epss = candidate.get("epss_score")
    if epss is not None and (
        isinstance(epss, bool) or not isinstance(epss, (int, float)) or not 0 <= float(epss) <= 1
    ):
        errors.append("invalid:epss_score")
    capability_map = candidate.get("capability_map")
    if capability_map is not None and not isinstance(capability_map, dict):
        errors.append("invalid:capability_map")
    return errors


def score_candidate(candidate: dict[str, Any], policy: dict[str, Any]) -> float:
    scores = candidate.get("scores") or {}
    weights = policy["weights"]
    total = sum(float(scores[field]) * float(weights[field]) for field in SCORE_FIELDS)
    return round(total, 2)


def _known(value: Any) -> bool:
    return str(value or "").upper().strip() not in {"", "UNKNOWN", "UNVERIFIED", "NOT_RUN", "NONE"}


def _verified_provenance(candidate: dict[str, Any], *, allow_not_applicable: bool = True) -> bool:
    values = {
        str(candidate.get("signature_status") or "").upper().strip(),
        str(candidate.get("provenance_status") or "").upper().strip(),
    }
    accepted = {"VERIFIED", "VALID", "SIGNED", "ATTESTED"}
    if allow_not_applicable:
        accepted.add("NOT_APPLICABLE")
    return bool(values & accepted)


def evidence_confidence(candidate: dict[str, Any], policy: dict[str, Any]) -> float:
    weights = policy.get("evidence_confidence_weights") or {
        "official_source": 15,
        "immutable_pin": 15,
        "verified_license": 10,
        "vulnerability_evidence": 15,
        "rollback": 10,
        "evidence_refs": 10,
        "sbom": 10,
        "provenance": 10,
        "capability_map": 5,
    }
    source = str(candidate.get("source") or "").lower().strip()
    official_source = bool(candidate.get("official_url")) and (
        source.startswith("official") or source in {"vendor", "upstream", "maintainer"}
    )
    immutable_pin = bool(
        str(candidate.get("image_digest") or "").strip()
        or str(candidate.get("commit_sha") or "").strip()
        or str(candidate.get("version") or "").strip()
    )
    verified_license = _known(candidate.get("license"))
    vuln_evidence = _known(candidate.get("vulnerability_status"))
    rollback = bool(str(candidate.get("rollback_method") or "").strip())
    refs = candidate.get("evidence_refs")
    evidence_refs = isinstance(refs, list) and any(str(value).strip() for value in refs)
    sbom = bool(str(candidate.get("sbom_path") or "").strip()) or str(
        candidate.get("sbom_status") or ""
    ).upper().strip() in {"READY", "GENERATED", "INGESTED", "VERIFIED"}
    provenance = _verified_provenance(candidate)
    capability_map = isinstance(candidate.get("capability_map"), dict)
    evidence = {
        "official_source": official_source,
        "immutable_pin": immutable_pin,
        "verified_license": verified_license,
        "vulnerability_evidence": vuln_evidence,
        "rollback": rollback,
        "evidence_refs": evidence_refs,
        "sbom": sbom,
        "provenance": provenance,
        "capability_map": capability_map,
    }
    return round(sum(float(weights.get(key, 0)) for key, present in evidence.items() if present), 2)


def required_authority(candidate: dict[str, Any], policy: dict[str, Any]) -> str:
    surface = str(candidate.get("install_surface") or "")
    mapping = policy.get("installation_tiers") or {}
    return str(mapping.get(surface) or ("L5_REQUIRED" if surface in L5_SURFACES else "UNKNOWN"))


def provenance_required(candidate: dict[str, Any], policy: dict[str, Any]) -> bool:
    high_risk = set(policy.get("high_risk_artifact_types") or HIGH_RISK_ARTIFACT_TYPES)
    return str(candidate.get("artifact_type") or "source_library").lower().strip() in high_risk


def capability_risks(candidate: dict[str, Any], policy: dict[str, Any]) -> tuple[str, ...]:
    capability_map = candidate.get("capability_map")
    if capability_map is None:
        if candidate.get("schema") == SCHEMA or provenance_required(candidate, policy):
            return ("unknown_capability_scope",)
        return ()
    if not isinstance(capability_map, dict):
        return ("invalid_capability_scope",)
    fields = tuple(policy.get("capability_risk_fields") or DEFAULT_CAPABILITY_FIELDS)
    risks = [field for field in fields if bool(capability_map.get(field))]
    return tuple(sorted(risks))


def hard_gate(candidate: dict[str, Any], policy: dict[str, Any]) -> tuple[str | None, str | None, tuple[str, ...]]:
    duplicate = str(candidate.get("duplicate_of_existing") or "").strip()
    replacement = str(candidate.get("replacement_of_existing") or "").strip()
    if duplicate and replacement != duplicate:
        return "duplicate", "REJECT_DUPLICATE", ()
    if bool(candidate.get("requires_secret_dump")):
        return "requires_secret_dump", "REJECT_SECRET_RISK", ()
    license_value = str(candidate.get("license") or "UNKNOWN").upper().strip()
    if license_value in {"", "UNKNOWN", "UNVERIFIED"}:
        return "unknown_license", "HOLD_LICENSE", ()
    if bool(candidate.get("cisa_kev_match")):
        return "cisa_kev_match", "QUARANTINE_KEV", ()
    vuln = str(candidate.get("vulnerability_status") or "UNKNOWN").upper().strip()
    if vuln in {
        "CRITICAL",
        "HIGH",
        "KNOWN_CRITICAL",
        "KNOWN_HIGH",
        "BLOCKED_CRITICAL",
        "BLOCKED_HIGH",
    }:
        return "critical_or_high_vulnerability", "REJECT_SECURITY", ()
    integrity_values = {
        str(candidate.get("signature_status") or "UNKNOWN").upper().strip(),
        str(candidate.get("provenance_status") or "UNKNOWN").upper().strip(),
    }
    if integrity_values & {"INVALID", "SUSPICIOUS", "FAILED", "TAMPERED"}:
        return "invalid_signature_or_provenance", "QUARANTINE", ()
    if provenance_required(candidate, policy) and not _verified_provenance(
        candidate, allow_not_applicable=False
    ):
        return "missing_required_provenance", "HOLD_PROVENANCE", ()
    risks = capability_risks(candidate, policy)
    if risks:
        return "capability_risk:" + ",".join(risks), "HOLD_CAPABILITY_RISK", risks
    if not str(candidate.get("rollback_method") or "").strip():
        return "missing_rollback", "HOLD_ROLLBACK", ()
    return None, None, ()


def decide(candidate: dict[str, Any], policy: dict[str, Any]) -> Decision:
    errors = validate_candidate(candidate)
    candidate_id = str(candidate.get("candidate_id") or "UNKNOWN")
    if errors:
        return Decision(
            candidate_id=candidate_id,
            score=0.0,
            evidence_confidence=0.0,
            decision="HOLD_INVALID_CONTRACT",
            gate=";".join(errors),
            required_authority="UNKNOWN",
            auto_executable=False,
            next_safe_action="repair candidate evidence contract before any execution",
        )

    score = score_candidate(candidate, policy)
    confidence = evidence_confidence(candidate, policy)
    authority = required_authority(candidate, policy)
    gate, gate_decision, risks = hard_gate(candidate, policy)
    if gate_decision:
        return Decision(
            candidate_id=candidate_id,
            score=score,
            evidence_confidence=confidence,
            decision=gate_decision,
            gate=gate,
            required_authority=authority,
            auto_executable=False,
            next_safe_action=f"resolve hard gate: {gate}",
            capability_risks=risks,
        )

    thresholds = policy["thresholds"]
    auto_score = float(thresholds["auto_sandbox_min"])
    research_score = float(thresholds["research_more_min"])
    evidence_min = float(thresholds.get("auto_sandbox_evidence_min", 80))
    if score >= auto_score and confidence >= evidence_min:
        decision = "AUTO_SANDBOX"
        action = "create strict isolated sandbox/integration job with acceptance evidence"
    elif score >= research_score:
        decision = "RESEARCH_MORE"
        action = "collect missing official provenance/security/license/capability/benchmark evidence"
    else:
        decision = "REJECT_LOW_VALUE"
        action = "retain receipt only; no execution"

    auto_executable = decision in {"AUTO_SANDBOX", "RESEARCH_MORE"}
    return Decision(
        candidate_id=candidate_id,
        score=score,
        evidence_confidence=confidence,
        decision=decision,
        gate=None,
        required_authority=authority,
        auto_executable=auto_executable,
        next_safe_action=action,
    )


def _evidence_summary(candidate: dict[str, Any]) -> str:
    refs = [str(value) for value in (candidate.get("evidence_refs") or []) if str(value).strip()]
    return ", ".join(refs[:10]) if refs else "NONE_PROVIDED"


def build_job(candidate: dict[str, Any], decision: Decision, *, base_sha: str) -> dict[str, Any] | None:
    if decision.decision == "AUTO_SANDBOX":
        marker = f"SOFTWARE_INTAKE_RECEIPT:{decision.candidate_id}"
        prompt = (
            "Evaluate this candidate only inside the canonical isolated worktree/sandbox. "
            "STRICT SANDBOX: run non-root/rootless where practical; never privileged; never mount the host Docker socket; "
            "never use host networking; preserve seccomp/MAC controls; drop unneeded capabilities; keep host inputs read-only; "
            "use only the isolated writable worktree/tmp; mount no secrets by default; deny or allowlist network egress; "
            "enforce CPU/RAM/PID/time/disk limits; clean the environment deterministically; record exact artifact digest. "
            "Do not merge, deploy, mutate production, DNS, DB, secrets, firewall, root system state, send, publish, pay, or buy. "
            "Use official source/provenance, immutable pin, license evidence, SBOM, OSV/Trivy findings, CISA KEV status, "
            "EPSS only as prioritization evidence, and Sigstore/SLSA or publisher provenance where applicable. "
            "For MCP/agent/browser/coding runtimes record tools, auth scopes, process execution, filesystem reach, network destinations, "
            "telemetry/data retention, untrusted-content boundary, credential visibility, and material-action confirmation. "
            "Prepare only draft-safe repo integration if it clearly wins. Fail closed on unknown evidence or unexpected capability. "
            f"Candidate={json.dumps(candidate, ensure_ascii=False)}. "
            f"Value score={decision.score}; evidence confidence={decision.evidence_confidence}. "
            f"Required eventual authority={decision.required_authority}. Evidence refs={_evidence_summary(candidate)}. "
            f"Finish stdout with exact marker {marker}."
        )
        return make_job(
            owner_agent="dealix-engineer",
            business_goal=f"Strict-sandbox and verify software candidate {candidate['name']}",
            economic_reason=str(candidate.get("dealix_gap") or "reduce founder minutes/cost/risk"),
            job_class="ENGINEERING",
            authority_level="L4",
            priority=min(100.0, decision.score),
            base_sha=base_sha,
            modifying=True,
            executor={"prompt": prompt},
            acceptance={
                "criteria": "strict isolated evidence-backed software intake receipt",
                "checks": [
                    {"kind": "exit_zero"},
                    {"kind": "stdout_contains", "text": marker},
                ],
            },
            context_refs=[str(value) for value in (candidate.get("evidence_refs") or [])],
            next_action="review sandbox receipt; keep L5 effects parked",
        )

    if decision.decision == "RESEARCH_MORE":
        marker = f"SOFTWARE_RESEARCH_RECEIPT:{decision.candidate_id}"
        prompt = (
            "Research this software candidate using official/public sources only. Do not install or mutate the repo/system. "
            "Return: official source, latest stable immutable version/commit/digest, license evidence, maintenance activity, "
            "OSV/Trivy vulnerability status, CISA KEV match, EPSS prioritization where relevant, signature/provenance availability, "
            "SBOM support, full capability/blast-radius map, integration fit, alternatives, cash/resource cost, rollback path, "
            "and evidence refs. For MCP/AI/agent tools include auth scopes, command execution, filesystem/network/data/secret reach. "
            "Internet discovery is not trust. Do not invent claims. "
            f"Candidate={json.dumps(candidate, ensure_ascii=False)}. Finish stdout with exact marker {marker}."
        )
        return make_job(
            owner_agent="dealix-engineer",
            business_goal=f"Research missing evidence for software candidate {candidate['name']}",
            economic_reason=str(candidate.get("dealix_gap") or "reduce uncertainty before adoption"),
            job_class="RESEARCH",
            authority_level="L1",
            priority=min(90.0, decision.score),
            base_sha=base_sha,
            modifying=False,
            executor={"prompt": prompt},
            acceptance={
                "criteria": "evidence-backed research receipt",
                "checks": [
                    {"kind": "exit_zero"},
                    {"kind": "stdout_contains", "text": marker},
                ],
            },
            context_refs=[str(value) for value in (candidate.get("evidence_refs") or [])],
            next_action="update candidate registry from verified research evidence",
        )
    return None


def process_candidates(
    candidates: list[dict[str, Any]],
    *,
    policy: dict[str, Any],
    base_sha: str,
    enqueue: bool = False,
    session_state: Path = DEFAULT_SESSION_STATE,
    max_jobs: int = 3,
) -> dict[str, Any]:
    decisions: list[dict[str, Any]] = []
    submitted: list[dict[str, Any]] = []
    seen: set[str] = set()

    ordered = []
    for candidate in candidates:
        decision = decide(candidate, policy)
        ordered.append((decision.score, decision.evidence_confidence, candidate, decision))
    ordered.sort(key=lambda item: (item[0], item[1]), reverse=True)

    for _, _, candidate, decision in ordered:
        decisions.append(decision.as_dict())
        if not enqueue or not decision.auto_executable or len(submitted) >= max_jobs:
            continue
        if decision.candidate_id in seen:
            continue
        seen.add(decision.candidate_id)
        job = build_job(candidate, decision, base_sha=base_sha)
        if not job:
            continue
        result = submit_job(session_state, job)
        submitted.append(
            {
                "candidate_id": decision.candidate_id,
                "ok": bool(result.get("ok")),
                "job_id": (result.get("job") or {}).get("JOB_ID"),
                "status": (result.get("job") or {}).get("STATUS"),
                "errors": result.get("errors") or [],
            }
        )

    return {
        "schema": "dealix.software_acquisition_run.v2",
        "generated_at": now_iso(),
        "candidate_count": len(candidates),
        "decisions": decisions,
        "submitted_jobs": submitted,
        "max_jobs": max_jobs,
        "deep_wip_max": int(policy.get("deep_wip_max", 3)),
        "external_effects_executed": 0,
        "l5_executed": "NONE",
    }


def read_registry(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path, {"candidates": []})
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("candidates"), list):
        return [item for item in payload["candidates"] if isinstance(item, dict)]
    raise ValueError("candidate registry must be a list or an object with candidates[]")


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--session-state", type=Path, default=DEFAULT_SESSION_STATE)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--enqueue", action="store_true")
    parser.add_argument("--max-jobs", type=int, default=3)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()

    policy = load_policy(args.policy)
    candidates = read_registry(args.registry)
    result = process_candidates(
        candidates,
        policy=policy,
        base_sha=args.base_sha,
        enqueue=args.enqueue,
        session_state=args.session_state,
        max_jobs=max(0, min(int(args.max_jobs), int(policy.get("deep_wip_max", 3)))),
    )
    output = args.state_dir / "SOFTWARE_ACQUISITION_RECEIPT.json"
    write_json(output, result)
    if args.stdout:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    print("DEALIX_SOFTWARE_ACQUISITION_FACTORY=PASS")
    print(f"CANDIDATES={result['candidate_count']}")
    print(f"JOBS_SUBMITTED={len(result['submitted_jobs'])}")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
