from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_JSON = ROOT / "landing/assets/data/services-catalog.json"
FRONTEND_SNAPSHOT = ROOT / "apps/web/lib/service-catalog-snapshot.ts"
GENERATOR = ROOT / "scripts/commercial/generate_service_catalog_snapshot.py"
EXPORTER = ROOT / "scripts/dealix_export_service_catalog_json.py"


def _public_catalog() -> dict:
    return json.loads(PUBLIC_JSON.read_text(encoding="utf-8"))


def test_public_catalog_has_only_governed_launch_path() -> None:
    data = _public_catalog()
    assert data["public_commercial_truth"] == "one_governed_path"
    assert [item["id"] for item in data["offerings"]] == [
        "free_mini_diagnostic",
        "revenue_command_pilot_30d",
    ]
    paid = data["offerings"][1]
    assert paid["pricing"] == "customer_specific_quote_after_qualified_discovery"
    assert paid["commercial_status"] == "quote_only"
    assert paid["public_checkout"] is False
    assert paid["customer_result_guarantee"] is False


def test_frontend_snapshot_contains_only_public_authority() -> None:
    text = FRONTEND_SNAPSHOT.read_text(encoding="utf-8")
    assert '"public_only": true' in text
    assert '"free_mini_diagnostic"' in text
    assert '"revenue_command_pilot_30d"' in text
    for stale in (
        "data_to_revenue_pack_1500",
        "growth_ops_monthly_2999",
        "support_os_addon_1500",
        "executive_command_center_7500",
        "ai_agent_workforce_os",
        '"price_sar"',
        '"price_monthly_sar_min"',
        '"price_monthly_sar_max"',
    ):
        assert stale not in text, stale


def test_frontend_generator_uses_governed_public_projection() -> None:
    source = GENERATOR.read_text(encoding="utf-8")
    assert "dealix_export_service_catalog_json.py" in source
    assert "build_catalog_dict" in source
    assert "list_offerings" not in source


def test_exporter_output_matches_committed_public_catalog() -> None:
    spec = importlib.util.spec_from_file_location("dealix_public_catalog_test", EXPORTER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build_catalog_dict() == _public_catalog()
