# Venture Signal Model — جاهزية Venture

كل وحدة تحصل على **Venture Readiness Score** (مدخلات **0–100** بعد التطبيع).

## الصيغة (الأوزان المؤسسية)

```text
Venture Score =
  paid_clients_maturity     * 0.15
+ retainers_maturity       * 0.20
+ repeatability            * 0.20
+ product_module_usage     * 0.15
+ playbook_maturity        * 0.10
+ margin                   * 0.10
+ owner_readiness          * 0.10
```

*مثال تطبيع:* `paid_clients_maturity` من min(clients, 5)/5×100 إذا أردت ربطًا بعدد العملاء حتى عتبة 5.

## النطاقات

| Score | قرار |
|-------|------|
| **85+** | Venture candidate |
| **70–84** | Business unit |
| **55–69** | Service line |
| **<55** | ضمن خدمات نواة |

## شروط تشغيلية (تذكير)

5+ paid · 2+ retainers · تسليم متكرر · module واضح · owner · playbook ~80+ · هامش صحي · مكتبة proof · إشارة شريك/قناة عند التطبيق.

**الكود:** `compute_venture_readiness_score` · `classify_venture_readiness` في `intelligence_os/venture_signal.py`

**الوثيقة المرافقة:** [`../group/VENTURE_GRADUATION_GATE.md`](../group/VENTURE_GRADUATION_GATE.md)
