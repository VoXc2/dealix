# دورة حياة صلاحيات الوكلاء — Agent Permission Lifecycle
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 · **اللغة:** العربية · **الدليل:** L1 internal.

> **مبدأ:** «كل صلاحية لها مالك، تاريخ انتهاء، سجل تدقيق، ومحفز مراجعة. لا توجد صلاحية عالية الخطورة دائمة.»
> — Dealix Hard Constraint (L0).

---

## 1) المراحل الثماني

```
requested → reviewed → approved → active → monitored → expired/renewed → revoked → audited
```

### 1.1 Requested (مطلوبة)
- **الفاعل:** مالك الوكيل (Department Head) أو Agent #30
- **المخرجات:** `permission_request.json` يحتوي: `agent_id`, `scope`, `justification`, `requested_duration_days`, `evidence_link`
- **الدليل المطلوب:** L1 (وثيقة داخلية) + تقييم risk_classifier
- **السجل:** `data/ai_governance/agent_permissions.jsonl` بـ `status=pending`

### 1.2 Reviewed (قيد المراجعة)
- **الفاعل:** Agent #30 (AI Governance) + Security (للصلاحيات عالية الخطورة)
- **المخرجات:** `review_notes.md` + `risk_assessment.yaml`
- **الدليل المطلوب:** L1 + مقارنة مع [`AGENT_AUTONOMY_LEVELS_AR.md`](AGENT_AUTONOMY_LEVELS_AR.md) للتأكد من توافق الصلاحية مع المستوى
- **السجل:** تحديث `status=under_review` + append `review_event` في الـ JSONL

### 1.3 Approved (معتمدة)
- **الفاعل:** المؤسس (لـ high risk) أو المالك (لـ low/medium)
- **المخرجات:** `approval_token` (موقّع رقميًا) + `approval_record.json`
- **الدليل المطلوب:** L2 (نتائج اختبار) للقدرات الحساسة
- **السجل:** `status=active`، `granted_at=now`، `expires_at=now+duration`

### 1.4 Active (نشطة)
- **الفاعل:** الوكيل (التنفيذ) + runtime policy engine (التطبيق)
- **المخرجات:** كل استخدام يُسجَّل في `audit_event.schema.json`
- **الدليل المطلوب:** logs تلقائية
- **السجل:** كل write/send/network call → `audit_event` بـ `agent_id, action, target, result, evidence_hash`

### 1.5 Monitored (مراقبة)
- **الفاعل:** Agent #30 + eval pipeline
- **المخرجات:** `monitoring_dashboard.json` يومي
- **الدليل المطلوب:** نتائج التقييمات الدورية (انظر `AGENT_EVAL_CADENCE_AR.md`)
- **السجل:** `agent_evals.jsonl` بوتيرة محددة

### 1.6 Expired/Renewed (منتهية/مُجدَّدة)
- **Expired:** عند `expires_at`، تتحول تلقائيًا إلى `status=expired`
- **Renewed:** طلب جديد قبل الانتهاء بـ 14 يوم
  - **الدليل المطلوب:** L1 + L2 لتجديد high-risk (إعادة تقييم)
  - **السجل:** صف جديد بـ `granted_at=now` و `status=active` (الصف القديم يبقى `expired`)

### 1.7 Revoked (مُسحوبة)
- **المحفزات (Revocation Triggers):**
  1. حادث P0/P1 (فوري، تلقائي)
  2. خرق policy (فوري)
  3. انتهاء الـ duration دون تجديد
  4. قرار المالك أو Agent #30
  5. scope drift مكتشف
  6. ترقية/تخفيض autonomy level
- **الفاعل:** Agent #30 / Incident Commander / المؤسس
- **المخرجات:** `revocation_token` + `incident_link`
- **السجل:** `status=revoked`، `revoked_at=now`، `revoked_by=...`، `reason=...`

### 1.8 Audited (مدققة)
- **الفاعل:** Agent #30 (ربع سنوي) + Security (سنوي)
- **المخرجات:** `audit_report.md` مع جدول: granted/active/expired/revoked لكل permission_id
- **الدليل المطلوب:** جميع السجلات المرتبطة (logs, evals, incidents)
- **السجل:** `data/ai_governance/audit_log.jsonl` (إن وُجد) أو JSONL منفصل للـ audit

---

## 2) لا توجد صلاحيات عالية الخطورة دائمة

