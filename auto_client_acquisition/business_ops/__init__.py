# Wave 9 Business Operations OS
# Action modes: suggest_only / draft_only / approval_required / approved_manual / blocked
# Hard rules: no live WhatsApp/Gmail/LinkedIn/Moyasar, no scraping, no fake proof/revenue
from .stage_definitions import STAGES, JourneyStage

__all__ = [
    "STAGES",
    "JourneyStage",
]
