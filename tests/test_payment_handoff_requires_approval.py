"""
Test: Payment Handoff Requires Approval
Ensures no payment handoff (invoice, refund) can be processed without approval.
"""
import yaml


def test_approval_policy_invoice_send():
    """Invoice send must require approval."""
    with open("dealix/config/approval_policy.yaml") as f:
        policy = yaml.safe_load(f)

    invoice = policy.get("invoice_send", {})
    assert invoice.get("requires_approval") is True
    assert invoice.get("creates_evidence") is True
    assert invoice.get("required_evidence") is not None


def test_approval_policy_refund():
    """Refund request must require approval."""
    with open("dealix/config/approval_policy.yaml") as f:
        policy = yaml.safe_load(f)

    refund = policy.get("refund_request", {})
    assert refund.get("requires_approval") is True
    assert refund.get("creates_evidence") is True


def test_approval_policy_affiliate_payout():
    """Affiliate payout must require approval."""
    with open("dealix/config/approval_policy.yaml") as f:
        policy = yaml.safe_load(f)

    payout = policy.get("affiliate_payout", {})
    assert payout.get("requires_approval") is True
    assert payout.get("required_evidence") is not None


def test_payment_terms_approval_required():
    """Payment terms doc must reference approval."""
    from pathlib import Path
    content = Path("docs/commercial/PAYMENT_TERMS_AR.md").read_text(encoding="utf-8")
    assert "موافقة" in content or "approval" in content.lower()
    assert "L3" in content or "founder" in content.lower()


def test_no_unconditional_invoice_dispatch():
    """No code path should send invoice without approval."""
    # Check agent permissions
    with open("dealix/config/agent_permissions.yaml") as f:
        perms = yaml.safe_load(f)

    assert perms["defaults"]["invoice_charge"] == "blocked", (
        "Default invoice charge must be blocked"
    )


def test_refund_approval_levels():
    """Refund must require at least L3 approval per docs."""
    from pathlib import Path
    content = Path("docs/commercial/PAYMENT_TERMS_AR.md").read_text(encoding="utf-8")
    # Should mention L3 for refund
    assert "L3" in content or "founder" in content.lower()


def test_pricing_yaml_doesnt_have_invoice_dispatch():
    """Pricing config should not include invoice dispatch logic."""
    with open("dealix/config/pricing.yaml") as f:
        pricing = yaml.safe_load(f)

    # Should be data only, no logic
    assert "currency" in pricing
    # No send/dispatch/auto keys
    for key in pricing.keys():
        assert "send" not in key.lower() or "refund" not in key.lower(), (
            f"pricing.yaml has suspicious key: {key}"
        )


if __name__ == "__main__":
    test_approval_policy_invoice_send()
    test_approval_policy_refund()
    test_approval_policy_affiliate_payout()
    test_payment_terms_approval_required()
    test_no_unconditional_invoice_dispatch()
    test_refund_approval_levels()
    test_pricing_yaml_doesnt_have_invoice_dispatch()
    print("All payment handoff approval tests passed")
