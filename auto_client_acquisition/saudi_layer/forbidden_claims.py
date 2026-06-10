"""Expanded forbidden claims — 40+ entries with legal basis and alternatives."""

from __future__ import annotations

from typing import Any

FORBIDDEN_CLAIMS_ARABIC: list[dict[str, str]] = [
    # === Guarantees / ضمانات ===
    {
        "phrase": "نضمن",
        "category": "guarantee",
        "law": "نظام الإعلانات السعودي — المادة ٨",
        "alternative": "نسعى لتحقيق",
        "context": "لا يجوز ضمان نتائج غير قابلة للضمان القانوني",
    },
    {
        "phrase": "مضمون",
        "category": "guarantee",
        "law": "نظام الإعلانات السعودي",
        "alternative": "ذو موثوقية عالية",
    },
    {
        "phrase": "النتيجة مضمونة",
        "category": "guarantee",
        "law": "نظام الإعلانات السعودي — المادة ١٠",
        "alternative": "نتائجنا تتحدث عن نفسها",
    },
    {
        "phrase": "ضمان مبيعات",
        "category": "guarantee",
        "law": "نظام التجارة الإلكترونية",
        "alternative": "خطط لزيادة المبيعات",
    },
    {
        "phrase": "مضمون ١٠٠٪",
        "category": "guarantee",
        "law": "نظام الإعلانات السعودي — المادة ٨",
        "alternative": "نسبة نجاح عالية",
    },
    {
        "phrase": "ضمان استرداد الأموال",
        "category": "guarantee",
        "law": "نظام حماية المستهلك",
        "alternative": "سياسة استرداد مرنة",
        "context": "مسموح فقط إذا كانت السياسة مطبقة فعلاً",
    },
    # === Superlatives / مبالغات ===
    {
        "phrase": "الأفضل",
        "category": "superlative",
        "law": "نظام الإعلانات السعودي — المادة ٩",
        "alternative": "من الأفصل في السوق",
        "context": "الأفضل تتطلب إثباتاً موضوعياً",
    },
    {
        "phrase": "الأول",
        "category": "superlative",
        "law": "نظام الإعلانات السعودي",
        "alternative": "من الرواد في المجال",
    },
    {
        "phrase": "رقم واحد",
        "category": "superlative",
        "law": "نظام المنافسة",
        "alternative": "من الشركات الرائدة",
    },
    {
        "phrase": "الأسرع",
        "category": "superlative",
        "law": "نظام الإعلانات",
        "alternative": "من الأسرع في السوق",
    },
    {
        "phrase": "الأرخص",
        "category": "superlative",
        "law": "نظام حماية المستهلك",
        "alternative": "أسعار تنافسية",
    },
    {
        "phrase": "الأكبر",
        "category": "superlative",
        "law": "نظام المنافسة",
        "alternative": "من كبرى الشركات في المجال",
    },
    {
        "phrase": "الأفضل في المملكة",
        "category": "superlative",
        "law": "نظام الإعلانات السعودي",
        "alternative": "من الشركات المتميزة في المملكة",
    },
    # === Absolute claims / ادعاءات مطلقة ===
    {
        "phrase": "دائماً",
        "category": "absolute",
        "law": "نظام الإعلانات السعودي",
        "alternative": "في معظم الحالات",
    },
    {
        "phrase": "أبداً",
        "category": "absolute",
        "law": "نظام الإعلانات",
        "alternative": "في العادة",
    },
    {
        "phrase": "الكل",
        "category": "absolute",
        "law": "نظام الإعلانات",
        "alternative": "الكثير من",
    },
    {
        "phrase": "جميع العملاء",
        "category": "absolute",
        "law": "نظام حماية المستهلك",
        "alternative": "غالبية العملاء",
    },
    {
        "phrase": "صفر مخاطرة",
        "category": "absolute",
        "law": "نظام الإعلانات السعودي",
        "alternative": "مخاطرة منخفضة",
    },
    {
        "phrase": "لا منافس",
        "category": "absolute",
        "law": "نظام المنافسة",
        "alternative": "من بين المنافسين الرئيسيين",
    },
    # === Financial promises / وعود مالية ===
    {
        "phrase": "ربح مؤكد",
        "category": "financial",
        "law": "نظام السوق المالية",
        "alternative": "عوائد مجدية",
    },
    {
        "phrase": "عائد مضمون",
        "category": "financial",
        "law": "نظام هيئة السوق المالية",
        "alternative": "عائد متوقع",
    },
    {
        "phrase": "أرباح خيالية",
        "category": "financial",
        "law": "نظام مكافحة التضليل",
        "alternative": "أرباح مجدية",
    },
    {
        "phrase": "ضعف رأس المال",
        "category": "financial",
        "law": "نظام السوق المالية",
        "alternative": "نمو في رأس المال",
    },
    {
        "phrase": "استثمار مضمون",
        "category": "financial",
        "law": "نظام السوق المالية",
        "alternative": "فرصة استثمارية",
    },
    # === Medical/health / ادعاءات طبية ===
    {
        "phrase": "يعالج",
        "category": "medical",
        "law": "نظام الهيئة العامة للغذاء والدواء",
        "alternative": "يساعد في",
        "context": "الادعاءات العلاجية تخضع لترخيص هيئة الدواء",
    },
    {
        "phrase": "يشفي",
        "category": "medical",
        "law": "نظام الهيئة العامة للغذاء والدواء",
        "alternative": "يدعم الصحة",
    },
    {
        "phrase": "معجزة",
        "category": "medical",
        "law": "لائحة الإعلانات الصحية",
        "alternative": "فعال",
    },
    {
        "phrase": "علاج سحري",
        "category": "medical",
        "law": "لائحة الإعلانات الصحية",
        "alternative": "حل فعال",
    },
    # === Comparison claims / ادعاءات مقارنة ===
    {
        "phrase": "أفضل من",
        "category": "comparison",
        "law": "نظام المنافسة",
        "alternative": "من بين الخيارات المتميزة",
        "context": "لا يجوز ذكر المنافسين صراحة",
    },
    {
        "phrase": "نختلف عنهم لأن",
        "category": "comparison",
        "law": "نظام الإعلانات",
        "alternative": "مميزاتنا تشمل",
    },
    {
        "phrase": "المنافسون لا",
        "category": "comparison",
        "law": "نظام المنافسة — المادة ٤",
        "alternative": "نحن نتميز بـ",
    },
    # === Misleading / تضليل ===
    {
        "phrase": "مجاني",
        "category": "misleading",
        "law": "نظام حماية المستهلك — المادة ٥",
        "alternative": "بدون رسوم إضافية / ضمن الباقة",
        "context": "مجاني فقط إذا كان بالفعل بدون أي مقابل",
    },
    {
        "phrase": "خصم يصل إلى",
        "category": "misleading",
        "law": "نظام حماية المستهلك",
        "alternative": "خصم",
        "context": "يصل إلى تتطلب أن يشمل الأقلية",
    },
    {
        "phrase": "لفترة محدودة",
        "category": "misleading",
        "law": "نظام حماية المستهلك",
        "alternative": "عرض سار حتى تاريخ",
        "context": "يجب تحديد تاريخ انتهاء دقيق",
    },
    {
        "phrase": "الكثيرون يختاروننا",
        "category": "misleading",
        "law": "نظام الإعلانات",
        "alternative": "نفتخر بثقة عملائنا",
    },
    {
        "phrase": "المسحوبات الأخيرة",
        "category": "misleading",
        "law": "نظام الإعلانات",
        "alternative": "للاطلاع على نتائجنا",
        "context": "في غير المسابقات والجوائز المرخصة",
    },
    # === Religious/Trust / دينية ===
    {
        "phrase": "متوافق مع الشريعة (لغير المرخص)",
        "category": "religious",
        "law": "لائحة المصطلحات الشرعية",
        "alternative": "نلتزم بالضوابط الشرعية",
        "context": "يتطلب ترخيص هيئة الرقابة الشرعية",
    },
    {
        "phrase": "حلال (لغير الغذاء)",
        "category": "religious",
        "law": "نظام هيئة الغذاء والدواء",
        "alternative": "نلتزم بالمعايير الإسلامية",
    },
    {
        "phrase": "معتمد",
        "category": "trust",
        "law": "نظام الإعلانات",
        "alternative": "حاصل على شهادة",
        "context": "يجب ذكر جهة الاعتماد صراحة",
    },
    {
        "phrase": "مرخص",
        "category": "trust",
        "law": "نظام الإعلانات السعودي",
        "alternative": "مرخص من [الجهة]",
        "context": "يجب ذكر جهة الترخيص",
    },
    {
        "phrase": "حكومي",
        "category": "trust",
        "law": "نظام حماية العلامة التجارية",
        "alternative": "نعمل مع جهات حكومية من ضمنها",
    },
]


