from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/governed_channel_runtime_v1.json"
VERIFIER = ROOT / "scripts/verify_governed_channel_runtime_v1.py"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_governed_channel_runtime_verifier_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "GOVERNED_CHANNEL_RUNTIME_V1_PASS" in result.stdout


def test_material_external_effects_default_deny() -> None:
    effects = _contract()["global_external_effects_default"]
    assert effects
    assert all(value is False for value in effects.values())


def test_five_canonical_agents_only() -> None:
    service_model = _contract()["service_model"]
    assert service_model["permanent_agent_count"] == 5
    assert set(service_model["canonical_agents"]) == {
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    }


def test_social_and_messaging_boundaries_are_fail_closed() -> None:
    channels = _contract()["channels"]
    assert "unbounded_cold_bulk_email" in channels["email"]["blocked"]
    assert "send_after_opt_out" in channels["email"]["blocked"]
    assert "scraping" in channels["founder_linkedin"]["blocked"]
    assert "bot_dms" in channels["founder_linkedin"]["blocked"]
    assert "cold_whatsapp" in channels["whatsapp"]["blocked"]
    assert "bulk_unsolicited_whatsapp" in channels["whatsapp"]["blocked"]
    assert "public_publish_without_official_capability_and_authority" in channels["instagram_facebook_threads_x"]["blocked"]


def test_research_cannot_manufacture_commercial_truth() -> None:
    rules = _contract()["state_rules"]
    assert rules["research_cannot_promote_relationship"] is True
    assert rules["public_data_cannot_promote_consent"] is True
    assert rules["raw_engagement_cannot_promote_opportunity"] is True
    assert rules["payment_truth_requires_payment_evidence"] is True
