# العربية

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

محرّك تقارير المخاطر يجعل الاختناقات التشغيلية والامتثالية مرئيةً للقيادة قبل أن تتحوّل إلى خسارة. الهدف: لا تُفاجأ القيادة؛ كل خطر مرصود، مرتّب حسب الأثر، ومرتبط بمالك وإجراء.

## فئات المخاطر

- **مخاطر تشغيلية:** اختناقات سير العمل، تأخّر تجاوز SLA، تراكم طابور المعالجة المؤجَّلة.
- **مخاطر امتثال:** خطوات تواصل خارجي بلا موافقة، بيانات شخصية في مسار غير منقَّح، مصادر بلا أساس قانوني.
- **مخاطر تبنّي:** خدمات متعاقد عليها وغير مفعَّلة، انخفاض عمق الاستخدام.
- **مخاطر اعتمادية:** اعتماد مفرط على تكامل واحد أو مالك واحد.

## تدفّق التقرير

1. يجمع المحرّك إشارات المخاطر من سجل المعوّقات عبر `auto_client_acquisition/founder_v10/blockers.py`.
2. يضيف إشارات التكلفة الشاذة عبر `auto_client_acquisition/founder_v10/cost_summary.py`.
3. يرتّب كل خطر بثلاثة حقول: الاحتمالية، الأثر، المالك.
4. يُسقِط في كل تقرير الإجراء المقترح والدليل الداعم له.
5. تُحفَظ التقارير في `executive/risk_reports/` وتمرّ عبر العارض الآمن قبل أي مشاركة مع العميل.

## المقاييس

- نسبة المخاطر المفتوحة الحاملة لمالك معيَّن: 100% (هدف).
- زمن وسطي من رصد الخطر إلى ظهوره في تقرير: أقل من 24 ساعة.
- عدد المخاطر التشغيلية المغلقة شهرياً مقابل المفتوحة: مرصود ومعروض.
- نسبة المخاطر المرتبطة بإجراء مقترح: 100%.

## خطافات المراقبة

- تتبّع تجميع الإشارات عبر `dealix/observability/otel.py`.
- التقاط الأخطاء عبر `dealix/observability/sentry.py`.
- قيد تدقيق لكل تقرير مخاطر صادر عبر `dealix/trust/audit.py`.
- تنبيه عند ظهور خطر بدرجة أثر عالية بلا مالك خلال 24 ساعة.

## قواعد الحوكمة

- كل خطر يُعرَض بدليل مرصود؛ لا تخمين بلا مصدر.
- لا بيانات تعريف شخصية في تقرير مخاطر موجَّه للعميل.
- درجة الأثر تقديرية وتُوسَم كذلك صراحةً.
- التقرير الموجَّه للعميل لا يُشارَك دون موافقة بشرية موثَّقة.
- لا يُوصَف أي خطر بلغة تَعِد بنتيجة مضمونة بعد المعالجة.

## إجراء التراجع

1. عند خطأ في تصنيف خطر: تصحيح الدرجة ووسم النسخة السابقة "مصحَّحة".
2. تحديد مصدر الإشارة الخاطئة وإصلاحه عند المنبع.
3. إعادة توليد التقرير وإبلاغ مالك الخطر.
4. تسجيل التصحيح كقيد تدقيق.

## درجة الجاهزية الحالية

**70 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/executive_intelligence/architecture.md`، `platform/executive_intelligence/readiness.md`، `executive/risk_reports/README.md`.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

The Risk Reporting engine makes operational and compliance bottlenecks visible to leadership before they become a loss. The goal: leadership is not surprised; every risk is observed, ranked by impact, and tied to an owner and an action.

## Risk categories

- **Operational risk:** workflow bottlenecks, SLA breach delays, dead-letter queue backlog.
- **Compliance risk:** external communication steps without approval, PII in an unredacted path, sources without a lawful basis.
- **Adoption risk:** contracted but unactivated services, declining usage depth.
- **Dependency risk:** over-reliance on a single integration or a single owner.

## Reporting flow

1. The engine aggregates risk signals from the blocker register via `auto_client_acquisition/founder_v10/blockers.py`.
2. It adds anomalous cost signals via `auto_client_acquisition/founder_v10/cost_summary.py`.
3. It ranks every risk by three fields: likelihood, impact, owner.
4. It projects, per report, the suggested action and its supporting evidence.
5. Reports are stored in `executive/risk_reports/` and pass the customer-safe renderer before any customer sharing.

## Metrics

- Share of open risks carrying a named owner: 100% (target).
- Median time from risk detection to appearance in a report: under 24 hours.
- Operational risks closed per month versus opened: observed and shown.
- Share of risks tied to a suggested action: 100%.

## Observability hooks

- Signal aggregation traced via `dealix/observability/otel.py`.
- Errors captured via `dealix/observability/sentry.py`.
- An audit entry for every risk report issued via `dealix/trust/audit.py`.
- Alert when a high-impact risk appears without an owner within 24 hours.

## Governance rules

- Every risk is shown with observed evidence; no guess without a source.
- No PII in a customer-facing risk report.
- The impact score is an estimate and is labelled as such explicitly.
- A customer-facing report is not shared without a documented human approval.
- No risk is described in language that promises a guaranteed outcome after mitigation.

## Rollback procedure

1. On a risk misclassification: correct the score and mark the prior version "corrected".
2. Identify the faulty signal source and fix it at origin.
3. Regenerate the report and notify the risk owner.
4. Record the correction as an audit entry.

## Current readiness score

**70 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/executive_intelligence/architecture.md`, `platform/executive_intelligence/readiness.md`, `executive/risk_reports/README.md`.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
