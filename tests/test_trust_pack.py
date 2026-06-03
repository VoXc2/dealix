"""Trust pack assembler + endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.trust_os.trust_pack import assemble_trust_pack

client = TestClient(app)


def test_assemble_trust_pack_has_all_11_sections():
    pack = assemble_trust_pack(customer_handle="enterprise_prospect")
    required_sections = {
        "what_dealix_does",
        "what_dealix_refuses",
        "data_handling",
        "source_passport_policy",
        "governance_runtime",
        "ai_run_ledger",
        "human_oversight",
        "approval_workflow",
        "proof_pack_standard",
        "incident_response",
        "client_responsibilities",
    }
    assert required_sections <= set(pack.sections.keys())


def test_trust_pack_markdown_has_disclaimer():
    pack = assemble_trust_pack(customer_handle="prospect")
    md = pack.to_markdown()
    assert "Estimated outcomes are not guaranteed outcomes" in md
    assert "النتائج التقديرية" in md


def test_trust_pack_lists_all_11_non_negotiables():
    pack = assemble_trust_pack()
    refuses = pack.sections["what_dealix_refuses"]
    for rule in (
        "No scraping",
        "No cold WhatsApp",
        "No LinkedIn automation",
        "No fake / un-sourced claims",
        "No guaranteed sales outcomes",
        "No PII in logs",
        "No source-less knowledge answers",
        "No external action without approval",
        "No agent without identity",
        "No project without Proof Pack",
        "No project without Capital Asset",
    ):
        assert rule in refuses, f"missing rule: {rule}"


def test_trust_pack_endpoint_json():
    resp = client.get("/api/v1/value/trust-pack/enterprise_prospect")
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_handle"] == "enterprise_prospect"
    assert "sections" in body


def test_trust_pack_endpoint_markdown():
    resp = client.get("/api/v1/value/trust-pack/enterprise_prospect/markdown")
    assert resp.status_code == 200
    assert "Trust Pack" in resp.text
    assert "Governance Runtime" in resp.text
