# العربية

**Owner:** مالك طبقة الذكاء التنفيذي (Executive Intelligence Layer Lead) — قسم هندسة المنصة.

## الغرض

الطبقة 9 — الذكاء التنفيذي — ترفع Dealix من "مورّد تقنية" إلى "شريك استراتيجي". هدف الطبقة: عندما يفتح القائد لوحة القيادة، يرى أثراً واضحاً على الأعمال — أين الإيراد؟ أين الهدر؟ أين المخاطرة؟ أين التحسين القادم؟ لا تنتج هذه الطبقة بيانات استخدام خام بل تحوّلها إلى رواية أثر لكل خدمة، مدعومة بأدلة من سير العمل ومن دفتر القيمة.

## المكوّنات

- **محرّك الموجزات (Briefing Engine):** يجمّع الموجز التنفيذي الأسبوعي والموجز الشهري لمجلس الإدارة من الطبقات الأدنى. يستند إلى نمط `auto_client_acquisition/founder_v10/daily_brief.py` للتجميع الدفاعي ونمط `auto_client_acquisition/value_os/monthly_report.py` للإيقاع الشهري.
- **لوحة عائد الاستثمار (ROI Dashboard):** قصة عائد لكل خدمة — ساعات موفَّرة، عملاء مؤهَّلون، احتكاك مُزال — من `auto_client_acquisition/value_os/value_ledger.py`.
- **مركز القيادة التنفيذي (Executive Command Center):** يركّب اللوحة ذات الخمس عشرة لوحة فرعية عبر `auto_client_acquisition/executive_command_center/builder.py` ويعرضها بصيغة آمنة للعميل عبر `customer_safe_renderer.py`.
- **محرّك المخاطر (Risk Reporting):** يجمع إشارات المخاطر التشغيلية والامتثالية ويعرض الاختناقات المرئية، مستفيداً من سجل المخاطر في `auto_client_acquisition/founder_v10/blockers.py`.
- **محرّك التوقّعات (Forecasting):** يسقط الاتجاهات من البيانات المرصودة — لا وعود مضمونة، فقط مدى وثقة.
- **محرّك الأدلة (Proof Engine):** يربط كل توصية بدليل عبر `auto_client_acquisition/proof_os/proof_pack.py` و`proof_score.py`.

## تدفّق البيانات

1. تنشر الطبقات الأدنى أحداثاً: قيمة، احتكاك، تبنّي، أدلة، تكلفة.
2. يقرأ محرّك الموجزات الأحداث المجمَّعة (عدّ وحالات فقط، لا بيانات شخصية).
3. تحوّل لوحة عائد الاستثمار الأحداث إلى رواية أثر لكل خدمة.
4. يجمع محرّك المخاطر الإشارات ويرتّب الاختناقات حسب الأثر.
5. يسقط محرّك التوقّعات الاتجاهات بمدى وثقة معلن.
6. يركّب مركز القيادة التنفيذي اللوحة ويُصدر الموجز الأسبوعي آلياً.
7. كل تقرير موجَّه للعميل يمرّ عبر العارض الآمن وينتهي بإفصاح "القيمة التقديرية ليست قيمة مُتحقَّقة".

## الربط بالشيفرة الموجودة

| المكوّن | المسار الحقيقي في المستودع |
|---|---|
| تجميع الموجز اليومي (النمط) | `auto_client_acquisition/founder_v10/daily_brief.py` |
| باني لوحة المؤسس | `auto_client_acquisition/founder_v10/dashboard_builder.py` |
| ملخّص التكلفة | `auto_client_acquisition/founder_v10/cost_summary.py` |
| ملخّص الأدلة | `auto_client_acquisition/founder_v10/evidence_summary.py` |
| الاختناقات/المعوّقات | `auto_client_acquisition/founder_v10/blockers.py` |
| الإجراءات التالية | `auto_client_acquisition/founder_v10/next_actions.py` |
| باني مركز القيادة التنفيذي | `auto_client_acquisition/executive_command_center/builder.py` |
| لوحات مركز القيادة | `auto_client_acquisition/executive_command_center/panels.py` |
| القرارات التالية | `auto_client_acquisition/executive_command_center/next_decisions.py` |
| عارض آمن للعميل | `auto_client_acquisition/executive_command_center/customer_safe_renderer.py` |
| دفتر القيمة (تتبّع العائد) | `auto_client_acquisition/value_os/value_ledger.py` |
| التقرير الشهري للقيمة | `auto_client_acquisition/value_os/monthly_report.py` |
| حزمة الأدلة | `auto_client_acquisition/proof_os/proof_pack.py` |
| درجة الأدلة | `auto_client_acquisition/proof_os/proof_score.py` |
| البطاقة اليومية للمؤسس | `scripts/founder_daily_scorecard.py` |
| بطاقة وحدة الأعمال | `docs/scorecards/BUSINESS_UNIT_SCORECARD.md` |
| بطاقة المجموعة | `docs/scorecards/GROUP_SCORECARD.md` |
| البطاقة التشغيلية اليومية | `docs/ops/daily_scorecard.md` |

