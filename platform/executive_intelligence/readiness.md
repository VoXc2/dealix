# العربية

# جاهزية طبقة الذكاء التنفيذي — الطبقة التاسعة

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

ترفع الطبقة 9 Dealix من "مورّد تقنية" إلى "شريك استراتيجي": عندما يفتح القائد لوحة القيادة، يرى أين الإيراد، أين الهدر، أين المخاطرة، وأين التحسين القادم — كل ذلك مدعوماً بأدلة من سير العمل ومن دفتر القيمة.

## قائمة الجاهزية

- [x] لكل خدمة قصة عائد قابلة للعرض من `auto_client_acquisition/value_os/value_ledger.py`.
- [x] الموجز التنفيذي الأسبوعي يُولَّد آلياً من نمط `auto_client_acquisition/founder_v10/daily_brief.py`.
- [x] الساعات الموفَّرة مرصودة ومعروضة مع نافذة القياس.
- [x] العملاء المؤهَّلون مرصودون ومعروضون.
- [x] الاختناقات مرئية ومرتّبة حسب الأثر عبر `auto_client_acquisition/founder_v10/blockers.py`.
- [x] معدّل التبنّي مرئي عبر مركز القيادة التنفيذي.
- [x] كل توصية مرتبطة بدليل عبر `auto_client_acquisition/proof_os/proof_pack.py`.
- [x] كل تقرير موجَّه للعميل يمرّ عبر `customer_safe_renderer.py`.
- [x] التقارير تُظهر أثر الأعمال لا الاستخدام الخام فقط.
- [ ] موجز مجلس الإدارة الشهري مؤتمَت بالكامل (قالب قائم، الأتمتة قيد الإنشاء).
- [ ] خطأ الإسقاط الرجعي للتوقّعات مقيَّم على مجموعة تقييم ثابتة (قيد الإنشاء).

## المقاييس

- نسبة الخدمات الحاملة لقصة عائد: 100% (هدف).
- نسبة الموجزات الأسبوعية المولَّدة في الموعد: 100% (هدف).
- نسبة بنود التقارير المرتبطة بمصدر بيانات معلن: 100%.
- زمن وسطي من رصد الخطر إلى ظهوره في تقرير: أقل من 24 ساعة.
- نسبة التقارير الموجَّهة للعميل التي اجتازت العارض الآمن: 100%.
- نسبة التوقّعات المعروضة كمدى مع مدى ثقة: 100%.

## خطافات المراقبة

- تتبّع كل توليد تقرير عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- تتبّع التكلفة لكل تشغيل عبر `dealix/observability/cost_tracker.py`.
- قيد تدقيق لكل تقرير صادر عبر `dealix/trust/audit.py`.
- مقاييس القيمة عبر `auto_client_acquisition/value_os/value_ledger.py`.
- تنبيه عند فوات نافذة الموجز الأسبوعي أو غياب مالك لخطر عالي الأثر.

## قواعد الحوكمة

- لا يحوي أي تقرير رقماً مفبركاً؛ كل رقم مرصود أو محسوب من بيانات حقيقية.
- الأرقام التقديرية تُوسَم "تقديري" مع مدى الثقة، ولا تُعرض كحقيقة.
- لا ادعاء "مبيعات مضمونة"؛ تُستبدَل بـ "فرص مُثبتة بأدلة".
- لا بيانات تعريف شخصية في أي تقرير موجَّه للعميل.
- لا يُرسَل تقرير موجَّه للعميل دون موافقة بشرية موثَّقة.
- تقارير القطاع تعرض المنهجية والأنماط المجمَّعة فقط، لا مقاييس سرّية.
- يُراجَع تعريف كل مقياس وكل قالب ربع سنوياً من مالك الطبقة.

## إجراء التراجع

