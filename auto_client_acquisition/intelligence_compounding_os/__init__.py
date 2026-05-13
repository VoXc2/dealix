"""Dealix Intelligence Compounding OS — typed signals and confidence."""

from __future__ import annotations

from auto_client_acquisition.intelligence_compounding_os.pattern_confidence import (
    PatternConfidence,
    classify_confidence,
)
from auto_client_acquisition.intelligence_compounding_os.signal import (
    IntelligenceSignal,
    SignalKind,
)

__all__ = [
    "PatternConfidence",
    "classify_confidence",
    "IntelligenceSignal",
    "SignalKind",
]
