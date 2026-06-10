# سياسة حقوق الوصول للوكلاء — Agent Access Rights Policy
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 + Security · **اللغة:** العربية · **الدليل:** L1 internal (يستند إلى `docs/governance/PERMISSION_MIRRORING.md` و `docs/security/SECRETS_HANDLING_POLICY.md`، لم يُقاس ميدانيًا بعد).

> **المبدأ:** «الافتراضي هو الرفض (Default Deny). كل صلاحية استثناء يجب أن يُبرَّر، يُسجَّل، ويَنتهي.»
> — Dealix Hard Constraint (L0). غير قابل للتفاوض.

---

## 1) Default Deny (الرفض الافتراضي)

كل وكيل **يُمنع** من كل شيء بشكل افتراضي. كل قدرة تُمنح:
- بطلب موثّق
- بمراجعة ثنائية (Technical + Governance)
- بتجربة زمنية (expires_at)
- بإثبات مستوى الدليل ≥ L2 (اختبار) للقدرات عالية الخطورة

> **التطبيق التقني:** كل عملية كتابة (`write`) أو شبكة (`network`) أو إرسال (`send`) يجب أن تمر بـ `policy_engine.check(agent_id, action, target)` قبل التنفيذ.

---

## 2) نطاقات الملفات (File-Area Scopes)

### 2.1 السماح الافتراضي للقراءة (لكل الوكلاء ما عدا A5)
| المجلد | A0 | A1 | A2 | A3 | A4 | A5 |
|---|---|---|---|---|---|---|
| `docs/` (باستثناء `docs/security/secrets/`) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| `data/` (باستثناء `data/production/`) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| `schemas/` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| `reports/` | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

### 2.2 السماح بالكتابة
| المجلد | A0 | A1 | A2 | A3 | A4 | A5 |
|---|---|---|---|---|---|---|
| `reports/` (مسودات) | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| `data/ai_governance/queue/` | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| `docs/`, `data/` (غير production) | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| `data/production/` (محدد) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `api/`, `core/`, `frontend/`, `scripts/`, `integrations/` | ❌ | ❌ | ❌ | ❌ | ⚠️ نادر + موافقة | ❌ |
| `supabase/migrations/` | ❌ | ❌ | ❌ | ❌ | ⚠️ + موافقة المؤسس | ❌ |
| `schemas/agent_*.json` | ❌ | ❌ | ❌ | ❌ | ⚠️ + مراجعة | ❌ |

### 2.3 الممنوع دائمًا (لكل المستويات)
- `docs/security/secrets/`
- `.env*`، `secrets/`
- `.git/`، `data/production/secrets/`
- أي ملف يحوي API keys، tokens، PAT، credentials (انظر `docs/security/SECRETS_HANDLING_POLICY.md`)

---

## 3) نطاقات الشبكة (Network Scopes)

### 3.1 Allowlist (مسموح)
- `api.moyasar.com` — بوابة الدفع (فقط لـ A4 + founder approval لكل عملية)
- `graph.facebook.com` / `graph.instagram.com` — Meta APIs (فقط لـ A4 + template مُوافق)
- `api.whatsapp.com` / WhatsApp Business API — A4 فقط
- `api.hubapi.com` — CRM (A2 قراءة، A4 كتابة بعد موافقة)
- `api.calendly.com` — A4 بعد موافقة
- `api.openai.com` / `api.anthropic.com` — نماذج LLM (مسموح افتراضي للقراءة)
- `n8n.io/webhook/...` — A4 + موافقة

### 3.2 Denylist (ممنوع)
- LinkedIn API لأي أتمتة (`api.linkedin.com`)
- Twitter/X API للتلاعب (`api.twitter.com/2/.../tweets`)
- خوادم scraping عامة
- Cloud metadata endpoints (`169.254.169.254`, `metadata.google.internal`)
- أي IP داخلي (SSRF guard — `docs/security/`)

### 3.3 Default-deny SSRF
- كل طلب شبكة يمر بـ `api/security/ssrf_guard.py`
- ممنوع: private IP ranges، loopback، metadata، domains غير مسموحة

---

## 4) نطاقات الأسرار (Secret Scopes)

| المستوى | وصول الأسرار | ملاحظات |
|---|---|---|
| A0 | ❌ لا شيء | — |
| A1 | ❌ لا شيء | — |
| A2 | ❌ لا شيء | — |
| A3 | ❌ لا شيء | يُمرَّر token مُؤقت (≤15 دقيقة) فقط وقت التنفيذ |
| A4 | ⚠️ عبر OIDC federation | لا أسرار خامّة في الـ context؛ يُستبدل بـ short-lived token |
| A5 | ❌ ممنوع نهائيًا | **Hard Constraint** — لا أسرار في v1 |

