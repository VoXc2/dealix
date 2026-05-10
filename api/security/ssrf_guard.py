"""Wave 12.5 §33.2.6 — SSRF (Server-Side Request Forgery) Guard.

Blocks outbound HTTP requests to internal/private/cloud-metadata IP
ranges that an attacker could use to exfiltrate data from internal
services. Per OWASP API Top 10 2023 — API7:2023 Server Side Request
Forgery.

Hard rule: every outbound HTTP call from Dealix code MUST pass through
``check_url(url)`` before invoking httpx. Failure to call this function
is itself a code-review issue.

Allowlist approach: only domains in ``_APPROVED_EXTERNAL_DOMAINS`` are
permitted unconditionally. All others are checked against the blocklist
of internal/private/metadata ranges.

Sources:
- OWASP API7:2023 SSRF
  https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/
- AWS IMDSv2 metadata IP (169.254.169.254)
- GCP metadata IP (169.254.169.254)
- Azure IMDS (169.254.169.254)
"""
from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlparse

# Approved external domains — these bypass blocklist checks (still require https).
# When adding a new external integration, add the domain here AND document
# why in a code review.
_APPROVED_EXTERNAL_DOMAINS: frozenset[str] = frozenset({
    # Payment + invoicing
    "moyasar.com", "api.moyasar.com",
    "zatca.gov.sa", "fatoora.zatca.gov.sa",
    # Enrichment
    "api.hunter.io", "hunter.io",
    # Communication
    "graph.facebook.com",  # Meta WhatsApp Business API
    "api.resend.com",       # Email
    "smtp.gmail.com", "googleapis.com", "www.googleapis.com",
    "oauth2.googleapis.com",
    # LLM providers
    "api.openai.com", "api.anthropic.com",
    "generativelanguage.googleapis.com",  # Gemini
    "api.groq.com", "api.deepseek.com",
    "open.bigmodel.cn",  # Zhipu / GLM
    # Observability
    "cloud.langfuse.com",
    "ingest.sentry.io", "*.ingest.sentry.io",
    "us.posthog.com", "eu.posthog.com",
    # Calendars
    "api.cal.com", "calendly.com", "api.calendly.com",
    # Dealix self
    "api.dealix.me", "dealix.me", "www.dealix.me",
})

# Domains/IPs that are NEVER allowed — even with explicit override.
# These cover: localhost variants, private networks (RFC 1918), link-local
# (cloud metadata), and IPv6 equivalents.
_BLOCKED_HOST_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"^localhost$", re.IGNORECASE),
    re.compile(r"^127\."),
    re.compile(r"^0\."),
    re.compile(r"^169\.254\."),     # link-local + cloud metadata
    re.compile(r"^10\."),            # RFC 1918 private
    re.compile(r"^192\.168\."),     # RFC 1918 private
    re.compile(r"^172\.(1[6-9]|2[0-9]|3[01])\."),  # RFC 1918 private 172.16-31
    re.compile(r"^::1$"),            # IPv6 localhost
    re.compile(r"^fe80:", re.IGNORECASE),  # IPv6 link-local
    re.compile(r"^fc00:", re.IGNORECASE),  # IPv6 ULA
    re.compile(r"^fd00:", re.IGNORECASE),  # IPv6 ULA
    re.compile(r"\.local$", re.IGNORECASE),
    re.compile(r"\.internal$", re.IGNORECASE),
)


@dataclass(frozen=True, slots=True)
class SSRFCheckResult:
    """Outcome of an SSRF guard check.

    When ``allowed=False``, ``reason`` explains why and the caller MUST
    abort the outbound request.
    """

    allowed: bool
    reason: str
    classification: Literal[
        "approved_external",
        "blocked_internal",
        "blocked_private_network",
        "blocked_link_local",
        "blocked_cloud_metadata",
        "blocked_localhost",
        "blocked_ipv6_internal",
        "blocked_invalid_url",
        "blocked_non_https",
        "blocked_non_approved_domain",
    ]
    parsed_host: str
    parsed_scheme: str


