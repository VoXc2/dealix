# العربية

# اختبارات قبول العميل — Layer 10 / مرحلة ضمان الجودة

**المالك:** قائد الجودة (QA Lead)
**الجمهور:** فريق التسليم والعميل عند الإقرار النهائي بالمخرَج
**المراجع:** `playbooks/qa/pre_launch_checklist.md` · `clients/_TEMPLATE/04_qa_review.md` · `clients/_TEMPLATE/delivery_approval.md` · `docs/scorecards/CLIENT_SCORECARD.md`

> الغرض: مواصفة اختبار مكتوبة تحدد متى يَقبل العميل المخرَج رسمياً. كل عميل يحصل على نفس معايير القبول الواضحة. لا كود — مواصفة فقط.

## 1. متى تُستخدم هذه المواصفة

عند نهاية كل مرحلة تسليم، قبل توقيع موافقة العميل في `delivery_approval.md`.

## 2. حالات الاختبار (مواصفة)

### حالة AC-1: اكتمال المخرَج
- **المدخل:** المخرَج النهائي المُسلَّم للعميل.
- **الخطوة:** قارن بنود المخرَج بمعايير القبول المرحلية.
- **معيار النجاح:** كل بند مطلوب موجود ومكتمل.

### حالة AC-2: دقة الأدلة
- **المدخل:** كل رقم وادعاء في المخرَج.
- **الخطوة:** تتبّع كل عنصر إلى مصدره في بيانات العميل.
- **معيار النجاح:** 100% من العناصر مرتبطة بمصدر موثَّق.

### حالة AC-3: مطابقة النطاق
- **المدخل:** المخرَج و`clients/<client>/00_scope.md`.
- **الخطوة:** قارن المُسلَّم بالنطاق المتّفق عليه.
- **معيار النجاح:** لا بند خارج النطاق ولا بند ناقص.

### حالة AC-4: الامتثال للحوكمة
- **المدخل:** نص المخرَج كاملاً.
- **الخطوة:** ابحث عن «نضمن»، أرقام كحقيقة، بيانات شخصية، أسماء عملاء.
- **معيار النجاح:** صفر مخالفات.

### حالة AC-5: حالة المسودة
- **المدخل:** وسم حالة المخرَج.
- **الخطوة:** تأكّد من أن كل مخرَج قابل للإرسال معلَّم `draft_only`.
- **معيار النجاح:** لا مخرَج بحالة «مُرسَل» دون موافقة عميل صريحة.

### حالة AC-6: جودة اللغة
- **المدخل:** نص المخرَج.
- **الخطوة:** راجع الوضوح والمهنية، والتطابق ثنائي اللغة عند الحاجة.
- **معيار النجاح:** لغة طبيعية، وأقسام عربية وإنجليزية متطابقة الطول.

### حالة AC-7: إقرار العميل
- **المدخل:** مراجعة العميل للمخرَج.
- **الخطوة:** اجمع موافقة العميل المكتوبة.
- **معيار النجاح:** توقيع العميل مسجَّل في `delivery_approval.md`.

## 3. معايير القبول الإجمالية

- يُعدّ المخرَج «مقبولاً» فقط عندما تَنجح حالات AC-1 إلى AC-7 جميعها.
- أي حالة فاشلة تعني «مرفوض» وتُعاد للتسليم بملاحظة محددة.
- لا upsell ولا انتقال لمرحلة تالية قبل قبول كامل.

## 4. القواعد الحاكمة (Non-negotiables)

- العميل وحده يَقبل المخرَج رسمياً — لا قبول ذاتي من الفريق.
- لا اختبار يتجاوز فحص الحوكمة.
- لا إثبات مختلق في أي حالة اختبار.
- المخرَج يبقى `draft_only` حتى توقيع AC-7.

## 5. خطوات التنفيذ

1. شغّل حالات AC-1 إلى AC-6 داخلياً قبل عرض المخرَج.
2. اعرض المخرَج على العميل لتنفيذ AC-7.
3. سجّل نتيجة كل حالة في `clients/<client>/04_qa_review.md`.
4. عند القبول الكامل، حدّث `docs/scorecards/CLIENT_SCORECARD.md`.

## 6. المقاييس

