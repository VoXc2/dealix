# سياسة تقاعد الوكلاء — Agent Retirement Policy
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 · **اللغة:** العربية · **الدليل:** L1 internal.

> **مبدأ:** «كل وكيل له تاريخ ميلاد وموت مُسجَّلان. التقاعد ليس حذفًا، هو أرشفة + post-mortem.»
> — Dealix Hard Constraint (L0).

---

## 1) محفزات التقاعد (Triggers)

| الرمز | المحفز | مثال | الأولوية |
|---|---|---|---|
| RET-SUP-01 | **Superseded** (استُبدل) | وكيل جديد بأداء أفضل | عادية |
| RET-FAIL-01 | **Repeated Failure** (فشل متكرر) | 3 إخفاقات تقييم متتالية | عالية |
| RET-SEC-01 | **Security Incident** | تسريب PII | حرجة |
| RET-SCOPE-01 | **Scope Drift** (انحراف نطاق) | الوكيل يكتب في production بدون إذن | حرجة |
| RET-BIZ-01 | **Business Pivot** | تغيير في الـ ICP أو الاستراتيجية | عادية |
| RET-PERF-01 | **Underperforming** | < 10 استخدامات/شهر | عادية |
| RET-COMP-01 | **Compliance** | تغيير PDPL يُلغي use case | عالية |
| RET-DUP-01 | **Duplicate** | وكيل آخر يغطي نفس الدور | عادية |

---

## 2) عملية التقاعد (7 خطوات)

### 2.1 Announce (إعلان)
- **الزمن:** T-7 أيام (للعادية) أو فوري (للحرجة)
- **المخرج:** `retirement_notice.md` إلى المالك + Agent #30
- **المحتوى:** السبب، التاريخ المتوقع، الوكيل البديل (إن وُجد)

### 2.2 Freeze (تجميد)
- **الإجراء:** `status=frozen` في `agent_registry.jsonl`
- **المعنى:** لا يقبل مهام جديدة، يُنفّذ ما في الطابور فقط
- **الإطار الزمني:** 1-3 أيام

### 2.3 Drain In-flight (تصفية ما في الطابور)
- **المخرج:** قائمة `in_flight_tasks.json`
- **الإجراء:** إكمال أو نقل المهام الجارية
- **الحد الأقصى:** 3 أيام، وإلا تُلغى

### 2.4 Revoke Permissions (إلغاء الصلاحيات)
- **الإجراء:** كل `permission_id` نشط → `status=revoked` في `agent_permissions.jsonl`
- **الدوران (Rotation):** أي أسرار مرتبطة تُدوَّر خلال 24 ساعة
- **السجل:** `audit_log.jsonl` بـ `action=permission_revoked_due_to_retirement`

### 2.5 Archive Data (أرشفة)
- **المخرج:** `archive/agent_<id>_<date>.tar.gz` يحتوي:
  - eval history
  - audit events
  - prompts/versions
  - config
- **الاحتفاظ:** 7 سنوات (للوكلاء التجارية) أو 3 سنوات (للوكلاء الداخلية) — متوافق مع `docs/retention/DATA_RETENTION_POLICY.md`

### 2.6 Remove from Registry (إزالة من السجل)
- **الإجراء:** `status=retired` في `agent_registry.jsonl` (لا يُحذف)
- **السبب:** التاريخ مطلوب للتدقيق

### 2.7 Post-Mortem (تحليل ما بعد)
- **المخرج:** `post_mortem/agent_<id>_<date>.md` يحتوي:
  - ملخص حياة الوكيل
  - محفز التقاعد
  - دروس مُستفادة
  - توصيات (إن وُجدت)
- **المُقدِّم:** Agent #30 + Incident Commander (إن كان السبب حادث)
- **الزمن:** خلال 14 يوم من التقاعد

---

## 3) الاستبدال مقابل التقاعد البسيط

### 3.1 الاستبدال (Replacement Path)
- **متى:** RET-SUP-01, RET-PERF-01, RET-DUP-01
- **الإجراء:** إنشاء وكيل جديد (v2) مع onboarding كامل، ونقل الصلاحيات (لا المعرف)
- **الفترة:** 30 يوم تشغيل متوازي (old + new) قبل إيقاف old

### 3.2 التقاعد البسيط
- **متى:** RET-SEC-01, RET-COMP-01, RET-SCOPE-01
- **الإجراء:** إيقاف فوري + post-mortem إلزامي
- **لا استبدال** في هذه الحالة إلا بتصميم جديد تمامًا

### 3.3 التقاعد المؤقت (Pause)
- **متى:** سبب مؤقت (صيانة، انتظار)
- **الإجراء:** `status=paused`، يمكن إعادة التنشيط
- **الحد:** 90 يوم ثم يتحول لـ retired

---

## 4) قواعد الاحتفاظ بالبيانات (Data Retention)

| نوع البيانات | مدة الاحتفاظ | المبرر |
|---|---|---|
| Eval history | 7 سنوات | Audit + compliance |
| Audit events | 7 سنوات | PDPL + تدقيق |
| Prompts/versions | 3 سنوات | Engineering history |
| Customer data (إن وُجد) | 30 يوم من التقاعد، ثم حذف | PDPL |
| Secrets | فوري (دوران + حذف) | Security |
| Logs | 1 سنة | Operasional |

> **القاعدة:** بيانات العميل الشخصية تُحذف خلال 30 يوم من التقاعد. لا يحق لـ Dealix الاحتفاظ بها بعد ذلك.

---

## 5) Re-activation (إعادة التنشيط)

> **ممنوع** في v1.

- وكيل `retired` لا يُعاد — يُنشأ وكيل جديد
- هذا لمنع «إحياء» وكيل به تاريخ مشكلة
- استثناء: bug في الـ offboarding (Operator oversight) — بإجماع Agent #30 + المؤسس

---

## 6) الربط

- [`AGENT_ONBOARDING_OFFBOARDING_AR.md`](AGENT_ONBOARDING_OFFBOARDING_AR.md)
- [`AGENT_PERMISSION_LIFECYCLE_AR.md`](AGENT_PERMISSION_LIFECYCLE_AR.md)
- [`AI_AGENT_INCIDENT_RESPONSE_AR.md`](AI_AGENT_INCIDENT_RESPONSE_AR.md)
- [`../governance/DATA_RETENTION.md`](../governance/DATA_RETENTION.md)

---

## 7) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | 7 خطوات + 8 محفزات + قواعد الاحتفاظ |
