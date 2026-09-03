"""Wave 12.5 §33.2.6 — Email Deliverability Check (SPF/DKIM/DMARC).

Validates that a sending domain has the required DNS records before
any outbound email goes out. Per Google sender requirements (May 2024+):
- SPF: required for all senders
- DKIM: required for senders >5K/day
- DMARC: required for senders >5K/day; recommended for all
- One-click unsubscribe: required for marketing emails
- Metrics circuit-breaker: pause external sending when measured sender-health rates cross policy thresholds

Hard rule: when DNS records are missing/incomplete, email status
returns ``founder_action_needed`` so the caller MUST hold the email
as draft_only until the founder configures DNS.

Source: Google sender requirements 2024+ + RFC 7208 (SPF) + RFC 6376
(DKIM) + RFC 7489 (DMARC).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


# Operational circuit-breaker thresholds. Google’s 0.30% spam value is a
# hard stop for this guard; the other limits are conservative Dealix stop
# rules and are not claims about a provider or statute.
_RATE_PAUSE_THRESHOLDS: dict[str, float] = {
    "bounce_rate": 0.05,
    "spam_rate": 0.003,
    "unsubscribe_rate": 0.02,
    "negative_reply_rate": 0.10,
}


@dataclass(frozen=True, slots=True)
class DNSRecord:
    """One DNS record (SPF / DKIM / DMARC) with parse status."""

    record_type: Literal["SPF", "DKIM", "DMARC"]
    domain: str
    found: bool
    raw_value: str = ""
    is_valid: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class DeliverabilityStatus:
    """Composite deliverability readiness for a sending domain."""

    domain: str
    spf: DNSRecord
    dkim: DNSRecord
    dmarc: DNSRecord
    one_click_unsubscribe_supported: bool
    daily_cap_recommended: int  # max recommended sends/day in current state
    overall_status: Literal[
        "ready_for_marketing",       # all 3 records valid + unsubscribe
        "ready_for_transactional",   # SPF only (low volume)
        "needs_dkim",                 # SPF OK, DKIM missing
        "needs_dmarc",                # SPF + DKIM OK, DMARC missing
        "founder_action_needed",     # SPF missing or invalid
        "blocked_marketing",         # Marketing blocked because requirements not met
        "metrics_pause",              # Sender-health metrics crossed a stop rule
    ]
    safe_to_send_marketing: bool
    safe_to_send_transactional: bool
    next_founder_action_ar: str
    next_founder_action_en: str
    metrics_blocked: bool = False
    metrics_blockers: tuple[str, ...] = field(default_factory=tuple)


def check_deliverability(
    *,
    domain: str,
    spf_record: str | None = None,
    dkim_record: str | None = None,
    dmarc_record: str | None = None,
    one_click_unsubscribe_header_supported: bool = False,
    bounce_rate: float | None = None,
    spam_rate: float | None = None,
    unsubscribe_rate: float | None = None,
    negative_reply_rate: float | None = None,
) -> DeliverabilityStatus:
    """Validate the 3 DNS records for a sending domain.

    Args:
        domain: The sending domain (e.g. ``mail.dealix.me``).
        spf_record: TXT record value at ``domain`` (None when not yet
            queried — use ``check_dns_for_domain()`` upstream to fetch).
        dkim_record: TXT record value at ``selector._domainkey.domain``.
        dmarc_record: TXT record value at ``_dmarc.domain``.
        one_click_unsubscribe_header_supported: Whether the email sender
            puts ``List-Unsubscribe`` + ``List-Unsubscribe-Post`` headers.

    Returns:
        DeliverabilityStatus with readiness + safe_to_send flags +
        next_founder_action.
    """
    metrics_blockers = _metric_blockers(
        bounce_rate=bounce_rate,
        spam_rate=spam_rate,
        unsubscribe_rate=unsubscribe_rate,
        negative_reply_rate=negative_reply_rate,
    )
    spf = _check_spf(domain, spf_record)
    dkim = _check_dkim(domain, dkim_record)
    dmarc = _check_dmarc(domain, dmarc_record)

    # Composite logic
    status: Literal[
        "ready_for_marketing", "ready_for_transactional",
        "needs_dkim", "needs_dmarc",
        "founder_action_needed", "blocked_marketing", "metrics_pause",
    ]
    safe_marketing = False
    safe_transactional = False
    daily_cap = 0
    action_ar = ""
    action_en = ""

    if not spf.is_valid:
        status = "founder_action_needed"
        action_ar = (
            f"أضف SPF record على {domain}: "
            f"v=spf1 include:_spf.google.com include:moyasar.com ~all"
        )
        action_en = (
            f"Add SPF record to {domain}: "
            f"v=spf1 include:_spf.google.com include:moyasar.com ~all"
        )
        daily_cap = 0
    elif not dkim.is_valid:
        status = "needs_dkim"
        action_ar = (
            f"أضف DKIM key على selector._domainkey.{domain} "
            f"(انسخ من Google Admin Console أو موفر الإيميل)"
        )
        action_en = (
            f"Add DKIM key at selector._domainkey.{domain} "
            f"(copy from Google Admin Console or email provider)"
        )
        # SPF only → safe for low-volume transactional
        safe_transactional = True
        daily_cap = 50  # conservative for SPF-only
    elif not dmarc.is_valid:
        status = "needs_dmarc"
        action_ar = (
            f"أضف DMARC record على _dmarc.{domain}: "
            f"v=DMARC1; p=quarantine; rua=mailto:dmarc@{domain}"
        )
        action_en = (
            f"Add DMARC record at _dmarc.{domain}: "
            f"v=DMARC1; p=quarantine; rua=mailto:dmarc@{domain}"
        )
        safe_transactional = True
        daily_cap = 500  # SPF + DKIM allows higher volume
    elif not one_click_unsubscribe_header_supported:
        # All 3 DNS records valid but no unsubscribe header
        status = "blocked_marketing"
        action_ar = (
            "أضف رؤوس List-Unsubscribe + List-Unsubscribe-Post "
            "لكل رسالة تسويقية (مطلوب من Google منذ 2024)"
        )
        action_en = (
            "Add List-Unsubscribe + List-Unsubscribe-Post headers "
            "to every marketing email (Google requirement since 2024)"
        )
        safe_transactional = True
        safe_marketing = False
        daily_cap = 5000
    else:
        # All 3 + unsubscribe → ready for both
        status = "ready_for_marketing"
        action_ar = "جاهز — راقب bounce rate (يجب أن يبقى تحت 5%)"
        action_en = "Ready — monitor bounce rate (must stay <5%)"
        safe_transactional = True
        safe_marketing = True
        daily_cap = 50000

    if metrics_blockers:
        status = "metrics_pause"
        safe_marketing = False
        safe_transactional = False
        daily_cap = 0
        joined = ", ".join(metrics_blockers)
        action_ar = f"تم إيقاف الإرسال مؤقتًا بسبب مؤشرات صحة المرسل: {joined}. راجع المصدر قبل أي إرسال."
        action_en = f"External sending is paused because sender-health metrics crossed a stop rule: {joined}. Review the source before any send."

    return DeliverabilityStatus(
        domain=domain,
        spf=spf, dkim=dkim, dmarc=dmarc,
        one_click_unsubscribe_supported=one_click_unsubscribe_header_supported,
        daily_cap_recommended=daily_cap,
        overall_status=status,
        safe_to_send_marketing=safe_marketing,
        safe_to_send_transactional=safe_transactional,
        next_founder_action_ar=action_ar,
        next_founder_action_en=action_en,
        metrics_blocked=bool(metrics_blockers),
        metrics_blockers=metrics_blockers,
    )


def _metric_blockers(
    *,
    bounce_rate: float | None,
    spam_rate: float | None,
    unsubscribe_rate: float | None,
    negative_reply_rate: float | None,
) -> tuple[str, ...]:
    values = {
        "bounce_rate": bounce_rate,
        "spam_rate": spam_rate,
        "unsubscribe_rate": unsubscribe_rate,
        "negative_reply_rate": negative_reply_rate,
    }
    blockers: list[str] = []
    for name, raw_value in values.items():
        if raw_value is None:
            continue
        if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
            raise ValueError(f"{name} must be a numeric rate between 0 and 1")
        value = float(raw_value)
        if not 0 <= value <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
        threshold = _RATE_PAUSE_THRESHOLDS[name]
        if value >= threshold:
            blockers.append(f"{name}>={threshold:.2%}")
    return tuple(blockers)


def _check_spf(domain: str, raw: str | None) -> DNSRecord:
    """SPF record at the apex domain."""
    if raw is None:
        return DNSRecord(
            record_type="SPF", domain=domain, found=False, raw_value="",
            is_valid=False, notes=("not_yet_queried",),
        )
    if not raw.strip():
        return DNSRecord(
            record_type="SPF", domain=domain, found=False, raw_value=raw,
            is_valid=False, notes=("empty_record",),
        )
    # SPF: must start with "v=spf1"
    if not raw.lower().strip().startswith("v=spf1"):
        return DNSRecord(
            record_type="SPF", domain=domain, found=True, raw_value=raw,
            is_valid=False, notes=("missing_v=spf1_prefix",),
        )
    # SPF: must have at least one "include:" or "ip4:"/"ip6:" mechanism
    has_mechanism = any(m in raw.lower() for m in ("include:", "ip4:", "ip6:", "a ", "mx ", " mx", "+all", "~all", "-all"))
    if not has_mechanism:
        return DNSRecord(
            record_type="SPF", domain=domain, found=True, raw_value=raw,
            is_valid=False, notes=("no_authorized_senders_listed",),
        )
    notes: list[str] = []
    if "+all" in raw:
        notes.append("warning_unsafe_+all_mechanism")
    return DNSRecord(
        record_type="SPF", domain=domain, found=True, raw_value=raw,
        is_valid=True, notes=tuple(notes) if notes else (),
    )


def _check_dkim(domain: str, raw: str | None) -> DNSRecord:
    """DKIM record at selector._domainkey.domain."""
    if raw is None:
        return DNSRecord(
            record_type="DKIM", domain=domain, found=False, raw_value="",
            is_valid=False, notes=("not_yet_queried",),
        )
    if not raw.strip():
        return DNSRecord(
            record_type="DKIM", domain=domain, found=False, raw_value=raw,
            is_valid=False, notes=("empty_record",),
        )
    # DKIM: must have v=DKIM1 + k=rsa + p=<key>
    raw_lower = raw.lower()
    has_version = "v=dkim1" in raw_lower
    has_key = "p=" in raw_lower
    if not (has_version and has_key):
        notes = []
        if not has_version:
            notes.append("missing_v=DKIM1")
        if not has_key:
            notes.append("missing_p=key")
        return DNSRecord(
            record_type="DKIM", domain=domain, found=True, raw_value=raw,
            is_valid=False, notes=tuple(notes),
        )
    return DNSRecord(
        record_type="DKIM", domain=domain, found=True, raw_value=raw,
        is_valid=True,
    )


def _check_dmarc(domain: str, raw: str | None) -> DNSRecord:
    """DMARC record at _dmarc.domain."""
    if raw is None:
        return DNSRecord(
            record_type="DMARC", domain=domain, found=False, raw_value="",
            is_valid=False, notes=("not_yet_queried",),
        )
    if not raw.strip():
        return DNSRecord(
            record_type="DMARC", domain=domain, found=False, raw_value=raw,
            is_valid=False, notes=("empty_record",),
        )
    raw_lower = raw.lower()
    if not raw_lower.startswith("v=dmarc1"):
        return DNSRecord(
            record_type="DMARC", domain=domain, found=True, raw_value=raw,
            is_valid=False, notes=("missing_v=DMARC1_prefix",),
        )
    # Must specify a policy (p=)
    if "p=" not in raw_lower:
        return DNSRecord(
            record_type="DMARC", domain=domain, found=True, raw_value=raw,
            is_valid=False, notes=("missing_policy_p=",),
        )
    notes: list[str] = []
    if "p=none" in raw_lower:
        notes.append("warning_p=none_is_monitor_only")
    return DNSRecord(
        record_type="DMARC", domain=domain, found=True, raw_value=raw,
        is_valid=True, notes=tuple(notes) if notes else (),
    )
