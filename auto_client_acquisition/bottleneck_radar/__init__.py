"""Bottleneck Radar (Wave 13 Phase 9).

Founder/manager visibility layer — surfaces what's blocking revenue
in ONE single message, replacing 100-card dashboard overwhelm.

Per plan §32.4A.2.

Hard rule (Article 4): read-only; no external actions.
Article 8: today_single_action is text only; no fake_revenue numbers.
"""

from auto_client_acquisition.bottleneck_radar.computer import (
    compute_bottleneck,
    compute_founder_view,
)
from auto_client_acquisition.bottleneck_radar.schemas import (
    BottleneckSeverity,
    FounderBottleneck,
)

__all__ = [
    "BottleneckSeverity",
    "FounderBottleneck",
    "compute_bottleneck",
    "compute_founder_view",
]
