from __future__ import annotations

from dealix.commercial_ops.founder_agent_tasks import load_task_queue_config, templates_as_packets

EXPECTED = {"dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"}

def test_daily_missions_use_exactly_five_persistent_agents() -> None:
    cfg = load_task_queue_config()
    tasks = [t for t in cfg.get("tasks", []) if t.get("cadence") == "daily"]
    assert {t.get("agent") for t in tasks} == EXPECTED
    assert len(tasks) == 5

def test_daily_missions_cover_all_44_arms_exactly_once() -> None:
    cfg = load_task_queue_config()
    arms = [arm for t in cfg.get("tasks", []) for arm in t.get("arm_ids", [])]
    expected = {f"ARM-{i:03d}" for i in range(1, 45)}
    assert set(arms) == expected
    assert len(arms) == len(set(arms)) == 44

def test_packets_carry_execution_contract() -> None:
    packets = templates_as_packets()
    assert len(packets) == 5
    for packet in packets.values():
        assert packet["agent"] in EXPECTED
        assert packet["arm_ids"]
        assert packet["inputs"]
        assert packet["outputs"]
        assert packet["success_metrics"]
        assert packet["guardrails"]
        assert packet["verify_commands"]
