# معايير «نحن جاهزون» (10 نقاط)

Dealix جاهزة للتشغيل الاحترافي عندما:

1. **3 service packs كاملة** (مجلدات `docs/services/` + readiness).
2. **3 demo outputs** (انظر `sample_output.md` + أصول حقيقية عند توفرها).
3. **Report template** لكل خدمة رئيسية.
4. **Proof pack template** موحّد + ممتلئ.
5. **Governance checklist** (`docs/governance/` + فحوصات الكود).
6. **Pricing واضح** — [`PRICING.md`](PRICING.md).
7. **Sales script** — [`../sales/SALES_SCRIPT_AR.md`](../sales/SALES_SCRIPT_AR.md).
8. **Delivery timeline** — [`../delivery/DELIVERY_LIFECYCLE.md`](../delivery/DELIVERY_LIFECYCLE.md).
9. **QA score** — [`../quality/QA_DELIVERY_RUBRIC_AR.md`](../quality/QA_DELIVERY_RUBRIC_AR.md).
10. **أول module يساعد التسليم** — جاهزية الخدمة في YAML + مسارات Sprint.

التحقق: `py -3 scripts/verify_full_mvp_ready.py`
