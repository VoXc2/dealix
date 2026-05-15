# العربية

# تسليم Operations OS — Layer 10 / مرحلة التنفيذ

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يدير اشتراك Managed Ops الشهري (2,999–4,999 ريال/شهر)
**المراجع:** `docs/COMPANY_SERVICE_LADDER.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `clients/_TEMPLATE/OPERATING_CADENCE.md` · `clients/_TEMPLATE/DELIVERY_COMMAND.md` · `playbooks/monthly_optimization/monthly_review.md`

> الغرض: تشغيل اشتراك Managed Ops الشهري بإيقاع ثابت — حتى يحصل العميل على نفس جودة التشغيل كل أسبوع دون اعتماد على شخص واحد.

## 1. نطاق هذا الدليل

يغطي درجة Managed Ops (2,999–4,999 ريال/شهر): طبقة تشغيل شهرية متكررة. لا تُعرَض قبل Proof Pack موافق عليه من درجة الـ Sprint.

## 2. الإيقاع الأسبوعي الثابت

| اليوم | النشاط | المخرَج |
|---|---|---|
| الأحد | تقرير تنفيذي أسبوعي | حزمة تنفيذية |
| الإثنين | مراجعة فرص النمو | قائمة فرص محدَّثة |
| الثلاثاء | حزمة مسودات مبيعات | مسودات `draft_only` |
| الأربعاء | مراجعة الدعم والتسليم | تحديث الحالة |
| الخميس | مراجعة الجودة والحوكمة | فحص المخالفات |

## 3. خطوات التشغيل (دورة شهرية)

1. ثبّت الإيقاع الأسبوعي مع العميل من `clients/_TEMPLATE/OPERATING_CADENCE.md`.
2. سلّم حزمة تنفيذية كل أحد (راجع `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` القسم 2).
3. حدّث قائمة الفرص أسبوعياً بأدلة محدَّثة.
4. اكتب مسودات مبيعات أسبوعية — كلها `draft_only`.
5. أجرِ مراجعة جودة وحوكمة أسبوعية.
6. نفّذ المراجعة الشهرية عبر `playbooks/monthly_optimization/monthly_review.md`.
7. افحص إشارات التجديد والمخاطر كل أسبوع.

## 4. القواعد الحاكمة (Non-negotiables)

- كل مسودة بحالة `draft_only` — العميل يوافق قبل أي استخدام.
- لا إرسال نيابة عن العميل — العميل هو المرسل دائماً.
- لا «نضمن» نتائج شهرية — «فرص مُثبتة بأدلة».
- لا كشط ولا رسائل باردة ولا أتمتة LinkedIn.
- لا أرقام أداء كحقيقة — «تقديري» فقط.
- لا upsell لدرجة أعلى دون 3 أشهر تشغيل متواصل.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] إيقاع أسبوعي ثابت متّفق عليه وموثَّق.
- [ ] حزمة تنفيذية مُسلَّمة كل أحد دون انقطاع.
- [ ] ≥ 15 من 20 مسودة شهرية وافق عليها العميل.
- [ ] مراجعة جودة وحوكمة أسبوعية تمّت.
- [ ] مراجعة شهرية تمّت وموثَّقة.
- [ ] إشارات التجديد فُحصت أسبوعياً.

## 6. المقاييس

- التزام الإيقاع: نسبة الحزم الأسبوعية المُسلَّمة في موعدها.
- نسبة المسودات الموافق عليها (الهدف ≥ 75%).
- معدل تأخير المشروع (الهدف ≤ 10%).
- رضا العميل الشهري (الهدف ≥ 4/5).
- أحداث إثبات شهرية موثقة (الهدف ≥ 5).

## 7. خطافات المراقبة (Observability)

- سجّل كل دورة أسبوعية في `clients/<client>/DELIVERY_COMMAND.md`.
- علّم حالة الحزمة: `delivered_on_time` / `delivered_late` / `missed`.
- سجّل أحداث الإثبات الشهرية في سجل الإثبات.
- مراجعة أسبوعية للالتزام بالإيقاع وإشارات المخاطر.

## 8. اتفاقية مستوى الخدمة (SLA)

- حزمة تنفيذية كل أحد دون استثناء.
- رد على ملاحظات العميل خلال 24 ساعة عمل (وفق SLA الدعم).
- مراجعة شهرية مجدولة قبل تجديد الاشتراك.

## 9. إجراء التراجع (Rollback)

إذا فاتت حزمة أسبوعية أو ظهرت مخالفة حوكمة:
1. أبلغ العميل باحترام وسلّم الحزمة خلال 24 ساعة.
2. سجّل الحادثة في سجل الحوكمة.
3. عند تكرار التأخر، نفّذ مراجعة سبب جذري قبل الأسبوع التالي.
4. إذا طلب العميل تجميداً، عالجه بإجراء الإنهاء المحترم في `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`.

# English

# Operations OS Delivery — Layer 10 / Implementation Stage

**Owner:** Delivery Lead
**Audience:** Team member running the monthly Managed Ops engagement (2,999–4,999 SAR/mo)
**References:** `docs/COMPANY_SERVICE_LADDER.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `clients/_TEMPLATE/OPERATING_CADENCE.md` · `clients/_TEMPLATE/DELIVERY_COMMAND.md` · `playbooks/monthly_optimization/monthly_review.md`

