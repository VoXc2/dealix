"""V12 Phase 2 — unified WorkItem layer tests."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from auto_client_acquisition.full_ops import (
    WorkItem,
    WorkQueue,
    from_agent_task,
    from_approval_request,
    from_journey_state,
    prioritize,
)


def test_work_item_minimum_required_fields() -> None:
    it = WorkItem.make(
        os_type="growth",
        title_ar="فرصة",
        title_en="opportunity",
        source="test",
    )
    assert it.id.startswith("wi_")
    assert it.tenant_id == "dealix"
    assert it.os_type == "growth"
    assert it.priority == "p2"
    assert it.status == "new"
    assert it.action_mode == "draft_only"
    assert it.owner_role == "founder"


def test_work_item_id_is_deterministic() -> None:
    a = WorkItem.make(os_type="sales", title_ar="x", title_en="x", source="s")
    b = WorkItem.make(os_type="sales", title_ar="x", title_en="x", source="s")
    assert a.id == b.id


def test_work_item_no_pii_in_repr() -> None:
    it = WorkItem.make(
        os_type="support",
        title_ar="مشكلة",
        title_en="issue",
        source="test",
        customer_id="cust_redacted_001",
    )
    rendered = it.model_dump_json()
    forbidden = ("+966", "@gmail", "@example.sa", "sk_live_", "ghp_")
    for f in forbidden:
        assert f not in rendered


def test_priority_ordering() -> None:
    items = [
        WorkItem.make(os_type="growth", title_ar="b", title_en="b", source="s", priority="p2"),
        WorkItem.make(os_type="growth", title_ar="a", title_en="a", source="s", priority="p0"),
        WorkItem.make(os_type="growth", title_ar="c", title_en="c", source="s", priority="p3"),
        WorkItem.make(os_type="growth", title_ar="d", title_en="d", source="s", priority="p1"),
    ]
    ranked = prioritize(items)
    assert [i.priority for i in ranked] == ["p0", "p1", "p2", "p3"]


def test_priority_risk_flags_then_age_breaks_ties() -> None:
    older = datetime.now(UTC) - timedelta(hours=2)
    newer = datetime.now(UTC)
    a = WorkItem.make(os_type="growth", title_ar="a", title_en="a", source="x")
    a = a.model_copy(update={"created_at": newer})
    b = WorkItem.make(os_type="growth", title_ar="b", title_en="b", source="y", risk_flags=["urgent"])
    b = b.model_copy(update={"created_at": older})
    ranked = prioritize([a, b])
    # b has risk_flags AND is older — must come first
    assert ranked[0].id == b.id


def test_work_queue_partitions_by_tenant() -> None:
    q = WorkQueue()
    a = WorkItem.make(os_type="growth", title_ar="a", title_en="a", source="x")
    b = WorkItem.make(os_type="growth", title_ar="b", title_en="b", source="y")
    b = b.model_copy(update={"tenant_id": "other"})
    q.add(a)
    q.add(b)
    assert len(q.list_all(tenant_id="dealix")) == 1
    assert len(q.list_all(tenant_id="other")) == 1


def test_work_queue_list_by_os_and_status() -> None:
    q = WorkQueue()
    g = WorkItem.make(os_type="growth", title_ar="g", title_en="g", source="x")
    s = WorkItem.make(os_type="support", title_ar="s", title_en="s", source="y", status="escalated")
    q.add(g)
    q.add(s)
    assert len(q.list_by_os("growth")) == 1
    assert q.list_by_os("growth")[0].id == g.id
    assert len(q.list_by_status("escalated")) == 1


def test_adapter_from_agent_task_dict() -> None:
    task = {"action_type": "draft_email", "status": "pending", "customer_id": "cust_a"}
    wi = from_agent_task(task, os_type="sales")
    assert wi.os_type == "sales"
    assert wi.status == "new"
    assert wi.action_mode == "approval_required"
    assert wi.customer_id == "cust_a"
    assert "draft_email" in wi.title_en


def test_adapter_from_approval_request_dict() -> None:
    req = {
        "approval_id": "appr_1",
        "object_type": "outreach_draft",
        "object_id": "draft_1",
        "action_mode": "draft_only",
        "status": "pending",
    }
    wi = from_approval_request(req)
    assert wi.os_type == "compliance"
    assert wi.status == "needs_approval"
    assert wi.action_mode == "draft_only"
    assert "outreach_draft" in wi.title_en


def test_adapter_from_journey_state_routes_to_correct_os() -> None:
    state_in_delivery = {"current_stage": "in_delivery", "customer_id": "c1"}
    wi = from_journey_state(state_in_delivery)
    assert wi.os_type == "delivery"
    assert wi.status == "in_progress"

    state_blocked = {"current_stage": "blocked", "customer_id": "c2"}
    wi2 = from_journey_state(state_blocked)
    assert wi2.os_type == "compliance"
    assert wi2.status == "blocked"
