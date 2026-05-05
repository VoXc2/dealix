"""Service Mapping v7 — customer goal → recommended Dealix service.

Pure deterministic mapping. No LLM calls, no external HTTP.

Public API:
    from auto_client_acquisition.service_mapping_v7 import (
        MapRequest, ServiceRecommendation,
        map_goal_to_service, value_ladder,
    )
"""
from auto_client_acquisition.service_mapping_v7.mapper import map_goal_to_service
from auto_client_acquisition.service_mapping_v7.schemas import (
    MapRequest,
    ServiceRecommendation,
)
from auto_client_acquisition.service_mapping_v7.value_ladder import value_ladder

__all__ = [
    "MapRequest",
    "ServiceRecommendation",
    "map_goal_to_service",
    "value_ladder",
]