1. عند خطأ في تقرير صادر: سحب النسخة ووسمها "مسحوبة" في سجل التدقيق.
2. تحديد المصدر الخاطئ من نسب البيانات في التقرير.
3. إيقاف التوليد الآلي للقالب المتأثّر حتى تأكيد المصدر.
4. إعادة التوليد من الأحداث المصحَّحة وإبلاغ المستلمين بنسخة مصحَّحة.
5. الرجوع إلى الإصدار المستقر السابق للقالب من سجل git عند الحاجة.
6. تسجيل التراجع كقيد تدقيق وإبلاغ مالك الطبقة.

## درجة الجاهزية الحالية

**الدرجة: 71 / 100 — internal beta (تجربة داخلية).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/executive_intelligence/architecture.md`، `platform/executive_intelligence/scorecard.yaml`، `platform/executive_intelligence/tests.md`.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

# Executive Intelligence Layer Readiness — Layer 9

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

Layer 9 lifts Dealix from a "technology vendor" to a "strategic partner": when a leader opens the leadership dashboard, they see where revenue is, where waste is, where risk is, and where the next improvement is — all supported by evidence from workflows and from the value ledger.

## Readiness checklist

- [x] Every service has a presentable ROI story from `auto_client_acquisition/value_os/value_ledger.py`.
- [x] The weekly executive brief is generated automatically from the pattern in `auto_client_acquisition/founder_v10/daily_brief.py`.
- [x] Hours saved are observed and shown with the measurement window.
- [x] Qualified leads are observed and shown.
- [x] Bottlenecks are visible and ranked by impact via `auto_client_acquisition/founder_v10/blockers.py`.
- [x] Adoption rate is visible through the Executive Command Center.
- [x] Every recommendation is tied to evidence via `auto_client_acquisition/proof_os/proof_pack.py`.
- [x] Every customer-facing report passes the `customer_safe_renderer.py`.
- [x] Reports show business impact, not just raw usage.
- [ ] The monthly board brief is fully automated (template exists, automation in progress).
- [ ] Forecast backtest error is evaluated on a fixed eval set (in progress).

## Metrics

- Share of services carrying an ROI story: 100% (target).
- Share of weekly briefs generated on time: 100% (target).
- Share of report items tied to a declared data source: 100%.
- Median time from risk detection to appearance in a report: under 24 hours.
- Share of customer-facing reports that passed the customer-safe renderer: 100%.
- Share of forecasts shown as a range with a confidence band: 100%.

## Observability hooks

- Every report generation traced via `dealix/observability/otel.py`.
- Errors captured via `dealix/observability/sentry.py`.
- Per-run cost tracking via `dealix/observability/cost_tracker.py`.
- An audit entry for every report issued via `dealix/trust/audit.py`.
- Value metrics via `auto_client_acquisition/value_os/value_ledger.py`.
- Alert when the weekly brief window is missed or a high-impact risk lacks an owner.

## Governance rules

- No report contains a fabricated number; every number is observed or computed from real data.
- Estimated numbers are labelled "estimated" with a confidence range and are never presented as fact.
- No "guaranteed sales" claim; replaced with "evidenced opportunities".
- No PII in any customer-facing report.
- A customer-facing report is not sent without a documented human approval.
- Sector reports present methodology and aggregated patterns only, no confidential metrics.
- Every metric definition and every template is reviewed quarterly by the Layer Lead.

## Rollback procedure

1. On an error in an issued report: withdraw the version and mark it "withdrawn" in the audit log.
2. Identify the faulty source from the report's data lineage.
3. Pause automated generation of the affected template until the source is confirmed.
4. Regenerate from corrected events and notify recipients with a corrected version.
5. Restore the previous stable template version from the git history if needed.
6. Record the rollback as an audit entry and notify the layer owner.

## Current readiness score

**Score: 71 / 100 — internal beta.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/executive_intelligence/architecture.md`, `platform/executive_intelligence/scorecard.yaml`, `platform/executive_intelligence/tests.md`.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
