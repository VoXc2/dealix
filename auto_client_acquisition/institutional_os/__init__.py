"""Institutional OS — laws, institutions, economy, defense constants."""

from auto_client_acquisition.institutional_os.defense import DEFENSE_LAYERS
from auto_client_acquisition.institutional_os.economy import ECONOMY_CURRENCIES
from auto_client_acquisition.institutional_os.institutions import DEALIX_INSTITUTIONS
from auto_client_acquisition.institutional_os.laws import DEALIX_LAWS, LawRef

__all__ = [
    "DEALIX_INSTITUTIONS",
    "DEALIX_LAWS",
    "DEFENSE_LAYERS",
    "ECONOMY_CURRENCIES",
    "LawRef",
]
