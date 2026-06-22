from __future__ import annotations

from .schemas import SignalRecord


def intent_score(signals: list[SignalRecord]) -> int:
    total = sum(signal.weight for signal in signals if signal.detected)
    return min(total, 100)