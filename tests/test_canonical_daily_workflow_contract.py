from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
CANONICAL = WORKFLOWS / "governed-full-ops-daily.yml"
LEGACY_DAILY_PATHS = (
    WORKFLOWS / "founder_commercial_daily.yml",
    WORKFLOWS / "daily_snapshot.yml",
    WORKFLOWS / "dealix-autonomous-company-os.yml",
    WORKFLOWS / "self-operating-company-os.yml",
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_governed_full_ops_is_the_only_scheduled_company_os_path() -> None:
    canonical = _text(CANONICAL)
    assert "schedule:" in canonical
    assert 'cron: "0 */4 * * *"' in canonical
    assert "python3 scripts/dealix_snapshot.py" in canonical
    assert "docs/snapshots/*.json" in canonical
    for path in LEGACY_DAILY_PATHS:
        content = _text(path)
        assert "workflow_dispatch:" in content, path
        assert "schedule:" not in content, path


def test_governed_full_ops_is_fail_closed_for_external_effects() -> None:
    canonical = _text(CANONICAL)
    for marker in (
        'DEALIX_EXTERNAL_SEND: "0"',
        'DEALIX_PUBLIC_PUBLISH: "0"',
        'DEALIX_PAID_SPEND: "0"',
        'DEALIX_LIVE_PAYMENT: "0"',
        'DEALIX_PRODUCTION_MUTATION: "0"',
    ):
        assert marker in canonical
    assert "Verify fail-closed operating boundary" in canonical


def test_governed_full_ops_has_bounded_ksa_pulse_modes() -> None:
    canonical = _text(CANONICAL)
    assert "Resolve governed pulse mode" in canonical
    assert '00|04) MODE="morning"' in canonical
    assert '08|12|16) MODE="commercial"' in canonical
    assert '20) MODE="evening"' in canonical


def test_ubuntu_workflows_do_not_use_windows_python_launcher() -> None:
    for path in (CANONICAL, *LEGACY_DAILY_PATHS):
        assert "py -3" not in _text(path), path


def test_cryptography_and_cffi_constraints_are_compatible() -> None:
    requirements = _text(ROOT / "requirements.txt")
    project = _text(ROOT / "pyproject.toml")
    # Current security pin moved cryptography to the 50.x line. Keep cffi on
    # the compatible >=2,<3 contract in both dependency authorities.
    assert "cryptography>=50.0.1,<51" in requirements
    assert "cffi>=2.0.0,<3" in requirements
    assert '"cffi>=2.0.0,<3"' in project


def test_production_trust_smoke_installs_asyncio_plugin() -> None:
    smoke = _text(WORKFLOWS / "production_api_trust_smoke.yml")
    assert "pytest-asyncio" in smoke
