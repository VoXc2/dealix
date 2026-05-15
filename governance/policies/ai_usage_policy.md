# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة.

## سياسة استخدام الذكاء الاصطناعي

تحدّد هذه السياسة كيف يُستخدم الذكاء الاصطناعي داخل Dealix، وما الذي يُسمح به، وما الذي يُمنع. السياسة قابلة للإصدار، ومراجعتها ربع سنوية أو عند أي تحديث تنظيمي.

**الإصدار:** 1.0 — **تاريخ السريان:** 2026-05-15 — **المراجعة التالية:** 2026-08-15.

### المبدأ الحاكم

وكلاء الذكاء الاصطناعي في Dealix يعملون بصفة **مراقب وموصٍ** فقط. هم يقترحون ولا يلتزمون نيابة عن العميل. كل إجراء خارجي مواجِه للعميل يُعرض كمسوّدة، ولا يُنفَّذ إلا بعد موافقة بشرية موثَّقة.

### الاستخدامات المسموحة

- تحليل البيانات الداخلية وتلخيصها وترتيب أولوياتها.
- صياغة مسوّدات للمراسلات والعروض لمراجعة بشرية.
- تصنيف الفرص حسب الأدلة المتوفرة.
- اقتراح الإجراء التالي مع ذكر الأساس والمصدر.

### الاستخدامات الممنوعة منعاً غير قابل للتفاوض

- ادعاء إثبات أو أرقام بلا مصدر موثَّق (قاعدة `no_fake_proof`).
- وعد نتائج أو مبيعات أو معدلات تحويل مضمونة (قاعدة `no_guaranteed_claims`)؛ تُستبدل بـ "فرص مُثبتة بأدلة".
- استخراج بيانات غير مرخّص (قاعدة `no_scraping`).
- أتمتة LinkedIn (قاعدة `no_linkedin_automation`).
- رسائل واتساب باردة غير مطلوبة (قاعدة `no_cold_whatsapp`).
- كتابة بيانات شخصية خام في السجلات (قاعدة `no_pii_in_logs`).
- تنفيذ أي إجراء خارجي دون موافقة (قاعدة `external_action_requires_approval`).
- إصدار إجابة موجّهة للعميل بلا مصدر (قاعدة `no_source_no_answer`).

### الحوكمة والتنفيذ

- كل القواعد أعلاه مفعّلة في `auto_client_acquisition/governance_os/rules/` ومُسجَّلة في `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- كل إجراء يمر عبر محرّك السياسات قبل التنفيذ؛ لا استثناء.
- الإجراءات عالية المخاطر تمر عبر مسار الموافقة في `dealix/trust/approval.py`.
- كل قرار يُسجَّل في سجل التدقيق `dealix/trust/audit.py`.
- لكل قاعدة مالك مسمّى وإصدار؛ تعديل أي قاعدة يتطلب موافقة مالك الطبقة وقيد تدقيق.

### مسؤوليات

- مالك الطبقة: صيانة السياسة والقواعد ومراجعتها الدورية.
- المراجع البشري: البتّ في الإجراءات المرفوعة وتوثيق سببه.
- كل مستخدم: عدم محاولة تجاوز محرّك السياسات.

### الإبلاغ عن الانتهاكات

أي مخرَج يخالف هذه السياسة يُرفع كحادث حوكمة فوري لمالك الطبقة، ويُسجَّل، ويُراجَع ضمن المراجعة الربع سنوية.

انظر أيضاً: `platform/governance/policy_engine.md`، `docs/DEALIX_OPERATING_CONSTITUTION.md`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## AI Usage Policy

This policy defines how AI is used inside Dealix, what is permitted, and what is forbidden. The policy is versioned, and reviewed quarterly or on any regulatory update.

**Version:** 1.0 — **Effective:** 2026-05-15 — **Next review:** 2026-08-15.

### Governing principle

Dealix AI agents act strictly as **observer and recommender**. They propose and do not commit on a customer's behalf. Every external, customer-facing action is presented as a draft and is executed only after a documented human approval.

### Permitted uses

- Analyzing, summarizing, and prioritizing internal data.
- Drafting correspondence and proposals for human review.
- Classifying opportunities by available evidence.
- Recommending the next action with its rationale and source.

### Forbidden uses (non-negotiable)

- Claiming proof or numbers without a documented source (`no_fake_proof` rule).
- Promising guaranteed results, sales, or conversion rates (`no_guaranteed_claims` rule); replaced with "evidenced opportunities".
- Unauthorized data extraction (`no_scraping` rule).
- LinkedIn automation (`no_linkedin_automation` rule).
- Unsolicited cold WhatsApp messages (`no_cold_whatsapp` rule).
- Writing raw personal data to logs (`no_pii_in_logs` rule).
- Executing any external action without approval (`external_action_requires_approval` rule).
- Issuing a customer-facing answer without a source (`no_source_no_answer` rule).

### Governance and enforcement

- All rules above are active in `auto_client_acquisition/governance_os/rules/` and registered in `auto_client_acquisition/governance_os/policies/default_registry.yaml`.
- Every action passes through the Policy Engine before execution; no exception.
- High-risk actions pass through the approval path in `dealix/trust/approval.py`.
- Every decision is recorded in the audit log `dealix/trust/audit.py`.
- Every rule has a named owner and a version; changing a rule requires the layer owner's approval and an audit entry.

### Responsibilities

- Layer owner: maintains the policy and rules and runs the periodic review.
- Human reviewer: decides on raised actions and documents the reason.
- Every user: does not attempt to bypass the Policy Engine.

### Reporting violations

Any output that breaches this policy is raised as an immediate governance incident to the layer owner, recorded, and reviewed in the quarterly review.

See also: `platform/governance/policy_engine.md`, `docs/DEALIX_OPERATING_CONSTITUTION.md`.
