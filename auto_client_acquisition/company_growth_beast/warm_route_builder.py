"""Warm routes only — no cold outbound."""

from __future__ import annotations

from typing import Any


def build_warm_route_pack(profile: dict[str, Any], targets: list[dict[str, Any]] | None) -> dict[str, Any]:
    top = (targets or [{}])[0] if targets else {}
    route = str(top.get("recommended_route") or "warm_intro_or_partner")

    routes_ar = {
        "warm_intro_or_partner": "أفضل مسار: مقدمة من مؤسس/شريك أو عميل حالي.",
        "inbound_diagnostic_then_manual_followup": "أفضل مسار: صفحة تشخيص ثم متابعة يدوية بعد الموافقة.",
        "content_cta_and_webinar_draft": "أفضل مسار: محتوى + دعوة جلسة (مسودة) ثم قائمة انتظار يدوية.",
    }

    return {
        "schema_version": 1,
        "action_mode": "draft_only",
        "primary_route": route,
        "primary_route_ar": routes_ar.get(route, "مقدمة دافئة أو inbound — بدون قوائم باردة."),
        "secondary_routes_ar": [
            "إحالة من عميل راضٍ",
            "مشاركة مجتمع محترمة (بدون إزعاج)",
            "بريد يدوي لجهة معروفة فقط",
        ],
        "blocked_routes_ar": ["واتساب بارد", "سكرابينغ", "أتمتة لينكدإن", "إرسال جماعي غير موافق"],
        "language_primary": "ar",
    }
