#!/usr/bin/env python3
"""Dealix Software Acquisition & Evolution Factory.

This is a governed intake/planning layer on top of the canonical Hermes Session
Factory. It does not create another scheduler or execution plane.

Responsibilities:
- normalize software/tool candidates discovered from official/public sources;
- score business value, security, maturity, maintenance, fit, license, cost,
  and reversibility;
- fail closed on supply-chain, license, rollback, duplicate, and secret risks;
- emit bounded L0-L4 jobs into the existing Session Factory;
- record when a useful candidate ultimately requires L5 production/root/DNS/DB/
  secret/firewall authority, without executing that authority.

Internet discovery is evidence, not trust. No downloader or installer is invoked
by this module directly.
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

from session_factory import make_job, submit_job  # noqa: E402

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

SCHEMA = "dealix.software_candidate.v1"
DECISION_SCHEMA = "dealix.software_acquisition_decision.v1"

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

L5_SURFACES = frozenset({"production", "root_system", "dns", "database", "secret", "firewall"})


@dataclass(frozen=True)
class Decision:
    candidate_id: str
    score: float
    decision: str
    gate: str | None
    required_authority: str
    auto_executable: bool
    next_safe_action: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": DECISION_SCHEMA,
            "candidate_id": self.candidate_id,
            "score": self.score,
            "decision": self.decision,
            "gate": self.gate,
            "required_authority": self.required_authority,
            "auto_executable": self.auto_executable,
            "next_safe_action": self.next_safe_action,
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
        "license": "UNKNOWN",
        "purpose": "",
        "dealix_gap": "",
        "scores": {field: 0 for field in SCORE_FIELDS},
        "monthly_cost": None,
        "resource_cost": "UNKNOWN",
        "alternatives": [],
        "duplicate_of_existing": "",
        "rollback_method": "",
        "sbom_path": "",
        "vulnerability_status": "UNKNOWN",
        "signature_status": "UNKNOWN",
        "requires_secret_dump": False,
        "install_surface": "dependency_sandbox",
        "sandbox_result": "NOT_RUN",
        "benchmark_result": "NOT_RUN",
        "evidence_refs": [],
        "observed_at": now_iso(),
    }


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if candidate.get("schema") not in (None, SCHEMA):
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
    surface = str(candidate.get("install_surface") or "")
    if not surface:
        errors.append("missing:install_surface")
    refs = candidate.get("evidence_refs")
    if refs is not None and not isinstance(refs, list):
        errors.append("invalid:evidence_refs")
    return errors


def score_candidate(candidate: dict[str, Any], policy: dict[str, Any]) -> float:
    scores = candidate.get("scores") or {}
    weights = policy["weights"]
    total = sum(float(scores[field]) * float(weights[field]) for field in SCORE_FIELDS)
    return round(total, 2)


def required_authority(candidate: dict[str, Any], policy: dict[str, Any]) -> str:
    surface = str(candidate.get("install_surface") or "")
    mapping = policy.get("installation_tiers") or {}
    return str(mapping.get(surface) or ("L5_REQUIRED" if surface in L5_SURFACES else "UNKNOWN"))


def hard_gate(candidate: dict[str, Any]) -> tuple[str | None, str | None]:
    duplicate = str(candidate.get("duplicate_of_existing") or "").strip()
    if duplicate:
        return "duplicate", "REJECT_DUPLICATE"
    if bool(candidate.get("requires_secret_dump")):
        return "requires_secret_dump", "REJECT_SECRET_RISK"
    license_value = str(candidate.get("license") or "UNKNOWN").upper().strip()
    if license_value in {"", "UNKNOWN", "UNVERIFIED"}:
        return "unknown_license", "HOLD_LICENSE"
    vuln = str(candidate.get("vulnerability_status") or "UNKNOWN").upper().strip()
    if vuln in {"CRITICAL", "KNOWN_CRITICAL", "BLOCKED_CRITICAL"}:
        return "critical_vulnerability", "REJECT_SECURITY"
    signature = str(candidate.get("signature_status") or "UNKNOWN").upper().strip()
    if signature in {"INVALID", "SUSPICIOUS", "FAILED"}:
        return "invalid_signature", "QUARANTINE"
    if not str(candidate.get("rollback_method") or "").strip():
        return "missing_rollback", "HOLD_ROLLBACK"
    return None, None


def decide(candidate: dict[str, Any], policy: dict[str, Any]) -> Decision:
    errors = validate_candidate(candidate)
    candidate_id = str(candidate.get("candidate_id") or "UNKNOWN")
    if errors:
        return Decision(
            candidate_id=candidate_id,
            score=0.0,
            decision="HOLD_INVALID_CONTRACT",
            gate=";".join(errors),
            required_authority="UNKNOWN",
            auto_executable=False,
            next_safe_action="repair candidate evidence contract before any execution",
        )

    score = score_candidate(candidate, policy)
    authority = required_authority(candidate, policy)
    gate, gate_decision = hard_gate(candidate)
    if gate_decision:
        return Decision(
            candidate_id=candidate_id,
            score=score,
            decision=gate_decision,
            gate=gate,
            required_authority=authority,
            auto_executable=False,
            next_safe_action=f"resolve hard gate: {gate}",
        )

    thresholds = policy["thresholds"]
    if score >= float(thresholds["auto_sandbox_min"]):
        decision = "AUTO_SANDBOX"
        action = "create isolated sandbox/integration job with acceptance evidence"
    elif score >= float(thresholds["research_more_min"]):
        decision = "RESEARCH_MORE"
        action = "collect missing official provenance/security/license/benchmark evidence"
    else:
        decision = "REJECT_LOW_VALUE"
        action = "retain receipt only; no execution"

    auto_executable = decision in {"AUTO_SANDBOX", "RESEARCH_MORE"}
    # A candidate may ultimately require L5 to reach production, but evaluation,
    # sandboxing, benchmarking, and draft integration remain safe L0-L4 work.
    return Decision(
        candidate_id=candidate_id,
        score=score,
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
            "Evaluate and integrate this software candidate only inside an isolated git worktree/sandbox. "
            "Do not merge, deploy, mutate production, DNS, DB, secrets, firewall, root system state, send, publish, pay, or buy. "
            "Use official source/provenance, pin version/commit/digest, inspect license, generate/ingest SBOM when tooling exists, "
            "scan for known vulnerabilities, verify signature/provenance when available, benchmark against the stated Dealix gap, "
            "and prepare only a draft-safe repo integration if it clearly wins. Fail closed on unknown evidence. "
            f"Candidate={json.dumps(candidate, ensure_ascii=False)}. "
            f"Required eventual authority={decision.required_authority}. Evidence refs={_evidence_summary(candidate)}. "
            f"Finish stdout with exact marker {marker}."
        )
        return make_job(
            owner_agent="dealix-engineer",
            business_goal=f"Sandbox and verify software candidate {candidate['name']}",
            economic_reason=str(candidate.get("dealix_gap") or "reduce founder minutes/cost/risk"),
            job_class="ENGINEERING",
            authority_level="L4",
            priority=min(100.0, decision.score),
            base_sha=base_sha,
            modifying=True,
            executor={"prompt": prompt},
            acceptance={
                "criteria": "isolated evidence-backed software intake receipt",
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
            "Return: official source, latest stable/pinned version or commit, license evidence, maintenance activity, security posture, "
            "signature/provenance availability, SBOM support, known CVE status, integration fit, alternatives, expected cash/resource cost, "
            "rollback path, and evidence refs. Internet discovery is not trust. Do not invent claims. "
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
        ordered.append((decision.score, candidate, decision))
    ordered.sort(key=lambda item: item[0], reverse=True)

    for _, candidate, decision in ordered:
        item = decision.as_dict()
        decisions.append(item)
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
        "schema": "dealix.software_acquisition_run.v1",
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
