# العربية

Owner: قائد نجاح العميل (Customer Success Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة تسليم العميل. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: اكتمال كتيّب التسليم

- **الهدف:** كل مرحلة في `clients/_TEMPLATE/` لها قالب وبوابة.
- **الخطوات:** راجع التسلسل من `01_intake.md` إلى `07_next_steps.md`.
- **النتيجة المتوقعة:** لا مرحلة بلا قالب أو بوابة.
- **معيار النجاح/الفشل:** مرحلة ناقصة = فشل يوقف الدمج.

### ت-2: بوابة الموافقة على التسليم

- **الهدف:** التسليم لا يتم بلا موافقة موثَّقة في `delivery_approval.md`.
- **الخطوات:** حاول إغلاق مشروع بلا موافقة.
- **النتيجة المتوقعة:** الإغلاق محجوب.
- **معيار النجاح/الفشل:** تسليم بلا موافقة = فشل.

### ت-3: سلامة حزمة الإثبات

- **الهدف:** حزمة الإثبات لا تحتوي أرقاماً مضمونة ولا عملاء وهميين.
- **الخطوات:** راجع `06_proof_pack.md` لمشروع.
- **النتيجة المتوقعة:** كل قيمة موسومة تقديرية حتى التحقق، كل دراسة حالة بلا اسم حقيقي تُوسَم "قالب افتراضي آمن".
- **معيار النجاح/الفشل:** رقم مضمون أو عميل وهمي = فشل يوقف الدمج.

### ت-4: مراجعة الجودة قبل التسليم

- **الهدف:** بوابة `04_qa_review.md` تمنع تسليماً بعيوب معروفة.
- **الخطوات:** قدّم مخرجاً بعيب معروف.
- **النتيجة المتوقعة:** المراجعة ترصد العيب وتحجب التسليم.
- **معيار النجاح/الفشل:** عيب يمر = فشل.

### ت-5: تمرين تسليم من البداية للنهاية (فجوة معروفة)

- **الهدف:** انتقال كامل من الاستلام إلى التسليم.
- **الخطوات:** نفّذ مشروعاً تجريبياً عبر `clients/_PROJECT_WORKBENCH/`.
- **النتيجة المتوقعة:** كل بوابة مُجتازة بدليل.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/delivery/readiness.md`
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Customer Success Lead

## Purpose

A readiness test specification for the Client Delivery layer. A spec in words, not code.

## Readiness tests

### T-1: Delivery playbook completeness

- **Goal:** every stage in `clients/_TEMPLATE/` has a template and a gate.
- **Steps:** review the sequence from `01_intake.md` to `07_next_steps.md`.
- **Expected result:** no stage without a template or a gate.
- **Pass/fail:** a missing stage = fail that blocks the merge.

### T-2: Delivery approval gate

- **Goal:** delivery does not happen without an approval documented in `delivery_approval.md`.
- **Steps:** attempt to close a project with no approval.
- **Expected result:** closure is blocked.
- **Pass/fail:** a delivery with no approval = fail.

### T-3: Proof-pack integrity

- **Goal:** the proof pack contains no guaranteed numbers and no fake customers.
- **Steps:** review `06_proof_pack.md` for a project.
- **Expected result:** every value labeled estimated until verified; every case study with no real name labeled "hypothetical / case-safe template".
- **Pass/fail:** a guaranteed number or a fake customer = fail that blocks the merge.

### T-4: QA review before delivery

- **Goal:** the `04_qa_review.md` gate blocks a delivery with known defects.
- **Steps:** submit a deliverable with a known defect.
- **Expected result:** the review flags the defect and blocks delivery.
- **Pass/fail:** a defect passing = fail.

### T-5: End-to-end delivery drill (known gap)

- **Goal:** a full transition from intake to handoff.
- **Steps:** run a test project through `clients/_PROJECT_WORKBENCH/`.
- **Expected result:** every gate passed with evidence.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/delivery/readiness.md`
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md`

Estimated value is not Verified value.
