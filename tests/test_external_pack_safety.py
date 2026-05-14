"""Smoke: partner/client/investor motion docs and registry avoid risky artifact references."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SCAN_RELS = (
    "docs/strategic/packs/PARTNER_MOTION_PACK_AR.md",
    "docs/strategic/packs/INVESTOR_MOTION_PACK_AR.md",
    "docs/strategic/packs/CLIENT_DEMO_PACK_AR.md",
    "docs/strategic/EXTERNAL_PACK_REGISTRY_AR.md",
)

# Substrings that should not appear in outbound-facing pack copy (case-insensitive).
_FORBIDDEN = (
    "partner_outreach_log.json",
    "first_invoice_log.json",
    "admin_key",
    "localstorage",
    "private_pricing",
)


def _combined_text() -> str:
    parts: list[str] = []
    for rel in SCAN_RELS:
        p = REPO_ROOT / rel
        assert p.is_file(), f"missing {rel}"
        parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts).lower()


def test_external_motion_docs_avoid_sensitive_artifacts() -> None:
    blob = _combined_text()
    for needle in _FORBIDDEN:
        assert needle not in blob, f"forbidden reference {needle!r} in external pack surface"
