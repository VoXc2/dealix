"""
Channel Performance — analyzes which outreach channels convert best.

Phase 3 skeleton. Full version with funnel-stage tracking lands at
3 paid + ≥30 stage transitions.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def analyze_channels(events: list) -> dict[str, Any]:
    """Compute reply_rate / meeting_rate / pilot_rate per channel.

    Args:
        events: iterable of ProofEventRecord-like with .unit_type + meta.channel
    """
    rows = list(events or [])
    by_channel_unit: dict[tuple[str, str], int] = defaultdict(int)

    for e in rows:
        meta = dict(getattr(e, "meta_json", None) or {})
        channel = str(meta.get("channel", "unknown"))
        by_channel_unit[(channel, e.unit_type)] += 1

    channels: dict[str, dict[str, int]] = defaultdict(lambda: {
        "draft_created": 0,
        "opportunity_created": 0,
        "meeting_drafted": 0,
        "approval_collected": 0,
        "meeting_closed": 0,
    })
    for (channel, unit), count in by_channel_unit.items():
        if unit in channels[channel]:
            channels[channel][unit] = count

    out = []
    for channel, counts in channels.items():
        sent = counts["draft_created"]
        replies = counts["opportunity_created"]
        meetings = counts["meeting_drafted"]
        pilots = counts["approval_collected"]
        wins = counts["meeting_closed"]
        out.append({
            "channel": channel,
            "drafts_sent": sent,
            "replies": replies,
            "meetings": meetings,
            "pilots": pilots,
            "wins": wins,
            "reply_rate": round(replies / sent, 3) if sent else 0.0,
            "meeting_rate": round(meetings / replies, 3) if replies else 0.0,
            "pilot_rate": round(pilots / meetings, 3) if meetings else 0.0,
            "win_rate": round(wins / pilots, 3) if pilots else 0.0,
        })
    out.sort(key=lambda x: x["reply_rate"], reverse=True)

    return {
        "channels_count": len(out),
        "channels": out,
        "best_channel": out[0]["channel"] if out else None,
        "note_ar": (
            "النتائج موثوقة بعد ≥٣٠ رسالة لكل قناة. "
            "الحالي قد يكون عيّنة صغيرة."
        ),
    }
