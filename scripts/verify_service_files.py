#!/usr/bin/env python3
"""Verify per-service file readiness for every offer under docs/services/.

سكربت التحقق من اكتمال ملفات كل خدمة تحت docs/services/.

Usage:
    python scripts/verify_service_files.py

Walks `docs/services/<offer>/` and confirms each folder ships the required
deliverable templates. The 3 starting offers must be complete; the two
expansion offers (ai_support_desk_sprint, ai_governance_program) are also
expected if present and are checked too. Exits 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SERVICES_ROOT = REPO / "docs" / "services"

# The 3 starting offers are mandatory.
STARTING_OFFERS: tuple[str, ...] = (
    "lead_intelligence_sprint",
    "ai_quick_win_sprint",
    "company_brain_sprint",
)

# Expansion offers — expected to exist; still required to be complete if present.
EXPANSION_OFFERS: tuple[str, ...] = (
    "ai_support_desk_sprint",
    "ai_governance_program",
)

EXPECTED_OFFERS: tuple[str, ...] = STARTING_OFFERS + EXPANSION_OFFERS

# Core templates required for every productized offer.
CORE_REQUIRED: tuple[str, ...] = (
    "offer.md",
    "scope.md",
    "qa_checklist.md",
    "delivery_checklist.md",
    "handoff.md",
    "upsell.md",
)

# Intake-style file: at least one of these must exist.
INTAKE_ALIASES: tuple[str, ...] = (
    "intake.md",
    "process_intake.md",
    "inbox_intake.md",
    "document_request.md",
)

# Proof-pack-style file: at least one of these must exist.
PROOF_ALIASES: tuple[str, ...] = (
    "proof_pack_template.md",
    "report_template.md",
    "support_report_template.md",
)


def _check_offer(offer_slug: str) -> tuple[bool, list[str]]:
    base = SERVICES_ROOT / offer_slug
    missing: list[str] = []
    if not base.is_dir():
        return False, [f"<folder missing: {base.relative_to(REPO)}>"]

    for fname in CORE_REQUIRED:
        if not (base / fname).is_file():
            missing.append(f"{offer_slug}/{fname}")

    if not any((base / a).is_file() for a in INTAKE_ALIASES):
        missing.append(f"{offer_slug}/<intake>(one of {', '.join(INTAKE_ALIASES)})")

    if not any((base / a).is_file() for a in PROOF_ALIASES):
        missing.append(f"{offer_slug}/<proof>(one of {', '.join(PROOF_ALIASES)})")

    return len(missing) == 0, missing


def _print(label: str, ok: bool, missing: list[str]) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}")
    for m in missing:
        print(f"       missing: {m}")


def main() -> int:
    print("== Dealix Service Files Readiness ==")
    if not SERVICES_ROOT.is_dir():
        print(f"[FAIL] services root missing: {SERVICES_ROOT.relative_to(REPO)}")
        print("--")
        print("SERVICE_FILES_PASS=false")
        return 1

    all_ok = True
    ready_count = 0

    for offer in EXPECTED_OFFERS:
        ok, missing = _check_offer(offer)
        _print(f"service folder: {offer}", ok, missing)
        all_ok &= ok
        if ok:
            ready_count += 1

    # Surface any *other* folders under docs/services/ so they don't drift silently.
    other = sorted(
        p.name for p in SERVICES_ROOT.iterdir()
        if p.is_dir() and p.name not in EXPECTED_OFFERS
    )
    if other:
        print(f"[INFO] additional service folders detected (not gated): {', '.join(other)}")

    print("--")
    print(f"SERVICE_FILES_PASS={'true' if all_ok else 'false'}")
    print(f"READY_SERVICES={ready_count}/{len(EXPECTED_OFFERS)}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
