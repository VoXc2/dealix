"""Wave 11 §31.13 — Legal self-execution guard.

Compile-time enforcement that the founder cannot accidentally:
1. Modify the DPA without re-signing (SHA256 mismatch detection)
2. Sell to a customer without the legal pack present

The guard is INTENTIONALLY soft about the founder's signature itself —
the file ``data/wave11/founder_legal_signature.txt`` is gitignored and
optional. If absent, the test PASSES with a warning (founder hasn't
signed yet); if present with a wrong SHA, the test FAILS (DPA was
modified after signing).

References:
- docs/LEGAL_FOUNDER_SELF_EXECUTION.md §7 (signature placeholder)
- docs/DPA_DEALIX_FULL.md (the document the founder signs)
- docs/wave8/DPA_CHECKLIST_AR_EN.md (per-customer checklist)
- landing/privacy.html (must reference the v2 doc)
"""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_legal_self_execution_doc_exists_and_has_signature_section():
    """The founder-self-execution doc must exist + have §7 signature placeholder."""
    doc = REPO_ROOT / "docs" / "LEGAL_FOUNDER_SELF_EXECUTION.md"
    assert doc.exists(), f"Missing legal self-execution doc: {doc}"
    content = doc.read_text(encoding="utf-8")
    # §7 placeholder MUST exist (the founder's commitment)
    assert "## 7." in content or "§7" in content or "## 7 " in content, \
        "LEGAL_FOUNDER_SELF_EXECUTION.md missing §7 signature section"
    # Placeholder line: "**Signed:** ___" / "Signed: ___" / "Sign here" etc.
    # Markdown bold variants (`**Signed:**`) are common — colon may sit inside
    # the bold markers OR after them. Multiple underscores = fillable slot.
    assert re.search(
        r"(\*+)?Signed[:\*\s]+_{3,}|(\*+)?signature[:\*\s]+_{3,}|Sign here",
        content,
        re.IGNORECASE,
    ), "LEGAL_FOUNDER_SELF_EXECUTION.md §7 missing 'Signed: ___' placeholder line"


def test_dpa_and_privacy_and_terms_v2_present():
    """The 3 customer-facing legal docs must all exist."""
    expected = [
        REPO_ROOT / "docs" / "DPA_DEALIX_FULL.md",
        REPO_ROOT / "docs" / "PRIVACY_POLICY_v2.md",
        REPO_ROOT / "docs" / "TERMS_OF_SERVICE_v2.md",
    ]
    missing = [p for p in expected if not p.exists()]
    assert not missing, f"Legal pack incomplete — missing: {missing}"
    # Each must be non-trivial (>1KB)
    for p in expected:
        size = p.stat().st_size
        assert size >= 1024, f"{p.name} suspiciously small ({size} bytes) — likely placeholder"


def test_dpa_checklist_present():
    """Per-customer DPA checklist (Wave 8) must exist."""
    checklist = REPO_ROOT / "docs" / "wave8" / "DPA_CHECKLIST_AR_EN.md"
    assert checklist.exists(), \
        f"Missing per-customer DPA checklist: {checklist}"


def test_dpa_signature_integrity_or_warn_if_unsigned():
    """If the founder has signed the DPA (gitignored signature file present),
    the DPA's current SHA256 MUST match the signed hash. If unsigned, this
    test PASSES with a warning — the founder may sign before customer #1.

    Format of ``data/wave11/founder_legal_signature.txt``:
        signed_by: Sami Assiri
        signed_at: 2026-05-09
        dpa_sha256: <64 hex chars>
    """
    sig_file = REPO_ROOT / "data" / "wave11" / "founder_legal_signature.txt"
    dpa = REPO_ROOT / "docs" / "DPA_DEALIX_FULL.md"

    # Case A — DPA file itself must always exist
    assert dpa.exists(), f"DPA missing: {dpa}"

    # Case B — signature file may or may not exist (gitignored, founder action)
    if not sig_file.exists():
        # Soft pass — founder hasn't signed yet. Print to stderr for visibility.
        import sys
        print(
            f"\n⚠️  WAVE11 LEGAL GUARD: data/wave11/founder_legal_signature.txt absent — "
            f"founder has not yet signed the DPA. This is acceptable until customer #1 "
            f"closes; signature file format documented in test_legal_self_execution_guard.py.",
            file=sys.stderr,
        )
        return

    # Case C — signature exists; the SHA must match
    sig_text = sig_file.read_text(encoding="utf-8")
    sha_match = re.search(r"dpa_sha256:\s*([0-9a-fA-F]{64})", sig_text)
    assert sha_match, (
        f"data/wave11/founder_legal_signature.txt present but missing 'dpa_sha256: <hex>' line. "
        f"Format: signed_by/signed_at/dpa_sha256. Current content (first 200 chars):\n"
        f"{sig_text[:200]}"
    )
    signed_sha = sha_match.group(1).lower()
    actual_sha = _sha256(dpa)
    assert signed_sha == actual_sha, (
        f"⛔ DPA WAS MODIFIED AFTER SIGNATURE.\n"
        f"  signed_sha: {signed_sha}\n"
        f"  actual_sha: {actual_sha}\n"
        f"  Action: founder MUST re-review the DPA + re-sign by updating "
        f"data/wave11/founder_legal_signature.txt with the new SHA256."
    )
