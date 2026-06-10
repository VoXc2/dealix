# Procurement FAQ — Dealix (AR)

> **Format:** سؤال → جواب قصير + Evidence Reference. يُحدّث مع كل صفقة enterprise.

---

## Security & Privacy

**Q1: ما البيانات التي تعالجونها؟**
بيانات العميل التي يقدمها + metadata الاستخدام + بيانات الفوترة. لا نجمع بيانات أعمى ما لم تكن لغرض محدد وموثّق.
→ `PRIVACY_OVERVIEW_AR.md` §3, `DATA_HANDLING_OVERVIEW_AR.md` §2

**Q2: أين تُخزّن البيانات؟**
في PostgreSQL مُدار (Railway). Region يحدد في DPA لكل عميل. البيانات الحساسة لا تخرج السعودية بدون DPA + redaction.
→ `TECHNICAL_ARCHITECTURE_OVERVIEW_AR.md` §2

**Q3: من يصل إليها؟**
- موظفو Dealix المخوّلون (least privilege)
- Agents بصلاحيات محددة (Tier A2)
- Sub-processors في القائمة المُعلنة فقط

**Q4: كيف تديرون الأسرار؟**
- Env vars (لا في الـ repo)
- لا تُمرر لنماذج LLM
- Redaction middleware
- rotation policy مُخطط E3
→ `SECURITY_OVERVIEW_AR.md` §4

**Q5: كيف تتعاملون مع ملفات العميل؟**
Upload عبر portal مشفّر، تخزين معزول per-tenant، حذف عند termination.
→ `DATA_HANDLING_OVERVIEW_AR.md` §4

**Q6: هل الـ agents ترسل رسائل تلقائياً؟**
**لا.** أي إرسال خارجي (email/WhatsApp) يحتاج موافقة بشرية. الـ Agent يولد مسودة، المؤسس يعتمد، ثم يُرسل.
→ `docs/governance/APPROVAL_MATRIX.md`, `docs/governance/AI_ACTION_TAXONOMY.md`

**Q7: ما الموافقات الموجودة؟**
- إرسال أي رسالة
- تغيير pricing
- موافقة دفع
- تغيير workflow permissions
- deploy production
→ `docs/governance/APPROVAL_MATRIX.md`

**Q8: ماذا لو أخطأ AI؟**
- كل output يمر schema validation + eval
- Human-in-loop للإجراءات الخارجية
- Audit trail كامل
- Incident response runbook

**Q9: كيف تمنعون prompt injection؟**
- عزل البيانات غير الموثوقة في delimiters
- Allowlist actions فقط
- Output filtering
- Audit + red team
→ `docs/agents_wave3/AGENT_SECURITY_FRAMEWORK_AR.md`

**Q10: كيف تتعاملون مع الـ opt-outs؟**
Opt-out flag في كل entity. Suppression list مركزية. يطبق على الفور في الـ next batch.
→ `DATA_HANDLING_OVERVIEW_AR.md` §8

**Q11: كيف تحذفون البيانات؟**
- خلال 30 يوم من الطلب
- audit log entry
- confirmation للعميل
→ `DATA_HANDLING_OVERVIEW_AR.md` §7, `PRIVACY_OVERVIEW_AR.md` §6

## Integrations & Operations

**Q12: ما الـ integrations المدعومة؟**
WhatsApp, Email, HubSpot, Calendly, Moyasar, plus model providers per Agent 19 policy.
→ `INTEGRATION_OVERVIEW_AR.md`

**Q13: ما نموذج الدعم؟**
4 tiers (Standard, Priority, Enterprise, Embedded). تفاصيل في `SUPPORT_MODEL_AR.md`.

**Q14: ما خطوات الـ implementation؟**
1. Discovery + signoff (week 1)
2. Setup + permission grants (week 1–2)
3. Pilot workflows (week 2–4)
4. Scale + handover (week 4–8)
→ `IMPLEMENTATION_PLAN_TEMPLATE_AR.md`

**Q15: ما الـ SLAs/SLOs؟**
- Uptime: 99.5% (E3+)
- AI p95: < 10s
- API p95: < 500ms
→ `SLA_SLO_DRAFT_AR.md`

**Q16: ما هو خارج النطاق؟**
- Custom development for one client
- Ad-hoc consulting
- Multi-region sovereign (until E5)
- Highly regulated industries (until E5)
- Custom AI model training
→ `SUPPORT_MODEL_AR.md` §7

**Q17: ما مسؤولية العميل؟**
- Account credential security
- User permission grants
- Legal basis for their data
- Opt-out management
- Acceptable use

---

> **Owner:** Founder · **Reviewer:** Council
