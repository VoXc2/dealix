"""Regression guard for OpenClaw memory remaining local and non-authoritative."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPAIR = ROOT / "scripts/ops/repair_dealix_openclaw_gateway.sh"


def test_openclaw_semantic_memory_is_schema_compatible_and_local() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert 'MEMORY_PREFIX="memory.search"' in text
    assert 'MEMORY_PREFIX="agents.defaults.memorySearch"' in text
    assert 'set_required "${MEMORY_PREFIX}.provider" ollama' in text
    assert 'set_required "${MEMORY_PREFIX}.model" "$EMBED_MODEL"' in text
    assert "OPENAI_API_KEY" not in text
    assert "models.providers.openai.apiKey" not in text


def test_openclaw_invalid_memory_schema_is_removed_before_config_writes() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "sanitize_known_memory_keys()" in text
    assert 'memory.pop("search", None)' in text
    assert 'defaults.pop("memorySearch", None)' in text
    sanitize_pos = text.index("sanitize_known_memory_keys\n")
    reassert_pos = text.index("set_required gateway.mode local")
    assert sanitize_pos < reassert_pos
    assert "doctor --fix" not in text


def test_openclaw_pre_memory_mutations_restore_full_backup_on_error() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "early_rollback()" in text
    assert 'restore_config_from "$BACKUP"' in text
    assert "early_repair_rollback=START" in text
    assert "early_repair_rollback=COMPLETE" in text
    backup_pos = text.index('cp -a "$CONFIG" "$BACKUP"')
    arm_pos = text.index("EARLY_ROLLBACK_ARMED=1")
    trap_pos = text.index("trap early_rollback ERR")
    sanitize_pos = text.index("sanitize_known_memory_keys\n")
    baseline_pos = text.index('chmod 0600 "$MEMORY_BASE"')
    disarm_pos = text.index("EARLY_ROLLBACK_ARMED=0", arm_pos + 1)
    assert backup_pos < arm_pos < trap_pos < sanitize_pos < baseline_pos < disarm_pos


def test_openclaw_schema_probing_is_atomic() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "pre-memory-compat" in text
    assert 'restore_config_from "$MEMORY_BASE"' in text
    assert "configure_memory_prefix()" in text
    assert "configure_memory_prefix memory.search" in text
    assert "configure_memory_prefix agents.defaults.memorySearch" in text
    assert "oc config get \"${prefix}.provider\"" in text
    assert "installed OpenClaw rejected both supported memory-search schemas" in text
    assert "memory_repair_rollback=START" in text
    assert "memory_repair_rollback=COMPLETE" in text


def test_openclaw_memory_transaction_keeps_err_rollback_armed_until_terminal_result() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "memory_rollback()" in text
    assert "memory_transaction_rollback=START" in text
    assert "memory_transaction_rollback=COMPLETE" in text
    baseline_pos = text.index('chmod 0600 "$MEMORY_BASE"')
    arm_pos = text.index("MEMORY_ROLLBACK_ARMED=1", baseline_pos)
    trap_pos = text.index("trap memory_rollback ERR", arm_pos)
    required_pos = text.index('set_required "${MEMORY_PREFIX}.provider" ollama', trap_pos)
    embed_pos = text.index('EMBED_RESPONSE="$(mktemp', required_pos)
    gateway_pos = text.index('oc gateway restart 2>&1 | redact || true', embed_pos)
    final_proof_pos = text.index('echo "===== FINAL OPENCLAW PROOF ====="', gateway_pos)
    success_disarm_pos = text.index("MEMORY_ROLLBACK_ARMED=0", final_proof_pos)
    assert baseline_pos < arm_pos < trap_pos < required_pos < embed_pos < gateway_pos < final_proof_pos < success_disarm_pos


def test_openclaw_gateway_readiness_is_bounded_and_not_fixed_sleep_only() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert 'GATEWAY_READY_TIMEOUT="${DEALIX_OPENCLAW_READY_TIMEOUT:-60}"' in text
    assert "wait_for_gateway_ready()" in text
    assert "gateway status --require-rpc" in text
    assert "ss -ltnH" in text
    assert "gateway_readiness=PASS" in text
    assert "gateway_readiness=TIMEOUT" in text
    assert "sleep 5" not in text


def test_openclaw_cli_uses_bundled_node_path_explicitly() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert 'OPENCLAW_NODE_DIR="${DEALIX_OPENCLAW_NODE_DIR:-}"' in text
    assert 'find "$OPENCLAW_HOME/tools"' in text
    assert 'OPENCLAW_PATH="${OPENCLAW_NODE_DIR}:${OPENCLAW_HOME}/bin:' in text
    assert 'PATH="$OPENCLAW_PATH"' in text
    assert '"$OPENCLAW_BIN" "$@"' in text
    assert "OpenClaw bundled Node runtime missing" in text


def test_openclaw_memory_workspace_and_index_are_initialized_locally() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert 'MEMORY_DIR="${OPENCLAW_HOME}/workspace/memory"' in text
    assert 'install -d -m 0700 -o "$RUN_USER" -g "$RUN_USER" "$MEMORY_DIR"' in text
    assert "memory_directory=READY" in text
    assert "memory status --index --agent main" in text
    assert "INDEX_RC" in text
    assert "memory_index_bootstrap=PASS" in text


def test_openclaw_memory_readiness_is_part_of_final_verdict() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "ollama_embedding_probe=PASS" in text
    assert "memory status --deep" in text
    assert "STATUS_RC" in text
    assert "GATEWAY_RC" in text
    assert "PROBE_RC" in text
    assert "CHANNEL_RC" in text
    assert "INDEX_RC" in text
    assert "MEMORY_RC" in text
    assert "MEMORY_PROVIDER_RC" in text
    assert "EMBED_RC" in text
    assert "OPENCLAW_GATEWAY_AND_MEMORY=PASS" in text
    assert "FAIL_REMOTE_OPENAI_DEPENDENCY" in text
    assert "&& $INDEX_RC -eq 0" in text


def test_openclaw_memory_does_not_weaken_founder_gateway_guards() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "gateway.bind loopback" in text
    assert "channels.telegram.dmPolicy pairing" in text
    assert "channels.telegram.groups '{}'" in text
    assert "channels.telegram.groupAllowFrom '[]'" in text
    assert 'tools.deny \'["group:runtime","group:fs","exec","process","write","edit","apply_patch"]\'' in text
    assert "OpenClaw memory is a local retrieval cache, not a second Company Brain" in text


def test_openclaw_memory_compatibility_does_not_add_live_actions_or_railway_linking() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    forbidden = (
        "gh pr merge",
        "railway up",
        "railway deploy",
        "railway link",
        "railway service list",
        "vercel --prod",
        "AUTO_SEND_ENABLED=true",
        "WHATSAPP_ALLOW_LIVE_SEND=true",
    )
    for marker in forbidden:
        assert marker not in text
