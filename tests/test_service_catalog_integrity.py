"""Service catalog integrity — confirms required service folders + files exist.

اختبارات تكامل كاتالوج الخدمات — يتأكد من اكتمال مجلدات وملفات الخدمات.

Mirrors `scripts/verify_service_files.py` but at pytest granularity so CI
catches regressions in the per-service folder layout.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("pydantic", reason="pydantic required for service catalog tests")

REPO = Path(__file__).resolve().parent.parent
SERVICES_ROOT = REPO / "docs" / "services"

STARTING_OFFERS: tuple[str, ...] = (
    "lead_intelligence_sprint",
    "ai_quick_win_sprint",
    "company_brain_sprint",
)

CORE_REQUIRED: tuple[str, ...] = (
    "offer.md",
    "scope.md",
    "qa_checklist.md",
)

INTAKE_ALIASES: tuple[str, ...] = (
    "intake.md",
    "process_intake.md",
    "inbox_intake.md",
    "document_request.md",
)

PROOF_ALIASES: tuple[str, ...] = (
    "proof_pack_template.md",
    "report_template.md",
    "support_report_template.md",
)


def _missing_for(offer: str) -> list[str]:
    base = SERVICES_ROOT / offer
    missing: list[str] = []
    if not base.is_dir():
        return [f"{offer}/<folder>"]
    for fname in CORE_REQUIRED:
        if not (base / fname).is_file():
            missing.append(f"{offer}/{fname}")
    if not any((base / a).is_file() for a in INTAKE_ALIASES):
        missing.append(f"{offer}/<intake>")
    if not any((base / a).is_file() for a in PROOF_ALIASES):
        missing.append(f"{offer}/<proof>")
    return missing


def test_services_root_directory_exists():
    assert SERVICES_ROOT.is_dir(), f"services root missing: {SERVICES_ROOT}"


@pytest.mark.parametrize("offer", STARTING_OFFERS)
def test_starting_offer_folder_has_required_files(offer: str):
    missing = _missing_for(offer)
    assert not missing, (
        f"service folder '{offer}' is missing files: " + ", ".join(missing)
    )


def test_all_starting_offers_have_proof_pack_template():
    failed: list[str] = []
    for offer in STARTING_OFFERS:
        candidates = [SERVICES_ROOT / offer / a for a in PROOF_ALIASES]
        if not any(c.is_file() for c in candidates):
            failed.append(offer)
    assert not failed, (
        "starting offers missing a proof/report template: " + ", ".join(failed)
    )


def test_missing_offer_folder_is_reported():
    """Negative path — a clearly bogus slug must be reported as missing."""
    missing = _missing_for("__definitely_not_a_real_offer__")
    assert missing, "expected missing entries for a non-existent offer"
    assert any("<folder>" in m for m in missing)
