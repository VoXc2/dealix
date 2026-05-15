"""Best-effort Postgres mirror for tier-2 JSONL append paths (catalog ids).

Writes to ``operational_event_streams`` when ``DEALIX_OPERATIONAL_STREAM_BACKEND``
is ``postgres`` or ``dual``. Failures are swallowed so JSONL remains canonical.
"""

from __future__ import annotations

import logging
import os
import threading
import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url

_LOG = logging.getLogger(__name__)

_STREAM_BACKEND_ENV = "DEALIX_OPERATIONAL_STREAM_BACKEND"


class _StreamBase(DeclarativeBase):
    pass


class OperationalEventStreamORM(_StreamBase):
    __tablename__ = "operational_event_streams"

    stream_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


_engine: Engine | None = None
_session_factory: sessionmaker | None = None
_lock = threading.Lock()


def _backend() -> str:
    raw = (
        os.environ.get(_STREAM_BACKEND_ENV)
        or os.environ.get("OPERATIONAL_STREAM_BACKEND")
        or ""
    ).strip().lower()
    if raw:
        return raw
    try:
        from core.config.settings import get_settings

        return str(getattr(get_settings(), "operational_stream_backend", "off") or "off").lower().strip()
    except Exception:  # noqa: BLE001
        return "off"


def _should_mirror() -> bool:
    return _backend() in ("postgres", "dual")


def _get_engine() -> Engine | None:
    global _engine, _session_factory
    if not _should_mirror():
        return None
    with _lock:
        if _engine is not None:
            return _engine
        raw = os.environ.get("DEALIX_OPERATIONAL_STREAM_SYNC_DATABASE_URL", "").strip()
        if not raw:
            try:
                from core.config.settings import get_settings

                raw = getattr(get_settings(), "database_url", "") or ""
            except Exception:  # noqa: BLE001
                raw = ""
        if not raw:
            return None
        url = sync_sqlalchemy_url(raw)
        try:
            eng = create_engine(url, future=True, pool_pre_ping=True)
            eng.connect().close()
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("operational_stream_mirror_engine_failed:%s", type(exc).__name__)
            return None
        _engine = eng
        OperationalEventStreamORM.__table__.create(bind=_engine, checkfirst=True)
        _session_factory = sessionmaker(_engine, expire_on_commit=False, future=True)
        return _engine


def reset_operational_stream_mirror_for_test() -> None:
    """Drop cached engine (pytest)."""
    global _engine, _session_factory
    with _lock:
        if _engine is not None:
            try:
                _StreamBase.metadata.drop_all(_engine)
            except Exception:  # noqa: BLE001
                pass
        _engine = None
        _session_factory = None


def mirror_append(
    *,
    stream_id: str,
    payload: dict[str, Any],
    event_id: str | None = None,
    occurred_at: datetime | None = None,
) -> None:
    """Append one mirrored row. No-op when backend is off or engine unavailable."""
    if not _should_mirror():
        return
    eid = (event_id or str(payload.get("event_id") or payload.get("payment_id") or "")).strip()
    if not eid:
        eid = f"mirror_{uuid.uuid4().hex[:16]}"
    when = occurred_at or datetime.now(UTC)
    eng = _get_engine()
    if eng is None or _session_factory is None:
        return
    row = OperationalEventStreamORM(
        stream_id=stream_id[:128],
        event_id=eid[:128],
        payload=dict(payload),
        occurred_at=when,
    )
    try:
        with _lock, _session_factory() as session:
            session.merge(row)
            session.commit()
    except Exception as exc:  # noqa: BLE001
        _LOG.debug("operational_stream_mirror_append_failed:%s", type(exc).__name__)


def list_mirrored(
    *,
    stream_id: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Test helper: newest first."""
    _get_engine()
    if _engine is None or _session_factory is None:
        return []
    stmt = (
        select(OperationalEventStreamORM)
        .where(OperationalEventStreamORM.stream_id == stream_id)
        .order_by(OperationalEventStreamORM.occurred_at.desc())
        .limit(limit)
    )
    with _lock, _session_factory() as session:
        rows = session.execute(stmt).scalars().all()
    return [
        {
            "stream_id": r.stream_id,
            "event_id": r.event_id,
            "payload": dict(r.payload or {}),
            "occurred_at": r.occurred_at.isoformat() if r.occurred_at else "",
        }
        for r in rows
    ]


__all__ = [
    "mirror_append",
    "list_mirrored",
    "reset_operational_stream_mirror_for_test",
]
