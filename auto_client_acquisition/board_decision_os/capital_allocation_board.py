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
