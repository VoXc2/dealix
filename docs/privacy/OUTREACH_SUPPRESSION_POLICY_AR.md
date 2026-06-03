# سياسة قائمة الاستبعاد للتواصل — Dealix (المرحلة 8)

سياسة قائمة الاستبعاد التي تحكم من لا يُتواصَل معه. القائمة القانونية الوحيدة: `data/outreach/suppression_list.jsonl` (`schemas/suppression.schema.json`). **الاستبعاد يحجب الإرسال دائمًا** ويُطبَّق قبل أي خطة. الإرسال موقوف افتراضيًا (`send_enabled=false`).

---

## 1. أنواع المُدخلات

| النوع | المعنى | مثال آمن |
|-------|--------|----------|
| `domain` | استبعاد نطاق كامل | `optout-example.sa` |
| `email` | استبعاد عنوان واحد | حساب بدور وظيفي |
| `company` | استبعاد شركة بالاسم | `DoNotContact Co` |

---

## 2. الأسباب

| السبب | الوصف |
|-------|-------|
| `opt_out_requested` | طلب المتلقي الإيقاف |
| `do_not_contact` | منع تواصل صريح |
| `role_account` | حساب بدور وظيفي (مثل noreply@) |
| `competitor` | جهة منافِسة |
| `hard_bounce` | ارتداد صلب دائم |
| `spam_complaint` | شكوى تصنيف كسبام |
| `manual` | إضافة يدوية مبرّرة |

---

## 3. النطاق (scope)

| القيمة | الأثر |
|--------|-------|
| `all` | استبعاد عبر كل الحملات والقطاعات |
| `sector` | استبعاد ضمن قطاع محدد |
| `campaign` | استبعاد ضمن حملة محددة |

> الافتراضي الأكثر أمانًا `all`. حقول المُدخل: `suppression_id` · `type` · `value` · `reason` · `scope` · `added_at`.

---

## 4. التطبيق قبل الإرسال

1. قبل بناء أي خطة دفعة، تُحمَّل قائمة الاستبعاد كاملة.
2. يُحجَب أي عنوان/نطاق/شركة مطابق — لا استثناءات.
3. لا تُعاد محاولة إرسال لعنوان مُستبعَد إطلاقًا.
4. تُسجَّل المراجعة الدورية في `reports/privacy/SUPPRESSION_REVIEW.md`.

مصادر الإضافة: `docs/outreach/BOUNCE_UNSUBSCRIBE_HANDLING_AR.md` و`docs/outreach/UNSUBSCRIBE_POLICY_AR.md`.

---

## 5. الخصوصية و PDPL

- لا بيانات شخصية في القائمة أو التقارير؛ نطاقات وأدوار وأسماء شركات فقط.
- طلب الاستبعاد قد يكون أساسًا لحق الحذف: `docs/privacy/DELETION_REQUEST_RUNBOOK_AR.md`.
- يتوافق مع `company_os/governance/pdpl_checklist.md` و`docs/privacy/SAUDI_PDPL_OUTBOUND_POLICY_AR.md`.

---

## 6. القواعد غير القابلة للتفاوض

1. القائمة القانونية الوحيدة هي `data/outreach/suppression_list.jsonl`.
2. الاستبعاد يحجب الإرسال دائمًا ويُطبَّق قبل أي خطة.
3. لا إزالة مُدخل دون مبرّر موثّق.
4. تبقى `send_enabled=false` حتى الحكم ≥ `LIMITED_SEND_READY` وموافقة المؤسس.

---

*Dealix · سياسة قائمة الاستبعاد · الاستبعاد يحجب الإرسال · `send_enabled=false` افتراضيًا · المرجع: SDAIA PDPL*
