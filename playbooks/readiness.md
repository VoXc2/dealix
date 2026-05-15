# العربية

# جاهزية Layer 10 — تسليم العميل

**Owner:** قائد التسليم (Delivery Lead)

**الجمهور:** قيادة Dealix وفريق التسليم والجودة ونجاح العملاء
**المراجع:** `docs/PILOT_DELIVERY_SOP.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `docs/CUSTOMER_SUCCESS_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `docs/scorecards/CLIENT_SCORECARD.md` · `docs/scorecards/PROJECT_SCORECARD.md` · `playbooks/tests.md`

> هدف Layer 10: تسليم نفس الجودة لكل عميل عبر أدلة عمل (playbooks) — حتى لا تكون Dealix «مشروعاً معتمداً على المؤسس». أي عضو في الفريق يستطيع التسليم من دليل.

## 1. قائمة الجاهزية (Readiness Checklist)

- [ ] كل مرحلة في رحلة العميل لها دليل عمل: اكتشاف، تهيئة، تنفيذ، جودة، تدريب، تسليم، تحسين شهري.
- [ ] أي عضو في الفريق يستطيع التسليم من الدليل دون اعتماد على المؤسس.
- [ ] كل عميل لديه معايير قبول موثَّقة (`playbooks/qa/client_acceptance_tests.md`).
- [ ] كل إطلاق له قائمة فحص (`playbooks/qa/pre_launch_checklist.md`).
- [ ] مراجعة شهرية موجودة وتُجرى لكل عميل اشتراك.
- [ ] كل خدمة على سُلَّم الخدمات لها SLA معلَن.
- [ ] زمن التهيئة معروف وموثَّق.
- [ ] زمن التسليم معروف لكل درجة خدمة.
- [ ] معدل تأخير المشروع متتبَّع ومنخفض.
- [ ] كل عميل لديه مقاييس نجاح موثَّقة.
- [ ] كل دليل عمل ثنائي اللغة ويحترم القواعد غير القابلة للتفاوض الإحدى عشرة.

## 2. المقاييس (Metrics)

| المقياس | الهدف |
|---|---|
| تغطية أدلة العمل للمراحل | 100% من مراحل رحلة العميل |
| زمن التهيئة (دفع → Kick-off) | ≤ 24 ساعة |
| زمن تسليم Sprint | 7 أيام عمل |
| معدل تأخير المشروع | ≤ 10% |
| معدل اجتياز الجودة من المحاولة الأولى | ≥ 90% |
| معدل قبول العميل من المحاولة الأولى | ≥ 85% |
| التزام SLA الدعم (الإقرار) | ≥ 95% |
| نسبة العملاء بمقاييس نجاح موثَّقة | 100% |
| رضا العميل | ≥ 4/5 |

## 3. خطافات المراقبة (Observability Hooks)

- سجّل تقدّم كل ارتباط في `clients/<client>/03_delivery_checklist.md` و`DELIVERY_COMMAND.md`.
- علّم حالة كل مخرَج: `draft` / `approved` / `delivered` / `accepted`.
- سجّل أحداث الإثبات في سجل الإثبات الداخلي.
- حدّث `docs/scorecards/CLIENT_SCORECARD.md` و`PROJECT_SCORECARD.md` عند كل قبول.
- مراجعة أسبوعية لزمن التسليم ومعدل التأخير والتزام SLA.

## 4. قواعد الحوكمة (Governance Rules)

- لا إثبات مختلق — كل قيمة مدعومة بدليل من سجل الإثبات.
- لا ضمان مبيعات أو نسب تحويل — «فرص مُثبتة بأدلة» و«تقديري».
- لا كشط ولا رسائل WhatsApp باردة ولا أتمتة LinkedIn.
- كل إجراء يخص العميل قائم على الموافقة المسبقة / مسودة فقط.
- Dealix لا يرسل رسائل خارجية نيابة عن العميل دون موافقة صريحة.
- لا بيانات شخصية ولا أسماء عملاء حقيقية في ملفات المستودع.
- لا قفز فوق درجات سُلَّم الخدمات.

## 5. إجراء التراجع (Rollback Procedure)

إذا فشل تسليم أو خالف دليلٌ القواعد:
1. أوقف التسليم المتأثر وأبلغ العميل باحترام خلال 24 ساعة.
2. سلّم نسخة مصححة وفق إجراء التراجع في الدليل المعني.
3. سجّل الحادثة في سجل الحوكمة.
4. أضف بنداً إلى `playbooks/monthly_optimization/improvement_backlog.md` لمنع التكرار.
5. لا upsell ولا انتقال لمرحلة تالية قبل إغلاق السبب الجذري.

