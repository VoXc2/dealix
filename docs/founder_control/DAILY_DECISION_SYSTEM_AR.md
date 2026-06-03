# نظام القرار اليومي — Daily Decision System (عربي أولًا)

> كيف يتحوّل ضجيج كل الأنظمة إلى **قرار حرج واحد** + قائمة موافقات قصيرة كل يوم.

---

## 1. خط التجميع اليومي
```
كل الطوابير (واتساب/عروض/دفع/تسليم/تجديد/مخاطر/خصوصية)
   → ترتيب حسب (المخاطرة × القيمة × الاستعجال)
   → أعلى 5 إجراءات موافقة
   → قرار حرج واحد
   → reports/founder/DAILY_SUPER_COMMAND.md
```

## 2. معادلة الأولوية (إرشادية)
`priority = risk_weight × value_weight × urgency` حيث:
- risk_weight: critical=4, high=3, medium=2, low=1.
- value_weight: حسب قيمة الصفقة/المنتج (الكتالوج).
- urgency: قرب انتهاء الصلاحية `expires_at` أو SLA.

## 3. ما الذي يُعرَض للقرار يوميًا
| الفئة | المصدر | الإجراء المتاح |
|---|---|---|
| بطاقات واتساب | `data/whatsapp/action_cards.jsonl` | approve/edit/reject |
| عروض بانتظار السعر | `data/proposals/*` (pending_founder_approval) | approve price/edit/reject |
| تسليمات دفع | `data/payments/*` (pending_approval) | approve/mark-sent/reject |
| تسليمات بشرية | `data/whatsapp/handoffs.jsonl` (open) | assign/resolve |
| تجديد/ترقية | `data/renewals/*` (draft) | approve/edit |

## 4. القرار الحرج الواحد
يُختار يوميًا أعلى عنصر أولوية ويُصاغ كسؤال نعم/لا أو خيار محدود، مع توصية و`evidence_level`. يُسجّل في `DECISION_LOG.md`.

## 5. قاعدة الصحة الذهنية للمؤسس
الهدف: ≤ 7 قرارات يوميًا. ما زاد يُجمّع في المراجعة الأسبوعية أو يُفوّض ضمن حدود مُعرّفة (مثل تسعير < 5,000 ريال باعتماد مباشر).

---
*المرجع: `docs/business_os/FOUNDER_COMMAND_SYSTEM_AR.md` · الحاكم: `AGENTS.md`.*
