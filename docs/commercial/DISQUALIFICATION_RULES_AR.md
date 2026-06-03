# قواعد الاستبعاد وبوابة الانسحاب — Dealix

> الحقيقة المرجعية: `data/commercial/icp_segments.yaml` (حقل `disqualifiers` لكل قطاع) +
> بوابة الانسحاب في الكود `evaluate_fit` داخل `tests/_loaders.py`، ويختبرها
> `tests/test_walk_away_rules.py`. هذا المستند يشرح القواعد ولا يكرّر الكود.

الهدف: نحمي وقت الطرفين. لا نلاحق عميلاً غير مناسب، ولا نَعِد بما لا نقدر عليه.
الاستبعاد قرار محترم لا رفض شخصي — نوضّح السبب ونترك الباب مفتوحاً عند تغيّر الظرف.

---

## 1) القواعد الصريحة (Hard disqualifiers)

| # | القاعدة | المعنى العملي | الإشارة في الكود |
|---|---------|----------------|-------------------|
| D1 | لا leads متكرّرة | لا تدفّق استفسارات منتظم نرتّبه ونقيسه | `recurring_leads = false` |
| D2 | لا وصول لصاحب القرار | لا نصل لمن يعتمد القرار والدفع | `decision_maker_access = false` |
| D3 | لا قدرة على الدفع | الميزانية خارج أدنى نطاق `DLX-L1` | `ability_to_pay = false` |
| D4 | يريد إرسالاً جماعياً/سبام | يطلب bulk/cold بلا موافقة أو تخصيص | `wants_mass_sending = true` |
| D5 | يريد ضمان مبيعات | يطلب وعداً بنتائج/إيرادات مضمونة | `wants_guaranteed_sales = true` |
| D6 | يرفض عملية الموافقة | لا يقبل approval قبل أي إرسال | `refuses_approval = true` |
| D7 | يطلب scraping مشبوه | جمع بيانات غير قانوني أو مخالف للخصوصية | `requests_scraping = true` |
| D8 | يرفض أساسيات الخصوصية | يرفض الحد الأدنى لحماية البيانات | يُمنع — راجع سياسة الخصوصية |
| D9 | عمل مخصّص ثقيل بلا مقابل | تطوير ضخم خارج النطاق بلا عقد | يُمنع — يُحوّل إلى `DLX-L6` بنطاق موقّع |
| D10 | مخاطر تسليم عالية جداً | لا نقدر تسليم نتيجة محترمة بثقة | يُقيّم يدوياً قبل العرض |

ملاحظة: القواعد D1–D7 مُمَكْنَنة في `evaluate_fit` وتُرجِع جميعها سبباً موحّداً
`disqualified_bad_fit`. القواعد D8–D10 حُكم بشري قبل العرض، ومتجذّرة في
`out_of_scope` و`risks` بكتالوج المنتج `data/commercial/product_catalog.yaml`.

---

## 2) ربط القطاعات بقواعد الاستبعاد

كل قطاع يُعلن `disqualifiers` صراحة (يفرضه `test_segments_declare_disqualifiers`).

| القطاع | disqualifiers المُعلنة |
|--------|------------------------|
| `marketing_agencies` | `no_recurring_leads`, `wants_mass_sending`, `refuses_approval_process` |
| `training_companies` | `no_decision_maker_access`, `no_recurring_leads` |
| `clinics` | `requests_pii_scraping`, `refuses_privacy_basics` |
| `real_estate_teams` | `wants_guaranteed_sales_claims`, `wants_mass_sending` |
| `recruitment_agencies` | `no_recurring_leads`, `refuses_approval_process` |
| `professional_services` | `no_decision_maker_access`, `delivery_risk_too_high` |
| `education_providers` | `no_recurring_leads`, `no_ability_to_pay` |
| `logistics_companies` | `no_decision_maker_access`, `refuses_approval_process` |
| `restaurant_groups` | `no_recurring_leads`, `wants_mass_sending` |
| `local_saas` | `wants_guaranteed_sales_claims`, `refuses_approval_process` |

---

## 3) كيف تتصل بالبوابة (Walk-away gate)

- المُقيِّم `evaluate_fit(x)` يعيد `ok=true` فقط إذا لم تتحقّق أي قاعدة سلبية.
- أي تحقّق لقاعدة واحدة كافٍ ⇐ `ok=false` والسبب `disqualified_bad_fit`.
- العميل الجيّد (كل الإيجابيات صحيحة وكل السلبيات خاطئة) يمرّ — يؤكّده
  `test_good_fit_passes`، والعميل المُسيء يُستبعد — يؤكّده `test_spam_client_is_disqualified`.
- حالات القبول/الرفض الكاملة في `data/evals/commercial_safety_cases.jsonl`
  (مثل `CS-PASS-FIT-GOOD` و`CS-FAIL-FIT-SPAM`) ويتحقّق منها `test_fit_eval_cases`.

تدفّق القرار:

```
إشارة/استفسار → فحص D1..D7 (evaluate_fit) → فحص بشري D8..D10
   ├─ مرّ      → نكمل التأهيل ومطابقة العرض (OFFER_MATCHING_RULES_AR.md)
   └─ استُبعد  → سبب واضح + باب مفتوح عند تغيّر الظرف (لا ملاحقة)
```

---

## 4) لغة الاستبعاد المسموحة

- نوضّح أننا **نساعد ونرتّب ونقيس بموافقة**، ولا **نضمن** نتائج ولا نرسل نيابة بلا اعتماد.
- لا ادّعاءات ممنوعة عند الرفض (لا «نضاعف الإيرادات»، لا «نتائج مضمونة»، لا «بدون مخاطرة»).
- لا بيانات شخصية في التوثيق — أدوار فقط. أي مثال يُوسم «مثال توضيحي».

> سطر واحد: نستبعد بوضوح واحترام؛ البوابة في `evaluate_fit` تحرسها اختبارات `test_walk_away_rules.py`.
