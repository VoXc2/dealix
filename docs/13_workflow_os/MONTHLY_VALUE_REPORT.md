# تقرير القيمة الشهري (Monthly Value Report)

الأقسام الثمانية المعيارية مُعرَّفة في `auto_client_acquisition/client_os/monthly_value_report.py`.

## الاستخدام

- `build_empty_monthly_value_report()` — هيكل فارغ للتعبئة اليدوية.
- `monthly_value_report_from_sprint_kpis(...)` — نقطة بداية حتمية من أرقام Sprint (لا تُرسل للعميل دون مراجعة).
- `monthly_value_report_sections_complete(...)` — يتحقق أن كل الأقسام مملوءة قبل النشر الداخلي/العميل.

## الموجة

جزء من **موجة Retainer Engine**: يجعل الاشتراك الشهري قابلًا للشرح بالأدلة وليس بالوعود.

راجع أيضًا: `docs/client_os/MONTHLY_VALUE_REPORT.md`.
