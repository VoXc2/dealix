# العربية

Owner: قائد التحول (Transformation Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة التحول. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: بوابات التبني

- **الهدف:** الطرح لا يتقدم مرحلة بلا اجتياز بوابة التبني في `enterprise_rollout_os/adoption_gates.py`.
- **الخطوات:** ادفع طرحاً عبر مرحلة بلا استيفاء معيار البوابة.
- **النتيجة المتوقعة:** الطرح محجوز عند البوابة.
- **معيار النجاح/الفشل:** تقدم بلا اجتياز بوابة = فشل يوقف الدمج.

### ت-2: تقييم مخاطر المؤسسة

- **الهدف:** `enterprise_risk.py` يصنّف مخاطر الطرح قبل التقدم.
- **الخطوات:** شغّل تقييم مخاطر على طرح عالي المخاطر.
- **النتيجة المتوقعة:** المخاطر مُصنَّفة ومرئية في لوحة الطرح.
- **معيار النجاح/الفشل:** مخاطرة غير مُصنَّفة = فشل.

### ت-3: مراحل الطرح

- **الهدف:** انتقالات المراحل في `rollout_stage.py` صحيحة ولا تقفز.
- **الخطوات:** ادفع طرحاً عبر كل انتقال مرحلة.
- **النتيجة المتوقعة:** كل انتقال غير مسموح مرفوض.
- **معيار النجاح/الفشل:** قفزة مرحلة غير قانونية = فشل.

### ت-4: خرائط الأدوار

- **الهدف:** `role_map.py` يربط كل دور بصلاحيات وبوابات صحيحة.
- **الخطوات:** راجع خريطة الأدوار لطرح.
- **النتيجة المتوقعة:** لا دور بلا صلاحيات محددة.
- **معيار النجاح/الفشل:** دور بلا صلاحيات = فشل.

### ت-5: تمرين تراجع الطرح (فجوة معروفة)

- **الهدف:** العودة من مرحلة طرح إلى السابقة بسلامة.
- **الخطوات:** قدّم مرحلة طرح، تراجع إلى السابقة عبر `rollout_stage.py`.
- **النتيجة المتوقعة:** المرحلة السابقة نشطة بلا أثر جزئي.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة داخلية.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/transformation/readiness.md`
- `readiness/cross_layer/rollback_drill.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Transformation Lead

## Purpose

A readiness test specification for the Transformation layer. A spec in words, not code.

## Readiness tests

### T-1: Adoption gates

- **Goal:** a rollout does not advance a stage without passing the adoption gate in `enterprise_rollout_os/adoption_gates.py`.
- **Steps:** push a rollout through a stage without meeting the gate criterion.
- **Expected result:** the rollout is held at the gate.
- **Pass/fail:** advancing without passing a gate = fail that blocks the merge.

### T-2: Enterprise risk assessment

- **Goal:** `enterprise_risk.py` classifies rollout risk before advancing.
- **Steps:** run a risk assessment on a high-risk rollout.
- **Expected result:** risk is classified and visible on the rollout dashboard.
- **Pass/fail:** an unclassified risk = fail.

### T-3: Rollout stages

- **Goal:** stage transitions in `rollout_stage.py` are valid and do not skip.
- **Steps:** push a rollout through every stage transition.
- **Expected result:** every disallowed transition is rejected.
- **Pass/fail:** an illegal stage skip = fail.

### T-4: Role maps

- **Goal:** `role_map.py` links every role to correct permissions and gates.
- **Steps:** review the role map for a rollout.
- **Expected result:** no role without defined permissions.
- **Pass/fail:** a role with no permissions = fail.

### T-5: Rollout rollback drill (known gap)

- **Goal:** return from a rollout stage to the prior one safely.
- **Steps:** advance a rollout stage, roll back to the prior one via `rollout_stage.py`.
- **Expected result:** the prior stage is active with no partial effect.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the internal-beta band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/transformation/readiness.md`
- `readiness/cross_layer/rollback_drill.md`

Estimated value is not Verified value.
