"""Public Dealix Promise endpoint.

A single read-only endpoint that prospects, partners, regulators, and
auditors can hit to verify Dealix's operating commitments. Each
commitment is parsed from `open-doctrine/11_NON_NEGOTIABLES.md` and
linked to a locking test file in `tests/`.

  GET /api/v1/dealix-promise
      Returns the eleven commitments + the test file that locks each.

The endpoint is public (no auth). It does not return PII, customer data,
pricing, or partner-pipeline information. Its purpose is the eleventh
non-negotiable: **verifiable, not merely trusted**.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["doctrine"])

REPO_ROOT = Path(__file__).resolve().parents[2]
NON_NEGOTIABLES_PATH = REPO_ROOT / "open-doctrine" / "11_NON_NEGOTIABLES.md"


COMMITMENT_TO_TEST: dict[int, str] = {
    1: "tests/test_no_source_passport_no_ai.py",
    2: "tests/test_pii_external_requires_approval.py",
    3: "tests/test_output_requires_governance_status.py",
    4: "tests/test_proof_pack_required.py",
    5: "tests/test_no_scraping_engine.py",
    6: "tests/test_no_cold_whatsapp.py",
    7: "tests/test_no_linkedin_automation.py",
    8: "tests/test_no_guaranteed_claims.py",
    9: "tests/test_agent_requires_identity_card.py",
    10: "tests/test_capital_asset_index_valid.py",
    11: "scripts/verify_all_dealix.py",
}


_HEADING_RE = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s+(.*)$")


@lru_cache(maxsize=1)
def _parse_commitments() -> list[dict[str, Any]]:
    """Parse the eleven commitments from the public doctrine source."""
    if not NON_NEGOTIABLES_PATH.exists():
        return []
    text = NON_NEGOTIABLES_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[dict[str, Any]] = []
    buf: list[str] | None = None
    current: dict[str, Any] | None = None
    for line in lines:
        m = _HEADING_RE.match(line.strip())
        if m:
            if current is not None and buf is not None:
                current["description"] = " ".join(buf).strip()
                out.append(current)
            num = int(m.group(1))
            current = {
                "number": num,
                "title": m.group(2).rstrip("."),
                "description": m.group(3).strip(),
                "verified_by": COMMITMENT_TO_TEST.get(num, ""),
            }
            buf = []
        elif current is not None and buf is not None:
            stripped = line.strip()
            if stripped:
                buf.append(stripped)
            else:
                if buf:
                    current["description"] = (
                        (current["description"] + " " + " ".join(buf)).strip()
                    )
                    out.append(current)
                    current = None
                    buf = None
    if current is not None and buf is not None:
        current["description"] = (current["description"] + " " + " ".join(buf)).strip()
        out.append(current)
    return out


@router.get("/dealix-promise")
async def dealix_promise() -> dict[str, Any]:
    """Public read-only view of the eleven Dealix non-negotiables."""
    commitments = _parse_commitments()
    return {
        "name": "Dealix Promise",
        "source": "open-doctrine/11_NON_NEGOTIABLES.md",
        "commitments": commitments,
        "count": len(commitments),
        "verification": {
            "rule": "Every commitment is locked by at least one test or "
                    "verifier check. Score 5 (market motion) requires real "
                    "operator action — file presence alone is not enough.",
            "master_verifier": "scripts/verify_all_dealix.py",
            "machine_readable_state": "/landing/assets/data/verifier-report.json",
        },
    }
