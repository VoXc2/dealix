# العربية

# تسليم Revenue OS — Layer 10 / مرحلة التنفيذ

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي ينفّذ Revenue Intelligence Sprint بسعر 499 ريال
**المراجع:** `docs/PILOT_DELIVERY_SOP.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `docs/COMPANY_SERVICE_LADDER.md` · `clients/_TEMPLATE/03_delivery_checklist.md` · `clients/_TEMPLATE/06_proof_pack.md`

> الغرض: تسليم Sprint الإيرادات لمدة 7 أيام بنفس الجودة لكل عميل. النتيجة Proof Pack حقيقي — لا وعود ولا أرقام مختلقة.

## 1. نطاق هذا الدليل

يغطي درجة Revenue Intelligence Sprint (499 ريال). المخرَج النهائي Proof Pack وفحص أهلية الاشتراك الشهري.

## 2. المراحل السبع للـ Sprint

1. **جواز المصدر (Source Passport):** وثّق مصدر كل ملف بيانات وحالته وتاريخه.
2. **درجة جودة البيانات (DQ score):** قيّم اكتمال البيانات ودقتها قبل أي تحليل.
3. **تقييم الحسابات (Account scoring):** رتّب الحسابات حسب الأولوية بمعايير معلنة.
4. **حزمة المسودات (Draft pack):** اكتب مسودات رسائل عربية تشبه صوت العميل — `draft_only`.
5. **مراجعة الحوكمة (Governance review):** افحص كل مخرَج ضد القواعد الحاكمة.
6. **تجميع Proof Pack:** اجمع المخرجات في حزمة إثبات من 4–6 صفحات.
7. **تسجيل الأصل الرأسمالي + فحص الأهلية:** سجّل الناتج كأصل وافحص أهلية الاشتراك الشهري.

## 3. خطوات التنفيذ اليومية

اتبع `docs/PILOT_DELIVERY_SOP.md` يوماً بيوم. كل يوم له مخرَج وحدث إثبات وقائمة جودة وموافقة عميل. لا تنتقل ليوم تالٍ قبل موافقة العميل على مخرَج اليوم السابق.

## 4. القواعد الحاكمة (Non-negotiables)

- كل مخرَج بحالة `draft_only` حتى موافقة العميل الصريحة.
- لا «نضمن مبيعات» — استخدم «فرص مُثبتة بأدلة».
- لا أرقام إيراد أو نسب تحويل كحقيقة — «تقديري» فقط.
- لا إرسال نيابة عن العميل — العميل هو المرسل دائماً.
- لا كشط ولا رسائل باردة ولا أتمتة LinkedIn.
- لا نشر اسم العميل دون إذن مكتوب.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] جواز المصدر مكتمل لكل ملف بيانات.
- [ ] درجة جودة البيانات محسوبة وموثقة.
- [ ] ≥ 3 فرص مُقيَّمة ومرتبطة بأدلة.
- [ ] ≥ 4 من 5 مسودات وافق عليها العميل.
- [ ] مراجعة الحوكمة تمّت دون مخالفات مفتوحة.
- [ ] Proof Pack (4–6 صفحات) مُسلَّم وموقّع.

## 6. المقاييس

- زمن التسليم: 7 أيام (الهدف: عدم التجاوز).
- معدل تأخير المشروع (الهدف ≤ 10%).
- نسبة المسودات الموافق عليها (الهدف ≥ 80%).
- رضا العميل (الهدف ≥ 4/5).
- أحداث إثبات موثقة (الهدف ≥ 3).

## 7. خطافات المراقبة (Observability)

- سجّل تقدّم كل يوم في `clients/<client>/03_delivery_checklist.md`.
- علّم حالة كل مخرَج: `draft` / `approved` / `delivered`.
- سجّل أحداث الإثبات في سجل الإثبات الداخلي.
- مراجعة أسبوعية لزمن التسليم ومعدل التأخير.

## 8. اتفاقية مستوى الخدمة (SLA)

- مدة الـ Sprint: 7 أيام عمل من اليوم 1.
- رد على ملاحظات العميل خلال 12 ساعة عمل.
- تسليم Proof Pack بنهاية اليوم 7.

## 9. إجراء التراجع (Rollback)

إذا اكتُشف خطأ في مخرَج مُسلَّم:
1. اسحب المخرَج وأبلغ العميل باحترام بنسخة مصححة خلال 24 ساعة.
2. لا تُجمّع Proof Pack بمخرَج معيب.
3. سجّل الحادثة في سجل الحوكمة وراجع السبب.
4. إذا تعذّر إكمال الشروط الإلزامية: اعرض تمديد 3 أيام دون رسوم، ولا upsell قبل الاكتمال.

# English

# Revenue OS Delivery — Layer 10 / Implementation Stage

**Owner:** Delivery Lead
**Audience:** Team member delivering the 499 SAR Revenue Intelligence Sprint
**References:** `docs/PILOT_DELIVERY_SOP.md` · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `docs/COMPANY_SERVICE_LADDER.md` · `clients/_TEMPLATE/03_delivery_checklist.md` · `clients/_TEMPLATE/06_proof_pack.md`

> Purpose: deliver the 7-day Revenue Sprint at the same quality for every client. The result is a real Proof Pack — no promises, no invented numbers.

## 1. Scope of this playbook

Covers the Revenue Intelligence Sprint rung (499 SAR). The final deliverable is a Proof Pack and a retainer eligibility check.

## 2. The seven Sprint stages

1. **Source Passport:** document the source, state, and date of each data file.
2. **DQ score:** assess data completeness and accuracy before any analysis.
3. **Account scoring:** rank accounts by priority using declared criteria.
4. **Draft pack:** write Arabic message drafts that match the client's voice — `draft_only`.
5. **Governance review:** check every deliverable against the governance rules.
6. **Proof Pack assembly:** gather deliverables into a 4–6 page evidence pack.
7. **Capital asset registration + eligibility check:** register the output as an asset and check retainer eligibility.

## 3. Daily execution steps

Follow `docs/PILOT_DELIVERY_SOP.md` day by day. Each day has a deliverable, a proof event, a quality checklist, and client approval. Do not move to the next day before the client approves the prior day's deliverable.

## 4. Governance rules (non-negotiables)

- Every deliverable is `draft_only` until explicit client approval.
- No "guaranteed sales" — use "evidenced opportunities".
- No revenue figures or conversion rates as fact — "estimated" only.
- No sending on the client's behalf — the client is always the sender.
- No scraping, no cold messaging, no LinkedIn automation.
- No publishing the client's name without written permission.

## 5. Acceptance criteria (readiness checklist)

- [ ] Source Passport complete for every data file.
- [ ] DQ score calculated and documented.
- [ ] ≥ 3 opportunities scored and evidence-linked.
- [ ] ≥ 4 of 5 drafts approved by the client.
- [ ] Governance review done with no open violations.
- [ ] Proof Pack (4–6 pages) delivered and signed.

## 6. Metrics

- Delivery time: 7 days (target: no overrun).
- Project delay rate (target ≤ 10%).
- Draft approval rate (target ≥ 80%).
- Client satisfaction (target ≥ 4/5).
- Documented proof events (target ≥ 3).

## 7. Observability hooks

- Log each day's progress in `clients/<client>/03_delivery_checklist.md`.
- Tag each deliverable state: `draft` / `approved` / `delivered`.
- Record proof events in the internal proof ledger.
- Weekly review of delivery time and delay rate.

## 8. Service-level agreement (SLA)

- Sprint duration: 7 working days from Day 1.
- Response to client feedback within 12 working hours.
- Proof Pack delivered by end of Day 7.

## 9. Rollback procedure

If an error is found in a delivered output:
1. Withdraw the output and respectfully send a corrected version within 24 hours.
2. Do not assemble the Proof Pack with a defective deliverable.
3. Record the incident in the governance log and review the cause.
4. If mandatory criteria cannot be completed: offer a 3-day extension at no charge, and no upsell before completion.
