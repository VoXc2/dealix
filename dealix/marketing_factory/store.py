"""JSON persistence for marketing calendar + UTM links."""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import TypeAdapter

from dealix.marketing_factory.schemas import CalendarSlotRecord, UtmLinkRecord

_DEFAULT_PATH_ENV = "DEALIX_MARKETING_FACTORY_STORE"
_SLOTS_TA = TypeAdapter(list[CalendarSlotRecord])
_UTM_TA = TypeAdapter(list[UtmLinkRecord])


def default_marketing_store_path() -> Path:
    raw = os.environ.get(_DEFAULT_PATH_ENV, "")
    if raw.strip():
        p = Path(raw)
    else:
        p = Path(__file__).resolve().parents[2] / "var" / "marketing_factory.json"
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _seed_path() -> Path:
    return Path(__file__).resolve().parent / "content_calendar.seed.yaml"


def uid(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


class MarketingJSONStore:
    def __init__(self, path: Path | None = None) -> None:
        self._path = path or default_marketing_store_path()
        self._lock = threading.Lock()

    def _read_raw(self) -> dict[str, Any]:
        if not self._path.exists():
            return self._empty_blob()
        try:
            return json.loads(self._path.read_text(encoding="utf-8"))
        except Exception:
            return self._empty_blob()

    @staticmethod
    def _empty_blob() -> dict[str, Any]:
        return {
            "version": 1,
            "calendar_slots": [],
            "utm_links": [],
        }

    def _write_atomic(self, data: dict[str, Any]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        data["generated_at"] = datetime.now(UTC).isoformat()
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        tmp.replace(self._path)

    def _mutate(self, fn: Any) -> Any:
        with self._lock:
            blob = self._read_raw()
            out = fn(blob)
            self._write_atomic(blob)
            return out

    def ensure_seed_loaded(self) -> int:
        """Load YAML seed once if store empty."""

        def _fn(blob: dict[str, Any]) -> int:
            existing = _SLOTS_TA.validate_python(blob.get("calendar_slots") or [])
            if existing:
                return 0
            seed = yaml.safe_load(_seed_path().read_text(encoding="utf-8"))
            added = 0
            for row in seed.get("slots") or []:
                slot = CalendarSlotRecord(
                    id=uid("cal"),
                    scheduled_date=str(row.get("scheduled_date") or ""),
                    channel=str(row.get("channel") or "linkedin"),
                    title_ar=str(row.get("title_ar") or ""),
                    body_draft_ar=str(row.get("body_draft_ar") or ""),
                    cta_label_ar=str(row.get("cta_label_ar") or ""),
                    cta_path=str(row.get("cta_path") or "/dealix-diagnostic"),
                    utm_campaign=str(row.get("utm_campaign") or ""),
                    utm_medium=str(row.get("utm_medium") or "social"),
                    utm_source=str(row.get("utm_source") or "dealix"),
                    status=row.get("status") or "draft",
                )
                existing.append(slot)
                added += 1
            blob["calendar_slots"] = [x.model_dump(mode="json") for x in existing]
            return added

        return self._mutate(_fn)

    def list_calendar(self, limit: int = 120) -> list[CalendarSlotRecord]:
        blob = self._read_raw()
        rows = _SLOTS_TA.validate_python(blob.get("calendar_slots") or [])
        rows.sort(key=lambda x: x.scheduled_date)
        return rows[:limit]

    def upsert_calendar_slot(self, slot: CalendarSlotRecord) -> CalendarSlotRecord:
        def _fn(blob: dict[str, Any]) -> CalendarSlotRecord:
            rows = _SLOTS_TA.validate_python(blob.get("calendar_slots") or [])
            rest = [x for x in rows if x.id != slot.id]
            rest.append(slot)
            blob["calendar_slots"] = [x.model_dump(mode="json") for x in rest]
            return slot

        return self._mutate(_fn)

    def list_utm_links(self, limit: int = 80) -> list[UtmLinkRecord]:
        blob = self._read_raw()
        rows = _UTM_TA.validate_python(blob.get("utm_links") or [])
        rows.sort(key=lambda x: x.created_at, reverse=True)
        return rows[:limit]

    def append_utm_link(self, link: UtmLinkRecord) -> UtmLinkRecord:
        def _fn(blob: dict[str, Any]) -> UtmLinkRecord:
            rows = _UTM_TA.validate_python(blob.get("utm_links") or [])
            rows.append(link)
            blob["utm_links"] = [x.model_dump(mode="json") for x in rows]
            return link

        return self._mutate(_fn)

    def stats(self) -> dict[str, Any]:
        slots = self.list_calendar(limit=500)
        utms = self.list_utm_links(limit=500)
        approved = sum(1 for s in slots if s.status in {"approved", "published_manual"})
        with_utm = sum(1 for s in slots if s.utm_campaign)
        return {
            "calendar_total": len(slots),
            "calendar_approved_or_published": approved,
            "calendar_with_utm_campaign": with_utm,
            "utm_links_total": len(utms),
        }


_default_singleton: MarketingJSONStore | None = None
_singleton_lock = threading.Lock()


def get_marketing_store() -> MarketingJSONStore:
    global _default_singleton
    if _default_singleton is None:
        with _singleton_lock:
            if _default_singleton is None:
                st = MarketingJSONStore()
                st.ensure_seed_loaded()
                _default_singleton = st
    return _default_singleton


def reset_marketing_store_for_tests(path: Path | None = None) -> MarketingJSONStore:
    global _default_singleton
    st = MarketingJSONStore(path=path)
    _default_singleton = st
    return st
