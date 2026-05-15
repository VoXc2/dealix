# العربية

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

محرّك الموجزات يحوّل أحداث الطبقات الأدنى إلى موجز تنفيذي مقروء في دقائق. الهدف: حين يبدأ القائد أسبوعه، يجد موجزاً جاهزاً يجيب عن أربعة أسئلة — أين الإيراد؟ أين الهدر؟ أين المخاطرة؟ أين التحسين القادم؟ المحرّك لا يكتب نصاً تسويقياً ولا يَعِد بأرقام؛ يعرض ما رُصِد فقط.

## المخرجات

- **الموجز التنفيذي الأسبوعي:** يُولَّد آلياً كل بداية أسبوع عمل، من قالب `executive/briefs/weekly_brief_template.md`.
- **موجز مجلس الإدارة الشهري:** إيقاع شهري، من قالب `executive/briefs/monthly_board_brief_template.md`.
- **مذكّرة استراتيجية عند الطلب:** تُكتَب يدوياً من القيادة وتُحفَظ في `executive/strategic_memos/`.

## تدفّق التوليد

1. يقرأ المحرّك الأحداث المجمَّعة عبر نمط `auto_client_acquisition/founder_v10/daily_brief.py` (عدّ وحالات فقط، لا بيانات شخصية).
2. يجمّع التكلفة عبر `auto_client_acquisition/founder_v10/cost_summary.py` والأدلة عبر `evidence_summary.py`.
3. يرتّب الاختناقات حسب الأثر عبر `auto_client_acquisition/founder_v10/blockers.py`.
4. يستخرج الإجراءات والقرارات التالية عبر `next_actions.py` و`next_decisions.py`.
5. يطبّق الإيقاع الشهري نمط `auto_client_acquisition/value_os/monthly_report.py`.
6. يمرّ كل موجز موجَّه للعميل عبر `customer_safe_renderer.py` وينتهي بإفصاح القيمة التقديرية.

## المقاييس

- نسبة الموجزات الأسبوعية المولَّدة في الموعد: 100% (هدف).
- زمن توليد الموجز من المحفّز إلى المسودّة: أقل من دقيقتين.
- نسبة بنود الموجز المرتبطة بمصدر بيانات معلن: 100%.
- نسبة الموجزات التي اجتازت العارض الآمن قبل الإرسال: 100%.

## خطافات المراقبة

- تتبّع كل توليد عبر `dealix/observability/otel.py`.
- التقاط أخطاء التوليد عبر `dealix/observability/sentry.py`.
- قيد تدقيق لكل موجز صادر عبر `dealix/trust/audit.py`.
- تنبيه عند فوات نافذة التوليد الأسبوعي.

## قواعد الحوكمة

- لا يحوي الموجز أي رقم مفبرك؛ كل رقم مرصود أو محسوب من بيانات حقيقية.
- الأرقام التقديرية تُوسَم "تقديري" مع مدى الثقة.
- لا بيانات تعريف شخصية في أي موجز موجَّه للعميل.
- لا ادعاء "مبيعات مضمونة"؛ تُستبدَل بـ "فرص مُثبتة بأدلة".
- الموجز الموجَّه للعميل لا يُرسَل دون موافقة بشرية موثَّقة.

## إجراء التراجع

1. عند خطأ في موجز صادر: سحب النسخة ووسمها "مسحوبة" في سجل التدقيق.
2. تحديد المصدر الخاطئ من نسب البيانات في الموجز.
3. إعادة التوليد من الأحداث المصحَّحة بعد تأكيد المصدر.
4. إبلاغ المستلمين بنسخة مصحَّحة وتسجيل السبب.

## درجة الجاهزية الحالية

**72 / 100 — internal beta.** المقياس: 0–59 نموذج أولي / 60–74 تجربة داخلية / 75–84 تجربة عميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/executive_intelligence/architecture.md`، `platform/executive_intelligence/readiness.md`، `executive/briefs/weekly_brief_template.md`.

الإفصاح: القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

---

# English

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

The Briefing Engine converts lower-layer events into an executive brief that reads in minutes. The goal: when a leader starts the week, a brief is already prepared that answers four questions — where is revenue, where is waste, where is risk, where is the next improvement. The engine writes no marketing copy and promises no numbers; it shows only what was observed.

## Outputs

- **Weekly executive brief:** generated automatically at the start of each working week, from the template `executive/briefs/weekly_brief_template.md`.
- **Monthly board brief:** a monthly cadence, from the template `executive/briefs/monthly_board_brief_template.md`.
- **Strategic memo on demand:** written by leadership and stored in `executive/strategic_memos/`.

## Generation flow

1. The engine reads aggregated events via the pattern in `auto_client_acquisition/founder_v10/daily_brief.py` (counts and statuses only, no PII).
2. It aggregates cost via `auto_client_acquisition/founder_v10/cost_summary.py` and evidence via `evidence_summary.py`.
3. It ranks bottlenecks by impact via `auto_client_acquisition/founder_v10/blockers.py`.
4. It extracts the next actions and decisions via `next_actions.py` and `next_decisions.py`.
5. The monthly cadence applies the pattern in `auto_client_acquisition/value_os/monthly_report.py`.
6. Every customer-facing brief passes the `customer_safe_renderer.py` and ends with the estimated-value disclosure.

## Metrics

- Share of weekly briefs generated on time: 100% (target).
- Brief generation time from trigger to draft: under two minutes.
- Share of brief items tied to a declared data source: 100%.
- Share of briefs that passed the customer-safe renderer before sending: 100%.

## Observability hooks

- Every generation traced via `dealix/observability/otel.py`.
- Generation errors captured via `dealix/observability/sentry.py`.
- An audit entry for every brief issued via `dealix/trust/audit.py`.
- Alert when the weekly generation window is missed.

## Governance rules

- A brief contains no fabricated number; every number is observed or computed from real data.
- Estimated numbers are labelled "estimated" with a confidence range.
- No PII in any customer-facing brief.
- No "guaranteed sales" claim; replaced with "evidenced opportunities".
- A customer-facing brief is not sent without a documented human approval.

## Rollback procedure

1. On an error in an issued brief: withdraw the version and mark it "withdrawn" in the audit log.
2. Identify the faulty source from the brief's data lineage.
3. Regenerate from corrected events after confirming the source.
4. Notify recipients with a corrected version and record the reason.

## Current readiness score

**72 / 100 — internal beta.** Scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/executive_intelligence/architecture.md`, `platform/executive_intelligence/readiness.md`, `executive/briefs/weekly_brief_template.md`.

Disclosure: Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
