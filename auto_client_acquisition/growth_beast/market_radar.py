"""Placeholder market radar — inbound/partner-safe signals only."""
from __future__ import annotations

from datetime import UTC, datetime


def synthetic_signals_today() -> list[dict[str, object]]:
    """Deterministic stand-in until external radar is wired."""
    day = datetime.now(UTC).strftime("%Y-%m-%d")
    return [
        {
            "signal_id": f"inbound-{day}",
            "source": "inbound_placeholder",
            "summary_ar": "لا استيراد تلقائي — استخدم قنوات مسموحة فقط",
            "strength": 40,
        }
    ]
