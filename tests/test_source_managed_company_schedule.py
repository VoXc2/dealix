from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts/ops/verify_source_managed_company_schedule.py"
TEMPLATES = ROOT / "scripts/ops/runtime_templates/autonomous_company"


def load_verifier():
    spec = importlib.util.spec_from_file_location("schedule_verify", VERIFY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_templates_include_content_and_delivery_cycles() -> None:
    dispatch = (TEMPLATES / "dealix-company-dispatch.core-v6").read_text()
    cycle = (TEMPLATES / "dealix-company-cycle").read_text()
    for token in ("1130 45 content_morning", "1330 45 delivery_midday", "1630 45 content_afternoon"):
        assert token in dispatch
    assert "scripts/dealix_content_factory_daily.py" in cycle
    assert "scripts/verify_delivery_os.py" in cycle
    assert "PUBLIC_PUBLISH=false" in cycle
    sentinel = (TEMPLATES / "dealix-server-sentinel").read_text()
    assert "RAILWAY_BIN=" not in sentinel
    assert "RAILWAY_CLI=" not in sentinel
    assert "SELFHOST_LOCAL_API_SHA=" in sentinel
    assert "SELFHOST_LOCAL_WEB_SHA=" in sentinel
    assert "SELFHOST_RUNTIME_PARITY=PASS" in sentinel
    assert "API_RELEASE_PARITY=PASS" in sentinel
    assert "SENTINEL_RESULT=PASS_WITH_WARNINGS" in sentinel
    # Availability stays on /healthz; immutable API identity comes from /version.
    assert 'check_http API https://api.dealix.me/healthz 1' in sentinel
    assert 'API_JSON=$(curl -fsS --max-time 12 https://api.dealix.me/version' in sentinel


def test_sentinel_uses_version_for_release_identity() -> None:
    sentinel = (TEMPLATES / "dealix-server-sentinel").read_text()
    assert 'check_http API https://api.dealix.me/healthz 1' in sentinel
    assert 'API_JSON=$(curl -fsS --max-time 12 https://api.dealix.me/version' in sentinel
    assert 'd.get("git_sha")' in sentinel
    assert 'API_RELEASE_PARITY' in sentinel




def test_sentinel_has_no_legacy_railway_authority() -> None:
    sentinel = (TEMPLATES / "dealix-server-sentinel").read_text()
    for token in ("RAILWAY_BIN=", "RAILWAY_CLI=", "dealix-railway-status.json"):
        assert token not in sentinel
    for token in ("SELFHOST_LOCAL_API_SHA=", "SELFHOST_LOCAL_WEB_SHA=", "SELFHOST_RUNTIME_PARITY=PASS"):
        assert token in sentinel

def test_verifier_detects_exact_runtime_and_drift(tmp_path: Path) -> None:
    verifier = load_verifier()
    for name in verifier.FILES:
        shutil.copy2(TEMPLATES / name, tmp_path / name)
    ok, errors = verifier.evaluate(tmp_path)
    assert ok, errors

    dispatch = tmp_path / "dealix-company-dispatch.core-v6"
    dispatch.write_text(dispatch.read_text().replace("1630 45 content_afternoon", "1650 45 content_afternoon"))
    ok, errors = verifier.evaluate(tmp_path)
    assert not ok
    assert any("runtime drift" in error or "missing schedule token" in error for error in errors)
