# العربية

# تسليم Company Brain — Layer 10 / مرحلة التنفيذ

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يسلّم Data Pack بسعر 1,500 ريال
**المراجع:** `docs/COMPANY_SERVICE_LADDER.md` · `docs/PILOT_DELIVERY_SOP.md` · `clients/_TEMPLATE/05_report.md` · `clients/_TEMPLATE/AI_OPERATING_MODEL.md` · `playbooks/delivery/revenue_os_delivery.md`

> الغرض: تسليم Data Pack — حزمة ذاكرة منظَّمة لشركة العميل — بنفس الجودة لكل عميل. النتيجة مصدر حقيقة واحد موثَّق المصدر.

## 1. نطاق هذا الدليل

يغطي درجة Data Pack (1,500 ريال): تحويل بيانات العميل المبعثرة إلى حزمة منظَّمة قابلة للاستخدام في القرارات. لا تُعرَض هذه الدرجة قبل تسليم Sprint موافق عليه.

## 2. مكوّنات Data Pack

| المكوّن | الوصف |
|---|---|
| جواز المصدر | مصدر وحالة وتاريخ كل مجموعة بيانات |
| تقرير جودة البيانات | درجة الاكتمال والدقة والفجوات |
| نموذج البيانات المنظَّم | جداول موحَّدة بحقول معرَّفة |
| قاموس البيانات | تعريف كل حقل ومصدره |
| تقرير الأنماط | أنماط مجمَّعة بلا بيانات شخصية |

## 3. خطوات التسليم (خطوة بخطوة)

1. استلم بيانات العميل عبر `playbooks/onboarding/data_request.md`.
2. أنشئ جواز مصدر لكل مجموعة بيانات.
3. احسب درجة جودة البيانات ووثّق الفجوات.
4. وحّد البيانات في نموذج منظَّم بحقول ثابتة.
5. اكتب قاموس بيانات يربط كل حقل بمصدره.
6. استخرج أنماطاً مجمَّعة — دون أي بيانات شخصية.
7. اعرض الحزمة على العميل واحصل على موافقته.

## 4. القواعد الحاكمة (Non-negotiables)

- لا كشط ولا بيانات من مصادر خارجية — العميل وحده المصدر.
- لا بيانات شخصية في تقرير الأنماط — أنماط مجمَّعة فقط.
- كل حقل في القاموس له مصدر موثَّق — لا تخمين.
- المخرَج بحالة `draft_only` حتى موافقة العميل.
- لا أرقام أداء كحقيقة — «تقديري» أو «نمط آمن للحالة».

## 5. معايير القبول (قائمة الجاهزية)

- [ ] جواز مصدر مكتمل لكل مجموعة بيانات.
- [ ] درجة جودة البيانات محسوبة وموثقة.
- [ ] نموذج البيانات موحَّد وقابل للاستخدام.
- [ ] قاموس البيانات يغطي كل حقل بمصدره.
- [ ] تقرير الأنماط خالٍ من البيانات الشخصية.
- [ ] العميل وافق كتابياً على الحزمة.

## 6. المقاييس

- زمن التسليم: من استلام البيانات إلى التسليم (الهدف معروف ومُعلَن مسبقاً).
- معدل تأخير المشروع (الهدف ≤ 10%).
- نسبة الحقول الموثَّقة المصدر (الهدف 100%).
- رضا العميل (الهدف ≥ 4/5).

## 7. خطافات المراقبة (Observability)

- سجّل تقدّم التسليم في `clients/<client>/05_report.md`.
- علّم حالة كل مكوّن: `draft` / `approved` / `delivered`.
- مراجعة أسبوعية لزمن التسليم ومعدل التأخير.

## 8. اتفاقية مستوى الخدمة (SLA)

- زمن التسليم المُعلَن: يُحدَّد عند العرض ويُلتزَم به.
- رد على ملاحظات العميل خلال 24 ساعة عمل.
- نسخة مصححة لأي خطأ خلال 24 ساعة من اكتشافه.

## 9. إجراء التراجع (Rollback)

إذا اكتُشفت بيانات شخصية في تقرير الأنماط أو حقل بلا مصدر:
1. اسحب المكوّن المعيب فوراً.
2. صحّحه وأعد تسليمه خلال 24 ساعة.
3. سجّل الحادثة في سجل الحوكمة وراجع السبب قبل العميل التالي.

# English

# Company Brain Delivery — Layer 10 / Implementation Stage

**Owner:** Delivery Lead
**Audience:** Team member delivering the 1,500 SAR Data Pack
**References:** `docs/COMPANY_SERVICE_LADDER.md` · `docs/PILOT_DELIVERY_SOP.md` · `clients/_TEMPLATE/05_report.md` · `clients/_TEMPLATE/AI_OPERATING_MODEL.md` · `playbooks/delivery/revenue_os_delivery.md`

> Purpose: deliver the Data Pack — a structured memory pack for the client's company — at the same quality for every client. The result is a single, source-documented source of truth.

## 1. Scope of this playbook

Covers the Data Pack rung (1,500 SAR): turning the client's scattered data into a structured pack usable for decisions. This rung is not offered before an approved Sprint has shipped.

## 2. Data Pack components

| Component | Description |
|---|---|
| Source Passport | Source, state, and date of each dataset |
| Data quality report | Completeness, accuracy, and gap scores |
| Structured data model | Standardized tables with defined fields |
| Data dictionary | Definition and source of each field |
| Pattern report | Aggregated patterns with no PII |

## 3. Delivery steps (step by step)

1. Receive client data via `playbooks/onboarding/data_request.md`.
2. Create a Source Passport for each dataset.
3. Calculate the data quality score and document gaps.
4. Standardize the data into a structured model with fixed fields.
5. Write a data dictionary linking each field to its source.
6. Extract aggregated patterns — with no PII.
7. Review the pack with the client and obtain approval.

## 4. Governance rules (non-negotiables)

- No scraping and no external-source data — the client is the only source.
- No PII in the pattern report — aggregated patterns only.
- Every dictionary field has a documented source — no guessing.
- The output is `draft_only` until client approval.
- No performance figures as fact — "estimated" or "case-safe pattern".

## 5. Acceptance criteria (readiness checklist)

- [ ] Source Passport complete for every dataset.
- [ ] Data quality score calculated and documented.
- [ ] Data model standardized and usable.
- [ ] Data dictionary covers every field with its source.
- [ ] Pattern report free of PII.
- [ ] Client approved the pack in writing.

## 6. Metrics

- Delivery time: data receipt to delivery (target known and declared in advance).
- Project delay rate (target ≤ 10%).
- Share of source-documented fields (target 100%).
- Client satisfaction (target ≥ 4/5).

## 7. Observability hooks

- Log delivery progress in `clients/<client>/05_report.md`.
- Tag each component state: `draft` / `approved` / `delivered`.
- Weekly review of delivery time and delay rate.

## 8. Service-level agreement (SLA)

- Declared delivery time: set at offer and honored.
- Response to client feedback within 24 working hours.
- Corrected version for any error within 24 hours of discovery.

## 9. Rollback procedure

If PII is found in the pattern report or a field has no source:
1. Withdraw the defective component immediately.
2. Correct it and redeliver within 24 hours.
3. Record the incident in the governance log and review the cause before the next client.
