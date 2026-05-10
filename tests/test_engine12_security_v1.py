"""Wave 12.5 §33.2.6 (Engine 12) — Trust/Security/Compliance v1 tests.

Validates the standalone Engine 12 hardening pieces:
- SSRF guard: blocks 8 internal-IP patterns + cloud metadata + IPv6
  loopback; allows ~30 approved external domains
- Email deliverability check: SPF + DKIM + DMARC validation +
  one-click unsubscribe + daily-cap recommendations

(Tenant isolation middleware + BOPLA decorator deferred to Wave 12.6
follow-up — they need full FastAPI app integration tests beyond
this commit's scope.)

All tests pure-function — no DNS lookups, no HTTP, deterministic.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

# Load ssrf_guard directly without triggering api/security/__init__.py
# (which eagerly imports python-jose — fails in sandbox per Wave 11 §31).
# Production runtime imports normally; this is a test-side workaround only.
_REPO_ROOT = Path(__file__).resolve().parents[1]
_SSRF_PATH = _REPO_ROOT / "api" / "security" / "ssrf_guard.py"
_spec = importlib.util.spec_from_file_location("ssrf_guard", _SSRF_PATH)
_ssrf_guard = importlib.util.module_from_spec(_spec)
sys.modules["ssrf_guard"] = _ssrf_guard
_spec.loader.exec_module(_ssrf_guard)

SSRFCheckResult = _ssrf_guard.SSRFCheckResult
approved_domains_count = _ssrf_guard.approved_domains_count
assert_safe_outbound = _ssrf_guard.assert_safe_outbound
check_url = _ssrf_guard.check_url

from auto_client_acquisition.email.deliverability_check import (
    DeliverabilityStatus,
    check_deliverability,
)


# ─────────────────────────────────────────────────────────────────────
# SSRF Guard (8 tests)
# ─────────────────────────────────────────────────────────────────────


def test_ssrf_blocks_localhost() -> None:
    """localhost / 127.0.0.1 / ::1 → blocked."""
    for host in ("https://localhost/x", "https://127.0.0.1/x", "https://[::1]/x"):
        result = check_url(host)
        assert result.allowed is False, f"{host} should be blocked"
        assert "localhost" in result.classification or "internal" in result.classification \
            or "blocked" in result.classification


def test_ssrf_blocks_aws_gcp_azure_metadata_ip() -> None:
    """169.254.169.254 (cloud metadata) → blocked."""
    result = check_url("https://169.254.169.254/latest/meta-data/")
    assert result.allowed is False
    assert result.classification in ("blocked_cloud_metadata", "blocked_link_local",
                                      "blocked_private_network", "blocked_internal")


def test_ssrf_blocks_rfc1918_private_networks() -> None:
    """RFC 1918 private ranges (10.*, 192.168.*, 172.16-31.*) → blocked."""
    private_ips = (
        "https://10.0.0.1/x",
        "https://192.168.1.1/x",
        "https://172.16.5.5/x",
        "https://172.31.255.255/x",
    )
    for url in private_ips:
        result = check_url(url)
        assert result.allowed is False, f"{url} should be blocked"


def test_ssrf_blocks_non_https_scheme() -> None:
    """http:// (not https://) → blocked unless localhost dev override."""
    result = check_url("http://api.dealix.me/x")
    assert result.allowed is False
    assert result.classification == "blocked_non_https"


def test_ssrf_blocks_non_approved_external_domain() -> None:
    """Random external domain not in allowlist → blocked."""
    result = check_url("https://random-untrusted-site.example.com/api/x")
    assert result.allowed is False
    assert result.classification == "blocked_non_approved_domain"


def test_ssrf_allows_approved_dealix_domains() -> None:
    """api.dealix.me + dealix.me → allowed."""
    for url in ("https://api.dealix.me/health", "https://dealix.me/", "https://www.dealix.me/x"):
        result = check_url(url)
        assert result.allowed is True, f"{url} should be allowed"
        assert result.classification == "approved_external"


def test_ssrf_allows_approved_third_party_apis() -> None:
    """Moyasar + Hunter + Anthropic + Langfuse → allowed."""
    for url in (
        "https://api.moyasar.com/v1/payments",
        "https://api.hunter.io/v2/email-finder",
        "https://api.anthropic.com/v1/messages",
        "https://cloud.langfuse.com/api/public/traces",
        "https://fatoora.zatca.gov.sa/api/v1/invoices",
    ):
        result = check_url(url)
        assert result.allowed is True, f"{url} should be allowed; got {result.reason}"


