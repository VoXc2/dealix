# AI Control Plane — خريطة التنفيذ (Dominance)

**لماذا؟** Agentic AI يوسّع مساحة الهجوم: tool calls · prompt injection · retrieval poisoning · صلاحيات وكلاء · مسارات خارجية.

بحث حديث يقترح **طبقات حوكمة وقت التنفيذ** (sandboxing، تحقق نية، تفويض صفري الثقة بين الوكلاء، وسجلات تدقيق غير قابلة للتلاعب) — في تقييم pipeline داخلي بلغت الطبقات مجتمعة نحو **96%** اعتراضًا لمسارات ضارة في عينة التقييم — انظر [Governance Architecture for Autonomous Agent Systems (arXiv:2603.07191)](https://arxiv.org/abs/2603.07191).

---

## مكوّنات مرجعية

Agent Registry · LLM Gateway · Prompt Registry · Model Router · Cost Guard · Eval Runner · AI Run Ledger · Policy Engine · Approval Engine · Audit Export · Kill Switch (لاحقًا)

---

## قواعد تشغيلية

- No agent without identity  
- No tool access without permission  
- No external action without approval  
- No run without log  
- No high-risk workflow without governance  

**مراجع:** [`../trust/AI_CONTROL_PLANE.md`](../trust/AI_CONTROL_PLANE.md) · [`../enterprise/AI_CONTROL_PLANE.md`](../enterprise/AI_CONTROL_PLANE.md)

**صعود:** [`GOVERNANCE_RUNTIME_PRODUCT.md`](GOVERNANCE_RUNTIME_PRODUCT.md)
