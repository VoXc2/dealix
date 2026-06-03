"""Operating evidence after founder commercial day."""

from __future__ import annotations

from dealix.commercial_ops.evidence_append import log_founder_commercial_day_if_needed


def test_log_commercial_day_dry_run() -> None:
    blob = log_founder_commercial_day_if_needed(dry_run=True)
    assert blob.get("reason") == "dry_run"
    assert blob.get("would_append", {}).get("event_type") == "scope_requested"
