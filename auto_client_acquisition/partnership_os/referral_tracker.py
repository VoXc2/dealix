"""V12 Partnership OS — in-memory referral log.

Placeholder names only. NO PII. Used to gate the revenue-share
motion (`partner_motion.recommend_motion(has_referral_data=...)`).
"""
from __future__ import annotations

from datetime import UTC, datetime
from threading import RLock

from pydantic import BaseModel, ConfigDict


class Referral(BaseModel):
    model_config = ConfigDict(extra="forbid")

    referral_id: str
    partner_id: str
    customer_placeholder: str
    status: str = "introduced"
    created_at: datetime


_REFERRALS: list[Referral] = []
_LOCK = RLock()


def add_referral(*, partner_id: str, customer_placeholder: str) -> Referral:
    with _LOCK:
        rid = f"ref_{len(_REFERRALS)+1:04d}"
        ref = Referral(
            referral_id=rid,
            partner_id=partner_id,
            customer_placeholder=customer_placeholder,
            created_at=datetime.now(UTC),
        )
        _REFERRALS.append(ref)
        return ref


def list_referrals(*, partner_id: str | None = None) -> list[Referral]:
    with _LOCK:
        if partner_id is None:
            return list(_REFERRALS)
        return [r for r in _REFERRALS if r.partner_id == partner_id]


def reset_referrals() -> None:
    """Test-only — wipe the in-memory log."""
    with _LOCK:
        _REFERRALS.clear()
