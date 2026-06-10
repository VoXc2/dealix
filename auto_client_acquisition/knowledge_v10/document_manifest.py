"""Manifest validation."""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import DocumentManifest


def validate_manifest(manifest: DocumentManifest | dict) -> DocumentManifest:
    """Coerce + validate. Pydantic v2 raises on bad shapes."""
    if isinstance(manifest, DocumentManifest):
        return manifest
    return DocumentManifest.model_validate(manifest)
