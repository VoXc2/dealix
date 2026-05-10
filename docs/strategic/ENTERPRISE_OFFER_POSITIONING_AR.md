# عرض Dealix للشركات — الطبقات A / B / C والسلسلة الذهبية

**الغرض:** تثبيت لغة بيع وتشغيل موحّدة لعملاء B2B enterprise دون وعد «كل شيء لكل أحد». كل طبقة ترتبط بمسارات في الريبو وسجل عدم المبالغة.

## المعادلة المرجعية

من [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md):

```text
Dealix = ذكاء الإيرادات + تنفيذ تشغيلي + محرك إثبات + نجاح عميل + طبقة ثقة + حلقة تعلّم
```

**السلسلة الذهبية (عقد المنتج):**

```text
إشارة → Lead → Decision Passport → إجراء معتمد → تسليم → Proof → توسعة → تعلّم
```

واجهات API ثابتة للمرجعية التجارية والتقنية:

- `GET /api/v1/decision-passport/golden-chain`
- `GET /api/v1/decision-passport/evidence-levels`
- `GET /api/v1/revenue-os/catalog`
- `POST /api/v1/revenue-os/signals/normalize`
- `POST /api/v1/revenue-os/anti-waste/check`
- `POST /api/v1/leads` (يُرجع `decision_passport` و `customer_readiness`)

## الطبقات الثلاث (A / B / C)

| الطبقة | الاسم | ما يشتريه العميل | ربط بالريبو |
|--------|--------|-------------------|-------------|
| **A** | Revenue & Pipeline | من إشارة إلى قرار إلى إجراء معتمد | `revenue_os/`, الوكلاء، Lead graph، Decision Passport |
| **B** | Delivery & Proof | تسليم خدمة، أدلة، توسعة مشروطة بالـ Proof | `delivery_os/`, `proof_ledger/`, `ProofEventCanonical`, بوابات التوسعة |
| **C** | Trust & Compliance | حوكمة، موافقات، تدقيق، PDPL-by-design | Trust Plane، `api/middleware/http_stack.py` (تدقيق مسارات بيانات شخصية)، سياسات القنوات |

**حزمة الخدمة الاستشارية/التشغيلية:** تشخيص → تصميم مسار على السلسلة الذهبية → Pilot مقيد → إثبات → توسعة (راجع [ENTERPRISE_PILOT_TEMPLATE_AR.md](ENTERPRISE_PILOT_TEMPLATE_AR.md)).

## الالتزام بعدم المبالغة

- أي ادّعاء عام أو شرائح مبيعات يجب أن يطابق حالة مسجّلة في [dealix/registers/no_overclaim.yaml](../../dealix/registers/no_overclaim.yaml).
- الحالات `Partial` / `Pilot` تعني قيوداً صريحة على ما يُقال للعميل؛ لا تُرفَع إلى «إنتاج كامل» في العقود دون تحديث السجل والأدلة.

## ما لا نعد به (لحماية العلامة)

- إرسال واتساب بارد تلقائياً، أو سكرابينغ، أو أتمتة LinkedIn — محظورة في المنتج والسرد التجاري.
- «ذكاء يُنفّذ الخارجي بدون موافقة» — يتعارض مع دستور التشغيل (مسودات وموافقات أولاً).

## مراجع

- [DEALIX_MASTER_OPERATING_MODEL_AR.md](DEALIX_MASTER_OPERATING_MODEL_AR.md)
- [DEALIX_ROLE_SERVICE_LADDER_AR.md](DEALIX_ROLE_SERVICE_LADDER_AR.md) — أدوار المشتري ↔ `service_id`
- [DEALIX_MARKET_DIFFERENTIATION_AR.md](DEALIX_MARKET_DIFFERENTIATION_AR.md) — تمييز مقابل أنماط السوق
- [WAVE13_LANDING_PORTAL_ALIGNMENT_AR.md](WAVE13_LANDING_PORTAL_ALIGNMENT_AR.md) — محاذاة البوابة والـ landing
- [ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md](ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md)
- [ENTERPRISE_P0_GAP_BACKLOG_AR.md](ENTERPRISE_P0_GAP_BACKLOG_AR.md)
