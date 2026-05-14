"""Canonical Value OS — tier-aware value ledger + monthly value report.

Value tiers (no auto-promotion ever):
  estimated         → model-derived range; NEVER externally claimable
  observed          → measured inside a Dealix workflow
  verified          → cross-checked vs client data; requires source_ref
  client_confirmed  → Verified + a signed confirmation_ref; case-study eligible
"""
from auto_client_acquisition.value_os.value_ledger import (
    ValueDisciplineError,
    ValueEvent,
    add_event,
    clear_for_test,
    list_events,
    summarize,
)
from auto_client_acquisition.value_os.monthly_report import (
    MonthlyValueReport,
    generate,
)

__all__ = [
    "MonthlyValueReport",
    "ValueDisciplineError",
    "ValueEvent",
    "add_event",
    "clear_for_test",
    "generate",
    "list_events",
    "summarize",
]
