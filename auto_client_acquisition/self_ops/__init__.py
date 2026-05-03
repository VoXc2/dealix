"""
Self-Ops — Dealix uses Dealix to grow Dealix.

The doctrine says "Dealix is a Revenue OS." If we sell it as full-ops to
customers, we should run it on ourselves. This module is the self-customer:

  - dealix_brain: Dealix's own Company Brain (offer, ICP, tone, channels)
  - runner: daily self-ops loop (creates own prospects, drafts, sprint)

Used by `scripts/cron_dealix_self_ops.py` + `/api/v1/self-ops/*` endpoints.
"""

from auto_client_acquisition.self_ops.dealix_brain import DEALIX_BRAIN
from auto_client_acquisition.self_ops.runner import (
    SelfOpsResult,
    daily_self_ops,
)

__all__ = ["DEALIX_BRAIN", "SelfOpsResult", "daily_self_ops"]
