"""System 28 — Assurance Contract Engine.

Contracts that gate what every agent action may see / propose / execute.
"""

from auto_client_acquisition.assurance_contract_os.core import (
    ContractEngine,
    ContractError,
    get_contract_engine,
    reset_contract_engine,
)
from auto_client_acquisition.assurance_contract_os.schemas import (
    AssuranceContract,
    ContractCheckResult,
    ContractDecision,
    ContractType,
)

__all__ = [
    "AssuranceContract",
    "ContractCheckResult",
    "ContractDecision",
    "ContractEngine",
    "ContractError",
    "ContractType",
    "get_contract_engine",
    "reset_contract_engine",
]
