"""Decision tree helpers — thin layer over ``qualify_opportunity`` for docs/tests."""

from __future__ import annotations

from auto_client_acquisition.sales_os.qualification import QualificationVerdict


def verdict_label_ar(verdict: QualificationVerdict) -> str:
    return {
        QualificationVerdict.ACCEPT: "قبول — Sprint محدد",
        QualificationVerdict.DIAGNOSTIC_ONLY: "تشخيص فقط",
        QualificationVerdict.REFRAME: "إعادة صياغة العرض",
        QualificationVerdict.REJECT: "رفض",
        QualificationVerdict.REFER_OUT: "إحالة خارجية",
    }.get(verdict, verdict.value)


__all__ = ["verdict_label_ar"]
