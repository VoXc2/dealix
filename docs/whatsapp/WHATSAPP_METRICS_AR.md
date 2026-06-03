# مقاييس أداء واتساب (WhatsApp Metrics)
## تعريفات المقاييس وكيف تغذّي تقارير reports/whatsapp/

> **الغرض:** يعرّف هذا المستند مقاييس الأداء الرئيسية لقناة واتساب بعد الموافقة — تعريف كل مقياس، طريقة الحساب، المصدر، وكيف تُدمج في تقارير `reports/whatsapp/`.

---

## 1. نظرة عامة على إطار القياس

```
data/whatsapp/sessions.jsonl       → مقاييس الجلسات
data/whatsapp/action_cards.jsonl   → مقاييس البطاقات
data/whatsapp/client_assessments.jsonl → مقاييس الفحص
data/whatsapp/handoffs.jsonl       → مقاييس التسليم
data/whatsapp/support_tickets.jsonl → مقاييس الدعم
          │
          ▼
    reports/whatsapp/WHATSAPP_METRICS_REPORT.md
    (أسبوعي + شهري)
```

---

## 2. مقاييس الجلسات (Session Metrics)

### م1: معدل تحويل ما بعد الرد (Post-Reply Conversion Rate)

```
= عدد الجلسات التي أكملت readiness_scan ÷ إجمالي الجلسات × 100
```
- **المصدر:** `sessions.jsonl` → `current_flow == 'service_recommendation' AND status != 'opted_out'`
- **الهدف:** ≥ 60%
- **يُبلَّغ عنه:** أسبوعيًا

### م2: معدل الجلسات النشطة

```
= عدد الجلسات بـ status='active' ÷ إجمالي الجلسات المفتوحة × 100
```
- **المصدر:** `sessions.jsonl`

### م3: معدل الانسحاب (Opt-Out Rate)

```
= عدد الجلسات بـ consent.opt_out=true ÷ إجمالي الجلسات × 100
```
- **التنبيه:** إذا تجاوز 5% → تحقيق فوري في سبب الانسحاب
- **المصدر:** `sessions.jsonl` → `consent.opt_out == true`

---

## 3. مقاييس بطاقات الإجراء (Action Card Metrics)

### م4: معدل الموافقة (Card Approval Rate)

```
= عدد البطاقات بـ status='approved' ÷ إجمالي البطاقات بـ approval_required=true × 100
```
- **يقيس:** كفاءة طابور الموافقات
- **الهدف:** ≥ 80% خلال SLA

### م5: معدل انتهاء الصلاحية (Card Expiry Rate)

```
= عدد البطاقات بـ status='expired' ÷ إجمالي البطاقات × 100
```
- **التنبيه:** إذا تجاوز 20% → مراجعة أوقات SLA أو عمليات الموافقة

### م6: معدل استخدام "ما أعرف — اقترح علي"

```
= عدد المرات التي اختار فيها العميل dont_know_suggest ÷ إجمالي تفاعلات البطاقات × 100
```
- **يقيس:** وضوح الخيارات المُقدَّمة. معدل مرتفع = رسائل غير واضحة

---

## 4. مقاييس فحص الجاهزية (Assessment Metrics)

### م7: متوسط درجة جاهزية الإيراد

```
= مجموع revenue_readiness لكل التقييمات ÷ عدد التقييمات
```
- **المصدر:** `client_assessments.jsonl` → `scores.revenue_readiness`

### م8: توزيع المنتج الموصى به

```
= تعداد recommended_product_id لكل القيم
```
- **يساعد في:** توقع الطلب على كل منتج في الكتالوج

### م9: متوسط درجة نضج المتابعة

```
= مجموع followup_maturity ÷ عدد التقييمات
```

---

## 5. مقاييس التسليم البشري (Handoff Metrics)

### م10: معدل التسليم البشري (Human Handoff Rate)

```
= عدد HHO التي أُنشئت ÷ إجمالي الجلسات × 100
```
- **الهدف:** < 30% (تسليم بشري كثير يعني مشكلة في الأتمتة أو وضوح الرسائل)
- **المصدر:** `handoffs.jsonl`

### م11: معدل التسليم بسبب طلب العميل

```
= عدد HHO بـ reason='client_requested' ÷ إجمالي HHO × 100
```
- **يفرّق بين:** تسليم اختياري (إيجابي) وتسليم إجباري (مشكلة)

### م12: الوقت للاستجابة الأولى (First Response Time)

```
= متوسط (assigned_at - created_at) لكل سجلات HHO
```
- **المصدر:** `handoffs.jsonl` → مقارنة `created_at` مع أول تغيير في `status`
- **الهدف:** ≤ SLA المحدد لكل urgency

---

## 6. مقاييس الدعم (Support Metrics)

### م13: متوسط وقت حل التذاكر (Mean Time to Resolution)

```
= متوسط (resolved_at - created_at) لكل SUP بـ status='closed'
```
- **المصدر:** `support_tickets.jsonl`

### م14: معدل انتهاك SLA

```
= عدد التذاكر التي تجاوزت sla_due_at ÷ إجمالي التذاكر × 100
```
- **التنبيه:** أي انتهاك لـ`critical` يستوجب تحقيقًا فوريًا

### م15: توزيع تصنيف التذاكر

```
= تعداد category لكل قيمة
```
- يكشف عن أكثر نقاط الاحتكاك شيوعًا

---

## 7. لوحة المقاييس الأسبوعية (Weekly Dashboard)

يُنشر أسبوعيًا في `reports/whatsapp/WHATSAPP_WEEKLY_REPORT.md`:

| المقياس | الرمز | الهدف | الحالة |
|---|---|---|---|
| تحويل ما بعد الرد | م1 | ≥ 60% | تُحسب |
| معدل الانسحاب | م3 | < 5% | تُراقب |
| معدل الموافقة على البطاقات | م4 | ≥ 80% | تُحسب |
| معدل التسليم البشري | م10 | < 30% | تُحسب |
| زمن الاستجابة (high) | م12 | < 4 ساعات | تُراقب |
| انتهاكات SLA | م14 | 0 لـcritical | تُراقب |

---

## 8. قيود مهمة

1. **لا ROI مضمون في التقارير:** الأرقام تُعرض مع `evidence_level` صريح.
2. **لا PII في التقارير:** الأرقام مُجمَّعة، لا أسماء أو جوالات.
3. **التقارير للمؤسس فقط:** لا تُشارَك مع العملاء إلا عبر البوابة الآمنة بعد موافقة.

---

## مراجع

- `data/whatsapp/sessions.jsonl`
- `data/whatsapp/action_cards.jsonl`
- `data/whatsapp/client_assessments.jsonl`
- `data/whatsapp/handoffs.jsonl`
- `data/whatsapp/support_tickets.jsonl`
- `reports/whatsapp/` (التقارير الدورية)
- `AGENTS.md §12` (الإيقاع الأسبوعي/اليومي)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
