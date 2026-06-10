"""Expanded Saudi sector taxonomy — 30+ sectors, 70+ sub-sectors.

Based on Saudi Chambers of Commerce classification and NAICS/ISIC mapping.
"""

from __future__ import annotations

from typing import Any

SAUDI_SECTORS: dict[str, dict[str, Any]] = {
    "technology": {
        "name_ar": "تقنية المعلومات",
        "name_en": "Information Technology",
        "code": "IT",
        "naics": "5415",
        "isic": "620",
        "sub_sectors": [
            {"name_ar": "تطوير البرمجيات", "name_en": "Software Development"},
            {"name_ar": "الخدمات السحابية", "name_en": "Cloud Services"},
            {"name_ar": "الأمن السيبراني", "name_en": "Cybersecurity"},
            {"name_ar": "الذكاء الاصطناعي", "name_en": "Artificial Intelligence"},
            {"name_ar": "تحليل البيانات", "name_en": "Data Analytics"},
            {"name_ar": "استشارات تقنية", "name_en": "IT Consulting"},
            {"name_ar": "البنية التحتية التقنية", "name_en": "IT Infrastructure"},
            {"name_ar": "تطوير التطبيقات", "name_en": "App Development"},
            {"name_ar": "استضافة المواقع", "name_en": "Web Hosting"},
        ],
    },
    "services": {
        "name_ar": "الخدمات",
        "name_en": "Services",
        "code": "SV",
        "naics": "561",
        "isic": "702",
        "sub_sectors": [
            {"name_ar": "خدمات الأعمال", "name_en": "Business Services"},
            {"name_ar": "خدمات تنظيف وصيانة", "name_en": "Cleaning & Maintenance"},
            {"name_ar": "خدمات الأمن والحراسة", "name_en": "Security Services"},
            {"name_ar": "خدمات تقديم الطعام", "name_en": "Catering Services"},
            {"name_ar": "خدمات استضافة الفعاليات", "name_en": "Event Management"},
            {"name_ar": "خدمات الترجمة", "name_en": "Translation Services"},
            {"name_ar": "خدمات التوظيف", "name_en": "Recruitment Services"},
            {"name_ar": "خدمات الاستشارات الإدارية", "name_en": "Management Consulting"},
        ],
    },
    "consulting": {
        "name_ar": "الاستشارات",
        "name_en": "Consulting",
        "code": "CS",
        "naics": "5416",
        "isic": "702",
        "sub_sectors": [
            {"name_ar": "استشارات إدارية", "name_en": "Management Consulting"},
            {"name_ar": "استشارات مالية", "name_en": "Financial Consulting"},
            {"name_ar": "استشارات قانونية", "name_en": "Legal Consulting"},
            {"name_ar": "استشارات استراتيجية", "name_en": "Strategy Consulting"},
            {"name_ar": "استشارات موارد بشرية", "name_en": "HR Consulting"},
            {"name_ar": "استشارات تسويقية", "name_en": "Marketing Consulting"},
            {"name_ar": "استشارات بيئية", "name_en": "Environmental Consulting"},
        ],
    },
    "training_education": {
        "name_ar": "التدريب والتعليم",
        "name_en": "Training & Education",
        "code": "ED",
        "naics": "611",
        "isic": "854",
        "sub_sectors": [
            {"name_ar": "التدريب المهني", "name_en": "Vocational Training"},
            {"name_ar": "التعليم الإلكتروني", "name_en": "E-Learning"},
            {"name_ar": "تدريب القيادة", "name_en": "Leadership Training"},
            {"name_ar": "التدريب التقني", "name_en": "Technical Training"},
            {"name_ar": "مراكز التدريب", "name_en": "Training Centers"},
            {"name_ar": "استشارات تعليمية", "name_en": "Educational Consulting"},
            {"name_ar": "تدريب اللغات", "name_en": "Language Training"},
            {"name_ar": "التعليم العالي", "name_en": "Higher Education"},
        ],
    },
    "real_estate": {
        "name_ar": "العقارات",
        "name_en": "Real Estate",
        "code": "RE",
        "naics": "531",
        "isic": "681",
        "sub_sectors": [
            {"name_ar": "تطوير عقاري", "name_en": "Real Estate Development"},
            {"name_ar": "إدارة أملاك", "name_en": "Property Management"},
            {"name_ar": "وساطة عقارية", "name_en": "Real Estate Brokerage"},
            {"name_ar": "تقييم عقاري", "name_en": "Property Valuation"},
            {"name_ar": "الإسكان والتمويل", "name_en": "Housing & Finance"},
            {"name_ar": "العقارات التجارية", "name_en": "Commercial Real Estate"},
            {"name_ar": "العقارات السكنية", "name_en": "Residential Real Estate"},
        ],
    },
    "logistics": {
        "name_ar": "الخدمات اللوجستية",
        "name_en": "Logistics",
        "code": "LG",
        "naics": "488",
        "isic": "522",
        "sub_sectors": [
            {"name_ar": "النقل البري", "name_en": "Land Transport"},
            {"name_ar": "النقل البحري", "name_en": "Maritime Transport"},
            {"name_ar": "النقل الجوي", "name_en": "Air Transport"},
            {"name_ar": "التخزين والتوزيع", "name_en": "Warehousing & Distribution"},
            {"name_ar": "خدمات سلسلة التوريد", "name_en": "Supply Chain Services"},
            {"name_ar": "الخدمات اللوجستية الإلكترونية", "name_en": "E-Logistics"},
            {"name_ar": "التخليص الجمركي", "name_en": "Customs Clearance"},
            {"name_ar": "إدارة الأساطيل", "name_en": "Fleet Management"},
        ],
    },
    "healthcare": {
        "name_ar": "الرعاية الصحية",
        "name_en": "Healthcare",
        "code": "HC",
        "naics": "621",
        "isic": "861",
        "sub_sectors": [
            {"name_ar": "المستشفيات", "name_en": "Hospitals"},
            {"name_ar": "المستوصفات والعيادات", "name_en": "Clinics"},
            {"name_ar": "الصيدليات", "name_en": "Pharmacies"},
            {"name_ar": "الخدمات الطبية المساندة", "name_en": "Support Medical Services"},
            {"name_ar": "التأمين الصحي", "name_en": "Health Insurance"},
            {"name_ar": "الصحة الرقمية", "name_en": "Digital Health"},
            {"name_ar": "المختبرات الطبية", "name_en": "Medical Laboratories"},
            {"name_ar": "مراكز التأهيل", "name_en": "Rehabilitation Centers"},
        ],
    },
    "finance": {
        "name_ar": "الخدمات المالية",
        "name_en": "Financial Services",
        "code": "FI",
        "naics": "522",
        "isic": "641",
        "sub_sectors": [
            {"name_ar": "البنوك", "name_en": "Banking"},
            {"name_ar": "التمويل", "name_en": "Financing"},
            {"name_ar": "التقنيات المالية", "name_en": "Fintech"},
            {"name_ar": "إدارة الثروات", "name_en": "Wealth Management"},
            {"name_ar": "الاستثمار", "name_en": "Investment"},
            {"name_ar": "الصيرفة الإسلامية", "name_en": "Islamic Banking"},
            {"name_ar": "بورصات الأسواق المالية", "name_en": "Financial Markets"},
        ],
    },
    "retail": {
        "name_ar": "التجزئة",
        "name_en": "Retail",
        "code": "RT",
        "naics": "452",
        "isic": "471",
        "sub_sectors": [
            {"name_ar": "التجزئة الإلكترونية", "name_en": "E-Commerce"},
            {"name_ar": "الأسواق المركزية", "name_en": "Hypermarkets"},
            {"name_ar": "الملابس والأزياء", "name_en": "Apparel & Fashion"},
            {"name_ar": "الإلكترونيات", "name_en": "Electronics"},
            {"name_ar": "الأثاث والديكور", "name_en": "Furniture & Decor"},
            {"name_ar": "المواد الغذائية", "name_en": "Food & Beverage Retail"},
            {"name_ar": "المجوهرات", "name_en": "Jewelry"},
        ],
    },
    "manufacturing": {
        "name_ar": "التصنيع",
        "name_en": "Manufacturing",
        "code": "MF",
        "naics": "31",
        "isic": "210",
        "sub_sectors": [
            {"name_ar": "البلاستيك والكيماويات", "name_en": "Plastics & Chemicals"},
            {"name_ar": "المواد الغذائية", "name_en": "Food Manufacturing"},
            {"name_ar": "مواد البناء", "name_en": "Building Materials"},
            {"name_ar": "الأدوية", "name_en": "Pharmaceuticals"},
            {"name_ar": "البتروكيماويات", "name_en": "Petrochemicals"},
            {"name_ar": "الإلكترونيات", "name_en": "Electronics Manufacturing"},
            {"name_ar": "المنسوجات", "name_en": "Textiles"},
            {"name_ar": "المعادن", "name_en": "Metals Manufacturing"},
        ],
    },
    "construction": {
        "name_ar": "المقاولات",
        "name_en": "Construction",
        "code": "CN",
        "naics": "236",
        "isic": "410",
        "sub_sectors": [
            {"name_ar": "المقاولات العامة", "name_en": "General Contracting"},
            {"name_ar": "المقاولات الكهربائية", "name_en": "Electrical Contracting"},
            {"name_ar": "المقاولات الميكانيكية", "name_en": "Mechanical Contracting"},
            {"name_ar": "الهندسة المدنية", "name_en": "Civil Engineering"},
            {"name_ar": "التشييد والبناء", "name_en": "Building Construction"},
            {"name_ar": "البنية التحتية", "name_en": "Infrastructure"},
            {"name_ar": "الديكور والتشطيب", "name_en": "Finishing & Decoration"},
        ],
    },
    "agriculture": {
        "name_ar": "الزراعة",
        "name_en": "Agriculture",
        "code": "AG",
        "naics": "111",
        "isic": "111",
        "sub_sectors": [
            {"name_ar": "إنتاج المحاصيل", "name_en": "Crop Production"},
            {"name_ar": "الثروة الحيوانية", "name_en": "Animal Husbandry"},
            {"name_ar": "الصيد البحري", "name_en": "Fisheries"},
            {"name_ar": "التقنيات الزراعية", "name_en": "AgriTech"},
            {"name_ar": "الزراعة العضوية", "name_en": "Organic Farming"},
            {"name_ar": "تشجير واستصلاح أراضي", "name_en": "Land Reclamation"},
        ],
    },
    "energy": {
        "name_ar": "الطاقة",
        "name_en": "Energy",
        "code": "EN",
        "naics": "221",
        "isic": "351",
        "sub_sectors": [
            {"name_ar": "الطاقة المتجددة", "name_en": "Renewable Energy"},
            {"name_ar": "النفط والغاز", "name_en": "Oil & Gas"},
            {"name_ar": "الكهرباء", "name_en": "Electricity"},
            {"name_ar": "كفاءة الطاقة", "name_en": "Energy Efficiency"},
            {"name_ar": "الهيدروجين الأخضر", "name_en": "Green Hydrogen"},
            {"name_ar": "الطاقة الشمسية", "name_en": "Solar Energy"},
            {"name_ar": "طاقة الرياح", "name_en": "Wind Energy"},
        ],
    },
    "mining": {
        "name_ar": "التعدين",
        "name_en": "Mining",
        "code": "MN",
        "naics": "212",
        "isic": "510",
        "sub_sectors": [
            {"name_ar": "التعدين الخام", "name_en": "Ore Mining"},
            {"name_ar": "المعادن الثمينة", "name_en": "Precious Metals"},
            {"name_ar": "التعدين البحري", "name_en": "Offshore Mining"},
            {"name_ar": "المحاجر", "name_en": "Quarrying"},
            {"name_ar": "الفوسفات", "name_en": "Phosphates"},
            {"name_ar": "الألمنيوم", "name_en": "Aluminum"},
        ],
    },
    "media": {
        "name_ar": "الإعلام والترفيه",
        "name_en": "Media & Entertainment",
        "code": "MD",
        "naics": "512",
        "isic": "591",
        "sub_sectors": [
            {"name_ar": "الإنتاج التلفزي", "name_en": "TV Production"},
            {"name_ar": "الإعلان والتسويق", "name_en": "Advertising & Marketing"},
            {"name_ar": "النشر", "name_en": "Publishing"},
            {"name_ar": "صناعة الأفلام", "name_en": "Film Industry"},
            {"name_ar": "الألعاب الإلكترونية", "name_en": "Gaming"},
            {"name_ar": "الإعلام الرقمي", "name_en": "Digital Media"},
            {"name_ar": "العلاقات العامة", "name_en": "Public Relations"},
            {"name_ar": "منصات التواصل", "name_en": "Social Media Platforms"},
        ],
    },
    "tourism": {
        "name_ar": "السياحة والضيافة",
        "name_en": "Tourism & Hospitality",
        "code": "TH",
        "naics": "721",
        "isic": "551",
        "sub_sectors": [
            {"name_ar": "الفنادق والمنتجعات", "name_en": "Hotels & Resorts"},
            {"name_ar": "وكالات السفر", "name_en": "Travel Agencies"},
            {"name_ar": "تنظيم الرحلات", "name_en": "Tour Operations"},
            {"name_ar": "السياحة الدينية", "name_en": "Religious Tourism"},
            {"name_ar": "السياحة الترفيهية", "name_en": "Entertainment Tourism"},
            {"name_ar": "الضيافة", "name_en": "Hospitality Services"},
            {"name_ar": "السياحة البيئية", "name_en": "Eco-Tourism"},
        ],
    },
    "transportation": {
        "name_ar": "النقل",
        "name_en": "Transportation",
        "code": "TR",
        "naics": "484",
        "isic": "491",
        "sub_sectors": [
            {"name_ar": "النقل العام", "name_en": "Public Transport"},
            {"name_ar": "النقل الخاص", "name_en": "Private Transport"},
            {"name_ar": "النقل المدرسي", "name_en": "School Transport"},
            {"name_ar": "النقل الدولي", "name_en": "International Transport"},
            {"name_ar": "خدمات التوصيل", "name_en": "Delivery Services"},
            {"name_ar": "النقل الثقيل", "name_en": "Heavy Transport"},
            {"name_ar": "النقل السياحي", "name_en": "Tourist Transport"},
        ],
    },
    "telecommunications": {
        "name_ar": "الاتصالات",
        "name_en": "Telecommunications",
        "code": "TC",
        "naics": "517",
        "isic": "611",
        "sub_sectors": [
            {"name_ar": "شبكات الاتصالات", "name_en": "Telecom Networks"},
            {"name_ar": "الإنترنت والنطاق العريض", "name_en": "Broadband & Internet"},
            {"name_ar": "الهواتف المحمولة", "name_en": "Mobile Services"},
            {"name_ar": "الاتصالات المؤسسية", "name_en": "Enterprise Telecom"},
            {"name_ar": "خدمات الأقمار الصناعية", "name_en": "Satellite Services"},
            {"name_ar": "الاتصالات الموحدة", "name_en": "Unified Communications"},
        ],
    },
    "legal": {
        "name_ar": "الخدمات القانونية",
        "name_en": "Legal Services",
        "code": "LE",
        "naics": "5411",
        "isic": "691",
        "sub_sectors": [
            {"name_ar": "المحاماة", "name_en": "Law Firms"},
            {"name_ar": "الاستشارات القانونية", "name_en": "Legal Consulting"},
            {"name_ar": "التوثيق", "name_en": "Notary Services"},
            {"name_ar": "التحكيم التجاري", "name_en": "Commercial Arbitration"},
            {"name_ar": "الملكية الفكرية", "name_en": "Intellectual Property"},
            {"name_ar": "التقاضي الإلكتروني", "name_en": "E-Litigation"},
        ],
    },
    "accounting": {
        "name_ar": "المحاسبة والتدقيق",
        "name_en": "Accounting & Auditing",
        "code": "AC",
        "naics": "5412",
        "isic": "692",
        "sub_sectors": [
            {"name_ar": "المحاسبة العامة", "name_en": "General Accounting"},
            {"name_ar": "التدقيق المالي", "name_en": "Financial Auditing"},
            {"name_ar": "الزكاة والضرائب", "name_en": "Zakat & Tax"},
            {"name_ar": "محاسبة التكاليف", "name_en": "Cost Accounting"},
            {"name_ar": "محاسبة قانونية", "name_en": "Forensic Accounting"},
            {"name_ar": "محاسبة إدارية", "name_en": "Management Accounting"},
        ],
    },
    "insurance": {
        "name_ar": "التأمين",
        "name_en": "Insurance",
        "code": "IN",
        "naics": "524",
        "isic": "651",
        "sub_sectors": [
            {"name_ar": "التأمين الصحي", "name_en": "Health Insurance"},
            {"name_ar": "التأمين على السيارات", "name_en": "Auto Insurance"},
            {"name_ar": "التأمين الهندسي", "name_en": "Engineering Insurance"},
            {"name_ar": "التأمين البحري", "name_en": "Marine Insurance"},
            {"name_ar": "التأمين على الحياة", "name_en": "Life Insurance"},
            {"name_ar": "التأمين التعاوني", "name_en": "Cooperative Insurance"},
            {"name_ar": "إعادة التأمين", "name_en": "Reinsurance"},
        ],
    },
    "real_estate_services": {
        "name_ar": "الخدمات العقارية",
        "name_en": "Real Estate Services",
        "code": "RS",
        "naics": "5313",
        "isic": "682",
        "sub_sectors": [
            {"name_ar": "التسويق العقاري", "name_en": "Real Estate Marketing"},
            {"name_ar": "الإدارة العقارية", "name_en": "Real Estate Management"},
            {"name_ar": "الاستشارات العقارية", "name_en": "Real Estate Consulting"},
            {"name_ar": "التثمين العقاري", "name_en": "Real Estate Appraisal"},
        ],
    },
    "advertising": {
        "name_ar": "الإعلان والتسويق",
        "name_en": "Advertising & Marketing",
        "code": "AD",
        "naics": "5418",
        "isic": "731",
        "sub_sectors": [
            {"name_ar": "الإعلانات الرقمية", "name_en": "Digital Advertising"},
            {"name_ar": "التسويق عبر المؤثرين", "name_en": "Influencer Marketing"},
            {"name_ar": "تسويق المحتوى", "name_en": "Content Marketing"},
            {"name_ar": "تحسين محركات البحث", "name_en": "SEO"},
            {"name_ar": "التسويق بالعمولة", "name_en": "Affiliate Marketing"},
            {"name_ar": "التسويق عبر البريد", "name_en": "Email Marketing"},
            {"name_ar": "الإعلانات الخارجية", "name_en": "Outdoor Advertising"},
        ],
    },
    "food_beverage": {
        "name_ar": "الأغذية والمشروبات",
        "name_en": "Food & Beverage",
        "code": "FB",
        "naics": "722",
        "isic": "561",
        "sub_sectors": [
            {"name_ar": "المطاعم", "name_en": "Restaurants"},
            {"name_ar": "المقاهي", "name_en": "Cafes"},
            {"name_ar": "الخدمات الغذائية", "name_en": "Food Services"},
            {"name_ar": "صناعة المشروبات", "name_en": "Beverage Manufacturing"},
            {"name_ar": "التموين", "name_en": "Catering"},
        ],
    },
    "ecommerce": {
        "name_ar": "التجارة الإلكترونية",
        "name_en": "E-Commerce",
        "code": "EC",
        "naics": "454",
        "isic": "479",
        "sub_sectors": [
            {"name_ar": "متاجر إلكترونية", "name_en": "Online Stores"},
            {"name_ar": "منصات التجارة", "name_en": "E-Commerce Platforms"},
            {"name_ar": "الدفع الإلكتروني", "name_en": "Digital Payments"},
            {"name_ar": "التجارة الاجتماعية", "name_en": "Social Commerce"},
            {"name_ar": "دروب شيبينج", "name_en": "Dropshipping"},
        ],
    },
    "environment": {
        "name_ar": "البيئة والاستدامة",
        "name_en": "Environment & Sustainability",
        "code": "ES",
        "naics": "562",
        "isic": "370",
        "sub_sectors": [
            {"name_ar": "إدارة النفايات", "name_en": "Waste Management"},
            {"name_ar": "إعادة التدوير", "name_en": "Recycling"},
            {"name_ar": "الاستدامة", "name_en": "Sustainability"},
            {"name_ar": "معالجة المياه", "name_en": "Water Treatment"},
            {"name_ar": "الاستشارات البيئية", "name_en": "Environmental Consulting"},
            {"name_ar": "الطاقة النظيفة", "name_en": "Clean Energy"},
        ],
    },
    "sports": {
        "name_ar": "الرياضة",
        "name_en": "Sports",
        "code": "SP",
        "naics": "711",
        "isic": "931",
        "sub_sectors": [
            {"name_ar": "الأندية الرياضية", "name_en": "Sports Clubs"},
            {"name_ar": "المراكز الرياضية", "name_en": "Sports Centers"},
            {"name_ar": "التسويق الرياضي", "name_en": "Sports Marketing"},
            {"name_ar": "المعدات الرياضية", "name_en": "Sports Equipment"},
            {"name_ar": "الرياضة الإلكترونية", "name_en": "E-Sports"},
            {"name_ar": "اللياقة البدنية", "name_en": "Fitness"},
        ],
    },
    "design_creative": {
        "name_ar": "التصميم والإبداع",
        "name_en": "Design & Creative",
        "code": "DC",
        "naics": "5414",
        "isic": "741",
        "sub_sectors": [
            {"name_ar": "التصميم الجرافيكي", "name_en": "Graphic Design"},
            {"name_ar": "تصميم المنتجات", "name_en": "Product Design"},
            {"name_ar": "تصميم المواقع", "name_en": "Web Design"},
            {"name_ar": "تصميم الداخلي", "name_en": "Interior Design"},
            {"name_ar": "تصميم الأزياء", "name_en": "Fashion Design"},
            {"name_ar": "الهوية البصرية", "name_en": "Brand Identity"},
        ],
    },
    "hr_manpower": {
        "name_ar": "الموارد البشرية والتوظيف",
        "name_en": "HR & Manpower",
        "code": "HR",
        "naics": "5613",
        "isic": "782",
        "sub_sectors": [
            {"name_ar": "التوظيف", "name_en": "Recruitment"},
            {"name_ar": "تأجير العمالة", "name_en": "Manpower Leasing"},
            {"name_ar": "الاستشارات HR", "name_en": "HR Consulting"},
            {"name_ar": "التدريب HR", "name_en": "HR Training"},
            {"name_ar": "إدارة الأداء", "name_en": "Performance Management"},
        ],
    },
    "aviation": {
        "name_ar": "الطيران",
        "name_en": "Aviation",
        "code": "AV",
        "naics": "481",
        "isic": "511",
        "sub_sectors": [
            {"name_ar": "شركات الطيران", "name_en": "Airlines"},
            {"name_ar": "الشحن الجوي", "name_en": "Air Cargo"},
            {"name_ar": "خدمات المطارات", "name_en": "Airport Services"},
            {"name_ar": "صيانة الطائرات", "name_en": "Aircraft Maintenance"},
            {"name_ar": "الطيران الخاص", "name_en": "Private Aviation"},
        ],
    },
    "defense_security": {
        "name_ar": "الدفاع والأمن",
        "name_en": "Defense & Security",
        "code": "DS",
        "naics": "5416",
        "isic": "842",
        "sub_sectors": [
            {"name_ar": "التصنيع العسكري", "name_en": "Defense Manufacturing"},
            {"name_ar": "الأمن الخاص", "name_en": "Private Security"},
            {"name_ar": "الأمن السيبراني", "name_en": "Cybersecurity Defense"},
            {"name_ar": "الاستشارات الأمنية", "name_en": "Security Consulting"},
        ],
    },
    "beauty_wellness": {
        "name_ar": "التجميل والعناية",
        "name_en": "Beauty & Wellness",
        "code": "BW",
        "naics": "8121",
        "isic": "960",
        "sub_sectors": [
            {"name_ar": "صالونات التجميل", "name_en": "Beauty Salons"},
            {"name_ar": "منتجات التجميل", "name_en": "Beauty Products"},
            {"name_ar": "العناية بالبشرة", "name_en": "Skincare"},
            {"name_ar": "المنتجعات الصحية", "name_en": "Spas & Wellness"},
            {"name_ar": "العطور", "name_en": "Perfumes"},
        ],
    },
    "pharmaceuticals": {
        "name_ar": "المستحضرات الدوائية",
        "name_en": "Pharmaceuticals",
        "code": "PH",
        "naics": "3254",
        "isic": "210",
        "sub_sectors": [
            {"name_ar": "صناعة الأدوية", "name_en": "Drug Manufacturing"},
            {"name_ar": "توزيع الأدوية", "name_en": "Pharmaceutical Distribution"},
            {"name_ar": "المستلزمات الطبية", "name_en": "Medical Supplies"},
            {"name_ar": "مستحضرات التجميل", "name_en": "Cosmeceuticals"},
        ],
    },
    "furniture": {
        "name_ar": "صناعة الأثاث",
        "name_en": "Furniture Manufacturing",
        "code": "FU",
        "naics": "337",
        "isic": "310",
        "sub_sectors": [
            {"name_ar": "الأثاث المنزلي", "name_en": "Home Furniture"},
            {"name_ar": "الأثاث المكتبي", "name_en": "Office Furniture"},
            {"name_ar": "أثاث خارجي", "name_en": "Outdoor Furniture"},
            {"name_ar": "أثاث مؤقت", "name_en": "Custom Furniture"},
        ],
    },
    "petrochemicals": {
        "name_ar": "البتروكيماويات",
        "name_en": "Petrochemicals",
        "code": "PC",
        "naics": "3251",
        "isic": "201",
        "sub_sectors": [
            {"name_ar": "البوليمرات", "name_en": "Polymers"},
            {"name_ar": "الأسمدة", "name_en": "Fertilizers"},
            {"name_ar": "المواد الكيميائية", "name_en": "Industrial Chemicals"},
            {"name_ar": "المشتقات النفطية", "name_en": "Petroleum Derivatives"},
        ],
    },
    "home_services": {
        "name_ar": "الخدمات المنزلية",
        "name_en": "Home Services",
        "code": "HS",
        "naics": "5617",
        "isic": "952",
        "sub_sectors": [
            {"name_ar": "التنظيف المنزلي", "name_en": "Home Cleaning"},
            {"name_ar": "الصيانة المنزلية", "name_en": "Home Maintenance"},
            {"name_ar": "السباكة والكهرباء", "name_en": "Plumbing & Electrical"},
            {"name_ar": "مكافحة الحشرات", "name_en": "Pest Control"},
            {"name_ar": "نقل الأثاث", "name_en": "Furniture Moving"},
        ],
    },
    "automotive": {
        "name_ar": "قطاع السيارات",
        "name_en": "Automotive",
        "code": "AU",
        "naics": "441",
        "isic": "451",
        "sub_sectors": [
            {"name_ar": "وكلاء السيارات", "name_en": "Car Dealerships"},
            {"name_ar": "قطع الغيار", "name_en": "Spare Parts"},
            {"name_ar": "صيانة السيارات", "name_en": "Car Maintenance"},
            {"name_ar": "تأجير السيارات", "name_en": "Car Rental"},
            {"name_ar": "غسيل السيارات", "name_en": "Car Wash"},
        ],
    },
}

