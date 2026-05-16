"""Filesystem contracts for the Dealix Enterprise Maturity Operating System."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

# NOTE:
# We intentionally use `dealix_platform/` instead of top-level `platform/`
# to avoid shadowing Python's stdlib `platform` module during imports.
PLATFORM_ROOT = "dealix_platform"

SYSTEM_ARTIFACTS: tuple[str, ...] = (
    "architecture.md",
    "readiness.md",
    "observability.md",
    "rollback.md",
    "metrics.md",
    "risk_model.md",
    "tests",
    "evals",
)


@dataclass(frozen=True)
class DomainContract:
    domain: str
    required_paths: tuple[str, ...]
    system_root: str


@dataclass(frozen=True)
class DomainFilesystemStatus:
    domain: str
    coverage: float
    existing_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    missing_system_artifacts: tuple[str, ...]


DOMAIN_CONTRACTS: tuple[DomainContract, ...] = (
    DomainContract(
        domain="foundation_maturity",
        required_paths=(
            f"{PLATFORM_ROOT}/foundation",
            f"{PLATFORM_ROOT}/identity",
            f"{PLATFORM_ROOT}/rbac",
            f"{PLATFORM_ROOT}/multi_tenant",
            f"{PLATFORM_ROOT}/security",
            f"{PLATFORM_ROOT}/deployment",
            f"{PLATFORM_ROOT}/observability",
        ),
        system_root=f"{PLATFORM_ROOT}/foundation",
    ),
    DomainContract(
        domain="agentic_runtime_maturity",
        required_paths=(
            "agents",
            f"{PLATFORM_ROOT}/agent_runtime",
            f"{PLATFORM_ROOT}/tool_registry",
            f"{PLATFORM_ROOT}/agent_memory",
            f"{PLATFORM_ROOT}/escalation",
        ),
        system_root=f"{PLATFORM_ROOT}/agent_runtime",
    ),
    DomainContract(
        domain="workflow_orchestration_maturity",
        required_paths=(
            "workflows",
            f"{PLATFORM_ROOT}/workflow_engine",
            f"{PLATFORM_ROOT}/orchestration",
            f"{PLATFORM_ROOT}/execution_engine",
        ),
        system_root=f"{PLATFORM_ROOT}/workflow_engine",
    ),
    DomainContract(
        domain="organizational_memory_maturity",
        required_paths=(
            "memory",
            f"{PLATFORM_ROOT}/knowledge",
            f"{PLATFORM_ROOT}/retrieval",
            f"{PLATFORM_ROOT}/reranking",
        ),
        system_root=f"{PLATFORM_ROOT}/knowledge",
    ),
    DomainContract(
        domain="governance_maturity",
        required_paths=(
            "governance",
            f"{PLATFORM_ROOT}/policy_engine",
            f"{PLATFORM_ROOT}/approval_engine",
            f"{PLATFORM_ROOT}/risk_engine",
        ),
        system_root=f"{PLATFORM_ROOT}/policy_engine",
    ),
    DomainContract(
        domain="evaluation_maturity",
        required_paths=(
            "evals/retrieval",
            "evals/hallucination",
            "evals/workflow_execution",
            "evals/agent_behavior",
            "evals/governance",
            "evals/business_impact",
        ),
        system_root="evals",
    ),
    DomainContract(
        domain="continuous_evolution_maturity",
        required_paths=(
            "continuous_improvement",
            "releases",
            "changelogs",
            "versions",
        ),
        system_root="continuous_improvement",
    ),
)


def _exists(repo_root: Path, rel_path: str) -> bool:
    path = repo_root / rel_path
    return path.is_file() or path.is_dir()


def _missing_system_artifacts(repo_root: Path, system_root: str) -> tuple[str, ...]:
    root = repo_root / system_root
    missing: list[str] = []
    for artifact in SYSTEM_ARTIFACTS:
        probe = root / artifact
        if not (probe.is_file() or probe.is_dir()):
            missing.append(f"{system_root}/{artifact}")
    return tuple(missing)


def evaluate_domain_filesystem_status(
    repo_root: Path,
    contract: DomainContract,
) -> DomainFilesystemStatus:
    existing: list[str] = []
    missing: list[str] = []
    for rel_path in contract.required_paths:
        if _exists(repo_root, rel_path):
            existing.append(rel_path)
        else:
            missing.append(rel_path)
    missing_artifacts = _missing_system_artifacts(repo_root, contract.system_root)
    total = len(contract.required_paths) + len(SYSTEM_ARTIFACTS)
    present = len(existing) + (len(SYSTEM_ARTIFACTS) - len(missing_artifacts))
    coverage = round((present / total) * 100, 2) if total else 0.0
    return DomainFilesystemStatus(
        domain=contract.domain,
        coverage=coverage,
        existing_paths=tuple(existing),
        missing_paths=tuple(missing),
        missing_system_artifacts=missing_artifacts,
    )


def evaluate_all_domain_filesystem_status(repo_root: Path) -> tuple[DomainFilesystemStatus, ...]:
    return tuple(
        evaluate_domain_filesystem_status(repo_root, contract)
        for contract in DOMAIN_CONTRACTS
    )


def domain_coverage_map(statuses: Iterable[DomainFilesystemStatus]) -> dict[str, float]:
    return {status.domain: status.coverage for status in statuses}
