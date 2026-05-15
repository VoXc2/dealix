# العربية

**Owner:** المالك التجاري (Commercial Owner) — بالتنسيق مع مالك طبقة الحوكمة.

## سياسة التواصل مع العملاء

تحدّد هذه السياسة كيف تُنشأ المراسلات الموجّهة للعملاء وتُراجَع وتُرسَل. المبدأ الحاكم: الذكاء الاصطناعي يصوغ مسوّدة، والإنسان يراجع ويوافق، والنظام يرسل بعد الموافقة فقط.

**الإصدار:** 1.0 — **تاريخ السريان:** 2026-05-15 — **المراجعة التالية:** 2026-08-15.

### المبدأ الحاكم: مسوّدة أولاً

كل رسالة موجّهة لطرف خارجي — بريد، عرض، رد — تُنشأ كمسوّدة فقط (draft-only). لا يرسل النظام أي رسالة خارجية نيابة عن العميل دون موافقته الصريحة الموثَّقة. تُطبَّق هذه القاعدة عبر `auto_client_acquisition/governance_os/draft_gate.py` وقاعدة `external_action_requires_approval`.

### القنوات المسموحة

- البريد الإلكتروني عبر مزوّد متعاقَد، بعد موافقة على المسوّدة.
- المراسلات داخل علاقة قائمة وبأساس نظامي مُسجَّل.

### القنوات الممنوعة

- رسائل واتساب باردة غير مطلوبة (قاعدة `no_cold_whatsapp`).
- أتمتة LinkedIn أو الرسائل الجماعية عبره (قاعدة `no_linkedin_automation`).
- أي تواصل جماعي بلا أساس نظامي مُسجَّل.

### قواعد المحتوى

- لا ادعاء إثبات أو أرقام بلا مصدر موثَّق (قاعدة `no_fake_proof`).
- لا وعد نتائج أو مبيعات مضمونة (قاعدة `no_guaranteed_claims`)؛ تُستخدم صياغة "فرص مُثبتة بأدلة".
- كل دراسات الحالة غير المسماة تُوسَم صراحةً "نموذج افتراضي آمن".
- لا إجابة موجّهة للعميل بلا مصدر (قاعدة `no_source_no_answer`).
- القيمة التقديرية تُوصَف دائماً بأنها تقديرية لا مُتحقَّقة.

### آلية الموافقة

1. يصوغ الوكيل مسوّدة الرسالة.
2. تمر المسوّدة عبر محرّك السياسات؛ أي مخالفة محتوى تُحجب.
3. الإجراء الخارجي يُرفع لمحرّك الموافقات؛ تصنيف الموافقة حسب القناة والجمهور (راجع `governance/approval_rules/sales_approval_rules.md`).
4. عند موافقة المراجع فقط يُرسَل المحتوى.
5. كل خطوة تُسجَّل كقيد تدقيق.

### الحوكمة

- لا قناة جديدة تُفعَّل دون مراجعة قانونية وأساس نظامي.
- مراجعة السياسة ربع سنوية.
- أي إرسال دون موافقة يُرفع كحادث حوكمة فوري.

انظر أيضاً: `governance/approval_rules/sales_approval_rules.md`، `governance/policies/ai_usage_policy.md`.

---

# English

**Owner:** Commercial Owner — in coordination with the Governance Platform Lead.

## Customer Communication Policy

This policy defines how customer-facing communications are created, reviewed, and sent. The governing principle: AI drafts, a human reviews and approves, and the system sends only after approval.

**Version:** 1.0 — **Effective:** 2026-05-15 — **Next review:** 2026-08-15.

### Governing principle: draft-first

Every message to an external party — email, proposal, reply — is created draft-only. The system never sends an external message on a customer's behalf without their explicit, documented approval. This rule is enforced via `auto_client_acquisition/governance_os/draft_gate.py` and the `external_action_requires_approval` rule.

### Permitted channels

- Email via a contracted provider, after approval of the draft.
- Correspondence within an existing relationship and with a recorded lawful basis.

### Forbidden channels

- Unsolicited cold WhatsApp messages (`no_cold_whatsapp` rule).
- LinkedIn automation or bulk messaging on it (`no_linkedin_automation` rule).
- Any bulk outreach without a recorded lawful basis.

### Content rules

- No proof claim or numbers without a documented source (`no_fake_proof` rule).
- No promise of guaranteed results or sales (`no_guaranteed_claims` rule); "evidenced opportunities" phrasing is used.
- Every unnamed case study is explicitly labeled "hypothetical, case-safe template".
- No customer-facing answer without a source (`no_source_no_answer` rule).
- Estimated value is always described as estimated, not verified.

### Approval mechanism

1. The agent drafts the message.
2. The draft passes through the Policy Engine; any content breach is blocked.
3. The external action is raised to the Approval Engine; the approval class depends on channel and audience (see `governance/approval_rules/sales_approval_rules.md`).
4. Only on reviewer approval is the content sent.
5. Every step is recorded as an audit entry.

### Governance

- No new channel is activated without a legal review and a lawful basis.
- The policy is reviewed quarterly.
- Any send without approval is raised as an immediate governance incident.

See also: `governance/approval_rules/sales_approval_rules.md`, `governance/policies/ai_usage_policy.md`.
