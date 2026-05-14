import json
from pathlib import Path


def test_founder_command_center_status_marker_exists():
    p = Path("data/founder_command_center_status.json")
    assert p.exists()
    data = json.loads(p.read_text())
    assert data["deployment_marker"] is True
    assert "Partner Motion" in data["required_cards"]
    assert "Invoice #1" in data["required_cards"]