def forbidden_arabic_claim_detected(text: str, detailed: bool = False) -> bool | dict[str, Any]:
    """Check if text contains any forbidden claims.

    Args:
        text: The Arabic text to check.
        detailed: If True, return details of matched claims.

    Returns:
        bool if detailed=False, dict with match info if detailed=True.
    """
    blob = text.lower()
    matches: list[dict[str, str]] = []
    for entry in FORBIDDEN_CLAIMS_ARABIC:
        if entry["phrase"] in blob:
            matches.append(entry)

    if not matches:
        return False if not detailed else {"detected": False, "matches": []}

    if detailed:
        return {
            "detected": True,
            "matches": matches,
            "suggestions": [
                {"original": m["phrase"], "alternative": m["alternative"]}
                for m in matches
            ],
        }
    return True


def get_claim(phrase: str) -> dict[str, str] | None:
    """Get details about a specific forbidden phrase."""
    for entry in FORBIDDEN_CLAIMS_ARABIC:
        if entry["phrase"] == phrase.strip():
            return entry
    return None


def get_claims_by_category(category: str) -> list[dict[str, str]]:
    """Get all forbidden claims in a category."""
    return [e for e in FORBIDDEN_CLAIMS_ARABIC if e.get("category") == category.strip().lower()]


def safe_alternative(text: str) -> str:
    """Replace known forbidden phrases with safe alternatives."""
    result = text
    for entry in FORBIDDEN_CLAIMS_ARABIC:
        result = result.replace(entry["phrase"], entry["alternative"])
    return result


def render_permitted_alternative(phrase: str) -> str | None:
    """Get the permitted alternative for a given forbidden phrase."""
    entry = get_claim(phrase)
    return entry["alternative"] if entry else None


__all__ = [
    "FORBIDDEN_CLAIMS_ARABIC",
    "forbidden_arabic_claim_detected",
    "get_claim",
    "get_claims_by_category",
    "render_permitted_alternative",
    "safe_alternative",
]
