# العربية

## مؤشرات أداء الوكيل التنفيذي

تُتتبَّع المؤشرات عبر `auto_client_acquisition/agent_observability/quality.py` و`cost.py`.

| المؤشر | التعريف | الهدف |
|---|---|---|
| `decision_memo_turnaround` | زمن تسليم مسودة مذكّرة القرار | اتجاه نازل |
| `evidence_backed_recommendations` | نسبة التوصيات المرفقة بأدلة | 100% |
| `forecast_calibration` | مدى تطابق التوقّعات التقديرية مع النتائج اللاحقة | يُقاس، لا يُضمَن |
| `escalation_quality` | نسبة التصعيدات التي قبلها المؤسس دون تعديل جوهري | يُقاس |

كل الأرقام تقديرية ومجمَّعة؛ لا تُعرض كضمان. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

## Executive agent KPIs

KPIs are tracked via `auto_client_acquisition/agent_observability/quality.py` and `cost.py`.

| KPI | Definition | Target |
|---|---|---|
| `decision_memo_turnaround` | Time to deliver a decision memo draft | Downward trend |
| `evidence_backed_recommendations` | Share of recommendations attached to evidence | 100% |
| `forecast_calibration` | How well estimated forecasts match later outcomes | Measured, not guaranteed |
| `escalation_quality` | Share of escalations the founder accepted without material edit | Measured |

All figures are estimated and aggregated; none are presented as a guarantee. Estimated value is not Verified value.
