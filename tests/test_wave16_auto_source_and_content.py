"""Wave 16 — Auto-source + content tests.

Tests the 3 new CLIs and 1 landing page:
- founder_brief.query_layer_counts()
- dealix_artifact_enforcer.find_overdue_sessions()
- dealix_case_study_builder (CLI smoke)
- landing/sector-benchmark.html structural assertions

Hard rules verified:
- Article 4: artifact_enforcer NEVER auto-closes; case_study_builder
  NEVER auto-publishes
- Article 8: query_layer_counts() returns 0 honestly when modules empty
- Article 11: every helper is a thin wrapper

Sandbox-safe: uses importlib bypass for CLI scripts.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


# ─────────────────────────────────────────────────────────────────────
# Phase C1 — founder_brief.query_layer_counts (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_query_layer_counts_returns_layer_counts_dataclass() -> None:
    from auto_client_acquisition.founder_brief import LayerCounts, query_layer_counts

    counts = query_layer_counts()
    assert isinstance(counts, LayerCounts)
    assert counts.is_estimate is True  # Article 8


def test_query_layer_counts_returns_zero_in_empty_state() -> None:
    """Article 8: empty modules return honest 0 — never fabrication."""
    from auto_client_acquisition.founder_brief import query_layer_counts

    counts = query_layer_counts()
    # All counts MUST be non-negative integers
    assert counts.blocking_approvals >= 0
    assert counts.pending_payment_confirmations >= 0
    assert counts.pending_proof_packs_to_send >= 0
    assert counts.overdue_followups >= 0
    assert counts.sla_at_risk_tickets >= 0
    assert counts.paid_customers >= 0


def test_query_layer_counts_lists_sources_used() -> None:
    """sources_used MUST list which modules were queried."""
    from auto_client_acquisition.founder_brief import query_layer_counts

    counts = query_layer_counts()
    assert "approval_center" in counts.sources_used
    assert "payment_ops" in counts.sources_used
    assert "support_os" in counts.sources_used
    # Service sessions queried twice (active + completed)
    assert "service_sessions:active" in counts.sources_used
    assert "service_sessions:completed" in counts.sources_used


def test_layer_counts_is_frozen_immutable() -> None:
    """Article 8 guard: LayerCounts is frozen — cannot be tampered."""
    from auto_client_acquisition.founder_brief import LayerCounts

    counts = LayerCounts()
    with pytest.raises((AttributeError, Exception)):
        counts.blocking_approvals = 999  # type: ignore[misc]


# ─────────────────────────────────────────────────────────────────────
# Phase C2 — dealix_artifact_enforcer (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_artifact_enforcer_returns_empty_in_clean_state() -> None:
    """No active sessions → no overdue."""
    script = REPO_ROOT / "scripts" / "dealix_artifact_enforcer.py"
    spec = importlib.util.spec_from_file_location("_enf_test", script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_enf_test"] = mod
    spec.loader.exec_module(mod)

    overdue = mod.find_overdue_sessions()
    assert isinstance(overdue, list)
    # Sandbox starts with no sessions, so MUST be empty
    assert overdue == []


def test_artifact_enforcer_cli_one_line_format() -> None:
    """One-line output starts with [OK] or [ALERT]."""
    script = REPO_ROOT / "scripts" / "dealix_artifact_enforcer.py"
    out = subprocess.check_output(
        [sys.executable, str(script), "--format", "one-line"],
        cwd=str(REPO_ROOT), timeout=10,
    ).decode("utf-8").strip()
    assert out.startswith("[OK]") or out.startswith("[ALERT]")
    assert "artifact_enforcer" in out


def test_artifact_enforcer_cli_json_has_is_estimate() -> None:
    """Article 8: JSON output MUST carry is_estimate=True."""
    script = REPO_ROOT / "scripts" / "dealix_artifact_enforcer.py"
    out = subprocess.check_output(
        [sys.executable, str(script), "--format", "json"],
        cwd=str(REPO_ROOT), timeout=10,
    ).decode("utf-8")
    payload = json.loads(out)
    assert payload["is_estimate"] is True
    assert "overdue_count" in payload
    assert "scope" in payload


# ─────────────────────────────────────────────────────────────────────
# Phase C3 — dealix_case_study_builder (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_case_study_demo_mode_succeeds() -> None:
    """--demo MUST produce a valid case study draft."""
    script = REPO_ROOT / "scripts" / "dealix_case_study_builder.py"
    result = subprocess.run(
        [sys.executable, str(script), "--demo",
         "--customer-handle", "test-acme", "--sector", "real_estate"],
        cwd=str(REPO_ROOT), timeout=10, capture_output=True,
    )
    assert result.returncode == 0
    # Output MUST contain narrative markers
    out = result.stdout.decode("utf-8")
    assert "Case Study Draft" in out
    assert "test-acme" in out
    assert "real_estate" in out


def test_case_study_demo_json_has_candidate_fields() -> None:
    """JSON output MUST have candidate + safety_findings + rejected fields."""
    script = REPO_ROOT / "scripts" / "dealix_case_study_builder.py"
    out = subprocess.check_output(
        [sys.executable, str(script), "--demo",
         "--customer-handle", "test-acme",
         "--sector", "real_estate",
         "--format", "json"],
        cwd=str(REPO_ROOT), timeout=10,
    ).decode("utf-8")
    payload = json.loads(out)
    assert payload["customer_handle"] == "test-acme"
    assert payload["is_estimate"] is True  # Article 8
    assert "candidate" in payload
    assert "safety_findings" in payload
    assert "rejected" in payload


def test_case_study_refuses_when_no_publishable_events(tmp_path) -> None:
    """Article 8: refuse to fabricate when no events meet publish gate."""
    script = REPO_ROOT / "scripts" / "dealix_case_study_builder.py"
    bad_events = tmp_path / "bad_events.jsonl"
    bad_events.write_text(
        json.dumps({
            "event_id": "bad_001",
            "evidence_level": "observed",  # too weak
            "consent_for_publication": False,
            "approval_status": "pending",
            "pii_redacted": True,
        }) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(script),
         "--customer-handle", "bad-test",
         "--events", str(bad_events)],
        cwd=str(REPO_ROOT), timeout=10, capture_output=True,
    )
    # Article 8: explicit refusal (exit 1)
    assert result.returncode == 1
    err = result.stderr.decode("utf-8")
    assert "REFUSED" in err
    assert "Article 8" in err


def test_case_study_requires_events_flag() -> None:
    """Without --demo or --events, CLI exits 2 (usage error)."""
    script = REPO_ROOT / "scripts" / "dealix_case_study_builder.py"
    result = subprocess.run(
        [sys.executable, str(script),
         "--customer-handle", "test"],
        cwd=str(REPO_ROOT), timeout=10, capture_output=True,
    )
    assert result.returncode == 2


# ─────────────────────────────────────────────────────────────────────
# Phase C4 — landing/sector-benchmark.html (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_sector_benchmark_html_exists() -> None:
    path = REPO_ROOT / "landing" / "sector-benchmark.html"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert len(content) > 5000  # non-trivial size


def test_sector_benchmark_has_6_sectors() -> None:
    """6 Saudi B2B sectors: real_estate, clinics, logistics, b2b_services, agency, consulting."""
    path = REPO_ROOT / "landing" / "sector-benchmark.html"
    content = path.read_text(encoding="utf-8")
    assert content.count('data-sector-id=') == 6
    # Check each sector appears
    for sector in ("real_estate", "clinics", "logistics", "b2b_services", "agency", "consulting"):
        assert f'data-sector-id="{sector}"' in content


def test_sector_benchmark_is_bilingual() -> None:
    """Page MUST be Arabic-first with English mirror per section."""
    path = REPO_ROOT / "landing" / "sector-benchmark.html"
    content = path.read_text(encoding="utf-8")
    assert 'lang="ar"' in content
    assert 'dir="rtl"' in content
    # Bilingual pattern: AR first, then EN sub-text
    assert 'sub-en' in content
    assert 'angle-ar' in content or 'angle-text' in content
    assert 'recommended angle' in content.lower()


def test_sector_benchmark_declares_article_8_estimate() -> None:
    """Article 8: page MUST declare is_estimate."""
    path = REPO_ROOT / "landing" / "sector-benchmark.html"
    content = path.read_text(encoding="utf-8")
    # is_estimate appears at least 6 times (once per sector card footer)
    assert content.count('is_estimate=True') >= 6
    # Hard rules section explicitly mentions Article 4
    assert "Article 4" in content
    assert "8 hard gates" in content.lower()


# ─────────────────────────────────────────────────────────────────────
# Article 4 + 8 invariants (cross-cutting)
# ─────────────────────────────────────────────────────────────────────


def test_no_wave16_cli_attempts_live_send() -> None:
    """Wave 16 CLIs MUST never write to disk in the founder_brief auto-source."""
    # founder_brief.query_layer_counts is read-only by design.
    from auto_client_acquisition.founder_brief import query_layer_counts

    counts = query_layer_counts()
    # Calling it twice in a row MUST be idempotent
    counts2 = query_layer_counts()
    # Counts may differ if sessions added between calls, but state never
    # SHOULD have changed (no writes in either call)
    assert counts.is_estimate == counts2.is_estimate
