# Account Scoring Model — نموذج تقييم الحسابات

نموذجان مستقلان لكل Pack: **Account Score** (لترتيب Top 100) و**Cash Priority Score** (لأولوية الكاش).

---

## 1. Account Score — من 100 (لاختيار Top 100)

| المعيار | الوزن | كيف يُحسب |
|---------|------:|-----------|
| Pain clarity | 25 | يرتفع مع مستوى الدليل (L0=8 … L4=25) |
| Contact availability | 20 | C0=4 · C1=10 · C2=15 · C3=18 · C4=20 |
| System fit | 20 | القطاع ضمن أول نظامين للنظام=20، ضمن القائمة=17، غير ذلك=11 |
| Ability-to-pay signal | 15 | low=5 · medium=10 · high=15 |
| Evidence level | 10 | L0=2 · L1=4 · L2=6 · L3=8 · L4=10 |
| Low risk | 10 | low=10 · medium=6 · high=0 |

### الحالات (Buckets)

```
85+    = Top Priority
75–84  = Approval Queue
65–74  = More Research / Rewrite
<65    = Reject / Nurture
```

> ملاحظة: «Top 100» = أفضل 100 **مؤهّلة** بحسب الترتيب، حتى لو نزل بعضها إلى bucket أدنى؛ الأهم أنها اجتازت قواعد الاستبعاد.

---

## 2. قواعد الاستبعاد من Top 100 (Hard Gates)

يُستبعد الحساب — مهما كان رقمه — إذا تحقق أيٌّ من:

```
لا يوجد recommended_system
لا يوجد best_contact_route
risk_level = high
evidence_level مفقود
status = suppressed أو do_not_contact = true
الإيميل يحتوي ادعاء مضمون
الألم مكتوب كحقيقة بلا دليل (L0/L1 بدون لغة احتمالية)
```

تُسجَّل الأسباب في `account_scoring.jsonl#exclusion_reasons`، ويتحقق المدقّق من صحتها.

---

## 3. Cash Priority Score — من 100 (لأولوية الكاش)

| المعيار | الوزن | كيف يُحسب |
|---------|------:|-----------|
| Ability to pay | 25 | low=9 · medium=17 · high=25 |
| Urgency | 25 | low=8 · medium=16 · high=25 |
| Ease of delivery | 20 | حسب النظام (Proposal&Proof=20 … WhatsApp=10) |
| Upsell potential | 15 | حسب النظام |
| Contact availability | 15 | C0=3 … C4=15 |

الأنظمة الأسرع تحويلًا للكاش (هامش أعلى، تكامل أقل): **Proposal & Proof OS**، **Follow-up Recovery OS**، **Executive Command OS**.

---

## 4. سلامة الحساب (تتحقق آليًا)

- مجموع تفصيل `account_score_breakdown` = `account_score` بالضبط.
- مجموع تفصيل `cash_priority_breakdown` = `cash_priority_score` بالضبط.
- كل المكوّنات ضمن سقوفها، والنتيجة بين 0 و100.

يتحقق `validate_account_intelligence.py` من هذه السلامة لكل 400 سجل.

---

*Version 1.0 — يقرأ مع EVIDENCE_LEVELS_AR و CONTACT_CONFIDENCE_LEVELS_AR*
