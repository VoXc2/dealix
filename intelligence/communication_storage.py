"""Durable, serverless-safe storage for the Communication OS.

The router imports this module during application startup, so constructors must
not touch the filesystem or connect to the database. Reads and mutations are
performed lazily. Production and staging default to PostgreSQL; local and test
environments use the explicit file adapter.

The same storage substrate also owns the append-only Collaboration OS event
collection so Dealix does not introduce a parallel database or source of truth.
"""

from __future__ import annotations

import copy
import json
import os
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal, Protocol, TypeVar

from sqlalchemy import JSON, DateTime, String, create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url
from core.config.settings import get_settings

CommunicationCollection = Literal[
    "contact_log",
    "sequences",
    "collaboration_events",
]
MutationResult = TypeVar("MutationResult")

_COLLECTIONS: tuple[CommunicationCollection, ...] = (
    "contact_log",
    "sequences",
    "collaboration_events",
)


class CommunicationStorageUnavailable(RuntimeError):
    """Raised when Communication OS cannot safely access durable storage."""


class CommunicationStorage(Protocol):
    """Storage contract used by CommunicationHub and CollaborationHub."""

    backend_name: str
    durable: bool

    def read(self, collection: CommunicationCollection) -> list[dict[str, Any]]:
        """Return a detached snapshot of one collection."""

    def mutate(
        self,
        collection: CommunicationCollection,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        """Atomically mutate one collection and return the mutation result."""

    def readiness(self) -> dict[str, Any]:
        """Return a non-secret backend readiness signal."""


def _validate_collection(collection: str) -> CommunicationCollection:
    if collection not in _COLLECTIONS:
        raise ValueError(f"Unknown communication collection: {collection}")
    return collection  # type: ignore[return-value]


class FileCommunicationStorage:
    """Lazy JSON-file adapter for local development and tests only."""

    backend_name = "file"
    durable = False

    def __init__(self, base_path: Path | str = Path("data/comms")) -> None:
        self._base_path = Path(base_path)
        self._locks = {collection: threading.RLock() for collection in _COLLECTIONS}

    def _path(self, collection: CommunicationCollection) -> Path:
        names = {
            "contact_log": "contact_log.json",
            "sequences": "sequences.json",
            "collaboration_events": "collaboration_events.json",
        }
        return self._base_path / names[collection]

    def _read_unlocked(self, collection: CommunicationCollection) -> list[dict[str, Any]]:
        path = self._path(collection)
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise CommunicationStorageUnavailable(
                "Communication file storage could not be read safely"
            ) from exc
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise CommunicationStorageUnavailable(
                "Communication file storage contains an invalid snapshot"
            )
        return data

    def read(self, collection: CommunicationCollection) -> list[dict[str, Any]]:
        collection = _validate_collection(collection)
        with self._locks[collection]:
            return copy.deepcopy(self._read_unlocked(collection))

    def mutate(
        self,
        collection: CommunicationCollection,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        collection = _validate_collection(collection)
        path = self._path(collection)
        with self._locks[collection]:
            data = self._read_unlocked(collection)
            result = mutation(data)
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                temp_path = path.with_suffix(f"{path.suffix}.tmp")
                temp_path.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                temp_path.replace(path)
            except Exception as exc:
                raise CommunicationStorageUnavailable(
                    "Communication file storage is not writable"
                ) from exc
            return result

    def readiness(self) -> dict[str, Any]:
        try:
            for collection in _COLLECTIONS:
                self.read(collection)
        except CommunicationStorageUnavailable:
            return {
                "status": "degraded",
                "backend": self.backend_name,
                "durable": self.durable,
                "write_ready": False,
                "reason": "file_storage_unavailable",
            }
        return {
            "status": "ready",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": True,
            "reason": "local_or_test_file_backend",
        }


class _CommunicationStorageBase(DeclarativeBase):
    pass


class CommunicationSnapshotORM(_CommunicationStorageBase):
    """One row per Communication/Collaboration OS collection."""

    __tablename__ = "communication_hub_snapshots"

    collection: Mapped[str] = mapped_column(String(32), primary_key=True)
    data: Mapped[list[dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PostgresCommunicationStorage:
    """Transactional JSON snapshot storage backed by PostgreSQL."""

    backend_name = "postgres"
    durable = True

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = False,
    ) -> None:
        if engine is None:
            if not database_url:
                raise ValueError("database_url is required for PostgreSQL communication storage")
            engine = create_engine(
                database_url,
                future=True,
                pool_pre_ping=True,
                pool_size=2,
                max_overflow=2,
                pool_timeout=10,
                pool_recycle=1800,
            )
        self._engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        if create_tables:
            _CommunicationStorageBase.metadata.create_all(self._engine)

    def read(self, collection: CommunicationCollection) -> list[dict[str, Any]]:
        collection = _validate_collection(collection)
        try:
            with self._sessionmaker() as session:
                row = session.get(CommunicationSnapshotORM, collection)
                data = row.data if row is not None else []
                if not isinstance(data, list) or not all(
                    isinstance(item, dict) for item in data
                ):
                    raise CommunicationStorageUnavailable(
                        "Communication database snapshot is invalid"
                    )
                return copy.deepcopy(data)
        except CommunicationStorageUnavailable:
            raise
        except Exception as exc:
            raise CommunicationStorageUnavailable(
                "Durable communication storage is unavailable"
            ) from exc

    def mutate(
        self,
        collection: CommunicationCollection,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        collection = _validate_collection(collection)
        try:
            with self._sessionmaker() as session:
                row = session.execute(
                    select(CommunicationSnapshotORM)
                    .where(CommunicationSnapshotORM.collection == collection)
                    .with_for_update()
                ).scalar_one_or_none()
                if row is None:
                    row = CommunicationSnapshotORM(
                        collection=collection,
                        data=[],
                        updated_at=datetime.now(UTC),
                    )
                    session.add(row)
                data = copy.deepcopy(row.data or [])
                if not isinstance(data, list) or not all(
                    isinstance(item, dict) for item in data
                ):
                    raise CommunicationStorageUnavailable(
                        "Communication database snapshot is invalid"
                    )
                result = mutation(data)
                row.data = data
                row.updated_at = datetime.now(UTC)
                session.commit()
                return result
        except CommunicationStorageUnavailable:
            raise
        except Exception as exc:
            raise CommunicationStorageUnavailable(
                "Durable communication storage mutation failed closed"
            ) from exc

    def readiness(self) -> dict[str, Any]:
        try:
            with self._sessionmaker() as session:
                session.execute(select(CommunicationSnapshotORM.collection).limit(1)).all()
        except Exception:
            return {
                "status": "degraded",
                "backend": self.backend_name,
                "durable": self.durable,
                "write_ready": False,
                "reason": "postgres_unavailable_or_migration_missing",
            }
        return {
            "status": "ready",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": True,
            "reason": "postgres_available",
        }


class UnavailableCommunicationStorage:
    """Fail-closed backend that keeps the router importable."""

    backend_name = "unavailable"
    durable = False

    def __init__(self, reason: str) -> None:
        self._reason = reason

    def read(self, collection: CommunicationCollection) -> list[dict[str, Any]]:
        _validate_collection(collection)
        raise CommunicationStorageUnavailable(
            "Communication storage is not configured safely"
        )

    def mutate(
        self,
        collection: CommunicationCollection,
        mutation: Callable[[list[dict[str, Any]]], MutationResult],
    ) -> MutationResult:
        _validate_collection(collection)
        raise CommunicationStorageUnavailable(
            "Communication storage mutation blocked because durable storage is unavailable"
        )

    def readiness(self) -> dict[str, Any]:
        return {
            "status": "degraded",
            "backend": self.backend_name,
            "durable": self.durable,
            "write_ready": False,
            "reason": self._reason,
        }


def get_communication_storage(
    *,
    environment: str | None = None,
    backend: str | None = None,
    database_url: str | None = None,
    file_base_path: Path | str = Path("data/comms"),
) -> CommunicationStorage:
    """Select storage without performing filesystem or network I/O."""

    settings = get_settings()
    environment = (environment or settings.app_env).strip().lower()
    selected_backend = (
        backend
        or os.getenv("DEALIX_COMMUNICATION_STORAGE_BACKEND", "").strip().lower()
        or ("postgres" if environment in {"staging", "production"} else "file")
    )

    if environment in {"staging", "production"} and selected_backend != "postgres":
        return UnavailableCommunicationStorage(f"{environment}_requires_postgres")
    if selected_backend == "file":
        return FileCommunicationStorage(file_base_path)
    if selected_backend != "postgres":
        return UnavailableCommunicationStorage("unsupported_storage_backend")

    raw_url = (database_url or settings.database_url or "").strip()
    if not raw_url:
        return UnavailableCommunicationStorage("database_url_missing")
    try:
        return PostgresCommunicationStorage(
            database_url=sync_sqlalchemy_url(raw_url),
            create_tables=False,
        )
    except Exception:
        return UnavailableCommunicationStorage("postgres_configuration_invalid")


__all__ = [
    "CommunicationCollection",
    "CommunicationSnapshotORM",
    "CommunicationStorage",
    "CommunicationStorageUnavailable",
    "FileCommunicationStorage",
    "PostgresCommunicationStorage",
    "UnavailableCommunicationStorage",
    "get_communication_storage",
]
