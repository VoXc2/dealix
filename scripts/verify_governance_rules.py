#!/usr/bin/env python3
"""Verify governance docs exist under docs/governance/."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "COMPLIANCE_PERIMETER.md",
    "PDPL_DATA_RULES.md",
    "APPROVAL_MATRIX.md",
    "DATA_RETENTION.md",
    "PII_REDACTION_POLICY.md",
    "AUDIT_LOG_POLICY.md",
    "FORBIDDEN_ACTIONS.md",
    "GOVERNANCE_SERVICE_CHECKS_AR.md",
    "RISK_REGISTER.md",
    "TRUST_SAFETY_CHARTER.md",
    "RUNTIME_GOVERNANCE.md",
    "PERMISSION_MIRRORING.md",
    "AI_ACTION_TAXONOMY.md",
    "INCIDENT_RESPONSE.md",
    "HUMAN_IN_THE_LOOP_MATRIX.md",
    "AI_INFORMATION_GOVERNANCE.md",
    "AUTONOMY_VALIDATION_GATES.md",
    "AGENT_SPRAWL_PREVENTION.md",
    "AI_ACTION_CONTROL.md",
    "REVERSIBILITY_ROLLBACK.md",
    "GOVERNANCE_PRODUCT_LADDER.md",
)


def main() -> int:
    missing = [n for n in REQUIRED if not (REPO / "docs" / "governance" / n).is_file()]
    for m in missing:
        print(f"missing_governance:{m}", file=sys.stderr)
    ok = not missing
    print(f"GOVERNANCE_DOCS_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