SAUDI_B2B_SECTORS: frozenset[str] = frozenset(SAUDI_SECTORS.keys())


def sector_known(slug: str) -> bool:
    return slug.strip().lower() in SAUDI_B2B_SECTORS


def get_all_sectors() -> dict[str, dict[str, Any]]:
    return dict(SAUDI_SECTORS)


def get_sector_names_ar() -> list[str]:
    return [v["name_ar"] for v in SAUDI_SECTORS.values()]


def get_sector_by_code(code: str) -> dict[str, Any] | None:
    code_upper = code.upper().strip()
    for v in SAUDI_SECTORS.values():
        if v["code"] == code_upper:
            return v
    return None


def get_sub_sectors(sector: str) -> list[dict[str, str]]:
    s = sector.strip().lower()
    entry = SAUDI_SECTORS.get(s)
    if entry is None:
        return []
    return list(entry["sub_sectors"])


def get_sector_naics(sector: str) -> str | None:
    s = sector.strip().lower()
    entry = SAUDI_SECTORS.get(s)
    return entry["naics"] if entry else None


def get_sector_isic(sector: str) -> str | None:
    s = sector.strip().lower()
    entry = SAUDI_SECTORS.get(s)
    return entry["isic"] if entry else None


def search_sectors(query: str) -> list[dict[str, Any]]:
    q = query.strip().lower()
    results: list[dict[str, Any]] = []
    for key, val in SAUDI_SECTORS.items():
        if q in key or q in val["name_ar"].lower() or q in val["name_en"].lower():
            results.append({"key": key, **val})
    return results


__all__ = [
    "SAUDI_B2B_SECTORS",
    "SAUDI_SECTORS",
    "get_all_sectors",
    "get_sector_by_code",
    "get_sector_isic",
    "get_sector_naics",
    "get_sector_names_ar",
    "get_sub_sectors",
    "sector_known",
    "search_sectors",
]
