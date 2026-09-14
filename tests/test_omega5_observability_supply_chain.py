"""Omega5 observability + supply-chain focused tests (no network, no installs)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "scripts" / "ops" / "verify_supply_chain_gates_v1.py"
RECEIPT_SCHEMA = ROOT / "schemas" / "execution_receipt.schema.json"


def _load_gate():
    spec = importlib.util.spec_from_file_location("verify_supply_chain_gates_v1", GATE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _base_record(**overrides):
    base = {
        "correlation_id": "cor_omega5_0001",
        "customer_id": "cust_anon_7",
        "agent_id": "agent_executor",
        "workflow_id": "wf_runtime",
    }
    base.update(overrides)
    return base


def test_execution_contract_fields_present_with_defaults():
    from auto_client_acquisition.observability_v10 import TraceRecordV10

    rec = TraceRecordV10(correlation_id="cor_x")
    for field in (        "trace_id",
        "case_id",
        "job_id",
        "owner",
        "effect_class",
        "authority",
        "model_provider_class",
        "tool_name",
        "action_name",
        "verifier",
        "result",
        "cost_known_state",
        "evidence_refs",
        "release_sha",
    ):
        assert field in TraceRecordV10.model_fields
    assert rec.effect_class == "none"
    assert rec.result == "unknown"
    assert rec.cost_known_state == "unknown"
    assert rec.evidence_refs == []


def test_execution_contract_roundtrip_with_new_fields():
    from auto_client_acquisition.observability_v10 import (
        _reset_v10_buffer,
        list_v10_traces,
        record_v10_trace,
    )

    _reset_v10_buffer()
    try:
        stored = record_v10_trace(
            _base_record(
                case_id="case_42",
                job_id="job_9",
                owner="sector-company/logical-agent",
                effect_class="repo_execute",
                authority="L4",
                model_provider_class="local-loopback",
                tool_name="pytest",
                action_name="bounded_verify",
                verifier="independent-verifier",
                result="ok",
                cost_known_state="estimated",
                evidence_refs=["reports/omega5/receipt.json"],
                release_sha="4d5f49038",
            )
        )
        assert stored.case_id == "case_42"
        assert stored.release_sha == "4d5f49038"
        rows = list_v10_traces(limit=5)
        assert len(rows) == 1
        assert rows[0].trace_id == stored.trace_id
    finally:
        _reset_v10_buffer()


def test_denied_payload_keys_coerce_to_hold():
    from auto_client_acquisition.observability_v10 import _reset_v10_buffer, record_v10_trace
    from auto_client_acquisition.observability_v10.trace_schema import (
        coerce_denied_payload_keys,
    )

    coerced = coerce_denied_payload_keys(
        {"prompt": "secret plan", "summary": "ok", "nested": {"tool_args": {"a": 1}}}
    )
    assert coerced["prompt"] == "HOLD"
    assert coerced["summary"] == "ok"
    assert coerced["nested"]["tool_args"] == "HOLD"

    _reset_v10_buffer()
    try:
        stored = record_v10_trace(
            _base_record(redacted_payload={"prompt": "do not store", "note": "fine"})
        )
        assert stored.redacted_payload["prompt"] == "HOLD"
        assert stored.redacted_payload["note"] == "fine"
    finally:
        _reset_v10_buffer()


def test_agent_trace_carries_contract_fields():
    # Verify statically via AST: importing through the package __init__
    # pulls the radar_events/persistence chain (sqlalchemy), which is out
    # of scope for this hermetic gate test.
    import ast

    src = (
        ROOT / "auto_client_acquisition" / "agent_observability" / "schemas.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(src)
    agent_fields: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "AgentTrace":
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    agent_fields.add(stmt.target.id)
    for field in (
        "trace_id",
        "case_id",
        "job_id",
        "owner",
        "effect_class",
        "authority",
        "model_provider_class",
        "tool_name",
        "action_name",
        "verifier",
        "result",
        "cost_known_state",
        "evidence_refs",
        "release_sha",
        "redacted_payload",
    ):
        assert field in agent_fields, field
    assert 'result: str = "unknown"' in src
    assert 'effect_class: str = "none"' in src

    # record_trace must persist through the redaction path (static check).
    trace_src = (
        ROOT / "auto_client_acquisition" / "agent_observability" / "trace.py"
    ).read_text(encoding="utf-8")
    assert "redact_trace(payload or {})" in trace_src


def test_receipt_schema_is_deterministic_and_closed():
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    assert schema["title"].startswith("Dealix Omega5")
    assert schema["additionalProperties"] is False
    for field in (
        "schema_version",
        "receipt_id",
        "trace_id",
        "result",
        "effect_class",
        "authority",
        "produced_at",
        "release_sha",
    ):
        assert field in schema["required"]
    assert "prompt" not in schema["properties"]
    assert "tool_args" not in schema["properties"]
    assert "raw_result" not in schema["properties"]


def test_openobserve_adapter_disabled_by_default_no_network(monkeypatch):
    from auto_client_acquisition.observability_adapters.base import get_adapter
    from auto_client_acquisition.observability_adapters.openobserve_adapter import (
        OpenObserveAdapter,
    )

    for var in (
        "OPENOBSERVE_ENABLED",
        "OPENOBSERVE_URL",
        "OPENOBSERVE_TOKEN",
        "OPENOBSERVE_ORG",
        "OPENOBSERVE_STREAM",
    ):
        monkeypatch.delenv(var, raising=False)
    adapter = OpenObserveAdapter()
    assert adapter.is_configured() is False
    # emit must be a safe noop and never raise
    from auto_client_acquisition.observability_adapters.base import ObservabilityEvent

    adapter.emit(ObservabilityEvent(event_type="test", model="x"))
    assert isinstance(get_adapter("openobserve"), OpenObserveAdapter)
    assert isinstance(get_adapter("bogus_adapter"), object)


def test_supply_chain_gate_missing_tools_is_hold_never_pass(capsys, monkeypatch, tmp_path):
    gate = _load_gate()
    monkeypatch.setattr(gate.shutil, "which", lambda _name: None)
    monkeypatch.setenv("DEALIX_SUPPLY_CHAIN_LAB_ROOT", str(tmp_path / "no-lab"))
    for var in ("COSIGN_IDENTITY", "COSIGN_DIGEST", "COSIGN_DIGEST_FILE"):
        monkeypatch.delenv(var, raising=False)
    rc = gate.main()
    out = capsys.readouterr().out
    assert rc == 2
    assert "DEALIX_SUPPLY_CHAIN_GATES_V1=HOLD" in out
    assert "DEALIX_SUPPLY_CHAIN_GATES_V1=PASS" not in out
    assert "production_mutation=false" in out
    assert "auto_install=false" in out
    assert "auto_sign=false" in out


def test_supply_chain_gate_never_installs_or_signs():
    text = GATE_PATH.read_text(encoding="utf-8")
    # Forbid executed install/sign/push commands (prose mentions in the
    # docstring such as "no installs" are allowed — only invocations count).
    for forbidden in (
        '["curl"',
        "['curl'",
        '["wget"',
        '"pip install"',
        "'pip install'",
        '"cosign sign"',
        "'cosign sign'",
        '"docker push"',
        "'docker push'",
        "urllib.request.urlretrieve",
    ):
        assert forbidden not in text, forbidden
    assert "shutil.which" in text
