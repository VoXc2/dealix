"""Master scorecard field registries (deterministic keys, no I/O)."""

from auto_client_acquisition.scorecards.business_unit_scorecard import (
    BUSINESS_UNIT_SCORECARD_FIELDS,
)
from auto_client_acquisition.scorecards.client_scorecard import CLIENT_SCORECARD_FIELDS
from auto_client_acquisition.scorecards.group_scorecard import GROUP_SCORECARD_FIELDS
from auto_client_acquisition.scorecards.project_scorecard import PROJECT_SCORECARD_FIELDS
from auto_client_acquisition.scorecards.service_scorecard import SERVICE_SCORECARD_FIELDS

__all__ = [
    "BUSINESS_UNIT_SCORECARD_FIELDS",
    "CLIENT_SCORECARD_FIELDS",
    "GROUP_SCORECARD_FIELDS",
    "PROJECT_SCORECARD_FIELDS",
    "SERVICE_SCORECARD_FIELDS",
]
