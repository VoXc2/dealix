"""HermesMemory — in-memory session context store with asyncio safety."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class SharedContext:
    """A snapshot of all key-value data stored for a single session."""

    agent_name: str
    session_id: str
    data: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "session_id": self.session_id,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class HermesMemory:
    """Thread-safe in-memory key-value store scoped by session_id.

    All mutations are protected by :class:`asyncio.Lock` so concurrent
    coroutines sharing the same instance do not race on the underlying dict.

    An optional Redis backend can be added in the future by overriding the
    private ``_store`` / ``_get`` helpers without changing the public API.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def store(self, session_id: str, key: str, value: Any) -> None:
        """Persist a key-value pair under the given session."""
        async with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = {}
            self._sessions[session_id][key] = value
        logger.debug("hermes_memory_store", session_id=session_id, key=key)

    async def get(self, session_id: str, key: str, default: Any = None) -> Any:
        """Retrieve a single key from a session, returning *default* if absent."""
        async with self._lock:
            return self._sessions.get(session_id, {}).get(key, default)

    async def get_session(self, session_id: str) -> dict[str, Any]:
        """Return a shallow copy of the entire session context dict."""
        async with self._lock:
            return dict(self._sessions.get(session_id, {}))

    async def clear_session(self, session_id: str) -> None:
        """Remove all data associated with a session."""
        async with self._lock:
            self._sessions.pop(session_id, None)
        logger.debug("hermes_memory_clear", session_id=session_id)

    async def list_sessions(self) -> list[str]:
        """Return a sorted list of all active session IDs."""
        async with self._lock:
            return sorted(self._sessions.keys())

    async def update_session(self, session_id: str, data: dict[str, Any]) -> None:
        """Merge a dict of key-value pairs into an existing session."""
        async with self._lock:
            if session_id not in self._sessions:
                self._sessions[session_id] = {}
            self._sessions[session_id].update(data)


__all__ = ["HermesMemory", "SharedContext"]
