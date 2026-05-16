"""Master strategy verification smoke tests."""
from __future__ import annotations

from pathlib import Path


def test_os_tier_registry_exists() -> None:
    path = Path("dealix/transformation/os_tier_registry.yaml")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "T1_production" in text
    assert "golden_chain_modules" in text


def test_program_unified_mapping() -> None:
    path = Path("dealix/transformation/program_unified.yaml")
    assert path.exists()
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["layers"]["strategic_200"]["registry"].endswith("strategic_initiatives_registry.yaml")
    assert "doctrine-lock" in data["mapping"]


def test_private_beta_tracker() -> None:
    path = Path("dealix/transformation/private_beta_tracker.yaml")
    assert path.exists()
    import yaml

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["target_pilots"] >= 3


def test_kpi_founder_required_keys() -> None:
    path = Path("dealix/transformation/kpi_founder_required.yaml")
    import yaml

    keys = yaml.safe_load(path.read_text(encoding="utf-8"))["founder_required_keys"]
    assert "measured_customer_value_sar" in keys


def test_verify_os_tier_registry_script() -> None:
    import subprocess

    r = subprocess.run(
        ["python3", "scripts/verify_os_tier_registry.py"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0
    assert "OS_TIER_REGISTRY: PASS" in r.stdout


def test_record_win_loss_entry() -> None:
    import subprocess
    import yaml

    r = subprocess.run(
        [
            "python3",
            "scripts/record_win_loss_entry.py",
            "--outcome",
            "win",
            "--account",
            "TestCo",
            "--evidence-ref",
            "proof:test:1",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0
    data = yaml.safe_load(Path("dealix/registers/win_loss.yaml").read_text(encoding="utf-8"))
    assert any(e.get("account") == "TestCo" for e in data.get("entries") or [])
