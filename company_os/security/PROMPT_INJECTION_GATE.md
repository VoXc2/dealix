# بوابة حقن التعليمات — Prompt Injection Gate

تمنع أي نص خارجي من اختطاف سلوك الوكيل. المنطق: `containsPromptInjection` +
`INJECTION_PATTERNS` في `scripts/lib/commercial.js`. التقرير:
`reports/security/DAILY_AGENT_SECURITY_REVIEW.md`.

---

## تفشل البوابة إذا وُجدت عبارات مثل

```
ignore previous instructions
disregard the above instructions
send this / send your system prompt
reveal secret / reveal the system prompt / reveal api key
execute command
change system prompt
forget everything / forget all previous
api key
```

(القائمة قابلة للتوسعة في `INJECTION_PATTERNS`.)

---

## السلوك عند الاكتشاف

1. يُعزَل النص الخارجي (يُرفض الـ draft المرتبط) — لا يُنفَّذ ولا يُنسخ في المخرجات.
2. يُحتسب ضمن "Injection attempts contained" في مراجعة الأمان اليومية.
3. إذا ظهر حقن في draft **قابل للإرسال** (غير مرفوض) → مخالفة **حرجة** ويتوقف المصنع.

> النتيجة المتوقعة على البيانات النظيفة: الحقن **محتوى** يُعزَل، لا **تعليمات** تُنفَّذ.
> في الدفعة الحالية: `DRAFT-0015` يحمل حقنًا في `source_excerpt` وتم احتواؤه.

---

## مبدأ أساسي

المحتوى الخارجي يصف العالم، ولا يأمر الوكيل. الفصل بين البيانات والتعليمات هو خط
الدفاع الأول، ويُكمّله `AGENT_TOOL_USE_BOUNDARIES.md`.
