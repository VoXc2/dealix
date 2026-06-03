#!/usr/bin/env python3
"""Aggregate every component check into a weighted Launch Score and write the scorecard.

Exit 0 only when the score meets LAUNCH_MIN (default 90 — Full Launch).
Reused by `python dealix.py launch-score`.
"""
import importlib
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, rel, run_check  # noqa: E402

# module name -> (label_ar, weight). Weights sum to 100.
COMPONENTS = [
    ("check_file_manifest", "اكتمال الملفات (Manifest)", 10),
    ("check_schema_contracts", "صلاحية السكيمات والعقود", 12),
    ("check_business_os_catalog", "كتالوج أنظمة الأعمال", 10),
    ("check_need_intelligence", "ذكاء احتياج الأعمال", 12),
    ("check_account_pack_contract", "عقد Account Pack", 12),
    ("check_email_quality_gate", "بوابة جودة البريد", 10),
    ("check_proposal_gate", "بوابة العروض", 8),
    ("check_delivery_gate", "بوابة التسليم", 8),
    ("check_security_privacy_gates", "بوابات الأمن والخصوصية", 10),
    ("check_site_routes", "مسارات الموقع", 8),
]


def compute_scorecard() -> dict:
    rows = []
    score = 0
    for module_name, label, weight in COMPONENTS:
        mod = importlib.import_module(module_name)
        try:
            result = mod.check()
            passed = result.passed
            detail = "; ".join(result.errors[:2]) if result.errors else (result.info[0] if result.info else "")
        except Exception as exc:  # a crashing check is a failing check
            passed, detail = False, f"crash: {exc}"
        if passed:
            score += weight
        rows.append({"module": module_name, "label": label, "weight": weight,
                     "passed": passed, "detail": detail})
    full = score >= 90
    soft = score >= 75
    return {"score": score, "rows": rows, "full_launch_ready": full, "soft_launch_ready": soft}


def render_report(sc: dict) -> str:
    lines = [
        "# بطاقة الجاهزية للإطلاق (Ready-to-Launch Scorecard)",
        "",
        f"> Launch Score: **{sc['score']} / 100** — تاريخ: {date.today().isoformat()}",
        "",
        f"- Soft Launch Ready (≥ 75): **{'نعم' if sc['soft_launch_ready'] else 'لا'}**",
        f"- Full Launch Ready (≥ 90): **{'نعم' if sc['full_launch_ready'] else 'لا'}**",
        "",
        "## مكوّنات الدرجة",
        "",
        "| الفحص | الوزن | الحالة | تفاصيل |",
        "| --- | --- | --- | --- |",
    ]
    for row in sc["rows"]:
        status = "✅ PASS" if row["passed"] else "❌ FAIL"
        detail = (row["detail"] or "").replace("|", "/")[:80]
        lines.append(f"| {row['label']} | {row['weight']} | {status} | {detail} |")
    lines += [
        "",
        "## الحكم",
        "",
        ("✅ **Dealix جاهز للإطلاق الحقيقي** — الدرجة ≥ 90 وكل البوابات خضراء."
         if sc["full_launch_ready"] else
         ("🟡 جاهز لإطلاق ناعم (Soft Launch) — راجع الفحوصات الراسبة قبل الإطلاق الكامل."
          if sc["soft_launch_ready"] else
          "🔴 غير جاهز للإطلاق — عالج الفحوصات الراسبة.")),
        "",
        "_تم توليد هذه البطاقة عبر `python scripts/checks/check_ready_to_launch_scorecard.py`._",
    ]
    return "\n".join(lines) + "\n"


def check() -> CheckResult:
    r = CheckResult("ready_to_launch_scorecard")
    sc = compute_scorecard()
    out = rel("reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(sc), encoding="utf-8")

    minimum = int(os.environ.get("LAUNCH_MIN", "90"))
    for row in sc["rows"]:
        if not row["passed"]:
            r.error(f"{row['label']} FAILED: {row['detail']}")
    r.note(f"Launch Score = {sc['score']}/100 (min required {minimum})")
    r.require(sc["score"] >= minimum, f"Launch Score {sc['score']} < required {minimum}")
    return r


if __name__ == "__main__":
    from _common import main
    main(check)
