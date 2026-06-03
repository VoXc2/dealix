"""Customer Loop v5 — repeatable journey over the existing infra.

Composes pieces already in the repo (founder alert, diagnostic
checklist, Moyasar invoice CLI, proof_snippet_engine,
service_activation_matrix) into a single state machine over the
customer's journey:

    lead_intake → diagnostic_requested → diagnostic_sent
    → pilot_offered → payment_pending → paid_or_committed
    → in_delivery → proof_pack_ready → proof_pack_sent
    → upsell_recommended

Every state advance returns a typed checklist of NEXT actions —
none of them external sends. The founder/operator carries out
each action manually until proven safe, per the hard rules.
"""
from auto_client_acquisition.customer_loop.customer_journey import (
    advance,
    list_states,
    next_actions_for_state,
)
from auto_client_acquisition.customer_loop.schemas import (
    JourneyAdvanceRequest,
    JourneyAdvanceResult,
    JourneyState,
    JourneyTransition,
)

__all__ = [
    "JourneyAdvanceRequest",
    "JourneyAdvanceResult",
    "JourneyState",
    "JourneyTransition",
    "advance",
    "list_states",
    "next_actions_for_state",
]
