# العربية

Owner: قائد جاهزية المؤسسة (Enterprise Readiness Lead)

## اختبار عابر للطبقات: الوكيل يستخدم ذاكرة المستأجر الصحيح فقط

الطبقات المشاركة: 1 (الأساس) + 2 (زمن تشغيل الوكيل) + 4 (الذاكرة والمعرفة).

## الهدف

التحقق من أن وكيلاً يعمل لمستأجر معيّن لا يقرأ ولا يكتب في ذاكرة مستأجر آخر، وأن عزل المستأجر يصمد عبر حدود الوكيل والذاكرة معاً.

## المتطلبات المسبقة

- مستأجران فاعلان: مستأجر-أ ومستأجر-ب، لكل منهما `tenant_id` مميز.
- ذاكرة منفصلة لكل مستأجر عبر `auto_client_acquisition/knowledge_os/` و`core/memory/`.
- وكيل مكوَّن عبر `auto_client_acquisition/agent_os/` يعمل ضمن حدود `secure_agent_runtime_os/four_boundaries.py`.

## الخطوات

1. اكتب سجل ذاكرة مميزاً لمستأجر-أ وآخر لمستأجر-ب.
2. شغّل الوكيل بهوية مستأجر-أ واطلب استرجاع ذاكرة.
3. سجّل ما يُعاد.
4. شغّل الوكيل بهوية مستأجر-أ واطلب صراحةً سجل مستأجر-ب.
5. اكتب سجلاً جديداً بهوية مستأجر-أ، ثم تحقق بهوية مستأجر-ب أنه غير ظاهر.

## النتيجة المتوقعة

- الخطوة 2 و3: الوكيل يرى سجل مستأجر-أ فقط.
- الخطوة 4: الطلب مرفوض على حدود البيانات في `four_boundaries.py`.
- الخطوة 5: سجل مستأجر-أ غير ظاهر لمستأجر-ب.

## معيار النجاح/الفشل

- **نجاح:** لا تسرّب في أي اتجاه؛ كل وصول عبر المستأجرين مرفوض ومُسجَّل.
- **فشل:** أي سجل عبر المستأجرين يظهر، أو أي طلب عبر المستأجرين يُقبَل. الفشل يوقف الدمج ويضع سقفاً على الطبقات 1 و2 و4 عند نطاق تجربة عميل.

## روابط ذات صلة

- `readiness/foundation/readiness.md`
- `readiness/agents/readiness.md`
- `readiness/memory/readiness.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Enterprise Readiness Lead

## Cross-layer test: an agent uses only the correct tenant's memory

Participating layers: 1 (Foundation) + 2 (Agent Runtime) + 4 (Memory & Knowledge).

## Goal

Verify that an agent operating for a given tenant does not read from or write to another tenant's memory, and that tenant isolation holds across the agent and memory boundaries together.

## Preconditions

- Two active tenants: tenant-A and tenant-B, each with a distinct `tenant_id`.
- Separate memory per tenant via `auto_client_acquisition/knowledge_os/` and `core/memory/`.
- An agent configured via `auto_client_acquisition/agent_os/` running inside the `secure_agent_runtime_os/four_boundaries.py` boundaries.

## Steps

1. Write a distinct memory record for tenant-A and another for tenant-B.
2. Run the agent as tenant-A and request a memory retrieval.
3. Record what is returned.
4. Run the agent as tenant-A and explicitly request tenant-B's record.
5. Write a new record as tenant-A, then verify as tenant-B that it is not visible.

## Expected result

- Steps 2 and 3: the agent sees only tenant-A's record.
- Step 4: the request is rejected on the data boundary in `four_boundaries.py`.
- Step 5: tenant-A's record is not visible to tenant-B.

## Pass/fail criteria

- **Pass:** no leak in either direction; every cross-tenant access is rejected and logged.
- **Fail:** any cross-tenant record appears, or any cross-tenant request is accepted. A failure blocks the merge and caps Layers 1, 2, and 4 at the client-pilot band.

## Related links

- `readiness/foundation/readiness.md`
- `readiness/agents/readiness.md`
- `readiness/memory/readiness.md`

Estimated value is not Verified value.
