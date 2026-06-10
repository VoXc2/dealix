"""Operational JSONL stream mirror (SQLite)."""

from __future__ import annotations

import pytest

pytest.importorskip("sqlalchemy")

from auto_client_acquisition.persistence.operational_stream_mirror import (
    list_mirrored,
    mirror_append,
    reset_operational_stream_mirror_for_test,
)


def test_mirror_append_writes_row(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_operational_stream_mirror_for_test()
    monkeypatch.setenv("DEALIX_OPERATIONAL_STREAM_BACKEND", "postgres")
    monkeypatch.setenv("DEALIX_OPERATIONAL_STREAM_SYNC_DATABASE_URL", "sqlite:///:memory:")
    mirror_append(stream_id="test_stream", payload={"k": 1}, event_id="e1")
    rows = list_mirrored(stream_id="test_stream", limit=5)
    assert len(rows) == 1
    assert rows[0]["event_id"] == "e1"
    assert rows[0]["payload"]["k"] == 1
    reset_operational_stream_mirror_for_test()
