#!/usr/bin/env python3
"""Verify repo-level project closure artifacts exist (templates + Definition of Done)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "docs/company/DEFINITION_OF_DONE.md",
    "projects/_TEMPLATE/POST_PROJECT_REVIEW.md",
    "clients/_TEMPLATE/delivery_approval.md",
    "clients/_TEMPLATE/06_proof_pack.md",
    "clients/_TEMPLATE/07_next_steps.md",
    "clients/_PROJECT_WORKBENCH/README.md",
    "clients/_PROJECT_WORKBENCH/04_governance_log.md",
    "clients/_PROJECT_WORKBENCH/06_qa_review.md",
    "clients/_PROJECT_WORKBENCH/07_proof_pack.md",
)


def main() -> int:
    missing = [p for p in REQUIRED_PATHS if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_project_done:{m}", file=sys.stderr)
    ok = not missing
    print(f"PROJECT_DONE_TEMPLATES_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
