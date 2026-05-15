# العربية

## مؤشرات أداء وكيل الحوكمة

تُتتبَّع المؤشرات عبر `auto_client_acquisition/agent_observability/quality.py` و`trace.py`.

| المؤشر | التعريف | الهدف |
|---|---|---|
| `policy_evaluation_coverage` | نسبة إجراءات الوكلاء التي مرت بتقييم سياسة | 100% |
| `escalation_routing_accuracy` | نسبة التصعيدات الموجَّهة للمُوافِق الصحيح | اتجاه صاعد |
| `audit_trace_completeness` | نسبة التقييمات ذات أثر قرار كامل | 100% |
| `non_negotiable_violations_blocked` | عدد محاولات انتهاك اللاءات المحجوبة | يُقاس، يجب حجب الكل |

كل الأرقام تقديرية ومجمَّعة؛ لا تُعرض كضمان. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

## Governance agent KPIs

KPIs are tracked via `auto_client_acquisition/agent_observability/quality.py` and `trace.py`.

| KPI | Definition | Target |
|---|---|---|
| `policy_evaluation_coverage` | Share of agent actions that passed a policy evaluation | 100% |
| `escalation_routing_accuracy` | Share of escalations routed to the correct approver | Upward trend |
| `audit_trace_completeness` | Share of evaluations with a complete decision trace | 100% |
| `non_negotiable_violations_blocked` | Count of attempted non-negotiable violations blocked | Measured, all must be blocked |

All figures are estimated and aggregated; none are presented as a guarantee. Estimated value is not Verified value.
