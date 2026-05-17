"""Affiliate / Partner Commission Machine — persistence layer.

External affiliates and partners (consultants, creators, agencies, CRM/AI
implementers) apply, get scored, receive a referral link, submit leads, and
earn CASH commissions — paid only after the referred customer's invoice is
paid, with a 30-day clawback window on refunds.

This is DISTINCT from the customer-referral program in
`referral_store.py` (an existing paying tenant referring a prospect for
NON-CASH subscription credit). New tables, new code prefix (`APT-`), new
store. Nothing here touches `referral_store.py`.

JSONL-backed, mirroring the `referral_store.py` pattern: dataclasses,
`_resolve()` path helpers, a process lock, `_append`/`_read_all`/`_rewrite`,
and `mirror_append` to the operational stream mirror. Designed to swap to
Postgres (see `db/migrations/013_affiliate_program.sql`) with no API change.

Doctrine honored:
  - No PII in storage: emails are hashed, never stored raw.
  - No unverified outcomes: a commission is gated strictly on a recorded
    `invoice_paid` event — never on a projection or promise.
  - Ledger trail: every mutation appends to JSONL + the stream mirror.
  - Approval gate: a payout settles only `approved` commissions.

Tables modelled:
  affiliate_partners          → AffiliatePartner
  affiliate_partner_links     → PartnerLink
  affiliate_referrals         → AffiliateReferral
  affiliate_commissions       → Commission
  affiliate_payouts           → Payout
  affiliate_approved_assets   → ApprovedAsset
  affiliate_compliance_events → ComplianceEvent
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4

# ── Program parameters ───────────────────────────────────────────────

# Commission percentage of the first paid deal, by partner tier.
# tier4 (implementation partner) is a negotiated handoff fee, not a pct.
TIER_PCT: dict[str, int] = {
    "tier1": 5,    # Affiliate Lead — 5% of first paid Diagnostic
    "tier2": 10,   # Qualified Referral — 10% of first paid deal
    "tier3": 15,   # Strategic Partner — 15% (founder may raise to 20)
    "tier4": 0,    # Implementation Partner — flat negotiated handoff fee
}
TIER3_MAX_PCT = 20
CLAWBACK_WINDOW_DAYS = 30


class PartnerStatus(StrEnum):
    SCORED = "scored"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class AffiliateReferralStatus(StrEnum):
    SUBMITTED = "submitted"
    QUALIFIED = "qualified"
    REJECTED = "rejected"
    INVOICE_PAID = "invoice_paid"
    COMMISSIONED = "commissioned"
    CLAWED_BACK = "clawed_back"


class CommissionStatus(StrEnum):
    CALCULATED = "calculated"
    APPROVED = "approved"
    PAID = "paid"
    CLAWED_BACK = "clawed_back"


class PayoutStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"


# ── Storage paths ────────────────────────────────────────────────────

_PATH_DEFAULTS: dict[str, str] = {
    "DEALIX_AFFILIATE_PARTNERS_PATH": "var/affiliate-partners.jsonl",
    "DEALIX_AFFILIATE_LINKS_PATH": "var/affiliate-links.jsonl",
    "DEALIX_AFFILIATE_REFERRALS_PATH": "var/affiliate-referrals.jsonl",
    "DEALIX_AFFILIATE_COMMISSIONS_PATH": "var/affiliate-commissions.jsonl",
    "DEALIX_AFFILIATE_PAYOUTS_PATH": "var/affiliate-payouts.jsonl",
    "DEALIX_AFFILIATE_ASSETS_PATH": "var/affiliate-approved-assets.jsonl",
    "DEALIX_AFFILIATE_COMPLIANCE_PATH": "var/affiliate-compliance-events.jsonl",
}

_lock = threading.Lock()


def _resolve(env_var: str) -> Path:
    p = Path(os.environ.get(env_var, _PATH_DEFAULTS[env_var]))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _partners_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_PARTNERS_PATH")


def _links_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_LINKS_PATH")


def _referrals_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_REFERRALS_PATH")


def _commissions_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_COMMISSIONS_PATH")


def _payouts_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_PAYOUTS_PATH")


def _assets_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_ASSETS_PATH")


def _compliance_path() -> Path:
    return _resolve("DEALIX_AFFILIATE_COMPLIANCE_PATH")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_email(email: str) -> str:
    """PII-safe: store only a short hash, never the raw address."""
    return hashlib.sha256((email or "").strip().lower().encode("utf-8")).hexdigest()[:16]


def _generate_link_code(partner_id: str) -> str:
    """APT-XXXXXXXX — distinct prefix from the customer-referral REF- codes."""
    seed = hashlib.sha256(
        (partner_id + secrets.token_hex(8)).encode("utf-8")
    ).hexdigest()[:8].upper()
    return f"APT-{seed}"


# ── Dataclasses ──────────────────────────────────────────────────────


@dataclass
class AffiliatePartner:
    partner_id: str = field(default_factory=lambda: f"apt_{uuid4().hex[:12]}")
    display_name: str = ""
    email_hash: str = ""
    partner_category: str = "other"
    audience_type: str = ""
    region: str = ""
    score: int = 0
    score_breakdown: dict[str, int] = field(default_factory=dict)
    tier: str = ""
    status: str = PartnerStatus.SCORED.value
    disclosure_accepted: bool = False
    plan_text: str = ""
    rejected_reason: str = ""
    created_at: str = field(default_factory=_now)
    scored_at: str = field(default_factory=_now)
    approved_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PartnerLink:
    code: str = ""
    partner_id: str = ""
    tier: str = ""
    is_revoked: bool = False
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AffiliateReferral:
    affiliate_referral_id: str = field(
        default_factory=lambda: f"afr_{uuid4().hex[:12]}"
    )
    code: str = ""
    partner_id: str = ""
    lead_company: str = ""
    lead_email_hash: str = ""
    status: str = AffiliateReferralStatus.SUBMITTED.value
    qualified: bool = False
    disclosure_present: bool = False
    decline_reason: str = ""
    invoice_id: str = ""
    deal_amount_sar: int = 0
    created_at: str = field(default_factory=_now)
    qualified_at: str = ""
    invoice_paid_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Commission:
    commission_id: str = field(
        default_factory=lambda: f"cmm_{uuid4().hex[:12]}"
    )
    affiliate_referral_id: str = ""
    partner_id: str = ""
    tier: str = ""
    pct: int = 0
    base_amount_sar: int = 0
    commission_sar: int = 0
    status: str = CommissionStatus.CALCULATED.value
    clawback_deadline: str = ""
    clawback_reason: str = ""
    calculated_at: str = field(default_factory=_now)
    approved_at: str = ""
    payout_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Payout:
    payout_id: str = field(default_factory=lambda: f"apo_{uuid4().hex[:12]}")
    partner_id: str = ""
    commission_ids: list[str] = field(default_factory=list)
    total_sar: int = 0
    method: str = ""
    reference: str = ""
    status: str = PayoutStatus.PENDING.value
    created_at: str = field(default_factory=_now)
    paid_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ApprovedAsset:
    asset_id: str = field(default_factory=lambda: f"ast_{uuid4().hex[:10]}")
    kind: str = "post"
    lang: str = "en"
    body: str = ""
    is_active: bool = True
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComplianceEvent:
    event_id: str = field(default_factory=lambda: f"cev_{uuid4().hex[:10]}")
    partner_id: str = ""
    event_type: str = ""
    severity: str = "low"
    detail: str = ""
    created_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Persistence helpers ──────────────────────────────────────────────


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _append(path: Path, payload: dict[str, Any], *, stream_id: str, event_id: str) -> None:
    _ensure_dir(path)
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    try:
        from auto_client_acquisition.persistence.operational_stream_mirror import (
            mirror_append,
        )

        mirror_append(stream_id=stream_id, payload=payload, event_id=event_id or None)
    except Exception:  # noqa: BLE001 — the JSONL write is the source of truth
        pass


def _read_all(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with _lock:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:  # noqa: BLE001
                    continue
    return out


def _rewrite(path: Path, items: list[dict[str, Any]]) -> None:
    _ensure_dir(path)
    with _lock:
        path.write_text(
            "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
            + ("\n" if items else ""),
            encoding="utf-8",
        )


# ── Partner scoring ──────────────────────────────────────────────────

# Founder-defined additive signed weights (see Growth Machine vision §7).
_SCORE_WEIGHTS: dict[str, int] = {
    "audience_is_b2b": 4,
    "audience_is_gcc": 3,
    "is_consultant_operator": 3,
    "has_prior_referrals": 2,
    "content_quality_good": 2,
    "trusted_brand": 2,
    "spam_history": -5,
    "fake_audience_suspected": -4,
    "no_disclosure": -3,
    "vague_plan": -3,
}


def score_partner(
    *,
    audience_is_b2b: bool = False,
    audience_is_gcc: bool = False,
    is_consultant_operator: bool = False,
    has_prior_referrals: bool = False,
    content_quality_good: bool = False,
    trusted_brand: bool = False,
    spam_history: bool = False,
    fake_audience_suspected: bool = False,
    disclosure_accepted: bool = False,
    plan_is_vague: bool = False,
) -> tuple[int, dict[str, int]]:
    """Score an external partner application. Returns (score, breakdown).

    This is intentionally distinct from `partnership_os.compute_fit_score`,
    which scores strategic-partner *fit* on a different 0-100 scale. The
    affiliate program uses the founder's signed additive model.
    """
    signals = {
        "audience_is_b2b": audience_is_b2b,
        "audience_is_gcc": audience_is_gcc,
        "is_consultant_operator": is_consultant_operator,
        "has_prior_referrals": has_prior_referrals,
        "content_quality_good": content_quality_good,
        "trusted_brand": trusted_brand,
        "spam_history": spam_history,
        "fake_audience_suspected": fake_audience_suspected,
        "no_disclosure": not disclosure_accepted,
        "vague_plan": plan_is_vague,
    }
    breakdown = {
        key: _SCORE_WEIGHTS[key] for key, active in signals.items() if active
    }
    return sum(breakdown.values()), breakdown


def tier_from_score(score: int) -> str:
    """Recommended tier from score. Empty string ⇒ recommend rejection."""
    if score >= 10:
        return "tier3"
    if score >= 6:
        return "tier2"
    if score >= 2:
        return "tier1"
    return ""


# ── Partner API ──────────────────────────────────────────────────────


def apply_partner(
    *,
    display_name: str,
    email: str = "",
    partner_category: str = "other",
    audience_type: str = "",
    region: str = "",
    plan_text: str = "",
    disclosure_accepted: bool = False,
    score_signals: dict[str, bool] | None = None,
) -> AffiliatePartner:
    """Record a partner application, score it, and persist as `scored`."""
    if not display_name.strip():
        raise ValueError("display_name is required")
    signals = dict(score_signals or {})
    plan_is_vague = len(plan_text.strip()) < 40
    score, breakdown = score_partner(
        audience_is_b2b=signals.get("audience_is_b2b", False),
        audience_is_gcc=signals.get("audience_is_gcc", False),
        is_consultant_operator=signals.get("is_consultant_operator", False),
        has_prior_referrals=signals.get("has_prior_referrals", False),
        content_quality_good=signals.get("content_quality_good", False),
        trusted_brand=signals.get("trusted_brand", False),
        spam_history=signals.get("spam_history", False),
        fake_audience_suspected=signals.get("fake_audience_suspected", False),
        disclosure_accepted=disclosure_accepted,
        plan_is_vague=plan_is_vague,
    )
    partner = AffiliatePartner(
        display_name=display_name.strip(),
        email_hash=_hash_email(email),
        partner_category=partner_category,
        audience_type=audience_type,
        region=region,
        score=score,
        score_breakdown=breakdown,
        tier=tier_from_score(score),
        status=PartnerStatus.SCORED.value,
        disclosure_accepted=disclosure_accepted,
        plan_text=plan_text.strip()[:2000],
    )
    _append(
        _partners_path(),
        partner.to_dict(),
        stream_id="affiliate_store_partners",
        event_id=partner.partner_id,
    )
    return partner


def get_partner(partner_id: str) -> AffiliatePartner | None:
    for row in _read_all(_partners_path()):
        if row.get("partner_id") == partner_id:
            return AffiliatePartner(**row)
    return None


def list_partners(*, status: str | None = None) -> list[AffiliatePartner]:
    out: list[AffiliatePartner] = []
    for row in _read_all(_partners_path()):
        if status and row.get("status") != status:
            continue
        out.append(AffiliatePartner(**row))
    return out


def _update_partner(partner_id: str, mutate: Any) -> AffiliatePartner | None:
    rows = _read_all(_partners_path())
    updated: AffiliatePartner | None = None
    for row in rows:
        if row.get("partner_id") == partner_id:
            mutate(row)
            updated = AffiliatePartner(**row)
            break
    if updated:
        _rewrite(_partners_path(), rows)
    return updated


def approve_partner(
    *, partner_id: str, tier: str | None = None
) -> tuple[AffiliatePartner, PartnerLink] | None:
    """Admin gate: approve a partner and issue their referral link."""
    partner = get_partner(partner_id)
    if partner is None or partner.status == PartnerStatus.APPROVED.value:
        return None
    final_tier = tier or partner.tier or "tier1"
    if final_tier not in TIER_PCT:
        raise ValueError(f"invalid tier: {final_tier}")

    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = PartnerStatus.APPROVED.value
        row["tier"] = final_tier
        row["approved_at"] = _now()

    updated = _update_partner(partner_id, _mutate)
    if updated is None:
        return None
    link = PartnerLink(
        code=_generate_link_code(partner_id),
        partner_id=partner_id,
        tier=final_tier,
    )
    _append(
        _links_path(),
        link.to_dict(),
        stream_id="affiliate_store_links",
        event_id=link.code,
    )
    return updated, link


def reject_partner(*, partner_id: str, reason: str) -> AffiliatePartner | None:
    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = PartnerStatus.REJECTED.value
        row["rejected_reason"] = reason[:256]

    return _update_partner(partner_id, _mutate)


def suspend_partner(*, partner_id: str, reason: str) -> AffiliatePartner | None:
    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = PartnerStatus.SUSPENDED.value
        row["rejected_reason"] = reason[:256]

    return _update_partner(partner_id, _mutate)


def get_link(code: str) -> PartnerLink | None:
    code = (code or "").strip().upper()
    for row in _read_all(_links_path()):
        if row.get("code") == code and not row.get("is_revoked", False):
            return PartnerLink(**row)
    return None


def list_links(*, partner_id: str) -> list[PartnerLink]:
    return [
        PartnerLink(**r)
        for r in _read_all(_links_path())
        if r.get("partner_id") == partner_id
    ]


# ── Lead / referral API ──────────────────────────────────────────────


def submit_referral(
    *,
    code: str,
    lead_company: str,
    lead_email: str = "",
) -> AffiliateReferral:
    """Partner submits a lead via their link code. Idempotent on
    (code, lead_email_hash). Rejects suspended partners and self-referrals."""
    if not lead_company.strip():
        raise ValueError("lead_company is required")
    link = get_link(code)
    if link is None:
        raise ValueError(f"invalid or revoked code: {code}")
    partner = get_partner(link.partner_id)
    if partner is None or partner.status != PartnerStatus.APPROVED.value:
        raise ValueError("partner not in good standing")

    lead_hash = _hash_email(lead_email)
    if lead_email and lead_hash == partner.email_hash:
        log_compliance_event(
            partner_id=partner.partner_id,
            event_type="self_referral",
            severity="high",
            detail="lead email matches partner email",
        )
        raise ValueError("self-referral not allowed")

    # Idempotency / duplicate-lead guard.
    for row in _read_all(_referrals_path()):
        if row.get("code") == link.code and row.get("lead_email_hash") == lead_hash:
            log_compliance_event(
                partner_id=partner.partner_id,
                event_type="duplicate_lead",
                severity="medium",
                detail=f"duplicate submission for company {lead_company.strip()[:80]}",
            )
            return AffiliateReferral(**row)

    referral = AffiliateReferral(
        code=link.code,
        partner_id=partner.partner_id,
        lead_company=lead_company.strip()[:255],
        lead_email_hash=lead_hash,
        status=AffiliateReferralStatus.SUBMITTED.value,
    )
    _append(
        _referrals_path(),
        referral.to_dict(),
        stream_id="affiliate_store_referrals",
        event_id=referral.affiliate_referral_id,
    )
    return referral


def get_referral(affiliate_referral_id: str) -> AffiliateReferral | None:
    for row in _read_all(_referrals_path()):
        if row.get("affiliate_referral_id") == affiliate_referral_id:
            return AffiliateReferral(**row)
    return None


def list_referrals(*, partner_id: str | None = None) -> list[AffiliateReferral]:
    out: list[AffiliateReferral] = []
    for row in _read_all(_referrals_path()):
        if partner_id and row.get("partner_id") != partner_id:
            continue
        out.append(AffiliateReferral(**row))
    return out


def _update_referral(affiliate_referral_id: str, mutate: Any) -> AffiliateReferral | None:
    rows = _read_all(_referrals_path())
    updated: AffiliateReferral | None = None
    for row in rows:
        if row.get("affiliate_referral_id") == affiliate_referral_id:
            mutate(row)
            updated = AffiliateReferral(**row)
            break
    if updated:
        _rewrite(_referrals_path(), rows)
    return updated


def qualify_referral(
    *,
    affiliate_referral_id: str,
    disclosure_present: bool,
) -> AffiliateReferral | None:
    """Admin marks a lead qualified. `disclosure_present` records whether the
    partner included the required affiliate disclosure when promoting."""
    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = AffiliateReferralStatus.QUALIFIED.value
        row["qualified"] = True
        row["disclosure_present"] = bool(disclosure_present)
        row["qualified_at"] = _now()

    return _update_referral(affiliate_referral_id, _mutate)


def reject_referral(
    *, affiliate_referral_id: str, reason: str
) -> AffiliateReferral | None:
    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = AffiliateReferralStatus.REJECTED.value
        row["decline_reason"] = reason[:256]

    return _update_referral(affiliate_referral_id, _mutate)


def mark_invoice_paid(
    *,
    affiliate_referral_id: str,
    invoice_id: str,
    deal_amount_sar: int,
) -> AffiliateReferral | None:
    """The ONLY trusted signal that a referred deal is paid. A commission
    cannot be calculated until a referral reaches this state."""
    referral = get_referral(affiliate_referral_id)
    if referral is None or referral.status != AffiliateReferralStatus.QUALIFIED.value:
        return None
    if deal_amount_sar <= 0:
        raise ValueError("deal_amount_sar must be positive")

    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = AffiliateReferralStatus.INVOICE_PAID.value
        row["invoice_id"] = invoice_id
        row["deal_amount_sar"] = int(deal_amount_sar)
        row["invoice_paid_at"] = _now()

    return _update_referral(affiliate_referral_id, _mutate)


# ── Commission API ───────────────────────────────────────────────────


def calculate_commission(
    *,
    affiliate_referral_id: str,
    pct_override: int | None = None,
    flat_fee_sar: int | None = None,
) -> Commission:
    """Calculate a commission for a paid referral. Hard gates:
      - referral must be in `invoice_paid`
      - referral must be qualified and have disclosure present
      - partner must be approved (not suspended)
      - no commission may already exist for this referral
    """
    referral = get_referral(affiliate_referral_id)
    if referral is None:
        raise ValueError("referral not found")

    for row in _read_all(_commissions_path()):
        if row.get("affiliate_referral_id") == affiliate_referral_id:
            raise ValueError("commission already exists for this referral")

    if referral.status != AffiliateReferralStatus.INVOICE_PAID.value:
        raise ValueError("commission requires a recorded invoice_paid event")
    if not referral.qualified:
        raise ValueError("referral is not qualified")
    if not referral.disclosure_present:
        raise ValueError("affiliate disclosure was not present — commission blocked")

    partner = get_partner(referral.partner_id)
    if partner is None or partner.status != PartnerStatus.APPROVED.value:
        raise ValueError("partner not in good standing")

    tier = partner.tier or "tier1"
    if tier == "tier4":
        if flat_fee_sar is None or flat_fee_sar <= 0:
            raise ValueError("tier4 requires an explicit flat_fee_sar")
        pct = 0
        commission_sar = int(flat_fee_sar)
    else:
        pct = TIER_PCT.get(tier, 0) if pct_override is None else int(pct_override)
        if tier == "tier3" and pct > TIER3_MAX_PCT:
            raise ValueError(f"tier3 commission cannot exceed {TIER3_MAX_PCT}%")
        if pct < 0 or pct > TIER3_MAX_PCT:
            raise ValueError("commission pct out of allowed range")
        commission_sar = referral.deal_amount_sar * pct // 100

    paid_at = datetime.fromisoformat(referral.invoice_paid_at)
    deadline = (paid_at + timedelta(days=CLAWBACK_WINDOW_DAYS)).isoformat()

    commission = Commission(
        affiliate_referral_id=affiliate_referral_id,
        partner_id=referral.partner_id,
        tier=tier,
        pct=pct,
        base_amount_sar=referral.deal_amount_sar,
        commission_sar=commission_sar,
        status=CommissionStatus.CALCULATED.value,
        clawback_deadline=deadline,
    )
    _append(
        _commissions_path(),
        commission.to_dict(),
        stream_id="affiliate_store_commissions",
        event_id=commission.commission_id,
    )
    _update_referral(
        affiliate_referral_id,
        lambda row: row.__setitem__("status", AffiliateReferralStatus.COMMISSIONED.value),
    )
    return commission


def get_commission(commission_id: str) -> Commission | None:
    for row in _read_all(_commissions_path()):
        if row.get("commission_id") == commission_id:
            return Commission(**row)
    return None


def list_commissions(*, partner_id: str | None = None) -> list[Commission]:
    out: list[Commission] = []
    for row in _read_all(_commissions_path()):
        if partner_id and row.get("partner_id") != partner_id:
            continue
        out.append(Commission(**row))
    return out


def _update_commission(commission_id: str, mutate: Any) -> Commission | None:
    rows = _read_all(_commissions_path())
    updated: Commission | None = None
    for row in rows:
        if row.get("commission_id") == commission_id:
            mutate(row)
            updated = Commission(**row)
            break
    if updated:
        _rewrite(_commissions_path(), rows)
    return updated


def approve_commission(*, commission_id: str) -> Commission | None:
    """Admin approval gate — a payout may only settle approved commissions."""
    commission = get_commission(commission_id)
    if commission is None or commission.status != CommissionStatus.CALCULATED.value:
        return None

    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = CommissionStatus.APPROVED.value
        row["approved_at"] = _now()

    return _update_commission(commission_id, _mutate)


def clawback_commission(*, commission_id: str, reason: str) -> Commission | None:
    """Reverse a commission after a refund. Allowed only inside the 30-day
    clawback window and only before the commission has been paid out."""
    commission = get_commission(commission_id)
    if commission is None:
        return None
    if commission.status in (
        CommissionStatus.PAID.value,
        CommissionStatus.CLAWED_BACK.value,
    ):
        raise ValueError("commission already paid or clawed back")
    if commission.clawback_deadline:
        deadline = datetime.fromisoformat(commission.clawback_deadline)
        if datetime.now(timezone.utc) > deadline:
            raise ValueError("clawback window (30 days) has closed")

    def _mutate(row: dict[str, Any]) -> None:
        row["status"] = CommissionStatus.CLAWED_BACK.value
        row["clawback_reason"] = reason[:256]

    updated = _update_commission(commission_id, _mutate)
    if updated:
        _update_referral(
            updated.affiliate_referral_id,
            lambda row: row.__setitem__(
                "status", AffiliateReferralStatus.CLAWED_BACK.value
            ),
        )
    return updated


# ── Payout API ───────────────────────────────────────────────────────


def mark_payout_paid(
    *,
    partner_id: str,
    commission_ids: list[str],
    method: str = "bank_transfer",
    reference: str = "",
) -> Payout:
    """Settle a payout. Only `approved` commissions for the named partner are
    eligible — calculated-but-unapproved commissions are rejected."""
    if not commission_ids:
        raise ValueError("commission_ids is required")
    total = 0
    eligible: list[Commission] = []
    for cid in commission_ids:
        commission = get_commission(cid)
        if commission is None:
            raise ValueError(f"commission not found: {cid}")
        if commission.partner_id != partner_id:
            raise ValueError(f"commission {cid} belongs to another partner")
        if commission.status != CommissionStatus.APPROVED.value:
            raise ValueError(
                f"commission {cid} is not approved (status={commission.status})"
            )
        eligible.append(commission)
        total += commission.commission_sar

    payout = Payout(
        partner_id=partner_id,
        commission_ids=list(commission_ids),
        total_sar=total,
        method=method,
        reference=reference,
        status=PayoutStatus.PAID.value,
        paid_at=_now(),
    )
    _append(
        _payouts_path(),
        payout.to_dict(),
        stream_id="affiliate_store_payouts",
        event_id=payout.payout_id,
    )
    for commission in eligible:
        _update_commission(
            commission.commission_id,
            lambda row, pid=payout.payout_id: (
                row.__setitem__("status", CommissionStatus.PAID.value),
                row.__setitem__("payout_id", pid),
            ),
        )
    return payout


def list_payouts(*, partner_id: str | None = None) -> list[Payout]:
    out: list[Payout] = []
    for row in _read_all(_payouts_path()):
        if partner_id and row.get("partner_id") != partner_id:
            continue
        out.append(Payout(**row))
    return out


# ── Approved assets + compliance events ──────────────────────────────


def add_approved_asset(*, kind: str, lang: str, body: str) -> ApprovedAsset:
    asset = ApprovedAsset(kind=kind, lang=lang, body=body.strip())
    _append(
        _assets_path(),
        asset.to_dict(),
        stream_id="affiliate_store_assets",
        event_id=asset.asset_id,
    )
    return asset


def list_approved_assets(*, active_only: bool = True) -> list[ApprovedAsset]:
    out: list[ApprovedAsset] = []
    for row in _read_all(_assets_path()):
        if active_only and not row.get("is_active", True):
            continue
        out.append(ApprovedAsset(**row))
    return out


def log_compliance_event(
    *,
    partner_id: str,
    event_type: str,
    severity: str = "low",
    detail: str = "",
) -> ComplianceEvent:
    event = ComplianceEvent(
        partner_id=partner_id,
        event_type=event_type,
        severity=severity,
        detail=detail[:512],
    )
    _append(
        _compliance_path(),
        event.to_dict(),
        stream_id="affiliate_store_compliance",
        event_id=event.event_id,
    )
    return event


def list_compliance_events(*, partner_id: str | None = None) -> list[ComplianceEvent]:
    out: list[ComplianceEvent] = []
    for row in _read_all(_compliance_path()):
        if partner_id and row.get("partner_id") != partner_id:
            continue
        out.append(ComplianceEvent(**row))
    return out


# ── Dashboard aggregate ──────────────────────────────────────────────


def partner_dashboard(partner_id: str) -> dict[str, Any] | None:
    """Aggregate a partner's full state for the partner portal."""
    partner = get_partner(partner_id)
    if partner is None:
        return None
    commissions = list_commissions(partner_id=partner_id)
    earned = sum(
        c.commission_sar
        for c in commissions
        if c.status != CommissionStatus.CLAWED_BACK.value
    )
    paid = sum(
        c.commission_sar for c in commissions if c.status == CommissionStatus.PAID.value
    )
    pending = sum(
        c.commission_sar
        for c in commissions
        if c.status in (CommissionStatus.CALCULATED.value, CommissionStatus.APPROVED.value)
    )
    clawed_back = sum(
        c.commission_sar
        for c in commissions
        if c.status == CommissionStatus.CLAWED_BACK.value
    )
    return {
        "partner": partner.to_dict(),
        "links": [link.to_dict() for link in list_links(partner_id=partner_id)],
        "referrals": [r.to_dict() for r in list_referrals(partner_id=partner_id)],
        "commissions": [c.to_dict() for c in commissions],
        "payouts": [p.to_dict() for p in list_payouts(partner_id=partner_id)],
        "totals_sar": {
            "earned": earned,
            "paid": paid,
            "pending": pending,
            "clawed_back": clawed_back,
        },
    }


