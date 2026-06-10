"""Arabic executive QA — 12 scoring dimensions with weighted evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ArabicQADimensions:
    clarity: int                       # الوضوح
    executive_tone: int                # النبرة التنفيذية
    saudi_business_fit: int            # ملاءمة السوق السعودي
    no_exaggeration: int               # عدم المبالغة
    claim_safety: int                  # أمان الادعاءات
    actionability: int                 # قابلية التنفيذ
    grammar_correctness: int = 100     # الصحة النحوية
    cultural_appropriateness: int = 100# الملاءمة الثقافية
    formatting_quality: int = 100      # جودة التنسيق
    honorific_usage: int = 100         # استخدام الألقاب
    pdpl_compliance: int = 100         # الامتثال لخصوصية البيانات
    vision_2030_alignment: int = 100   # التوافق مع رؤية ٢٠٣٠


@dataclass
class QAResult:
    total_score: int
    dimensions: dict[str, int]
    level: str                         # ممتاز / جيد / مقبول / ضعيف
    failures: list[str]
    warnings: list[str]
    recommendations: list[str]

    LEVELS = [
        (90, "ممتاز"),
        (75, "جيد"),
        (60, "مقبول"),
        (0, "ضعيف"),
    ]

    def __post_init__(self) -> None:
        for threshold, label in self.LEVELS:
            if self.total_score >= threshold:
                object.__setattr__(self, "level", label)
                break

    def passes(self) -> bool:
        return self.total_score >= 60

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_score": self.total_score,
            "level": self.level,
            "dimensions": self.dimensions,
            "passes": self.passes(),
            "failures": self.failures,
            "warnings": self.warnings,
            "recommendations": self.recommendations,
        }


# Dimension weights for weighted scoring
DIMENSION_WEIGHTS: dict[str, float] = {
    "clarity": 0.15,
    "executive_tone": 0.12,
    "saudi_business_fit": 0.10,
    "no_exaggeration": 0.12,
    "claim_safety": 0.12,
    "actionability": 0.08,
    "grammar_correctness": 0.07,
    "cultural_appropriateness": 0.08,
    "formatting_quality": 0.04,
    "honorific_usage": 0.04,
    "pdpl_compliance": 0.05,
    "vision_2030_alignment": 0.03,
}

# Dimension names in Arabic
DIMENSION_NAMES_AR: dict[str, str] = {
    "clarity": "الوضوح",
    "executive_tone": "النبرة التنفيذية",
    "saudi_business_fit": "ملاءمة السوق السعودي",
    "no_exaggeration": "عدم المبالغة",
    "claim_safety": "أمان الادعاءات",
    "actionability": "قابلية التنفيذ",
    "grammar_correctness": "الصحة النحوية",
    "cultural_appropriateness": "الملاءمة الثقافية",
    "formatting_quality": "جودة التنسيق",
    "honorific_usage": "استخدام الألقاب",
    "pdpl_compliance": "الامتثال لخصوصية البيانات",
    "vision_2030_alignment": "التوافق مع رؤية ٢٠٣٠",
}


def arabic_qa_score(d: ArabicQADimensions) -> int:
    """Compute a weighted QA score from dimensions (0-100)."""
    weights = DIMENSION_WEIGHTS
    dims_map = {
        "clarity": d.clarity,
        "executive_tone": d.executive_tone,
        "saudi_business_fit": d.saudi_business_fit,
        "no_exaggeration": d.no_exaggeration,
        "claim_safety": d.claim_safety,
        "actionability": d.actionability,
        "grammar_correctness": d.grammar_correctness,
        "cultural_appropriateness": d.cultural_appropriateness,
        "formatting_quality": d.formatting_quality,
        "honorific_usage": d.honorific_usage,
        "pdpl_compliance": d.pdpl_compliance,
        "vision_2030_alignment": d.vision_2030_alignment,
    }
    total_weight = sum(weights.values())
    score = sum(
        max(0, min(100, dims_map[k])) * w
        for k, w in weights.items()
    )
    return int(round(score / total_weight)) if total_weight > 0 else 0


def evaluate_qa(d: ArabicQADimensions) -> QAResult:
    """Full QA evaluation with warnings, failures, and recommendations."""
    composite = arabic_qa_score(d)
    dims = {
        "clarity": d.clarity,
        "executive_tone": d.executive_tone,
        "saudi_business_fit": d.saudi_business_fit,
        "no_exaggeration": d.no_exaggeration,
        "claim_safety": d.claim_safety,
        "actionability": d.actionability,
        "grammar_correctness": d.grammar_correctness,
        "cultural_appropriateness": d.cultural_appropriateness,
        "formatting_quality": d.formatting_quality,
        "honorific_usage": d.honorific_usage,
        "pdpl_compliance": d.pdpl_compliance,
        "vision_2030_alignment": d.vision_2030_alignment,
    }

    failures = []
    warnings = []
    recommendations = []

    # Check each dimension
    if d.clarity < 60:
        failures.append("الوضوح منخفض — استخدم جملاً أقصر وأكثر مباشرة")
    elif d.clarity < 80:
        warnings.append("يمكن تحسين الوضوح بجمل أكثر تركيزاً")

    if d.executive_tone < 60:
        failures.append("النبرة التنفيذية منخفضة — استخدم لغة أكثر رسمية")
    elif d.executive_tone < 80:
        warnings.append("يمكن تعزيز النبرة التنفيذية")

    if d.claim_safety < 70:
        failures.append("مخالفات ادعاءات محتملة — راجع قائمة الادعاءات الممنوعة")

    if d.no_exaggeration < 70:
        failures.append("مبالغة في الادعاءات — استخدم بدائل أكثر تحفظاً")

    if d.pdpl_compliance < 70:
        failures.append("مخالفة خصوصية البيانات — أضف إفصاح خصوصية واضح")

    if d.grammar_correctness < 60:
        failures.append("أخطاء نحوية — راجع النص مع مدقق لغوي")

    if d.saudi_business_fit < 60:
        failures.append("لا يتناسب مع سياق الأعمال السعودي")
    elif d.saudi_business_fit < 80:
        recommendations.append("عزز الملاءمة للسوق السعودي بأمثلة محلية")

    if d.honorific_usage < 80:
        recommendations.append("استخدم الألقاب المناسبة (الدكتور، المهندس، الأستاذ)")

    if d.vision_2030_alignment < 50:
        warnings.append("يمكن ربط المحتوى برؤية المملكة ٢٠٣٠")

    return QAResult(
        total_score=composite,
        dimensions=dims,
        level="",
        failures=list(set(failures)),
        warnings=list(set(warnings)),
        recommendations=list(set(recommendations)),
    )


def find_lowest_dimension(d: ArabicQADimensions) -> tuple[str, int]:
    """Return the name and score of the lowest dimension."""
    dims = {
        "clarity": d.clarity,
        "executive_tone": d.executive_tone,
        "saudi_business_fit": d.saudi_business_fit,
        "no_exaggeration": d.no_exaggeration,
        "claim_safety": d.claim_safety,
        "actionability": d.actionability,
        "grammar_correctness": d.grammar_correctness,
        "cultural_appropriateness": d.cultural_appropriateness,
        "formatting_quality": d.formatting_quality,
        "honorific_usage": d.honorific_usage,
        "pdpl_compliance": d.pdpl_compliance,
        "vision_2030_alignment": d.vision_2030_alignment,
    }
    lowest = min(dims.items(), key=lambda x: x[1])
    return lowest


__all__ = [
    "ArabicQADimensions",
    "DIMENSION_NAMES_AR",
    "DIMENSION_WEIGHTS",
    "QAResult",
    "arabic_qa_score",
    "evaluate_qa",
    "find_lowest_dimension",
]
