# العربية

## مواصفة الاختبار — الطبقة الخامسة (الحوكمة)

Owner: مالك طبقة الحوكمة (Governance Platform Lead)

### الغرض

تحدّد هذه المواصفة حالات الاختبار ومعايير القبول لطبقة الحوكمة. هي مواصفة مكتوبة لا تحتوي كوداً.

### حالات الاختبار

#### G-T1 — تصنيف مخاطر لكل إجراء

- خطوات: تمرير مجموعة إجراءات متنوعة عبر `classify()` في `dealix/classifications/__init__.py`.
- القبول: كل إجراء يعود بتصنيف A/R/S؛ لا إجراء بلا تصنيف.

#### G-T2 — التصنيف الافتراضي للمجهول

- خطوات: تمرير إجراء غير معروف بلا تصنيف مسبق.
- القبول: يُسند له افتراضياً A2/R2/S2 ولا يُنفَّذ آلياً (fail-closed).

#### G-T3 — حجب الإجراءات غير العكوسة

- خطوات: تمرير إجراء بتصنيف R3 أو مدرج في `NEVER_AUTO_EXECUTE`.
- القبول: محرّك السياسات يعيد `require_approval`؛ لا تنفيذ آلي إطلاقاً.

#### G-T4 — القواعد غير القابلة للتفاوض

- خطوات: تمرير محتوى يحوي ادعاء إثبات بلا مصدر، ووعد نتائج مضمونة، ووصف استخراج بيانات.
- القبول: تُفعَّل `no_fake_proof` و`no_guaranteed_claims` و`no_scraping` وتعيد `block`.

#### G-T5 — منع أتمتة القنوات الباردة

- خطوات: تمرير إجراء أتمتة LinkedIn وإجراء واتساب بارد.
- القبول: `no_linkedin_automation` و`no_cold_whatsapp` تعيدان `block`.

#### G-T6 — الإجراء الخارجي يتطلب موافقة

- خطوات: اقتراح إجراء خارجي مواجِه للعميل دون موافقة.
- القبول: تُفعَّل `external_action_requires_approval` ويُعرض الإجراء كمسوّدة فقط؛ لا إرسال.

#### G-T7 — الموافقة المزدوجة للإجراءات A3

- خطوات: رفع إجراء A3 للموافقة ومنح موافقة مراجع واحد فقط.
- القبول: الإجراء يبقى `pending` حتى اكتمال مراجعَين مختلفَين؛ لا تفويض ذاتي.

#### G-T8 — انتهاء مهلة الموافقة

- خطوات: ترك طلب موافقة دون بتّ حتى انتهاء مدته.
- القبول: الطلب يصبح `expired` ويُعامل كرفض؛ لا تنفيذ.

#### G-T9 — قيد تدقيق لكل قرار وموافقة

- خطوات: تنفيذ سلسلة تقييمات سياسة وموافقات وفحص سجل التدقيق.
- القبول: لكل قرار وموافقة قيد `AuditEntry` غير قابل للتعديل يحوي الفاعل والإجراء والتصنيف والقرار و`decision_id`.

#### G-T10 — تعذّر التلاعب بسجل التدقيق

- خطوات: محاولة تعديل أو حذف قيد تدقيق عبر الواجهة.
- القبول: لا واجهة تتيح التعديل أو الحذف؛ التصحيح يتم بقيد جديد فقط.

#### G-T11 — منع البيانات الشخصية في السجلات

- خطوات: تمرير إجراء يحوي معرّفاً شخصياً وفحص السجلات وقيود التدقيق.
- القبول: تُفعَّل `no_pii_in_logs`؛ لا يظهر معرّف شخصي خام.

#### G-T12 — السياسة لها مالك وإصدار

- خطوات: فحص كل قاعدة في `default_registry.yaml`.
- القبول: لكل قاعدة مُعرّف وإصدار ومالك مسمّى؛ لا قاعدة ناقصة.

#### G-T13 — تصنيف S3 يستوجب التحقق من الأساس النظامي

