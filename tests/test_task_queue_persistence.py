"""Task queue — snapshot persistence, resumability, idempotency (Layer 9)."""

from __future__ import annotations

from auto_client_acquisition.orchestrator.queue import TaskQueue, TaskStatus


def _enqueue(q: TaskQueue, **kw):
    return q.enqueue(
        customer_id=kw.get("customer_id", "acme"),
        agent_id=kw.get("agent_id", "intake"),
        action_type=kw.get("action_type", "score_lead"),
        payload=kw.get("payload", {}),
        idempotency_key=kw.get("idempotency_key"),
    )


def test_in_memory_default_writes_no_file(tmp_path):
    q = TaskQueue()
    _enqueue(q)
    assert q.path is None
    assert not list(tmp_path.iterdir())


def test_snapshot_roundtrip_resumes_state(tmp_path):
    path = tmp_path / "task-queue.json"
    q1 = TaskQueue(path=path)
    t1 = _enqueue(q1)
    t2 = _enqueue(q1)
    q1.mark_executing(t1.task_id)
    q1.succeed(t2.task_id, result={"ok": True})

    # A fresh queue at the same path restores every task + its status.
    q2 = TaskQueue(path=path)
    assert set(q2.tasks) == {t1.task_id, t2.task_id}
    assert q2.tasks[t1.task_id].status == TaskStatus.EXECUTING
    assert q2.tasks[t2.task_id].status == TaskStatus.SUCCEEDED
    assert q2.tasks[t2.task_id].result == {"ok": True}


def test_resumable_lists_non_terminal_tasks(tmp_path):
    q = TaskQueue(path=tmp_path / "q.json")
    pending = _enqueue(q)
    done = _enqueue(q)
    q.succeed(done.task_id, result={})
    resumable_ids = {t.task_id for t in q.resumable()}
    assert resumable_ids == {pending.task_id}


def test_idempotency_key_dedupes(tmp_path):
    q = TaskQueue(path=tmp_path / "q.json")
    first = _enqueue(q, idempotency_key="lead-42")
    second = _enqueue(q, idempotency_key="lead-42")
    assert first.task_id == second.task_id
    assert len(q.tasks) == 1


def test_distinct_idempotency_keys_create_distinct_tasks(tmp_path):
    q = TaskQueue(path=tmp_path / "q.json")
    a = _enqueue(q, idempotency_key="lead-1")
    b = _enqueue(q, idempotency_key="lead-2")
    assert a.task_id != b.task_id
    assert len(q.tasks) == 2
