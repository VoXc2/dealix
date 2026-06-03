"""Railway launch readiness checks — env matrix (no secrets printed)."""

from __future__ import annotations

import os
from typing import Any


def _set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def check_railway_api_env() -> dict[str, Any]:
    """Backend production variables."""
    required = {
        "DATABASE_URL": _set("DATABASE_URL"),
        "APP_SECRET_KEY": _set("APP_SECRET_KEY"),
        "ENVIRONMENT": (os.getenv("ENVIRONMENT") or "").strip() == "production",
        "CORS_ORIGINS": _set("CORS_ORIGINS"),
        "ADMIN_API_KEYS": _set("ADMIN_API_KEYS"),
    }
    payments = {
        "MOYASAR_SECRET_KEY": _set("MOYASAR_SECRET_KEY"),
        "MOYASAR_WEBHOOK_SECRET": _set("MOYASAR_WEBHOOK_SECRET"),
    }
    ci = {
        "DEALIX_API_BASE": _set("DEALIX_API_BASE"),
        "DEALIX_API_KEY": _set("DEALIX_API_KEY"),
        "DEALIX_ADMIN_API_KEY": _set("DEALIX_ADMIN_API_KEY"),
    }
    missing_required = [k for k, ok in required.items() if not ok]
    missing_pay = [k for k, ok in payments.items() if not ok]
    missing_ci = [k for k, ok in ci.items() if not ok]
    return {
        "api_required": required,
        "payments": payments,
        "github_ci": ci,
        "missing_required": missing_required,
        "missing_payments": missing_pay,
        "missing_github_ci": missing_ci,
        "ready_for_api_deploy": len(missing_required) == 0,
        "ready_for_payments": len(missing_pay) == 0,
        "ready_for_daily_ci": len(missing_ci) == 0,
        "hint_ar": (
            "ADMIN_API_KEYS على API = نفس قيمة NEXT_PUBLIC_DEALIX_ADMIN_API_KEY على الفرونت"
            if not missing_required
            else "أكمل المتغيرات المطلوبة على خدمة API في Railway"
        ),
    }


def check_railway_frontend_env() -> dict[str, Any]:
    use_proxy = (os.getenv("NEXT_PUBLIC_USE_DEALIX_OPS_PROXY") or "").strip() == "1"
    fe = {
        "NEXT_PUBLIC_API_URL": _set("NEXT_PUBLIC_API_URL"),
        "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY": use_proxy,
        "DEALIX_ADMIN_API_KEY": _set("DEALIX_ADMIN_API_KEY"),
        "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY": _set("NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"),
    }
    missing = [k for k, ok in fe.items() if not ok]
    if use_proxy and not fe["DEALIX_ADMIN_API_KEY"]:
        if "DEALIX_ADMIN_API_KEY" not in missing:
            missing.append("DEALIX_ADMIN_API_KEY")
    if not use_proxy and not fe["NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"]:
        if "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY" not in missing:
            missing.append("NEXT_PUBLIC_DEALIX_ADMIN_API_KEY")
    return {
        "frontend": fe,
        "missing": missing,
        "ready_for_fe_deploy": len(missing) == 0,
        "hint_ar": (
            "استخدم NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1 + DEALIX_ADMIN_API_KEY على server "
            "(لا تضع المفتاح في المتصفح)"
            if use_proxy
            else "أو فعّل ops proxy — NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1"
        ),
    }
