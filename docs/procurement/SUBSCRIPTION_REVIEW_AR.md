# مراجعة الاشتراكات الشهرية — Dealix Subscription Review

> **كل شهر، مراجعة كل اشتراك.** هذا الـ doc يحدد الإيقاع والخطوات.

**الحالة:** مسودة — Phase 3 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. الإيقاع (Cadence)

- **Weekly:** تكلفة LLM (SLO).
- **Monthly:** كل subscription في `data/procurement/subscriptions.jsonl`.
- **Quarterly:** vendor risk review.
- **Yearly:** contract renewal.

## 2. خطوات المراجعة الشهرية

1. **افتح** `data/procurement/subscriptions.jsonl`.
2. **لكل entry** تحقق من:
   - **Usage:** هل استُخدم في آخر 30 يوم؟
   - **Cost:** هل السعر تغيّر؟
   - **Tier:** هل في tier أرخص متاح؟
   - **Renewal:** متى ينتهي العقد؟
3. **ألغِ** أي subscription غير مستخدم.
4. **ترحيل** أي subscription إلى tier أرخص.
5. **سجّل** في `reports/procurement/SUBSCRIPTION_REVIEW.md`.

## 3. Subscription Schema

```json
{
  "subscription_id": "sub_2026_postHog",
  "vendor_id": "v_posthog",
  "tier": "free",
  "monthly_cost_sar": 0,
  "billing_cycle": "monthly",
  "started_at": "2026-01-01",
  "next_renewal": "monthly",
  "auto_renew": false,
  "cancellation_url": "https://posthog.com/billing",
  "status": "active|paused|cancelled",
  "owner": "founder",
  "last_used": "2026-06-02"
}
```

## 4. قاعدة الإلغاء التلقائي (Auto-Cancel Rules)

ألغِ تلقائياً (بعد موافقة المؤسس) لو:
- لم يُستخدم 60 يوم.
- tier أرخص متاح مع نفس الـ features.
- vendor فقد certification (PDPL/SOC2).

## 5. قائمة المراجعة (Checklist)

- [ ] قراءة `subscriptions.jsonl`
- [ ] فحص usage لكل entry
- [ ] فحص pricing changes
- [ ] تحديد candidates للإلغاء
- [ ] PR + founder approval
- [ ] تنفيذ الإلغاء
- [ ] تحديث السجل

## 6. المراجع

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/procurement/API_COST_CONTROL_AR.md`
- `docs/procurement/TOOL_SELECTION_POLICY_AR.md`
- `data/procurement/subscriptions.jsonl`
- `data/procurement/vendors.jsonl`
- `schemas/subscription.schema.json` (TBD)
