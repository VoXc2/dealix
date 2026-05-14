"""PDF renderer — Wave 14D.4."""
from __future__ import annotations

from auto_client_acquisition.proof_to_market.pdf_renderer import (
    is_pdf_available,
    render_markdown_to_pdf,
)


def test_render_returns_none_on_empty_input():
    assert render_markdown_to_pdf("") is None


def test_is_pdf_available_returns_shape():
    info = is_pdf_available()
    assert "weasyprint" in info
    assert "pandoc" in info
    assert "any" in info
    assert isinstance(info["any"], bool)


def test_render_gracefully_handles_missing_backend():
    # When neither weasyprint nor pandoc is available, returns None (NOT raise).
    info = is_pdf_available()
    pdf = render_markdown_to_pdf("# Hello\n\nWorld.", title="Test")
    if info["any"]:
        # If a backend exists, PDF bytes start with %PDF-.
        assert pdf is not None
        assert pdf[:5] == b"%PDF-"
    else:
        assert pdf is None
