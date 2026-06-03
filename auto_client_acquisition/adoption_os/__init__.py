"""Enterprise adoption & change management — deterministic adoption economics."""

from __future__ import annotations

from auto_client_acquisition.adoption_os.adoption_dashboard import (
    ADOPTION_DASHBOARD_SIGNALS,
    adoption_dashboard_coverage_score,
)
from auto_client_acquisition.adoption_os.adoption_review import (
    ADOPTION_REVIEW_SIGNALS,
    ONBOARDING_PHASES,
    AdoptionOutcome,
    adoption_review_coverage_score,
    onboarding_phase_index,
)
from auto_client_acquisition.adoption_os.adoption_score import (
    AdoptionDimensions,
    adoption_band,
    adoption_score,
)
from auto_client_acquisition.adoption_os.client_roles import (
    CLIENT_ADOPTION_ROLES,
    ENABLEMENT_KIT_ITEMS,
    enablement_kit_coverage_score,
)
from auto_client_acquisition.adoption_os.friction_log import (
    FRICTION_TYPES,
    FrictionEvent,
    friction_event_valid,
    friction_type_known,
)
from auto_client_acquisition.adoption_os.retainer_readiness import (
    AdoptionRetainerReadiness,
    adoption_retainer_readiness_passes,
    wave2_retainer_eligibility,
)
from auto_client_acquisition.adoption_os.training_products import (
    TRAINING_PRODUCT_SLUGS,
    training_product_known,
)

__all__ = (
    "ADOPTION_DASHBOARD_SIGNALS",
    "ADOPTION_REVIEW_SIGNALS",
    "CLIENT_ADOPTION_ROLES",
    "ENABLEMENT_KIT_ITEMS",
    "FRICTION_TYPES",
    "ONBOARDING_PHASES",
    "TRAINING_PRODUCT_SLUGS",
    "AdoptionDimensions",
    "AdoptionOutcome",
    "AdoptionRetainerReadiness",
    "FrictionEvent",
    "adoption_band",
    "adoption_dashboard_coverage_score",
    "adoption_retainer_readiness_passes",
    "adoption_review_coverage_score",
    "adoption_score",
    "enablement_kit_coverage_score",
    "friction_event_valid",
    "friction_type_known",
    "onboarding_phase_index",
    "training_product_known",
    "wave2_retainer_eligibility",
)
