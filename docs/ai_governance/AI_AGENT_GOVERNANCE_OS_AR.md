# خريطة نظام حوكمة وكلاء الذكاء الاصطناعي — Dealix AI Agent Governance OS
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 — AI Governance, Agent Maturity & Permission Lifecycle · **المرجع التقني:** Dealix Constitution § Governance · **اللغة الأساسية:** العربية · **مستوى الدليل (Evidence Level):** مختلط (L0 افتراض، L1 وثيقة داخلية، L2 اختبار، L3 staging، L4 إنتاج)

> **اقتباس اختصار (دليل):** «لا حوكمة بدون رؤية، ولا رؤية بدون سجل، ولا سجل بدون تجديد ربع سنوي.»
> — صياغة مشتقة من نهج NIST AI RMF (GOVERN/MAP/MEASURE/MANAGE) و ISO/IEC 42001 (AIMS). المصدران مرجعيان فقط، لا يُقتبسان نصيًا.

---

## 1) الرسالة والحدود

### 1.1 الرسالة
تأسيس **نظام تشغيل حوكمة** (Governance OS) لـ **كل وكيل ذكاء اصطناعي** تُنشئه Dealix — داخليًا كان أو مُستضافًا عبر مورد خارجي — بحيث:

1. كل وكيل له **هوية، مالك، مستوى استقلالية، نطاق صلاحيات، مسار موافقة، وتقييم دوري**.
2. لا يُسمح بـ **A5 (استقلالي تام)** لإجراء تجاري خارجي في الإصدار الأول (v1).
3. لا توجد **صلاحيات عالية الخطورة دائمة** — كل صلاحية تنتهي وتُجدَّد.
4. لا يوجد **وصول للأسرار** للوكلاء في وضع A5.
5. لا يوجد **إرسال خارجي** (email, WhatsApp, LinkedIn, SMS, web publish) بدون موافقة المؤسس.

### 1.2 الحدود بين «وكيل Dealix الداخلي» و«وكيل المورّد الخارجي»

| البُعد | وكيل Dealix الداخلي | وكيل المورّد الخارجي |
|---|---|---|
| المصدر/التشغيل | داخل مستودع Dealix (هذا الـ repo) أو خوادم Dealix | API لمورّد (OpenAI Assistants, Anthropic Tools, Salesforce Agentforce, Microsoft Copilot Agents) |
| تسجيل دورة الحياة | إلزامي في `data/ai_governance/agent_registry.jsonl` | إلزامي **كذلك**، مع حقل `external_vendor` إلزامي |
| الموافقة | مالك + مؤسس | مؤسس + مراجعة قانونية (DPA/Sub-processor) |
| الأسرار | ممر OIDC مختصر (لا أسرار خام) | ممنوع في A5، مسموح بقيود في A4 |
| البيانات | وفق `docs/responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md` | يخضع لـ `docs/security/CROSS_BORDER_TRANSFER_ADDENDUM.md` |
| السجل | مدمج مع `audit_event.schema.json` | يخضع لـ Sub-processor disclosure + سجل مدمج |

> **قاعدة فصل صارمة:** لا يحق لوكيل المورّد الخارجي استلام **سياسة** أو **مفاتيح** أو **بيانات عميل** قبل توقيع تقييم الأهلية (Vendor Due Diligence) في `data/procurement/` + سجل اعتماد في `data/ai_governance/agent_registry.jsonl` بـ `evidence_level="validated"`.

---

## 2) نموذج التهديد (Threat Model — موجز)

| الفئة | التهديد | الحد الأدنى من التحكم |
|---|---|---|
| Prompt injection | محتوى خارجي يُفسد الوكيل | `docs/security/PROMPT_INJECTION_DEFENSE_AR.md` (L2 observed) |
| تسريب أسرار | استدعاء نموذج بأسرار في السياق | `docs/security/SECRETS_HANDLING_POLICY.md` (L1 internal) |
| انحراف الصلاحيات (Scope drift) | الوكيل يكتب في مجلدات خارج نطاقه | فحص قائمة (allowlist) قبل كل كتابة — هذا المستند (L2 script) |
| إجراء خارجي غير مصرّح | إرسال بريد/واتساب بدون موافقة | `docs/security/EXTERNAL_ACTION_APPROVAL_POLICY.md` (L2 script) |
| Hallucination | ادّعاء تجاري بلا دليل | `docs/responsible_ai/RESPONSIBLE_AI_OPERATING_STANDARD.md` §7 (L1) |
| Agent sprawl | عشرات الوكلاء بلا تسجيل | `docs/governance/AGENT_SPRAWL_PREVENTION.md` (L1) + `data/ai_governance/agent_registry.jsonl` |
| Drift طويل المدى | تغيّر سلوك الوكيل بصمت | تقييم أسبوعي/يومي (L0 افتراض، يجب التحول لـ L2 بقياس) |
| ترقية نموذج تكسر ضابط | تبديل نموذج دون إعادة تقييم | مطلب إعادة تقييم إلزامي قبل الترقية (L0 افتراض) |

