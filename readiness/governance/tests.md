# العربية

Owner: قائد الحوكمة (Governance Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة الحوكمة. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: الموافقة على الأفعال الخارجية

- **الهدف:** فعل خارجي لا يُنفَّذ بلا موافقة عبر `governance_os/rules/external_action_requires_approval`.
- **الخطوات:** اطلب إرسالاً خارجياً بلا موافقة.
- **النتيجة المتوقعة:** الفعل محجوز بانتظار الموافقة.
- **معيار النجاح/الفشل:** أي فعل خارجي بلا موافقة = فشل يوقف الدمج.

### ت-2: قواعد اللاتفاوضيات

- **الهدف:** القواعد المكتوبة تمنع السلوك الممنوع.
- **الخطوات:** حاول إنشاء ادعاء مضمون، أو إثبات مُختلَق، أو كشط، أو رسالة واتساب باردة.
- **النتيجة المتوقعة:** كل محاولة مرفوضة عبر `no_guaranteed_claims`، `no_fake_proof`، `no_scraping`، `no_cold_whatsapp`.
- **معيار النجاح/الفشل:** مرور أي سلوك ممنوع = فشل يوقف الدمج.

### ت-3: مصفوفة الخطورة

- **الهدف:** كل فعل يُصنَّف بمستوى خطورة صحيح في `governance_os/approval_matrix.py`.
- **الخطوات:** صنّف مجموعة أفعال معروفة الخطورة.
- **النتيجة المتوقعة:** التصنيفات مطابقة للمصفوفة.
- **معيار النجاح/الفشل:** تصنيف خاطئ يخفّض الخطورة = فشل.

### ت-4: سجل التدقيق

- **الهدف:** كل قرار حوكمة مُسجَّل في `dealix/trust/audit.py` بلا معلومات تعريف شخصية.
- **الخطوات:** نفّذ قرارات حوكمة، افحص سجل التدقيق.
- **النتيجة المتوقعة:** كل قرار مُسجَّل، لا معلومات شخصية مكشوفة.
- **معيار النجاح/الفشل:** قرار غير مُسجَّل أو معلومات شخصية مكشوفة = فشل.

### ت-5: تمرين تراجع السياسة (فجوة معروفة)

- **الهدف:** إعادة إصدار سياسة سابق معروف.
- **الخطوات:** انشر سياسة جديدة، تراجع إلى السابقة عبر `policy_registry.py`.
- **النتيجة المتوقعة:** السياسة السابقة نشطة وفاعلة.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/governance/readiness.md`
- `readiness/cross_layer/workflow_governance_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Governance Lead

## Purpose

A readiness test specification for the Governance layer. A spec in words, not code.

## Readiness tests

### T-1: External-action approval

- **Goal:** an external action is not executed without approval via `governance_os/rules/external_action_requires_approval`.
- **Steps:** request an external send with no approval.
- **Expected result:** the action is held awaiting approval.
- **Pass/fail:** any external action without approval = fail that blocks the merge.

### T-2: Non-negotiable rules

- **Goal:** the written rules block forbidden behavior.
- **Steps:** attempt to create a guaranteed claim, a fabricated proof, scraping, or a cold WhatsApp message.
- **Expected result:** every attempt is rejected via `no_guaranteed_claims`, `no_fake_proof`, `no_scraping`, `no_cold_whatsapp`.
- **Pass/fail:** any forbidden behavior passing = fail that blocks the merge.

### T-3: Risk matrix

- **Goal:** every action is classified at the correct risk level in `governance_os/approval_matrix.py`.
- **Steps:** classify a set of actions of known risk.
- **Expected result:** classifications match the matrix.
- **Pass/fail:** a wrong classification that lowers risk = fail.

### T-4: Audit log

- **Goal:** every governance decision is recorded in `dealix/trust/audit.py` with no PII.
- **Steps:** execute governance decisions, inspect the audit log.
- **Expected result:** every decision is recorded, no PII exposed.
- **Pass/fail:** an unrecorded decision or exposed PII = fail.

### T-5: Policy rollback drill (known gap)

- **Goal:** restore a prior known policy version.
- **Steps:** deploy a new policy, roll back to the prior one via `policy_registry.py`.
- **Expected result:** the prior policy is active and effective.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/governance/readiness.md`
- `readiness/cross_layer/workflow_governance_test.md`

Estimated value is not Verified value.
