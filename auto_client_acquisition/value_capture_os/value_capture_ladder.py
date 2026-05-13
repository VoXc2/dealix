"""Value Capture Ladder — 10 commercial stages."""

from __future__ import annotations

from enum import IntEnum


class ValueCaptureStage(IntEnum):
    EDUCATION = 1
    PAID_DIAGNOSTIC = 2
    SPRINT = 3
    PILOT = 4
    RETAINER = 5
    MANAGED_PLATFORM = 6
    ENTERPRISE_PROGRAM = 7
    ACADEMY = 8
    PARTNER_REVENUE = 9
    VENTURE = 10


VALUE_CAPTURE_LADDER: tuple[ValueCaptureStage, ...] = tuple(ValueCaptureStage)
