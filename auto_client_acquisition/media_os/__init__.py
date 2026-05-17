"""Full Ops 2.0 — Media OS.

Authority/media capability. Currently hosts the GCC Governed AI Ops
Pulse — a quarterly, aggregated, anonymized report built from
governance risk-score signals.

DOCTRINE — the Pulse report is aggregate/anonymized only. It must never
expose an individual client's data without consent.
"""
from auto_client_acquisition.media_os.gcc_pulse import (
    GovernedAIOpsPulse,
    build_gcc_pulse,
)

__all__ = ["GovernedAIOpsPulse", "build_gcc_pulse"]
