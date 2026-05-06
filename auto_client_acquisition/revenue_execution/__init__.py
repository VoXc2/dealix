"""Revenue execution facade — read-only composition for founder daily ops."""

from .daily_snapshot import build_daily_command_center

__all__ = ["build_daily_command_center"]
