#!/usr/bin/env python3
"""Orchestrator — runs all 5 Dealix readiness verifiers and prints a scorecard.

سكربت التحقق الشامل — يشغّل كل فحوصات الجاهزية ويعرض البطاقة النهائية.

Usage:
    python scripts/verify_full_mvp_ready.py

Imports and runs each individual verifier in turn:
- verify_company_ready
- verify_service_files
- verify_service_catalog
- verify_governance_rules
- verify_proof_pack

Each verifier is treated as a black box: success is its exit-zero contract.
A single final scorecard is emitted. Exit 0 if all PASS, non-zero otherwise.
"""
from __future__ import annotations

import contextlib
import importlib
import io
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO / "scripts"

# Ensure repo root *and* scripts/ are importable.
for p in (REPO, SCRIPTS_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)


VERIFIERS: tuple[tuple[str, str], ...] = (
    ("verify_company_ready", "COMPANY_READY_PASS"),
    ("verify_service_files", "SERVICE_FILES_PASS"),
    ("verify_service_catalog", "SERVICE_CATALOG_PASS"),
    ("verify_governance_rules", "GOVERNANCE_PASS"),
    ("verify_proof_pack", "PROOF_PACK_PASS"),
)


def _run(module_name: str) -> tuple[int, str]:
    """Import and invoke <module>.main(); return (exit_code, captured_output)."""
    buf = io.StringIO()
    try:
        module = importlib.import_module(module_name)
        if not hasattr(module, "main"):
            return 2, f"[FAIL] {module_name}: no main() entrypoint\n"
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = module.main()
    except Exception as exc:  # noqa: BLE001 — orchestrator must keep running
        return 3, buf.getvalue() + f"[FAIL] {module_name}: exception: {exc!r}\n"
    return int(code or 0), buf.getvalue()


def main() -> int:
    print("== Dealix Full MVP Readiness ==")
    results: dict[str, bool] = {}
    ready_services = 0

    for module_name, scorecard_key in VERIFIERS:
        print()
        print(f"-- running {module_name} --")
        code, output = _run(module_name)
        sys.stdout.write(output)
        passed = code == 0
        results[scorecard_key] = passed
        if passed:
            ready_services += 1
        print(f"-- {module_name}: {'PASS' if passed else 'FAIL'} (exit={code}) --")

    overall = all(results.values())
    print()
    print("== Final Scorecard ==")
    print(f"DEALIX_READY={'true' if overall else 'false'}")
    print(f"READY_SERVICES={ready_services}/{len(VERIFIERS)}")
    for _, key in VERIFIERS:
        print(f"{key}={'true' if results.get(key, False) else 'false'}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
