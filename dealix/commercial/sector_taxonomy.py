"""Saudi sector taxonomy — internal structural mapping for sector company cells.

ISIC Rev.4 section-level mapping plus an internal Saudi strategic overlay.
Both are PATTERN knowledge, not customer facts, and both carry an explicit
validation status: section-level mapping still requires official class-level
validation before any external or regulatory use.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector

UNKNOWN = "UNKNOWN"
SECTION_MAPPING_STATUS = "ISIC_REV4_SECTION_LEVEL_INTERNAL_MAPPING_UNVALIDATED"
SAUDI_MAPPING_STATUS = "SAUDI_STRATEGIC_OVERLAY_INTERNAL_UNVALIDATED"

ISIC_SECTIONS: dict[str, str] = {
    "A": "Agriculture, forestry and fishing",
    "B": "Mining and quarrying",
    "C": "Manufacturing",
    "D": "Electricity, gas, steam and air conditioning supply",
    "E": "Water supply; sewerage, waste management and remediation activities",
    "F": "Construction",
    "G": "Wholesale and retail trade; repair of motor vehicles and motorcycles",
    "H": "Transportation and storage",
    "I": "Accommodation and food service activities",
    "J": "Information and communication",
    "K": "Financial and insurance activities",
    "L": "Real estate activities",
    "M": "Professional, scientific and technical activities",
    "N": "Administrative and support service activities",
    "O": "Public administration and defence; compulsory social security",
    "P": "Education",
    "Q": "Human health and social work activities",
    "R": "Arts, entertainment and recreation",
    "S": "Other service activities",
    "T": "Activities of households as employers",
    "U": "Activities of extraterritorial organizations and bodies",
}

# Primary ISIC section first. Section-level only; class-level mapping is a later,
# official-source-validated step.
SECTOR_ISIC: dict[Sector, list[str]] = {
    Sector.GOVERNMENT_B2G: ["O"],
    Sector.CONSTRUCTION_EPC: ["F"],
    Sector.INDUSTRIAL_MANUFACTURING: ["C"],
    Sector.LOGISTICS_SUPPLY_CHAIN: ["H"],
    Sector.ENERGY_UTILITIES_OIL_GAS: ["D", "B"],
    Sector.MINING_METALS: ["B"],
    Sector.REAL_ESTATE_PROPTECH: ["L", "N"],
    Sector.HEALTHCARE: ["Q"],
    Sector.FINANCE_FINTECH_INSURANCE: ["K"],
    Sector.RETAIL_COMMERCE_ECOMMERCE: ["G"],
    Sector.TOURISM_HOSPITALITY: ["I"],
    Sector.PROFESSIONAL_SERVICES: ["M"],
    Sector.TECHNOLOGY_SAAS_SI: ["J"],
    Sector.TELECOM_MEDIA_MARKETING: ["J", "M"],
    Sector.EDUCATION_TRAINING: ["P"],
    Sector.AGRICULTURE_FOOD_WATER: ["A", "E"],
    Sector.MOBILITY_AUTOMOTIVE: ["H", "G"],
    Sector.EXPORT_IMPORT_RHQ: ["G", "M"],
    Sector.CREATIVE_SPORTS_GAMING: ["R", "J"],
    Sector.ASSOCIATIONS_NONPROFITS: ["S", "T"],
}

# Internal overlay only. Program names are reference labels for prioritization,
# never a claim of official alignment, access, or endorsement.
SAUDI_STRATEGIC_OVERLAY: dict[Sector, list[str]] = {
    Sector.GOVERNMENT_B2G: ["Government transformation", "Digital government"],
    Sector.CONSTRUCTION_EPC: ["Housing and infrastructure delivery"],
    Sector.INDUSTRIAL_MANUFACTURING: ["National industrial development"],
    Sector.LOGISTICS_SUPPLY_CHAIN: ["Logistics and transport"],
    Sector.ENERGY_UTILITIES_OIL_GAS: ["Energy sustainability"],
    Sector.MINING_METALS: ["Mining and mineral wealth"],
    Sector.REAL_ESTATE_PROPTECH: ["Housing programme"],
    Sector.HEALTHCARE: ["Health sector transformation"],
    Sector.FINANCE_FINTECH_INSURANCE: ["Financial sector development"],
    Sector.RETAIL_COMMERCE_ECOMMERCE: ["Private sector and retail enablement"],
    Sector.TOURISM_HOSPITALITY: ["Tourism and hospitality"],
    Sector.PROFESSIONAL_SERVICES: ["Private sector enablement"],
    Sector.TECHNOLOGY_SAAS_SI: ["Digital economy and innovation"],
    Sector.TELECOM_MEDIA_MARKETING: ["Digital economy and media"],
    Sector.EDUCATION_TRAINING: ["Human capability development"],
    Sector.AGRICULTURE_FOOD_WATER: ["Food and water security"],
    Sector.MOBILITY_AUTOMOTIVE: ["Transport and mobility"],
    Sector.EXPORT_IMPORT_RHQ: ["Regional headquarters and export enablement"],
    Sector.CREATIVE_SPORTS_GAMING: ["Entertainment, sports and quality of life"],
    Sector.ASSOCIATIONS_NONPROFITS: ["Civil society enablement"],
}

# Regulator labels are pattern references for research planning only. Every entry
# must be verified against the official regulator before external use.
SECTOR_REGULATORS: dict[Sector, list[str]] = {
    Sector.GOVERNMENT_B2G: ["NCA", "SDAIA", "PDPL", "Etimad", "GAZT/ZATCA"],
    Sector.CONSTRUCTION_EPC: ["Saudi Contractors Authority", "PDPL", "ZATCA"],
    Sector.INDUSTRIAL_MANUFACTURING: ["MODON", "SASO", "ZATCA"],
    Sector.LOGISTICS_SUPPLY_CHAIN: ["TGA", "ZATCA", "SASO"],
    Sector.ENERGY_UTILITIES_OIL_GAS: ["NCA", "ECRA", "PDPL"],
    Sector.MINING_METALS: ["Ministry of Industry and Mineral Resources", "ZATCA"],
    Sector.REAL_ESTATE_PROPTECH: ["REGA", "Ejar", "ZATCA"],
    Sector.HEALTHCARE: ["MOH", "SFDA", "CHI", "Nupco", "PDPL"],
    Sector.FINANCE_FINTECH_INSURANCE: ["SAMA", "CMA", "NCA", "ZATCA", "PDPL"],
    Sector.RETAIL_COMMERCE_ECOMMERCE: ["MC", "ZATCA", "SASO", "PDPL"],
    Sector.TOURISM_HOSPITALITY: ["Ministry of Tourism", "ZATCA"],
    Sector.PROFESSIONAL_SERVICES: ["SOCPA", "ZATCA", "PDPL"],
    Sector.TECHNOLOGY_SAAS_SI: ["CST", "NCA", "SDAIA", "PDPL"],
    Sector.TELECOM_MEDIA_MARKETING: ["CST", "GAMR", "PDPL"],
    Sector.EDUCATION_TRAINING: ["ETEC", "Ministry of Education", "TETC"],
    Sector.AGRICULTURE_FOOD_WATER: ["MEA", "SFDA", "SWA"],
    Sector.MOBILITY_AUTOMOTIVE: ["TGA", "SASO", "ZATCA"],
    Sector.EXPORT_IMPORT_RHQ: ["MISA", "RHQ Programme", "ZATCA", "GAZT"],
    Sector.CREATIVE_SPORTS_GAMING: ["GEA", "Ministry of Sport", "GAMR"],
    Sector.ASSOCIATIONS_NONPROFITS: ["NCVAE", "Ministry of Human Resources"],
}


class TaxonomyRef(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    isic_sections: list[str] = Field(default_factory=list)
    isic_section_names: list[str] = Field(default_factory=list)
    isic_mapping_status: str = SECTION_MAPPING_STATUS
    saudi_strategic_overlay: list[str] = Field(default_factory=list)
    saudi_mapping_status: str = SAUDI_MAPPING_STATUS
    regulator_labels: list[str] = Field(default_factory=list)
    truth_class: str = "PATTERN"
    is_customer_fact: bool = False
    validation_required: bool = True


def taxonomy_for(sector: Sector) -> TaxonomyRef:
    sections = SECTOR_ISIC.get(sector, [])
    return TaxonomyRef(
        isic_sections=sections,
        isic_section_names=[ISIC_SECTIONS.get(section, UNKNOWN) for section in sections],
        saudi_strategic_overlay=SAUDI_STRATEGIC_OVERLAY.get(sector, []),
        regulator_labels=SECTOR_REGULATORS.get(sector, []),
    )


def coverage() -> dict[str, Any]:
    mapped = [sector.value for sector in Sector if sector in SECTOR_ISIC]
    return {
        "sectors_total": len(list(Sector)),
        "sectors_with_isic_section": len(mapped),
        "sectors_missing_isic_section": sorted({s.value for s in Sector} - set(mapped)),
        "isic_mapping_status": SECTION_MAPPING_STATUS,
        "saudi_mapping_status": SAUDI_MAPPING_STATUS,
    }


__all__ = [
    "ISIC_SECTIONS",
    "SECTOR_ISIC",
    "SAUDI_STRATEGIC_OVERLAY",
    "SECTOR_REGULATORS",
    "SECTION_MAPPING_STATUS",
    "SAUDI_MAPPING_STATUS",
    "TaxonomyRef",
    "taxonomy_for",
    "coverage",
    "UNKNOWN",
]
