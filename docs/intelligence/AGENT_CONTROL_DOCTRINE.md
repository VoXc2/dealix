# Agent Control Doctrine — عقيدة ضبط الوكلاء

**قاعدة:** لا يوجد agent بلا **بطاقة هوية**، **حوكمة وقت تشغيل**، **سجل تشغيل**، و**مسار موافقة بشري** حيث ينطبق.

## كل agent يجب أن يحدد

- **identity** · **owner**  
- **permissions** · **autonomy level**  
- **tool access** · **allowed outputs** · **forbidden actions**  
- **audit** · **eval** · **decommission rule**  

## لماذا التصميم وليس الـ prompt فقط؟

سلوك الوكلاء **path-dependent** — لا يمكن حوكمه بالكامل عند التصميم فقط؛ السياسات تُقيَّم على **المسار الجزئي**، **الفعل المقترح**، **حالة المؤسسة**، وهوية الـ agent. مرجع أكاديمي: [Runtime Governance for AI Agents: Policies on Paths (arXiv:2603.16586)](https://arxiv.org/abs/2603.16586).

طبقات **حوكمة تشغيلية** حديثة تقترح دمج **system-of-record**، **تحقق قائم على أدلة**، **تسجيل تفسير قرار وقت التشغيل**، **telemetry**، **كشف انحراف**، **تصعيد حوكمة** — انظر [AI Governance Control Stack for Operational Stability (arXiv:2604.03262)](https://arxiv.org/abs/2604.03262).

**تنفيذ Dealix:** [`../governance/AGENT_REGISTRY.md`](../governance/AGENT_REGISTRY.md) · [`../product/AGENT_LIFECYCLE_MANAGEMENT.md`](../product/AGENT_LIFECYCLE_MANAGEMENT.md) · [`../governance/AI_RUN_LEDGER.md`](../governance/AI_RUN_LEDGER.md) · MI9 كإطار تشغيلي مكمل: [arXiv:2508.03858](https://arxiv.org/abs/2508.03858)
