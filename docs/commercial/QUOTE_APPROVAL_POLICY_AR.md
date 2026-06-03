# سياسة اعتماد التسعيرة (QUOTE APPROVAL POLICY)

> **المصدر:** [`data/commercial/pricing_rules.yaml`](../../data/commercial/pricing_rules.yaml) (PR-001) · الحوكمة [`agent_permissions.md`](../../company_os/governance/agent_permissions.md) · طابور [`approval_queue.json`](../../company_os/governance/approval_queue.json).
> العملة `ر.س` · كل الأسعار **نطاق** · **السعر النهائي بموافقة المؤسّس** · الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false`.

## المبدأ
**الـ AI يجهّز نطاقاً → المؤسّس يعتمد السعر النهائي → إنسان يرسل.**
لا يُعرض **رقم نهائي** يقتبسه أحد بحرية (قاعدة **PR-001**)، ولا إرسال خارجي تلقائي.
نحن **نساعد، نجهّز، نرتّب، نقيس، نكشف فرص التحسين، نقترح، ونجهّز مسودّات بموافقة** — بلا وعد بنتائج مضمونة.

## مسار الاعتماد (workflow)
| الخطوة | المنفّذ | المستوى (حوكمة) | الناتج |
|--------|---------|------------------|--------|
| 1. تجهيز نطاق + مسودّة عرض | الـ AI | Draft / Advise | نطاق سعري + مخرجات + مدة + بند خارج النطاق |
| 2. إدخال في طابور الموافقة | الـ AI | Draft | عنصر في `approval_queue.json` بحالة `pending` |
| 3. اعتماد السعر النهائي | **المؤسّس** | Act with Approval | سعر نهائي معتمد ضمن النطاق |
| 4. الإرسال للعميل | **إنسان** | Human only | عرض مُرسَل يدوياً |
| 5. تسجيل القرار | الحوكمة | Observe | قيد في `ai_action_ledger.jsonl` |

> يطابق مسار الحوكمة: `AI drafts → Human reviews → Approve/Reject → If approved: execute → Log`.

## ما يفعله الـ AI وما لا يفعله
- **يفعل:** يجهّز نطاقاً سعرياً، يربطه بالمخرجات والمدة (PR-007)، يضمّن «خارج النطاق» (PR-006)، يقترح سبب أي خصم (PR-002)، ويضع العنصر في الطابور.
- **لا يفعل:** لا يقرّر سعراً نهائياً، لا يمنح خصماً (`max_discount_pct_without_founder = 0`)، لا يرسل خارجياً، لا ينشئ فاتورة، لا يعالج دفعة.

> خطوط الحوكمة الحمراء ذات الصلة: «AI never makes pricing decisions» و«AI never sends external messages without approval».

## بوابة المؤسّس وحالات التصعيد
وفق escalation matrix في الحوكمة:

| نوع القرار | المعتمِد |
|------------|----------|
| تسعير أقل من 5,000 ر.س | المؤسّس |
| تسعير أعلى من 5,000 ر.س | المؤسّس + تهدئة 24 ساعة |
| العروض/التسعيرات | المؤسّس |
| الخصومات (أي نسبة) | المؤسّس (سبب موثّق — PR-002) |

- **`DLX-L1`** (1,500–5,000 ر.س): اعتماد المؤسّس.
- **`DLX-L2`..`DLX-L6`** (أعلى من 5,000 ر.س): اعتماد المؤسّس + تهدئة 24 ساعة.
- **`DLX-L5`** (3,000–15,000 ر.س/شهر): اعتماد المؤسّس لقيمة الاشتراك وأي تعديل.

## حالات الطابور (approval_status)
`pending` (افتراضي) · `approved` · `rejected` · `needs_revision`.
- **`pending`:** بانتظار المؤسّس — لا إرسال.
- **`approved`:** سعر نهائي معتمد ضمن النطاق — يجوز للإنسان الإرسال.
- **`rejected` / `needs_revision`:** يعاد للتجهيز أو يُلغى — لا إرسال.

## ربط بالضوابط
- ضوابط التسعير: [`PRICING_GUARDRAILS_AR.md`](./PRICING_GUARDRAILS_AR.md).
- الخصومات: [`DISCOUNT_POLICY_AR.md`](./DISCOUNT_POLICY_AR.md).
- شروط الدفع: [`PAYMENT_TERMS_AR.md`](./PAYMENT_TERMS_AR.md).
- صلاحيات الوكلاء: [`agent_permissions.md`](../../company_os/governance/agent_permissions.md).

---
*Dealix · سياسة اعتماد التسعيرة · AI يجهّز نطاقاً → المؤسّس يعتمد → إنسان يرسل · السعر النهائي بموافقة المؤسّس.*