- معدل القبول من المحاولة الأولى (الهدف ≥ 85%).
- متوسط عدد دورات المراجعة قبل القبول (الهدف ≤ 2).
- نسبة العملاء الذين لديهم معايير قبول موثَّقة (الهدف 100%).

## 7. خطافات المراقبة (Observability)

- سجّل نتيجة كل حالة اختبار: `pass` / `fail`.
- علّم حالة المخرَج: `accepted` / `returned`.
- مراجعة أسبوعية لمعدل القبول ودورات المراجعة.

## 8. إجراء التراجع (Rollback)

إذا قُبل مخرَج ثم اكتُشف عيب لاحقاً:
1. أبلغ العميل باحترام بنسخة مصححة خلال 24 ساعة.
2. سجّل الحادثة في سجل الحوكمة.
3. أضف حالة اختبار جديدة تغطي العيب لمنع تكراره.

# English

# Client Acceptance Tests — Layer 10 / QA Stage

**Owner:** QA Lead
**Audience:** The delivery team and the client at final sign-off of a deliverable
**References:** `playbooks/qa/pre_launch_checklist.md` · `clients/_TEMPLATE/04_qa_review.md` · `clients/_TEMPLATE/delivery_approval.md` · `docs/scorecards/CLIENT_SCORECARD.md`

> Purpose: a written test specification that defines when the client formally accepts a deliverable. Every client gets the same clear acceptance criteria. No code — specification only.

## 1. When to use this specification

At the end of every delivery stage, before signing client approval in `delivery_approval.md`.

## 2. Test cases (specification)

### Case AC-1: Deliverable completeness
- **Input:** the final deliverable handed to the client.
- **Step:** compare deliverable items against the stage acceptance criteria.
- **Pass criterion:** every required item is present and complete.

### Case AC-2: Evidence accuracy
- **Input:** every figure and claim in the deliverable.
- **Step:** trace each element to its source in the client's data.
- **Pass criterion:** 100% of elements linked to a documented source.

### Case AC-3: Scope match
- **Input:** the deliverable and `clients/<client>/00_scope.md`.
- **Step:** compare what was delivered against the agreed scope.
- **Pass criterion:** no out-of-scope item and no missing item.

### Case AC-4: Governance compliance
- **Input:** the full deliverable text.
- **Step:** search for "guaranteed", figures as fact, PII, client names.
- **Pass criterion:** zero violations.

### Case AC-5: Draft state
- **Input:** the deliverable's state tag.
- **Step:** confirm every sendable deliverable is tagged `draft_only`.
- **Pass criterion:** no deliverable in a "sent" state without explicit client approval.

### Case AC-6: Language quality
- **Input:** the deliverable text.
- **Step:** review clarity and professionalism, and bilingual match where needed.
- **Pass criterion:** natural language, and Arabic and English sections matched in length.

### Case AC-7: Client sign-off
- **Input:** the client's review of the deliverable.
- **Step:** collect the client's written approval.
- **Pass criterion:** client signature recorded in `delivery_approval.md`.

## 3. Overall acceptance criteria

- A deliverable is "accepted" only when cases AC-1 through AC-7 all pass.
- Any failed case means "rejected" and is returned to delivery with a specific note.
- No upsell and no move to a next stage before full acceptance.

## 4. Governance rules (non-negotiables)

- The client alone formally accepts the deliverable — no self-acceptance by the team.
- No test bypasses the governance check.
- No fake proof in any test case.
- The deliverable stays `draft_only` until AC-7 is signed.

## 5. Execution steps

1. Run cases AC-1 through AC-6 internally before showing the deliverable.
2. Present the deliverable to the client to run AC-7.
3. Log each case result in `clients/<client>/04_qa_review.md`.
4. On full acceptance, update `docs/scorecards/CLIENT_SCORECARD.md`.

## 6. Metrics

- First-pass acceptance rate (target ≥ 85%).
- Average review cycles before acceptance (target ≤ 2).
- Share of clients with documented acceptance criteria (target 100%).

## 7. Observability hooks

- Log each test case result: `pass` / `fail`.
- Tag the deliverable state: `accepted` / `returned`.
- Weekly review of acceptance rate and review cycles.

## 8. Rollback procedure

If a deliverable was accepted and a defect is found later:
1. Respectfully send the client a corrected version within 24 hours.
2. Record the incident in the governance log.
3. Add a new test case covering the defect to prevent recurrence.
