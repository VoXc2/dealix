# حدود الموافقة البشرية — Human Approval Boundaries
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 + Security · **اللغة:** العربية · **الدليل:** L1 internal.

> **مبدأ:** «كل إجراء ذي أثر خارجي أو مالي أو قانوني يحتاج مؤسس. كل قراءة أو مسودة داخلية لا تحتاج.»
> — Dealix Hard Constraint (L0).

---

## 1) ما يحتاج دائمًا موافقة بشرية (Always-Approve)

| الإجراء | المُعتمد | الأصول المطلوبة | الملاحظات |
|---|---|---|---|
| **إرسال خارجي** (email, WhatsApp, SMS, publish) | المؤسس | `draft` + `evidence_level ≥ L3` + `suppression_check` | لا cold outreach بدون ICP مُتحقَّق |
| **دفع مالي** (payment link, invoice send) | المؤسس | `terms` + `legal_review` | عبر Moyasar gateway فقط |
| **عقد/اتفاقية** (contract, ToS) | المؤسس + Legal | `draft` + `dpa_check` | **ممنوع** autonomous نهائيًا |
| **ترقية نموذج** (model promotion) | المؤسس + Agent #30 | `eval_report` + `drift_analysis` | قبل أي deployment |
| **تغيير schema في production** | المؤسس | `migration_plan` + `rollback_plan` | Alembic head check |
| **وصول للأسرار** (secret access) | المؤسس + Security | `justification` + `time_boxed_token` | A5 ممنوع |
| **تصدير بيانات عميل** (customer data export) | المؤسس + Legal | `pilot_contract` + `redaction_proof` | PDPL compliance |
| **نشر عام** (public blog, social) | المؤسس | `content` + `claim_safety_check` | Evidence L3+ |
| **حذف بيانات** (data delete) | المؤسس | `audit_trail` | PDPL/Right to Erasure |
| **نقل بيانات عبر الحدود** (cross-border) | المؤسس + Legal | `transfer_addendum` | انظر `docs/security/CROSS_BORDER_TRANSFER_ADDENDUM.md` |
| **Promote agent to A4** | المؤسس | `30-day A3 track record` + `audit_pass` | |
| **Onboarding vendor AI** | المؤسس + Legal | `vendor_due_diligence` | |

---

## 2) ما لا يحتاج موافقة (Auto-Allow)

| الإجراء | الشروط |
|---|---|
| قراءة وثيقة داخلية | ضمن `docs/`/`data/`/`schemas/`/`reports/` |
| قراءة ملف عام | في `docs/public/` |
| إنشاء مسودة (draft) | في `reports/`/`docs/`/`data/` (غير production) |
| تلخيص/تصنيف/استخراج | على بيانات داخلية |
| تقييم سلوكي (eval run) | في pipeline التقييم |
| كتابة سجل تدقيق (audit event) | تلقائي |
| تسجيل وكيل في `agent_registry.jsonl` | بعد onboarding كامل |
| إضافة eval record | في `agent_evals.jsonl` |
| قراءة KPIs من dashboards | read-only |

---

## 3) متطلبات واجهة الموافقة (UI/UX)

### 3.1 قناة الموافقة
- **افتراضي:** `/[locale]/ops/approvals` (Dealix Founder Cockpit)
- **بديل:** Mobile push + email + Slack/Feishu (للمؤسس)
- **شرط:** يجب أن يكون المُعتمد متاحًا (online) أو من ينوب عنه

### 3.2 الأصول المرفقة
- **دائمًا:** draft كامل (preview) + risk_level + evidence_level
- **للعالي الخطورة:** justification + counterfactual + rollback plan
- **للدفع/العقد:** legal review status + DPA status

### 3.3 صيغة الطلب (Approval Request)
```yaml
approval_request:
  id: "APR-20260603-0001"
  agent_id: "AGENT-FIN-001"
  action: "send_invoice"
  risk_level: "high"
  requester: "AGENT-FIN-001"
  approver: "founder"
  timestamp: "2026-06-03T08:30:00Z"
  justification: "Pilot delivery invoice for ACME."
  artifacts:
    draft: "invoices/ACME_2026-06.json"
    evidence_level: "L4"
    pilot_contract: "data/contracts/ACME_pilot_2026.pdf"
  compliance_checks:
    suppression_check: "passed"
    icp_verified: true
    consent_record: "CRM-CONSENT-12345"
  status: "pending"
  timeout_at: "2026-06-03T20:30:00Z"
  response: null
```

### 3.4 سجل الموافقة
- كل موافقة تُسجَّل في `data/ai_governance/audit_log.jsonl`
- تحتوي: `approval_id`, `approver_id`, `decision`, `timestamp`, `notes`

---

## 4) سياسة المهلة (Approval Timeout)

| مستوى الخطر | المهلة | الإجراء عند انتهاء المهلة |
|---|---|---|
| Low | 24 ساعة | تصعيد للمالك |
| Medium | 4 ساعات | تصعيد + reminder |
| High | 1 ساعة | **إلغاء تلقائي** + تسجيل |
| Critical | 15 دقيقة | **إلغاء تلقائي** + تسجيل + P1 إن تكرر |

> **القاعدة:** لا تنفيذ بعد انتهاء المهلة. الإجراء يحتاج طلبًا جديدًا.

### 4.1 الاستثناءات
- **حالة طوارئ مُعتمدة** (Emergency Exception): المُؤسس يُعطي pre-approval لفئة إجراءات — كل تنفيذ يُسجَّل بعلامة `emergency=true`، يحتاج post-incident review.
- **Override مع توثيق**: موافقة واحدة مع توثيق صريح تُلغي المهلة (يُسجَّل في audit).

---

## 5) حدود صلاحية المُعتمد (Approver Authority)

| الشخص | يمكنه الموافقة على |
|---|---|
| **المؤسس** | كل شيء |
| **Department Head** | low + medium (داخل قسمه) |
| **Agent #30** | لا موافقة (مراجعة فقط) |
| **Security Lead** | security-related (مثل secret access) |
| **Legal** | legal/contract/DPA/PDPL |
| **MLOps** | model promotion (مع المؤسس) |

> **القاعدة:** لا أحد يوافق على إجراء يخص نفسه (segregation of duties).

---

## 6) الربط

- [`../security/EXTERNAL_ACTION_APPROVAL_POLICY.md`](../security/EXTERNAL_ACTION_APPROVAL_POLICY.md)
- [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)
- [`../governance/APPROVAL_POLICY.md`](../governance/APPROVAL_POLICY.md)
- [`../governance/HUMAN_IN_THE_LOOP_MATRIX.md`](../governance/HUMAN_IN_THE_LOOP_MATRIX.md)
- [`AGENT_AUTONOMY_LEVELS_AR.md`](AGENT_AUTONOMY_LEVELS_AR.md)
- [`AGENT_PERMISSION_LIFECYCLE_AR.md`](AGENT_PERMISSION_LIFECYCLE_AR.md)

---

## 7) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | Always-Approve + Auto-Allow + UI/UX + Timeout |
