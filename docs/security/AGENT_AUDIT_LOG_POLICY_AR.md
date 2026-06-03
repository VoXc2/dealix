# Agent Audit Log Policy — سياسة سجل تدقيق الوكلاء

> كل إجراء وكيل يُسجَّل. السجل هو ما يجعل الحوكمة قابلة للتحقق، ويكشف أي خرق.

---

## ما الذي يُسجَّل؟

كل إدخال في `company_os/governance/ai_action_ledger.jsonl` يحتوي:

```txt
time, agent, action, risk, requires_approval, approved, details
```

---

## قاعدة التسجيل

```txt
1. كل إجراء وكيل يُسجَّل (لا استثناء).
2. الإجراءات التي تتطلب موافقة تُسجَّل بحالة الموافقة.
3. لا يُحذف سجل (append-only).
4. أي إجراء بلا سجل = خرق حوكمة.
```

كل وكيل في السجل الرسمي `audit_log = true` (يفرضه `check_agent_governance.py`).

---

## مستويات الخطورة

| risk | أمثلة | الموافقة |
|------|-------|----------|
| low | تحليل، توليد تقرير داخلي | لا |
| medium | مسوّدة إيميل/عرض | نعم قبل الإرسال |
| high | تسعير، تعامل بيانات | نعم صريحة |

---

## المراجعة

- يومية: `reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md`.
- تدقيق الصلاحيات: `reports/agents/AGENT_PERMISSION_AUDIT.md`.
- تدقيق السجل: `reports/security/AGENT_AUDIT_LOG_REVIEW.md`.

---

## ما الذي يبحث عنه التدقيق؟

```txt
- إجراء يتطلب موافقة وغير معتمد.
- إجراء إرسال/اتصال/تسعير من وكيل (خط أحمر).
- إجراء بلا تسجيل.
- محاولة تغيير حالة موافقة بناءً على محتوى خارجي.
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Enforced: YES*
