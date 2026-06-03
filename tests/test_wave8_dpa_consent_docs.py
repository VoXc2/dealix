"""Wave 8 — DPA & Consent Documents tests."""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WAVE8_DIR = REPO_ROOT / "docs" / "wave8"

REQUIRED_DOCS = {
    "DPA_CHECKLIST_AR_EN.md":             WAVE8_DIR / "DPA_CHECKLIST_AR_EN.md",
    "CONSENT_RECORD_TEMPLATE.json":       WAVE8_DIR / "CONSENT_RECORD_TEMPLATE.json",
    "DSR_REQUEST_TEMPLATE.md":            WAVE8_DIR / "DSR_REQUEST_TEMPLATE.md",
    "PROOF_PUBLICATION_CONSENT_TEMPLATE.md": WAVE8_DIR / "PROOF_PUBLICATION_CONSENT_TEMPLATE.md",
    "WHATSAPP_CONSENT_CHECKLIST_AR_EN.md": WAVE8_DIR / "WHATSAPP_CONSENT_CHECKLIST_AR_EN.md",
    "WAVE8_DPA_AND_CONSENT_READINESS.md": REPO_ROOT / "docs" / "WAVE8_DPA_AND_CONSENT_READINESS.md",
}


def test_all_dpa_consent_docs_exist():
    for name, path in REQUIRED_DOCS.items():
        assert path.exists(), f"Missing DPA/consent doc: {name} at {path}"


def test_dpa_checklist_has_arabic():
    content = (WAVE8_DIR / "DPA_CHECKLIST_AR_EN.md").read_text(encoding="utf-8")
    assert "PDPL" in content
    assert "محامٍ" in content or "lawyer" in content.lower()


def test_consent_record_template_valid_json():
    content = (WAVE8_DIR / "CONSENT_RECORD_TEMPLATE.json").read_text(encoding="utf-8")
    data = json.loads(content)
    assert data["_schema"] == "wave8_consent_record_v1"
    assert "consent_events" in data
    assert isinstance(data["consent_events"], list)


def test_consent_record_has_dpa_event():
    data = json.loads((WAVE8_DIR / "CONSENT_RECORD_TEMPLATE.json").read_text(encoding="utf-8"))
    types = [e["consent_type"] for e in data["consent_events"]]
    assert "dpa_signing" in types


def test_consent_record_has_whatsapp_event():
    data = json.loads((WAVE8_DIR / "CONSENT_RECORD_TEMPLATE.json").read_text(encoding="utf-8"))
    types = [e["consent_type"] for e in data["consent_events"]]
    assert "whatsapp_opt_in" in types


def test_dsr_template_mentions_30_days():
    content = (WAVE8_DIR / "DSR_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")
    assert "30" in content  # 30-day legal deadline


def test_proof_publication_consent_no_fake_results():
    content = (WAVE8_DIR / "PROOF_PUBLICATION_CONSENT_TEMPLATE.md").read_text(encoding="utf-8")
    assert "fabricated" in content.lower() or "مصطنعة" in content


def test_whatsapp_consent_mentions_cold_blocked():
    content = (WAVE8_DIR / "WHATSAPP_CONSENT_CHECKLIST_AR_EN.md").read_text(encoding="utf-8")
    assert "cold" in content.lower() or "بارد" in content


def test_dpa_readiness_doc_mentions_lawyer_review():
    content = (REPO_ROOT / "docs" / "WAVE8_DPA_AND_CONSENT_READINESS.md").read_text(encoding="utf-8")
    assert "lawyer" in content.lower() or "محامٍ" in content


def test_dpa_readiness_doc_has_pdpl_section():
    content = (REPO_ROOT / "docs" / "WAVE8_DPA_AND_CONSENT_READINESS.md").read_text(encoding="utf-8")
    assert "PDPL" in content
