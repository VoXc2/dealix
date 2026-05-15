#!/usr/bin/env python3
"""Full MVP readiness gate — prints DEALIX_READY and component flags."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import yaml  # noqa: E402

from auto_client_acquisition.delivery_os.service_readiness import (  # noqa: E402
    compute_service_readiness_score,
)


def _run(script: str) -> bool:
    code = subprocess.call(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / script)],
        cwd=REPO,
    )
    return code == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-tests", action="store_true")
    args = ap.parse_args()

    service_files = _run("verify_service_files.py")
    service_catalog = _run("verify_service_catalog.py")
    governance = _run("verify_governance_rules.py")
    quality_docs = (REPO / "docs" / "quality" / "QUALITY_STANDARD.md").is_file()
    proof = _run("verify_proof_pack.py")
    ai_q = _run("verify_ai_output_quality.py")

    sales = (
        (REPO / "docs" / "sales" / "SALES_PLAYBOOK.md").is_file()
        and (REPO / "docs" / "sales" / "PROPOSAL_TEMPLATE.md").is_file()
    )

    mp = yaml.safe_load((REPO / "docs" / "company" / "SERVICE_ID_MAP.yaml").read_text(encoding="utf-8")) or {}

    ready = 0
    seen: set[str] = set()
    for row in mp.get("mappings") or []:
        sid = row.get("service_id")
        if not sid or sid in seen:
            continue
        seen.add(sid)
        if compute_service_readiness_score(sid)["score"] >= 80:
            ready += 1

    tests_ok = True
    if not args.skip_tests:
        tests_ok = (
            subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "tests/test_company_os_verify.py",
                    "tests/test_data_os_helpers.py",
                    "tests/test_reporting_os_proof_pack.py",
                    "tests/test_delivery_os_catalog.py",
                    "tests/test_knowledge_os_policy.py",
                    "tests/test_governance_approval_matrix.py",
                    "-q",
                    "--no-cov",
                ],
                cwd=REPO,
            )
            == 0
        )

    print(f"SERVICE_FILES_PASS={'true' if service_files else 'false'}")
    print(f"GOVERNANCE_PASS={'true' if governance else 'false'}")
    print(f"QUALITY_PASS={'true' if quality_docs else 'false'}")
    print(f"PROOF_PACK_PASS={'true' if proof else 'false'}")
    print(f"SALES_ASSETS_PASS={'true' if sales else 'false'}")
    print(f"TESTS_PASS={'true' if tests_ok else 'false'}")
    print(f"READY_SERVICES={ready}/{len(seen)}")

    ready_ok = (
        service_files
        and service_catalog
        and governance
        and quality_docs
        and proof
        and sales
        and ai_q
        and ready >= 3
        and tests_ok
    )
    print(f"DEALIX_READY={'true' if ready_ok else 'false'}")
    return 0 if ready_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
