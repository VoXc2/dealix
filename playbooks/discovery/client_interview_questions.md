# العربية

# أسئلة مقابلة العميل — Layer 10 / مرحلة الاكتشاف

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** أي عضو في الفريق يجري مكالمة اكتشاف أولى (30 دقيقة)
**المراجع:** `playbooks/discovery/ai_opportunity_audit.md` · `clients/_TEMPLATE/01_intake.md` · `docs/COMPANY_SERVICE_LADDER.md`

> الغرض: مجموعة أسئلة موحّدة بحيث يحصل كل عميل على نفس جودة الاكتشاف. الأسئلة مصمَّمة لتغذية تدقيق الفرص مباشرة.

## 1. قبل المكالمة

- راجع موقع العميل أو ملفه العام لمدة 5 دقائق.
- اطلب من العميل تخصيص 30 دقيقة دون مقاطعة.
- وضّح أن المكالمة استكشافية ولا تُسجَّل دون إذن.

## 2. الأسئلة الستة الأساسية (هيكل ثابت)

1. **الإيراد:** ما المصدر الأساسي لإيراد شركتك اليوم؟
2. **العميل المثالي:** من هو العميل المثالي لك (القطاع، الحجم، المنطقة)؟
3. **خط الأنابيب:** صف خط الأنابيب الحالي — كم مرحلة، وأين يتعطل؟
4. **الوقت الضائع:** ما العمل المتكرر الذي يستهلك وقت فريقك أسبوعياً؟
5. **القرار:** ما القرار الذي تتمنى لو كانت لديك بيانات أفضل لاتخاذه؟
6. **النجاح:** كيف يبدو النجاح بعد 30 يوماً من العمل معنا؟

## 3. أسئلة متابعة (اختيارية حسب السياق)

- ما الأدوات التي تستخدمها لإدارة العملاء حالياً؟
- من يملك قرار الشراء في شركتك؟
- ما الذي جرّبته سابقاً ولم ينجح؟

## 4. القواعد الحاكمة

- لا تطلب بيانات شخصية أو أرقام تواصل في المكالمة الأولى.
- لا تَعِد بنتيجة أو رقم — المكالمة للاستماع فقط.
- لا تقترح خدمة قبل اكتمال تدقيق الفرص.
- لا تذكر الكشط أو الرسائل الباردة كحلول.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] الأسئلة الستة كلها طُرحت ودُوّنت إجاباتها.
- [ ] سياق العميل واضح بما يكفي لكتابة فقرة تأطير.
- [ ] حُدّدت 3 نقاط ألم على الأقل.
- [ ] الملاحظات محفوظة بصيغة خالية من البيانات الشخصية.

## 6. المقاييس

- زمن المكالمة (الهدف ≤ 30 دقيقة).
- اكتمال الأسئلة: نسبة الأسئلة الستة المُجابة.
- معدل التحول إلى تشخيص: نسبة المكالمات التي تنتهي بتدقيق فرص.

## 7. خطافات المراقبة

- سجّل كل مكالمة اكتشاف في سجل الاكتشاف الداخلي.
- علّم النتيجة: `discovery_complete` / `not_a_fit` / `follow_up`.

## 8. إجراء التراجع

إذا تبيّن أن المكالمة لم تجمع سياقاً كافياً:
1. أعِد جدولة 15 دقيقة لاستكمال الأسئلة الناقصة.
2. لا تبدأ تدقيق الفرص بمعلومات ناقصة.
3. سجّل سبب النقص لتحسين قالب الأسئلة.

# English

# Client Interview Questions — Layer 10 / Discovery Stage

**Owner:** Delivery Lead
**Audience:** Any team member running a first 30-minute discovery call
**References:** `playbooks/discovery/ai_opportunity_audit.md` · `clients/_TEMPLATE/01_intake.md` · `docs/COMPANY_SERVICE_LADDER.md`

> Purpose: a standard question set so every client gets the same discovery quality. The questions are designed to feed the opportunity audit directly.

## 1. Before the call

- Spend 5 minutes reviewing the client's website or public profile.
- Ask the client to set aside 30 uninterrupted minutes.
- Clarify the call is exploratory and not recorded without permission.

## 2. The six core questions (fixed structure)

1. **Revenue:** what is your company's primary revenue source today?
2. **Ideal client:** who is your ideal client (sector, size, region)?
3. **Pipeline:** describe your current pipeline — how many stages, and where does it stall?
4. **Lost time:** what repetitive work consumes your team's time each week?
5. **Decision:** which decision do you wish you had better data to make?
6. **Success:** what does success look like 30 days after working with us?

## 3. Follow-up questions (optional, context-dependent)

- What tools do you use to manage clients today?
- Who owns the buying decision in your company?
- What have you tried before that did not work?

## 4. Governance rules

- Do not request PII or contact numbers in the first call.
- Do not promise an outcome or number — the call is for listening only.
- Do not propose a service before the opportunity audit is complete.
- Do not mention scraping or cold messaging as solutions.

## 5. Acceptance criteria (readiness checklist)

- [ ] All six questions asked and answers recorded.
- [ ] Client context clear enough to write a framing paragraph.
- [ ] At least 3 pain points identified.
- [ ] Notes saved in a PII-free form.

## 6. Metrics

- Call duration (target ≤ 30 minutes).
- Question completeness: share of the six questions answered.
- Conversion to diagnostic: share of calls that end in an opportunity audit.

## 7. Observability hooks

- Log every discovery call in the internal discovery log.
- Tag the outcome: `discovery_complete` / `not_a_fit` / `follow_up`.

## 8. Rollback procedure

If the call did not gather enough context:
1. Reschedule 15 minutes to complete the missing questions.
2. Do not start the opportunity audit with incomplete information.
3. Record the cause of the gap to improve the question template.
