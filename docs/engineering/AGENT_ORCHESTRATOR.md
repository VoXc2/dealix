# Agent Orchestrator — Engineering Notes

**استراتيجياً:** [`../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md`](../strategy/DEALIX_FULL_OPS_MASTER_PLAN_AR.md)  
**V12 قواعد صلبة:** [`../V12_FULL_OPS_ARCHITECTURE.md`](../V12_FULL_OPS_ARCHITECTURE.md)

## التصميم المستهدف

- **Orchestrator** واحد يقرر: أي وكيل يعمل، بأي **وضع تنفيذ** (`suggest_only` | `draft_only` | `approval_required` | `blocked`).  
- **Policies** ثابتة (YAML + كود): موافقات، ممنوعات، حدود أدوات.  
- **Evidence** لكل تشغيل: مصادر، قرر السياسة، نتيجة، معرف موافقة إن وُجد.  
- **Observability / evaluation**: سجلات تشغيل، تقييم جودة مسودات، بدون «إرسال حي» افتراضياً.

## مرجع خارجي (تشغيلي)

وثائق منصات الوكلاء (مثل OpenAI Agents) تفصل orchestration وguardrails والتكاملات والمراقبة والتقييم — يدعم فصل **التنسيق** عن **التنفيذ** وربط **الحوكمة** كطبقة أولى وليست لاحقة.

## ارتباط داخلي

- WorkItem / Full Ops: `auto_client_acquisition/full_ops/`  
- صلاحيات الوكلاء المرجعية: [`../../dealix/config/agent_permissions.yaml`](../../dealix/config/agent_permissions.yaml)

## ممنوعات (غير قابلة للمناقشة)

لا live send · لا live charge · لا cold WhatsApp · لا LinkedIn automation · لا scraping · لا fake proof.
