"""Connector base — every connector must subclass this."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ConnectorManifest:
    name: str
    source_type: str
    allowed_use: str
    restricted_use: list[str] = field(default_factory=list)
    human_review_required: bool = True
    terms_review_required: bool = True
    auto_send_allowed: bool = False
    risk_level: str = "low"  # low | medium | high
    notes: str = ""


class BaseConnector(ABC):
    manifest: ConnectorManifest

    def __init__(self, root: Path | None = None):
        self.root = root or Path(__file__).resolve().parents[1]

    @abstractmethod
    def fetch_or_load(self) -> list[dict]: ...

    @abstractmethod
    def normalize(self, raw: list[dict]) -> list[dict]: ...

    @abstractmethod
    def validate(self, record: dict) -> bool: ...

    def audit_source(self) -> dict:
        return {
            "name": self.manifest.name,
            "source_type": self.manifest.source_type,
            "risk_level": self.manifest.risk_level,
            "auto_send_allowed": self.manifest.auto_send_allowed,
            "human_review_required": self.manifest.human_review_required,
            "notes": self.manifest.notes,
        }
