"""Wave 4 Integration Upgrade — non-breaking adapter shim.

Lets every new module call into existing Dealix modules safely:
- missing module → degraded section (never exception)
- failing call → degraded section
- internal terms → stripped before customer output

This shim is the foundation for the 7 new Wave 4 modules
(unified_operating_graph, full_ops_radar, executive_command_center,
whatsapp_decision_bot, channel_policy_gateway, radar_events,
agent_observability).
"""
from auto_client_acquisition.integration_upgrade.adapters import (
    safe_call,
)
from auto_client_acquisition.integration_upgrade.contract_status import (
    contract_status,
)
from auto_client_acquisition.integration_upgrade.customer_safe_labels import (
    customer_safe_label,
    hide_internal_terms,
)
from auto_client_acquisition.integration_upgrade.degraded import (
    degraded_section,
)
from auto_client_acquisition.integration_upgrade.safe_imports import (
    safe_import,
)

__all__ = [
    "contract_status",
    "customer_safe_label",
    "degraded_section",
    "hide_internal_terms",
    "safe_call",
    "safe_import",
]
