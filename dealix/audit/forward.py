"""
Customer-side audit-log forwarding.

A tenant can configure where their audit rows should land in addition
to Dealix's own AuditLogRecord table:

- S3 bucket (`AUDIT_FORWARD_S3_BUCKET` + AWS creds).
- Datadog Logs (`AUDIT_FORWARD_DATADOG_API_KEY`).
- Splunk HEC (`AUDIT_FORWARD_SPLUNK_URL` + `AUDIT_FORWARD_SPLUNK_TOKEN`).

Each destination is best-effort: failures log + return False. We never
break the underlying request because a customer-side sink is down.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _is_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes"}


async def forward(row: dict[str, Any]) -> dict[str, bool]:
    """Best-effort forward of one audit row to every configured sink."""
    results: dict[str, bool] = {}

    ddk = os.getenv("AUDIT_FORWARD_DATADOG_API_KEY", "").strip()
    if ddk:
        results["datadog"] = await _forward_datadog(row, ddk)

    splunk_url = os.getenv("AUDIT_FORWARD_SPLUNK_URL", "").strip()
    splunk_token = os.getenv("AUDIT_FORWARD_SPLUNK_TOKEN", "").strip()
    if splunk_url and splunk_token:
        results["splunk"] = await _forward_splunk(row, splunk_url, splunk_token)

    s3_bucket = os.getenv("AUDIT_FORWARD_S3_BUCKET", "").strip()
    if s3_bucket:
        results["s3"] = await _forward_s3(row, s3_bucket)

    return results


async def _forward_datadog(row: dict[str, Any], api_key: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                "https://http-intake.logs.datadoghq.com/api/v2/logs",
                headers={
                    "DD-API-KEY": api_key,
                    "Content-Type": "application/json",
                },
                json=[
                    {
                        "ddsource": "dealix-audit",
                        "service": "dealix-api",
                        "hostname": "dealix",
                        "message": json.dumps(row, ensure_ascii=False),
                        "ddtags": f"env:{os.getenv('APP_ENV', 'unknown')}",
                    }
                ],
            )
            r.raise_for_status()
        return True
    except Exception:
        log.exception("audit_forward_datadog_failed")
        return False


async def _forward_splunk(row: dict[str, Any], url: str, token: str) -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{url.rstrip('/')}/services/collector/event",
                headers={"Authorization": f"Splunk {token}"},
                json={
                    "event": row,
                    "sourcetype": "dealix:audit",
                    "time": int(datetime.now(timezone.utc).timestamp()),
                },
            )
            r.raise_for_status()
        return True
    except Exception:
        log.exception("audit_forward_splunk_failed")
        return False


async def _forward_s3(row: dict[str, Any], bucket: str) -> bool:
    """Best-effort. Real wiring needs aioboto3; without it we no-op."""
    try:
        import aioboto3  # type: ignore
    except ImportError:
        log.info("aioboto3_not_installed; s3 audit forward skipped")
        return False
    key = (
        f"audit/{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/"
        f"{row.get('tenant_id', 'unknown')}/{row.get('id', 'noid')}.json"
    )
    try:
        session = aioboto3.Session()
        async with session.client("s3") as s3:
            await s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(row, ensure_ascii=False).encode("utf-8"),
                ContentType="application/json",
            )
        return True
    except Exception:
        log.exception("audit_forward_s3_failed", key=key)
        return False