## 6. درجة الجاهزية الحالية (Current Readiness Score)

**الدرجة: 78 / 100 — تجريبي مع العميل (Client Pilot)**

سلّم النطاقات الخمس:
- 0–59: نموذج أولي (prototype)
- 60–74: تجريبي داخلي (internal beta)
- 75–84: تجريبي مع العميل (client pilot)
- 85–94: جاهز للمؤسسات (enterprise-ready)
- 95+: حرج للمهام (mission-critical)

**سبب الدرجة:** أدلة العمل تغطي كل مراحل رحلة العميل بقواعد قبول وSLA وخطافات مراقبة. الرفع إلى «جاهز للمؤسسات» يتطلب بيانات تشغيلية من عدة عملاء تثبت ثبات معدل التأخير ومعدلات الاجتياز عبر فريق غير المؤسس.

# English

# Layer 10 Readiness — Client Delivery

**Owner:** Delivery Lead

**Audience:** Dealix leadership and the delivery, QA, and customer success teams
**References:** `docs/PILOT_DELIVERY_SOP.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `docs/CUSTOMER_SUCCESS_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `docs/scorecards/CLIENT_SCORECARD.md` · `docs/scorecards/PROJECT_SCORECARD.md` · `playbooks/tests.md`

> Layer 10 goal: deliver the same quality to every client through playbooks — so Dealix is not "a founder-dependent project". Any team member can deliver from a playbook.

## 1. Readiness Checklist

- [ ] Every stage of the client journey has a playbook: discovery, onboarding, implementation, QA, training, handover, monthly optimization.
- [ ] Any team member can deliver from the playbook without depending on the founder.
- [ ] Every client has documented acceptance criteria (`playbooks/qa/client_acceptance_tests.md`).
- [ ] Every launch has a checklist (`playbooks/qa/pre_launch_checklist.md`).
- [ ] A monthly review exists and is run for every subscription client.
- [ ] Every service on the service ladder has a declared SLA.
- [ ] Onboarding time is known and documented.
- [ ] Delivery time is known for every service rung.
- [ ] Project delay rate is tracked and low.
- [ ] Every client has documented success metrics.
- [ ] Every playbook is bilingual and honors the eleven non-negotiables.

## 2. Metrics

| Metric | Target |
|---|---|
| Playbook coverage of journey stages | 100% of client journey stages |
| Onboarding time (payment → Kick-off) | ≤ 24 hours |
| Sprint delivery time | 7 working days |
| Project delay rate | ≤ 10% |
| First-pass QA pass rate | ≥ 90% |
| First-pass client acceptance rate | ≥ 85% |
| Support SLA adherence (acknowledgement) | ≥ 95% |
| Share of clients with documented success metrics | 100% |
| Client satisfaction | ≥ 4/5 |

## 3. Observability Hooks

- Log each engagement's progress in `clients/<client>/03_delivery_checklist.md` and `DELIVERY_COMMAND.md`.
- Tag each deliverable state: `draft` / `approved` / `delivered` / `accepted`.
- Record proof events in the internal proof ledger.
- Update `docs/scorecards/CLIENT_SCORECARD.md` and `PROJECT_SCORECARD.md` on every acceptance.
- Weekly review of delivery time, delay rate, and SLA adherence.

## 4. Governance Rules

- No fake proof — every value is backed by evidence from the proof ledger.
- No guaranteed sales or conversion rates — "evidenced opportunities" and "estimated".
- No scraping, no cold WhatsApp, no LinkedIn automation.
- Every client-facing action is approval-first / draft-only.
- Dealix does not send external messages on the client's behalf without explicit approval.
- No PII and no real client names in repository files.
- No skipping rungs of the service ladder.

## 5. Rollback Procedure

If a delivery fails or a playbook breaches the rules:
1. Stop the affected delivery and respectfully inform the client within 24 hours.
2. Deliver a corrected version per the rollback procedure in the relevant playbook.
3. Record the incident in the governance log.
4. Add an item to `playbooks/monthly_optimization/improvement_backlog.md` to prevent recurrence.
5. No upsell and no move to a next stage before the root cause is closed.

## 6. Current Readiness Score

**Score: 78 / 100 — Client Pilot**

The five-band scale:
- 0–59: prototype
- 60–74: internal beta
- 75–84: client pilot
- 85–94: enterprise-ready
- 95+: mission-critical

**Reason for the score:** the playbooks cover every stage of the client journey with acceptance criteria, SLAs, and observability hooks. Raising to "enterprise-ready" requires operational data from multiple clients proving a stable delay rate and pass rates across a non-founder team.
