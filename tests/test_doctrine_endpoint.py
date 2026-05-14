"""Open Governed AI Operations Doctrine — Wave 19 public endpoint."""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.governance_os.non_negotiables import NON_NEGOTIABLES

client = TestClient(app)
REPO = Path(__file__).resolve().parent.parent


def test_doctrine_endpoint_is_public_no_admin_required():
    resp = client.get("/api/v1/doctrine")
    assert resp.status_code == 200
    body = resp.json()
    assert body["public_framework"] is True
    assert body["commercial_reference_implementation"] == "Dealix"
    assert body["governance_decision"] == "allow"


def test_doctrine_has_11_non_negotiables():
    body = client.get("/api/v1/doctrine").json()
    assert body["non_negotiables_count"] == 11
    assert len(body["controls"]) == 11


def test_doctrine_control_mapping_complete():
    body = client.get("/api/v1/doctrine").json()
    required = {
        "id", "name_en", "name_ar",
        "control_summary_en", "control_summary_ar",
        "refusal_en", "refusal_ar",
        "evidence_artifact", "test_reference",
    }
    for c in body["controls"]:
        missing = required - set(c.keys())
        assert not missing, f"{c.get('id')} missing fields: {missing}"
        assert c["test_reference"], f"{c['id']} must list at least one test reference"


def test_doctrine_license_posture_dual_layer():
    """Doctrine text under CC BY 4.0; code examples under MIT; trademark reserved."""
    body = client.get("/api/v1/doctrine").json()
    assert "CC BY 4.0" in body["license_doctrine"]
    assert body["license_code_examples"] == "MIT"
    assert "Dealix" in body["trademark_note"]


def test_doctrine_markdown_endpoint_is_bilingual():
    resp = client.get("/api/v1/doctrine/markdown")
    assert resp.status_code == 200
    body = resp.text
    assert "Governed AI Operations Doctrine" in body
    assert "دستور تشغيل AI المحوكم" in body
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body


def test_doctrine_controls_endpoint_returns_just_controls():
    body = client.get("/api/v1/doctrine/controls").json()
    assert body["controls_count"] == 11
    for c in body["controls"]:
        assert c["id"].startswith("NN-")


def test_public_doctrine_repo_files_exist_when_present():
    """If open-doctrine/* files exist on disk, they must not reference
    commercial-sensitive tokens. Acts as a canary against accidentally
    publishing internal materials in the open framework."""
    open_doctrine_dir = REPO / "open-doctrine"
    if not open_doctrine_dir.exists():
        return  # files not yet written; agent still in flight
    forbidden = (
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
    )
    violations: list[str] = []
    for path in open_doctrine_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for tok in forbidden:
            if tok in text:
                rel = path.relative_to(REPO)
                violations.append(f"{rel}: contains forbidden token {tok!r}")
    assert not violations, "\n".join(violations)
