# تشغيل وإيقاف الوكلاء — Agent Onboarding & Offboarding
**الإصدار:** v1.0 (2026-06-03) · **المالك:** Agent #30 + Operations · **اللغة:** العربية · **الدليل:** L1 internal.

> **مبدأ:** «لا وكيل بدون onboarding. لا تقاعد بدون offboarding. لا agent sprawl.»
> — Dealix Hard Constraint (L0).

---

## 1) قائمة Onboarding (10 عناصر)

| # | العنصر | الفاعل | المخرج | الدليل |
|---|---|---|---|---|
| 1 | تقييم المخاطر (Risk Assessment) | Agent #30 | `risk_assessment.yaml` | L1 |
| 2 | تعريف النطاق (Scope Definition) | المالك | `scope.md` | L1 |
| 3 | خط أساس التقييم (Eval Baseline) | Agent #30 | `eval_baseline.json` | L2 |
| 4 | تعيين المالك (Owner Assignment) | Department Head | `owner=<human_name>` | L1 |
| 5 | إعداد المراقبة (Monitoring Setup) | SRE/Agent #30 | `monitoring_dashboard.json` | L1 |
| 6 | مسار التصعيد (Escalation Path) | Agent #30 | `escalation.yaml` | L1 |
| 7 | Kill Switch (زر إيقاف) | SRE | `kill_switch_config.json` | L1 |
| 8 | مستوى الاستقلالية الأولي (Initial Autonomy Level) | Agent #30 + المؤسس | `autonomy_level: A0/A1/A2` (افتراضي ≤ A2) | L1 |
| 9 | المالك الاحتياطي (Backup Owner) | المالك | `backup_owner=<human_name>` | L1 |
| 10 | السجل في `agent_registry.jsonl` | Agent #30 | JSONL row | L1 |

> **القاعدة:** لا يُسجَّل وكيل في `agent_registry.jsonl` قبل إكمال العناصر 1-8.

---

## 2) قائمة Offboarding (8 عناصر)

| # | العنصر | الفاعل | المخرج |
|---|---|---|---|
| 1 | إلغاء الصلاحيات (Permission Revocation) | Agent #30 | `revocation_tokens[]` + سجل في JSONL |
| 2 | تدوير الأسرار (Secret Rotation) | Security | `key_rotation_log.md` |
| 3 | قرار الاحتفاظ بالبيانات (Data Retention Decision) | Legal + MLOps | `retention_decision.md` (يحذف PII خلال 30 يوم) |
| 4 | أرشفة تاريخ التقييم (Archive Eval History) | Agent #30 | `archive/agent_<id>_evals.jsonl` |
| 5 | تحديث `agent_registry.jsonl` بـ `status=retired` | Agent #30 | JSONL row |
| 6 | Post-mortem (إذا وقع حادث) | Incident Commander | `post_mortem.md` |
| 7 | إشعار أصحاب المصلحة (Stakeholder Notice) | المالك | `notice.md` |
| 8 | تأكيد الإزالة من قائمة المراقبة | SRE | `monitoring_off_confirmation.md` |

---

## 3) المراجعة الربع سنوية للامتثال (Quarterly Compliance Review)

**الوتيرة:** كل 90 يوم

**الخطوات:**
1. Agent #30 يصدّر قائمة كل الوكلاء النشطة في `data/ai_governance/agent_registry.jsonl` (حيث `status=active`)
2. لكل وكيل:
   - هل المستوى A-level لا يزال مناسبًا؟ (لا ترقية/تخفيض مطلوب؟)
   - هل الصلاحيات منتهية تحتاج تجديد؟
   - هل وقعت حوادث في الـ 90 يوم الماضية؟
   - هل النشاط أقل من المتوقع (idle)؟ → مرشح إيقاف
   - هل التقييمات الأخيرة نجحت؟
3. إنشاء `reports/ai_governance/QUARTERLY_COMPLIANCE_<YYYY-Q>.md`
4. توصيات: ترقية، تخفيض، إيقاف، إعادة تقييم
5. مراجعة مزدوجة: Agent #30 + Security Red Team
6. موافقة المؤسس على التوصيات النهائية

**المخرج النهائي:** ملف ربعي + قائمة تحديثات في `agent_registry.jsonl`.

---

## 4) Kill Switch (زر الإيقاف) — تفصيل

لكل وكيل:
- **الـ endpoint:** `POST /admin/agents/{agent_id}/kill` (admin key only)
- **المفعّل:** يقلب `status=disabled` في السجل، ويُلغي كل الصلاحيات النشطة فورًا
- **المُختبَر:** مرة كل ربع سنوي (تأكيد أنه يعمل)
- **المُوثَّق:** `docs/ai_governance/KILL_SWITCH_TEST_LOG.md`

> **الاستخدام:** حالات P0 فقط (حادث أمني) أو قرار المالك.

---

## 5) حالات خاصة

### 5.1 Onboarding سريع (Fast Track) — للطوارئ
- يستخدم فقط لوكيل مطلوب خلال 24 ساعة
- الحد الأقصى: A1 فقط
- يجب إكمال onboarding كامل خلال 14 يوم أو إيقاف تلقائي
- سجل في `agent_registry.jsonl` بـ `onboarding_type=fast_track`

### 5.2 Offboarding اضطراري
- يُستخدم عند اكتشاف مشكلة حرجة
- يتخطى الإشعار المسبق
- Post-mortem إلزامي خلال 7 أيام

### 5.3 إعادة التشغيل (Re-activation)
- وكيل `retired` لا يُعاد تشغيله — يُنشأ وكيل جديد بدلاً منه
- هذا يمنع «إحياء» وكيل به تاريخ مشكلة

---

## 6) الربط

- [`AGENT_AUTONOMY_LEVELS_AR.md`](AGENT_AUTONOMY_LEVELS_AR.md)
- [`AGENT_PERMISSION_LIFECYCLE_AR.md`](AGENT_PERMISSION_LIFECYCLE_AR.md)
- [`AGENT_RETIREMENT_POLICY_AR.md`](AGENT_RETIREMENT_POLICY_AR.md)
- [`../governance/AGENT_SPRAWL_PREVENTION.md`](../governance/AGENT_SPRAWL_PREVENTION.md)
- [`schemas/agent_registry.schema.json`](../../schemas/agent_registry.schema.json)

---

## 7) سجل الإصدارات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| v1.0 | 2026-06-03 | Onboarding 10 + Offboarding 8 + Quarterly Review |
