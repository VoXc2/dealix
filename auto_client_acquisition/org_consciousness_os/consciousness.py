"""Top-level synthesis for ``org_consciousness_os``.

Runs Systems 36-45 in order and assembles a single
``OrgConsciousnessSnapshot``. Read-only synthesis + draft proposals.
"""

from __future__ import annotations

from auto_client_acquisition.capital_os.capital_ledger import CapitalLedgerEvent
from auto_client_acquisition.org_consciousness_os._common import utcnow_naive
from auto_client_acquisition.org_consciousness_os.causal import build_causal_report
from auto_client_acquisition.org_consciousness_os.learning import detect_learning_patterns
from auto_client_acquisition.org_consciousness_os.meta_orchestration import (
    recommend_meta_orchestration,
)
from auto_client_acquisition.org_consciousness_os.resilience import compute_resilience
from auto_client_acquisition.org_consciousness_os.schemas import (
    DOCTRINE_POSTURE,
    ExecutionHealthSignal,
    OrgConsciousnessSnapshot,
)
from auto_client_acquisition.org_consciousness_os.self_evolving import (
    propose_optimizations,
)
from auto_client_acquisition.org_consciousness_os.signals import compute_execution_health
from auto_client_acquisition.org_consciousness_os.strategic import benchmark_customer
from auto_client_acquisition.org_consciousness_os.trust import compute_trust
from auto_client_acquisition.org_consciousness_os.value import compute_operational_value
from auto_client_acquisition.org_consciousness_os.workforce_governance import (
    build_workforce_governance,
)
from auto_client_acquisition.proof_architecture_os.value_ledger import ValueLedgerEvent
from auto_client_acquisition.revenue_memory.event_store import EventStore


def synthesize_consciousness(
    *,
    customer_id: str,
    window_days: int = 30,
    store: EventStore | None = None,
    value_events: list[ValueLedgerEvent] | None = None,
    capital_events: list[CapitalLedgerEvent] | None = None,
    cohort_signals: dict[str, ExecutionHealthSignal] | None = None,
) -> OrgConsciousnessSnapshot:
    """Synthesize the full organizational-consciousness snapshot."""
    execution_health = compute_execution_health(
        customer_id=customer_id, window_days=window_days, store=store
    )
    causal = build_causal_report(customer_id=customer_id, window_days=window_days, store=store)
    workforce = build_workforce_governance(customer_id=customer_id)
    resilience = compute_resilience(customer_id=customer_id, window_days=window_days, store=store)
    trust = compute_trust(customer_id=customer_id)
    value = compute_operational_value(
        customer_id=customer_id,
        value_events=value_events,
        capital_events=capital_events,
        friction_window_days=window_days,
    )
    learning = detect_learning_patterns(customer_id=customer_id, window_days=window_days)
    meta = recommend_meta_orchestration(
        customer_id=customer_id, window_days=window_days, store=store
    )

    # Strategic: benchmark against the supplied cohort, or against a
    # single-customer cohort when none is provided.
    cohort = dict(cohort_signals or {})
    cohort[customer_id] = execution_health
    strategic = benchmark_customer(customer_id=customer_id, cohort_signals=cohort)

    proposals = propose_optimizations(
        customer_id=customer_id,
        learning=learning,
        resilience=resilience,
        workforce=workforce,
    )

    return OrgConsciousnessSnapshot(
        customer_id=customer_id,
        generated_at=utcnow_naive().isoformat(),
        window_days=window_days,
        execution_health=execution_health,
        causal=causal,
        workforce_governance=workforce,
        resilience=resilience,
        trust=trust,
        value=value,
        learning=learning,
        meta_orchestration=meta,
        strategic=strategic,
        evolution_proposals=tuple(proposals),
        doctrine=dict(DOCTRINE_POSTURE),
    )


__all__ = ["synthesize_consciousness"]
