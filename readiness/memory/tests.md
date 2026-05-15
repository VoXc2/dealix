# العربية

Owner: قائد المعرفة والذاكرة (Knowledge & Memory Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة الذاكرة والمعرفة. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: عزل ذاكرة المستأجر

- **الهدف:** الاسترجاع لا يعيد شريحة من مستأجر آخر.
- **الخطوات:** افهرس مستندات لمستأجرَين، استرجِع بهوية كل مستأجر عبر `knowledge_os/`.
- **النتيجة المتوقعة:** كل مستأجر يرى شرائحه فقط.
- **معيار النجاح/الفشل:** أي شريحة عبر المستأجرين = فشل يوقف الدمج.

### ت-2: لا مصدر، لا إجابة

- **الهدف:** الإجابة لا تُرجَع بلا مصدر مُستشهَد.
- **الخطوات:** اطرح سؤالاً لا يغطيه أي مستند.
- **النتيجة المتوقعة:** امتناع صريح، لا إجابة مُختلَقة، اتساقاً مع `no_source_no_answer.yaml`.
- **معيار النجاح/الفشل:** إجابة بلا مصدر = فشل.

### ت-3: أذونات الاسترجاع

- **الهدف:** الاسترجاع لا يعيد مصدراً خارج أذونات المستخدم.
- **الخطوات:** افهرس مستنداً مقيّداً، استرجِع بهوية مستخدم بلا إذن.
- **النتيجة المتوقعة:** المصدر المقيّد غير مُعاد.
- **معيار النجاح/الفشل:** أي مصدر مقيّد مُعاد = فشل.

### ت-4: نسب المصدر

- **الهدف:** كل استشهاد يربط بمصدر حقيقي قابل للتتبع.
- **الخطوات:** تحقق من الاستشهادات في إجابة عبر `source_lineage`.
- **النتيجة المتوقعة:** كل استشهاد يحلّ إلى مستند مصدر.
- **معيار النجاح/الفشل:** استشهاد بلا مصدر قابل للتتبع = فشل.

### ت-5: تمرين حذف مستأجر للفهرس (فجوة معروفة)

- **الهدف:** حذف مستأجر يزيل شرائحه من فهرس البحث.
- **الخطوات:** افهرس مستأجراً، احذفه، استرجِع لاحقاً.
- **النتيجة المتوقعة:** لا شرائح متبقية.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/memory/readiness.md`
- `readiness/cross_layer/rag_permission_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Knowledge & Memory Lead

## Purpose

A readiness test specification for the Memory & Knowledge layer. A spec in words, not code.

## Readiness tests

### T-1: Tenant memory isolation

- **Goal:** retrieval does not return a chunk from another tenant.
- **Steps:** index documents for two tenants, retrieve as each tenant via `knowledge_os/`.
- **Expected result:** each tenant sees only its own chunks.
- **Pass/fail:** any cross-tenant chunk = fail that blocks the merge.

### T-2: No source, no answer

- **Goal:** an answer is not returned without a cited source.
- **Steps:** ask a question no document covers.
- **Expected result:** explicit abstention, no fabricated answer, consistent with `no_source_no_answer.yaml`.
- **Pass/fail:** an answer with no source = fail.

### T-3: Retrieval permissions

- **Goal:** retrieval does not return a source outside the user's permissions.
- **Steps:** index a restricted document, retrieve as a user with no permission.
- **Expected result:** the restricted source is not returned.
- **Pass/fail:** any restricted source returned = fail.

### T-4: Source lineage

- **Goal:** every citation links to a real traceable source.
- **Steps:** verify citations in an answer via `source_lineage`.
- **Expected result:** every citation resolves to a source document.
- **Pass/fail:** a citation with no traceable source = fail.

### T-5: Tenant-deletion drill for the index (known gap)

- **Goal:** deleting a tenant removes its chunks from the search index.
- **Steps:** index a tenant, delete it, retrieve afterward.
- **Expected result:** no residual chunks.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/memory/readiness.md`
- `readiness/cross_layer/rag_permission_test.md`

Estimated value is not Verified value.
