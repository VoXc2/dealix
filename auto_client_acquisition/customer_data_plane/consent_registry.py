"""In-process consent registry.

Thread-safe append-only store for ``ConsentRecord``. The public API
matches what a future Postgres-backed implementation would expose,
so the swap is mechanical when the DB ships.
"""
from __future__ import annotations

import threading
from collections.abc import Iterable
from datetime import UTC, datetime

from auto_client_acquisition.customer_data_plane.schemas import (
    ChannelKind,
    ConsentRecord,
    ConsentSource,
    ConsentStatus,
)


class ConsentRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: list[ConsentRecord] = []

    def grant(
        self,
        contact_id: str,
        channel: ChannelKind | str,
        source: ConsentSource | str = ConsentSource.WEBSITE_FORM,
        purposes: Iterable[str] | None = None,
        method_note: str = "",
        evidence_id: str | None = None,
    ) -> ConsentRecord:
        rec = ConsentRecord(
            contact_id=str(contact_id),
            channel=channel if isinstance(channel, ChannelKind) else ChannelKind(channel),
            consent_status=ConsentStatus.GRANTED,
            consent_source=source if isinstance(source, ConsentSource) else ConsentSource(source),
            consent_method_note=method_note,
            allowed_purposes=list(purposes or []),
            evidence_id=evidence_id,
        )
        with self._lock:
            self._records.append(rec)
        return rec

    def withdraw(
        self,
        contact_id: str,
        channel: ChannelKind | str | None = None,
    ) -> list[ConsentRecord]:
        """Mark every active consent for the contact as withdrawn.

        If ``channel`` is given, only that channel's consents are
        withdrawn. Returns the list of withdrawn records.
        """
        ch = (
            None if channel is None
            else (channel if isinstance(channel, ChannelKind) else ChannelKind(channel))
        )
        out: list[ConsentRecord] = []
        with self._lock:
            for i, rec in enumerate(self._records):
                if rec.contact_id != str(contact_id):
                    continue
                if ch is not None and rec.channel != ch.value:
                    continue
                if rec.withdrawal_timestamp is not None:
                    continue
                replacement = rec.model_copy(update={
                    "withdrawal_timestamp": datetime.now(UTC),
                    "consent_status": ConsentStatus.WITHDRAWN.value,
                })
                self._records[i] = replacement
                out.append(replacement)
        return out

    def status_for(
        self,
        contact_id: str,
        channel: ChannelKind | str,
    ) -> tuple[ConsentStatus, ConsentRecord | None]:
        ch = channel if isinstance(channel, ChannelKind) else ChannelKind(channel)
        with self._lock:
            relevant = [
                r for r in self._records
                if r.contact_id == str(contact_id) and r.channel == ch.value
            ]
        if not relevant:
            return ConsentStatus.UNKNOWN, None
        # If any active grant exists, status is granted.
        active = next(
            (r for r in reversed(relevant) if r.is_active()),
            None,
        )
        if active is not None:
            return ConsentStatus.GRANTED, active
        # Otherwise return the most recent record (likely withdrawn).
        latest = relevant[-1]
        return ConsentStatus(latest.consent_status), latest

    def all_records(self) -> list[ConsentRecord]:
        with self._lock:
            return list(self._records)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


# Module-level default registry (process-scoped).
_DEFAULT = ConsentRegistry()


def get_default_registry() -> ConsentRegistry:
    return _DEFAULT
