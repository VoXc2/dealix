from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "scripts" / "commercial" / "run_inbound_execution_diagnostic_bridge_v1.py"
DAILY = ROOT / "scripts" / "commercial" / "run_company_os_daily.py"


def test_daily_company_os_runs_inbound_diagnostic_bridge_before_canonical_cycle():
    text = DAILY.read_text(encoding="utf-8")
    assert "run_inbound_execution_diagnostic_bridge_v1.py" in text
    bridge_pos = text.index("inbound_rc = run")
    canonical_pos = text.index("canonical_rc = run")
    assert bridge_pos < canonical_pos
    assert "BLOCKED_INBOUND_DIAGNOSTIC_BRIDGE" in text
    assert "INBOUND_EXECUTION_DIAGNOSTIC_BRIDGE=PASS" in text


def test_bridge_is_read_only_over_canonical_revenue_store_and_material_authority_is_false():
    text = BRIDGE.read_text(encoding="utf-8")
    assert "load_company_os_inbound_diagnostics" in text
    assert '"source": "canonical_revenue_ops_autopilot"' in text
    assert '"external_send": False' in text
    assert '"public_publish": False' in text
    assert '"paid_spend": False' in text
    assert '"payment_execution": False' in text
    assert '"production_mutation": False' in text
    assert '"binding_commercial_commitment": False' in text
    assert "INBOUND_NO_FOLLOWUP" in text
    assert "customer_reported_context_is_not_verified_customer_proof" in text


def test_bridge_uses_repo_local_import_without_global_git_or_python_mutation():
    text = BRIDGE.read_text(encoding="utf-8")
    assert "sys.path.insert(0, str(ROOT))" in text
    assert "--global" not in text
    assert "safe.directory=*" not in text
