"""
Benchmarks — Phase 5 light: sector-aggregated anonymized stats.

Returns aggregated metrics across customers, grouped by sector. Honest
small-sample warnings when sector has < 3 customers.

Pure computation. No I/O.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any


_MIN_SECTOR_SAMPLE = 3


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def aggregate(
    customers: list | None = None,
    proof_events: list | None = None,
    sector_filter: str | None = None,
) -> dict[str, Any]:
    """Group customers + proof events by sector and compute averages.

    Args:
        customers: iterable of CustomerRecord-like (.id, .sector,
                   .pilot_start_at, .created_at)
        proof_events: iterable of ProofEventRecord-like (.customer_id,
                      .unit_type, .occurred_at)
        sector_filter: optional — return only the matching sector
    """
    custs = list(customers or [])
    events = list(proof_events or [])

    by_sector: dict[str, list] = defaultdict(list)
    for c in custs:
        sec = (getattr(c, "sector", None) or "unknown").strip() or "unknown"
        by_sector[sec].append(c)

    events_by_customer: dict[str, list] = defaultdict(list)
    for e in events:
        cid = getattr(e, "customer_id", None)
        if cid:
            events_by_customer[cid].append(e)

    sectors_out: list[dict[str, Any]] = []
    for sector, cust_list in by_sector.items():
        if sector_filter and sector_filter.lower() != sector.lower():
            continue
        n = len(cust_list)
        # Aggregate proof events for this sector's customers
        sector_events: list = []
        days_to_close: list[float] = []
        for c in cust_list:
            sector_events.extend(events_by_customer.get(c.id, []))
            start = getattr(c, "pilot_start_at", None) or getattr(c, "created_at", None)
            if start:
                # Find the meeting_closed event for this customer (= close)
                close_evs = [
                    e for e in events_by_customer.get(c.id, [])
                    if getattr(e, "unit_type", "") == "meeting_closed"
                ]
                if close_evs:
                    closed_at = getattr(close_evs[0], "occurred_at", None)
                    if closed_at:
                        try:
                            delta = (closed_at - start).total_seconds() / 86400.0
                            if delta > 0:
                                days_to_close.append(delta)
                        except (TypeError, ValueError):
                            pass

        rwu_counts: Counter[str] = Counter(
            getattr(e, "unit_type", "unknown") for e in sector_events
        )
        top_rwus = rwu_counts.most_common(3)

        avg_proof_per_customer = round(
            len(sector_events) / n if n else 0.0, 2
        )
        avg_days_to_close = (
            round(sum(days_to_close) / len(days_to_close), 1)
            if days_to_close else None
        )

        sectors_out.append({
            "sector": sector,
            "customers_count": n,
            "sample_quality_ar": (
                f"low (n={n}<{_MIN_SECTOR_SAMPLE})"
                if n < _MIN_SECTOR_SAMPLE else
                f"medium (n={n})" if n < 10 else f"high (n={n})"
            ),
            "avg_proof_events_per_customer": avg_proof_per_customer,
            "avg_pilot_days_to_close": avg_days_to_close,
            "top_rwus": [{"unit_type": k, "count": v} for k, v in top_rwus],
        })

    sectors_out.sort(key=lambda x: -x["customers_count"])

    overall = {
        "as_of": _now().isoformat(),
        "total_customers": len(custs),
        "sectors_analyzed": len(sectors_out),
        "sectors": sectors_out,
        "min_sample_for_confidence": _MIN_SECTOR_SAMPLE,
        "note_ar": (
            "Phase 5 light: نتائج إرشادية. الإصدار الكامل (مع playbook "
            "نشر تلقائي) يتفعّل عند ≥٥ retainers + ٩٠ يوم بيانات."
        ),
    }
    if not custs:
        overall["empty_ar"] = "لا توجد بيانات customers بعد — اشتغل أول Pilot 499."
    return overall
