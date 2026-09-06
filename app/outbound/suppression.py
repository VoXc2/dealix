"""Suppression authority for recipients who must never receive outbound messages.

The default implementation remains in-memory and is suitable only for unit
 tests, synthetic drills, and draft-only execution.  Controlled-live execution
can opt into the existing PostgreSQL ``data_suppression_list`` truth store with:

    DEALIX_SUPPRESSION_BACKEND=postgres
    DATABASE_URL=<existing Dealix PostgreSQL URL>

The Postgres path is fail-closed: an unavailable database, missing table, or
query error never becomes permission to send.  No backend switch enables live
send by itself; the outbound policy gate still requires all other authority,
consent, approval, rate-limit and channel controls.
"""

from __future__ import annotations

import os
import uuid
from contextlib import contextmanager
from threading import Lock
from typing import Any, Iterator

_LOCK = Lock()
# _SUPPRESSED[identifier] = set(channels) | {"__all__"}
_SUPPRESSED: "dict[str, set[str]]" = {}

ALL_CHANNELS = "__all__"
_MEMORY_BACKEND = "memory"
_POSTGRES_BACKEND = "postgres"


def suppression_backend_kind() -> str:
    """Return the configured suppression backend identifier.

    Unknown values deliberately collapse to ``memory`` rather than silently
    activating a new persistence mode.
    """

    value = os.getenv("DEALIX_SUPPRESSION_BACKEND", _MEMORY_BACKEND).strip().lower()
    return _POSTGRES_BACKEND if value == _POSTGRES_BACKEND else _MEMORY_BACKEND


def _postgres_dsn() -> str | None:
    value = os.getenv("DATABASE_URL", "").strip()
    if not value:
        return None
    if value.startswith("postgresql+asyncpg://"):
        return "postgresql://" + value.removeprefix("postgresql+asyncpg://")
    if value.startswith("postgres://"):
        return "postgresql://" + value.removeprefix("postgres://")
    if value.startswith("postgresql://"):
        return value
    return None


@contextmanager
def _postgres_connection() -> Iterator[Any]:
    dsn = _postgres_dsn()
    if not dsn:
        raise RuntimeError("postgres suppression backend requires PostgreSQL DATABASE_URL")

    import psycopg

    with psycopg.connect(dsn, connect_timeout=3, autocommit=True) as conn:
        yield conn


def _postgres_table_ready() -> bool:
    try:
        with _postgres_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT to_regclass('public.data_suppression_list') IS NOT NULL")
            row = cur.fetchone()
            return bool(row and row[0] is True)
    except Exception:
        return False


def persistent_suppression_ready() -> bool:
    """Whether suppression durability is proven for controlled live sends."""

    if suppression_backend_kind() != _POSTGRES_BACKEND:
        return False
    return _postgres_table_ready()


def suppression_backend_status() -> dict[str, Any]:
    """Return a non-sensitive status record for diagnostics and proof packs."""

    backend = suppression_backend_kind()
    persistent = persistent_suppression_ready()
    if backend == _MEMORY_BACKEND:
        reason = "in_memory_suppression_is_not_durable"
    elif persistent:
        reason = "postgres_suppression_table_verified"
    else:
        reason = "postgres_suppression_not_verified"
    return {
        "backend": backend,
        "persistent": persistent,
        "live_send_eligible": persistent,
        "reason": reason,
    }


def _norm(identifier: str) -> str:
    return (identifier or "").strip().lower()


def _looks_phone(identifier: str) -> bool:
    compact = identifier.replace(" ", "").replace("-", "")
    return compact.startswith("+") or compact.isdigit()


def _target(identifier: str, channel: str) -> tuple[str, str]:
    ident = _norm(identifier)
    if channel == "email" or "@" in ident:
        return "email", ident
    if channel in {"sms", "whatsapp"} or _looks_phone(ident):
        return "phone", ident
    return "domain", ident


