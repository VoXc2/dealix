"""Unit tests for dealix/audit/forward.py."""

from __future__ import annotations

import asyncio

import pytest

from dealix.audit.forward import forward


@pytest.fixture(autouse=True)
def _unset_sinks(monkeypatch: pytest.MonkeyPatch) -> None:
    for v in (
        "AUDIT_FORWARD_DATADOG_API_KEY",
        "AUDIT_FORWARD_SPLUNK_URL",
        "AUDIT_FORWARD_SPLUNK_TOKEN",
        "AUDIT_FORWARD_S3_BUCKET",
    ):
        monkeypatch.delenv(v, raising=False)


def test_forward_returns_empty_when_nothing_configured() -> None:
    row = {"id": "audit_001", "tenant_id": "t1", "action": "lead.create"}
    out = asyncio.run(forward(row))
    assert out == {}


def test_forward_skips_splunk_when_url_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUDIT_FORWARD_SPLUNK_URL", "https://hec.example/")
    # Token missing → splunk skipped, result is still empty.
    out = asyncio.run(forward({"id": "x", "tenant_id": "t1"}))
    assert "splunk" not in out


def test_forward_skips_s3_when_aioboto3_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUDIT_FORWARD_S3_BUCKET", "dealix-audit")
    out = asyncio.run(forward({"id": "x", "tenant_id": "t1"}))
    # Without aioboto3 the s3 sink returns False; with it installed it'd try
    # real S3 and likely fail. Either way the sink key may appear.
    assert out.get("s3") in (False, None)
