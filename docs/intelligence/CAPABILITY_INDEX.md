# Dealix Capability Index (DCI)

**مؤشر نضج العميل** عبر **7 قدرات** (كل مدخل 0–100 ثم مركب):

Revenue · Customer · Operations · Knowledge · Data · Governance · Reporting  

## الصيغة المؤسسية

```text
DCI =
  revenue_capability * 0.20
+ data_capability * 0.15
+ governance_capability * 0.20
+ operations_capability * 0.15
+ knowledge_capability * 0.10
+ customer_capability * 0.10
+ reporting_capability * 0.10
```

## الاستخدام في العرض

```text
Current DCI: 32
Target DCI after Sprint: 48
Target DCI after Retainer: 65
```

**البيع:** رحلة **نضج** لا «خدمة عشوائية».

**سياق الأدبيات:** AI readiness تنظيمي وتعلّم عبر ثقافة وعمليات وبيانات وحوكمة — لا شراء تقنية فقط؛ يدعم فكرة DCI؛ انظر [McKinsey — state of AI / workflow redesign](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai).

**الكود:** `CapabilityScores` · `compute_dci` في `intelligence_os/capability_index.py`

**خريطة العروض:** [`OFFER_TO_CAPABILITY_MAP.md`](OFFER_TO_CAPABILITY_MAP.md) · [`../company/CLIENT_CAPABILITY_SCORE.md`](../company/CLIENT_CAPABILITY_SCORE.md)