def check_url(
    url: str,
    *,
    allow_http_for_localhost_dev: bool = False,
) -> SSRFCheckResult:
    """Check whether an outbound URL is safe to invoke.

    Hard rules (Article 4):
    - Scheme MUST be https (only exception: explicit dev override for
      localhost — never use in production)
    - Host MUST NOT match any blocklisted pattern
    - Host MUST be in approved external domains (or its TLD)

    Args:
        url: The URL to check.
        allow_http_for_localhost_dev: Set True ONLY in tests (default
            False — production never allows HTTP).

    Returns:
        SSRFCheckResult — caller checks ``allowed`` before httpx call.
    """
    # 1. Parse URL — reject malformed
    try:
        parsed = urlparse(url)
    except (ValueError, AttributeError):
        return SSRFCheckResult(
            allowed=False, reason="malformed url",
            classification="blocked_invalid_url",
            parsed_host="", parsed_scheme="",
        )

    scheme = (parsed.scheme or "").lower()
    host = (parsed.hostname or "").lower()

    if not host or not scheme:
        return SSRFCheckResult(
            allowed=False, reason="missing host or scheme",
            classification="blocked_invalid_url",
            parsed_host=host, parsed_scheme=scheme,
        )

    # 2. Scheme check
    if scheme != "https":
        if scheme == "http" and allow_http_for_localhost_dev and host in ("localhost", "127.0.0.1"):
            # Test/dev exception only — never reachable in production
            pass
        else:
            return SSRFCheckResult(
                allowed=False, reason=f"scheme {scheme!r} not allowed (https required)",
                classification="blocked_non_https",
                parsed_host=host, parsed_scheme=scheme,
            )

    # 3. Block-pattern check (always wins, even over allowlist)
    for pat in _BLOCKED_HOST_PATTERNS:
        if pat.search(host):
            classification = _classify_block(host)
            return SSRFCheckResult(
                allowed=False, reason=f"host {host!r} matches blocked pattern {pat.pattern!r}",
                classification=classification,
                parsed_host=host, parsed_scheme=scheme,
            )

    # 4. IP-address-as-host check (catches numeric IPs that bypassed regex)
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return SSRFCheckResult(
                allowed=False, reason=f"IP {host} is private/loopback/link-local",
                classification="blocked_private_network",
                parsed_host=host, parsed_scheme=scheme,
            )
    except ValueError:
        # Not an IP literal; fine to continue
        pass

    # 5. Allowlist check — exact match or known TLD wildcards
    if _is_approved_domain(host):
        return SSRFCheckResult(
            allowed=True, reason="approved external domain",
            classification="approved_external",
            parsed_host=host, parsed_scheme=scheme,
        )

    # 6. Default deny — every outbound destination must be explicit
    return SSRFCheckResult(
        allowed=False,
        reason=f"host {host!r} not in approved external domains list",
        classification="blocked_non_approved_domain",
        parsed_host=host, parsed_scheme=scheme,
    )


def _classify_block(host: str) -> Literal[
    "blocked_internal", "blocked_private_network", "blocked_link_local",
    "blocked_cloud_metadata", "blocked_localhost", "blocked_ipv6_internal",
]:
    """Sub-classify the blocked reason for audit clarity."""
    if host in ("localhost", "127.0.0.1") or host.startswith("127."):
        return "blocked_localhost"
    if host == "169.254.169.254":
        return "blocked_cloud_metadata"
    if host.startswith("169.254."):
        return "blocked_link_local"
    if host.startswith("10.") or host.startswith("192.168.") or "172." in host:
        return "blocked_private_network"
    if host == "::1" or host.startswith("fe80:") or host.startswith("fc00:") or host.startswith("fd00:"):
        return "blocked_ipv6_internal"
    return "blocked_internal"


def _is_approved_domain(host: str) -> bool:
    """Check exact domain match + handle wildcard TLDs (*.ingest.sentry.io)."""
    if host in _APPROVED_EXTERNAL_DOMAINS:
        return True
    # Wildcard TLD support — check each entry that starts with '*.'
    for entry in _APPROVED_EXTERNAL_DOMAINS:
        if entry.startswith("*."):
            suffix = entry[2:]  # drop the *.
            if host.endswith(f".{suffix}") or host == suffix:
                return True
    # Also check if host is a subdomain of an approved domain
    for entry in _APPROVED_EXTERNAL_DOMAINS:
        if not entry.startswith("*.") and host.endswith(f".{entry}"):
            return True
    return False


def assert_safe_outbound(url: str) -> None:
    """Convenience wrapper — raises ``RuntimeError`` if URL is blocked.

    Use this when you want SSRF protection without manually checking
    the result. Article 4 — every outbound call should call this OR
    check_url() explicitly.
    """
    result = check_url(url)
    if not result.allowed:
        raise RuntimeError(
            f"SSRF guard blocked outbound request: "
            f"url={url!r} reason={result.reason!r} "
            f"classification={result.classification!r}"
        )


def approved_domains_count() -> int:
    """For tests + verifier — confirms the allowlist is non-empty."""
    return len(_APPROVED_EXTERNAL_DOMAINS)
