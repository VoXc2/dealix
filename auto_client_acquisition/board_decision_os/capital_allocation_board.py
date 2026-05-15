"""Capital allocation board buckets — monthly must/should/hold/kill lists."""

from __future__ import annotations

CAPITAL_BOARD_BUCKETS: tuple[str, ...] = ("must_fund", "should_test", "hold", "kill")

_MUST_FUND: frozenset[str] = frozenset(
    {
        "proof_pack_generator",
        "source_passport",
        "governance_runtime",
        "revenue_intelligence_sprint",
        "board_memo_generator",
    },
)
_SHOULD_TEST: frozenset[str] = frozenset(
    {
        "client_workspace_mvp",
        "approval_center",
        "monthly_value_report",
        "partner_referral_program",
    },
)
_HOLD: frozenset[str] = frozenset(
    {
        "academy_portal",
        "marketplace",
        "white_label",
        "complex_rbac",
    },
)
_KILL: frozenset[str] = frozenset(
    {
        "scraping_engine",
        "cold_whatsapp_automation",
        "guaranteed_sales_claims",
        "sourceless_chatbot",
    },
)


def capital_board_bucket(investment_slug: str) -> str | None:
    s = investment_slug.strip().lower().replace(" ", "_").replace("-", "_")
    if s in _MUST_FUND:
        return "must_fund"
    if s in _SHOULD_TEST:
        return "should_test"
    if s in _HOLD:
        return "hold"
    if s in _KILL:
        return "kill"
    return None


_DEFAULT_CATALOG: dict[str, list[str]] = {
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


def classify_initiative(name: str) -> str | None:
    """Return bucket if name matches catalog (case-insensitive contains)."""
    n = name.strip().lower()
    for bucket, items in _DEFAULT_CATALOG.items():
        for item in items:
            if item.lower() in n or n in item.lower():
                return bucket
    return None
