"""V12 Compliance OS — structured action × consent_state policy matrix.

This is the ONE missing piece audit found in the existing
``compliance_os/`` + ``customer_data_plane/consent_registry`` stack:
a deterministic table that, given an action_type + channel +
consent_state, returns ``allowed`` / ``blocked`` / ``needs_review``
with a bilingual reason and an action_mode.

This module wraps (does not replace) the existing layers.
"""
from auto_client_acquisition.compliance_os_v12.action_policy import (
    ActionDecision,
    ActionVerdict,
    Channel,
    ConsentState,
    evaluate_action,
)

__all__ = [
    "ActionDecision",
    "ActionVerdict",
    "Channel",
    "ConsentState",
    "evaluate_action",
]
