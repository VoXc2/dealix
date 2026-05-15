# العربية

# تدقيق فرص الذكاء الاصطناعي — Layer 10 / مرحلة الاكتشاف

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** فريق Dealix الذي يجري تشخيصاً مع عميل محتمل
**المراجع:** `docs/PILOT_DELIVERY_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md` (الدرجة 0: التشخيص المجاني) · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `clients/_TEMPLATE/01_intake.md`

> الغرض: أي عضو في الفريق يستطيع إجراء تدقيق فرص خلال 48 ساعة دون اعتماد على المؤسس. النتيجة قائمة فرص واقعية مرتبطة بأدلة من بيانات العميل — لا وعود ولا أرقام مختلقة.

## 1. متى يُستخدم هذا الدليل

يُستخدم في الدرجة 0 من سُلَّم الخدمات (التشخيص المجاني) وقبل عرض درجة Revenue Intelligence Sprint بسعر 499 ريال. هو الخطوة التي تربط الاكتشاف بالعرض.

## 2. المدخلات المطلوبة قبل البدء

- إجابات العميل على أسئلة التشخيص الستة (راجع `playbooks/discovery/client_interview_questions.md`).
- وصف القطاع والمنطقة والحجم التقريبي للشركة.
- وصف نصي لحالة pipeline الحالية (بصيغة عامة، دون بيانات شخصية).
- لا تُطلب ملفات بيانات في هذه المرحلة — التشخيص يعتمد على المقابلة فقط.

## 3. خطوات التدقيق (خطوة بخطوة)

1. **تأطير السياق:** اكتب فقرة واحدة تصف عمل العميل ومصدر إيراده الأساسي.
2. **خريطة القيمة:** حدد المراحل الثلاث الأكبر التي يضيع فيها الوقت أو الفرص.
3. **تحديد الفرص:** لكل مرحلة، اكتب فرصة واحدة قابلة للتنفيذ — ماذا يمكن تحسينه ولماذا الآن.
4. **ربط الدليل:** لكل فرصة، اذكر المصدر من كلام العميل (اقتباس أو ملاحظة). الفرصة بلا دليل تُحذف.
5. **تقدير الحجم:** صنّف كل فرصة (أثر مرتفع/متوسط/منخفض) دون ذكر رقم إيراد مؤكد.
6. **توصية الخدمة:** اربط الفرص بدرجة واحدة فقط من سُلَّم الخدمات.
7. **صياغة المخرَج:** صفحة واحدة ثنائية اللغة — 3 فرص + خطر واحد + مسودة رسالة واحدة + توصية.

## 4. القواعد الحاكمة (Non-negotiables)

- لا أرقام إيراد أو نسب تحويل مؤكدة — استخدم «تقديري» أو «نمط آمن للحالة».
- لا ذكر للكشط (scraping) أو الرسائل الباردة أو أتمتة LinkedIn كخدمات.
- لا أسماء عملاء حقيقية في أي ملف داخل المستودع.
- كل مخرَج بحالة `draft_only` حتى موافقة العميل.
- التشخيص يعكس سياق العميل الفعلي — لا نسخة عامة معاد استخدامها.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] التشخيص مُسلَّم خلال 48 ساعة من المقابلة.
- [ ] كل فرصة مرتبطة باقتباس أو ملاحظة من العميل.
- [ ] خطر واحد موثق على الأقل.
- [ ] توصية خدمة واحدة فقط (لا قفز فوق درجات السُلَّم).
- [ ] الصفحة ثنائية اللغة ومتطابقة الطول.

## 6. المقاييس

- زمن التشخيص: من المقابلة إلى التسليم (الهدف ≤ 48 ساعة).
- معدل قبول التشخيص: نسبة العملاء الذين يقبلون عرض الدرجة التالية.
- جودة الدليل: نسبة الفرص المرتبطة بمصدر موثق (الهدف 100%).

