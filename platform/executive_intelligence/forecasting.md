# العربية

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

محرّك التوقّعات يُسقِط الاتجاهات من البيانات المرصودة فقط. الهدف: مساعدة القيادة على رؤية الاتجاه القادم دون الوعد به. كل توقّع يُعرَض كمدى مع مدى ثقة معلن، لا كرقم مفرد ولا كضمان.

## مبادئ التوقّع

- **بيانات مرصودة فقط:** المدخلات من أحداث `value_ledger` والتقارير الشهرية، لا أرقام مفترَضة.
- **مدى لا رقم:** كل توقّع له حدّ أدنى وحدّ أعلى ومدى ثقة (مثل 80%).
- **نافذة معلنة:** كل توقّع يذكر نافذة البيانات المستخدَمة وأفق الإسقاط.
- **لا ضمان:** لا تُستخدَم لغة "سنحقّق" أو "مضمون"؛ تُستخدَم "الاتجاه المرصود يشير إلى".

## مجالات التوقّع

- اتجاه الساعات الموفَّرة على أفق ربع سنوي.
- اتجاه العملاء المؤهَّلين بناءً على معدّل الرصد التاريخي.
- اتجاه التكلفة لكل نتيجة.
- اتجاه معدّل التبنّي عبر الخدمات المتعاقد عليها.

## تدفّق التوقّع

1. يقرأ المحرّك السلاسل الزمنية المجمَّعة عبر `auto_client_acquisition/value_os/value_ledger.py`.
2. يطبّق نمط الإيقاع الشهري من `auto_client_acquisition/value_os/monthly_report.py`.
3. يحسب المدى ومدى الثقة من تباين البيانات المرصودة.
4. يمرّ كل توقّع موجَّه للعميل عبر `customer_safe_renderer.py`.

## المقاييس

- نسبة التوقّعات المعروضة كمدى لا كرقم مفرد: 100%.
- نسبة التوقّعات الحاملة لمدى ثقة معلن: 100%.
- خطأ الإسقاط الرجعي مقابل المرصود الفعلي: مرصود ومراجَع شهرياً.
- نسبة التوقّعات التي تذكر نافذة البيانات: 100%.

## خطافات المراقبة

- تتبّع كل إسقاط عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- قيد تدقيق لكل توقّع صادر عبر `dealix/trust/audit.py`.
- تنبيه عند اتساع خطأ الإسقاط الرجعي فوق العتبة.

## قواعد الحوكمة

- لا يُعرَض أي توقّع كرقم مضمون أو وعد.
- مدى الثقة إلزامي في كل توقّع.
- التوقّعات بنافذة بيانات قصيرة جداً تُوسَم "ثقة منخفضة" صراحةً.
- لا بيانات تعريف شخصية في أي توقّع موجَّه للعميل.

## إجراء التراجع

1. عند اتساع خطأ الإسقاط: تعليق التوقّع المتأثّر ووسمه "قيد المراجعة".
2. مراجعة جودة السلسلة الزمنية المدخَلة وإصلاح أي ثغرة.
3. إعادة الإسقاط بنافذة مصحَّحة وإبلاغ القيادة.
4. تسجيل التصحيح كقيد تدقيق.

## درجة الجاهزية الحالية

**66 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/executive_intelligence/architecture.md`، `platform/executive_intelligence/executive_metrics.md`.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

The Forecasting engine projects trends from observed data only. The goal: help leadership see the coming trend without promising it. Every forecast is shown as a range with a stated confidence band — not a single number and not a guarantee.

## Forecasting principles

- **Observed data only:** inputs come from `value_ledger` events and monthly reports, no assumed numbers.
- **Range, not a number:** every forecast has a lower bound, an upper bound, and a confidence band (for example 80%).
- **Stated window:** every forecast states the data window used and the projection horizon.
- **No guarantee:** no "we will achieve" or "guaranteed" language; "the observed trend points to" is used instead.

## Forecast domains

- Hours-saved trend over a quarterly horizon.
- Qualified-leads trend based on the historical detection rate.
- Cost-per-outcome trend.
- Adoption-rate trend across contracted services.

## Forecasting flow

1. The engine reads aggregated time series via `auto_client_acquisition/value_os/value_ledger.py`.
2. It applies the monthly cadence pattern from `auto_client_acquisition/value_os/monthly_report.py`.
3. It computes the range and confidence band from the variance of observed data.
4. Every customer-facing forecast passes the `customer_safe_renderer.py`.

## Metrics

- Share of forecasts shown as a range, not a single number: 100%.
- Share of forecasts carrying a stated confidence band: 100%.
- Backtest projection error versus observed actuals: observed and reviewed monthly.
- Share of forecasts stating their data window: 100%.

## Observability hooks

- Every projection traced via `dealix/observability/otel.py`.
- Errors captured via `dealix/observability/sentry.py`.
- An audit entry for every forecast issued via `dealix/trust/audit.py`.
- Alert when the backtest error widens beyond the threshold.

## Governance rules

- No forecast is shown as a guaranteed number or a promise.
- A confidence band is mandatory on every forecast.
- Forecasts with a very short data window are explicitly labelled "low confidence".
- No PII in any customer-facing forecast.

## Rollback procedure

1. On a widening projection error: suspend the affected forecast and mark it "under review".
2. Review the quality of the input time series and fix any gap.
3. Re-project with a corrected window and notify leadership.
4. Record the correction as an audit entry.

## Current readiness score

**66 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/executive_intelligence/architecture.md`, `platform/executive_intelligence/executive_metrics.md`.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
