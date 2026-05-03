"""
Forbidden-claims invariant — Dealix must never promise guaranteed sales.

Sweeps the static text surfaces of the repo and the classifier output for
forbidden tokens. The goal is to catch regressions where a marketing edit
sneaks "guaranteed", "نضمن", or similar into a customer-facing surface.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.safety import classify_intent


REPO = Path(__file__).resolve().parents[1]


# Tokens that must NEVER appear in customer-facing surfaces.
FORBIDDEN_TOKENS = (
    "guaranteed sales",
    "guaranteed revenue",
    "guaranteed leads",
    "guaranteed pipeline",
    "نضمن لك",
    "نضمن مبيعات",
    "نضمن إيرادات",
    "نضمن نتائج",
    "مضمون 100%",
    "guaranteed 100%",
)


# Surfaces we sweep — only files that ship as customer-facing text.
SCAN_GLOBS = [
    "landing/*.html",
    "auto_client_acquisition/safety/*.py",
    "auto_client_acquisition/customer_ops/*.py",
]


@pytest.mark.parametrize("token", FORBIDDEN_TOKENS)
def test_no_forbidden_token_in_customer_surfaces(token: str) -> None:
    matches: list[str] = []
    for pattern in SCAN_GLOBS:
        for path in REPO.glob(pattern):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            low = text.lower()
            if token.lower() in low:
                matches.append(str(path.relative_to(REPO)))
    assert not matches, f"Forbidden token {token!r} found in: {matches}"


def test_classifier_response_never_contains_guarantee() -> None:
    """The bilingual classifier must not return a 'guarantee' phrase."""
    samples = [
        "أبي عملاء أكثر",
        "I need more leads",
        "أبي تقرير للإدارة",
        "بدون موافقة",
    ]
    for s in samples:
        d = classify_intent(s)
        for k in ("reason_ar", "reason_en"):
            v = (getattr(d, k) or "").lower()
            assert "guarantee" not in v
            assert "نضمن" not in v
