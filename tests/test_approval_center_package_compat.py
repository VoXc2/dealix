from __future__ import annotations

from auto_client_acquisition.approval_center import (
    approve,
    create_approval,
    edit,
    get_default_approval_store,
    list_history,
    list_pending,
    reject,
    reset_default_approval_store_for_tests,
)
from auto_client_acquisition.approval_center.schemas import ApprovalRequest


def _request(suffix: str) -> ApprovalRequest:
    return ApprovalRequest(
        approval_id=f"apr_{suffix}",
        object_type="lead",
        object_id=f"lead_{suffix}",
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        summary_en=f"request {suffix}",
        proof_impact=f"leadops:{suffix}",
    )


def test_historical_package_helpers_remain_callable() -> None:
    assert callable(create_approval)
    assert callable(approve)
    assert callable(reject)
    assert callable(edit)
    assert callable(list_pending)
    assert callable(list_history)


def test_package_create_approval_routes_to_configured_default_store(monkeypatch) -> None:
    for key in (
        "DEALIX_APPROVAL_STORE_BACKEND",
        "DEALIX_APPROVAL_DATABASE_URL",
        "DEALIX_APPROVAL_ALLOW_SQLITE_TEST_BACKEND",
        "DATABASE_URL",
        "APP_ENV",
    ):
        monkeypatch.delenv(key, raising=False)

    reset_default_approval_store_for_tests()
    try:
        created = create_approval(_request("compat"))
        store = get_default_approval_store()
        persisted = store.get(created.approval_id)
        assert persisted is not None
        assert persisted.approval_id == "apr_compat"
        assert [item.approval_id for item in list_pending()] == ["apr_compat"]
    finally:
        reset_default_approval_store_for_tests()
