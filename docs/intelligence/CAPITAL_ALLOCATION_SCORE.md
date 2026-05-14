# Capital Allocation Score — أولوية الاستثمار الداخلي

**الغرض:** أي وحدة / خدمة / feature تحصل على **Priority Score** فيحدد **أين يذهب الوقت والمال**.

## الصيغة

```text
Priority Score =
  revenue_score           * 0.25
+ repeatability_score     * 0.20
+ proof_score             * 0.20
+ productization_score    * 0.15
+ strategic_moat_score    * 0.10
+ risk_adjusted_score     * 0.10
```

كل مدخل **0–100** (بعد تطبيع من الأدلة الفعلية).

## النطاقات

| Score | قرار |
|-------|------|
| **85–100** | Invest / Scale |
| **70–84** | Build carefully |
| **55–69** | Pilot only |
| **40–54** | Hold |
| **<40** | Kill |

## أمثلة

**Revenue Intelligence** بأرقام عالية → **Invest / Scale**.  
**Random custom chatbot** بأرقام منخفضة وإثبات ضعيف → **Kill** أو إعادة إطار كـ **Company Brain** بحوكمة.

**التنفيذ المحض في الكود:** `compute_capital_priority_score` · `capital_priority_band` في `auto_client_acquisition/intelligence_os/capital_allocator.py`

**السياق المؤسسي:** [`../group/CAPITAL_ALLOCATION_MODEL.md`](../group/CAPITAL_ALLOCATION_MODEL.md)
