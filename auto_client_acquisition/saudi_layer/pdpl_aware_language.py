"""PDPL-aware language module — complete Saudi Data Privacy compliance.

Saudi Personal Data Protection Law (PDPL) — نظام حماية البيانات الشخصية
Royal Decree M/148, effective September 2023, enforced March 2024.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Standard PDPL disclosure template
PDPL_DISCLOSURE_AR = (
    "نحن نلتزم بحماية بياناتكم الشخصية وفقاً لنظام حماية البيانات الشخصية "
    "الصادر بالمرسوم الملكي رقم م/١٤٨. تُجمع بياناتكم لغرض تقديم الخدمة "
    "وتُحتفظ بها طوال مدة المشروع. لكم الحق في طلب تعديل أو حذف بياناتكم "
    "في أي وقت بالتواصل معنا. لمزيد من المعلومات، يرجى زيارة سياسة الخصوصية."
)

PDPL_DISCLOSURE_EN = (
    "We are committed to protecting your personal data under the Saudi "
    "Personal Data Protection Law (PDPL), Royal Decree M/148. Your data "
    "is collected for service delivery and retained for the project duration. "
    "You have the right to request modification or deletion at any time. "
    "Visit our Privacy Policy for more information."
)

PDPL_HINT_AR = "توضيح الغرض، أساس الاستخدام، مدة الاحتفاظ، وحق طلب الحذف عند انتهاء المشروع."

# Minimum disclosure elements required by PDPL Article 13
REQUIRED_DISCLOSURE_ELEMENTS_AR = [
    "الغرض من جمع البيانات",
    "أساس المعالجة القانوني",
    "مدة الاحتفاظ بالبيانات",
    "حقوق صاحب البيانات",
    "معلومات الاتصال بمسؤول حماية البيانات",
    "إمكانية نقل البيانات",
    "سياسة الاحتفاظ والتخلص",
]

REQUIRED_DISCLOSURE_ELEMENTS_EN = [
    "Purpose of data collection",
    "Lawful basis for processing",
    "Data retention period",
    "Data subject rights",
    "DPO contact information",
    "Data portability",
    "Retention and disposal policy",
]


@dataclass
class PDPLConsentRecord:
    """Record of PDPL consent obtained from a data subject."""

    data_subject_id: str
    purpose: str
    obtained_at: str  # ISO timestamp
    valid_until: str | None = None
    consent_type: str = "explicit"  # explicit, implicit, contractual
    withdrawn: bool = False
    withdrawn_at: str | None = None
    data_categories: list[str] = field(default_factory=lambda: [
        "الاسم", "رقم الجوال", "البريد الإلكتروني", "اسم الشركة"
    ])

    def is_valid(self) -> bool:
        if self.withdrawn:
            return False
        if self.valid_until is not None:
            from datetime import datetime
            expiry = datetime.fromisoformat(self.valid_until)
            return datetime.now() < expiry
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "data_subject_id": self.data_subject_id,
            "purpose": self.purpose,
            "obtained_at": self.obtained_at,
            "valid_until": self.valid_until,
            "consent_type": self.consent_type,
            "withdrawn": self.withdrawn,
            "withdrawn_at": self.withdrawn_at,
            "data_categories": self.data_categories,
            "is_valid": self.is_valid(),
        }


@dataclass
class PDPLAssessment:
    """PDPL compliance assessment for a piece of content or a process."""

    compliant: bool
    missing_elements: list[str]
    score: int  # 0-100
    risks: list[str]
    recommendations: list[str]

    def passes(self) -> bool:
        return self.compliant and self.score >= 70


PDPL_DATA_CATEGORIES: dict[str, dict[str, str]] = {
    "basic_contact": {
        "name_ar": "معلومات الاتصال الأساسية",
        "name_en": "Basic Contact Information",
        "examples_ar": "الاسم، رقم الجوال، البريد الإلكتروني",
        "sensitivity": "low",
    },
    "professional": {
        "name_ar": "البيانات المهنية",
        "name_en": "Professional Data",
        "examples_ar": "المسمى الوظيفي، اسم الشركة، القطاع",
        "sensitivity": "low",
    },
    "financial": {
        "name_ar": "البيانات المالية",
        "name_en": "Financial Data",
        "examples_ar": "رقم الحساب البنكي، معلومات الدفع",
        "sensitivity": "high",
    },
    "identification": {
        "name_ar": "بيانات الهوية",
        "name_en": "Identification Data",
        "examples_ar": "رقم الهوية، رقم الإقامة، جواز السفر",
        "sensitivity": "high",
    },
    "biometric": {
        "name_ar": "البيانات البيومترية",
        "name_en": "Biometric Data",
        "examples_ar": "بصمة الوجه، بصمة الإصبع",
        "sensitivity": "very_high",
    },
    "health": {
        "name_ar": "البيانات الصحية",
        "name_en": "Health Data",
        "examples_ar": "التاريخ الطبي، نتائج الفحوصات",
        "sensitivity": "very_high",
    },
}


def pdpl_required_disclosure_missing(text: str) -> list[str]:
    """Check which required PDPL disclosure elements are missing from text.

    Args:
        text: Arabic text to check.

    Returns:
        List of missing disclosure elements (Arabic).
    """
    blob = text.lower()
    missing: list[str] = []
    for element in REQUIRED_DISCLOSURE_ELEMENTS_AR:
        if element not in blob:
            missing.append(element)
    return missing


def assess_pdpl_compliance(text: str) -> PDPLAssessment:
    """Assess PDPL compliance of a piece of Arabic text.

    Args:
        text: Arabic text to assess.

    Returns:
        PDPLAssessment with findings.
    """
    missing = pdpl_required_disclosure_missing(text)
    risks: list[str] = []
    recommendations: list[str] = []

    if missing:
        risks.append(f"يفتقد {len(missing)} من عناصر الإفصاح المطلوبة في المادة ١٣")

    # Check for consent language
    if "موافقة" not in text and "أوافق" not in text:
        if "الغرض" in text:
            recommendations.append("أضف عبارة طلب موافقة صريحة")

    # Check for data retention language
    if "مدة" not in text:
        recommendations.append("أضف مدة الاحتفاظ بالبيانات")

    # Check for rights language
    if "حق" not in text or "الحق" not in text:
        recommendations.append("أذكر حقوق صاحب البيانات (طلب التعديل، الحذف)")

    score = max(0, 100 - (len(missing) * 15))

    compliant = len(missing) == 0 and score >= 70

    return PDPLAssessment(
        compliant=compliant,
        missing_elements=missing,
        score=score,
        risks=risks,
        recommendations=list(set(recommendations)),
    )


def get_pdpl_disclosure(
    language: str = "ar",
    include_contact: bool = True,
    dpo_email: str | None = None,
) -> str:
    """Get standard PDPL disclosure in the requested language.

    Args:
        language: 'ar' or 'en'.
        include_contact: Include DPO contact info.
        dpo_email: DPO email to include (optional).

    Returns:
        PDPL disclosure string.
    """
    if language == "en":
        text = PDPL_DISCLOSURE_EN
    else:
        text = PDPL_DISCLOSURE_AR

    if include_contact and dpo_email:
        contact_clause_ar = f"للتواصل مع مسؤول حماية البيانات: {dpo_email}"
        contact_clause_en = f"Contact our Data Protection Officer: {dpo_email}"
        text += f"\n{contact_clause_en if language == 'en' else contact_clause_ar}"

    return text


PDPL_SAFE_PHRASES_AR: list[str] = [
    "وفقاً لنظام حماية البيانات الشخصية",
    "بموافقتك المسبقة",
    "لغرض تقديم الخدمة",
    "لأغراض التعاقد",
    "يجوز لك طلب حذف بياناتك",
    "يمكنك تعديل بياناتك بالتواصل معنا",
    "نحتفظ ببياناتك طوال مدة العلاقة التعاقدية",
    "سياسة الخصوصية متوفرة على موقعنا",
]

PDPL_SAFE_PHRASES_EN: list[str] = [
    "In accordance with PDPL",
    "With your prior consent",
    "For service delivery purposes",
    "For contractual purposes",
    "You may request deletion of your data",
    "You can modify your data by contacting us",
    "We retain data for the duration of the contractual relationship",
    "Privacy policy is available on our website",
]


__all__ = [
    "PDPLAssessment",
    "PDPLConsentRecord",
    "PDPL_DATA_CATEGORIES",
    "PDPL_DISCLOSURE_AR",
    "PDPL_DISCLOSURE_EN",
    "PDPL_HINT_AR",
    "PDPL_SAFE_PHRASES_AR",
    "PDPL_SAFE_PHRASES_EN",
    "REQUIRED_DISCLOSURE_ELEMENTS_AR",
    "REQUIRED_DISCLOSURE_ELEMENTS_EN",
    "assess_pdpl_compliance",
    "get_pdpl_disclosure",
    "pdpl_required_disclosure_missing",
]
