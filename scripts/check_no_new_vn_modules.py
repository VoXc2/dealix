#!/usr/bin/env python3
"""Version-sprawl guard — freeze creation of new ``*_vN`` modules.

The repo accumulated versioned-duplicate module families (company_brain_v6,
observability_v10, llm_gateway_v10, ...). Each new ``_vN`` fork dilutes the
canonical surface and confuses delivery. This guard fails CI if a NEW
versioned module directory appears under ``auto_client_acquisition/``.

To intentionally add one (rare): update ``_FROZEN_VN_MODULES`` in the same
PR, with a note in docs/company/DEPRECATED_MODULES.md explaining why a new
version is justified over extending the canonical module.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_ACQ = Path(__file__).resolve().parents[1] / "auto_client_acquisition"

# The versioned modules that existed when the guard was introduced.
_FROZEN_VN_MODULES: frozenset[str] = frozenset(
    {
        "ai_workforce_v10",
        "company_brain_v6",
        "compliance_os_v12",
        "crm_v10",
        "customer_inbox_v10",
        "executive_pack_v2",
        "founder_v10",
        "growth_v10",
        "knowledge_v10",
        "llm_gateway_v10",
        "observability_v10",
        "observability_v6",
        "platform_v10",
        "safety_v10",
        "service_mapping_v7",
        "workflow_os_v10",
    }
)

_VN_PATTERN = re.compile(r"_v\d+$")


def main() -> int:
    current = {
        p.name
        for p in _ACQ.iterdir()
        if p.is_dir() and _VN_PATTERN.search(p.name)
    }
    new = sorted(current - _FROZEN_VN_MODULES)
    if new:
        print("VN_MODULE_GUARD=FAIL")
        for name in new:
            print(f"  new versioned module not allowed: auto_client_acquisition/{name}")
        print(
            "Extend the canonical module instead of forking a new version, "
            "or update _FROZEN_VN_MODULES with justification."
        )
        return 1
    print(f"VN_MODULE_GUARD=OK ({len(current)} frozen versioned modules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
