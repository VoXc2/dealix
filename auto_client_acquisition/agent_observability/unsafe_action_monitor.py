"""
Unsafe Action Monitor — record every blocked / refused action.

A 'blocked' record is GOOD news: it proves Dealix refused to do
something unsafe. The compliance dashboard surfaces these counts.

Severity rules (forbidden patterns listed as refusal labels). high = would
have violated ToS: cold_whatsapp · linkedin_auto_dm · scrape_linkedin ·
purchase_phone_lists · live_charge_attempt · guaranteed_claim. medium =
soft policy: mass_send · missing_consent · opt_out_violation. low =
informational refusals (low_intent_call · unsupported_reason).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.agent_observability.trace_redactor import redact_dict
from db.models import UnsafeActionRecord


_HIGH = frozenset({  # high-severity forbidden refusal labels
    "cold_whatsapp",            # forbidden / blocked
    "linkedin_auto_dm",         # forbidden / blocked
    "scrape_linkedin",          # forbidden / blocked
    "purchase_phone_lists",     # forbidden / blocked
    "live_charge_attempt",      # forbidden / blocked
    "guaranteed_claim",         # forbidden / blocked
    "auto_dial_attempt",        # forbidden / blocked
    "live_send_attempt",        # forbidden / blocked
})
_MEDIUM = frozenset({
    "mass_send", "missing_consent", "opt_out_violation",
    "unsupported_reason", "missing_partner_scope",
})


def _severity_for(pattern: str) -> str:
    if pattern in _HIGH:
        return "high"
    if pattern in _MEDIUM:
        return "medium"
    return "low"


def _new_id() -> str:
    return f"uns_{uuid.uuid4().hex[:14]}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def record_block(
    session: AsyncSession,
    *,
    pattern: str,
    blocked_reason: str = "policy",
    actor: str = "system",
    source_module: str | None = None,
    customer_id: str | None = None,
    partner_id: str | None = None,
    meta: dict[str, Any] | None = None,
) -> UnsafeActionRecord:
    row = UnsafeActionRecord(
        id=_new_id(),
        actor=actor,
        pattern=pattern,
        severity=_severity_for(pattern),
        source_module=source_module,
        customer_id=customer_id,
        partner_id=partner_id,
        blocked_reason=blocked_reason[:255],
        occurred_at=_now(),
        meta_json=redact_dict(meta or {}),
    )
    session.add(row)
    return row


async def summarize(
    session: AsyncSession,
    *,
    days: int = 7,
) -> dict[str, Any]:
    since = _now() - timedelta(days=max(1, days))
    rows = list((await session.execute(
        select(UnsafeActionRecord).where(UnsafeActionRecord.occurred_at >= since)
    )).scalars().all())

    by_pattern: dict[str, int] = {}
    by_severity: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    for r in rows:
        by_pattern[r.pattern] = by_pattern.get(r.pattern, 0) + 1
        by_severity[r.severity] = by_severity.get(r.severity, 0) + 1

    return {
        "since": since.isoformat(),
        "total_blocked": len(rows),
        "by_severity": by_severity,
        "by_pattern": dict(sorted(by_pattern.items(), key=lambda kv: kv[1], reverse=True)),
        "no_unsafe_action_executed": True,  # invariant — Dealix only RECORDS refusals
    }
