# العربية

## مؤشرات أداء وكيل العمليات

تُتتبَّع المؤشرات عبر `auto_client_acquisition/agent_observability/quality.py` و`cost.py`.

| المؤشر | التعريف | الهدف |
|---|---|---|
| `tasks_completed_on_time` | نسبة المهام المكتملة في موعدها | اتجاه صاعد |
| `delivery_cycle_time` | زمن دورة التسليم من البدء إلى الإغلاق | اتجاه نازل |
| `evidence_pack_completeness` | نسبة حزم الأدلة المكتملة العناصر | اتجاه صاعد |
| `rework_rate` | نسبة المهام التي احتاجت إعادة عمل | اتجاه نازل |

كل الأرقام تقديرية ومجمَّعة؛ لا تُعرض كضمان. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

## Ops agent KPIs

KPIs are tracked via `auto_client_acquisition/agent_observability/quality.py` and `cost.py`.

| KPI | Definition | Target |
|---|---|---|
| `tasks_completed_on_time` | Share of tasks completed on schedule | Upward trend |
| `delivery_cycle_time` | Delivery cycle time from start to close | Downward trend |
| `evidence_pack_completeness` | Share of evidence packs complete on all items | Upward trend |
| `rework_rate` | Share of tasks that needed rework | Downward trend |

All figures are estimated and aggregated; none are presented as a guarantee. Estimated value is not Verified value.
