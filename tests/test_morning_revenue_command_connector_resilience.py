from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_morning_revenue_command.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("dealix_morning_revenue_command", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_morning_command_survives_missing_external_connector_evidence(tmp_path: Path) -> None:
    module = _load_generator()

    current = tmp_path / "current"
    current.mkdir()
    (current / "economic_truth.json").write_text(
        json.dumps(
            {
                "verified_revenue_sar": 0,
                "verified_paid_pilots": 0,
                "real_interactions": 0,
                "verified_relationships": 0,
                "qualified_problems": 0,
                "diagnostics_active": 0,
                "discoveries_active": 0,
                "customer_specific_proposals": 0,
            }
        ),
        encoding="utf-8",
    )

    command = module.build(current)

    assert command["connectors"]["hubspot"] == module.UNKNOWN
    assert command["connectors"]["posthog"] == module.UNKNOWN
    assert command["connectors"]["clay"] == module.UNKNOWN
    assert command["connectors"]["canva"] == module.UNKNOWN
    assert command["money"]["verified_revenue_sar"] == module.UNKNOWN
    assert command["next_best_action"]["action"] == "CAPTURE_REAL_RELATIONSHIP_EVIDENCE"


def test_morning_command_uses_local_connector_receipt_without_network_dependency(tmp_path: Path) -> None:
    module = _load_generator()

    current = tmp_path / "current"
    current.mkdir()
    (current / "connector_receipt.json").write_text(
        json.dumps(
            {
                "schema": "dealix.connector-receipt.runtime.v1",
                "scope": "dealix_company",
                "hubspot_status": "DEGRADED_ADAPTER_NOT_FATAL",
                "posthog_status": "READY",
                "verified_revenue_sar": 0,
                "verified_paid_pilots": 0,
                "verified_relationships": 0,
                "diagnostics_active": 0,
            }
        ),
        encoding="utf-8",
    )

    command = module.build(current)

    assert command["connectors"]["hubspot"] == "DEGRADED_ADAPTER_NOT_FATAL"
    assert command["connectors"]["posthog"] == "READY"
    assert command["next_best_action"]["action"] == "CAPTURE_REAL_RELATIONSHIP_EVIDENCE"
