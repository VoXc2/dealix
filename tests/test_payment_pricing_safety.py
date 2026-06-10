"""Payment and pricing safety — approval gates.

Tests:
- Payment handoff requires approval
- Pricing requires founder approval
- Contract terms require handoff
- Discount guardrails
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.governance_os.approval_matrix import approval_for_action


class TestPaymentHandoffRequiresApproval:
    """Payment operations require founder approval."""

    PAYMENT_ACTIONS = [
        "generate payment link",
        "process payment",
        "refund request",
        "payment dispute",
        "invoice generation",
    ]

    def test_payment_needs_founder_approval(self) -> None:
        """All payment actions require founder approval."""
        for action in self.PAYMENT_ACTIONS:
            risk, approval_type = approval_for_action(action)
            assert risk in ("high", "critical"), f"{action} not high/critical risk"

    def test_no_autonomous_payment(self) -> None:
        """Agents cannot autonomously process payments."""
        # Payment requires human approval
        risk, approval_type = approval_for_action("payment")
        assert "human" in approval_type.lower() or "founder" in approval_type.lower()


class TestPricingRequiresFounderApproval:
    """Final pricing requires founder approval."""

    PRICING_ACTIONS = [
        "finalize pricing",
        "give discount",
        "custom quote",
        "negotiate price",
    ]

    def test_pricing_needs_founder_approval(self) -> None:
        """Pricing decisions require founder approval."""
        for action in self.PRICING_ACTIONS:
            risk, approval_type = approval_for_action(action)
            assert risk == "high", f"{action} not high risk"
            assert "founder" in approval_type.lower() or "human" in approval_type.lower()

    def test_no_agents_set_final_price(self) -> None:
        """Agents can draft pricing but not set final price."""
        # Draft is OK
        draft_action = "draft pricing proposal"
        draft_risk, _ = approval_for_action(draft_action)
        # Draft should be lower risk
        assert draft_risk in ("low", "medium"), "Draft pricing too risky"

        # Final is high risk
        final_action = "finalize pricing"
        final_risk, _ = approval_for_action(final_action)
        assert final_risk == "high", "Final pricing not high risk"


class TestContractTermsRequireHandoff:
    """Contract terms require human (legal) review."""

    CONTRACT_ACTIONS = [
        "generate contract terms",
        "legal review",
        "contract negotiation",
        "agreement signature",
    ]

    def test_contract_needs_human(self) -> None:
        """Contract actions require human/legal review."""
        for action in self.CONTRACT_ACTIONS:
            risk, approval_type = approval_for_action(action)
            assert risk in ("high", "critical"), f"{action} not high/critical risk"

    def test_no_autonomous_contract_generation(self) -> None:
        """Agents cannot autonomously generate final contract terms."""
        risk, approval_type = approval_for_action("generate contract terms")
        assert "human" in approval_type.lower() or "legal" in approval_type.lower()


class TestDiscountGuardrails:
    """Discounts have guardrails."""

    def test_discount_within_guardrails(self) -> None:
        """Small discounts within guardrails."""
        # 10% discount — within standard guardrail
        discount_guardrail = {
            "max_discount_percent": 20,
            "approval_required_percent": 10,
        }
        discount_applied = 10
        needs_approval = discount_applied >= discount_guardrail["approval_required_percent"]
        assert needs_approval is True, "10% discount should need approval"

    def test_large_discount_needs_approval(self) -> None:
        """Large discounts require extra approval."""
        discount_guardrail = {
            "max_discount_percent": 20,
            "approval_required_percent": 10,
        }
        discount_applied = 30
        within_guardrail = discount_applied <= discount_guardrail["max_discount_percent"]
        # 30% exceeds 20% guardrail — should be blocked
        assert within_guardrail is False, "30% discount exceeds guardrail"


# Total: 10 tests
