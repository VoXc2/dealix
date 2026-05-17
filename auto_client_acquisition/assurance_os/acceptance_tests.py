"""Layer 3 — weekly Acceptance Tests.

25 behavioural tests across Sales, Marketing, Support, Affiliate and
Governance. These are RESULT-assurance checks the founder runs weekly;
each result is supplied via ``AssuranceInputs.acceptance_results`` as
``pass`` / ``fail``. Any test with no supplied result stays ``unknown``.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.models import (
    AcceptanceTestResult,
    AssuranceInputs,
)

_VALID = {"pass", "fail", "unknown"}

# (id, category, name_en, name_ar, expected)
ACCEPTANCE_TESTS: list[tuple[str, str, str, str, str]] = [
    ("at_sales_1", "sales", "Strong lead routes to qualified-A + approval task",
     "lead قوي يصل qualified_A وينشئ approval task", "qualified_A + approval task"),
    ("at_sales_2", "sales", "Weak lead is nurtured/archived without founder noise",
     "lead ضعيف يُؤرشف بلا إزعاج الفاوندر", "nurture/archive, no noise"),
    ("at_sales_3", "sales", "Interested reply returns proof pack + booking CTA",
     "رد مهتم يعيد proof pack و booking CTA", "proof pack + booking CTA"),
    ("at_sales_4", "sales", "Meeting done without notes is blocked",
     "Meeting done بلا notes مرفوض", "blocked"),
    ("at_sales_5", "sales", "Invoice send without approved scope is blocked",
     "إرسال فاتورة بلا scope معتمد مرفوض", "blocked"),
    ("at_mkt_1", "marketing", "Every CTA link contains a UTM",
     "كل رابط CTA يحتوي UTM", "UTM present"),
    ("at_mkt_2", "marketing", "Risk Score source appears in the lead record",
     "مصدر Risk Score يظهر في سجل الـ lead", "source recorded"),
    ("at_mkt_3", "marketing", "Proof Pack request creates a lead + evidence event",
     "طلب Proof Pack يخلق lead و evidence event", "lead + evidence event"),
    ("at_mkt_4", "marketing", "Every campaign shows the full funnel metrics",
     "كل حملة تعرض مقاييس القمع كاملة", "impressions..meetings"),
    ("at_mkt_5", "marketing", "Content without a CTA is not published",
     "محتوى بلا CTA لا يُنشر", "not published"),
    ("at_sup_1", "support", "'What is a Diagnostic?' answered from the KB",
     "سؤال ما هو Diagnostic يُجاب من KB", "answered from KB"),
    ("at_sup_2", "support", "'Do you guarantee revenue?' triggers escalation",
     "سؤال هل تضمنون الإيراد يُصعّد", "escalation"),
    ("at_sup_3", "support", "Refund request triggers escalation",
     "طلب refund يُصعّد", "escalation"),
    ("at_sup_4", "support", "Unknown question creates a knowledge gap",
     "سؤال مجهول يخلق knowledge gap", "knowledge gap"),
    ("at_sup_5", "support", "Answer without a source is blocked",
     "إجابة بلا مصدر مرفوضة", "blocked"),
    ("at_aff_1", "affiliate", "Affiliate without disclosure raises a compliance flag",
     "مسوّق بلا إفصاح يرفع compliance flag", "compliance flag"),
    ("at_aff_2", "affiliate", "Affiliate guaranteed-ROI claim is blocked",
     "ادعاء ROI مضمون من المسوّق مرفوض", "blocked"),
    ("at_aff_3", "affiliate", "Duplicate lead earns no commission",
     "lead مكرر لا يستحق عمولة", "no commission"),
    ("at_aff_4", "affiliate", "Unpaid invoice earns no commission",
     "فاتورة غير مدفوعة لا تستحق عمولة", "no commission"),
    ("at_aff_5", "affiliate", "Refund within clawback reverses the commission",
     "refund ضمن فترة الاسترداد يعكس العمولة", "commission reversed"),
    ("at_gov_1", "governance", "Security claim without a source is blocked",
     "ادعاء أمني بلا مصدر مرفوض", "blocked"),
    ("at_gov_2", "governance", "Case study without client permission is blocked",
     "دراسة حالة بلا إذن العميل مرفوضة", "blocked"),
    ("at_gov_3", "governance", "Revenue mark without invoice_paid is blocked",
     "تسجيل إيراد بلا invoice_paid مرفوض", "blocked"),
    ("at_gov_4", "governance", "High-risk agent action requires approval",
     "إجراء وكيل عالي الخطورة يتطلب موافقة", "approval required"),
    ("at_gov_5", "governance", "Evidence completeness below 90% blocks scaling",
     "اكتمال الأدلة أقل من 90% يمنع التوسع", "no scale"),
]


def run_acceptance_tests(inputs: AssuranceInputs) -> list[AcceptanceTestResult]:
    """Collect supplied weekly acceptance-test results."""
    results: list[AcceptanceTestResult] = []
    for tid, category, name_en, name_ar, expected in ACCEPTANCE_TESTS:
        raw = str(inputs.acceptance_results.get(tid, "unknown")).lower()
        result = raw if raw in _VALID else "unknown"
        results.append(
            AcceptanceTestResult(tid, category, name_en, name_ar, expected, result)
        )
    return results
