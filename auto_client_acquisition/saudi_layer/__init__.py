"""Saudi / Arabic intelligence layer (deterministic helpers)."""

from __future__ import annotations

from auto_client_acquisition.saudi_layer.arabic_qa import ArabicQADimensions, arabic_qa_score
from auto_client_acquisition.saudi_layer.arabic_style import STYLE_RULES_AR
from auto_client_acquisition.saudi_layer.bilingual_reports import BILINGUAL_REPORT_KEYS, bilingual_report_complete
from auto_client_acquisition.saudi_layer.city_region_normalizer import normalize_saudi_city
from auto_client_acquisition.saudi_layer.forbidden_claims import forbidden_arabic_claim_detected
from auto_client_acquisition.saudi_layer.pdpl_aware_language import PDPL_HINT_AR
from auto_client_acquisition.saudi_layer.proof_safe_language import PROOF_SAFE_PHRASE_AR
from auto_client_acquisition.saudi_layer.saudi_sector_taxonomy import SAUDI_B2B_SECTORS, sector_known
from auto_client_acquisition.saudi_layer.whatsapp_boundary import WHATSAPP_POSTURE_AR

__all__ = [
    "BILINGUAL_REPORT_KEYS",
    "PDPL_HINT_AR",
    "PROOF_SAFE_PHRASE_AR",
    "SAUDI_B2B_SECTORS",
    "STYLE_RULES_AR",
    "WHATSAPP_POSTURE_AR",
    "ArabicQADimensions",
    "arabic_qa_score",
    "bilingual_report_complete",
    "forbidden_arabic_claim_detected",
    "normalize_saudi_city",
    "sector_known",
]