def _postgres_is_suppressed(identifier: str, channel: str) -> bool:
    column, value = _target(identifier, channel)
    if not value:
        return False

    try:
        with _postgres_connection() as conn, conn.cursor() as cur:
            if column == "email":
                domain = value.rsplit("@", 1)[1] if "@" in value else ""
                cur.execute(
                    """
                    SELECT 1
                      FROM data_suppression_list
                     WHERE lower(email) = lower(%s)
                        OR (%s <> '' AND lower(domain) = lower(%s))
                     LIMIT 1
                    """,
                    (value, domain, domain),
                )
            else:
                cur.execute(
                    f"SELECT 1 FROM data_suppression_list WHERE lower({column}) = lower(%s) LIMIT 1",
                    (value,),
                )
            return cur.fetchone() is not None
    except Exception:
        # Suppression uncertainty must never turn into live-send permission.
        return True


def is_suppressed(identifier: str, channel: str = "email") -> bool:
    """True if ``identifier`` is suppressed for ``channel`` or globally.

    Postgres errors fail closed and return True.
    """

    ident = _norm(identifier)
    if not ident:
        return False
    if suppression_backend_kind() == _POSTGRES_BACKEND:
        return _postgres_is_suppressed(ident, channel)

    with _LOCK:
        entry = _SUPPRESSED.get(ident)
        if not entry:
            return False
        return ALL_CHANNELS in entry or channel in entry


def _postgres_add(identifier: str, channel: str, reason: str) -> None:
    column, value = _target(identifier, channel)
    if not value:
        return
    with _postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT 1 FROM data_suppression_list WHERE lower({column}) = lower(%s) LIMIT 1",
            (value,),
        )
        if cur.fetchone() is not None:
            return
        cur.execute(
            f"INSERT INTO data_suppression_list (id, {column}, reason) VALUES (%s, %s, %s)",
            (uuid.uuid4().hex, value, reason or "opt_out"),
        )


def add_suppression(
    identifier: str,
    channel: str = ALL_CHANNELS,
    reason: str = "",
) -> None:
    """Add ``identifier`` to the active suppression authority."""

    ident = _norm(identifier)
    if not ident:
        return
    if suppression_backend_kind() == _POSTGRES_BACKEND:
        _postgres_add(ident, channel, reason)
        return

    with _LOCK:
        entry = _SUPPRESSED.setdefault(ident, set())
        entry.add(channel or ALL_CHANNELS)


def _postgres_remove(identifier: str, channel: str | None) -> None:
    column, value = _target(identifier, channel or ALL_CHANNELS)
    if not value:
        return
    with _postgres_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM data_suppression_list WHERE lower({column}) = lower(%s)",
            (value,),
        )


def remove_suppression(identifier: str, channel: str | None = None) -> None:
    """Remove an entry from the active suppression authority."""

    ident = _norm(identifier)
    if suppression_backend_kind() == _POSTGRES_BACKEND:
        _postgres_remove(ident, channel)
        return

    with _LOCK:
        if channel is None:
            _SUPPRESSED.pop(ident, None)
            return
        entry = _SUPPRESSED.get(ident)
        if entry:
            entry.discard(channel)
            if not entry:
                _SUPPRESSED.pop(ident, None)


def suppressed_channels(identifier: str) -> set[str]:
    """Return channels suppressed for ``identifier`` (may include ``__all__``)."""

    ident = _norm(identifier)
    if not ident:
        return set()
    if suppression_backend_kind() == _POSTGRES_BACKEND:
        if "@" in ident:
            return {"email"} if _postgres_is_suppressed(ident, "email") else set()
        if _looks_phone(ident):
            return {"sms", "whatsapp"} if _postgres_is_suppressed(ident, "sms") else set()
        return {ALL_CHANNELS} if _postgres_is_suppressed(ident, ALL_CHANNELS) else set()

    with _LOCK:
        return set(_SUPPRESSED.get(ident, set()))


def clear_suppressions() -> None:
    """Clear process-local suppression state; used by tests only.

    Durable suppression must never be bulk-cleared through a test helper.
    """

    if suppression_backend_kind() == _POSTGRES_BACKEND:
        raise RuntimeError("clear_suppressions is disabled for durable suppression")
    with _LOCK:
        _SUPPRESSED.clear()


def load_suppressions(items: list[dict[str, Any]]) -> None:
    """Bulk-load suppression entries through the active authority."""

    for item in items:
        add_suppression(
            str(item.get("identifier", "")),
            channel=str(item.get("channel", ALL_CHANNELS)),
            reason=str(item.get("reason", "")),
        )
