"""Contracts for the Hermes arm portfolio controller (planning only).

Covers the non-negotiables: canonical 44-arm registry + playbooks, Omega V3
Agentic Holding as logical-agent authority, the historical five owner aliases only
as compatibility executors, ACTIVE_DEEP ARM-001/002/003 preserved as the initial
portfolio Top-3 unless real customer/economic evidence exists, research-only ranking stays LIGHT/HOLD,
no invented revenue/pipeline, and L5 material effects stay WAITING_L5.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ctrl = _load("hermes_arm_portfolio_controller")


def _arm(plan: dict, arm_id: str) -> dict:
    return next(record for record in plan["records"] if record["arm_id"] == arm_id)


def test_canonical_contract_passes() -> None:
    assert ctrl.contract_failures(ctrl.load_registry(), ctrl.load_playbooks()) == []


def test_contract_fails_closed_on_missing_arm() -> None:
    registry = ctrl.load_registry()
    registry["arms"] = registry["arms"][:-1]
    assert "ARMS_44" in ctrl.contract_failures(registry, ctrl.load_playbooks())


def test_no_evidence_preserves_deep_wedges_and_top3() -> None:
    plan = ctrl.plan_portfolio(generated_at="fixed")
    assert plan["overall"] == "PLAN_READY"
    assert len(plan["records"]) == 44
    # Compatibility fields remain readable, but canonical architecture lives in
    # agent_authority and runtime capacity is not inferred from either value.
    assert plan["deep_wip_max"] == 3
    assert len(plan["permanent_agents"]) == 5
    authority = plan["agent_authority"]
    assert authority["canonical_architecture"] == "agentic_holding_sector_company_mesh"
    assert authority["logical_agents"] > len(plan["permanent_agents"])
    assert authority["sector_companies"] >= 20
    assert authority["legacy_executor_aliases"] == plan["permanent_agents"]
    assert authority["portfolio_deep_wip_max"] == 3
    assert authority["runtime_capacity_authority"].startswith("ResourceGovernor")
    assert authority["fixed_five_runtime_authority"] is False
    assert authority["fixed_three_runtime_worker_ceiling"] is False
    assert plan["deep_wedge_ids"] == ["ARM-001", "ARM-002", "ARM-003"]
    assert plan["preserved_deep_ids"] == ["ARM-001", "ARM-002", "ARM-003"]
    assert plan["promoted_by_evidence_ids"] == []
    assert plan["counts"] == {"DEEP": 3, "LIGHT": 25, "HOLD": 16}
    assert [entry["arm_id"] for entry in plan["top3"]] == ["ARM-001", "ARM-002", "ARM-003"]


def test_every_record_emits_required_transparent_outputs() -> None:
    factory = ctrl.session_factory()
    valid_model_classes = set(factory.CLASS_TO_MODEL_CLASS.values())
    plan = ctrl.plan_portfolio(generated_at="fixed")
    for record in plan["records"]:
        assert record["score"]["semantics"] == ctrl.SCORE_SEMANTICS
        assert set(record["score"]["factors"]) == set(ctrl.FACTOR_WEIGHTS)
        assert record["next_safe_action"]
        assert isinstance(record["evidence_refs"], list)
        assert record["model_job_class"]["job_class"] in factory.JOB_CLASSES
        assert record["model_job_class"]["model_class"] in valid_model_classes
        assert record["cost"]["cash_class"] == "NONE"
        assert record["risk"]["class"] in {"LOW", "MEDIUM", "HIGH"}
        assert "reported" in record["founder_minutes"]
        assert "satisfied" in record["proof_gap"]
        assert record["classification"] in {ctrl.CLASS_DEEP, ctrl.CLASS_LIGHT, ctrl.CLASS_HOLD}


def test_research_only_never_promotes_to_deep() -> None:
    evidence = ctrl.normalize_evidence(
        {"arms": {"ARM-004": {"research_evidence_refs": ["evidence://r/1"]}}}
    )
    plan = ctrl.plan_portfolio(evidence=evidence, generated_at="fixed")
    record = _arm(plan, "ARM-004")
    assert record["classification"] in {ctrl.CLASS_LIGHT, ctrl.CLASS_HOLD}
    assert "ARM-004" not in plan["deep_wedge_ids"]


def test_stop_loss_demotes_and_evidence_promotes_within_limit() -> None:
    evidence = ctrl.normalize_evidence(
        {
            "arms": {
                "ARM-001": {"stop_loss_evidence_refs": ["evidence://stop/1"]},
                "ARM-004": {"customer_evidence_refs": ["evidence://c/1"]},
            }
        }
    )
    plan = ctrl.plan_portfolio(evidence=evidence, generated_at="fixed")
    assert "ARM-001" not in plan["deep_wedge_ids"]
    assert "ARM-004" in plan["deep_wedge_ids"]
    assert len(plan["deep_wedge_ids"]) <= plan["deep_wip_max"]
    assert plan["counts"]["DEEP"] == 3
    assert _arm(plan, "ARM-001")["classification"] == ctrl.CLASS_HOLD


def test_blocked_and_regulated_arms_are_risk_flagged() -> None:
    plan = ctrl.plan_portfolio(generated_at="fixed")
    assert _arm(plan, "ARM-042")["classification"] == ctrl.CLASS_HOLD
    assert _arm(plan, "ARM-042")["risk"]["class"] == "HIGH"
    assert _arm(plan, "ARM-024")["risk"]["class"] == "HIGH"


def test_external_send_is_l5_and_never_auto_executable() -> None:
    evidence = ctrl.normalize_evidence(
        {
            "arms": {
                "ARM-004": {
                    "customer_evidence_refs": ["evidence://c/2"],
                    "requires_external_send": True,
                }
            }
        }
    )
    plan = ctrl.plan_portfolio(evidence=evidence, generated_at="fixed")
    record = _arm(plan, "ARM-004")
    assert record["l5_required"] is True
    assert record["model_job_class"]["authority_level"] == "L5"
    assert record["model_job_class"]["auto_executable"] is False
    assert "WAITING_L5" in record["next_safe_action"]


def test_plan_never_invents_revenue_or_pipeline() -> None:
    plan = ctrl.plan_portfolio(generated_at="fixed")
    assert plan["truth"]["counts_as_revenue"] is False
    assert plan["truth"]["counts_as_pipeline"] is False
    assert plan["truth"]["invented_amounts"] is False
    assert plan["truth"]["external_effect"] == "NONE"
    assert plan["truth"]["l5_policy"] == ctrl.L5_POLICY
    monetary_keys = {"roi", "arr", "mrr", "revenue", "pipeline_value", "expected_revenue", "amount"}
    for record in plan["records"]:
        assert not (monetary_keys & set(record))


def test_plan_is_deterministic() -> None:
    assert ctrl.plan_portfolio(generated_at="fixed") == ctrl.plan_portfolio(generated_at="fixed")


def test_tripwire_blocks_plan(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_EXTERNAL_SEND", "1")
    plan = ctrl.plan_portfolio(generated_at="fixed")
    assert plan["overall"] == "BLOCKED"
    assert "DEALIX_EXTERNAL_SEND" in plan["safety"]["tripwires"]


def test_evidence_normalization_drops_unknown_and_cleans_refs() -> None:
    evidence = ctrl.normalize_evidence(
        {
            "arms": {
                "ARM-999": {"research_evidence_refs": ["evidence://x"]},
                "ARM-004": {"research_evidence_refs": ["evidence://a", "evidence://a", ""]},
            }
        },
        allowed_ids={"ARM-004"},
    )
    assert set(evidence) == {"ARM-004"}
    assert evidence["ARM-004"]["research_evidence_refs"] == ["evidence://a"]
    assert ctrl.evidence_tier(evidence["ARM-004"]) == "RESEARCH"


def test_build_job_uses_permanent_owner_and_marker() -> None:
    plan = ctrl.plan_portfolio(generated_at="fixed")
    job = ctrl.build_job(_arm(plan, "ARM-001"))
    assert job["OWNER_AGENT"] in ctrl.session_factory().PERMANENT_AGENTS
    assert "arm_portfolio:ARM-001" in job["CONTEXT_REFS"]
    assert job["AUTHORITY_LEVEL"] == "L2"
    assert job["MODIFYING"] is False


def test_controller_defines_no_duplicate_scheduler() -> None:
    source = (ROOT / "scripts" / "ops" / "hermes_arm_portfolio_controller.py").read_text(
        encoding="utf-8"
    )
    for token in (
        "while True",
        "schedule.every",
        "crontab",
        "APScheduler",
        "process_queue(",
        "run_job(",
    ):
        assert token not in source


def test_render_summary_is_truthful() -> None:
    summary = ctrl.render_summary(ctrl.plan_portfolio(generated_at="fixed"))
    assert "HERMES_ARM_PORTFOLIO=PLAN_READY" in summary
    assert "L5_POLICY=WAITING_L5_never_auto_executed" in summary
    assert "COUNTS_AS_REVENUE=False" in summary
    assert "PERMANENT_AGENTS=" not in summary
    assert "LEGACY_EXECUTOR_ALIASES=5" in summary
    assert "PORTFOLIO_DEEP_WIP=3" in summary
    assert "HOLDING_LOGICAL_AGENTS=" in summary


def test_legacy_aliases_and_top3_are_not_runtime_capacity_authority() -> None:
    source = (ROOT / "scripts" / "ops" / "hermes_arm_portfolio_controller.py").read_text(encoding="utf-8")
    assert "Exactly five permanent agents" not in source
    assert "runtime capacity belongs to ResourceGovernor / Session Factory" in source
    plan = ctrl.plan_portfolio(generated_at="fixed")
    authority = plan["agent_authority"]
    assert authority["fixed_five_runtime_authority"] is False
    assert authority["fixed_three_runtime_worker_ceiling"] is False


def test_registry_copy_is_not_mutated_by_planning() -> None:
    registry = ctrl.load_registry()
    snapshot = copy.deepcopy(registry)
    ctrl.plan_portfolio(registry=registry, generated_at="fixed")
    assert registry == snapshot


def test_build_job_prompt_and_acceptance_require_receipt_marker() -> None:
    record = _arm(ctrl.plan_portfolio(generated_at="fixed"), "ARM-001")
    job = ctrl.build_job(record)
    marker = "ARM_PORTFOLIO_RECEIPT:ARM-001"
    prompt = job["EXECUTOR"]["prompt"]
    assert marker in prompt
    for field in (
        "FINDINGS",
        "EVIDENCE_REFS_USED",
        "RELATIONSHIP_TRUTH",
        "PIPELINE_TRUTH",
        "REVENUE_TRUTH",
        "NEXT_SAFE_ACTION",
        "L5_REQUIRED",
    ):
        assert field in prompt
    assert "research != relationship" in prompt
    assert "no external effect" in prompt.lower()
    assert "no repository modification" in prompt.lower()
    checks = job["ACCEPTANCE"]["checks"]
    assert [check["kind"] for check in checks] == ["exit_zero", "stdout_contains"]
    assert checks[1]["text"] == marker
    assert marker in job["ACCEPTANCE"]["criteria"]


def test_build_job_prompt_includes_evidence_refs() -> None:
    evidence = ctrl.normalize_evidence(
        {
            "arms": {
                "ARM-004": {
                    "research_evidence_refs": ["evidence://r/1", "evidence://r/2"],
                }
            }
        }
    )
    record = _arm(ctrl.plan_portfolio(evidence=evidence, generated_at="fixed"), "ARM-004")
    prompt = ctrl.build_job(record)["EXECUTOR"]["prompt"]
    assert "evidence://r/1" in prompt
    assert "evidence://r/2" in prompt
    assert "ARM_PORTFOLIO_RECEIPT:ARM-004" in prompt


def test_build_job_prompt_without_refs_is_explicit() -> None:
    record = _arm(ctrl.plan_portfolio(generated_at="fixed"), "ARM-006")
    prompt = ctrl.build_job(record)["EXECUTOR"]["prompt"]
    assert "NONE (no evidence refs supplied)" in prompt


def test_l5_build_job_receipt_declares_l5_required() -> None:
    evidence = ctrl.normalize_evidence(
        {"arms": {"ARM-004": {"customer_evidence_refs": ["evidence://c/1"], "requires_external_send": True}}}
    )
    record = _arm(ctrl.plan_portfolio(evidence=evidence, generated_at="fixed"), "ARM-004")
    job = ctrl.build_job(record)
    assert job["AUTHORITY_LEVEL"] == "L5"
    assert "L5_REQUIRED: YES" in job["EXECUTOR"]["prompt"]
    assert job["ACCEPTANCE"]["checks"][1]["text"] == "ARM_PORTFOLIO_RECEIPT:ARM-004"


def test_built_job_acceptance_is_fail_closed_on_missing_marker(tmp_path) -> None:
    factory = ctrl.session_factory()
    job = ctrl.build_job(_arm(ctrl.plan_portfolio(generated_at="fixed"), "ARM-001"))
    with_marker = factory.run_acceptance_checks(
        job, tmp_path, {"ok": True, "stdout": "ARM_PORTFOLIO_RECEIPT:ARM-001\nFINDINGS: none"}
    )
    assert with_marker["passed"] is True
    without_marker = factory.run_acceptance_checks(
        job, tmp_path, {"ok": True, "stdout": "exit zero but no receipt"}
    )
    assert without_marker["passed"] is False
    checks = {item["kind"]: item["ok"] for item in without_marker["checks"]}
    assert checks == {"exit_zero": True, "stdout_contains": False}
