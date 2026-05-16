"""
Cursor-based (opaque) and offset-based pagination utilities.
أدوات الترقيم المستند إلى المؤشر (المعتم) والترقيم المستند إلى الإزاحة.

Cursor encoding: base64( json({created_at, id}) )

Usage (FastAPI endpoint):
    from api.schemas.pagination import PaginationParams, encode_cursor, decode_cursor

    @router.get("/leads")
    async def list_leads(p: PaginationParams = Depends()):
        ...
        after_id, after_ts = decode_cursor(p.cursor) if p.cursor else (None, None)
        ...
        return paginated(items, next_cursor=encode_cursor(last_item), has_more=has_more)
"""

from __future__ import annotations

import base64
import json
from datetime import datetime
from typing import Any

from fastapi import Query
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """
    Shared pagination query parameters — inject via Depends().
    معاملات الترقيم المشتركة — أدخلها عبر Depends().
    """

    cursor: str | None = Field(
        default=None,
        description="Opaque cursor for forward pagination (base64-encoded JSON).",
    )
    limit: int = Field(
        default=20,
        ge=1,
        le=200,
        description="Number of items per page (1–200, default 20).",
    )

    @classmethod
    def from_query(
        cls,
        cursor: str | None = Query(default=None, description="Pagination cursor"),
        limit: int = Query(default=20, ge=1, le=200, description="Items per page"),
    ) -> "PaginationParams":
        return cls(cursor=cursor, limit=limit)


def encode_cursor(row: Any, *, ts_field: str = "created_at", id_field: str = "id") -> str:
    """
    Encode a SQLAlchemy ORM row (or dict) into an opaque cursor string.
    يرمّز صف ORM أو قاموس إلى سلسلة مؤشر معتمة.
    """
    if isinstance(row, dict):
        ts = row.get(ts_field)
        row_id = row.get(id_field)
    else:
        ts = getattr(row, ts_field, None)
        row_id = getattr(row, id_field, None)

    if isinstance(ts, datetime):
        ts = ts.isoformat()

    payload = json.dumps({"ts": ts, "id": str(row_id) if row_id else None})
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_cursor(cursor: str) -> tuple[str | None, str | None]:
    """
    Decode an opaque cursor → (timestamp_iso, id).
    فكّ تشفير المؤشر → (طابع زمني ISO، معرّف).

    Returns (None, None) on any decode failure (treat as start of list).
    """
    try:
        raw = base64.urlsafe_b64decode(cursor.encode() + b"==").decode()
        data = json.loads(raw)
        return data.get("ts"), data.get("id")
    except Exception:  # noqa: BLE001
        return None, None


def offset_from_cursor(cursor: str | None, limit: int) -> int:
    """
    Fallback: decode offset-style cursor produced by encode_offset_cursor().
    احتياطي: فك تشفير المؤشر بناءً على الإزاحة.
    """
    if not cursor:
        return 0
    try:
        raw = base64.urlsafe_b64decode(cursor.encode() + b"==").decode()
        data = json.loads(raw)
        # Clamp to >= 0: a tampered/malformed cursor must not yield a
        # negative OFFSET (invalid on Postgres) — degrade to page one.
        return max(0, int(data.get("offset", 0)))
    except Exception:  # noqa: BLE001
        return 0


def encode_offset_cursor(offset: int) -> str:
    """Encode a simple numeric offset as a cursor."""
    payload = json.dumps({"offset": offset})
    return base64.urlsafe_b64encode(payload.encode()).decode()
