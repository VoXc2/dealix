# Weekly Value Reports — تقارير القيمة الأسبوعية

**الهدف:** كل أسبوع، يُجهَّز تقرير قيمة لكل عميل في التسليم يوضح: ما أُنجز، أي قيمة تحققت، حالة القبول، وتركيز الأسبوع القادم. التقرير يبقى **مسودة حتى موافقة المؤسس** قبل الإرسال.

- **Schema:** [`schemas/weekly_value_report.schema.json`](../../schemas/weekly_value_report.schema.json)
- **البيانات:** [`data/delivery/weekly_value_reports.jsonl`](../../data/delivery/weekly_value_reports.jsonl)
- **الطابور:** [`reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md`](../../reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md)

---

## 1. البنية

```txt
report_id · pipeline_id · company · system · week_of
deliverables_completed[] · metrics[] · value_delivered
acceptance_status (pending|accepted|changes_requested)
next_week_focus · blockers[] · approval_required (true)
```

## 2. مثال (من البيانات)

```txt
Company: Digital Rise Agency — Revenue Operating System
Week of: 2026-05-26
Deliverables: Revenue Leakage Map · Opportunity Stage Model · Follow-up Workflow
Value delivered: كل فرصة أصبحت لها حالة وخطوة تالية، وتحدّدت أكبر نقطة تسرب في خط البيع.
Acceptance: accepted
Next week: تثبيت تقرير الإيراد الأسبوعي وتشغيل تدفق المتابعة عمليًا.
```

## 3. الإيقاع والموافقة

```txt
- تقرير لكل عميل في التسليم، أسبوعيًا.
- يبقى مسودة (approval_required = true) حتى يعتمده المؤسس.
- الحالات pending تظهر في طابور الموافقة لتُراجَع وتُرسَل.
```

## 4. قواعد المحتوى

- لا أرقام عائد مؤكدة ولا وعود — نوثّق **ما أُنجز فعلًا** و**قيمة قابلة للملاحظة**.
- لا أسرار ولا بيانات شخصية (يُفحَص بـ C07).
- الفحص **C06** يمنع أي مصطلح ضمان في `value_delivered` / `next_week_focus`.
- الفحص **C08** يضمن أن التقرير يبقى مسودة (`approval_required = true`).
