"""Commercial Evidence State Machine (CEL).

Canonical backend for `docs/commercial/COMMERCIAL_EVIDENCE_STATE_MACHINE.md`
and `docs/commercial/COMMERCIAL_GATES.md`.

CEL is an axis orthogonal to the L0-L5 proof/autonomy axis: it tracks how far
a commercial engagement has progressed and what recorded evidence proves it.
"""

from __future__ import annotations

from auto_client_acquisition.commercial_os.cel import (
    CEL_LEVELS,
    COMMERCIAL_STATES,
    STATE_TO_CEL,
    CommercialEvidenceLevel,
    CommercialState,
)
from auto_client_acquisition.commercial_os.engine import (
    CommercialEngine,
    RecordedTransition,
)
from auto_client_acquisition.commercial_os.gates import GateStatus, evaluate_gates
from auto_client_acquisition.commercial_os.market_proof import (
    record_meeting_used,
    record_prepared,
    record_reply_classified,
    record_sent,
)
from auto_client_acquisition.commercial_os.projections import current_commercial_state
from auto_client_acquisition.commercial_os.transitions import (
    TransitionResult,
    validate_transition,
)

__all__ = [
    "CEL_LEVELS",
    "COMMERCIAL_STATES",
    "STATE_TO_CEL",
    "CommercialEngine",
    "CommercialEvidenceLevel",
    "CommercialState",
    "GateStatus",
    "RecordedTransition",
    "TransitionResult",
    "current_commercial_state",
    "evaluate_gates",
    "record_meeting_used",
    "record_prepared",
    "record_reply_classified",
    "record_sent",
    "validate_transition",
]
