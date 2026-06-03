# RFC — إرسال تلقائي منخفض المخاطرة (استكشاعي)

**الحالة:** مسودة — غير مفعّل في الإنتاج افتراضياً  
**المالك:** المؤسس + امتثال  
**الكود:** `api/routers/drafts.py` · `DEALIX_ENABLE_AUTO_SEND_LOW_RISK`

## القرار المطلوب قبل التفعيل

| القناة | افتراضي Dealix | مسموح تلقائياً بعد الموافقة؟ |
|--------|----------------|------------------------------|
| واتساب بارد | ممنوع دائماً | لا |
| LinkedIn DM جماعي | ممنوع (ToS) | لا — يدوي فقط |
| Gmail business | مسودات فقط | **استكشاع:** فقط إذا `warm_outreach_eligible=true` على الحساب |
| تقويم خارجي | موافقة صريحة | لا |

## شروط PDPL (إلزامية)

1. `allowed_use` و`consent_status` موثّقان في `AccountRecord.extra`
2. لا قوائم مشتراة بدون عقد استخدام
3. سقف معدل: `DAILY_EMAIL_LIMIT` / `EMAIL_BATCH_SIZE` (انظر `compliance.py`)
4. سجل تدقيق في `EmailSendLog` لكل محاولة

## تفعيل تقني (لا يُستخدم في prod بدون قرار)

```bash
# محلي/تجريبي فقط
export DEALIX_ENABLE_AUTO_SEND_LOW_RISK=1
```

```json
POST /api/v1/automation/revenue-machine/run
{
  "approval_mode": "auto_send_low_risk",
  "gmail_drafts": 5
}
```

الفرع يرسل فقط عندما:

- المتغير البيئي مفعّل
- `approval_mode=auto_send_low_risk`
- `check_outreach.allowed` وبدون `requires_human_review`
- `risk_level=low` على الحساب
- `extra.warm_outreach_eligible=true` (يدوي من CRM/المؤسس)
- Gmail OAuth مُعدّ

## LinkedIn

لا يُضاف auto-send لـ LinkedIn في هذا RFC — التزاماً بتعليق الراوتر والـ ToS.

## الخطوة التالية

- [ ] مراجعة قانونية PDPL للبريد business-only
- [ ] تحديد معيار `warm_outreach_eligible` في CRM
- [ ] تجربة على ≤5 حسابات owned قبل أي توسع