## 7. خطافات المراقبة (Observability)

- سجّل كل تشخيص في سجل الاكتشاف الداخلي (تاريخ، قطاع، نتيجة).
- علّم حالة المخرَج: `draft_delivered` / `accepted` / `declined`.
- راجعة أسبوعية: عدد التشخيصات وزمنها ومعدل القبول.

## 8. إجراء التراجع (Rollback)

إذا اكتُشف أن تشخيصاً يحتوي رقماً غير مدعوم بدليل أو نسخة عامة:
1. سحب المخرَج وإبلاغ العميل باحترام بنسخة مصححة خلال 24 ساعة.
2. تسجيل الحادثة في سجل الحوكمة.
3. مراجعة سبب الخلل قبل التشخيص التالي.

# English

# AI Opportunity Audit — Layer 10 / Discovery Stage

**Owner:** Delivery Lead
**Audience:** Dealix team member running a diagnostic with a prospective client
**References:** `docs/PILOT_DELIVERY_SOP.md` · `docs/COMPANY_SERVICE_LADDER.md` (Rung 0: Free Diagnostic) · `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md` · `clients/_TEMPLATE/01_intake.md`

> Purpose: any team member can run an opportunity audit within 48 hours without depending on the founder. The output is a realistic, evidence-linked opportunity list — no promises, no invented numbers.

## 1. When to use this playbook

Use it at Rung 0 of the service ladder (Free Diagnostic) and before offering the 499 SAR Revenue Intelligence Sprint. It is the step that bridges discovery to offer.

## 2. Inputs required before starting

- Client answers to the six diagnostic questions (see `playbooks/discovery/client_interview_questions.md`).
- Sector, region, and approximate company size.
- A text description of the current pipeline state (generic form, no PII).
- No data files are requested at this stage — the diagnostic relies on the interview only.

## 3. Audit steps (step by step)

1. **Frame the context:** write one paragraph describing the client's business and primary revenue source.
2. **Value map:** identify the three stages where the most time or opportunity is lost.
3. **Identify opportunities:** for each stage, write one actionable opportunity — what can improve and why now.
4. **Link the evidence:** for each opportunity, cite the source from the client's own words. An opportunity with no evidence is deleted.
5. **Estimate size:** classify each opportunity (high/medium/low impact) without stating a confirmed revenue figure.
6. **Service recommendation:** map the opportunities to exactly one rung of the service ladder.
7. **Draft the output:** a single bilingual page — 3 opportunities + 1 risk + 1 message draft + recommendation.

## 4. Governance rules (non-negotiables)

- No confirmed revenue figures or conversion rates — use "estimated" or "case-safe pattern".
- No scraping, cold messaging, or LinkedIn automation described as a service.
- No real client names in any file inside the repository.
- Every output is `draft_only` until client approval.
- The diagnostic reflects the client's actual context — never a reused generic copy.

## 5. Acceptance criteria (readiness checklist)

- [ ] Diagnostic delivered within 48 hours of the interview.
- [ ] Every opportunity linked to a client quote or note.
- [ ] At least one documented risk.
- [ ] Exactly one service recommendation (no ladder skipping).
- [ ] Page is bilingual and length-matched.

## 6. Metrics

- Diagnostic time: interview to delivery (target ≤ 48 hours).
- Diagnostic acceptance rate: share of clients who accept the next-rung offer.
- Evidence quality: share of opportunities linked to a documented source (target 100%).

## 7. Observability hooks

- Log every diagnostic in the internal discovery log (date, sector, outcome).
- Tag output state: `draft_delivered` / `accepted` / `declined`.
- Weekly review: count of diagnostics, their time, and acceptance rate.

## 8. Rollback procedure

If a diagnostic is found to contain an unsupported figure or a generic copy:
1. Withdraw the output and respectfully send the client a corrected version within 24 hours.
2. Record the incident in the governance log.
3. Review the root cause before the next diagnostic.
