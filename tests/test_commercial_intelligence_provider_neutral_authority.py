from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/commercial/verify_commercial_intelligence.py"
SPEC = importlib.util.spec_from_file_location("verify_commercial_intelligence_provider_neutral", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _authority_root(tmp_path: Path, provider: str) -> Path:
    path = tmp_path / "dealix/config/railway_services.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"productionProviderAuthority": {"provider": provider}}), encoding="utf-8")
    return tmp_path


def test_current_provider_authority_is_supported_and_vercel_is_not_required() -> None:
    provider, required = MODULE.resolve_provider_requirements(ROOT)
    assert provider in {"railway", "selfhost"}
    assert "vercel.json" not in MODULE.REQUIRED
    assert all("vercel" not in item.lower() for items in MODULE.PROVIDER_REQUIRED.values() for item in items)
    assert required == MODULE.PROVIDER_REQUIRED[provider]


def test_railway_provider_requires_only_railway_authority_artifacts(tmp_path: Path) -> None:
    provider, required = MODULE.resolve_provider_requirements(_authority_root(tmp_path, "railway"))
    assert provider == "railway"
    assert "railway.json" in required
    assert "dealix/config/railway_services.json" in required
    assert "vercel.json" not in required


def test_selfhost_provider_requires_canonical_single_plane_artifacts(tmp_path: Path) -> None:
    provider, required = MODULE.resolve_provider_requirements(_authority_root(tmp_path, "selfhost"))
    assert provider == "selfhost"
    assert "deploy/selfhost/compose.yml" in required
    assert "scripts/ops/verify_selfhosted_production_plane.py" in required
    assert "scripts/ops/verify_selfhost_production_cutover_contract.py" in required
    assert "docker-compose.prod.yml" not in required


def test_unknown_provider_fails_closed(tmp_path: Path) -> None:
    try:
        MODULE.resolve_provider_requirements(_authority_root(tmp_path, "mystery-cloud"))
    except RuntimeError as exc:
        assert "unsupported production provider authority" in str(exc)
    else:
        raise AssertionError("unknown provider authority must fail closed")
