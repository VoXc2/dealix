"""Track C (C2-C6) "smart enough to run with API keys" assertions.

Tests the modules that ship in this batch:
- C2 LLM-driven daily brief (auto_client_acquisition.personal_operator.llm_brief)
- C3 Watchdog drift check (scripts.watchdog_drift_check)
- C4 Founder command bus (api.routers.command_bus)
- C5 Moyasar webhook reconciliation (auto_client_acquisition.payment_ops.reconciliation)
- C6 Weekly self-improvement (core.queue.weekly_self_improvement)

These tests must pass WITHOUT any live LLM/Redis/Postgres infrastructure
(graceful fallback discipline). Real-LLM coverage lives in
test_*_live.py files that run only when API keys are set.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO = Path(__file__).resolve().parents[1]


# ─── C2: LLM-driven daily brief ──────────────────────────────────────


class TestC2DailyBriefLLM:
    @pytest.fixture
    def llm_brief_module(self):
        from auto_client_acquisition.personal_operator import llm_brief
        return llm_brief

    def test_module_imports(self, llm_brief_module):
        assert hasattr(llm_brief_module, "generate_llm_brief")
        assert hasattr(llm_brief_module, "fetch_recent_proof_events")

    def test_fallback_brief_no_data(self, llm_brief_module):
        brief = llm_brief_module._fallback_brief(
            proof_events=[], pending_approvals=[], inbound_count=0
        )
        assert brief.data_status == "insufficient_data"
        # No-data brief steers toward safe early actions — the warm-intro
        # guidance lives in the narrative, the concrete step in next_action.
        guidance = f"{brief.next_action} {brief.narrative}".lower()
        assert "warm intro" in guidance or "diagnostic" in guidance
        assert brief.headline  # non-empty

    def test_fallback_brief_with_data(self, llm_brief_module):
        brief = llm_brief_module._fallback_brief(
            proof_events=[{"level": "L3"}, {"level": "L5"}],
            pending_approvals=[{"mode": "approval", "title": "test"}],
            inbound_count=2,
        )
        assert brief.data_status == "fallback"
        assert "2 proof event" in brief.narrative or "موافقة" in brief.narrative

    def test_format_input_compact(self, llm_brief_module):
        out = llm_brief_module._format_input_data(
            proof_events=[{"level": "L5"}, {"level": "L1"}],
            pending_approvals=[{"mode": "approval", "title": "Test approval"}],
            inbound_count=3,
        )
        assert "Proof events" in out
        assert "L5: 1" in out
        # Stays under token budget — char check as proxy
        assert len(out) < 2000

    def test_parse_brief_extracts_three_sections(self, llm_brief_module):
        text = """\
