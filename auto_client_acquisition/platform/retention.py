"""Retention policy helpers by sensitivity tier."""

from __future__ import annotations

from auto_client_acquisition.platform.memory_governance import MemorySensitivity


def retention_window_seconds(sensitivity: MemorySensitivity) -> int:
    if sensitivity == MemorySensitivity.PUBLIC:
        return 365 * 24 * 3600
    if sensitivity == MemorySensitivity.INTERNAL:
        return 180 * 24 * 3600
    if sensitivity == MemorySensitivity.CONFIDENTIAL:
        return 90 * 24 * 3600
    return 30 * 24 * 3600


def should_purge(*, now_epoch: int, created_at_epoch: int, sensitivity: MemorySensitivity, legal_hold: bool) -> bool:
    if legal_hold:
        return False
    return now_epoch - created_at_epoch > retention_window_seconds(sensitivity)


__all__ = ['retention_window_seconds', 'should_purge']
