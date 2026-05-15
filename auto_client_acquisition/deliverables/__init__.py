"""Dealix Deliverable Entity (Wave 13 Phase 4).

First-class entity for every customer-visible service output.
Decoupled from ServiceSessionRecord (Article 11: ServiceSessionRecord
shape preserved; deliverables become a separate first-class entity).

Article 4: customer_visible=False blocks portal display.
Article 8: proof_related=True only when paired with proof_engine event.
"""

from auto_client_acquisition.deliverables.lifecycle import (
    DELIVERABLE_TRANSITIONS,
    InvalidTransitionError,
    advance,
    is_terminal,
)
from auto_client_acquisition.deliverables.schemas import (
    Deliverable,
    DeliverableStatus,
    DeliverableType,
)
from auto_client_acquisition.deliverables.store import (
    create_deliverable,
    get_deliverable,
    list_by_session,
)

__all__ = [
    "DELIVERABLE_TRANSITIONS",
    "Deliverable",
    "DeliverableStatus",
    "DeliverableType",
    "InvalidTransitionError",
    "advance",
    "create_deliverable",
    "get_deliverable",
    "is_terminal",
    "list_by_session",
]