> **مستوى الدليل الإجمالي:** خليط من L0 (افتراضات هندسة)، L1 (سياسات داخلية موجودة)، L2 (اختبارات قابلة للتنفيذ). لم يُقاس ميدانيًا بعد (L3 غير متوفر).

---

## 3) لماذا يفشل النهج «مقاس واحد للجميع» (One-Size-Fits-All)؟

> **المرجع (للاستشهاد فقط، لا اقتباس نصي):**
> NIST AI Risk Management Framework (AI RMF 1.0, يناير 2023) — يُصرّح بأن «إدارة مخاطر الذكاء الاصطناعي يجب أن تكون خاصة بالسياق، ومرنة، وقابلة للتكيّف عبر دورة الحياة، لا وصفة جامدة.»
> المصدر: <https://www.nist.gov/itl/ai-risk-management-framework> (دليل: L0 افتراض معياري، يُذكر كمصدر عام لا كحقيقة مُقاسة).

**لماذا لا يكفي معامل واحد لـ Dealix؟**

1. **اختلاف أثر الضرر:** وكيل يلخّص تقريرًا داخليًا (ضرر = تقريبًا صفر) ≠ وكيل يُرسل فاتورة لعميل (ضرر = مالي وقانوني). يجب أن يختلفا في **نطاق الصلاحيات** و**مسار الموافقة** و**كثافة التقييم**.
2. **اختلاف نضج النموذج:** وكيل مبني على GPT-4o في RAG مُقيَّد ≠ وكيل يستخدم استدعاء دوال (Function Calling) على CRM. الأول أقل تذبذبًا.
3. **اختلاف قنوات الإجراء:** القراءة من مجلد `docs/` تختلف عن الكتابة في `data/production/`. تختلف عن استدعاء API خارجي.
4. **اختلاف عمر الوكيل:** وكيل عمره يوم (تجريبي) ≠ وكيل عمره 9 أشهر (مُعتمد). الأول يحتاج تقييمًا أعرض، الثاني يحتاج تقييم انحراف سلوك.
5. **اختلاف البيئة التنظيمية:** لوكلاء يستقبلون PII سعودية = قيود PDPL مختلفة عن وكلاء يلخّصون نصوصًا عامة.

> **النتيجة:** نحتاج **طبقات استقلالية** (A0–A5) + **دورة حياة** (Lifecycle) + **مصفوفة تقييم/تجديد**. هذا ما يقدّمه نظام `docs/ai_governance/`.

---

## 4) خريطة المستندات التسعة

```
docs/ai_governance/
├── AI_AGENT_GOVERNANCE_OS_AR.md          ← هذا الملف (الخريطة)
├── AGENT_AUTONOMY_LEVELS_AR.md           ← A0..A5
├── AGENT_ACCESS_RIGHTS_POLICY_AR.md      ← Default-deny + scopes
├── AGENT_PERMISSION_LIFECYCLE_AR.md      ← requested → audited
├── AGENT_ONBOARDING_OFFBOARDING_AR.md    ← Checklists
├── AGENT_EVAL_CADENCE_AR.md              ← يومي/أسبوعي/شهري
├── AGENT_RETIREMENT_POLICY_AR.md         ← Triggers + freeze
├── HUMAN_APPROVAL_BOUNDARIES_AR.md       ← ما يحتاج مؤسس
└── AI_AGENT_INCIDENT_RESPONSE_AR.md      ← P0..P3 + post-mortem
```

### 4.1 المالك (Owner) لكل ملف

| المستند | المالك | المراجعة | مستوى الدليل |
|---|---|---|---|
| AI_AGENT_GOVERNANCE_OS_AR.md | Agent #30 | ربع سنوي | L1 internal |
| AGENT_AUTONOMY_LEVELS_AR.md | Agent #30 | ربع سنوي | L1 |
| AGENT_ACCESS_RIGHTS_POLICY_AR.md | Agent #30 + Security | نصف سنوي | L1 |
| AGENT_PERMISSION_LIFECYCLE_AR.md | Agent #30 | نصف سنوي | L1 |
| AGENT_ONBOARDING_OFFBOARDING_AR.md | Agent #30 + Operations | ربع سنوي | L1 |
| AGENT_EVAL_CADENCE_AR.md | Agent #30 + Evals | ربع سنوي | L0 → L2 هدف |
| AGENT_RETIREMENT_POLICY_AR.md | Agent #30 | سنوي | L1 |
| HUMAN_APPROVAL_BOUNDARIES_AR.md | Agent #30 + Security | ربع سنوي | L1 |
| AI_AGENT_INCIDENT_RESPONSE_AR.md | Agent #30 + Security | نصف سنوي | L1 |

