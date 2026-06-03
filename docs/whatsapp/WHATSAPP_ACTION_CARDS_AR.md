# بطاقات الإجراء في واتساب (Action Cards)
## الأنواع التسعة، الحقول الإلزامية، والأمثلة

> **الغرض:** يوثّق هذا المستند بطاقات الإجراء (`Action Cards`) كوحدة التفاعل الهيكلية الأساسية في واتساب — بديل عن الدردشة الطويلة غير المنظّمة. كل بطاقة واضحة، قصيرة، قابلة للمراجعة، وخاضعة لإطار الموافقة.  
> مرجع السكيمة: `schemas/whatsapp_action_card.schema.json`.  
> بيانات أمثلة: `data/whatsapp/action_cards.jsonl`.

---

## 1. لماذا بطاقات الإجراء؟

بدلًا من: "ما هو الوضع؟ ماذا تقترحون؟ ما السعر؟" — محادثة مبعثرة وغير قابلة للتتبع.

باستخدام البطاقات:
- **عنوان واضح** (≤ 80 حرف)
- **ملخص موجز** (≤ 600 حرف)
- **سبب مُوثَّق** (`reason`) + مستوى دليل (`evidence_level`)
- **خيارات مرقّمة** (بما فيها "ما أعرف — اقترح علي" دائمًا)
- **انتهاء صلاحية** (`expires_at`) — لا بطاقة مفتوحة إلى الأبد
- **حالة قابلة للتتبع** (`status`)

---

## 2. الأنواع التسعة (`type`)

| النوع | الوصف | مستوى الخطورة الشائع | يحتاج موافقة؟ |
|---|---|---|---|
| `recommendation` | توصية بمنتج أو خطوة تالية | `low` – `medium` | لا (L2 Advise) |
| `approval` | طلب موافقة على إجراء معلّق | `medium` – `high` | نعم (L4) |
| `permission` | طلب صلاحية قراءة فقط عبر البوابة | `medium` | نعم (L4) |
| `proposal` | إخطار بعرض مبدئي في البوابة | `medium` | نعم (L4) |
| `proof_pack` | إخطار بـProof Pack جاهز في البوابة | `medium` | نعم (L4) |
| `payment_handoff` | إعداد خطوة الدفع للمراجعة البشرية | `high` | نعم (L5) |
| `onboarding` | checklist البداية بعد إتمام الصفقة | `low` | نعم |
| `support_escalation` | تحويل لبشري + إنشاء تذكرة دعم | `medium` | — |
| `renewal` | اقتراح تجديد أو ترقية | `low` – `medium` | نعم (L4) |

---

## 3. الحقول الإلزامية (required fields)

```json
{
  "id":                "WAC-xxxx",          // نمط: WAC-[A-Za-z0-9_-]+
  "type":              "recommendation",    // أحد الأنواع التسعة
  "title":             "...",               // ≤ 80 حرف
  "summary":           "...",               // ≤ 600 حرف
  "reason":            "...",               // لماذا هذا الإجراء؟
  "risk_level":        "low|medium|high|critical",
  "evidence_level":    "none|assumption|benchmark|client_reported|client_data|measured|verified",
  "options":           [...],               // min 1 خيار، يشمل is_dont_know=true
  "approval_required": true/false,
  "next_action":       "...",              // الإجراء التالي في النظام
  "expires_at":        "ISO-8601",         // انتهاء صلاحية إلزامي
  "owner":             "founder",
  "status":            "proposed",         // القيمة الأولى دائمًا
  "dry_run":           true,               // افتراضي
  "send_enabled":      false               // افتراضي
}
```

**تحذير:** أي بطاقة بدون `evidence_level` = غير صالحة (تفشل في الاختبارات).  
**تحذير:** أي بطاقة بدون خيار `is_dont_know: true` = تنتهك الثوابت.

---

## 4. دورة حياة البطاقة (status)

```
proposed
   │
   ├─ موافقة المؤسس    → approved
   │                      │
   │                      └─ إرسال يدوي   → sent_manually
   ├─ رفض              → rejected
   ├─ انتهاء الصلاحية  → expired
   └─ بطاقة جديدة تحلّها → superseded
```

**ملاحظة:** لا يوجد `sent_automatically` — الإرسال دائمًا يدوي بعد الموافقة في v1.

---

## 5. الخيارات وشرط "ما أعرف — اقترح علي"

كل بطاقة يجب أن تحتوي على خيار واحد على الأقل بـ`is_dont_know: true`:

```json
{
  "label": "ما أعرف — اقترح علي",
  "value": "dont_know_suggest",
  "is_dont_know": true
}
```

هذا الخيار يُوجِّه العميل إلى تدفق `dont_know_suggest` الذي يقترح الخطوة الأنسب.

---

## 6. أمثلة من data/whatsapp/action_cards.jsonl

### بطاقة توصية (WAC-0001) — خطورة منخفضة

```json
{
  "id": "WAC-0001",
  "type": "recommendation",
  "title": "الخطوة المقترحة: فحص الجاهزية",
  "summary": "نقترح إكمال فحص الجاهزية ثم تشخيص تسرب الإيراد.",
  "reason": "إشارات على ضعف المتابعة بعد أول رد.",
  "risk_level": "low",
  "evidence_level": "client_reported",
  "options": [
    { "label": "أكمل الفحص", "value": "continue_readiness", "is_dont_know": false },
    { "label": "ما أعرف — اقترح علي", "value": "dont_know_suggest", "is_dont_know": true }
  ],
  "approval_required": false,
  "status": "proposed",
  "dry_run": true,
  "send_enabled": false
}
```

### بطاقة صلاحية (WAC-0002) — خطورة متوسطة، تحتاج موافقة

```json
{
  "id": "WAC-0002",
  "type": "permission",
  "title": "صلاحية قراءة فقط لمصدر البيانات",
  "summary": "نحتاج قراءة فقط لجدول العملاء عبر البوابة الآمنة، صلاحية محدودة وتنتهي تلقائيًا.",
  "reason": "لتشخيص نقاط التسرب على بيانات فعلية.",
  "risk_level": "medium",
  "evidence_level": "assumption",
  "approval_required": true,
  "approved": false
}
```

### بطاقة تسليم دفع (WAC-0003) — خطورة عالية، L5

```json
{
  "id": "WAC-0003",
  "type": "payment_handoff",
  "title": "تجهيز خطوة الدفع (للمراجعة)",
  "summary": "لا يُرسل رابط دفع تلقائيًا. الدفع يحتاج موافقة المؤسس وتسليم بشري.",
  "risk_level": "high",
  "approval_required": true,
  "send_enabled": false
}
```

---

## 7. قواعد إضافية للبطاقات ذات الخطورة العالية

| النوع | القاعدة |
|---|---|
| `payment_handoff` | `risk_level: high/critical` + `approval_required: true` + `send_enabled: false` دائمًا في v1 |
| `proposal` | السعر النهائي في البوابة فقط، لا في `summary` |
| `renewal` | `evidence_level` يجب أن يكون من `{client_data, measured, verified}` |
| أي بطاقة `legal_or_contract` | تُنشئ تسليم بشري تلقائيًا |

---

## مراجع

- `schemas/whatsapp_action_card.schema.json`
- `data/whatsapp/action_cards.jsonl` (أمثلة: WAC-0001 إلى WAC-0003)
- `data/whatsapp/flows.yaml`
- `AGENTS.md §2` (الخطوط الحمراء) و`§4` (مستويات الصلاحية)
- `docs/whatsapp/WHATSAPP_ACTION_CARD_UX_AR.md` (تجربة الاستخدام)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
