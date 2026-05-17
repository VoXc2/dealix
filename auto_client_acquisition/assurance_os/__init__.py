"""Dealix Assurance System — a unification layer over existing Dealix
infrastructure that runs the 7-layer assurance pipeline:

    Gate -> Scorecard -> Test -> Evidence -> KPI -> Review -> Improvement

It does not rebuild any machine; it reads existing scorecards, gates,
evidence and KPI sources through pluggable adapters and emits one
composite AssuranceReport with a Full Ops Health Score and a binary
scale / no-scale verdict. Unwired data sources surface as ``unknown`` —
never fabricated values (doctrine: no fake data, no fake proof).
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.assurance_system import (
    LAYERS,
    run_assurance,
)
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    AssuranceReport,
    Status,
)

__all__ = [
    "LAYERS",
    "run_assurance",
    "AssuranceInputs",
    "AssuranceReport",
    "Status",
]
