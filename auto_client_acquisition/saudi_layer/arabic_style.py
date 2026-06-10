"""Expanded Arabic style rules — 25+ rules for Saudi business communication."""

from __future__ import annotations

from typing import Any

ARABIC_STYLE_RULES: dict[str, dict[str, Any]] = {
    "formality": {
        "description": "Use formal Saudi Arabic, avoid Egyptian/Levantine dialect",
        "do": ["حضرة", "الأستاذ", "سعادة", "المدير", "فخامة"],
        "dont": ["أخي", "حبيبي", "باشا", "افندي", "عم", "خال"],
        "example": "سعادة المدير التنفيذي المحترم",
    },
    "gender": {
        "description": "Use masculine form as default for business, detect female names",
        "rules": [
            "Use masculine verbs for unknown gender",
            "Detect female names and switch to مؤنث",
            "For females use أنتِ not أنت",
        ],
        "example_male": "نشكركم على ثقتكم",
        "example_female": "نشكركن على ثقتكن",
    },
    "numbers": {
        "description": "Use Arabic-Indic numerals for Arabic text",
        "rules": [
            "٠١٢٣٤٥٦٧٨٩ for Arabic UI text",
            "Latin 0123 for technical content and code",
            "Mixed: use Arabic-Indic in full Arabic paragraphs",
        ],
        "example": "المبلغ ١٬٥٠٠ ريال سعودي",
    },
    "honorifics": {
        "description": "Use Saudi business honorifics appropriately",
        "rules": [
            "الأستاذ for professionals and educators",
            "الدكتور for PhD holders and medical doctors",
            "المهندس for engineers",
            "سعادة for executives, ministers, high officials",
            "صاحب السمو for princes",
            "صاحب السمو الملكي for crown princes and kings",
        ],
    },
    "short_sentences": {
        "description": "Prefer short, clear sentences in Arabic business writing",
        "rules": [
            "Maximum 25-30 words per sentence",
            "One idea per sentence",
            "Use bullet points for lists",
        ],
        "do": "نقدم حلولاً متكاملة. نضمن الجودة. نسلم في الوقت المحدد.",
        "dont": "نقدم حلولاً متكاملة ونضمن الجودة ونسلم في الوقت المحدد.",
    },
    "active_voice": {
        "description": "Prefer active voice over passive in business Arabic",
        "rules": [
            "Use active verbs: نقدم, نطور, نساعد",
            "Avoid passive: يتم تقديم, يتم تطوير",
        ],
        "do": "نطور حلولاً مبتكرة",
        "dont": "يتم تطوير حلول مبتكرة",
    },
    "direct_address": {
        "description": "Address the reader directly in Arabic business writing",
        "rules": [
            "Use لكم/لك instead of يتم/يتم",
            "Use personal address when possible",
        ],
        "do": "نقدم لكم حلولنا المتكاملة",
        "dont": "يتم تقديم الحلول المتكاملة",
    },
    "islamic_expressions": {
        "description": "Use Islamic expressions appropriately in Saudi context",
        "rules": [
            "بسم الله الرحمن الرحيم at start of formal documents",
            "السلام عليكم ورحمة الله وبركاته for greetings",
            "الحمد لله for positive news",
            "إن شاء الله for future plans",
            "ما شاء الله for compliments",
            "Avoid overuse in professional emails — use once is sufficient",
        ],
    },
    "greeting_sequence": {
        "description": "Standard Saudi greeting sequence for business",
        "rules": [
            "1. السلام عليكم ورحمة الله وبركاته",
            "2. ثم التحية: تحية طيبة وبعد،",
            "3. المقدمة: نشكر لكم تواصلكم",
            "4. الموضوع: نود إعلامكم...",
        ],
    },
    "closing_sequence": {
        "description": "Standard Saudi closing sequence",
        "rules": [
            "1. شاكرين لكم حسن تعاونكم",
            "2. وتفضلوا بقبول فائق الاحترام",
            "3. مع تحيات",
        ],
    },
    "avoid_translationese": {
        "description": "Avoid literal translation from English",
        "rules": [
            "Don't use English sentence structure mapped to Arabic",
            "Avoid: سيتم الاتصال بك (will be contacted)",
            "Prefer: سوف نتصل بك",
            "Avoid: هذا سوف يكون (this will be)",
            "Prefer: سيكون",
        ],
    },
    "saudi_digital_first": {
        "description": "Saudi Arabia is a digital-first market — acknowledge this in tone",
        "rules": [
            "Reference digital transformation and Vision 2030 when relevant",
            "Use terms like تحول رقمي and رقمنة",
            "Avoid implying Saudi Arabia is behind in technology",
        ],
    },
    "pronouns": {
        "description": "Pronoun usage in Saudi business Arabic",
        "rules": [
            "نحن (royal/formal we) for company voice",
            "أنتم (formal plural you) for client address",
            "هم (they) for third-party references",
            "Avoid أنا (I) in business — use نحن",
        ],
    },
    "negation": {
        "description": "Negation patterns in Arabic business writing",
        "rules": [
            "Use لم + past verb for past negation: لم نقم",
            "Use لن + present verb for future negation: لن نقوم",
            "Use لا + present verb for present negation: لا نقوم",
            "Avoid استخدام negative with ما in formal settings",
        ],
    },
    "emphasis": {
        "description": "Emphasis patterns in Saudi business Arabic",
        "rules": [
            "Use إن for emphasis: إننا نعمل بجد",
            "Use قد for certainty: قد أنجزنا المشروع",
            "Use لـ emphasis prefix: لنعملن معاً",
            "Avoid overemphasis — can sound arrogant",
        ],
    },
    "punctuation": {
        "description": "Punctuation in Arabic text",
        "rules": [
            "Arabic comma ، not English ,",
            "Arabic question mark ؟ not ?",
            "Arabic quotation marks « » not \"",
            "Use English numbers for mixed Arabic/English content",
            "Keep spaces around punctuation consistent",
        ],
    },
    "currency_format": {
        "description": "Currency formatting in Arabic business content",
        "rules": [
            "ريال سعودي or ر.س after the amount",
            "Space between number and currency: ١٬٠٠٠ ر.س",
            "For large numbers: ١٬٠٠٠٬٠٠٠ (comma separators)",
            "ثمنمائة not 800 when writing out in formal contracts",
        ],
    },
    "date_format": {
        "description": "Date formatting for Saudi context",
        "rules": [
            "Hijri dates come first when both are shown: ١٥ رمضان ١٤٤٦هـ",
            "Gregorian in parentheses: ١٥ مارس ٢٠٢٥م",
            "Preferred Saudi format: DD/MM/YYYY",
        ],
    },
    "time_format": {
        "description": "Time formatting",
        "rules": [
            "Use 24-hour format in formal Arabic",
            "Example: الساعة ١٥:٠٠ not 3:00 PM",
        ],
    },
    "titles_and_headers": {
        "description": "Title and header formatting",
        "rules": [
            "Arabic titles: bold and right-aligned",
            "Use title case sparingly — Arabic doesn't have capitalization",
            "Separate Arabic and English titles clearly",
        ],
    },
    "brand_voice": {
        "description": "Dealix-specific brand voice in Arabic",
        "rules": [
            "ديلكس as the brand name (transliteration)",
            "Professional, trustworthy, innovative tone",
            "Reference: نصنع الفرق, نبتكر الحلول",
            "Avoid: رخيص, سعر منخفض (cheap connotations)",
        ],
    },
    "sector_specific_tone": {
        "description": "Tone adjustments by sector",
        "rules": [
            "Technology: modern, innovative terms",
            "Healthcare: reassuring, professional",
            "Finance: formal, precise, trustworthy",
            "Real Estate: aspirational, detailed",
            "Retail: energetic, benefit-focused",
            "Government: extremely formal, protocol-rich",
        ],
    },
    "email_subject_format": {
        "description": "Arabic email subject line conventions",
        "rules": [
            "Prefix with موضوع: for formal contexts",
            "Keep under 60 characters",
            "Use: بخصوص for 'regarding'",
            "Format: [نوع الرسالة] — [الموضوع]",
        ],
        "example": "بخصوص: عرض خدمات التسويق الرقمي",
    },
    "sign_off_variations": {
        "description": "Appropriate sign-offs by relationship stage",
        "rules": [
            "Initial contact: وتفضلوا بقبول فائق الاحترام",
            "Active client: مع جزيل الشكر والتقدير",
            "Long-term partner: والسلام عليكم ورحمة الله وبركاته",
            "Internal: مع التحية",
        ],
    },
    "vision2030_references": {
        "description": "When and how to reference Vision 2030",
        "rules": [
            "Use sparingly — don't over-reference",
            "Relevant for: digital transformation, innovation, quality of life",
            "Format: رؤية المملكة ٢٠٣٠",
            "Reference specific programs when relevant: برنامج التحول الوطني",
        ],
    },
}

