# العربية

# رسم الوضع الحالي — Layer 10 / مرحلة الاكتشاف

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يوثّق عمليات العميل قبل العرض
**المراجع:** `playbooks/discovery/client_interview_questions.md` · `playbooks/discovery/ai_opportunity_audit.md` · `clients/_TEMPLATE/00_scope.md` · `clients/_TEMPLATE/01_intake.md`

> الغرض: تحويل مخرجات المقابلة إلى خريطة منظَّمة للوضع الحالي تجعل الفجوات مرئية. الخريطة هي الأساس الذي يبني عليه تدقيق الفرص.

## 1. متى يُستخدم هذا الدليل

بعد مكالمة الاكتشاف وقبل تدقيق الفرص. يربط ما قاله العميل بصورة عملياتية واحدة يفهمها أي عضو في الفريق.

## 2. المدخلات المطلوبة

- ملاحظات مكالمة الاكتشاف (خالية من البيانات الشخصية).
- وصف نصي لخط الأنابيب الحالي.
- قائمة الأدوات التي يستخدمها العميل اليوم.

## 3. خطوات الرسم (خطوة بخطوة)

1. **رحلة الإيراد:** ارسم المراحل من أول تواصل حتى الإغلاق كقائمة مرتّبة.
2. **المالكون:** لكل مرحلة، حدّد من يملكها داخل شركة العميل.
3. **الأدوات:** اربط كل مرحلة بالأداة المستخدمة (أو «بدون أداة»).
4. **نقاط التعطل:** علّم المراحل التي ذكر العميل فيها تأخيراً أو فقداناً للفرص.
5. **مصادر البيانات:** سجّل أين تعيش بيانات كل مرحلة وحالتها (منظَّمة / مبعثرة).
6. **الفجوات:** اكتب فجوة واحدة واضحة لكل نقطة تعطل.
7. **التحقق:** أرسل الخريطة للعميل لتأكيد الدقة قبل الانتقال للتدقيق.

## 4. القواعد الحاكمة (Non-negotiables)

- الخريطة تصف الواقع لا الحل — لا توصيات في هذه المرحلة.
- لا بيانات شخصية ولا أسماء عملاء حقيقية في الملف.
- لا افتراضات غير مؤكدة — كل عنصر مصدره كلام العميل.
- المخرَج بحالة `draft_only` حتى يؤكده العميل.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] رحلة الإيراد كاملة من أول تواصل حتى الإغلاق.
- [ ] كل مرحلة لها مالك وأداة.
- [ ] حُدّدت 3 نقاط تعطل على الأقل بفجواتها.
- [ ] أكّد العميل دقة الخريطة كتابياً.
- [ ] الملف ثنائي اللغة ومتطابق الطول.

## 6. المقاييس

- زمن الرسم: من المقابلة إلى تأكيد العميل (الهدف ≤ 24 ساعة).
- نسبة المراحل المربوطة بمالك وأداة (الهدف 100%).
- معدل تأكيد العميل من المحاولة الأولى.

## 7. خطافات المراقبة (Observability)

- سجّل الخريطة في ملف العميل تحت `clients/<client>/00_scope.md`.
- علّم الحالة: `draft` / `client_confirmed` / `revised`.
- مراجعة أسبوعية لعدد الخرائط وزمنها.

## 8. إجراء التراجع (Rollback)

إذا اكتشف العميل خطأً في الخريطة:
1. صحّح العنصر وأعد الإرسال خلال 24 ساعة.
2. لا تبدأ تدقيق الفرص على خريطة غير مؤكدة.
3. سجّل سبب الخطأ لتحسين قالب الرسم.

# English

# Current-State Mapping — Layer 10 / Discovery Stage

**Owner:** Delivery Lead
**Audience:** Team member documenting a client's operations before the offer
**References:** `playbooks/discovery/client_interview_questions.md` · `playbooks/discovery/ai_opportunity_audit.md` · `clients/_TEMPLATE/00_scope.md` · `clients/_TEMPLATE/01_intake.md`

> Purpose: turn interview output into a structured current-state map that makes gaps visible. The map is the foundation the opportunity audit builds on.

## 1. When to use this playbook

After the discovery call and before the opportunity audit. It converts what the client said into one operational picture any team member can read.

## 2. Inputs required

- Discovery call notes (PII-free).
- A text description of the current pipeline.
- The list of tools the client uses today.

## 3. Mapping steps (step by step)

1. **Revenue journey:** draw the stages from first contact to close as an ordered list.
2. **Owners:** for each stage, identify who owns it inside the client company.
3. **Tools:** map each stage to the tool used (or "no tool").
4. **Stall points:** mark the stages where the client reported delays or lost opportunities.
5. **Data sources:** record where each stage's data lives and its state (structured / scattered).
6. **Gaps:** write one clear gap for each stall point.
7. **Validation:** send the map to the client to confirm accuracy before moving to the audit.

## 4. Governance rules (non-negotiables)

- The map describes reality, not the solution — no recommendations at this stage.
- No PII and no real client names in the file.
- No unconfirmed assumptions — every element traces to the client's own words.
- The output is `draft_only` until the client confirms it.

## 5. Acceptance criteria (readiness checklist)

- [ ] Revenue journey complete from first contact to close.
- [ ] Every stage has an owner and a tool.
- [ ] At least 3 stall points identified with their gaps.
- [ ] Client confirmed the map's accuracy in writing.
- [ ] File is bilingual and length-matched.

## 6. Metrics

- Mapping time: interview to client confirmation (target ≤ 24 hours).
- Share of stages mapped to an owner and a tool (target 100%).
- First-pass client confirmation rate.

## 7. Observability hooks

- Save the map in the client folder under `clients/<client>/00_scope.md`.
- Tag the state: `draft` / `client_confirmed` / `revised`.
- Weekly review of map count and time.

## 8. Rollback procedure

If the client finds an error in the map:
1. Correct the element and resend within 24 hours.
2. Do not start the opportunity audit on an unconfirmed map.
3. Record the cause of the error to improve the mapping template.
