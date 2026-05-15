# العربية

Owner: قائد التقييم (Evaluation Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة التقييم. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: تشغيل مجموعات التقييم في CI

- **الهدف:** كل مجموعة تقييم في `evals/` تعمل في CI وتنتج درجة.
- **الخطوات:** شغّل `evals/company_brain_eval.yaml` و`evals/lead_intelligence_eval.yaml` و`evals/outreach_quality_eval.yaml`.
- **النتيجة المتوقعة:** درجة لكل مجموعة بمصدر حالاتها.
- **معيار النجاح/الفشل:** مجموعة لا تعمل أو بلا درجة = فشل يوقف الدمج.

### ت-2: تقييم الحوكمة

- **الهدف:** `evals/governance_eval.yaml` يكشف أي خرق للاتفاوضيات.
- **الخطوات:** شغّل التقييم على مخرجات تتضمن ادعاءً مضموناً أو إثباتاً مُختلَقاً.
- **النتيجة المتوقعة:** التقييم يرصد الخرق ويفشل.
- **معيار النجاح/الفشل:** خرق يمر بلا رصد = فشل يوقف الدمج.

### ت-3: تقييم الجودة العربية

- **الهدف:** `evals/arabic_quality_eval.yaml` يحافظ على عتبة جودة المخرجات العربية.
- **الخطوات:** شغّل التقييم على عينة مخرجات عربية.
- **النتيجة المتوقعة:** الدرجة فوق العتبة المحددة.
- **معيار النجاح/الفشل:** درجة دون العتبة = فشل.

### ت-4: عتبة منع التراجع

- **الهدف:** إصدار يتراجع في التقييم لا يُطرَح.
- **الخطوات:** قدّم إصداراً بدرجة أدنى من خط الأساس.
- **النتيجة المتوقعة:** الطرح محجوب.
- **معيار النجاح/الفشل:** طرح إصدار متراجع = فشل.

### ت-5: مقارنة آلية بين الإصدارين (فجوة معروفة)

- **الهدف:** مقارنة آلية بين الإصدار 1 والإصدار 2 على نفس مجموعة الحالات.
- **الخطوات:** شغّل المقارنة، افحص فرق الدرجات.
- **النتيجة المتوقعة:** فرق مُسجَّل ومرئي، طرح محجوب عند التراجع.
- **معيار النجاح/الفشل:** غياب مقارنة آلية على وتيرة متحقَّقة = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/evals/readiness.md`
- `evals/tests.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Evaluation Lead

## Purpose

A readiness test specification for the Evaluation layer. A spec in words, not code.

## Readiness tests

### T-1: Running eval suites in CI

- **Goal:** every eval suite in `evals/` runs in CI and produces a score.
- **Steps:** run `evals/company_brain_eval.yaml`, `evals/lead_intelligence_eval.yaml`, and `evals/outreach_quality_eval.yaml`.
- **Expected result:** a score per suite with its case source.
- **Pass/fail:** a suite that does not run or has no score = fail that blocks the merge.

### T-2: Governance eval

- **Goal:** `evals/governance_eval.yaml` catches any non-negotiable breach.
- **Steps:** run the eval on output containing a guaranteed claim or a fabricated proof.
- **Expected result:** the eval flags the breach and fails.
- **Pass/fail:** a breach passing unflagged = fail that blocks the merge.

### T-3: Arabic quality eval

- **Goal:** `evals/arabic_quality_eval.yaml` holds an Arabic output quality threshold.
- **Steps:** run the eval on a sample of Arabic output.
- **Expected result:** the score is above the defined threshold.
- **Pass/fail:** a score below the threshold = fail.

### T-4: Regression-block threshold

- **Goal:** a version that regresses on evals is not rolled out.
- **Steps:** submit a version with a score below baseline.
- **Expected result:** the rollout is blocked.
- **Pass/fail:** rolling out a regressing version = fail.

### T-5: Automated v1/v2 comparison (known gap)

- **Goal:** an automated comparison of v1 and v2 on the same case set.
- **Steps:** run the comparison, inspect the score delta.
- **Expected result:** a recorded, visible delta; rollout blocked on regression.
- **Pass/fail:** absence of an automated comparison on a verified cadence = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/evals/readiness.md`
- `evals/tests.md`

Estimated value is not Verified value.
