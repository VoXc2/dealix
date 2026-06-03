# Launch Decision Gate (بوابة قرار الإطلاق)

البوابة التي تقرر **هل نطلق، وبأي وضع**. لا إطلاق بدون المرور بهذه البوابة وتوقيع
المؤسس في `reports/launch/GO_NO_GO_DECISION.md`.

---

## خطوات البوابة

```txt
1. شغّل: python scripts/checks/check_launch_readiness.py
2. اقرأ: reports/launch/LAUNCH_SCORECARD.md  → السكور
3. اقرأ: reports/launch/LAUNCH_BLOCKERS.md   → عدد No-Go blockers المفتوحة
4. اقرأ: reports/launch/SECURITY_GO_NO_GO.md → بوابة الأمن/الخصوصية
5. قرّر الوضع وفق الجدول أدناه
6. وقّع القرار في reports/launch/GO_NO_GO_DECISION.md
```

## جدول القرار

| الحالة | القرار | الوضع المسموح |
|--------|--------|----------------|
| hard gates تفشل | **NO-GO** | لا شيء — أصلح أولًا |
| hard gates تمر، Score < 60 | CONDITIONAL GO | Internal Dry Run فقط |
| Score 60–74 | CONDITIONAL GO | Internal Dry Run فقط |
| Score 75–84، 0 blockers حرجة | GO | Soft Launch |
| Score 85–89 | GO | Controlled Launch |
| Score ≥ 90، 0 blockers، Actions green | GO | Full Launch |

## شروط NO-GO الفورية (تتجاوز السكور)

أي واحدة من هذه = NO-GO حتى لو كان كل شيء آخر جاهزًا:

```txt
- نظام يخترع أرقامًا أو إيميلات
- ادعاء مضمون في أي مسودّة
- لا suppression / do-not-contact
- لا external-content untrusted policy
- لا Email Quality Gate (للأوضاع فوق Dry Run)
- لا Mini Proposal approval gate (للأوضاع فوق Dry Run)
- secrets ظاهرة في logs/prompts/reports
```

## الحالة الحالية

```txt
hard gates: PASS
Launch Score: ≈ 45  →  بند "أقل من 60"
القرار: CONDITIONAL GO — Internal Dry Run فقط
بانتظار: توقيع المؤسس + بناء الأنظمة الناقصة لرفع السكور
```

القرار الموقّع: `reports/launch/GO_NO_GO_DECISION.md`.
