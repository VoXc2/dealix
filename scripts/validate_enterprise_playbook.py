#!/usr/bin/env python3
"""Validate enterprise playbook generator outputs."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.enterprise_playbook import generate_enterprise_playbook_bundle


def main() -> int:
    intake_path = ROOT / "intake/demo_customer_intake.json"
    intake = json.loads(intake_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="enterprise_playbook_validate_") as td:
        bundle = generate_enterprise_playbook_bundle(
            service_id="CUSTOMER_PORTAL_GOLD",
            intake=intake,
            profile="hybrid_governed_execution",
            output_dir=Path(td),
        )
        for name, path in {
            "proposal": bundle.proposal,
            "sow": bundle.sow,
            "kpi_contract": bundle.kpi_contract,
            "governance_contract": bundle.governance_contract,
        }.items():
            if not path.exists():
                errors.append(f"missing output: {name}")
            elif not path.read_text(encoding="utf-8").strip():
                errors.append(f"empty output: {name}")

    if errors:
        print("ENTERPRISE_PLAYBOOK_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("ENTERPRISE_PLAYBOOK_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
