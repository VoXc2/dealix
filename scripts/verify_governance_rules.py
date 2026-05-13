#!/usr/bin/env python3
"""Verify Governance OS files exist and compile.

سكربت التحقق من وجود وسلامة ملفات Governance OS.

Usage:
    python scripts/verify_governance_rules.py

For each Trust/Governance source file, confirm presence and that it
py_compile's successfully. Exits 0 on PASS, non-zero on FAIL.
"""
from __future__ import annotations

import py_compile
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

GOVERNANCE_FILES: tuple[str, ...] = (
    "dealix/trust/policy.py",
    "dealix/trust/approval.py",
    "dealix/trust/pii_detector.py",
    "dealix/trust/forbidden_claims.py",
    "dealix/trust/approval_matrix.py",
)


def _check(rel: str) -> tuple[bool, str | None]:
    path = REPO / rel
    if not path.is_file():
        return False, f"missing file: {rel}"
    try:
        py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, f"compile error: {exc.msg.strip()}"
    except OSError as exc:
        return False, f"io error: {exc}"
    return True, None


def main() -> int:
    print("== Dealix Governance OS Files ==")
    all_ok = True

    for rel in GOVERNANCE_FILES:
        ok, err = _check(rel)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {rel}")
        if not ok:
            print(f"       {err}")
            all_ok = False

    print("--")
    print(f"GOVERNANCE_PASS={'true' if all_ok else 'false'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
