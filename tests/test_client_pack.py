"""Client pack generator — proposal + deck notes."""

from __future__ import annotations

from dealix.commercial_ops.client_pack import build_client_pack_from_row


def test_build_client_pack_from_row_writes_manifest(tmp_path, monkeypatch):
    from dealix.commercial_ops import client_pack as cp

    monkeypatch.setattr(cp, "CLIENT_PACKS_DIR", tmp_path)

    row = {
        "company": "وكالة اختبار",
        "contact": "مدير",
        "segment": "agency_wedge",
        "pain_hypothesis": "لا proof أسبوعي",
        "offer_id": "ten_lead_audit",
        "motion": "A",
        "channel": "email_warm",
    }
    pack = build_client_pack_from_row(row, write_disk=True)
    assert pack["company"] == "وكالة اختبار"
    assert "proposal" in pack
    assert pack["paths"].get("directory")
    slug_dir = tmp_path / "وكالة-اختبار"
    assert (slug_dir / "proposal.md").is_file()
    assert (slug_dir / "manifest.json").is_file()
