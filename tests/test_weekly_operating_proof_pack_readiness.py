"""Proof-pack readiness must not confuse source presence with verified proof."""

from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_weekly_operating_proof_pack.py"


def _write_fixture(tmp_path: Path, *, baseline_date: str, source_ref: str) -> Path:
    transform = tmp_path / "dealix" / "transformation"
    transform.mkdir(parents=True)
    (transform / "kpi_registry.yaml").write_text(
        yaml.safe_dump(
            {
                "version": 2,
                "kpis": {
                    "north_star": [
                        {
                            "key": "measured_customer_value_sar",
                            "owner_os": "value",
                            "evidence": {
                                "primary_source": "value ledger",
                                "weekly_proof_fields": ["value"],
                                "verification_commands": ["verify-value"],
                            },
                        }
                    ],
                    "leading": [],
                    "guardrails": [],
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (transform / "ownership_matrix.yaml").write_text(
        yaml.safe_dump(
            {"os_ownership": {"value": {"human_assignee_name": "Founder"}}},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    (transform / "kpi_baselines.yaml").write_text(
        yaml.safe_dump(
            {
                "updated_period_iso": baseline_date,
                "snapshots": {
                    "measured_customer_value_sar": {
                        "value_numeric": 10.0,
                        "source_ref": source_ref,
                    }
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return tmp_path


def _run(repo_root: Path, *, strict: bool) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), "--repo-root", str(repo_root)]
    if strict:
        command.append("--strict")
    return subprocess.run(command, capture_output=True, text=True, check=False)


def test_unsynced_source_is_not_reported_as_filled(tmp_path: Path) -> None:
    today = datetime.now(UTC).date().isoformat()
    repo_root = _write_fixture(
        tmp_path,
        baseline_date=today,
        source_ref="crm:export:not_synced_yet",
    )
    result = _run(repo_root, strict=False)
    assert result.returncode == 0
    assert "proof_readiness**: `NOT_READY`" in result.stdout
    assert "UNVERIFIED_SOURCE" in result.stdout
    assert "FILLED" not in result.stdout


def test_stale_baseline_fails_strict_mode(tmp_path: Path) -> None:
    stale = (datetime.now(UTC).date() - timedelta(days=30)).isoformat()
    repo_root = _write_fixture(
        tmp_path,
        baseline_date=stale,
        source_ref="ledger:value_event:evt_001",
    )
    result = _run(repo_root, strict=True)
    assert result.returncode != 0
    assert "baseline_freshness**: `STALE`" in result.stdout
    assert "NOT_READY" in result.stdout


def test_synthetic_source_fails_strict_mode(tmp_path: Path) -> None:
    today = datetime.now(UTC).date().isoformat()
    repo_root = _write_fixture(
        tmp_path,
        baseline_date=today,
        source_ref="computed:synthetic_default_economics_inputs",
    )
    result = _run(repo_root, strict=True)
    assert result.returncode != 0
    assert "UNVERIFIED_SOURCE" in result.stdout


def test_current_non_placeholder_source_is_ready_for_verification(tmp_path: Path) -> None:
    today = datetime.now(UTC).date().isoformat()
    repo_root = _write_fixture(
        tmp_path,
        baseline_date=today,
        source_ref="ledger:value_event:evt_001",
    )
    result = _run(repo_root, strict=True)
    assert result.returncode == 0
    assert "proof_readiness**: `READY_FOR_VERIFICATION`" in result.stdout
    assert "SOURCE_REF_PRESENT" in result.stdout
