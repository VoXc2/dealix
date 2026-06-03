# تسليم الدفع (Payment Handoff)

> **نظام Dealix — Saudi B2B Revenue Operating System**
> الإصدار: 1.0 | التاريخ: 2026-06-03 | المالك: Agent #2
> السكيمة المرجعية: `schemas/payment_handoff.schema.json`

---

## 1. ما هو تسليم الدفع؟

تسليم الدفع (`payment_handoff`) هو الكيان الذي **يُحضّر — لا يُرسل** — خطوة الدفع لموافقة المؤسس. في Dealix، لا يوجد إرسال تلقائي لأي طلب دفع. كل شيء يمر بـ:

```
تحضير ذكي → موافقة المؤسس → تسليم بشري يدوي
```

---

## 2. الثوابت الأمنية (لا تتغير)

| الثابت | القيمة | المعنى |
|---|---|---|
| `approval_required` | `true` (const) | الموافقة إلزامية دائمًا |
| `send_enabled` | `false` (v1) | لا إرسال تلقائي في النسخة الأولى |
| `dry_run` | `true` افتراضيًا | وضع التجربة حتى موافقة صريحة |
| `risk_level` | `high` افتراضيًا | كل دفع عالي الخطورة |

---

## 3. الحقول الأساسية (payment_handoff.schema.json)

| الحقل | الإلزامية | الوصف |
|---|---|---|
| `id` | إلزامي | `PAY-XXXX` |
| `proposal_id` | إلزامي | **يجب** أن يُشير لعرض `founder_approved=true` |
| `company` | إلزامي | اسم الشركة العميلة |
| `amount_sar` | إلزامي | المبلغ بالريال (لا يتجاوز ما في العرض المعتمد) |
| `payment_provider` | إلزامي | من القائمة المعتمدة (§5) |
| `payment_link_ref` | اختياري | `portal://...` — مرجع فقط، لا URL مباشر في البيانات |
| `approved` | إلزامي | `false` حتى موافقة فعلية |
| `approved_by` | عند الموافقة | هوية المُوافق (المؤسس) |
| `approved_at` | عند الموافقة | توقيت الموافقة |
| `status` | إلزامي | انظر §4 |
| `notes` | اختياري | ملاحظات — لا أسرار ولا أرقام حسابات كاملة |

---

## 4. دورة حياة تسليم الدفع

| الحالة | المعنى | الإجراء التالي |
|---|---|---|
| `draft` | قيد الإعداد الذكي | مراجعة داخلية |
| `pending_approval` | في طابور موافقة المؤسس | المؤسس يراجع |
| `approved` | المؤسس وافق | تسليم بشري يدوي |
| `sent_manually` | أُرسل يدويًا للعميل | انتظار السداد |
| `paid` | تم السداد والتأكيد | انتقال لمرحلة التسليم |
| `rejected` | رفضه المؤسس | مراجعة وتعديل |
| `cancelled` | إلغاء بطلب العميل/المؤسس | توثيق السبب |

---

## 5. مزودو الدفع المعتمدون

| payment_provider | الاستخدام المناسب |
|---|---|
| `bank_transfer` | التحويل البنكي — الأكثر شيوعًا في B2B السعودي |
| `moyasar` | بوابة دفع إلكتروني سعودية |
| `hyperpay` | بطاقات بنكية + متعدد الوسائل |
| `stc_pay` | محفظة STC الرقمية |
| `tap` | بوابة دفع خليجية |
| `other` | بتوثيق مسبق + موافقة المؤسس |

---

## 6. قاعدة `payment_link_ref`

- القيمة دائمًا `portal://payment/...` — مرجع منطقي.
- **لا يُخزَّن** أي URL مباشر قابل للدفع في JSONL أو تقارير أو سجلات.
- الرابط الفعلي يُنشأ ويُرسَل يدويًا في البوابة فقط.
- الرابط منتهي الصلاحية (لا روابط أبدية).

---

## 7. العلاقة بالعرض والبيانات

```
PROP-XXXX (founder_approved=true)
    ↓
RAC-XXXX (type=prepare_payment_handoff) ← كارت إجراء يُوجد PAY
    ↓
PAY-XXXX (proposal_id=PROP-XXXX, status=pending_approval)
    ↓ موافقة
/client/payment في البوابة
```

**قاعدة:** لا يُنشأ `payment_handoff` لعرض لم يعتمده المؤسس. `proposal_id` الذي `founder_approved=false` = **يُرفض**.

---

## 8. مثال واقعي: Digital Rise Agency — PAY-1001

| الحقل | القيمة |
|---|---|
| `id` | PAY-1001 |
| `proposal_id` | PROP-1002 (founder_approved=true، وافق 2026-06-02) |
| `company` | Digital Rise Agency |
| `amount_sar` | 1,250 SAR (50% مقدم من عرض 2,500 SAR) |
| `payment_provider` | bank_transfer |
| `payment_link_ref` | null (لم يُنشأ بعد) |
| `approved` | false — ينتظر موافقة المؤسس |
| `status` | pending_approval |
| `risk_level` | high |
| `dry_run` | true |
| `send_enabled` | false |
| `notes` | دفعة مقدمة 50%. لا يُرسل إلا بعد موافقة + تسليم بشري. |

---

## 9. شروط الدفع الشائعة في Dealix

| النوع | الشروط المعتادة |
|---|---|
| `revenue_leakage_diagnostic` (P1) | 50% مقدم، 50% عند تسليم Proof Pack |
| `ai_revenue_ops_starter` (P2-Small) | شهري مقدم، التزام 3 أشهر |
| `full_revenue_os` (P2-Medium) | شهري مقدم، التزام 3 أشهر |
| `custom_company_os` (Enterprise) | جدول دفعات مخصص، التزام 6 أشهر |

---

## 10. ما هو ممنوع قطعًا

- إنشاء payment_handoff لعرض غير معتمد.
- تخزين أرقام IBAN أو بطاقات بنكية في أي ملف.
- تغيير `send_enabled` إلى `true` في v1.
- إرسال طلب دفع عبر واتساب أو بريد إلكتروني مباشرة.
- الدفع من طرف واحد (يجب الموافقة + التسليم البشري).

---

## الروابط المرجعية

- سكيمة تسليم الدفع: `schemas/payment_handoff.schema.json`
- الدفع في البوابة: [`../client_portal/CLIENT_PAYMENT_HANDOFF_AR.md`](../client_portal/CLIENT_PAYMENT_HANDOFF_AR.md)
- سياسة تسليم العقود: [`CONTRACT_HANDOFF_POLICY_AR.md`](CONTRACT_HANDOFF_POLICY_AR.md)
- مصنع العروض: [`PROPOSAL_FACTORY_AR.md`](PROPOSAL_FACTORY_AR.md)
- بطاقات الإجراء: [`REVENUE_ACTION_CARDS_AR.md`](REVENUE_ACTION_CARDS_AR.md)
- الحوكمة الموحّدة: [`AGENTS.md`](../../AGENTS.md)

---

*ينبغي قراءة هذا المستند مع [AGENTS.md](../../AGENTS.md) — عقد الحوكمة الموحّد لكل وكيل/سكربت/مستند في Dealix.*
