from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "company" / "dealix_command_room_v1.json"


def test_command_room_registers_event_driven_reply_intelligence_without_live_authority() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    intelligence = config["conversation_intelligence"]
    whatsapp = next(channel for channel in config["channels"] if channel["id"] == "whatsapp-business")

    assert intelligence["owner"] == "dealix-sales"
    assert intelligence["model_policy"] == "LOCAL_FIRST"
    assert intelligence["supported_languages"] == ["ar", "en"]
    assert set(intelligence["supported_intents"]) == {
        "pricing",
        "objection",
        "meeting",
        "support",
        "general",
    }
    assert intelligence["negotiation_mode"] == "NON_BINDING_PREPARATION"
    assert intelligence["material_terms_escalate"] is True
    assert intelligence["provider_execution_allowed_by_reply_engine"] is False
    assert intelligence["event_driven"] is True
    assert intelligence["source_ready"] is True
    assert intelligence["runtime_verified"] is False

    assert whatsapp["graph_api_version_env_ref"] == "WHATSAPP_GRAPH_API_VERSION"
    assert whatsapp["graph_api_default"] == "v26.0"
    assert whatsapp["draft_intelligence_source_ready"] is True
    assert whatsapp["runtime_verified"] is False
    assert whatsapp["live_execution_ready"] is False
