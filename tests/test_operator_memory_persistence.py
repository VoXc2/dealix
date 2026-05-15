"""Personal Operator memory — JSONL persistence + tenant scoping (Layer 7)."""

from __future__ import annotations

from auto_client_acquisition.personal_operator.memory import (
    MemoryType,
    PersonalOperatorMemory,
    add_memory,
    list_memories,
)


def test_in_memory_default_does_not_persist(tmp_path):
    store = PersonalOperatorMemory()
    add_memory(store, memory_type=MemoryType.GOAL, title="g", body="launch")
    assert len(store.items) == 1
    assert store.path is None


def test_persistence_roundtrip(tmp_path):
    path = tmp_path / "operator-memory.jsonl"
    first = PersonalOperatorMemory(path=path)
    add_memory(first, memory_type=MemoryType.GOAL, title="goal one", body="ship Dealix")
    add_memory(first, memory_type=MemoryType.DECISION, title="decision", body="pgvector")

    # A fresh store at the same path must reload the persisted items.
    reloaded = PersonalOperatorMemory(path=path)
    assert len(reloaded.items) == 2
    titles = {i.title for i in reloaded.items}
    assert titles == {"goal one", "decision"}


def test_tenant_scoped_load(tmp_path):
    path = tmp_path / "operator-memory.jsonl"
    store = PersonalOperatorMemory(path=path)
    add_memory(store, memory_type=MemoryType.GOAL, title="a", body="x", tenant_id="t_a")
    add_memory(store, memory_type=MemoryType.GOAL, title="b", body="y", tenant_id="t_b")

    only_a = PersonalOperatorMemory(path=path, tenant_id="t_a")
    assert len(only_a.items) == 1
    assert only_a.items[0].tenant_id == "t_a"


def test_list_memories_tenant_filter(tmp_path):
    store = PersonalOperatorMemory(path=tmp_path / "m.jsonl")
    add_memory(store, memory_type=MemoryType.GOAL, title="a", body="x", tenant_id="t1")
    add_memory(store, memory_type=MemoryType.GOAL, title="b", body="y", tenant_id="t2")
    assert len(list_memories(store, tenant_id="t1")) == 1
