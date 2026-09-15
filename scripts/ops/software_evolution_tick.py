#!/usr/bin/env python3
"""One bounded Internet Scout + Software Acquisition tick.

This script deliberately does not schedule itself. Hermes remains the canonical
scheduler and Session Factory remains the canonical executor. V2 discovery emits
the same evidence/capability contract consumed by the acquisition factory.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

OPS_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OPS_DIR))

from session_factory import make_job, submit_job
from software_acquisition_factory import (
    DEFAULT_REGISTRY,
    DEFAULT_SESSION_STATE,
    DEFAULT_STATE,
    POLICY_PATH,
    load_json,
    load_policy,
    process_candidates,
    read_registry,
    write_json,
)

SOURCES_PATH = REPO_ROOT / "config/company/software_acquisition_sources.json"


def load_sources(path: Path = SOURCES_PATH) -> dict[str, Any]:
    payload = load_json(path, None)
    if not isinstance(payload, dict) or not isinstance(payload.get("categories"), list):
        raise ValueError(f"invalid source registry: {path}")
    return payload


def scout_job(category: dict[str, Any], *, base_sha: str) -> dict[str, Any]:
    category_id = str(category.get("id") or "unknown")
    marker = f"SOFTWARE_SCOUT_RECEIPT:{category_id}"
    prompt = (
        "Act as Dealix Internet Scout for governed software/tool acquisition. Research only; do not install, buy, send, publish, "
        "merge, deploy, change DNS/DB/secrets/firewall/root state, or mutate production. Use official project docs, official repositories, "
        "release metadata, signed attestations/SBOMs, and authoritative vulnerability sources first. Third-party commentary is discovery evidence only. "
        "Find only software that materially improves verified economic movement, founder minutes, reliability, security, delivery, or cost. "
        "For every candidate return ONE machine-readable V2 candidate object with: schema=dealix.software_candidate.v2; candidate_id; name; "
        "source; official_url; repo; version; commit_sha and/or image_digest; artifact_type; license; purpose; dealix_gap; monthly_cost; resource_cost; "
        "alternatives; duplicate_of_existing; replacement_of_existing when applicable; rollback_method; sbom_path/status; vulnerability_status; "
        "cisa_kev_match; epss_score if applicable; signature_status; provenance_status; requires_secret_dump; install_surface; sandbox_result; "
        "benchmark_result; evidence_refs; and evidence-backed 0..100 scores for business_value/security/maturity/maintenance/integration_fit/license/cost/reversibility. "
        "Also include capability_map keys for privileged, host_docker_socket, host_network, unrestricted_egress, broad_filesystem_write, "
        "broad_secret_access, kernel_device_access, firewall_mutation; network_allowlist; and data_egress. "
        "For MCP/agent/browser/coding runtimes additionally document tool inventory, auth scopes, process execution, filesystem reach, network destinations, "
        "data retention/telemetry, untrusted-content boundary, credential visibility, and whether material actions require human/L5 confirmation. "
        "Use OSV/Trivy evidence for affected components, CISA KEV for known exploitation, and FIRST EPSS only as exploitation-likelihood prioritization. "
        "Prefer Sigstore/Cosign/SLSA or equivalent publisher provenance when available. If a score or security field is not evidence-backed, mark it UNKNOWN "
        "or conservatively low rather than inventing confidence. Research is not trust; popularity is not security; score is not evidence. "
        f"Category={json.dumps(category, ensure_ascii=False)}. Finish stdout with exact marker {marker}."
    )
    return make_job(
        owner_agent="dealix-engineer",
        business_goal=f"Discover high-value evidence-backed software candidates for {category_id}",
        economic_reason=str(category.get("purpose") or "improve Dealix capability safely"),
        job_class="RESEARCH",
        authority_level="L1",
        priority=float(category.get("priority") or 50),
        base_sha=base_sha,
        modifying=False,
        data_sensitivity="PUBLIC",
        executor={"prompt": prompt},
        acceptance={
            "criteria": "official-source V2 software scout receipt with trust and capability evidence",
            "checks": [
                {"kind": "exit_zero"},
                {"kind": "stdout_contains", "text": marker},
            ],
        },
        context_refs=[str(value) for value in (category.get("official_sources") or [])],
        next_action="ingest only evidence-backed V2 candidates into the canonical software registry",
    )


def run_tick(
    *,
    base_sha: str,
    source_path: Path = SOURCES_PATH,
    registry_path: Path = DEFAULT_REGISTRY,
    state_dir: Path = DEFAULT_STATE,
    session_state: Path = DEFAULT_SESSION_STATE,
    enqueue_scouts: bool = True,
    enqueue_candidates: bool = True,
    max_scouts: int = 3,
    max_candidate_jobs: int = 3,
) -> dict[str, Any]:
    policy = load_policy(POLICY_PATH)
    sources = load_sources(source_path)
    categories = sorted(
        [item for item in sources["categories"] if isinstance(item, dict)],
        key=lambda item: -float(item.get("priority") or 0),
    )

    scout_receipts: list[dict[str, Any]] = []
    if enqueue_scouts:
        for category in categories[: max(0, min(max_scouts, int(policy.get("deep_wip_max", 3))))]:
            result = submit_job(session_state, scout_job(category, base_sha=base_sha))
            scout_receipts.append(
                {
                    "category": category.get("id"),
                    "ok": bool(result.get("ok")),
                    "job_id": (result.get("job") or {}).get("JOB_ID"),
                    "status": (result.get("job") or {}).get("STATUS"),
                    "errors": result.get("errors") or [],
                }
            )

    if registry_path.is_file():
        candidates = read_registry(registry_path)
        acquisition = process_candidates(
            candidates,
            policy=policy,
            base_sha=base_sha,
            enqueue=enqueue_candidates,
            session_state=session_state,
            max_jobs=max(0, min(max_candidate_jobs, int(policy.get("deep_wip_max", 3)))),
        )
    else:
        acquisition = {
            "schema": "dealix.software_acquisition_run.v2",
            "candidate_count": 0,
            "decisions": [],
            "submitted_jobs": [],
            "registry_status": "ABSENT_EMPTY_NOT_ERROR",
            "external_effects_executed": 0,
            "l5_executed": "NONE",
        }

    receipt = {
        "schema": "dealix.software_evolution_tick.v2",
        "base_sha": base_sha,
        "scout_jobs": scout_receipts,
        "acquisition": acquisition,
        "deep_wip_max": int(policy.get("deep_wip_max", 3)),
        "scheduler_created": False,
        "external_effects_executed": 0,
        "l5_executed": "NONE",
    }
    write_json(state_dir / "SOFTWARE_EVOLUTION_TICK_RECEIPT.json", receipt)
    return receipt


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--sources", type=Path, default=SOURCES_PATH)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--session-state", type=Path, default=DEFAULT_SESSION_STATE)
    parser.add_argument("--no-scouts", action="store_true")
    parser.add_argument("--no-candidates", action="store_true")
    parser.add_argument("--max-scouts", type=int, default=3)
    parser.add_argument("--max-candidate-jobs", type=int, default=3)
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    receipt = run_tick(
        base_sha=args.base_sha,
        source_path=args.sources,
        registry_path=args.registry,
        state_dir=args.state_dir,
        session_state=args.session_state,
        enqueue_scouts=not args.no_scouts,
        enqueue_candidates=not args.no_candidates,
        max_scouts=args.max_scouts,
        max_candidate_jobs=args.max_candidate_jobs,
    )
    if args.stdout:
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
    print("DEALIX_SOFTWARE_EVOLUTION_TICK=PASS")
    print(f"SCOUT_JOBS={len(receipt['scout_jobs'])}")
    print(f"CANDIDATE_JOBS={len(receipt['acquisition'].get('submitted_jobs', []))}")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