def test_assert_safe_outbound_raises_on_blocked() -> None:
    """assert_safe_outbound() raises RuntimeError when URL blocked."""
    with pytest.raises(RuntimeError, match="SSRF guard blocked"):
        assert_safe_outbound("https://10.0.0.1/x")


def test_approved_domains_count_non_empty() -> None:
    """Allowlist must be non-empty (sanity)."""
    assert approved_domains_count() >= 20  # we have ~30 approved domains


# ─────────────────────────────────────────────────────────────────────
# Email Deliverability (8 tests)
# ─────────────────────────────────────────────────────────────────────


def test_deliverability_no_dns_records_returns_founder_action() -> None:
    """When all 3 records None → founder_action_needed."""
    status = check_deliverability(domain="example.com")
    assert status.overall_status == "founder_action_needed"
    assert status.safe_to_send_marketing is False
    assert status.safe_to_send_transactional is False
    assert status.daily_cap_recommended == 0
    assert "SPF" in status.next_founder_action_en


def test_deliverability_spf_only_allows_low_volume_transactional() -> None:
    """SPF valid + DKIM/DMARC missing → low-volume transactional only."""
    status = check_deliverability(
        domain="example.com",
        spf_record="v=spf1 include:_spf.google.com ~all",
    )
    assert status.overall_status == "needs_dkim"
    assert status.safe_to_send_transactional is True
    assert status.safe_to_send_marketing is False
    assert status.daily_cap_recommended <= 100  # conservative


def test_deliverability_spf_dkim_no_dmarc_needs_dmarc() -> None:
    """SPF + DKIM valid + DMARC missing → needs_dmarc."""
    status = check_deliverability(
        domain="example.com",
        spf_record="v=spf1 include:_spf.google.com ~all",
        dkim_record="v=DKIM1; k=rsa; p=MIIBIjANBgkq...",
    )
    assert status.overall_status == "needs_dmarc"
    assert status.daily_cap_recommended <= 1000


def test_deliverability_all_3_records_no_unsubscribe_blocks_marketing() -> None:
    """All 3 DNS valid but no unsubscribe → marketing blocked."""
    status = check_deliverability(
        domain="example.com",
        spf_record="v=spf1 include:_spf.google.com ~all",
        dkim_record="v=DKIM1; k=rsa; p=MIIBIjANBgkq...",
        dmarc_record="v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com",
        one_click_unsubscribe_header_supported=False,
    )
    assert status.overall_status == "blocked_marketing"
    assert status.safe_to_send_transactional is True
    assert status.safe_to_send_marketing is False
    assert "List-Unsubscribe" in status.next_founder_action_en


def test_deliverability_all_3_records_plus_unsubscribe_ready_for_marketing() -> None:
    """All 3 DNS + unsubscribe → ready_for_marketing."""
    status = check_deliverability(
        domain="mail.dealix.me",
        spf_record="v=spf1 include:_spf.google.com ~all",
        dkim_record="v=DKIM1; k=rsa; p=MIIBIjANBgkq...",
        dmarc_record="v=DMARC1; p=quarantine; rua=mailto:dmarc@dealix.me",
        one_click_unsubscribe_header_supported=True,
    )
    assert status.overall_status == "ready_for_marketing"
    assert status.safe_to_send_marketing is True
    assert status.safe_to_send_transactional is True
    assert status.daily_cap_recommended >= 1000


def test_deliverability_invalid_spf_record_caught() -> None:
    """SPF without v=spf1 prefix → invalid."""
    status = check_deliverability(
        domain="example.com",
        spf_record="some random text",
    )
    assert status.spf.is_valid is False
    assert status.overall_status == "founder_action_needed"


def test_deliverability_dmarc_p_none_warning_present() -> None:
    """p=none DMARC is monitor-only → flagged in notes."""
    status = check_deliverability(
        domain="example.com",
        spf_record="v=spf1 include:_spf.google.com ~all",
        dkim_record="v=DKIM1; k=rsa; p=MIIBIjANBgkq...",
        dmarc_record="v=DMARC1; p=none; rua=mailto:dmarc@example.com",
    )
    assert status.dmarc.is_valid is True
    assert any("p=none" in n for n in status.dmarc.notes)


def test_deliverability_dkim_missing_p_invalid() -> None:
    """DKIM without p= (key) → invalid."""
    status = check_deliverability(
        domain="example.com",
        spf_record="v=spf1 include:_spf.google.com ~all",
        dkim_record="v=DKIM1; k=rsa; (no key)",
    )
    assert status.dkim.is_valid is False
    assert status.overall_status == "needs_dkim"


# ─────────────────────────────────────────────────────────────────────
# Total: 17 tests (9 SSRF + 8 Email)
# ─────────────────────────────────────────────────────────────────────