Headline: تجاوزنا أوّل proof L5
Narrative: الأسبوع كان قويّاً. 3 proof events، أحدها L5 من Slot-A.
Next action: راجع publish_consent مع Slot-A قبل الجمعة.
"""
        h, n, a = llm_brief_module._parse_brief(text)
        assert h
        assert "Slot-A" in n or "L5" in n
        assert "Slot-A" in a or "publish_consent" in a

    def test_generate_llm_brief_falls_back_when_router_unavailable(self, llm_brief_module):
        # Force the LLM call to fail
        async def _runner():
            with patch.object(
                llm_brief_module,
                "_call_llm",
                side_effect=RuntimeError("router unavailable"),
            ):
                return await llm_brief_module.generate_llm_brief(
                    proof_events=[{"level": "L4"}],
                    pending_approvals=[],
                    inbound_count=1,
                )
        brief = asyncio.run(_runner())
        assert brief.data_status in ("fallback", "insufficient_data")
        assert brief.headline


# ─── C3: Watchdog drift check ────────────────────────────────────────


class TestC3Watchdog:
    @pytest.fixture
    def watchdog(self):
        sys.path.insert(0, str(REPO / "scripts"))
        try:
            import watchdog_drift_check  # type: ignore
            return watchdog_drift_check
        finally:
            sys.path.pop(0)

    def test_run_all_returns_results(self, watchdog):
        results, failed = watchdog.run_all()
        assert isinstance(results, list)
        assert len(results) == len(watchdog.CHECKS)
        for r in results:
            assert "name" in r and "pass" in r and "detail" in r

    def test_hard_gate_defaults_check(self, watchdog):
        ok, detail = watchdog.check_hard_gate_defaults()
        # Should pass (whatsapp_allow_live_send: bool = False is in settings)
        assert ok, f"hard_gate_defaults failed: {detail}"

    def test_service_readiness_sync_check(self, watchdog):
        ok, detail = watchdog.check_service_readiness_sync()
        assert ok, f"service_readiness_sync failed: {detail}"
        assert "live=" in detail

    def test_health_endpoint_skips_when_no_url(self, watchdog, monkeypatch):
        monkeypatch.delenv("WATCHDOG_BASE_URL", raising=False)
        ok, detail = watchdog.check_health_endpoint(base_url=None)
        assert ok
        assert "skipped" in detail.lower()


# ─── C4: Command bus ─────────────────────────────────────────────────


class TestC4CommandBus:
    @pytest.fixture
    def cmd_bus(self):
        from api.routers import command_bus
        return command_bus

    def test_check_cold_intent_blocks_blast(self, cmd_bus):
        assert cmd_bus._check_cold_intent("ابعث blast لـ 1000 شركة")
        assert cmd_bus._check_cold_intent("send a cold whatsapp to leads")
        assert cmd_bus._check_cold_intent("scrape linkedin for CTOs")
        assert cmd_bus._check_cold_intent("بدون موافقة ابعث للقائمة")

    def test_check_cold_intent_allows_legitimate(self, cmd_bus):
        assert not cmd_bus._check_cold_intent(
            "جهّز رسالة متابعة لـ Acme بعد موافقتهم"
        )
        assert not cmd_bus._check_cold_intent(
            "draft a follow-up email to ahmad about the pilot"
        )

    def test_parse_llm_json_extracts_object(self, cmd_bus):
        text = """Some preamble.
{
  "action_type": "outbound_message",
  "summary_ar": "متابعة",
  "summary_en": "Follow-up",
  "draft_body": "السلام عليكم أحمد..."
}
Trailing text."""
        parsed = cmd_bus._parse_llm_json(text)
        assert parsed["action_type"] == "outbound_message"
        assert "أحمد" in parsed["draft_body"]

    def test_parse_llm_json_synthesizes_when_no_object(self, cmd_bus):
        parsed = cmd_bus._parse_llm_json("no json here, just text")
        assert parsed["action_type"] == "note"
        assert parsed["draft_body"]


# ─── C5: Moyasar reconciliation ──────────────────────────────────────


class TestC5MoyasarReconciliation:
    @pytest.fixture
    def recon(self):
        from auto_client_acquisition.payment_ops import reconciliation
        # Reset dedup state between tests
        reconciliation._RECONCILED_WEBHOOK_IDS.clear()
        return reconciliation

    def test_signature_verification_no_secret_test_mode(self, recon):
        # When MOYASAR_WEBHOOK_SECRET is unset, treat as valid (test mode)
        v = recon.verify_webhook_signature(b"{}", {}, secret=None)
        assert v.valid
        assert "test mode" in v.reason

    def test_signature_verification_missing_header(self, recon):
        v = recon.verify_webhook_signature(b"{}", {}, secret="my_secret")
        assert not v.valid
        assert "missing_signature_header" in v.reason

    def test_signature_verification_valid_hmac(self, recon):
        import hashlib
        import hmac
        secret = "secret_xyz"
        body = b'{"id":"evt_1","type":"payment.paid","data":{"id":"pay_1","invoice_id":"inv_1","amount":49900}}'
        sig = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        v = recon.verify_webhook_signature(
            body, {recon.SIGNATURE_HEADER: sig}, secret=secret
        )
        assert v.valid

    def test_reconcile_payment_idempotent(self, recon):
        payload = {
            "id": "evt_dedup",
            "type": "payment.paid",
            "data": {
                "id": "pay_x",
                "invoice_id": "inv_x",
                "amount": 49900,
                "currency": "SAR",
                "metadata": {"customer_handle": "Slot-A"},
            },
        }
        r1 = recon.reconcile_payment(payload)
        r2 = recon.reconcile_payment(payload)
        assert not r1.duplicate
        assert r2.duplicate
        assert r1.invoice_id == r2.invoice_id == "inv_x"
        assert r1.revenue_amount_sar == 499.0

    def test_reconcile_payment_l5_proof_event_id_present(self, recon):
        payload = {
            "id": "evt_l5",
            "type": "payment.paid",
            "data": {
                "id": "pay_l5",
                "invoice_id": "inv_l5",
                "amount": 299900,
                "metadata": {"customer_handle": "Slot-B"},
            },
        }
        r = recon.reconcile_payment(payload)
        assert r.proof_event_id
        assert r.proof_event_id.startswith("prf_l5_")
        assert r.revenue_amount_sar == 2999.0
        assert r.customer_handle == "Slot-B"

    def test_parse_webhook_request_invalid_json(self, recon):
        v, result = recon.parse_webhook_request(b"not json", {}, secret=None)
        assert not v.valid
        assert result is None


# ─── C6: Weekly self-improvement ─────────────────────────────────────


class TestC6WeeklySelfImprovement:
    @pytest.fixture
    def wsi(self):
        # Direct module import bypasses core.queue.__init__ which depends
        # on ARQ (not installed in this lightweight test env).
        # Must register in sys.modules before exec for @dataclass to resolve types.
        import importlib.util

        if "weekly_self_improvement" in sys.modules:
            return sys.modules["weekly_self_improvement"]

        spec = importlib.util.spec_from_file_location(
            "weekly_self_improvement",
            REPO / "core" / "queue" / "weekly_self_improvement.py",
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules["weekly_self_improvement"] = module
        spec.loader.exec_module(module)
        return module

    def test_module_imports(self, wsi):
        assert hasattr(wsi, "run_weekly_self_improvement")
        assert hasattr(wsi, "WeeklyScorecard")
        assert hasattr(wsi, "Suggestion")

    def test_default_suggestion_when_no_signals(self, wsi):
        empty_card = wsi.WeeklyScorecard(week_starting="2026-05-04")
        suggestions = wsi._generate_deterministic_suggestions(empty_card, None)
        assert len(suggestions) >= 1
        # Empty scorecard triggers either the no-proof-events rule or the
        # warm-intros default — both are acceptable signals to action.
        haystack = " ".join((s.title + " " + s.next_action) for s in suggestions).lower()
        assert any(
            keyword in haystack
            for keyword in ("warm intros", "proof event", "warm-intro", "diagnostic")
        )

    def test_pending_approvals_triggers_suggestion(self, wsi):
        card = wsi.WeeklyScorecard(week_starting="2026-05-04", pending_approvals=8)
        suggestions = wsi._generate_deterministic_suggestions(card, None)
        assert any("approval" in s.title.lower() or "موافقات" in s.title for s in suggestions)

    def test_revenue_regression_triggers_suggestion(self, wsi):
        prev = wsi.WeeklyScorecard(week_starting="2026-04-27", revenue_sar=2000.0)
        curr = wsi.WeeklyScorecard(week_starting="2026-05-04", revenue_sar=500.0)
        suggestions = wsi._generate_deterministic_suggestions(curr, prev)
        assert any("الإيراد" in s.title or "revenue" in s.title.lower()
                   for s in suggestions)

    def test_first_l5_milestone(self, wsi):
        prev = wsi.WeeklyScorecard(week_starting="2026-04-27", proof_events_l5=0)
        curr = wsi.WeeklyScorecard(week_starting="2026-05-04", proof_events_l5=1)
        suggestions = wsi._generate_deterministic_suggestions(curr, prev)
        assert any("L5" in s.title or "case study" in s.title.lower()
                   for s in suggestions)

    def test_max_three_suggestions(self, wsi):
        # Trigger every rule simultaneously
        prev = wsi.WeeklyScorecard(
            week_starting="2026-04-27", revenue_sar=5000.0, proof_events_l5=0
        )
        curr = wsi.WeeklyScorecard(
            week_starting="2026-05-04",
            pending_approvals=10,
            proof_events_total=0,
            proof_events_l5=1,
            revenue_sar=1000.0,
            forbidden_token_violations=2,
        )
        suggestions = wsi._generate_deterministic_suggestions(curr, prev)
        assert len(suggestions) <= 3, "cognitive-load discipline: max 3 suggestions"

    def test_run_weekly_returns_valid_card(self, wsi, tmp_path, monkeypatch):
        monkeypatch.setattr(wsi, "WEEKLY_CACHE", tmp_path / "wsi_test.json")
        card = wsi.run_weekly_self_improvement()
        assert isinstance(card, wsi.WeeklyScorecard)
        assert isinstance(card.suggestions, list)
        assert len(card.suggestions) <= 3


# ─── Cross-cutting: file existence + import sanity ───────────────────


def test_track_c_files_exist():
    expected = [
        REPO / "auto_client_acquisition" / "personal_operator" / "llm_brief.py",
        REPO / "scripts" / "watchdog_drift_check.py",
        REPO / "api" / "routers" / "command_bus.py",
        REPO / "auto_client_acquisition" / "payment_ops" / "reconciliation.py",
        REPO / "core" / "queue" / "cs_handoff_task.py",
        REPO / "core" / "queue" / "weekly_self_improvement.py",
        REPO / ".github" / "workflows" / "watchdog_drift.yml",
        REPO / ".github" / "workflows" / "weekly_self_improvement.yml",
        REPO / "landing" / "founder-command-bus.html",
    ]
    missing = [p for p in expected if not p.exists()]
    assert not missing, f"missing files: {missing}"


def test_track_d5_playwright_files_exist():
    expected = [
        REPO / "tests" / "playwright" / "playwright.config.js",
        REPO / "tests" / "playwright" / "tier1_smoke.spec.js",
        REPO / "tests" / "playwright" / "package.json",
        REPO / ".github" / "workflows" / "playwright_smoke.yml",
    ]
    missing = [p for p in expected if not p.exists()]
    assert not missing, f"missing files: {missing}"


def test_command_bus_html_has_safety_strip():
    html = (REPO / "landing" / "founder-command-bus.html").read_text(encoding="utf-8")
    assert "NO_LIVE_SEND" in html
    assert "NO_COLD_WHATSAPP" in html
    # The UI must surface the access-gate (founder-only)
    assert "access-gate.js" in html


def test_workflows_have_correct_cron():
    # Watchdog: every hour
    wd = (REPO / ".github" / "workflows" / "watchdog_drift.yml").read_text(encoding="utf-8")
    assert re.search(r'cron:\s*"\d+\s+\*\s+\*\s+\*\s+\*"', wd)
    # Weekly: Sunday 19:00 UTC
    ws = (
        REPO / ".github" / "workflows" / "weekly_self_improvement.yml"
    ).read_text(encoding="utf-8")
    assert "0 19 * * 0" in ws
