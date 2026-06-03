# Agent Runbooks — أدلة تشغيل الوكلاء

> لكل وكيل runbook: المدخل، الخطوات، بوابة الجودة، قاعدة الإيقاف، والمخرج.
> هذه الأدلة تجعل التفويض ممكنًا دون فقدان الجودة.

---

## القالب الموحّد

```txt
Agent:           <الاسم>
Level:           <L1–L5>
Workflow:        <اسم سير العمل>
Input contract:  <المدخل الدقيق>
Steps:           <الخطوات>
Quality gate:    <شرط قبول المخرج>
Stop rule:       <متى يتوقف>
Output:          <المخرج الدقيق>
Audit:           ai_action_ledger.jsonl
Owner:           Founder
```

---

## Account Research Agent (L1)

- **Input:** اسم الشركة + الدومين العام.
- **Steps:** اجمع بيانات عامة فقط → لخّص الملف → اذكر المصادر.
- **Quality gate:** كل ادعاء له مصدر، لا PII، لا بيانات خاصة.
- **Stop rule:** إذا تطلبت البيانات مصادقة أو بدت خاصة → توقّف وبلّغ.
- **Output:** `account_pack_draft` (مسوّدة).

## Need Detection Agent (L2)

- **Input:** Account Pack.
- **Steps:** حلّل الإشارات → استنتج الاحتياج → احسب درجة الوضوح.
- **Quality gate:** need clarity ≥ 75.
- **Stop rule:** الثقة < 60 → توقّف وبلّغ.
- **Output:** `recommended_need`.

## System Router Agent (L2)

- **Input:** recommended_need + system_catalog.
- **Steps:** طابق الاحتياج مع نظام من الكتالوج → حدّد أول Sprint.
- **Quality gate:** التوصية تطابق نظامًا واضحًا في الكتالوج.
- **Stop rule:** لا نظام يطابق → توقّف وبلّغ.
- **Output:** `recommendation`.

## Email Draft Agent (L3)

- **Input:** need card + account pack.
- **Steps:** اكتب subject + body → تحقّق من الامتثال.
- **Quality gate:** لا claims مضمونة، لا fake Re/Fwd، متوافق مع unsubscribe، لا PII.
- **Stop rule:** لا يرسل أبدًا → يضع المسوّدة في approval_queue.
- **Output:** `email draft`.

## Call Brief Agent (L3)

- **Input:** account pack + need card.
- **Steps:** جهّز نقاط الحديث + الاعتراضات المتوقعة.
- **Quality gate:** لا اتصال آلي، متصل بشري فقط.
- **Stop rule:** لا يجري اتصالات آلية أبدًا.
- **Output:** `call brief`.

## Proposal Agent (L3)

- **Input:** account pack + approved_need + price_band.
- **Steps:** جهّز Mini Proposal ضمن النطاق السعري المعتمد.
- **Quality gate:** السعر ضمن النطاق، لا ادعاء ROI مضمون.
- **Stop rule:** لا يرسل ولا يوقّع ولا يغيّر السعر خارج النطاق.
- **Output:** `proposal draft`.

## Delivery Agent (L4)

- **Input:** won deal + signed inputs + intake.
- **Steps:** ولّد قائمة المهام والـ checklist.
- **Quality gate:** كل المدخلات المطلوبة حاضرة قبل أي مهمة.
- **Stop rule:** لا يبدأ التسليم بدون مدخلات مؤكدة وموافقة.
- **Output:** `tasks/checklist`.

## Founder Command Agent (L2)

- **Input:** التقارير اليومية + pipeline + scale state.
- **Steps:** ابنِ War Room اليومي (النقاط التسع).
- **Quality gate:** القرارات تُرفع ولا تُنفّذ.
- **Stop rule:** لا ينفّذ قرارًا أبدًا.
- **Output:** `FOUNDER_WAR_ROOM_DAILY.md`.

## Internal Reporter Agent (L5)

- **Input:** بيانات company_os الداخلية.
- **Steps:** ولّد تقريرًا داخليًا.
- **Quality gate:** المخرج يبقى داخل المستودع.
- **Stop rule:** لا مخرج يواجه العميل أو يخرج خارجيًا.
- **Output:** تقرير داخلي في `reports/`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