- خطوات: تمرير إجراء يمسّ بيانات شخصية S3.
- القبول: يُطلب التحقق من الأساس النظامي في `dealix/registers/compliance_saudi.yaml` قبل المتابعة.

### معايير القبول الشاملة

- جميع حالات G-T1 إلى G-T13 ناجحة قبل أي نشر للإنتاج.
- 100% من الإجراءات عالية المخاطر تتطلب موافقة موثَّقة.
- 100% من القواعد تحمل مالكاً وإصداراً.
- التكامل المستمر يحجب الدمج عند فشل أي حالة.

### الروابط ذات الصلة

- `platform/governance/readiness.md`
- `platform/governance/architecture.md`
- `governance/approval_rules/`

# English

## Test Specification — Layer 5 (Governance)

Owner: Governance Platform Lead

### Purpose

This specification defines test cases and acceptance criteria for the Governance layer. It is a written spec and contains no code.

### Test cases

#### G-T1 — Risk classification per action

- Steps: pass a varied set of actions through `classify()` in `dealix/classifications/__init__.py`.
- Acceptance: every action returns an A/R/S classification; no action is unclassified.

#### G-T2 — Default classification of the unknown

- Steps: pass an unknown action with no prior classification.
- Acceptance: it is defaulted to A2/R2/S2 and does not auto-execute (fail-closed).

#### G-T3 — Blocking irreversible actions

- Steps: pass an action classified R3 or listed in `NEVER_AUTO_EXECUTE`.
- Acceptance: the Policy Engine returns `require_approval`; never any auto-execution.

#### G-T4 — Non-negotiable rules

- Steps: pass content containing a proof claim without a source, a guaranteed-results promise, and a data-extraction description.
- Acceptance: `no_fake_proof`, `no_guaranteed_claims`, and `no_scraping` fire and return `block`.

#### G-T5 — Blocking cold-channel automation

- Steps: pass a LinkedIn automation action and a cold WhatsApp action.
- Acceptance: `no_linkedin_automation` and `no_cold_whatsapp` return `block`.

#### G-T6 — External action requires approval

- Steps: propose an external, customer-facing action without approval.
- Acceptance: `external_action_requires_approval` fires and the action is presented draft-only; no send.

#### G-T7 — Dual approval for A3 actions

- Steps: raise an A3 action for approval and grant only one reviewer's approval.
- Acceptance: the action stays `pending` until two distinct reviewers complete; no self-approval.

#### G-T8 — Approval timeout

- Steps: leave an approval request undecided until its TTL elapses.
- Acceptance: the request becomes `expired` and is treated as a rejection; no execution.

#### G-T9 — Audit entry per decision and approval

- Steps: run a chain of policy evaluations and approvals and inspect the audit log.
- Acceptance: every decision and approval has an immutable `AuditEntry` holding actor, action, classification, decision, and `decision_id`.

#### G-T10 — Audit log tamper-evidence

- Steps: attempt to edit or delete an audit entry via the interface.
- Acceptance: no interface allows edit or delete; correction is only by a new entry.

#### G-T11 — No personal data in logs

- Steps: pass an action containing a personal identifier and inspect logs and audit entries.
- Acceptance: `no_pii_in_logs` fires; no raw personal identifier appears.

#### G-T12 — Policy has an owner and version

- Steps: inspect every rule in `default_registry.yaml`.
- Acceptance: every rule has an id, version, and named owner; no incomplete rule.

#### G-T13 — S3 classification requires lawful-basis verification

- Steps: pass an action touching S3 personal data.
- Acceptance: lawful-basis verification in `dealix/registers/compliance_saudi.yaml` is required before proceeding.

### Overall acceptance criteria

- All cases G-T1 through G-T13 pass before any production deploy.
- 100% of high-risk actions require a documented approval.
- 100% of rules carry an owner and version.
- CI blocks merge on any failing case.

### Related docs

- `platform/governance/readiness.md`
- `platform/governance/architecture.md`
- `governance/approval_rules/`
