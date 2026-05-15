# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## اختبار عابر للطبقات: سير العمل لا ينفّذ فعلاً عالي الخطورة بلا موافقة

الطبقات المشاركة: 3 (محرك سير العمل) + 5 (الحوكمة).

## الهدف

التحقق من أن سير عمل متعدد الخطوات يتوقف عند بوابة موافقة قبل تنفيذ أي فعل مُصنَّف عالي الخطورة، وأن الحوكمة تفرض ذلك ولا يلتفّ سير العمل عليها.

## المتطلبات المسبقة

- سير عمل معرَّف في `auto_client_acquisition/workflow_os/` يحتوي خطوة عالية الخطورة.
- بوابات في `auto_client_acquisition/execution_os/gates.py`.
- مصفوفة موافقة في `auto_client_acquisition/governance_os/approval_matrix.py` تصنّف الخطوة عالية الخطورة.

## الخطوات

1. شغّل سير العمل بلا أي موافقة معلّقة.
2. راقب سلوك سير العمل عند بلوغ الخطوة عالية الخطورة.
3. تحقق من سجل التدقيق في `dealix/trust/audit.py`.
4. امنح الموافقة، ثم تابع سير العمل.
5. أعد التشغيل مع محاولة تخطّي البوابة برمجياً.

## النتيجة المتوقعة

- الخطوة 2: سير العمل يتوقف عند البوابة بحالة "بانتظار الموافقة".
- الخطوة 3: التوقف مُسجَّل في سجل التدقيق.
- الخطوة 4: سير العمل يكمل فقط بعد الموافقة.
- الخطوة 5: محاولة التخطّي مرفوضة.

## معيار النجاح/الفشل

- **نجاح:** لا فعل عالي الخطورة يُنفَّذ قبل موافقة موثَّقة؛ كل محاولة تخطّي مرفوضة ومُسجَّلة.
- **فشل:** أي فعل عالي الخطورة يُنفَّذ بلا موافقة. الفشل يوقف الدمج ويضع سقفاً على الطبقتين 3 و5 عند نطاق تجربة عميل.

## روابط ذات صلة

- `readiness/workflows/readiness.md`
- `readiness/governance/readiness.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Cross-layer test: a workflow does not execute a high-risk action without approval

Participating layers: 3 (Workflow Engine) + 5 (Governance).

## Goal

Verify that a multi-step workflow halts at an approval gate before executing any action classified as high-risk, and that governance enforces this and the workflow cannot route around it.

## Preconditions

- A workflow defined in `auto_client_acquisition/workflow_os/` containing a high-risk step.
- Gates in `auto_client_acquisition/execution_os/gates.py`.
- An approval matrix in `auto_client_acquisition/governance_os/approval_matrix.py` that classifies the high-risk step.

## Steps

1. Run the workflow with no pending approval.
2. Observe the workflow behavior when it reaches the high-risk step.
3. Check the audit log in `dealix/trust/audit.py`.
4. Grant the approval, then continue the workflow.
5. Re-run with an attempt to skip the gate programmatically.

## Expected result

- Step 2: the workflow halts at the gate in an "awaiting approval" state.
- Step 3: the halt is recorded in the audit log.
- Step 4: the workflow completes only after approval.
- Step 5: the skip attempt is rejected.

## Pass/fail criteria

- **Pass:** no high-risk action executes before a documented approval; every skip attempt is rejected and logged.
- **Fail:** any high-risk action executes without approval. A failure blocks the merge and caps Layers 3 and 5 at the client-pilot band.

## Related links

- `readiness/workflows/readiness.md`
- `readiness/governance/readiness.md`

Estimated value is not Verified value.
