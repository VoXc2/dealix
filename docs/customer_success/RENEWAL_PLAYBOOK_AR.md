# دليل التجديد — Renewal Playbook

> **المستوى:** L3 Draft → L4 Act with Approval | **الموافقة:** موافقة المؤسس إلزامية قبل أي إرسال | **القاعدة الأولى:** لا تجديد بلا قيمة مُسلَّمة فعلية

---

## المبدأ الجوهري

التجديد في Dealix ليس عملية مبيعات — هو **استمرارية طبيعية** لعلاقة مبنية على قيمة مُسلَّمة وموثَّقة. لهذا **الشرط الأول والأخير: لا مسودة تجديد بلا دليل قيمة مُسلَّمة.**

```
evidence_level MUST ∈ {client_data, measured, verified}
cites_delivered_value MUST be non-empty
approval_required MUST be true
```

أي مسودة REN لا تستوفي هذه الشروط = **مرفوضة تلقائيًا** من سكربت الفحص.

---

## 1. محفزات التجديد (Renewal Triggers)

من `renewal.schema.json` — حقل `trigger`:

| المحفز | المعنى | متى يُفعَّل؟ |
|---|---|---|
| `first_successful_workflow` | أُسلِّم وعمل Workflow ناجح قابل للقياس | بعد تأكيد النتائج في WVR الأول |
| `weekly_value_proof` | WVR يحتوي رقمًا `measured`/`verified` | بعد إرسال WVR بموافقة + تحليل الاستجابة |
| `positive_feedback` | العميل أعرب عن رضاه صراحةً | بعد توثيق الرد الإيجابي |
| `21_30_days_post_delivery` | النافذة الزمنية الطبيعية بعد أول تسليم | اليوم 21–30 من بدء التسليم |
| `new_department_need` | العميل ذكر حاجة إدارة أخرى | بعد توثيق الحاجة في سجل الفرص |
| `new_campaign_or_source` | العميل أطلق حملة أو مصدر عملاء جديد | بعد تأكيد العميل للإطلاق |
| `delivery_milestone` | إنجاز تسليم رئيسي (milestone) موثَّق | بعد اعتماد الـ milestone |

**ملاحظة:** المحفز هو "ما حدث"، ليس "ما نريده". لا يُصنَّف محفز إلا إذا كان مُوثَّقًا في البيانات.

---

## 2. التوقيت المثالي للتجديد

**النافذة الذهبية: اليوم 21–30** من التسليم.

| ما قبل اليوم 14 | اليوم 14–20 | اليوم 21–30 | ما بعد اليوم 30 |
|---|---|---|---|
| مبكر جدًا — لا بيانات كافية | تقييم أولي فقط | النافذة المثالية — بيانات + قيمة + استجابة | لا يزال ممكنًا — راجع المحفزات |

**استثناء:** إذا كان `renewal_fit: strong` AND `evidence_level: verified` قبل اليوم 21 → يمكن تقديم المسودة مع موافقة المؤسس.

---

## 3. شروط فتح باب التجديد

**يجب توافر الشروط الأربعة معًا قبل كتابة أي مسودة REN-*:**

| # | الشرط | أين يُتحقق |
|---|---|---|
| 1 | `value_proof = true` في CHS-* | `data/customer_success/client_health.jsonl` |
| 2 | `evidence_level ∈ {client_data, measured, verified}` | حقل `evidence_level` في CHS-* |
| 3 | `cites_delivered_value` غير فارغ (مرجع WVR أو ميتريك) | يُكتب في مسودة REN-* |
| 4 | موافقة المؤسس مُخطَّط لها (`approval_required: true`) | ثابت في كل مسودة REN-* |

---

## 4. الخطوة الواحدة — قاعدة غير قابلة للتفاوض

**كل مسودة تجديد تقترح خطوة واحدة فقط.** لا خيارات متعددة، لا حزم، لا عروض مفتوحة في نفس الرسالة.