### 4.2 مخرجات البيانات والـ schemas (4 + 4)

```
schemas/
├── agent_registry.schema.json
├── agent_permission.schema.json
├── agent_eval.schema.json
└── agent_incident.schema.json

data/ai_governance/
├── agent_registry.jsonl    (≥6 وكلاء مختلفين)
├── agent_permissions.jsonl (≥6 منح)
├── agent_evals.jsonl       (≥6 سجلات)
└── agent_incidents.jsonl   (≥4 سجلات)
```

### 4.3 التقارير (3 + 1)

```
reports/ai_governance/
├── AGENT_GOVERNANCE_REVIEW.md     ← مراجعة الـ 6 وكلاء
├── AGENT_PERMISSION_REVIEW.md     ← مراجعة منح الصلاحيات
├── AGENT_INCIDENT_REVIEW.md       ← مراجعة الحوادث
└── AI_GOVERNANCE_FINAL_REPORT.md  ← التقييم النهائي
```

---

## 5) الربط بالأُطر الموجودة (Linkage)

### 5.1 إلى `docs/governance/` (موجود)
- [`../governance/AGENT_REGISTRY.md`](../governance/AGENT_REGISTRY.md) — هذا النظام **يوسّع**ه ليصبح JSON Schema + قابلًا للاستعلام.
- [`../governance/AI_ACTION_LEVELS.md`](../governance/AI_ACTION_LEVELS.md) و [`../governance/AI_ACTION_TAXONOMY.md`](../governance/AI_ACTION_TAXONOMY.md) — نظام **A0–A5** هنا **مكمّل** ولا يلغي. يوجد **جدول تحويل** في `AGENT_AUTONOMY_LEVELS_AR.md` §7.
- [`../governance/AUTONOMY_VALIDATION_GATES.md`](../governance/AUTONOMY_VALIDATION_GATES.md) — `AGENT_EVAL_CADENCE_AR.md` يربط كل مستوى A0–A5 بنوع التقييم المطلوب.
- [`../governance/HUMAN_IN_THE_LOOP_MATRIX.md`](../governance/HUMAN_IN_THE_LOOP_MATRIX.md) — `HUMAN_APPROVAL_BOUNDARIES_AR.md` يُوسّع هذا الجدول إلى قنوات + مهلة + أصول.
- [`../governance/PERMISSION_MIRRORING.md`](../governance/PERMISSION_MIRRORING.md) — `AGENT_PERMISSION_LIFECYCLE_AR.md` يطبّق «الميرور» على مستوى **الوكلاء** (وليس البشر فقط).
- [`../governance/INCIDENT_RESPONSE.md`](../governance/INCIDENT_RESPONSE.md) — `AI_AGENT_INCIDENT_RESPONSE_AR.md` يُوسّع لمنطق P0–P3 + تعلم.
- [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md) — كل تغيير صلاحية يجب أن يُسجَّل وفقًا لهذه السياسة.

### 5.2 إلى `docs/responsible_ai/`
- [`../responsible_ai/AI_INVENTORY.md`](../responsible_ai/AI_INVENTORY.md) — `data/ai_governance/agent_registry.jsonl` هو **نسخة مُهيكلة** قابلة للقراءة الآلية.
- [`../responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md`](../responsible_ai/AI_USE_CASE_RISK_CLASSIFIER.md) — حقول `risk_level` و `external_action_capability` في السجل تطابق مُصنِّف المخاطر.
- [`../responsible_ai/RESPONSIBLE_AI_OPERATING_STANDARD.md`](../responsible_ai/RESPONSIBLE_AI_OPERATING_STANDARD.md) — هذا النظام **يعمل على الأعمدة 1–7** (السيادة، الإشراف، حوكمة وقت التشغيل، التدقيق، proof، الإيقاع، التحسين).

### 5.3 إلى `docs/security/`
- [`../security/EXTERNAL_ACTION_APPROVAL_POLICY.md`](../security/EXTERNAL_ACTION_APPROVAL_POLICY.md) — `HUMAN_APPROVAL_BOUNDARIES_AR.md` يبني عليه ويضيف **مهل** و**قنوات** و**ما يُعتبر «موافقة»**.
- [`../security/SECRETS_HANDLING_POLICY.md`](../security/SECRETS_HANDLING_POLICY.md) — يُحظر وصول الأسرار على A5.
- [`../security/TRUST_SAFETY_OS_AR.md`](../security/TRUST_SAFETY_OS_AR.md) — هذا النظام يلتزم بـ 5 طبقات الأمان والثقة.
- [`../security/INCIDENT_RESPONSE_RUNBOOK_AR.md`](../security/INCIDENT_RESPONSE_RUNBOOK_AR.md) — تكامل: الحوادث P0/P1 تُسجَّل هنا **و** في `agent_incidents.jsonl`.

