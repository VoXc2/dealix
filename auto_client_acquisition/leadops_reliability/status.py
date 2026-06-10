"""Overall LeadOps health snapshot."""
from __future__ import annotations

from datetime import UTC, datetime, timezone
from typing import Any

from auto_client_acquisition.integration_upgrade import safe_call


def overall_status() -> dict[str, Any]:
    """Returns a single dict describing LeadOps health."""
    records_count = safe_call(
        name="records_count",
        fn=lambda: _count_records(),
        fallback=0,
    )
    drafts_count = safe_call(
        name="drafts_count",
        fn=lambda: _count_drafts(),
        fallback=0,
    )
    return {
        "records_total": records_count if isinstance(records_count, int) else 0,
        "drafts_pending": drafts_count if isinstance(drafts_count, int) else 0,
        "last_check_at": datetime.now(UTC).isoformat(),
        "is_healthy": (
            isinstance(records_count, int)
            and isinstance(drafts_count, int)
        ),
    }


def _count_records() -> int:
    from auto_client_acquisition.leadops_spine import list_records
    return len(list_records(limit=1000))


def _count_drafts() -> int:
    from auto_client_acquisition.leadops_spine import list_records
    return sum(1 for r in list_records(limit=1000) if r.draft_id is not None)
