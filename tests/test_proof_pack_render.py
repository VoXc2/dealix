"""Proof Pack renderer — markdown / PDF / email-body."""
from __future__ import annotations

from auto_client_acquisition.proof_architecture_os.proof_pack_render import (
    proof_pack_email_body,
    proof_pack_to_markdown,
    proof_pack_to_pdf,
)
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
)
from auto_client_acquisition.proof_to_market.pdf_renderer import is_pdf_available

_DISCLAIMER_AR = "النتائج التقديرية ليست نتائج مضمونة"


def _full_pack() -> dict:
    return {
        "engagement_id": "e1",
        "customer_id": "c1",
        "sections": {k: f"Content for {k}." for k in PROOF_PACK_V2_SECTIONS},
        "score": 100,
        "tier": "case_candidate",
    }


def test_markdown_renders_all_14_bilingual_sections():
    md = proof_pack_to_markdown(_full_pack(), customer_handle="Acme")
    assert md.count("## ") == len(PROOF_PACK_V2_SECTIONS) == 14
    assert "Executive Summary / الملخص التنفيذي" in md
    assert "Limitations / القيود والحدود" in md
    assert "Acme" in md
    assert _DISCLAIMER_AR in md


def test_markdown_empty_pack_renders_not_generated_notice():
    md = proof_pack_to_markdown({}, customer_handle="Acme")
    assert "not yet generated" in md.lower()
    assert "لم يُولَّد" in md
    # No fabricated section content for an empty pack.
    assert "## Executive Summary" not in md
    assert _DISCLAIMER_AR in md


def test_markdown_none_pack_is_safe():
    md = proof_pack_to_markdown(None, customer_handle="")
    assert "not yet generated" in md.lower()


def test_pdf_returns_bytes_or_none():
    pdf = proof_pack_to_pdf(_full_pack(), customer_handle="Acme")
    if is_pdf_available()["any"]:
        assert pdf is not None
        assert pdf[:5] == b"%PDF-"
    else:
        assert pdf is None


def test_email_body_is_bilingual_render_only():
    body = proof_pack_email_body(_full_pack(), customer_handle="Acme")
    assert "Acme" in body
    assert "Subject" in body
    assert "Proof score" in body
    assert "مرحباً" in body


def test_email_body_empty_pack_flags_not_generated():
    body = proof_pack_email_body({}, customer_handle="Acme")
    assert "not yet generated" in body.lower()


def test_render_coerces_non_string_section_values():
    """A non-string section value (arbitrary client JSON) must not crash
    rendering with an AttributeError."""
    pack = {
        "sections": {k: 0 for k in PROOF_PACK_V2_SECTIONS},
        "score": 10,
        "tier": "weak_proof",
    }
    pack["sections"]["executive_summary"] = 12345
    md = proof_pack_to_markdown(pack, customer_handle="Acme")
    assert "12345" in md


def test_render_handles_non_dict_pack():
    """A non-dict pack (malformed client JSON) renders the safe notice, not
    a 500/AttributeError."""
    assert "not yet generated" in proof_pack_to_markdown(
        123, customer_handle="X"
    ).lower()
    assert "not yet generated" in proof_pack_email_body(
        "garbage", customer_handle="X"
    ).lower()
