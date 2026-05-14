"""Global kill switch flag (in-process; callers persist externally for production)."""

from __future__ import annotations

_KILLED: bool = False


def kill_switch_active() -> bool:
    return _KILLED


def activate_kill_switch() -> None:
    global _KILLED
    _KILLED = True


def reset_kill_switch_for_tests() -> None:
    global _KILLED
    _KILLED = False


__all__ = ["activate_kill_switch", "kill_switch_active", "reset_kill_switch_for_tests"]
