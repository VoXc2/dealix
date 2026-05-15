# العربية

Owner: قائد زمن تشغيل الوكيل (Agent Runtime Lead)

## الغرض

مواصفة اختبار جاهزية لطبقة زمن تشغيل الوكيل. مواصفة بالكلمات، لا كود.

## اختبارات الجاهزية

### ت-1: حدود الأدوات

- **الهدف:** الوكيل لا يستدعي أداة خارج قائمة أذوناته.
- **الخطوات:** كوّن وكيلاً بأداتَين مصرَّح بهما، اطلب أداة ثالثة غير مصرَّح بها عبر `agent_os/tool_permissions.py`.
- **النتيجة المتوقعة:** الأداة غير المصرَّح بها مرفوضة قبل التنفيذ.
- **معيار النجاح/الفشل:** أي استدعاء غير مصرَّح = فشل يوقف الدمج.

### ت-2: حدود السياق والبيانات

- **الهدف:** الوكيل لا يقرأ سياقاً خارج مستأجره عبر `secure_agent_runtime_os/four_boundaries.py`.
- **الخطوات:** شغّل وكيلاً لمستأجر أ واطلب سياق مستأجر ب.
- **النتيجة المتوقعة:** الطلب مرفوض على حدود البيانات.
- **معيار النجاح/الفشل:** أي تجاوز للحدود = فشل.

### ت-3: مفتاح الإيقاف

- **الهدف:** تفعيل مفتاح الإيقاف يُوقف الوكيل في حالة آمنة.
- **الخطوات:** شغّل وكيلاً، فعّل `kill_switch.py` أثناء التنفيذ.
- **النتيجة المتوقعة:** الوكيل يتوقف بلا فعل خارجي معلّق.
- **معيار النجاح/الفشل:** استمرار الوكيل بعد الإيقاف = فشل.

### ت-4: حالات التشغيل

- **الهدف:** انتقالات الحالة في `runtime_states.py` صحيحة ولا تقفز فوق بوابة موافقة.
- **الخطوات:** ادفع الوكيل عبر كل انتقال حالة.
- **النتيجة المتوقعة:** كل انتقال غير مسموح مرفوض.
- **معيار النجاح/الفشل:** أي انتقال غير قانوني = فشل.

### ت-5: تمرين تراجع الوكيل (فجوة معروفة)

- **الهدف:** إعادة إصدار وكيل سابق معروف الحالة.
- **الخطوات:** انشر إصدار وكيل جديد، تراجع إلى السابق عبر `agent_lifecycle.py`.
- **النتيجة المتوقعة:** الإصدار السابق نشط بسلوك متطابق.
- **معيار النجاح/الفشل:** غياب تمرين دوري متحقَّق = فجوة تُبقي الطبقة في نطاق تجربة عميل.

## ما يوقف الدمج

فشل ت-1 أو ت-2 أو ت-3 أو ت-4 يوقف الدمج. ت-5 فجوة موثَّقة.

## روابط ذات صلة

- `readiness/agents/readiness.md`
- `readiness/cross_layer/agent_tool_approval_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Agent Runtime Lead

## Purpose

A readiness test specification for the Agent Runtime layer. A spec in words, not code.

## Readiness tests

### T-1: Tool boundaries

- **Goal:** the agent does not call a tool outside its permission list.
- **Steps:** configure an agent with two authorized tools, request a third unauthorized tool via `agent_os/tool_permissions.py`.
- **Expected result:** the unauthorized tool is rejected before execution.
- **Pass/fail:** any unauthorized call = fail that blocks the merge.

### T-2: Context and data boundaries

- **Goal:** the agent does not read context outside its tenant via `secure_agent_runtime_os/four_boundaries.py`.
- **Steps:** run an agent for tenant A and request tenant B context.
- **Expected result:** the request is rejected on the data boundary.
- **Pass/fail:** any boundary crossing = fail.

### T-3: Kill switch

- **Goal:** activating the kill switch stops the agent in a safe state.
- **Steps:** run an agent, trigger `kill_switch.py` mid-execution.
- **Expected result:** the agent halts with no pending external action.
- **Pass/fail:** the agent continuing after stop = fail.

### T-4: Runtime states

- **Goal:** state transitions in `runtime_states.py` are valid and do not skip an approval gate.
- **Steps:** drive the agent through every state transition.
- **Expected result:** every disallowed transition is rejected.
- **Pass/fail:** any illegal transition = fail.

### T-5: Agent rollback drill (known gap)

- **Goal:** restore a prior agent version of known state.
- **Steps:** deploy a new agent version, roll back to the prior one via `agent_lifecycle.py`.
- **Expected result:** the prior version is active with matching behavior.
- **Pass/fail:** absence of a periodic verified drill = a gap that keeps the layer in the client-pilot band.

## What blocks a merge

Failure in T-1, T-2, T-3, or T-4 blocks the merge. T-5 is a documented gap.

## Related links

- `readiness/agents/readiness.md`
- `readiness/cross_layer/agent_tool_approval_test.md`

Estimated value is not Verified value.
