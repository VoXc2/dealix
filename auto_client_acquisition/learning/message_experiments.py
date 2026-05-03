"""
Message Experiments — scores outreach drafts by reply rate, grouped by
segment + channel.

Phase 3 skeleton. Full version (Bayesian A/B) lands at 3 paid + ≥30
sent messages.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def score_messages(events: list) -> dict[str, Any]:
    """Group draft_created + opportunity_created (reply) events by
    segment+channel meta and compute reply rate.

    Args:
        events: iterable of ProofEventRecord-like with
            .unit_type, .meta_json (containing 'segment', 'channel', etc.)
    """
    rows = list(events or [])
    sent_by: dict[tuple[str, str], int] = defaultdict(int)
    replied_by: dict[tuple[str, str], int] = defaultdict(int)

    for e in rows:
        meta = dict(getattr(e, "meta_json", None) or {})
        segment = str(meta.get("segment", "unknown"))
        channel = str(meta.get("channel", "unknown"))
        key = (segment, channel)
        if e.unit_type == "draft_created":
            sent_by[key] += 1
        elif e.unit_type == "opportunity_created":
            # opportunity_created RWU corresponds to a reply received
            replied_by[key] += 1

    rows_out = []
    for key, sent in sent_by.items():
        replied = replied_by.get(key, 0)
        rate = (replied / sent) if sent else 0.0
        rows_out.append({
            "segment": key[0],
            "channel": key[1],
            "sent": sent,
            "replied": replied,
            "reply_rate": round(rate, 3),
        })
    rows_out.sort(key=lambda x: x["reply_rate"], reverse=True)

    total_sent = sum(sent_by.values())
    total_replied = sum(replied_by.values())

    return {
        "experiments_count": len(rows_out),
        "total_sent": total_sent,
        "total_replied": total_replied,
        "overall_reply_rate": round(
            total_replied / total_sent if total_sent else 0.0, 3
        ),
        "best_combinations": rows_out[:5],
        "note_ar": (
            "النتائج تصبح ذات دلالة بعد ≥٣٠ رسالة في كل combo. "
            "الحالي عيّنة صغيرة — استخدم كإرشاد لا كدليل قاطع."
            if total_sent < 30 else None
        ),
    }
