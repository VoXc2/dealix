# العربية

## مؤشرات أداء وكيل الدعم

تُتتبَّع المؤشرات عبر `auto_client_acquisition/agent_observability/quality.py` و`cost.py`.

| المؤشر | التعريف | الهدف |
|---|---|---|
| `tickets_resolved` | عدد التذاكر التي وصلت حالة الحل | اتجاه صاعد |
| `first_response_time` | زمن أول رد مسودة على التذكرة | أقل من المعيار المتفق عليه |
| `escalation_rate` | نسبة التذاكر المُصعَّدة لإنسان | يُقاس، يُراقَب |
| `customer_satisfaction` | رضا العميل بعد الحل (تقديري) | يُقاس، لا يُضمَن |

كل الأرقام تقديرية ومجمَّعة؛ لا تُعرض كضمان. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

## Support agent KPIs

KPIs are tracked via `auto_client_acquisition/agent_observability/quality.py` and `cost.py`.

| KPI | Definition | Target |
|---|---|---|
| `tickets_resolved` | Count of tickets that reached resolved status | Upward trend |
| `first_response_time` | Time to first draft reply on a ticket | Under the agreed baseline |
| `escalation_rate` | Share of tickets escalated to a human | Measured, monitored |
| `customer_satisfaction` | Customer satisfaction after resolution (estimated) | Measured, not guaranteed |

All figures are estimated and aggregated; none are presented as a guarantee. Estimated value is not Verified value.
