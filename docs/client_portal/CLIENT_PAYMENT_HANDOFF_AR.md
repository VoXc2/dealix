# خطوة الدفع داخل البوابة الآمنة

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/payment_handoff.schema.json`
> المسار: `/client/payment`

---

## 1. الثوابت التي لا تتغير

```
approval_required: true    ← دائمًا
send_enabled:      false   ← في v1 دائمًا (لا إرسال تلقائي)
dry_run:           true    ← افتراضي حتى موافقة المؤسس الصريحة
risk_level:        high    ← افتراضي لكل تسليم دفع
```

**لا يُرسَل أي رابط دفع أو طلب دفع بدون:**
1. موافقة المؤسس الصريحة (`approved=true`, `approved_by`, `approved_at`)
2. تسليم بشري (Human Handoff) — مؤسس أو ممثل معتمد يُنفّذ الإرسال يدويًا

---

## 2. دورة تسليم الدفع

```
[1] الذكاء يُحضّر payment_handoff (status: draft)
    → proposal_id يجب أن يكون founder_approved=true
    → send_enabled=false, dry_run=true
            ↓
[2] الكارت يُرسَل لطابور موافقة المؤسس
    status: pending_approval
            ↓ رفض → rejected
    موافقة:
    approved=true, approved_by="founder", approved_at=<timestamp>
    status: approved
            ↓
[3] المؤسس (أو ممثله) يُرسل رابط الدفع يدويًا للعميل
    عبر /client/payment في البوابة
    payment_link_ref = portal://... (مرجع فقط)
    status: sent_manually
            ↓
[4] العميل يُتمّ الدفع خارج البوابة
    status: paid
```

---

## 3. حقول payment_handoff.schema.json

| الحقل | الإلزامية | الوصف |
|---|---|---|
| `id` | إلزامي | `PAY-XXXX` |
| `proposal_id` | إلزامي | يجب أن يكون `founder_approved=true` |
| `company` | إلزامي | الشركة العميلة |
| `amount_sar` | إلزامي | المبلغ بالريال السعودي |
| `payment_provider` | إلزامي | `bank_transfer` / `moyasar` / `hyperpay` / `stc_pay` / `tap` / `other` |
| `payment_link_ref` | اختياري | `portal://...` — **مرجع فقط، لا URL مباشر** |
| `approval_required` | إلزامي | `true` دائمًا (const) |
| `approved` | إلزامي | `false` حتى موافقة فعلية |
| `approved_by` | عند الموافقة | من وافق (المؤسس) |
| `approved_at` | عند الموافقة | وقت الموافقة |
| `status` | إلزامي | `draft → pending_approval → approved → sent_manually → paid / rejected / cancelled` |
| `risk_level` | إلزامي | `high` افتراضيًا |
| `dry_run` | إلزامي | `true` افتراضيًا |
| `send_enabled` | إلزامي | `false` دائمًا في v1 |
| `notes` | اختياري | ملاحظات — **لا أسرار، لا أرقام حسابات كاملة** |

---

## 4. ما يراه العميل في `/client/payment`

- ملخص العرض المرتبط (`proposal_id`)
- المبلغ المطلوب (`amount_sar`)
- الجدول الزمني للدفع (50% مقدم، 50% عند التسليم — حسب شروط العرض)
- وسيلة الدفع المقترحة
- تعليمات التحويل (تُقدَّم يدويًا من المؤسس)
- **لا زر "ادفع الآن" آلي في v1**

---

## 5. مثال واقعي: Digital Rise Agency — PAY-1001

| الحقل | القيمة |
|---|---|
| `id` | PAY-1001 |
| `proposal_id` | PROP-1002 (founder_approved=true) |
| `company` | Digital Rise Agency |
| `amount_sar` | 1,250 SAR (50% مقدم من 2,500 SAR) |
| `payment_provider` | bank_transfer |
| `payment_link_ref` | null (لم يُنشأ بعد) |
| `approved` | false — ينتظر موافقة المؤسس |
| `status` | pending_approval |
| `risk_level` | high |
| `dry_run` | true |
| `send_enabled` | false |
| `notes` | دفعة مقدمة 50%. لا يُرسل رابط إلا بعد موافقة + تسليم بشري |

---

## 6. مزودو الدفع المدعومون

| المزود | الاستخدام الموصى به |
|---|---|
| `bank_transfer` | الأكثر شيوعًا في B2B السعودي |
| `moyasar` | بوابة دفع إلكتروني سعودية |
| `hyperpay` | بوابة دفع متعددة الوسائل |
| `stc_pay` | محفظة رقمية سعودية |
| `tap` | بوابة دفع خليجية |
| `other` | بتوثيق مسبق وموافقة |

---

## 7. ما هو محظور قطعًا

- إرسال رابط دفع تلقائيًا بدون موافقة المؤسس.
- تخزين أرقام بطاقات بنكية أو حسابات IBAN كاملة في JSONL أو سجلات.
- إنشاء `payment_handoff` بدون ربطه بـ `proposal_id` معتمد من المؤسس.
- تغيير `send_enabled` إلى `true` في v1.

---

## الروابط المرجعية

- سكيمة تسليم الدفع: `schemas/payment_handoff.schema.json`
- سياسة تسليم الدفع (Revenue Execution): [`../revenue_execution/PAYMENT_HANDOFF_AR.md`](../revenue_execution/PAYMENT_HANDOFF_AR.md)
- سياسة تسليم العقود: [`../revenue_execution/CONTRACT_HANDOFF_POLICY_AR.md`](../revenue_execution/CONTRACT_HANDOFF_POLICY_AR.md)
- سياسة البوابة: [`SECURE_CLIENT_PORTAL_AR.md`](SECURE_CLIENT_PORTAL_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
