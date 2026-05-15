# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## اختبار عابر للطبقات: التراجع يستعيد الوكيل وسير العمل والموجِّه والسياسة معاً

الطبقات المشاركة: 12 (التطور المستمر) + 2 (زمن تشغيل الوكيل) + 3 (محرك سير العمل) + 5 (الحوكمة).

## الهدف

التحقق من أن عملية تراجع واحدة تعيد المنصة إلى آخر حالة خضراء معروفة عبر أربعة مكونات معاً — الوكيل، سير العمل، الموجِّه (prompt)، والسياسة — بلا حالة مختلطة بين إصدارَين.

## المتطلبات المسبقة

- إصدار حالي معروف الحالة لكل من: وكيل، سير عمل، موجِّه، سياسة.
- منطق التطور المستمر عبر `auto_client_acquisition/self_growth_os/`.
- تراجع الوكيل عبر `auto_client_acquisition/agent_os/agent_lifecycle.py`.
- تراجع سير العمل عبر `auto_client_acquisition/workflow_os/` وإصداراته.
- تراجع السياسة عبر `auto_client_acquisition/governance_os/policy_registry.py`.
- نقطة استعادة موثَّقة (آخر حالة خضراء).

## الخطوات

1. سجّل الإصدارات الحالية الأربعة كخط أساس أخضر.
2. انشر إصداراً جديداً للمكونات الأربعة معاً.
3. أعلن حادثاً يستدعي التراجع.
4. نفّذ تراجعاً واحداً يستعيد المكونات الأربعة معاً.
5. تحقق من تطابق كل مكوّن مع خط الأساس الأخضر.
6. شغّل سير عمل تجريبياً للتأكد من عدم بقاء حالة مختلطة.
7. سجّل زمن التراجع وسلامة الحالة.

## النتيجة المتوقعة

- الخطوة 4: التراجع يستعيد الوكيل وسير العمل والموجِّه والسياسة في عملية واحدة متسقة.
- الخطوة 5: كل مكوّن مطابق لخط الأساس الأخضر.
- الخطوة 6: لا حالة مختلطة بين إصدارَين؛ لا أثر جزئي.
- الخطوة 7: زمن مُسجَّل ضمن حدود الخطة.

## معيار النجاح/الفشل

- **نجاح:** المكونات الأربعة مستعادة معاً، لا حالة مختلطة، زمن موثَّق.
- **فشل:** بقاء أي مكوّن على الإصدار الجديد، أو حالة مختلطة، أو غياب تمرين دوري متحقَّق. هذه الفجوة تُبقي المنصة في نطاق تجربة عميل وتمنع بلوغ "جاهز للمؤسسات".

## ملاحظة الجاهزية

هذا التمرين مُحدَّد لكنه لم يُنفَّذ بعد على وتيرة دورية متحقَّقة. وهو أحد أبرز الفجوات في قائمة `readiness/ENTERPRISE_READINESS_SCORECARD.md`.

## روابط ذات صلة

- `readiness/agents/readiness.md`
- `readiness/workflows/readiness.md`
- `readiness/governance/readiness.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Cross-layer test: a rollback restores agent, workflow, prompt, and policy together

Participating layers: 12 (Continuous Evolution) + 2 (Agent Runtime) + 3 (Workflow Engine) + 5 (Governance).

## Goal

Verify that a single rollback operation returns the platform to the last known-green state across four components together — agent, workflow, prompt, and policy — with no mixed state between two versions.

## Preconditions

- A current version of known state for each of: an agent, a workflow, a prompt, a policy.
- Continuous-evolution logic via `auto_client_acquisition/self_growth_os/`.
- Agent rollback via `auto_client_acquisition/agent_os/agent_lifecycle.py`.
- Workflow rollback via `auto_client_acquisition/workflow_os/` and its versions.
- Policy rollback via `auto_client_acquisition/governance_os/policy_registry.py`.
- A documented restore point (the last known-green state).

## Steps

1. Record the four current versions as a green baseline.
2. Deploy a new version of all four components together.
3. Declare an incident that calls for a rollback.
4. Execute a single rollback that restores all four components together.
5. Verify each component matches the green baseline.
6. Run a test workflow to confirm no mixed state remains.
7. Record the rollback time and state integrity.

## Expected result

- Step 4: the rollback restores agent, workflow, prompt, and policy in one consistent operation.
- Step 5: every component matches the green baseline.
- Step 6: no mixed state between two versions; no partial effect.
- Step 7: a recorded time within plan limits.

## Pass/fail criteria

- **Pass:** all four components restored together, no mixed state, a documented time.
- **Fail:** any component left on the new version, a mixed state, or the absence of a periodic verified drill. This gap keeps the platform in the client-pilot band and prevents reaching enterprise-ready.

## Readiness note

This drill is specified but has not yet been executed on a verified periodic cadence. It is one of the headline gaps in the `readiness/ENTERPRISE_READINESS_SCORECARD.md` list.

## Related links

- `readiness/agents/readiness.md`
- `readiness/workflows/readiness.md`
- `readiness/governance/readiness.md`
- `readiness/ENTERPRISE_READINESS_SCORECARD.md`

Estimated value is not Verified value.
