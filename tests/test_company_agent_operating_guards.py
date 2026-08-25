from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "dealix/registers/company_agent_operating_registry.json"
COUNCIL = ROOT / "scripts/ops/dealix_agent_council.sh"
INSTALLER = ROOT / "scripts/ops/install_dealix_company_agents.sh"
GATEWAY_REPAIR = ROOT / "scripts/ops/repair_dealix_openclaw_gateway.sh"
TELEGRAM_REPAIR = ROOT / "scripts/ops/repair_dealix_openclaw_telegram.sh"
WORKSPACE = ROOT / "docs/ops/openclaw_workspace"


def _registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def test_agent_registry_is_governed_and_complete() -> None:
    data = _registry()
    names = {agent["runtime_name"] for agent in data["agents"]}
    assert len(names) == 11
    assert {
        "company_brain",
        "sprint_orchestrator",
        "governance",
        "market_intel",
        "lead_intelligence",
        "revenue_intelligence",
        "sales_intelligence",
        "customer_acquisition",
        "diagnostic_agent",
        "data_architect",
        "managed_ops",
    } == names
    assert data["authority"]["external_send_enabled"] is False
    assert data["authority"]["production_mutation_enabled"] is False
    assert data["authority"]["merge_to_main_enabled"] is False
    assert data["authority"]["payment_execution_enabled"] is False
    assert data["agent_council"]["external_actions_executed"] == 0


def test_openclaw_is_founder_gateway_not_unrestricted_executor() -> None:
    data = _registry()["openclaw"]
    assert data["channel_owner"] == "Telegram"
    assert data["ordinary_prose_is_not_l5_approval"] is True
    blocked = set(data["blocked"])
    assert {
        "arbitrary_shell",
        "production_mutation",
        "merge_to_main",
        "payments",
        "secret_access",
        "automatic_external_send",
    } <= blocked


def test_telegram_founder_control_is_dm_only_by_default() -> None:
    for path in (GATEWAY_REPAIR, TELEGRAM_REPAIR):
        text = path.read_text(encoding="utf-8")
        assert "channels.telegram.dmPolicy pairing" in text
        assert "channels.telegram.groups '{}'" in text
        assert "channels.telegram.groupAllowFrom '[]'" in text
        assert "{\"*\":{\"requireMention\":true}}" not in text


def test_council_has_hard_safe_flags_and_no_l5_primitives() -> None:
    text = COUNCIL.read_text(encoding="utf-8")
    for expected in (
        "DEALIX_EXTERNAL_OUTREACH_ENABLED=false",
        "AUTO_SEND_ENABLED=false",
        "AGENT_APPROVAL_MODE=required",
        "WHATSAPP_ALLOW_LIVE_SEND=false",
        "MOYASAR_LIVE_MODE=0",
        "external_actions_executed\": 0",
    ):
        assert expected in text

    forbidden = (
        "gh pr merge",
        "railway up",
        "railway redeploy",
        "railway variables set",
        "vercel --prod",
        "git push origin main",
        "git checkout main && git merge",
        "curl -X DELETE",
    )
    for token in forbidden:
        assert token not in text


def test_council_runs_bounded_safe_hermes_seats() -> None:
    text = COUNCIL.read_text(encoding="utf-8")
    # Tool/rules scope stays pinned on BOTH seat and synthesis invocations.
    assert text.count("--ignore-rules chat --toolsets safe") >= 2
    # Bounded throughput contract: dynamic turn budgets + hard wall-clock
    # timeouts per seat and for synthesis, never unbounded hermes calls.
    assert '--toolsets safe --max-turns "$turns"' in text
    assert "--max-turns \"$SYNTH_TURNS\"" in text
    assert 'ROLE_TIMEOUT="${DEALIX_COUNCIL_ROLE_TIMEOUT:-300}"' in text
    assert 'SYNTH_TIMEOUT="${DEALIX_COUNCIL_SYNTH_TIMEOUT:-300}"' in text
    assert "timeout --kill-after=15 --signal=TERM" in text
    # SKIP_UNCHANGED: identical state must never re-bill LLM calls, and a
    # degraded run must never be persisted as reusable truth.
    assert "SKIP_REASON=input_unchanged" in text
    assert "COUNCIL_DEGRADED: seat failures/timeouts present; pointers NOT persisted" in text
    assert "seats_failed" in text and "seats_timeout" in text
    assert "exit 1" in text
    assert "BLOCKED: FAST_ROLES matched no known seat" in text
    # FAST/incremental mode without a second scheduler or council system
    assert "DEALIX_COUNCIL_FAST_ROLES" in text
    # Context slicing: provenance header survives, doctrine non-negotiable.
    assert "want || !insec { print }" in text
    assert '"${spec},CANONICAL RULES"' in text
    for seat in (
        "EXECUTIVE_OPERATIONS",
        "REVENUE_SALES",
        "MARKET_PARTNERSHIPS",
        "CUSTOMER_DELIVERY",
        "PRODUCT_ENGINEERING",
        "GOVERNANCE_FINANCE",
        "CEO_CHAIR",
    ):
        assert seat in text


