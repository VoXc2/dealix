"""Decision rights — owner seat and gate per decision type (reference table)."""

from __future__ import annotations

from typing import Final, NamedTuple


class DecisionRightRow(NamedTuple):
    """One row of the Dealix decision-rights matrix."""

    decision_type: str
    owner_seat: str
    gate: str


DECISION_RIGHTS_ROWS: Final[tuple[DecisionRightRow, ...]] = (
    DecisionRightRow("sell_service", "CEO/Growth", "Service Readiness"),
    DecisionRightRow("accept_project", "CEO/Delivery", "Project Acceptance"),
    DecisionRightRow("use_client_data", "Governance", "Data Gate"),
    DecisionRightRow("deliver_output", "QA/Governance", "QA + Governance"),
    DecisionRightRow("build_feature", "Product", "Productization Gate"),
    DecisionRightRow("offer_retainer", "CEO/CS", "Proof + Client Health"),
    DecisionRightRow("create_business_unit", "CEO/Strategy", "Unit Maturity"),
    DecisionRightRow("spin_venture", "Group Strategy", "Venture Gate"),
    DecisionRightRow("publish_claim", "Trust/Marketing", "Proof Gate"),
)


def decision_right_for_key(decision_type: str) -> DecisionRightRow | None:
    dt = decision_type.strip().lower().replace(" ", "_")
    for row in DECISION_RIGHTS_ROWS:
        if row.decision_type == dt:
            return row
    return None