> Purpose: run the monthly Managed Ops engagement on a fixed cadence — so the client gets the same operating quality every week without depending on one person.

## 1. Scope of this playbook

Covers the Managed Ops rung (2,999–4,999 SAR/mo): a recurring monthly operating layer. Not offered before an approved Proof Pack from the Sprint rung.

## 2. The fixed weekly cadence

| Day | Activity | Deliverable |
|---|---|---|
| Sunday | Weekly executive brief | Executive pack |
| Monday | Growth opportunity review | Updated opportunity list |
| Tuesday | Sales draft pack | `draft_only` drafts |
| Wednesday | Support and delivery review | Status update |
| Thursday | QA and governance review | Violation check |

## 3. Operating steps (monthly cycle)

1. Fix the weekly cadence with the client from `clients/_TEMPLATE/OPERATING_CADENCE.md`.
2. Deliver an executive pack every Sunday (see `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` Section 2).
3. Update the opportunity list weekly with fresh evidence.
4. Write weekly sales drafts — all `draft_only`.
5. Run a weekly QA and governance review.
6. Run the monthly review via `playbooks/monthly_optimization/monthly_review.md`.
7. Check renewal and risk signals every week.

## 4. Governance rules (non-negotiables)

- Every draft is `draft_only` — the client approves before any use.
- No sending on the client's behalf — the client is always the sender.
- No "guaranteed" monthly results — "evidenced opportunities".
- No scraping, no cold messaging, no LinkedIn automation.
- No performance figures as fact — "estimated" only.
- No upsell to a higher rung without 3 consecutive months of operation.

## 5. Acceptance criteria (readiness checklist)

- [ ] Fixed weekly cadence agreed and documented.
- [ ] Executive pack delivered every Sunday without a gap.
- [ ] ≥ 15 of 20 monthly drafts approved by the client.
- [ ] Weekly QA and governance review completed.
- [ ] Monthly review completed and documented.
- [ ] Renewal signals checked weekly.

## 6. Metrics

- Cadence adherence: share of weekly packs delivered on time.
- Draft approval rate (target ≥ 75%).
- Project delay rate (target ≤ 10%).
- Monthly client satisfaction (target ≥ 4/5).
- Documented monthly proof events (target ≥ 5).

## 7. Observability hooks

- Log each weekly cycle in `clients/<client>/DELIVERY_COMMAND.md`.
- Tag pack state: `delivered_on_time` / `delivered_late` / `missed`.
- Record monthly proof events in the proof ledger.
- Weekly review of cadence adherence and risk signals.

## 8. Service-level agreement (SLA)

- Executive pack every Sunday without exception.
- Response to client feedback within 24 working hours (per the support SLA).
- Monthly review scheduled before subscription renewal.

## 9. Rollback procedure

If a weekly pack is missed or a governance violation appears:
1. Respectfully inform the client and deliver the pack within 24 hours.
2. Record the incident in the governance log.
3. On repeated lateness, run a root-cause review before the next week.
4. If the client requests a freeze, handle it with the graceful offboarding process in `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`.
