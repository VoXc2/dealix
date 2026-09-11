"""Sector Solutions API — serves 20 sectors with services, agents manage."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/solutions", tags=["solutions"])

SECTORS = [
    {"id": "government_b2g", "nameAr": "الجهات الحكومية و B2G", "nameEn": "Government & B2G", "icon": "🏛️"},
    {"id": "construction_epc", "nameAr": "الإنشاءات و EPC", "nameEn": "Construction & EPC", "icon": "🏗️"},
    {"id": "industrial_manufacturing", "nameAr": "الصناعة", "nameEn": "Industrial", "icon": "🏭"},
    {"id": "logistics_supply_chain", "nameAr": "اللوجستيات", "nameEn": "Logistics", "icon": "🚚"},
    {"id": "energy_utilities_oil_gas", "nameAr": "الطاقة والمرافق", "nameEn": "Energy & Utilities", "icon": "⚡"},
    {"id": "mining_metals", "nameAr": "التعدين", "nameEn": "Mining & Metals", "icon": "⛏️"},
    {"id": "real_estate_proptech", "nameAr": "العقار", "nameEn": "Real Estate", "icon": "🏢"},
    {"id": "healthcare", "nameAr": "الرعاية الصحية", "nameEn": "Healthcare", "icon": "🏥"},
    {"id": "finance_fintech_insurance", "nameAr": "المالية والتأمين", "nameEn": "Finance & Insurance", "icon": "🏦"},
    {"id": "retail_commerce_ecommerce", "nameAr": "التجزئة", "nameEn": "Retail & eCommerce", "icon": "🛍️"},
    {"id": "tourism_hospitality", "nameAr": "السياحة والضيافة", "nameEn": "Tourism & Hospitality", "icon": "🏨"},
    {"id": "professional_services", "nameAr": "خدمات مهنية", "nameEn": "Professional Services", "icon": "💼"},
    {"id": "technology_saas_si", "nameAr": "التقنية و SaaS", "nameEn": "Technology & SaaS", "icon": "💻"},
    {"id": "telecom_media_marketing", "nameAr": "الاتصالات والإعلام", "nameEn": "Telecom & Media", "icon": "📡"},
    {"id": "education_training", "nameAr": "التعليم", "nameEn": "Education", "icon": "🎓"},
    {"id": "agriculture_food_water", "nameAr": "الزراعة والمياه", "nameEn": "Agriculture & Water", "icon": "🌾"},
    {"id": "mobility_automotive", "nameAr": "التنقل والسيارات", "nameEn": "Mobility & Automotive", "icon": "🚗"},
    {"id": "export_import_rhq", "nameAr": "الاستيراد والتصدير", "nameEn": "Export/Import & RHQ", "icon": "🌐"},
    {"id": "creative_sports_gaming", "nameAr": "إبداع ورياضة", "nameEn": "Creative & Sports", "icon": "🎮"},
    {"id": "associations_nonprofits", "nameAr": "جمعيات وغير ربحية", "nameEn": "Associations & Nonprofits", "icon": "🤝"},
]

@router.get("")
def list_sectors() -> dict[str, Any]:
    return {"sectors": SECTORS, "total": len(SECTORS), "managed_by": ["dealix-pm","dealix-sales","dealix-delivery","dealix-engineer","dealix-content"], "automation": "all sectors automated as temporary capabilities, DeepWIP ≤3"}

@router.get("/{sector_id}")
def get_sector(sector_id: str) -> dict[str, Any]:
    for s in SECTORS:
        if s["id"] == sector_id:
            return {**s, "services": 3, "agents": "pm,sales,delivery,engineer,content", "channels": ["website","email","whatsapp_opt_in","web_chat","support","partner","procurement"], "diagnostic": f"/api/v1/diagnostic?sector={sector_id}"}
    return {"error": "sector not found", "sector_id": sector_id}
