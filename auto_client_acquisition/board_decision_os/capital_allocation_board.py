"""Capital allocation defaults — policy catalog (v1)."""

from __future__ import annotations

from typing import Literal

Bucket = Literal["must_fund", "should_test", "hold", "kill"]

_DEFAULT_CATALOG: dict[Bucket, list[str]] = {
    "must_fund": [
        "Proof Pack Generator",
        "Source Passport",
        "Governance Runtime",
        "Revenue Intelligence Sprint",
        "Board Memo Generator",
    ],
    "should_test": [
        "Client Workspace MVP",
        "Approval Center",
        "Monthly Value Report",
        "Partner Referral Program",
    ],
    "hold": [
        "Academy Portal",
        "Marketplace",
        "White-label",
        "Complex RBAC",
    ],
    "kill": [
        "Scraping engine",
        "Cold WhatsApp automation",
        "Guaranteed sales claims",
        "Source-less chatbot",
    ],
}


def default_capital_allocation() -> dict[str, list[str]]:
    return {k: list(v) for k, v in _DEFAULT_CATALOG.items()}


def classify_initiative(name: str) -> Bucket | None:
    """Return bucket if name matches catalog (case-insensitive contains)."""
    n = name.strip().lower()
    for bucket, items in _DEFAULT_CATALOG.items():
        for item in items:
            if item.lower() in n or n in item.lower():
                return bucket
    return None
