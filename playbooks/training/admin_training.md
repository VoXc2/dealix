# العربية

# تدريب المسؤول — Layer 10 / مرحلة التدريب

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** مسؤول النظام لدى العميل (مدير العمليات أو من يملك القرار)
**المراجع:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `clients/_TEMPLATE/AI_OPERATING_MODEL.md` · `playbooks/training/user_training.md` · `playbooks/handover/handover_pack.md`

> الغرض: جلسة تدريب موحّدة تجعل مسؤول العميل قادراً على تشغيل المخرجات واتخاذ قرارات الموافقة دون اعتماد على Dealix.

## 1. متى تُستخدم هذه الجلسة

بعد قبول العميل للمخرَج وقبل التسليم النهائي. مدتها 60 دقيقة لمسؤول واحد.

## 2. أهداف التعلّم

عند نهاية الجلسة يستطيع المسؤول:
- فهم بنية المخرجات وأين تعيش.
- إدارة دورة الموافقة على المسودات (`draft_only`).
- قراءة التقرير التنفيذي الأسبوعي واتخاذ قرار.
- إدارة الصلاحيات والوصول للبيانات.
- معرفة متى وكيف يتصعّد طلباً للدعم.

## 3. أجندة الجلسة (60 دقيقة)

1. **جولة المخرجات (15 دقيقة):** أين تعيش الملفات وكيف تُقرأ.
2. **دورة الموافقة (15 دقيقة):** كيف يوافق المسؤول على مسودة، ولماذا لا يُرسَل شيء قبل موافقته.
3. **قراءة التقارير (10 دقائق):** تفسير الحزمة التنفيذية الأسبوعية.
4. **الحوكمة والصلاحيات (10 دقائق):** إدارة الوصول وحماية بيانات الفريق.
5. **الدعم والتصعيد (10 دقائق):** قنوات الدعم و SLA ومتى يتصعّد.

## 4. القواعد الحاكمة (Non-negotiables)

- يُدرَّب المسؤول على أن لا شيء يُرسَل دون موافقته الصريحة.
- لا تدريب على كشط أو رسائل باردة أو أتمتة LinkedIn.
- لا وعود بأرقام أداء في التدريب — «تقديري» فقط.
- المسؤول يفهم أن Dealix لا يرسل نيابة عنه.
- مواد التدريب خالية من البيانات الشخصية.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] الجلسة الستينية تمّت مع المسؤول.
- [ ] المسؤول نفّذ موافقة تجريبية على مسودة بنجاح.
- [ ] المسؤول قرأ تقريراً تنفيذياً واتخذ قراراً.
- [ ] المسؤول يعرف قنوات الدعم و SLA.
- [ ] دليل المسؤول السريع سُلّم.

## 6. المقاييس

- زمن التدريب: جلسة واحدة 60 دقيقة (الهدف معروف وثابت).
- معدل اجتياز التمرين التطبيقي (الهدف 100%).
- نسبة العملاء الذين أكمل مسؤولهم التدريب قبل التسليم.

## 7. خطافات المراقبة (Observability)

- سجّل اكتمال التدريب في `clients/<client>/AI_OPERATING_MODEL.md`.
- علّم الحالة: `admin_trained` / `pending`.
- مراجعة شهرية لعدد المسؤولين المُدرَّبين.

## 8. إجراء التراجع (Rollback)

إذا لم يجتز المسؤول التمرين التطبيقي:
1. أعِد جلسة 30 دقيقة تركّز على النقطة الناقصة.
2. لا تُجرِ التسليم النهائي قبل اجتياز التمرين.
3. سجّل سبب النقص لتحسين أجندة التدريب.

# English

# Admin Training — Layer 10 / Training Stage

**Owner:** Delivery Lead
**Audience:** The client's system admin (operations manager or decision owner)
**References:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` · `clients/_TEMPLATE/AI_OPERATING_MODEL.md` · `playbooks/training/user_training.md` · `playbooks/handover/handover_pack.md`

> Purpose: a standard training session that makes the client's admin able to operate the deliverables and make approval decisions without depending on Dealix.

## 1. When to use this session

After the client accepts the deliverable and before final handover. It runs 60 minutes for one admin.

## 2. Learning objectives

By the end of the session the admin can:
- Understand the deliverables' structure and where they live.
- Manage the draft approval cycle (`draft_only`).
- Read the weekly executive brief and make a decision.
- Manage access and data permissions.
- Know when and how to escalate a support request.

## 3. Session agenda (60 minutes)

1. **Deliverables tour (15 min):** where files live and how they are read.
2. **Approval cycle (15 min):** how the admin approves a draft, and why nothing is sent before their approval.
3. **Reading reports (10 min):** interpreting the weekly executive pack.
4. **Governance and access (10 min):** managing access and protecting team data.
5. **Support and escalation (10 min):** support channels, SLA, and when to escalate.

## 4. Governance rules (non-negotiables)

- The admin is trained that nothing is sent without their explicit approval.
- No training on scraping, cold messaging, or LinkedIn automation.
- No promises of performance figures in training — "estimated" only.
- The admin understands that Dealix does not send on their behalf.
- Training materials are free of PII.

## 5. Acceptance criteria (readiness checklist)

- [ ] The 60-minute session completed with the admin.
- [ ] The admin completed a practice draft approval successfully.
- [ ] The admin read an executive report and made a decision.
- [ ] The admin knows the support channels and SLA.
- [ ] The admin quick-reference guide handed over.

## 6. Metrics

- Training time: one 60-minute session (target known and fixed).
- Practice exercise pass rate (target 100%).
- Share of clients whose admin completed training before handover.

## 7. Observability hooks

- Log training completion in `clients/<client>/AI_OPERATING_MODEL.md`.
- Tag the state: `admin_trained` / `pending`.
- Monthly review of the count of trained admins.

## 8. Rollback procedure

If the admin does not pass the practice exercise:
1. Run a 30-minute session focused on the missing point.
2. Do not perform final handover before the exercise passes.
3. Record the cause of the gap to improve the training agenda.
