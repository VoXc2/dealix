#!/usr/bin/env python3
"""Verify proof_pack_template.md files contain required sections.

سكربت التحقق من اكتمال أقسام قوالب حِزَم الإثبات (Proof Pack).

Usage:
    python scripts/verify_proof_pack.py

Walks `docs/services/<offer>/proof_pack_template.md` and checks each one
contains the canonical Stage-7 sections (case-insensitive substring match):
Inputs, Outputs, Business impact, Artifacts, Next step. Exits 0 on PASS.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SERVICES_ROOT = REPO / "docs" / "services"

REQUIRED_SECTIONS: tuple[str, ...] = (
    "Inputs",
    "Outputs",
    "Business impact",
    "Artifacts",
    "Next step",
)


def _check_proof_pack(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8").lower()
    missing: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section.lower() not in text:
            missing.append(section)
    return missing


def main() -> int:
    print("== Dealix Proof Pack Templates ==")
    if not SERVICES_ROOT.is_dir():
        print(f"[FAIL] services root missing: {SERVICES_ROOT.relative_to(REPO)}")
        print("--")
        print("PROOF_PACK_PASS=false")
        return 1

    proof_files = sorted(SERVICES_ROOT.glob("*/proof_pack_template.md"))
    if not proof_files:
        print("[FAIL] no proof_pack_template.md files found under docs/services/*/")
        print("--")
        print("PROOF_PACK_PASS=false")
        return 1

    all_ok = True
    checked = 0
    for path in proof_files:
        rel = path.relative_to(REPO)
        missing = _check_proof_pack(path)
        if missing:
            print(f"[FAIL] {rel}")
            for section in missing:
                print(f"       missing section: {section}")
            all_ok = False
        else:
            print(f"[PASS] {rel}")
        checked += 1

    print("--")
    print(f"PROOF_PACK_PASS={'true' if all_ok else 'false'}")
    print(f"PROOF_PACK_FILES_CHECKED={checked}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
