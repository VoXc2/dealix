# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## اختبار عابر للطبقات: الاسترجاع لا يعيد مصدراً خارج أذونات المستخدم

الطبقات المشاركة: 4 (الذاكرة والمعرفة) + 1 (الأساس).

## الهدف

التحقق من أن الاسترجاع المستند (RAG) لا يعيد أبداً مصدراً يقع خارج أذونات المستخدم الطالب، وأن فرض الأذونات يصمد عبر طبقة المعرفة وطبقة الأساس معاً.

## المتطلبات المسبقة

- مستندان: مستند عام ومستند مقيّد، كلاهما مُفهرَس عبر `auto_client_acquisition/knowledge_os/`.
- مستخدمان ضمن نفس المستأجر: مستخدم بإذن للمستند المقيّد ومستخدم بلا إذن، عبر RBAC في طبقة الأساس.
- مسار إجابة بالاستشهادات عبر `auto_client_acquisition/knowledge_os/answer_with_citations.py`.

## الخطوات

1. اطرح سؤالاً يغطيه المستند المقيّد بهوية المستخدم المصرَّح له.
2. سجّل المصادر المُستشهَد بها.
3. اطرح نفس السؤال بهوية المستخدم غير المصرَّح له.
4. سجّل المصادر المُستشهَد بها والإجابة.
5. تحقق من سجل التدقيق لكلا الطلبين.

## النتيجة المتوقعة

- الخطوة 1 و2: المستخدم المصرَّح له يرى المستند المقيّد ضمن المصادر.
- الخطوة 3 و4: المستخدم غير المصرَّح له لا يرى المستند المقيّد؛ الإجابة تستند فقط للمستند العام أو تمتنع.
- الخطوة 5: كلا الطلبين مُسجَّلان بلا معلومات تعريف شخصية.

## معيار النجاح/الفشل

- **نجاح:** لا مصدر مقيّد يظهر لمستخدم بلا إذن، ولا حتى عبر إعادة صياغة السؤال.
- **فشل:** أي مصدر مقيّد يُعاد، أو تتسرّب محتوياته في الإجابة. الفشل يوقف الدمج ويضع سقفاً على الطبقتين 4 و1 عند نطاق تجربة عميل.

## روابط ذات صلة

- `readiness/memory/readiness.md`
- `readiness/foundation/readiness.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Cross-layer test: retrieval never returns a source outside the user's permissions

Participating layers: 4 (Memory & Knowledge) + 1 (Foundation).

## Goal

Verify that grounded retrieval (RAG) never returns a source that falls outside the requesting user's permissions, and that permission enforcement holds across the knowledge layer and the foundation layer together.

## Preconditions

- Two documents: a public document and a restricted document, both indexed via `auto_client_acquisition/knowledge_os/`.
- Two users within the same tenant: one with permission to the restricted document and one without, via RBAC in the foundation layer.
- A cited-answer path via `auto_client_acquisition/knowledge_os/answer_with_citations.py`.

## Steps

1. Ask a question covered by the restricted document as the authorized user.
2. Record the cited sources.
3. Ask the same question as the unauthorized user.
4. Record the cited sources and the answer.
5. Check the audit log for both requests.

## Expected result

- Steps 1 and 2: the authorized user sees the restricted document among the sources.
- Steps 3 and 4: the unauthorized user does not see the restricted document; the answer is grounded only in the public document or abstains.
- Step 5: both requests are logged with no PII.

## Pass/fail criteria

- **Pass:** no restricted source appears for a user without permission, not even via a reworded question.
- **Fail:** any restricted source is returned, or its content leaks into the answer. A failure blocks the merge and caps Layers 4 and 1 at the client-pilot band.

## Related links

- `readiness/memory/readiness.md`
- `readiness/foundation/readiness.md`

Estimated value is not Verified value.
