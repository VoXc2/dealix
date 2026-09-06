from __future__ import annotations

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    create_approval,
    get_default_approval_store,
    reset_default_approval_store_for_tests,
)
from auto_client_acquisition.leadops_spine.draft_builder import build_draft


def setup_function() -> None:
    reset_default_approval_store_for_tests()


def teardown_function() -> None:
    reset_default_approval_store_for_tests()


def test_public_facade_accepts_canonical_model() -> None:
    req = ApprovalRequest(
        object_type="lead",
        object_id="lead_model",
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        summary_en="model request",
        proof_impact="leadops:model",
    )

    created = create_approval(req)

    assert created.approval_id == req.approval_id
    assert get_default_approval_store().get(created.approval_id) is not None


def test_leadops_dict_payload_reaches_approval_store() -> None:
    draft = build_draft(
        leadops_id="lops_facade_contract",
        customer_handle="customer_test",
        sector="technology",
        offer_route={"channel": "email"},
        next_action={"owner": "dealix-sales"},
    )

    assert isinstance(draft["approval_payload"], dict)
    assert draft["action_mode"] == "approval_required"

    created = create_approval(draft["approval_payload"])

    assert created.object_id == draft["draft_id"]
    assert created.proof_impact == "leadops:lops_facade_contract"
    assert created.action_mode == "approval_required"
    assert get_default_approval_store().get(created.approval_id) is not None
