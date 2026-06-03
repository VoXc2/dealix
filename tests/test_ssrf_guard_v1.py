"""Wave 14 — SSRF (Server-Side Request Forgery) Guard tests.

Validates :func:`check_url` blocks the 7 dangerous host categories:
- localhost (127.*, ::1)
- private networks (RFC 1918: 10.*, 192.168.*, 172.16-31.*)
- link-local (169.254.*)
- cloud metadata IP (169.254.169.254)
- IPv6 internal (fe80:, fc00:, fd00:)
- .local / .internal hostnames
- non-https schemes (http://, ftp://, file://, gopher://)

Plus:
- Default-deny: random external domain → blocked_non_approved_domain
- Allowlist exact match: api.moyasar.com → approved_external
- Allowlist subdomain match: foo.api.sentry.io → approved_external

Hard rule (Article 4 + OWASP API7:2023): any URL the function marks
``allowed=True`` MUST be invocable from production without exfiltration
risk. Default deny.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest

# Sandbox bypass: load ssrf_guard.py directly without triggering
# api/security/__init__.py (which imports python-jose / cryptography
# that fails in this sandbox with _cffi_backend / pyo3 cascade).
# Production unaffected — this is purely a test-env shim.
# Register in sys.modules so @dataclass(slots=True) can resolve.
_MOD_NAME = "_ssrf_guard_isolated_wave14"
_SSRF_GUARD_PATH = pathlib.Path(__file__).resolve().parents[1] / "api" / "security" / "ssrf_guard.py"
_spec = importlib.util.spec_from_file_location(_MOD_NAME, _SSRF_GUARD_PATH)
assert _spec is not None and _spec.loader is not None
_ssrf_guard = importlib.util.module_from_spec(_spec)
sys.modules[_MOD_NAME] = _ssrf_guard
_spec.loader.exec_module(_ssrf_guard)

SSRFCheckResult = _ssrf_guard.SSRFCheckResult
assert_safe_outbound = _ssrf_guard.assert_safe_outbound
check_url = _ssrf_guard.check_url


# ─────────────────────────────────────────────────────────────────────
# Block patterns — 6 dangerous categories MUST be blocked
# ─────────────────────────────────────────────────────────────────────


def test_blocks_localhost_variants() -> None:
    """localhost / 127.* / 0.* → blocked_localhost."""
    for host in ("https://localhost/", "https://127.0.0.1/", "https://127.1.2.3/"):
        result = check_url(host)
        assert result.allowed is False, f"expected blocked: {host}"
        assert "localhost" in result.classification or "internal" in result.classification


def test_blocks_aws_gcp_azure_metadata_ip() -> None:
    """169.254.169.254 (cloud-instance metadata) → blocked_link_local
    OR blocked_cloud_metadata."""
    result = check_url("https://169.254.169.254/latest/meta-data/")
    assert result.allowed is False
    assert "metadata" in result.classification or "link_local" in result.classification


def test_blocks_rfc1918_private_networks() -> None:
    """10.* / 192.168.* / 172.16-31.* → blocked_private_network."""
    for host in (
        "https://10.0.0.1/", "https://192.168.1.1/",
        "https://172.16.0.1/", "https://172.31.255.255/",
    ):
        result = check_url(host)
        assert result.allowed is False, f"expected blocked: {host}"
        assert "private" in result.classification or "internal" in result.classification


def test_blocks_ipv6_loopback_and_link_local() -> None:
    """::1, fe80:, fc00:, fd00: → blocked_ipv6_internal or _internal."""
    # IPv6 must be wrapped in brackets in URLs
    for host in ("https://[::1]/", "https://[fe80::1]/", "https://[fc00::1]/"):
        result = check_url(host)
        # Either blocked by regex pattern or by ipaddress check
        assert result.allowed is False, f"expected blocked: {host}"


def test_blocks_dot_local_and_dot_internal_hostnames() -> None:
    """foo.local / bar.internal → blocked_internal."""
    for host in ("https://foo.local/", "https://bar.internal/"):
        result = check_url(host)
        assert result.allowed is False, f"expected blocked: {host}"


def test_blocks_non_https_schemes() -> None:
    """ftp://, file://, gopher://, http:// → blocked_non_https.

    HTTP is the most common SSRF abuse channel; non-https is rejected
    even for otherwise-approved domains.
    """
    for host in (
        "http://api.moyasar.com/charge",  # http even on approved domain
        "ftp://api.openai.com/data",
        "file:///etc/passwd",
        "gopher://localhost/",
    ):
        result = check_url(host)
        assert result.allowed is False, f"expected blocked non-https: {host}"


# ─────────────────────────────────────────────────────────────────────
# Allowlist — approved external domains MUST pass
# ─────────────────────────────────────────────────────────────────────


def test_allows_approved_external_domains_exact_match() -> None:
    """api.moyasar.com, api.openai.com → approved_external."""
    for host in (
        "https://api.moyasar.com/v1/payments",
        "https://api.openai.com/v1/chat/completions",
        "https://api.anthropic.com/v1/messages",
        "https://api.hunter.io/v2/domain-search",
        "https://cloud.langfuse.com/api/public/traces",
    ):
        result = check_url(host)
        assert result.allowed is True, (
            f"expected approved: {host} (got {result.classification})"
        )
        assert result.classification == "approved_external"


def test_allows_subdomain_of_approved_domain() -> None:
    """foo.dealix.me → approved_external via subdomain match."""
    result = check_url("https://foo.dealix.me/api/v1/health")
    assert result.allowed is True
    assert result.classification == "approved_external"


# ─────────────────────────────────────────────────────────────────────
# Default-deny + malformed URL
# ─────────────────────────────────────────────────────────────────────


def test_default_denies_random_external_domain() -> None:
    """evil-exfil.com → blocked_non_approved_domain (default-deny)."""
    result = check_url("https://evil-exfil.com/upload?data=secret")
    assert result.allowed is False
    assert result.classification == "blocked_non_approved_domain"


def test_malformed_url_returns_blocked_invalid_url() -> None:
    """Missing host or unparseable URL → blocked_invalid_url."""
    for url in ("", "https://", "not-a-url-at-all"):
        result = check_url(url)
        assert result.allowed is False, f"expected blocked: {url!r}"


# ─────────────────────────────────────────────────────────────────────
# assert_safe_outbound raises on block
# ─────────────────────────────────────────────────────────────────────


def test_assert_safe_outbound_raises_on_blocked() -> None:
    """The convenience helper raises RuntimeError on blocked URLs."""
    with pytest.raises(RuntimeError):
        assert_safe_outbound("https://169.254.169.254/latest/meta-data/")


def test_assert_safe_outbound_passes_on_approved() -> None:
    """Approved URLs return None (no raise)."""
    # Should not raise
    assert_safe_outbound("https://api.moyasar.com/v1/payments")
