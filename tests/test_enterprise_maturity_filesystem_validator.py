"""Tests for enterprise maturity filesystem contracts."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.enterprise_maturity_os import (
    DOMAIN_CONTRACTS,
    SYSTEM_ARTIFACTS,
    domain_coverage_map,
    evaluate_all_domain_filesystem_status,
    evaluate_domain_filesystem_status,
)


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("ok\n", encoding="utf-8")


def test_foundation_contract_full_coverage(tmp_path: Path) -> None:
    contract = next(c for c in DOMAIN_CONTRACTS if c.domain == "foundation_maturity")
    for rel in contract.required_paths:
        (tmp_path / rel).mkdir(parents=True, exist_ok=True)
    for artifact in SYSTEM_ARTIFACTS:
        target = tmp_path / contract.system_root / artifact
        if artifact in ("tests", "evals"):
            target.mkdir(parents=True, exist_ok=True)
        else:
            _touch(target)
    status = evaluate_domain_filesystem_status(tmp_path, contract)
    assert status.coverage == 100.0
    assert status.missing_paths == ()
    assert status.missing_system_artifacts == ()


def test_domain_coverage_map_contains_all_domains(tmp_path: Path) -> None:
    statuses = evaluate_all_domain_filesystem_status(tmp_path)
    coverage = domain_coverage_map(statuses)
    assert len(coverage) == len(DOMAIN_CONTRACTS)
    assert all(score == 0.0 for score in coverage.values())
