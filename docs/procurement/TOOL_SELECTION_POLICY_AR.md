# سياسة اختيار الأداة — Dealix Tool Selection Policy

> **قبل إضافة أداة جديدة، اسأل: هل نغطيها فعلاً؟** هذا الـ doc يحدد
> قواعد الاختيار.

**الحالة:** مسودة — Phase 3 من Agent #17
**التاريخ:** 2026-06-03

---

## 1. الـ 7 أسئلة قبل الإضافة

1. **هل هناك أداة حالية تغطي هذا الاستخدام؟**
   - نعم ⇒ لا تُضف. استخدمها أو وسّعها.
2. **هل هذا الاستخدام critical أم nice-to-have؟**
   - critical ⇒ founder approval.
3. **ما data risk؟** (low/medium/high/critical)
   - high+ ⇒ DPO + legal review.
4. **هل التكلفة ضمن budget؟**
   - لا ⇒ ارفض أو defer.
5. **هل هي monthly cancellable؟**
   - يفضّل. تجنّب annual contract في البداية.
6. **هل تدعم Saudi data residency؟** (للـ high/critical)
   - لا ⇒ ابحث عن بديل.
7. **هل هي vendor SaaS أم self-hosted؟**
   - self-hosted أفضل لـ data risk high+.

## 2. مستويات الاختيار

| المستوى | من يقرر | زمن |
| --- | --- | --- |
| **Low** | أي agent (داخل قواعد) | فوري |
| **Medium** | Operator (Agent #2) | < 4h |
| **High** | المؤسس | < 24h |
| **Critical** | المؤسس + DPO/Legal | < 5d |

## 3. Build vs Buy

| الحالة | القرار |
| --- | --- |
| Commodity SaaS، low differentiation | **Buy** |
| Core moat، no good off-shelf | **Build** |
| Data-sensitive | **Build** (أو self-host) |
| Fast iteration needed | **Buy** |
| Long-term cost > $50K/year | **Build** (أو negotiate) |

## 4. قائمة الأدوات المسموحة / الممنوعة (Live List)

### ممنوع حالياً
- أي tool يخزن PII خارج السعودية بدون DPO approval.
- أي tool يحتاج credit card على email شخصي (يستخدم founder's
  business card).
- أي tool free-tier فقط بدون exit plan.

### مفضّل
- tools with free tier للتجريب
- tools with monthly billing
- tools with public API + webhooks
- tools with PDPL/SOC2 documented

## 5. عملية الإضافة (Adding a Tool)

1. **Pre-check:** 7 أسئلة أعلاه.
2. **PR:** يفتح PR على `data/procurement/vendors.jsonl` بـ entry جديد.
3. **Review:** المؤسس يوافق.
4. **Provision:** إضافة API key في 1Password + Railway.
5. **Doc:** تحديث `.env.example` + هذا الـ doc.
6. **Monitor:** أول شهر = usage review.

## 6. عملية الإزالة (Removing a Tool)

1. **Check usage:** هل أحد يستخدمها؟ آخر 90 يوم.
2. **Migration plan:** لو نعم ⇒ migrate or grandfather.
3. **Cancel:** ألغِ الاشتراك.
4. **Cleanup:** احذف من `.env.example` + `vendors.jsonl` بعد 30 يوم.
5. **Document:** CHANGELOG.md.

## 7. المراجع

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/procurement/BUILD_VS_BUY_POLICY_AR.md`
- `docs/procurement/VENDOR_RISK_POLICY_AR.md`
- `docs/SUPPLIER_MASTER_LIST.md`
- `data/procurement/vendors.jsonl`
- `docs/infra/SECRETS_MANAGEMENT_AR.md`
