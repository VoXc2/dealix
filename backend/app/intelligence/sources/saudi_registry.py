"""
المركز السعودي للأعمال — Saudi Business Registry Source
=========================================================
Fetches and filters company records from the Saudi Business Center
(businesscenter.gov.sa) and related official registries (ZATCA, GOSI, Monsha'at).

STATUS: Placeholder implementation with seed data.
TODO: Integrate live API once the following credentials are available:
  - Saudi Business Center API key (businesscenter.gov.sa developer portal)
  - GOSI Open Data token (data.gov.sa)
  - ZATCA API credentials for VAT lookup
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import httpx

from ..models import (
    Company,
    Contact,
    DiscoveryCriteria,
    EstablishmentType,
    HiringSignal,
    Region,
    Sector,
    SocialHandles,
)


# ─────────────────────────── Static Seed Data ────────────────────────────────
# 30 well-known Saudi companies across target sectors.
# Data sourced from public knowledge: company websites, CR records, news.
# Fields use best-effort public information.

SAUDI_COMPANY_SEED: list[dict[str, Any]] = [
    # ── E-commerce ──────────────────────────────────────────────────────────
    {
        "name": "Jarir Marketing Company",
        "name_ar": "مجموعة جرير للتسويق",
        "domain": "jarir.com",
        "website": "https://www.jarir.com",
        "sector": Sector.RETAIL,
        "sub_sector": "electronics & books retail",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010150609",
        "isic_code": "4741",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1979,
        "employee_count": 4000,
        "revenue_estimate_sar": 5_800_000_000,
        "ceo_name": "Mohammed Abdulaziz Al-Agil",
        "ceo_name_ar": "محمد عبدالعزيز العقيل",
        "tech_stack": ["Magento", "Salesforce", "SAP"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/jarir",
            twitter="JarirBooks",
            instagram="jarirbookstore",
        ),
    },
    {
        "name": "eXtra Electronics",
        "name_ar": "إكسترا للإلكترونيات",
        "domain": "extra.com",
        "website": "https://www.extra.com",
        "sector": Sector.RETAIL,
        "sub_sector": "consumer electronics",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010231723",
        "isic_code": "4741",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 2003,
        "employee_count": 3500,
        "revenue_estimate_sar": 4_200_000_000,
        "ceo_name": "Abdulaziz Al-Agil",
        "ceo_name_ar": "عبدالعزيز العقيل",
        "tech_stack": ["Hybris SAP Commerce", "Adobe Analytics", "Salesforce"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/extra-stores",
            twitter="eXtraSA",
            instagram="extra_stores",
        ),
    },
    {
        "name": "Noon",
        "name_ar": "نون",
        "domain": "noon.com",
        "website": "https://www.noon.com/saudi-ar",
        "sector": Sector.ECOMMERCE,
        "sub_sector": "marketplace",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "4791",
        "establishment_type": EstablishmentType.LARGE,
        "founded_year": 2016,
        "employee_count": 5000,
        "revenue_estimate_sar": 3_000_000_000,
        "tech_stack": ["AWS", "React", "Node.js", "Kafka"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/noon-com",
            twitter="NoonKSA",
            instagram="noon",
        ),
    },
    {
        "name": "Salla",
        "name_ar": "سلة",
        "domain": "salla.com",
        "website": "https://salla.com",
        "sector": Sector.B2B_SAAS,
        "sub_sector": "ecommerce platform",
        "region": Region.MAKKAH,
        "city": "Jeddah",
        "city_ar": "جدة",
        "isic_code": "6201",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2016,
        "employee_count": 350,
        "revenue_estimate_sar": 120_000_000,
        "ceo_name": "Salah Al-Deen Al-Majali",
        "ceo_name_ar": "صلاح الدين المجالي",
        "tech_stack": ["Laravel", "Vue.js", "AWS", "Redis"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/sallaksa",
            twitter="salla",
            instagram="salla",
        ),
    },
    {
        "name": "Zid",
        "name_ar": "زد",
        "domain": "zid.sa",
        "website": "https://zid.sa",
        "sector": Sector.B2B_SAAS,
        "sub_sector": "ecommerce platform",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6201",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2017,
        "employee_count": 250,
        "revenue_estimate_sar": 80_000_000,
        "ceo_name": "Sultan Al-Dawsari",
        "ceo_name_ar": "سلطان الدوسري",
        "tech_stack": ["Django", "React", "PostgreSQL", "Redis"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/zid-sa",
            twitter="zid_sa",
            instagram="zid_sa",
        ),
    },
    # ── Technology / Telecom ─────────────────────────────────────────────────
    {
        "name": "Saudi Telecom Company (stc)",
        "name_ar": "الشركة السعودية للاتصالات",
        "domain": "stc.com.sa",
        "website": "https://www.stc.com.sa",
        "sector": Sector.TELECOM,
        "sub_sector": "telecommunications",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010150271",
        "vat_number": "300087331900003",
        "isic_code": "6110",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1998,
        "employee_count": 18000,
        "revenue_estimate_sar": 66_000_000_000,
        "ceo_name": "Olayan Alwetaid",
        "ceo_name_ar": "عليان الويتيد",
        "tech_stack": ["AWS", "Azure", "SAP", "Salesforce", "Oracle"],
        "social_handles": SocialHandles(
            linkedin="company/stc-ksa",
            twitter="stc_KSA",
            instagram="stc_ksa",
        ),
    },
    {
        "name": "Elm Company",
        "name_ar": "شركة علم",
        "domain": "elm.sa",
        "website": "https://www.elm.sa",
        "sector": Sector.TECHNOLOGY,
        "sub_sector": "government IT solutions",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010243234",
        "isic_code": "6202",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 2005,
        "employee_count": 5000,
        "revenue_estimate_sar": 3_800_000_000,
        "ceo_name": "Ahmad Al-Subaie",
        "ceo_name_ar": "أحمد السبيعي",
        "tech_stack": ["Java", "Oracle", "Azure", "Python"],
        "social_handles": SocialHandles(
            linkedin="company/elm-company",
            twitter="elm_sa",
            instagram="elm_sa",
        ),
    },
    {
        "name": "Solutions by STC",
        "name_ar": "سلوشنز",
        "domain": "solutions.com.sa",
        "website": "https://www.solutions.com.sa",
        "sector": Sector.TECHNOLOGY,
        "sub_sector": "enterprise IT services",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6202",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1999,
        "employee_count": 7000,
        "revenue_estimate_sar": 8_000_000_000,
        "ceo_name": "Riyadh Najm",
        "ceo_name_ar": "رياض نجم",
        "tech_stack": ["SAP", "Oracle", "Salesforce", "AWS", "Cisco"],
        "social_handles": SocialHandles(
            linkedin="company/solutions-by-stc",
            twitter="SolutionsbySTC",
        ),
    },
    # ── Healthcare ───────────────────────────────────────────────────────────
    {
        "name": "Nahdi Medical Company",
        "name_ar": "نهضة الوطن للصيدليات",
        "domain": "nahdi.sa",
        "website": "https://www.nahdi.sa",
        "sector": Sector.HEALTHCARE,
        "sub_sector": "pharmacy retail",
        "region": Region.MAKKAH,
        "city": "Jeddah",
        "city_ar": "جدة",
        "registration_number": "4030008313",
        "isic_code": "4773",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1986,
        "employee_count": 10000,
        "revenue_estimate_sar": 6_200_000_000,
        "ceo_name": "Mohammed Al-Shehri",
        "ceo_name_ar": "محمد الشهري",
        "tech_stack": ["SAP", "Salesforce", "Oracle", "Custom Mobile App"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/nahdi-medical",
            twitter="NahdiSA",
            instagram="nahdisa",
        ),
    },
    {
        "name": "Bupa Arabia",
        "name_ar": "بوبا العربية",
        "domain": "bupa.com.sa",
        "website": "https://www.bupa.com.sa",
        "sector": Sector.FINANCIAL_SERVICES,
        "sub_sector": "health insurance",
        "region": Region.MAKKAH,
        "city": "Jeddah",
        "city_ar": "جدة",
        "registration_number": "4030190082",
        "isic_code": "6512",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1997,
        "employee_count": 2500,
        "revenue_estimate_sar": 14_000_000_000,
        "ceo_name": "Tal Hisham Al-Zubair",
        "ceo_name_ar": "طل هشام الزبير",
        "tech_stack": ["SAP", "Salesforce", "Pega", "AWS"],
        "social_handles": SocialHandles(
            linkedin="company/bupa-arabia",
            twitter="BupaArabia",
            instagram="bupaarabia",
        ),
    },
    {
        "name": "Dr. Sulaiman Al Habib Medical Group",
        "name_ar": "مجموعة مستشفيات الدكتور سليمان الحبيب",
        "domain": "hmg.com",
        "website": "https://www.hmg.com",
        "sector": Sector.HEALTHCARE,
        "sub_sector": "private hospital group",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010119967",
        "isic_code": "8610",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1995,
        "employee_count": 15000,
        "revenue_estimate_sar": 10_000_000_000,
        "ceo_name": "Dr. Sulaiman Al-Habib",
        "ceo_name_ar": "د. سليمان الحبيب",
        "tech_stack": ["SAP", "Cerner EHR", "Oracle"],
        "social_handles": SocialHandles(
            linkedin="company/dr-sulaiman-al-habib-medical-group",
            twitter="HMGSaudi",
            instagram="hmgsaudi",
        ),
    },
    # ── Real Estate ───────────────────────────────────────────────────────────
    {
        "name": "ROSHN",
        "name_ar": "روشن",
        "domain": "roshn.sa",
        "website": "https://roshn.sa",
        "sector": Sector.REAL_ESTATE,
        "sub_sector": "mega real estate developer",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "4100",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 2019,
        "employee_count": 1000,
        "revenue_estimate_sar": 5_000_000_000,
        "ceo_name": "David Grover",
        "ceo_name_ar": "ديفيد غروفر",
        "tech_stack": ["Salesforce", "Oracle", "SAP", "BIM 360"],
        "social_handles": SocialHandles(
            linkedin="company/roshn",
            twitter="ROSHNsa",
            instagram="roshn_sa",
        ),
    },
    {
        "name": "Dar Al Arkan Real Estate",
        "name_ar": "دار الأركان للتطوير العقاري",
        "domain": "daralarkan.com",
        "website": "https://www.daralarkan.com",
        "sector": Sector.REAL_ESTATE,
        "sub_sector": "real estate development",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010174907",
        "isic_code": "6810",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1994,
        "employee_count": 2000,
        "revenue_estimate_sar": 3_000_000_000,
        "ceo_name": "Ziad El-Chaar",
        "ceo_name_ar": "زياد الشعار",
        "tech_stack": ["SAP", "Yardi", "Salesforce"],
        "social_handles": SocialHandles(
            linkedin="company/dar-al-arkan",
            twitter="DarAlArkan",
            instagram="daralarkan",
        ),
    },
    {
        "name": "Retal Urban Development",
        "name_ar": "ريتال للتطوير العمراني",
        "domain": "retal.com",
        "website": "https://retal.com",
        "sector": Sector.REAL_ESTATE,
        "sub_sector": "urban real estate",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "4100",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 2004,
        "employee_count": 800,
        "revenue_estimate_sar": 1_500_000_000,
        "ceo_name": "Abdullah Al-Rasheed",
        "ceo_name_ar": "عبدالله الرشيد",
        "tech_stack": ["SAP", "Salesforce", "AutoCAD"],
        "social_handles": SocialHandles(
            linkedin="company/retal-urban-development",
            twitter="RetalSA",
            instagram="retalsa",
        ),
    },
    # ── Digital Agencies ─────────────────────────────────────────────────────
    {
        "name": "Digital MENA",
        "name_ar": "ديجيتال مينا",
        "domain": "digitalmena.com",
        "website": "https://digitalmena.com",
        "sector": Sector.DIGITAL_AGENCY,
        "sub_sector": "performance marketing",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "7311",
        "establishment_type": EstablishmentType.SMALL,
        "founded_year": 2015,
        "employee_count": 80,
        "revenue_estimate_sar": 20_000_000,
        "tech_stack": ["Google Ads", "Meta Ads", "HubSpot", "Semrush"],
        "social_handles": SocialHandles(
            linkedin="company/digital-mena",
            twitter="DigitalMENA",
        ),
    },
    {
        "name": "Webmaster",
        "name_ar": "ويب ماستر",
        "domain": "webmaster.com.sa",
        "website": "https://webmaster.com.sa",
        "sector": Sector.DIGITAL_AGENCY,
        "sub_sector": "web development & digital marketing",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6201",
        "establishment_type": EstablishmentType.SMALL,
        "founded_year": 2009,
        "employee_count": 120,
        "revenue_estimate_sar": 30_000_000,
        "tech_stack": ["WordPress", "Laravel", "Google Analytics", "HubSpot"],
        "social_handles": SocialHandles(
            linkedin="company/webmaster-sa",
            twitter="WebmasterSA",
            instagram="webmaster_sa",
        ),
    },
    # ── Retail ───────────────────────────────────────────────────────────────
    {
        "name": "Abdullah Al Othaim Markets",
        "name_ar": "أسواق عبدالله العثيم",
        "domain": "alothaim.com.sa",
        "website": "https://www.alothaim.com.sa",
        "sector": Sector.RETAIL,
        "sub_sector": "grocery retail",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010115702",
        "isic_code": "4711",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1956,
        "employee_count": 20000,
        "revenue_estimate_sar": 10_700_000_000,
        "ceo_name": "Adel Abdullah Al-Othaim",
        "ceo_name_ar": "عادل عبدالله العثيم",
        "tech_stack": ["SAP", "Oracle", "Microsoft Dynamics"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/abdullah-al-othaim-markets",
            twitter="alothaim_ksa",
            instagram="alothaim_ksa",
        ),
    },
    {
        "name": "Aldrees Petroleum and Transport Services",
        "name_ar": "شركة الدريس للبترول وخدمات النقل",
        "domain": "aldrees.com",
        "website": "https://www.aldrees.com",
        "sector": Sector.ENERGY,
        "sub_sector": "fuel retail & transport",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "registration_number": "1010163808",
        "isic_code": "4730",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1981,
        "employee_count": 3500,
        "revenue_estimate_sar": 5_500_000_000,
        "ceo_name": "Abdullah Al-Drees",
        "ceo_name_ar": "عبدالله الدريس",
        "tech_stack": ["SAP", "Oracle", "Fleet Management System"],
        "social_handles": SocialHandles(
            linkedin="company/aldrees",
            twitter="aldrees_sa",
        ),
    },
    # ── Logistics ────────────────────────────────────────────────────────────
    {
        "name": "SMSA Express",
        "name_ar": "سمسا إكسبريس",
        "domain": "smsa.com",
        "website": "https://www.smsa.com",
        "sector": Sector.LOGISTICS,
        "sub_sector": "express courier",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "5320",
        "establishment_type": EstablishmentType.LARGE,
        "founded_year": 1985,
        "employee_count": 6000,
        "revenue_estimate_sar": 2_000_000_000,
        "tech_stack": ["SAP", "Custom TMS", "Mobile Apps"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/smsa-express",
            twitter="SMSAExpress",
            instagram="smsaexpress",
        ),
    },
    {
        "name": "Naqel Express",
        "name_ar": "ناقل إكسبريس",
        "domain": "naqelexpress.com",
        "website": "https://www.naqelexpress.com",
        "sector": Sector.LOGISTICS,
        "sub_sector": "logistics & courier",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "5320",
        "establishment_type": EstablishmentType.LARGE,
        "founded_year": 2002,
        "employee_count": 5000,
        "revenue_estimate_sar": 1_200_000_000,
        "tech_stack": ["SAP", "Oracle", "WMS"],
        "social_handles": SocialHandles(
            linkedin="company/naqel-express",
            twitter="naqelexpress",
        ),
    },
    # ── Financial Services / Fintech ─────────────────────────────────────────
    {
        "name": "Tabby",
        "name_ar": "تابي",
        "domain": "tabby.ai",
        "website": "https://tabby.ai",
        "sector": Sector.FINANCIAL_SERVICES,
        "sub_sector": "BNPL fintech",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6499",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2019,
        "employee_count": 500,
        "revenue_estimate_sar": 280_000_000,
        "ceo_name": "Hosam Arab",
        "ceo_name_ar": "حسام عرب",
        "tech_stack": ["React", "Node.js", "PostgreSQL", "AWS", "Stripe"],
        "social_handles": SocialHandles(
            linkedin="company/tabby-fintech",
            twitter="tabby",
            instagram="tabby",
        ),
    },
    {
        "name": "Tamara",
        "name_ar": "تمارا",
        "domain": "tamara.co",
        "website": "https://tamara.co",
        "sector": Sector.FINANCIAL_SERVICES,
        "sub_sector": "BNPL fintech",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6499",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2020,
        "employee_count": 400,
        "revenue_estimate_sar": 200_000_000,
        "ceo_name": "Abdulmajeed Alsukhan",
        "ceo_name_ar": "عبدالمجيد السخان",
        "tech_stack": ["React", "Python", "AWS", "PostgreSQL"],
        "social_handles": SocialHandles(
            linkedin="company/tamara-payments",
            twitter="tamara_sa",
            instagram="tamara_sa",
        ),
    },
    # ── Education ────────────────────────────────────────────────────────────
    {
        "name": "Noon Academy",
        "name_ar": "أكاديمية نون",
        "domain": "noonacademy.com",
        "website": "https://noonacademy.com",
        "sector": Sector.EDUCATION,
        "sub_sector": "edtech",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "8550",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2013,
        "employee_count": 200,
        "revenue_estimate_sar": 60_000_000,
        "tech_stack": ["React Native", "AWS", "Firebase", "Node.js"],
        "social_handles": SocialHandles(
            linkedin="company/noon-academy",
            twitter="NoonAcademy",
            instagram="noonacademy",
        ),
    },
    {
        "name": "Edraak",
        "name_ar": "إدراك",
        "domain": "edraak.org",
        "website": "https://www.edraak.org",
        "sector": Sector.EDUCATION,
        "sub_sector": "online learning platform",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "8550",
        "establishment_type": EstablishmentType.SMALL,
        "founded_year": 2013,
        "employee_count": 80,
        "revenue_estimate_sar": 15_000_000,
        "tech_stack": ["Django", "React", "AWS", "PostgreSQL"],
        "social_handles": SocialHandles(
            linkedin="company/edraak",
            twitter="edraakorg",
            instagram="edraakorg",
        ),
    },
    # ── B2B SaaS ──────────────────────────────────────────────────────────────
    {
        "name": "Foodics",
        "name_ar": "فودكس",
        "domain": "foodics.com",
        "website": "https://foodics.com",
        "sector": Sector.B2B_SAAS,
        "sub_sector": "restaurant management software",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6201",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2014,
        "employee_count": 400,
        "revenue_estimate_sar": 150_000_000,
        "ceo_name": "Ahmad Al-Zaini",
        "ceo_name_ar": "أحمد الزيني",
        "tech_stack": ["React", "Ruby on Rails", "PostgreSQL", "AWS"],
        "social_handles": SocialHandles(
            linkedin="company/foodics",
            twitter="FoodicsApp",
            instagram="foodics",
        ),
    },
    {
        "name": "Rewaa",
        "name_ar": "رواء",
        "domain": "rewaatech.com",
        "website": "https://rewaatech.com",
        "sector": Sector.B2B_SAAS,
        "sub_sector": "POS & inventory SaaS",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "6201",
        "establishment_type": EstablishmentType.SMALL,
        "founded_year": 2020,
        "employee_count": 120,
        "revenue_estimate_sar": 35_000_000,
        "ceo_name": "Rashid Al-Rashidi",
        "ceo_name_ar": "راشد الراشدي",
        "tech_stack": ["Vue.js", "Laravel", "PostgreSQL", "AWS"],
        "social_handles": SocialHandles(
            linkedin="company/rewaatech",
            twitter="rewaatech",
            instagram="rewaatech",
        ),
    },
    {
        "name": "HungerStation",
        "name_ar": "هنقرستيشن",
        "domain": "hungerstation.com",
        "website": "https://www.hungerstation.com",
        "sector": Sector.ECOMMERCE,
        "sub_sector": "food delivery platform",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "5630",
        "establishment_type": EstablishmentType.LARGE,
        "founded_year": 2012,
        "employee_count": 2000,
        "revenue_estimate_sar": 800_000_000,
        "tech_stack": ["React Native", "Node.js", "AWS", "Kafka"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/hungerstation",
            twitter="HungerStation",
            instagram="hungerstation",
        ),
    },
    {
        "name": "Tamer Group",
        "name_ar": "مجموعة تامر",
        "domain": "tamer.com.sa",
        "website": "https://www.tamer.com.sa",
        "sector": Sector.HEALTHCARE,
        "sub_sector": "pharmaceutical distribution",
        "region": Region.MAKKAH,
        "city": "Jeddah",
        "city_ar": "جدة",
        "registration_number": "4030019977",
        "isic_code": "4646",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1948,
        "employee_count": 3000,
        "revenue_estimate_sar": 7_000_000_000,
        "ceo_name": "Walid Tamer",
        "ceo_name_ar": "وليد تامر",
        "tech_stack": ["SAP", "Oracle"],
        "social_handles": SocialHandles(
            linkedin="company/tamer-group",
            twitter="TamerGroup",
        ),
    },
    {
        "name": "Mrsool",
        "name_ar": "مرسول",
        "domain": "mrsool.co",
        "website": "https://mrsool.co",
        "sector": Sector.LOGISTICS,
        "sub_sector": "on-demand delivery platform",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "5320",
        "establishment_type": EstablishmentType.MEDIUM,
        "founded_year": 2015,
        "employee_count": 300,
        "revenue_estimate_sar": 200_000_000,
        "ceo_name": "Mohammed Al-Ghamdi",
        "ceo_name_ar": "محمد الغامدي",
        "tech_stack": ["React Native", "Node.js", "AWS", "MongoDB"],
        "ecommerce_platform": "Custom",
        "social_handles": SocialHandles(
            linkedin="company/mrsoolapp",
            twitter="mrsoolapp",
            instagram="mrsoolapp",
        ),
    },
    {
        "name": "Al-Futtaim Saudi",
        "name_ar": "الفطيم السعودية",
        "domain": "alfuttaim.com",
        "website": "https://www.alfuttaim.com",
        "sector": Sector.RETAIL,
        "sub_sector": "diversified retail & automotive",
        "region": Region.RIYADH,
        "city": "Riyadh",
        "city_ar": "الرياض",
        "isic_code": "4511",
        "establishment_type": EstablishmentType.CORPORATION,
        "founded_year": 1992,
        "employee_count": 2500,
        "revenue_estimate_sar": 4_000_000_000,
        "tech_stack": ["SAP", "Oracle", "Salesforce"],
        "social_handles": SocialHandles(
            linkedin="company/al-futtaim-group",
            twitter="AlFuttaimGroup",
        ),
    },
]


class SaudiBusinessRegistrySource:
    """
    المركز السعودي للأعمال — Saudi Business Center data source.

    يوفر هذا المصدر:
    1. بيانات seed ثابتة لـ 30 شركة سعودية معروفة (تعمل فور التشغيل بدون API).
    2. stub لاستدعاء API المركز السعودي للأعمال الفعلي (يحتاج بيانات اعتماد).

    TODO credentials needed:
      - Saudi Business Center API key (businesscenter.gov.sa)
      - GOSI Open Data API token
      - ZATCA Fatoora API credentials for VAT verification
    """

    BASE_URL = "https://api.businesscenter.gov.sa/v1"  # placeholder — verify exact URL

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key
        self._seed_companies: list[Company] = self._build_seed()

    # ─────────────────────────── Public API ─────────────────────────────────

    async def discover(self, criteria: DiscoveryCriteria) -> list[Company]:
        """
        اكتشف شركات بناءً على المعايير المحددة.

        يستخدم بيانات الـ seed في غياب API key.
        إذا توفر API key → يُرسل طلباً حقيقياً.
        """
        if self.api_key:
            return await self._fetch_live(criteria)
        return self._filter_seed(criteria)

    async def get_company_details(self, registration_number: str) -> Company | None:
        """
        جلب تفاصيل شركة محددة برقم السجل التجاري.

        TODO: Implement live Saudi Business Center API call.
        Endpoint: GET /companies/{registration_number}
        Requires: API key in header X-API-Key
        """
        if self.api_key:
            raise NotImplementedError(
                "TODO: Implement live Saudi Business Center API lookup.\n"
                "Credential needed: SAUDI_BUSINESS_CENTER_API_KEY\n"
                "Endpoint: GET https://api.businesscenter.gov.sa/v1/companies/{cr_number}\n"
                "Docs: https://businesscenter.gov.sa/en/developers"
            )
        # Fallback: search seed
        for company in self._seed_companies:
            if company.registration_number == registration_number:
                return company
        return None

    async def verify_vat(self, vat_number: str) -> dict[str, Any]:
        """
        التحقق من الرقم الضريبي عبر ZATCA.

        TODO: Implement ZATCA Fatoora API integration.
        Endpoint: POST https://fatoora.zatca.gov.sa/taxpayer/verify
        Requires: ZATCA_API_USERNAME + ZATCA_API_PASSWORD
        """
        raise NotImplementedError(
            "TODO: Implement ZATCA VAT verification.\n"
            "Credentials needed: ZATCA_API_USERNAME, ZATCA_API_PASSWORD\n"
            "Endpoint: POST https://fatoora.zatca.gov.sa/taxpayer/verify\n"
            "Docs: https://zatca.gov.sa/en/E-Invoicing/Pages/Developer-Tools.aspx"
        )

    async def get_gosi_employees(self, company_id: str) -> int | None:
        """
        جلب عدد الموظفين المسجلين في GOSI (proxy موثوق للحجم).

        TODO: Implement GOSI open data lookup.
        Dataset: data.gov.sa GOSI dataset
        Requires: data.gov.sa API token
        """
        raise NotImplementedError(
            "TODO: Implement GOSI employee count lookup.\n"
            "Dataset URL: https://data.gov.sa/Data/en/dataset/gosi-statistical-data\n"
            "Credential needed: DATA_GOV_SA_API_TOKEN\n"
        )

    # ─────────────────────────── Seed Helpers ────────────────────────────────

    def _build_seed(self) -> list[Company]:
        """بناء كائنات Company من بيانات الـ seed الثابتة."""
        companies: list[Company] = []
        for raw in SAUDI_COMPANY_SEED:
            raw_copy = dict(raw)
            social = raw_copy.pop("social_handles", SocialHandles())
            company = Company(
                **raw_copy,
                social_handles=social,
                data_sources=["seed_saudi_registry"],
            )
            companies.append(company)
        return companies

    def _filter_seed(self, criteria: DiscoveryCriteria) -> list[Company]:
        """تصفية بيانات الـ seed بناءً على المعايير."""
        results = list(self._seed_companies)

        if criteria.sectors:
            results = [c for c in results if c.sector in criteria.sectors]

        if criteria.regions:
            results = [c for c in results if c.region in criteria.regions]

        if criteria.min_employees is not None:
            results = [
                c for c in results
                if c.employee_count is not None and c.employee_count >= criteria.min_employees
            ]

        if criteria.max_employees is not None:
            results = [
                c for c in results
                if c.employee_count is not None and c.employee_count <= criteria.max_employees
            ]

        if criteria.isic_codes:
            results = [
                c for c in results
                if c.isic_code in criteria.isic_codes
            ]

        if criteria.keywords:
            kws = [k.lower() for k in criteria.keywords]
            results = [
                c for c in results
                if any(
                    kw in (c.name or "").lower()
                    or kw in (c.name_ar or "").lower()
                    or kw in (c.sub_sector or "").lower()
                    for kw in kws
                )
            ]

        return results[: criteria.limit]

    # ─────────────────────────── Live API (stub) ──────────────────────────────

    async def _fetch_live(self, criteria: DiscoveryCriteria) -> list[Company]:
        """
        استدعاء API المركز السعودي للأعمال الفعلي.

        TODO: Complete field mapping once API docs are confirmed.
        Endpoint: GET /companies/search
        Params: isic_code, region, establishment_type, page, limit
        """
        raise NotImplementedError(
            "TODO: Implement live Saudi Business Center API search.\n"
            "Credential needed: SAUDI_BUSINESS_CENTER_API_KEY\n"
            "Set env var: SBC_API_KEY\n"
            "Endpoint: GET https://api.businesscenter.gov.sa/v1/companies/search\n"
            "Query params: isic_code, region_code, establishment_type, page, limit\n"
            "Auth header: X-API-Key: {SBC_API_KEY}\n"
        )

    @property
    def seed_count(self) -> int:
        """عدد الشركات في بيانات الـ seed."""
        return len(self._seed_companies)

    @property
    def all_seed_companies(self) -> list[Company]:
        """كل الشركات في بيانات الـ seed."""
        return list(self._seed_companies)
