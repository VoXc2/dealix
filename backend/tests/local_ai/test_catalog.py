"""Unit tests for the local AI catalog."""
from __future__ import annotations

import os
from unittest import mock

import pytest

from app.services.local_ai.catalog import (
    MODEL_CATALOG,
    ServerCapacity,
    ServerTier,
    TaskKind,
    detect_server_tier,
    pick_model_for_task,
    recommended_install_plan,
    select_models_for_tier,
)


def test_catalog_is_nonempty_and_covers_all_task_kinds():
    assert len(MODEL_CATALOG) >= 5
    covered = {t for m in MODEL_CATALOG for t in m.tasks}
    for required in (TaskKind.ROUTER, TaskKind.GENERAL, TaskKind.CODER,
                     TaskKind.MULTILINGUAL, TaskKind.REASONER):
        assert required in covered


def test_nano_tier_only_sees_nano_models():
    eligible = select_models_for_tier(ServerTier.NANO)
    assert eligible, "nano tier should still have at least one model"
    assert all(m.tier == ServerTier.NANO for m in eligible)


def test_balanced_tier_includes_small_and_nano():
    eligible = {m.ollama_tag for m in select_models_for_tier(ServerTier.BALANCED)}
    assert "qwen2.5:0.5b" in eligible            # nano included
    assert "qwen2.5:3b-instruct" in eligible      # small included
    assert "qwen2.5:7b-instruct" in eligible      # balanced included
    # performance-only model should NOT appear
    assert "qwen2.5:14b-instruct" not in eligible


def test_pick_model_for_task_prefers_arabic_when_requested():
    ar = pick_model_for_task(TaskKind.MULTILINGUAL, ServerTier.BALANCED, prefer_arabic=True)
    en = pick_model_for_task(TaskKind.GENERAL, ServerTier.BALANCED, prefer_arabic=False)
    assert ar is not None
    assert en is not None
    # Qwen should win when Arabic quality is the primary criterion at balanced tier.
    assert ar.family == "qwen2.5"


def test_pick_model_falls_back_to_general_when_task_unsupported():
    # There is no "reasoner" in nano tier → should fall back to general (llama3.2:1b)
    picked = pick_model_for_task(TaskKind.REASONER, ServerTier.NANO)
    assert picked is not None
    assert TaskKind.GENERAL in picked.tasks


def test_recommended_install_plan_respects_disk_budget():
    capacity = ServerCapacity(
        total_ram_gb=16.0, available_ram_gb=10.0, free_disk_gb=6.0,
        has_gpu=False, tier=ServerTier.BALANCED,
    )
    plan = recommended_install_plan(capacity)
    used = sum(m.approx_size_gb for m in plan)
    assert used <= capacity.free_disk_gb * 0.70 + 1e-6
    # Plan should always contain a router-capable model (nano tier entry).
    from app.services.local_ai.catalog import TaskKind
    assert any(TaskKind.ROUTER in m.tasks for m in plan)


def test_recommended_install_plan_tight_disk_keeps_router_only():
    capacity = ServerCapacity(
        total_ram_gb=8.0, available_ram_gb=3.0, free_disk_gb=1.0,
        has_gpu=False, tier=ServerTier.SMALL,
    )
    plan = recommended_install_plan(capacity)
    # Only the 0.5 GB router should fit into 0.7 GB budget.
    assert all(m.approx_size_gb <= 0.7 for m in plan)


def test_detect_server_tier_respects_force_env():
    with mock.patch.dict(os.environ, {"LOCAL_LLM_FORCE_TIER": "performance"}):
        cap = detect_server_tier()
    assert cap.tier == ServerTier.PERFORMANCE


@pytest.mark.parametrize("forced,expected", [
    ("nano", ServerTier.NANO),
    ("small", ServerTier.SMALL),
    ("balanced", ServerTier.BALANCED),
])
def test_detect_server_tier_force_options(forced, expected):
    with mock.patch.dict(os.environ, {"LOCAL_LLM_FORCE_TIER": forced}):
        cap = detect_server_tier()
    assert cap.tier == expected