STYLE_RULES_AR: tuple[str, ...] = tuple(
    v["description"] for v in ARABIC_STYLE_RULES.values()
)

# Quick-reference lists
FORMAL_GREETINGS = [
    "السلام عليكم ورحمة الله وبركاته",
    "تحية طيبة وبعد",
    "سعادة / الأستاذ المحترم",
]

FORMAL_CLOSINGS = [
    "وتفضلوا بقبول فائق الاحترام والتقدير",
    "مع جزيل الشكر والتقدير",
    "شاكرين لكم حسن تعاونكم",
    "والسلام عليكم ورحمة الله وبركاته",
]

HONORIFICS_MAP: dict[str, str] = {
    "أستاذ": "الأستاذ",
    "دكتور": "الدكتور",
    "مهندس": "المهندس",
    "مستشار": "المستشار",
    "سعادة": "سعادة",
    "صاحب السمو": "صاحب السمو",
}


def get_style_rule(name: str) -> dict[str, Any] | None:
    return ARABIC_STYLE_RULES.get(name.strip().lower())


def get_all_style_rule_names() -> list[str]:
    return list(ARABIC_STYLE_RULES.keys())


def honorific_for_title(title: str) -> str | None:
    return HONORIFICS_MAP.get(title.strip().lower())


__all__ = [
    "ARABIC_STYLE_RULES",
    "FORMAL_CLOSINGS",
    "FORMAL_GREETINGS",
    "HONORIFICS_MAP",
    "STYLE_RULES_AR",
    "get_all_style_rule_names",
    "get_style_rule",
    "honorific_for_title",
]
