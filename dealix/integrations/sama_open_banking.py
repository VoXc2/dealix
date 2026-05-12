"""
SAMA Open Banking — Saudi Central Bank's Account Information Services
(AIS) and Payment Initiation Services (PIS).

Currently a documentation-only stub: live AIS/PIS access requires a
SAMA-issued participant licence. This client surfaces the API contract
we'd target once licensed so the rest of the app can plan against it.

Reference: https://www.sama.gov.sa/en-US/RulesInstructions/Pages/OpenBanking.aspx
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from core.logging import get_logger

log = get_logger(__name__)


def is_configured() -> bool:
    return bool(os.getenv("SAMA_OB_CLIENT_ID", "").strip())


@dataclass
class AISResult:
    accounts: list[dict[str, str]]
    licensed: bool


async def list_accounts(*, customer_consent_id: str) -> AISResult:
    """Stub. Returns empty + licensed=False until SAMA licence is issued."""
    if not is_configured():
        return AISResult(accounts=[], licensed=False)
    # Real wiring lands here after licence:
    #   POST {SAMA_OB_HOST}/aisp/accounts with consent_id header.
    log.info("sama_ob_call_skipped_until_licensed")
    return AISResult(accounts=[], licensed=True)
