# العربية

## مؤشرات أداء وكيل المبيعات

تُتتبَّع المؤشرات عبر `auto_client_acquisition/agent_observability/quality.py` و`cost.py`.

| المؤشر | التعريف | الهدف |
|---|---|---|
| `qualified_leads` | عدد العملاء المحتملين الذين اجتازوا التأهيل | اتجاه صاعد |
| `meeting_bookings` | عدد طلبات حجز الاجتماعات المُنشأة | اتجاه صاعد |
| `proposal_acceptance_rate` | نسبة العروض المقبولة (تقديري) | يُقاس، لا يُضمَن |
| `response_time` | زمن استجابة الوكيل للعميل المحتمل | أقل من المعيار المتفق عليه |

كل الأرقام تقديرية ومجمَّعة؛ لا تُعرض كضمان. القيمة التقديرية ليست قيمة مُتحقَّقة.

---

# English

## Sales agent KPIs

KPIs are tracked via `auto_client_acquisition/agent_observability/quality.py` and `cost.py`.

| KPI | Definition | Target |
|---|---|---|
| `qualified_leads` | Count of prospects that passed qualification | Upward trend |
| `meeting_bookings` | Count of meeting booking requests created | Upward trend |
| `proposal_acceptance_rate` | Share of accepted proposals (estimated) | Measured, not guaranteed |
| `response_time` | Agent response time to a prospect | Under the agreed baseline |

All figures are estimated and aggregated; none are presented as a guarantee. Estimated value is not Verified value.