انظر أيضاً: `platform/executive_intelligence/readiness.md`، `platform/executive_intelligence/executive_metrics.md`، `platform/executive_intelligence/briefing_engine.md`.

---

# English

**Owner:** Executive Intelligence Layer Lead — Platform Engineering.

## Purpose

Layer 9 — Executive Intelligence — lifts Dealix from a "technology vendor" to a "strategic partner". The layer goal: when a leader opens the leadership dashboard, they see a clear business impact — where is revenue, where is waste, where is risk, where is the next improvement. This layer does not emit raw usage data; it converts that data into an impact narrative for every service, supported by evidence from workflows and from the value ledger.

## Components

- **Briefing Engine:** composes the weekly executive brief and the monthly board brief from lower layers. Built on the defensive aggregation pattern of `auto_client_acquisition/founder_v10/daily_brief.py` and the monthly cadence pattern of `auto_client_acquisition/value_os/monthly_report.py`.
- **ROI Dashboard:** an ROI story for every service — hours saved, qualified leads, friction removed — sourced from `auto_client_acquisition/value_os/value_ledger.py`.
- **Executive Command Center:** assembles the 15-panel view via `auto_client_acquisition/executive_command_center/builder.py` and renders it customer-safe via `customer_safe_renderer.py`.
- **Risk Reporting engine:** aggregates operational and compliance risk signals and surfaces visible bottlenecks, drawing on the risk register in `auto_client_acquisition/founder_v10/blockers.py`.
- **Forecasting engine:** projects trends from observed data only — no guaranteed promises, only a range and a confidence band.
- **Proof Engine:** ties every recommendation to evidence via `auto_client_acquisition/proof_os/proof_pack.py` and `proof_score.py`.

## Data flow

1. Lower layers publish events: value, friction, adoption, proof, cost.
2. The Briefing Engine reads aggregated events (counts and statuses only, no PII).
3. The ROI Dashboard converts events into a per-service impact narrative.
4. The Risk Reporting engine aggregates signals and ranks bottlenecks by impact.
5. The Forecasting engine projects trends with a stated range and confidence band.
6. The Executive Command Center assembles the view and emits the weekly brief automatically.
7. Every customer-facing report passes the customer-safe renderer and ends with the disclosure "Estimated value is not Verified value".

## Mapping to existing code

| Component | Real repo path |
|---|---|
| Daily brief aggregation (pattern) | `auto_client_acquisition/founder_v10/daily_brief.py` |
| Founder dashboard builder | `auto_client_acquisition/founder_v10/dashboard_builder.py` |
| Cost summary | `auto_client_acquisition/founder_v10/cost_summary.py` |
| Evidence summary | `auto_client_acquisition/founder_v10/evidence_summary.py` |
| Bottlenecks/blockers | `auto_client_acquisition/founder_v10/blockers.py` |
| Next actions | `auto_client_acquisition/founder_v10/next_actions.py` |
| Executive Command Center builder | `auto_client_acquisition/executive_command_center/builder.py` |
| Command Center panels | `auto_client_acquisition/executive_command_center/panels.py` |
| Next decisions | `auto_client_acquisition/executive_command_center/next_decisions.py` |
| Customer-safe renderer | `auto_client_acquisition/executive_command_center/customer_safe_renderer.py` |
| Value ledger (ROI tracking) | `auto_client_acquisition/value_os/value_ledger.py` |
| Monthly value report | `auto_client_acquisition/value_os/monthly_report.py` |
| Proof pack | `auto_client_acquisition/proof_os/proof_pack.py` |
| Proof score | `auto_client_acquisition/proof_os/proof_score.py` |
| Founder daily scorecard | `scripts/founder_daily_scorecard.py` |
| Business unit scorecard | `docs/scorecards/BUSINESS_UNIT_SCORECARD.md` |
| Group scorecard | `docs/scorecards/GROUP_SCORECARD.md` |
| Daily ops scorecard | `docs/ops/daily_scorecard.md` |

See also: `platform/executive_intelligence/readiness.md`, `platform/executive_intelligence/executive_metrics.md`, `platform/executive_intelligence/briefing_engine.md`.