| نوع الصلاحية | المدة القصوى | التجديد |
|---|---|---|
| قراءة فقط (Read) | 365 يوم | تلقائي + spot-check |
| كتابة مسودة (Draft) | 90 يوم | يدوي |
| شبكة على نطاق مسموح (Network allowlist) | 30 يوم | يدوي + اختبار |
| إرسال خارجي (External Send) | **معاملة واحدة فقط** | لا تجديد — معاملة جديدة |
| بيانات عميل (Customer Data) | مدة pilot أو 30 يوم | مرتبط بـ contract |
| أسرار (Secrets — A4 فقط) | 15 دقيقة token | لا تجديد — token جديد |
| نشر/محتوى عام | معاملة واحدة | لا تجديد |

---

## 3) وتيرة التجديد (Renewal Cadence) حسب مستوى الخطر

| Risk Level | وتيرة التقييم | وتيرة تجديد الصلاحية |
|---|---|---|
| **Low** | شهري | 180 يوم |
| **Medium** | أسبوعي | 90 يوم |
| **High** | يومي | 30 يوم |
| **Critical** | مستمر (real-time) | **معاملة واحدة** (لا تجديد) |

---

## 4) محفزات الإلغاء (Revocation Triggers) — قائمة شاملة

| الرمز | المحفز | الإجراء | الإطار الزمني |
|---|---|---|---|
| REV-INC-01 | حادث P0/P1 | إلغاء + تخفيض A-level | فوري |
| REV-INC-02 | حادث P2 | إعادة مراجعة | 7 أيام |
| REV-POL-01 | خرق policy موثّق | إلغاء + تحقيق | فوري |
| REV-SCOPE-01 | scope drift مكتشف | تضييق أو إلغاء | 14 يوم |
| REV-MODEL-01 | ترقية نموذج بدون إعادة تقييم | إلغاء، إعادة تقييم | 30 يوم |
| REV-OWNER-01 | تغيّر المالك بدون إعادة توقيع | إلغاء، مطالبة | فوري |
| REV-CUST-01 | انتهاء pilot | إلغاء + حذف PII | 30 يوم |
| REV-LEGAL-01 | تغيير في PDPL/تنظيمي | مراجعة شاملة | 30 يوم |
| REV-TIME-01 | انتهاء duration بدون تجديد | تحويل لـ expired | تلقائي |

---

## 5) صيغة سجل التدقيق (Audit Trail Format)

كل تغيير في الصلاحية يُسجَّل في `data/ai_governance/audit_log.jsonl` (JSONL) بالصيغة:

```json
{
  "audit_id": "AUD-20260603-0001",
  "timestamp": "2026-06-03T08:30:00Z",
  "actor": "agent_30",
  "actor_type": "human|agent|system",
  "action": "permission_granted|permission_revoked|permission_renewed|permission_expired|permission_reviewed",
  "permission_id": "PERM-20260603-0001",
  "agent_id": "AGENT-SEC-001",
  "scope": "network:api.moyasar.com",
  "evidence_level": "L1",
  "evidence_link": "docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md#approved",
  "previous_status": "pending",
  "new_status": "active",
  "notes": "First-time grant for invoicing agent."
}
```

**حقول إلزامية:** `audit_id`, `timestamp`, `actor`, `action`, `permission_id`, `agent_id`, `new_status`.

---

## 6) المخرجات المطلوبة لكل مرحلة (Artifacts Checklist)

| المرحلة | Artifact |
|---|---|
| Requested | `permission_request.json` |
| Reviewed | `review_notes.md`, `risk_assessment.yaml` |
| Approved | `approval_token`, `approval_record.json` |
| Active | `audit_event.jsonl` entries (continuous) |
| Monitored | `monitoring_dashboard.json` (daily) |
| Expired/Renewed | `renewal_request.json`, `renewal_eval.json` |
| Revoked | `revocation_token`, `incident_link` |
| Audited | `audit_report.md` (quarterly) |

---

## 7) الربط

- [`AGENT_ACCESS_RIGHTS_POLICY_AR.md`](AGENT_ACCESS_RIGHTS_POLICY_AR.md)
- [`AGENT_AUTONOMY_LEVELS_AR.md`](AGENT_AUTONOMY_LEVELS_AR.md)
- [`AGENT_EVAL_CADENCE_AR.md`](AGENT_EVAL_CADENCE_AR.md)
- [`AGENT_RETIREMENT_POLICY_AR.md`](AGENT_RETIREMENT_POLICY_AR.md)
- [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md)
- [`schemas/agent_permission.schema.json`](../../schemas/agent_permission.schema.json)

---

## 8) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | تعريف المراحل الثماني + صيغة Audit Trail |
