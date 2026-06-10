"""Source passport schema — aligns with docs/architecture/SOURCE_PASSPORT.md."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class SourcePassport:
    source_id: str
    source_type: str
    owner: str
    allowed_use: list[str]
    contains_pii: bool
    sensitivity: str
    relationship_status: str
    retention_policy: str
    ai_access_allowed: bool
    external_use_allowed: bool
    extra: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        base = asdict(self)
        extra = base.pop("extra", {}) or {}
        out = dict(base)
        out.update(extra)
        return out


def example_client_upload_passport() -> SourcePassport:
    return SourcePassport(
        source_id="SRC-001",
        source_type="client_upload",
        owner="client",
        allowed_use=["internal_analysis", "draft_only"],
        contains_pii=True,
        sensitivity="medium",
        relationship_status="existing_relationship",
        retention_policy="project_duration",
        ai_access_allowed=True,
        external_use_allowed=False,
    )
