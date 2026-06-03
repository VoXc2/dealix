# Agent Autonomy Levels — مستويات استقلالية الوكلاء

> لا تخلِّ الوكلاء كلهم بنفس الصلاحية. نموذج "كل الوكلاء موثوقين أو كلهم مقفلين" خطأ.
> الحوكمة الصحيحة تدرّج الصلاحية حسب الاستقلالية: observe → advise → draft →
> act with approval → autonomous داخل guardrails قوية.

---

## المستويات الخمسة

| Level | الاسم | ماذا يفعل؟ | أمثلة | يحتاج موافقة؟ |
|-------|-------|------------|-------|---------------|
| L1 | Observe | يقرأ ويحلل فقط | Account Research, Signal Detection | لا، إذا data عامة |
| L2 | Advise | يقترح ولا ينفذ | System Recommendation, Scores | لا / مراجعة دورية |
| L3 | Draft | يكتب drafts | Email, Call Brief, Mini Proposal draft | نعم قبل الإرسال |
| L4 | Act with Approval | ينفذ بعد موافقة | إرسال إيميل، إرسال Proposal | نعم صريحة |
| L5 | Autonomous | تنفيذ محدود داخل sandbox | تقارير داخلية فقط | مسموح داخليًا فقط |

المصدر الرسمي: `company_os/agents/agent_registry.json`.

---

## القاعدة الحاسمة

```txt
Dealix agents may generate.
Dealix agents may recommend.
Dealix agents may prepare.
Dealix agents may not externally send, call, price-change, contract,
or start delivery without founder approval.
```

---

## كيف يُطبَّق المستوى

| المستوى | الإجراء المسموح | الحاجز التقني |
|---------|------------------|----------------|
| L1 | قراءة بيانات عامة | لا كتابة، لا أدوات خارجية |
| L2 | إخراج توصية مع سبب | لا كتابة في ملفات تنفيذية |
| L3 | كتابة draft في approval_queue | `requires_approval = true` |
| L4 | تنفيذ بعد موافقة مسجّلة | موافقة في approval_queue + سجل |
| L5 | كتابة تقارير داخلية فقط | `internal_only = true` |

---

## حدود L5 (Autonomous)

```txt
L5 يعمل داخل sandbox فقط.
لا مخرجات تواجه العميل.
لا إرسال خارجي.
كل إخراج يبقى داخل المستودع (reports/).
```

أي وكيل L5 يجب أن يكون `internal_only = true` في السجل، ويتحقق منه فحص
`check_agent_permissions.py`.

---

## التحقق الآلي

- `python dealix.py agent-audit` يفحص أن كل وكيل ضمن مستوى صالح، وأن لا وكيل
  يملك صلاحية إرسال/اتصال/تسعير/تعاقد/بدء تسليم.
- أي خرق يوقف الفحص (exit 1) ويُسجَّل في `reports/agents/AGENT_PERMISSION_AUDIT.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
