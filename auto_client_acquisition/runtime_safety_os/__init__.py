"""System 31 — Enterprise Safety Engine.

Circuit breakers, kill switches, execution limits for runtime operational safety.
"""

from auto_client_acquisition.runtime_safety_os.core import (
    SafetyEngine,
    SafetyError,
    get_safety_engine,
    reset_safety_engine,
)
from auto_client_acquisition.runtime_safety_os.schemas import (
    CircuitBreaker,
    CircuitState,
    ExecutionLimit,
    KillSwitch,
    SafetyVerdict,
)

__all__ = [
    "CircuitBreaker",
    "CircuitState",
    "ExecutionLimit",
    "KillSwitch",
    "SafetyEngine",
    "SafetyError",
    "SafetyVerdict",
    "get_safety_engine",
    "reset_safety_engine",
]
