"""Object storage contract for proof packs / artifacts (adapter-ready)."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, Field


class StoredObjectRef(BaseModel):
    """Pointer to an object in external or local storage."""

    bucket: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)
    content_type: str | None = None
    tenant_id: str = Field(..., min_length=1)


@runtime_checkable
class ObjectStorageContract(Protocol):
    """Implement in Phase E (e.g. MinIO, S3)."""

    def put_bytes(self, ref: StoredObjectRef, data: bytes) -> str: ...
    def get_bytes(self, ref: StoredObjectRef) -> bytes: ...
    def delete(self, ref: StoredObjectRef) -> None: ...
