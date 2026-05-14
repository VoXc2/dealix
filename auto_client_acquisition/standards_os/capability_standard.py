"""D-GAOS — Capability Diagnostic standard (aligned with client capability model)."""

from __future__ import annotations

from auto_client_acquisition.client_os.capability_dashboard import (
    CAPABILITY_DOMAINS,
    CAPABILITY_LEVEL_MAX,
    capability_level_valid,
)

__all__ = ("CAPABILITY_DOMAINS", "CAPABILITY_LEVEL_MAX", "capability_level_valid")
