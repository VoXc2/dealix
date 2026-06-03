"""GTM ABM wave 1 config — structure smoke."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / "dealix" / "config" / "gtm_abm_wave1.yaml"
PLAYBOOK = REPO / "docs" / "commercial" / "GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md"


def test_gtm_abm_wave1_yaml_loads() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert data["wave_id"] == "abm_wave_1"
    assert data["account_count"]["min"] == 30
    assert data["account_count"]["target"] == 50
    assert "cold_whatsapp" in data["channels_forbidden"]


def test_gtm_playbook_and_abm_doc_exist() -> None:
    assert PLAYBOOK.is_file()
    assert (REPO / "docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md").is_file()
    assert (REPO / "docs/commercial/operations/GTM_DUAL_TRACK_CLARIFICATION_AR.md").is_file()
