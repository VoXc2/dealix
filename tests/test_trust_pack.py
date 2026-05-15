"""Enterprise trust pack section outline."""
from __future__ import annotations

from auto_client_acquisition.trust_os.trust_pack import (
    ENTERPRISE_TRUST_SECTIONS,
    TRUST_PACK_MARKDOWN_PATH,
)


def test_trust_sections_cover_the_core_outline():
    assert "what_dealix_does" in ENTERPRISE_TRUST_SECTIONS
    assert "what_dealix_does_not_do" in ENTERPRISE_TRUST_SECTIONS
    assert "ai_governance" in ENTERPRISE_TRUST_SECTIONS
    assert "human_oversight" in ENTERPRISE_TRUST_SECTIONS


def test_trust_sections_are_unique_and_nonempty():
    assert len(ENTERPRISE_TRUST_SECTIONS) == len(set(ENTERPRISE_TRUST_SECTIONS))
    assert all(s.strip() for s in ENTERPRISE_TRUST_SECTIONS)


def test_trust_pack_markdown_path_points_into_docs():
    assert TRUST_PACK_MARKDOWN_PATH.startswith("docs/")
    assert TRUST_PACK_MARKDOWN_PATH.endswith(".md")