> **القاعدة:** الأسرار لا تظهر في prompts، لا في logs، لا في reports. تُحقن عبر OIDC/GCP Service Account في runtime فقط.

---

## 5) نطاقات بيانات العميل (Customer Data Scopes)

### 5.1 المبدأ
**افتراضي: لا وصول.** كل وصول لبيانات العميل يحتاج:

1. **Pilot صريح** (موقّع من العميل) — `data/contracts/`
2. **موافقة المؤسس** لكل وكيل يصل
3. **سجل في `data/ai_governance/agent_permissions.jsonl`** بـ `scope=customer_data`
4. **تقييم risk_classifier** = high
5. **PII redaction** إلزامي في كل مخرج (`docs/security/CONTEXT_SANITIZATION_POLICY.md`)

### 5.2 التصنيف
- **Pilot نشط:** وصول read-only للحقول اللازمة
- **Pilot منتهي:** تصدير البيانات الشخصية خلال 30 يوم (PDPL)
- **لا Pilot:** **ممنوع** الوصول

---

## 6) Tool Allowlist vs Denylist

### 6.1 Allowlist (مفعّل افتراضيًا)
- `read_file`, `search`, `list_directory`
- `write_file` (في النطاقات المسموحة فقط)
- `send_email` (A4 فقط، مع approval)
- `send_whatsapp_template` (A4 فقط، مع approval)
- `queue_create` (A3+)
- `execute_approved_action` (A4 فقط)
- `llm_call` (مع rate limit)

### 6.2 Denylist (ممنوع)
- `scrape_url` (إلا بمصدر مُعتمد)
- `linkedin_*` (كلها)
- `bulk_email` (كلها — A4 فقط single-recipient بعد موافقة)
- `bulk_whatsapp` (كلها)
- `modify_production_schema` (إلا بـ A4 + founder)
- `access_raw_secrets` (A5 دائمًا)
- `pay` (ممنوع في v1 — يتم عبر Moyasar gateway المُعتمد)

### 6.3 لا توجد «Disabled by Default» Tools
- أي أداة غير مُدرجة = مرفوضة
- إضافة أداة جديدة تحتاج: PR + مراجعة Agent #30 + سجل في `data/ai_governance/`

---

## 7) محفزات إعادة المراجعة (Re-Review Triggers)

يُعاد فتح مراجعة الصلاحيات **تلقائيًا** عند:

| المحفز | الإجراء | الإطار الزمني |
|---|---|---|
| **تغيير دور (Role Change)** | المالك الجديد يُوقّع، يُعاد تقييم A-level | فوري |
| **حادث P0/P1** | تخفيض A-level تلقائي، مراجعة كاملة | فوري |
| **حادث P2** | مراجعة الصلاحيات | 7 أيام |
| **حادث P3** | إضافة للـ follow-up | 30 يوم |
| **Scope drift مكتشف** | تجديد الصلاحيات وتضييق | 14 يوم |
| **تغيير نموذج أساسي** | إعادة تقييم | 30 يوم |
| **تغيير 25% في الاستخدام** | تجديد | 30 يوم |
| **انتهاء صلاحية** | مراجعة كاملة | يوم الانتهاء |
| **تحديث سياسة** | إعادة موافقة | 30 يوم من نشر السياسة |
| **Audit ربع سنوي** | مراجعة شاملة | 90 يوم |

---

## 8) المراجعة (Audit)

- ربع سنوي: Agent #30 يراجع كل سجل `agent_permissions.jsonl`
- سنوي: Security Red Team يدقق السجلات في `data/ai_governance/`
- عند أي خرق: تسجيل في `data/ai_governance/agent_incidents.jsonl`

---

## 9) الربط

- [`../governance/PERMISSION_MIRRORING.md`](../governance/PERMISSION_MIRRORING.md)
- [`../security/SECRETS_HANDLING_POLICY.md`](../security/SECRETS_HANDLING_POLICY.md)
- [`../security/EXTERNAL_ACTION_APPROVAL_POLICY.md`](../security/EXTERNAL_ACTION_APPROVAL_POLICY.md)
- [`../responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md`](../responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md)
- [`AGENT_PERMISSION_LIFECYCLE_AR.md`](AGENT_PERMISSION_LIFECYCLE_AR.md)
- [`HUMAN_APPROVAL_BOUNDARIES_AR.md`](HUMAN_APPROVAL_BOUNDARIES_AR.md)

---

## 10) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | سياسة Default Deny الكاملة |