### 5.4 إلى `docs/audit/`
- [`../audit/AUDIT_STANDARD.md`](../audit/AUDIT_STANDARD.md) — كل صف في JSONL يجب أن يحقق قابلية التدقيق.
- [`../audit/AI_OUTPUT_AUDIT.md`](../audit/AI_OUTPUT_AUDIT.md) — مُخرجات الوكلاء في كل مستوى تخضع لمعيار التدقيق.

---

## 6) مالك المستند وسلسلة التغيير (File Ownership & Change Control)

| الإجراء | المالك | الموافقة | السجل |
|---|---|---|---|
| إنشاء/تعديل سياسة | Agent #30 (AI Governance) | مؤسس Dealix | git commit + سجل في `data/ai_governance/` |
| إضافة وكيل جديد إلى `agent_registry.jsonl` | مالك الوكيل (Department Head) | Agent #30 (مراجعة) | JSONL row |
| منح صلاحية عالية الخطورة | المؤسس | Agent #30 (توصية) | `agent_permissions.jsonl` |
| ترقية مستوى A→A+1 | المؤسس | Agent #30 (مراجعة) + سجل |
| تخفيض مستوى بعد حادث | Agent #30 (توصية) | المؤسس | `agent_incidents.jsonl` + سجل تغيير |
| إيقاف/تقاعد وكيل | مالك الوكيل | Agent #30 | `agent_registry.jsonl` بـ `status=retired` |

**قواعد إلزامية:**
1. كل تغيير في `data/ai_governance/*.jsonl` يجب أن يكون **PR** مع مراجعة **كود** و**سياسة** (مراجعان مختلفان: تقني + governance).
2. لا تُقبل تعديلات بـ `force-push` على أي ملف في `docs/ai_governance/` أو `data/ai_governance/` أو `schemas/agent_*.json`.
3. أي انتهاك يُسجَّل في `reports/ai_governance/AGENT_INCIDENT_REVIEW.md`.

---

## 7) كيفية الاستخدام العملي (Quick Start)

1. **لإنشاء وكيل جديد:** اقرأ `AGENT_AUTONOMY_LEVELS_AR.md` لاختيار المستوى، ثم املأ `AGENT_ONBOARDING_OFFBOARDING_AR.md` checklist، ثم سجّل صفًا في `data/ai_governance/agent_registry.jsonl`.
2. **لطلب صلاحية:** املأ `AGENT_PERMISSION_LIFECYCLE_AR.md` §3 (طلب) ثم أرسل للمؤسس.
3. **لتشغيل تقييم:** شغّل سكربت التقييم ثم سجّل صفًا في `data/ai_governance/agent_evals.jsonl` — انظر `AGENT_EVAL_CADENCE_AR.md`.
4. **عند وقوع حادث:** افتح `AI_AGENT_INCIDENT_RESPONSE_AR.md` → Triage → Containment → Post-mortem.

---

## 8) عبارات «الحدود» (Hard Constraints) — غير قابلة للتفاوض

1. **ممنوع A5** على أي إجراء تجاري خارجي في v1.
2. **ممنوع** منح صلاحية عالية الخطورة **دائمة**. كل صلاحية لها تاريخ انتهاء.
3. **ممنوع** وصول A5 إلى الأسرار.
4. **ممنوع** الإرسال الخارجي (email, WhatsApp, LinkedIn, SMS, publish) بدون موافقة المؤسس **والأدلة** (evidence_level ≥ L3).
5. **ممنوع** تعديل ملفات الإنتاج (`api/`, `core/`, `data/production/`, `supabase/`) من وكيل فوق A2.
6. **ممنوع** الترويج/إلغاء تقاعد وكيل بدون موافقة المؤسس.
7. **ممنوع** تجاوز المراجعة الربع سنوية للحوكمة.

> **التطبيق:** كل خرق لقاعدة أعلاه يُسجَّل فورًا في `data/ai_governance/agent_incidents.jsonl` بـ `severity ≥ P1` ويُرفع إلى المؤسس.

---

## 9) سجل الإصدارات

| الإصدار | التاريخ | التغيير | المالك |
|---|---|---|---|
| v1.0 | 2026-06-03 | إنشاء الخريطة الكاملة | Agent #30 |