أمثلة على خطوة واحدة صحيحة:
- "الاستمرار بنفس الباقة لشهر إضافي."
- "تجربة شهر من `ai_revenue_ops_starter` لتثبيت النتائج."
- "مناقشة قصيرة (15 دقيقة) لمراجعة نتائج الشهر."

أمثلة مرفوضة:
- ❌ "يمكنك الاختيار بين X وY وZ."
- ❌ "لا تفوّت هذه الفرصة!"
- ❌ "هذا العرض محدود المدة."

---

## 5. موافقة المؤسس — إلزامية

كل مسودة REN-* تمر بـ:

```
1. كتابة المسودة بالذكاء الاصطناعي (L3 Draft)
2. مراجعة المؤسس للمسودة
3. موافقة المؤسس → تسجيل approved_by + approved_at
4. إرسال يدوي (L4 Act with Approval) — لا إرسال آلي في v1
5. تسجيل الإجراء في ai_action_ledger
```

`send_enabled = false` في كل مسودة حتى يُعدَّل يدويًا بعد موافقة المؤسس.

---

## 6. مسار التجديد خطوة بخطوة

```
تحقق من شروط التجديد (4 شروط)
          ↓
شروط مكتملة؟ ── لا ──→ استمر في بناء القيمة
          ↓
         نعم
          ↓
حدّد المحفز من القائمة المعتمدة
          ↓
اكتب مسودة REN-* بالذكاء الاصطناعي (L3)
  - trigger: [المحفز]
  - cites_delivered_value: [مرجع WVR + الرقم]
  - evidence_level: [measured/verified]
  - suggested_next_step: [خطوة واحدة فقط]
  - approval_required: true
  - approved: false
          ↓
أرسل المسودة للمؤسس للمراجعة
          ↓
موافقة المؤسس؟ ── لا ──→ سجّل الملاحظات وعدّل
          ↓
         نعم
          ↓
سجّل approved_by + approved_at
          ↓
أرسل للعميل يدويًا (L4)
          ↓
سجّل في ai_action_ledger
```

---

## 7. مثال حقيقي — REN-1001

من `data/renewals/renewals.jsonl`:

```json
{
  "id": "REN-1001",
  "company": "Digital Rise Agency",
  "product_id": "revenue_leakage_diagnostic",
  "trigger": "weekly_value_proof",
  "cites_delivered_value": [
    "WVR-1001: نسبة المتابعة 43%→61% (measured)",
    "استرجاع 12 فرصة في الأسبوع الأول"
  ],
  "evidence_level": "measured",
  "suggested_next_step": "الاستمرار بباقة شهرية لتثبيت المكسب (خطوة واحدة، بلا ضغط).",
  "approval_required": true,
  "approved": false,
  "status": "draft"
}
```

**لماذا هذه المسودة صحيحة؟**
- `evidence_level: measured` ✅
- `cites_delivered_value` يحتوي رقمًا محددًا ✅
- `suggested_next_step` خطوة واحدة فقط ✅
- `approval_required: true` ✅
- لا ضغط، لا وعد ROI ✅

---

## 8. ما لا يجوز أبدًا في مسودة التجديد

| المحظور | السبب |
|---|---|
| أسلوب ضغط أو إلحاح | يتعارض مع قيم Dealix ومع AGENTS.md §2 |
| ضمان ROI أو نتيجة محددة | محظور في AGENTS.md §2 و§7 |
| `evidence_level: assumption` أو `benchmark` | لا يكفي للتجديد — يفشل في الفحص |
| إرسال بلا موافقة المؤسس | L4/L5 يتطلب موافقة موثَّقة |
| أكثر من خطوة واحدة في نفس الرسالة | يُربك العميل ويُضعف الثقة |
| منتج خارج الكتالوج | `product_id` يجب أن ∈ `valid_product_ids` |

---

*آخر تحديث: 2026-06-03 | السكيمة: [renewal.schema.json](../../schemas/renewal.schema.json) | مرجع: [AGENTS.md](../../AGENTS.md) | محرك التجديد: [docs/renewal/RENEWAL_ENGINE_AR.md](../renewal/RENEWAL_ENGINE_AR.md)*
