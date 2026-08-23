from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = (ROOT / "scripts/ops/dealix_founder_master_command.sh").read_text(encoding="utf-8")
REPAIR = (ROOT / "scripts/ops/repair_and_run_founder_master.sh").read_text(encoding="utf-8")


def test_founder_master_keeps_l5_kill_switches_closed():
    assert "MOYASAR_LIVE_MODE=0" in MASTER
    assert "MOYASIR_LIVE_MODE" not in MASTER
    assert "AUTO_SEND_ENABLED=false" in MASTER
    assert "WHATSAPP_ALLOW_LIVE_SEND=false" in MASTER
    assert "DEALIX_AUTO_MERGE=false" in MASTER
    assert "DEALIX_PRODUCTION_MUTATION=false" in MASTER


def test_executive_synthesis_uses_compatible_no_terminal_chat_path():
    expected = "chat -Q --ignore-rules --toolsets clarify --max-turns 1 --query-file"
    assert expected in MASTER
    assert "--toolsets terminal -z" not in MASTER
    assert "You have NO terminal or mutation tools in this run" in MASTER
    assert "tail -c 24000" in MASTER


def test_summary_fails_closed_when_critical_evidence_is_missing():
    assert "missing_critical_evidence" in MASTER
    assert "missing = [name for name in critical" in MASTER
    assert 'overall = "PASS" if not failed and not missing and heads_verified else "DEGRADED"' in MASTER


def test_repair_wrapper_does_not_patch_source_at_runtime_or_duplicate_synthesis():
    assert "sed -i 's/MOYASIR_LIVE_MODE/MOYASAR_LIVE_MODE/g'" not in REPAIR
    assert "DEALIX_RUN_LOCAL_AI=1" in REPAIR
    assert "FOUNDER_MASTER_SOURCE_GUARDS=PASS" in REPAIR
    assert "HERMES_SYNTHESIS_RC" in REPAIR
    assert "cd '$REPO' && '$HERMES' --ignore-rules" not in REPAIR
    assert "timeout 420 sudo -iu" not in REPAIR


def test_repair_wrapper_rejects_obsolete_hermes_oneshot_in_fetched_master():
    assert "grep -Fq -- '--toolsets terminal -z' \"$MASTER\"" in REPAIR
    assert "BLOCKED: obsolete Hermes oneshot path still present" in REPAIR


def test_repair_wrapper_sources_founder_master_only_from_current_main():
    assert "MAIN_SHA=" in REPAIR
    assert "PR_HEAD=" not in REPAIR
    assert "DEALIX_FOUNDER_MASTER_PR" not in REPAIR
    assert "founder_master_ref=%s" in REPAIR
    assert "contents/scripts/ops/dealix_founder_master_command.sh?ref=${MAIN_SHA}" in REPAIR
    assert "FETCH AND VERIFY FOUNDER MASTER FROM CURRENT MAIN" in REPAIR
