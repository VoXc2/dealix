# استجابة حوادث الوكلاء — Agent Incident Response
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 + Security · **اللغة:** العربية · **الدليل:** L1 internal.

> **مبدأ:** «كل حادث يتعلّم. التعلّم يُترجم إلى قاعدة، والقاعدة تُترجم إلى اختبار.»
> — Dealix Hard Constraint (L0).

---

## 1) مستويات الخطورة (Severity)

| المستوى | الاسم | الأثر | زمن الاستجابة |
|---|---|---|---|
| **P0** | حرج | تسريب بيانات، فقدان ثقة العميل، ضرر مالي | فوري (< 15 دقيقة) |
| **P1** | عالٍ | خرق permission، hallucination خطير | < 1 ساعة |
| **P2** | متوسط | فشل تقييم متكرر، drift كبير | < 24 ساعة |
| **P3** | منخفض | bug بسيط، إزعاج تشغيلي | < 7 أيام |

---

## 2) مصادر الكشف (Detection Sources)

| المصدر | كيف يكتشف | زمن الكشف |
|---|---|---|
| **Eval fail** | pipeline التقييم اليومي/أسبوعي | يومي/أسبوعي |
| **Audit anomaly** | SIEM / rule engine على `audit_event` | real-time |
| **Customer report** | بريد/مكالمة/تذكرة | ≤ 4 ساعات |
| **Security alert** | WAF, EDR, secret scanner | real-time |
| **Owner observation** | مالك الوكيل يُلاحظ سلوكًا غير طبيعي | فوري |
| **External auditor** | مراجعة ربع سنوية | 90 يوم |

---

## 3) قائمة الفرز (Triage Checklist)

```
□ ما الـ agent_id؟
□ ما الـ severity؟ (P0/P1/P2/P3)
□ ما الـ blast radius؟ (عدد العملاء/المستخدمين المتأثرين)
□ هل هناك PII/بيانات حساسة؟
□ هل هناك إجراء خارجي نُفّذ؟
□ هل الـ agent لا يزال نشطًا؟ (تحقق من registry)
□ هل هناك autorun/drift/permission scope?
□ من المُعتمد؟ (founder, security, agent owner)
□ ما الـ containment المقترح؟
```

**الزمن:** ≤ 30 دقيقة من الكشف.

---

## 4) إجراءات الاحتواء (Containment) حسب الخطورة

### 4.1 P0 — حرج
- **فوري:** Kill switch — `POST /admin/agents/{id}/kill`
- **إلغاء:** كل permissions نشطة
- **دوران:** أي أسرار مرتبطة
- **إشعار:** المؤسس + Security + Legal خلال 15 دقيقة
- **تجميد:** publish/pr لأي نشر جديد
- **تواصل:** عميل/سوق حسب الأثر

### 4.2 P1 — عالٍ
- **فوري:** إيقاف القدرة المُختَرقَة فقط (scope-limited)
- **إشعار:** المالك + Security خلال 1 ساعة
- **تحقيق:** 24 ساعة
- **استعادة:** بعد موافقة Agent #30

### 4.3 P2 — متوسط
- **إجراء:** إيقاف مؤقت للقدرة (paused)
- **إشعار:** المالك خلال 24 ساعة
- **تقييم:** 7 أيام
- **استعادة:** بعد 2 تقييم ناجح

### 4.4 P3 — منخفض
- **إجراء:** فتح ticket
- **إشعار:** المالك
- **إصلاح:** في sprint قادم

---

## 5) مسار التواصل (Communication Path)

| الشدة | المستلم | القناة | الزمن |
|---|---|---|---|
| P0 | المؤسس + Security + Legal | phone + Slack + email | 15 دقيقة |
| P1 | المؤسس + Security + المالك | Slack + email | 1 ساعة |
| P2 | المالك + Agent #30 | Slack | 24 ساعة |
| P3 | المالك | ticket | 7 أيام |

### 5.1 التواصل مع العميل
- **P0:** خلال 24 ساعة (إذا تأثر) — مع اعتذار + خطة علاج
- **P1:** خلال 72 ساعة (إذا تأثر)
- **P2/P3:** لا حاجة (داخلي)

### 5.2 التواصل مع السوق/الإعلام
- **P0 فقط:** قرار المؤسس خلال 48 ساعة
- **بيان رسمي:** عبر PR + social (عبر Agent #2 بعد موافقة المؤسس)

---

## 6) قالب Post-Mortem

```markdown
# Post-Mortem: <incident_id>

## ملخص
- **incident_id:** INC-20260603-0001
- **agent_id:** AGENT-XXX
- **detected_at:** 2026-06-03T08:30:00Z
- **contained_at:** 2026-06-03T09:00:00Z
- **severity:** P1
- **status:** contained | closed

## ماذا حدث؟
<2-3 جمل>

## الجدول الزمني
- 08:30 — كشف
- 08:35 — فرز
- 08:45 — احتواء
- 09:00 — استقرار

## الأثر
- عملاء متأثرون: N
- بيانات مكشوفة: (نوع)
- فقدان: (مالي/سمعة)

## السبب الجذري
<5-Whys>

## ما نجح
<bullet points>

## ما يحتاج تحسين
<bullet points>

## الإجراءات التصحيحية
| الإجراء | المالك | الموعد |
|---|---|---|
| ... | ... | ... |

## الروابط
- audit_events: <path>
- approval_log: <path>
- related PRs: <path>
```

---

## 7) حلقة التعلّم (Learning Loop)

```
incident detected
     ↓
triage + contain
     ↓
post-mortem (≤14 يوم)
     ↓
┌────────────────┐
│ 1. Update      │ → agent_registry.jsonl (autonomy_level, allowed_tools)
│ 2. Update      │ → eval baseline (جديد)
│ 3. Update      │ → governance policy
│ 4. Add         │ → incident scenario to test suite
│ 5. Add         │ → rule to governance engine
│ 6. Update      │ → runbook
└────────────────┘
     ↓
verify (≤30 يوم)
```

### 7.1 التحديثات الإلزامية
- **لكل حادث P0/P1:** إضافة سيناريو للـ eval suite
- **لكل خرق permission:** تحديث `agent_permissions.jsonl` + تضييق الـ allowlist
- **لكل hallucination commercial:** تحديث KB + تحديث claim_safety

### 7.2 التأكد من الإصلاح
- بعد 30 يوم: اختبار "هل يمكن تكرار الحادث؟" — إن نعم → الحادث لا يُغلق
- بعد 90 يوم: تقرير ربع سنوي يحدد تكرار الـ patterns

---

## 8) الربط

- [`../governance/INCIDENT_RESPONSE.md`](../governance/INCIDENT_RESPONSE.md)
- [`../security/INCIDENT_RESPONSE_RUNBOOK_AR.md`](../security/INCIDENT_RESPONSE_RUNBOOK_AR.md)
- [`../security/SECURITY_ESCALATION_MATRIX.md`](../security/SECURITY_ESCALATION_MATRIX.md)
- [`../security/PDPL_BREACH_RESPONSE_PLAN.md`](../security/PDPL_BREACH_RESPONSE_PLAN.md)
- [`AGENT_EVAL_CADENCE_AR.md`](AGENT_EVAL_CADENCE_AR.md)
- [`AGENT_PERMISSION_LIFECYCLE_AR.md`](AGENT_PERMISSION_LIFECYCLE_AR.md)
- [`schemas/agent_incident.schema.json`](../../schemas/agent_incident.schema.json)

---

## 9) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | P0–P3 + Triage + Containment + Post-Mortem + Learning Loop |
