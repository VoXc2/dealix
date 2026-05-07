"""Wave 8 — Integration Registry tests."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_YAML = REPO_ROOT / "docs" / "wave8" / "integration_registry.yaml"
REGISTRY_MD = REPO_ROOT / "docs" / "WAVE8_INTEGRATION_REGISTRY.md"

REQUIRED_INTEGRATIONS = [
    "Google Sheets", "Google Drive", "HubSpot", "Gmail Drafts",
    "WhatsApp Business", "Moyasar", "Resend", "Slack", "Notion",
    "Chatwoot", "Cal.com", "Langfuse", "OpenTelemetry", "PostHog",
    "Qdrant", "pgvector", "Sentry", "Meta WhatsApp Templates",
    "Railway", "GitHub Actions",
]

HARD_BLOCKED_ACTIONS = [
    "live_customer_outbound", "auto_send", "live_charge",
    "cold_whatsapp", "bulk_whatsapp",
]


def test_registry_yaml_exists():
    assert REGISTRY_YAML.exists(), "integration_registry.yaml must exist"


def test_registry_md_exists():
    assert REGISTRY_MD.exists(), "WAVE8_INTEGRATION_REGISTRY.md must exist"


def test_registry_has_20_integrations():
    try:
        import yaml
    except ImportError:
        # If yaml not installed, test the MD file instead
        content = REGISTRY_MD.read_text(encoding="utf-8")
        for name in REQUIRED_INTEGRATIONS:
            assert name in content, f"Integration '{name}' missing from registry MD"
        return

    data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
    names = [i["name"] for i in data["integrations"]]
    assert len(names) == 20, f"Expected 20 integrations, got {len(names)}"


def test_registry_all_required_integrations_present():
    try:
        import yaml
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
        names = [i["name"] for i in data["integrations"]]
    except ImportError:
        content = REGISTRY_MD.read_text(encoding="utf-8")
        names = content
    for name in REQUIRED_INTEGRATIONS:
        assert name in names, f"Required integration '{name}' missing"


def test_registry_moyasar_blocked():
    try:
        import yaml
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
        moyasar = next(i for i in data["integrations"] if i["name"] == "Moyasar")
        assert moyasar["live_gate"] == "blocked", "Moyasar live_gate must be blocked"
        assert not moyasar["write_allowed"], "Moyasar write_allowed must be false"
        assert "live_charge" in moyasar["blocked_actions"]
    except ImportError:
        content = REGISTRY_YAML.read_text(encoding="utf-8")
        assert "live_gate: blocked" in content


def test_registry_whatsapp_blocked_outbound():
    try:
        import yaml
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
        wa = next(i for i in data["integrations"] if i["name"] == "WhatsApp Business")
        assert not wa["write_allowed"], "WhatsApp write_allowed must be false"
        assert "live_customer_outbound" in wa["blocked_actions"]
    except ImportError:
        content = REGISTRY_YAML.read_text(encoding="utf-8")
        assert "live_customer_outbound" in content


def test_registry_gmail_drafts_only():
    try:
        import yaml
        data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
        gmail = next(i for i in data["integrations"] if i["name"] == "Gmail Drafts")
        assert "live_send" in gmail["blocked_actions"]
        assert "auto_send" in gmail["blocked_actions"]
    except ImportError:
        content = REGISTRY_YAML.read_text(encoding="utf-8")
        assert "live_send" in content


def test_registry_schema_required_fields():
    try:
        import yaml
    except ImportError:
        return  # Skip schema test if yaml unavailable

    data = yaml.safe_load(REGISTRY_YAML.read_text(encoding="utf-8"))
    required_fields = {
        "name", "purpose", "current_status", "required_env_vars",
        "live_gate", "customer_facing", "requires_dpa",
        "requires_human_approval", "risk_level", "safe_default",
        "first_customer_needed", "fallback_behavior", "blocked_actions",
    }
    for integration in data["integrations"]:
        missing = required_fields - set(integration.keys())
        assert not missing, f"Integration '{integration.get('name')}' missing fields: {missing}"
