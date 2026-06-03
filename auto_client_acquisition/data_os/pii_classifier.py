"""PII classification helpers (Data OS facade over pii_detection)."""

from __future__ import annotations

from auto_client_acquisition.data_os.pii_detection import (
    column_name_suggests_pii,
    pii_flags_for_row,
)

__all__ = ["column_name_suggests_pii", "pii_flags_for_row"]