def test_council_schedule_fills_gap_without_duplicate_existing_cadence() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert "Sun,Mon,Tue,Wed,Thu *-*-* 10:15:00 Asia/Riyadh" in text
    # Known Company Autopilot times must not be duplicated by this installer.
    for existing in ("06:30:00", "08:45:00", "12:30:00", "19:00:00", "21:15:00", "23:30:00"):
        assert existing not in text


def test_systemd_sandbox_keeps_repo_read_only_and_memory_bounded() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert "User=dealix" in text
    assert "NoNewPrivileges=true" in text
    assert "ProtectSystem=full" in text
    assert "ProtectHome=read-only" in text
    assert "ReadOnlyPaths=/opt/dealix/workspace/dealix /home/dealix/.openclaw" in text
    assert "CapabilityBoundingSet=" in text
    assert "MemoryMax=6G" in text
    assert "CPUQuota=300%" in text
    assert "Environment=DEALIX_LOCAL_MODEL=qwen3:4b-instruct-2507-q4_K_M" in text


def test_council_installer_enforces_proof_integrity_on_every_reinstall() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    for expected in (
        "DEALIX PROOF INTEGRITY — NON-NEGOTIABLE",
        "Synthetic, demo, test, placeholder",
        "Missing evidence MUST remain a Proof Gap",
        'evidence_events_tracker.csv',
        "Never recommend synthetic evidence as a substitute for a Truth Matrix proof",
        "a healthy API does not prove the frontend is",
        "Approval Items contain only actions that actually require an L5 founder gate",
        "COUNCIL_PROOF_INTEGRITY=ENFORCED",
    ):
        assert expected in text
    assert '"${PROOF_INTEGRITY_POLICY}"' in text
    assert "bash -n \"$TMP/dealix_agent_council.sh\"" in text


def test_council_timer_is_installed_but_fail_closed_by_default() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert "systemctl disable --now dealix-agent-council.timer" in text
    assert "systemctl enable --now dealix-agent-council.timer" not in text
    assert "agent_council_activation=requires_hermes_8k_acceptance" in text


def test_openclaw_bootstrap_files_are_compact_and_present() -> None:
    required = ("AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md", "TOOLS.md", "HEARTBEAT.md")
    for name in required:
        path = WORKSPACE / name
        assert path.is_file(), name
        assert path.stat().st_size < 12_000, name

    agents = (WORKSPACE / "AGENTS.md").read_text(encoding="utf-8")
    assert "ordinary conversation" in agents
    assert "Synthetic evidence never counts" in agents
    assert "No second Company Brain" not in agents  # avoid adding a second system by wording as a new component


def test_installer_hardens_subagents_without_touching_owner_or_secrets() -> None:
    text = INSTALLER.read_text(encoding="utf-8")
    assert "agents.defaults.subagents.maxConcurrent 2" in text
    assert "agents.defaults.subagents.delegationMode prefer" in text
    assert "tools.subagents.tools.deny" in text
    assert '"exec"' in text
    assert '"write"' in text
    assert '"apply_patch"' in text
    assert "commands.ownerAllowFrom" not in text
    assert "gateway.auth.token" not in text
    assert "channels.telegram.botToken" not in text