def clear_for_test() -> None:
    for p in (
        _partners_path(),
        _links_path(),
        _referrals_path(),
        _commissions_path(),
        _payouts_path(),
        _assets_path(),
        _compliance_path(),
    ):
        if p.exists():
            with _lock:
                p.write_text("", encoding="utf-8")


__all__ = [
    "CLAWBACK_WINDOW_DAYS",
    "TIER3_MAX_PCT",
    "TIER_PCT",
    "AffiliatePartner",
    "AffiliateReferral",
    "AffiliateReferralStatus",
    "ApprovedAsset",
    "Commission",
    "CommissionStatus",
    "ComplianceEvent",
    "PartnerLink",
    "PartnerStatus",
    "Payout",
    "PayoutStatus",
    "add_approved_asset",
    "apply_partner",
    "approve_commission",
    "approve_partner",
    "calculate_commission",
    "clawback_commission",
    "clear_for_test",
    "get_commission",
    "get_link",
    "get_partner",
    "get_referral",
    "list_approved_assets",
    "list_commissions",
    "list_compliance_events",
    "list_links",
    "list_partners",
    "list_payouts",
    "list_referrals",
    "log_compliance_event",
    "mark_invoice_paid",
    "mark_payout_paid",
    "partner_dashboard",
    "qualify_referral",
    "reject_partner",
    "reject_referral",
    "score_partner",
    "submit_referral",
    "suspend_partner",
    "tier_from_score",
]
