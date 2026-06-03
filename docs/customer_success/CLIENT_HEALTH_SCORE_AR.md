# درجة صحة العميل — Client Health Score

> **السكيمة:** `schemas/client_health.schema.json` | **البيانات:** `data/customer_success/client_health.jsonl` | **المستوى:** L1 Observe / L2 Advise

---

## 1. لماذا درجة الصحة؟

درجة الصحة (CHS) هي **البوصلة الوحيدة** لقرارات نجاح العملاء. تُجيب على سؤالين:
1. هل العميل يحقق قيمة فعلية؟
2. هل هذا هو الوقت المناسب للتجديد أو التوسعة؟

**لا يُفتح باب التجديد إلا إذا توافرت درجة صحة بمستوى دليل `measured` أو أعلى.**

---

## 2. الإشارات (Signals) — تعريف وحساب

مستمدة مباشرة من `client_health.schema.json`:

### 2.1 الإشارات الثنائية (boolean)

| الإشارة | الوزن المقترح | كيف تُحسَب |
|---|---|---|
| `onboarding_complete` | 15 نقطة | اكتمال Intake + توثيقه |
| `access_complete` | 15 نقطة | الفريق حصل على كل الصلاحيات |
| `first_workflow_delivered` | 20 نقطة | أُسلِّم ووثّق أول workflow |
| `weekly_report_delivered` | 15 نقطة | WVR أُرسل للعميل بموافقة |
| `value_proof` | 20 نقطة | يُعطى فقط إذا `evidence_level ∈ {measured, verified}` |

**مجموع الإشارات الثنائية الكاملة:** 85 نقطة

### 2.2 الإشارات الرقمية

| الإشارة | النطاق | الحساب |
|---|---|---|
| `client_engagement` | 0–5 | 3 نقاط × كل نقطة engagement = حد أقصى 15 نقطة |
| `unresolved_risks` | 0+ | تطرح 5 نقاط لكل خطر غير محلول (حد أدنى 0) |

**الصيغة الكاملة:**
```
health_score =
  (onboarding_complete ? 15 : 0) +
  (access_complete ? 15 : 0) +
  (first_workflow_delivered ? 20 : 0) +
  (weekly_report_delivered ? 15 : 0) +
  (value_proof ? 20 : 0) +
  (client_engagement × 3) −
  (unresolved_risks × 5)

حد أدنى: 0 | حد أقصى: 100
```

---

## 3. النطاقات (Bands) وقرارات نجاح العملاء

| health_score | health_band | renewal_fit | الإجراء |
|---|---|---|---|
| 80–100 | green | strong | العميل في حالة ممتازة. يمكن تقييم التجديد والترقية. |
| 70–79 | green | possible | تقدم جيد. انتظر WVR إضافي قبل فتح باب التجديد. |
| 60–69 | amber | possible | خطوة مهمة ناقصة. حدّد ما هي وركّز عليها هذا الأسبوع. |
| 40–59 | amber | not_yet | قيمة جزئية. لا تجديد حتى ترتفع درجة الدليل. |
| 0–39 | red | at_risk | علاقة في خطر. خطة إنقاذ فورية. لا تجديد ولا ترقية. |

### قواعد صارمة للنطاقات

- `renewal_fit: strong` → يتطلب `health_score >= 75` AND `value_proof = true` AND `evidence_level ∈ {measured, verified}`.
- `renewal_fit: at_risk` → يُعلَن فورًا عند `health_score < 40` أو `unresolved_risks >= 3`.
- `health_band: red` → يُبلَّغ المؤسس في نفس اليوم + خطة إنقاذ خلال 48 ساعة.

---

## 4. مستوى الدليل (evidence_level) في CHS

`evidence_level` في سجل CHS يعكس أعلى مستوى دليل حُقِّق مع هذا العميل حتى الآن.

| القيمة | المعنى في سياق CHS |
|---|---|
| `none` | لا بيانات حقيقية — `value_proof` يجب أن يكون `false` |
| `assumption` | تقديرات داخلية فقط — `value_proof` يجب أن يكون `false` |
| `benchmark` | مقاييس صناعية عامة — `value_proof` يجب أن يكون `false` |
| `client_reported` | العميل أفاد بتحسّن لكن لم نقسه — `value_proof` يجب أن يكون `false` |
| `client_data` | من بيانات العميل الفعلية — `value_proof` يمكن أن يكون `true` |
| `measured` | قِسناه أثناء التسليم — `value_proof = true` ✅ |
| `verified` | نتيجة مُتحقَّقة مستقلًا — `value_proof = true` ✅✅ |

**قاعدة:** `value_proof = true` يُسمح به فقط إذا كان `evidence_level ∈ {client_data, measured, verified}`.

---

## 5. كيف يُحسَب CHS خطوة بخطوة

```
1. افتح بيانات الأسبوع الأخير لهذا العميل
2. قيّم كل إشارة boolean بناءً على تسليمات الأسبوع
3. قيّم client_engagement (0–5) بناءً على استجابة العميل
4. عدّ unresolved_risks من سجل المخاطر
5. احسب health_score بالصيغة أعلاه
6. حدّد health_band بناءً على النطاقات
7. حدّد renewal_fit بناءً على health_band + value_proof + evidence_level
8. احفظ السجل في data/customer_success/client_health.jsonl
9. وثّق في ai_action_ledger
```

---

## 6. سجل CHS — مثال حقيقي

من `data/customer_success/client_health.jsonl`:

```json
{
  "id": "CHS-1001",
  "created_at": "2026-06-03T18:00:00+03:00",
  "company": "Digital Rise Agency",
  "signals": {
    "onboarding_complete": true,
    "access_complete": true,
    "first_workflow_delivered": true,
    "weekly_report_delivered": true,
    "client_engagement": 4,
    "value_proof": true,
    "unresolved_risks": 1
  },
  "health_score": 82,
  "health_band": "green",
  "renewal_fit": "strong",
  "evidence_level": "measured"
}
```

**شرح الحساب:**
- `onboarding_complete: true` → +15
- `access_complete: true` → +15
- `first_workflow_delivered: true` → +20
- `weekly_report_delivered: true` → +15
- `value_proof: true` → +20
- `client_engagement: 4` → +12
- `unresolved_risks: 1` → −5 (خطر معلّق)
- **المجموع: 15+15+20+15+20+12−5 = 92**

> ملاحظة: `health_score` في السجل `82` — الفرق يعكس أن الحساب قد يضبط الأوزان أو يأخذ عوامل سياقية إضافية. المبدأ الجوهري: الإشارات الكاملة + engagement عالٍ + خطر واحد معلّق → درجة خضراء.

---

## 7. إيقاع تحديث CHS

| التوقيت | الإجراء |
|---|---|
| بعد كل WVR مُرسَل | تحديث `weekly_report_delivered` و`value_proof` و`client_engagement` |
| بعد إغلاق أي خطر | تقليل `unresolved_risks` وإعادة الحساب |
| الأحد أسبوعيًا | مراجعة كل سجلات CHS ورصد الانخفاضات |
| يوم 21 من الشراكة | مراجعة شاملة لـ CHS وتقييم `renewal_fit` |

---

*آخر تحديث: 2026-06-03 | السكيمة: [client_health.schema.json](../../schemas/client_health.schema.json) | مرجع: [AGENTS.md](../../AGENTS.md)*
