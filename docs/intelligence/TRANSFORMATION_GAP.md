# Dealix Transformation Gap (DTG)

```text
DTG = Target Capability − Current Capability
```

## ربط DTG بالفرصة

| DTG | جدوى تنفيذ (feasibility) | قرار |
|-----|---------------------------|------|
| عالٍ | عالٍ | **أفضل فرصة sprint** |
| عالٍ | منخفض | **Diagnostic أولًا** |
| منخفض | عالٍ | **Quick win** |
| منخفض | منخفض | **إعادة أولوية** |

**السياق:** قياس «فجوة تحول» مرتبط بقيمة تنفيذية أفضل من تصنيفات نضج عامة فقط — انظر نقاشات scaling والـ ROI في [McKinsey — gen AI programs](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/overcoming-two-issues-that-are-sinking-gen-ai-programs).

**الكود:** `transformation_gap` · `classify_sprint_opportunity` في `intelligence_os/transformation_gap.py`
