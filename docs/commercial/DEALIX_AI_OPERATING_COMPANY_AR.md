# Dealix — شركة تشغيل محكوم للإيراد والذكاء الاصطناعي (المرجع الشامل)

**الموقف:** Dealix ليست «وكالة AI»، وليست RevOps تقليدية، وليست dashboard SaaS.
هي **Governed Revenue & AI Operations Company**: تبني وتشغّل **طبقة التشغيل
المحكومة** بين تجارب الذكاء الاصطناعي، وworkflows الإيراد، والعمليات المؤسسية،
والموافقات، والأدلة، وإثبات القيمة.

**المعنى العملي:** كل مخرج AI له مصدر؛ كل فعل له موافقة؛ كل فرصة لها دليل؛ كل
قرار عميل له passport؛ كل engagement ينتج proof؛ كل proof يتحول إلى asset.

**الأسعار التفصيلية:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md)
و [../COMPANY_SERVICE_LADDER.md](../COMPANY_SERVICE_LADDER.md).

## الرؤية

Dealix تصبح **طبقة التشغيل الخليجية** التي تحوّل تجارب الذكاء الاصطناعي وعمليات
الإيراد إلى workflows محكومة، قابلة للقياس، ومربوطة بالأدلة.

السوق متخم بأدوات AI لكنه ناقص في التشغيل والحوكمة والثقة والـ ROI. الفرصة ليست
في «AI أكثر» بل في «AI يعمل داخل شركة بطريقة محكومة ومربوطة بالقيمة».

## الاستراتيجية الكبرى — Service-led, software-assisted, evidence-first

لا تبدأ كـ SaaS. التسلسل:

```text
Diagnostic -> Sprint -> Retainer -> Reusable Playbook -> Internal Platform
```

- بدء SaaS قبل proof = بناء أشياء لا يطلبها السوق.
- بدء خدمات بلا نظام = agency عادية.
- الصحيح: خدمات عالية القيمة مدعومة بنظام داخلي يتحول تدريجياً إلى منصة — وفق
  بوابة G7 فقط.

## نجم الشمال

**Governed Value Decisions Created** — تفصيل قاعدة العدّ في
[NORTH_STAR_METRICS_AR.md](NORTH_STAR_METRICS_AR.md).

## القاعدة الذهبية لكل خدمة

1. وعد واضح
2. نطاق واضح
3. مدخلات مطلوبة من العميل
4. عملية تنفيذ ثابتة
5. مخرجات ملموسة
6. مقياس نجاح
7. ترقية طبيعية للخدمة التالية

## كتالوج الخدمات

المرجع الكامل للخدمات السبع والعروض الثلاثة الرئيسية في
[كتالوج الخدمات](../COMPANY_SERVICE_LADDER.md). ملخص: Governed Revenue Ops
Diagnostic (نطاق 4,999–25,000)، Revenue Intelligence Sprint
(`recommended_draft`)، Governed Ops Retainer (`recommended_draft`)، AI
Governance for Revenue Teams، CRM / Data Readiness for AI، Board Decision Memo،
Trust Pack Lite.

## أنظمة التشغيل الداخلية (الكود)

طبقة التشغيل المحكومة مبنية من وحدات تحت `auto_client_acquisition/`:

| النظام | الغرض | وحدة الكود |
|--------|-------|------------|
| Commercial OS | آلة الحالة CEL والبوابات G1–G7 | `commercial_os/` |
| Revenue Ops | تشخيص، رفع CRM، scoring، مسودات متابعة | `revenue_os/`، `revenue_ops/` |
| Data OS | جودة بيانات وجاهزية AI | `data_os/` |
| Governance OS | سياسات، بوابة مسودات، مصفوفة موافقات | `governance_os/` |
| Proof OS | تجميع وتقييم Proof Pack | `proof_os/` |
| Value OS | سجل القيمة وتقارير القيمة | `value_os/` |
| Capital OS | سجل الأصول الرأسمالية | `capital_os/` |
| Sales OS | تأهيل، عروض، scoring | `sales_os/` |
| Board Decision OS | مذكرات وقرارات تنفيذية | `board_decision_os/` |

ربط الأنظمة بالراوترات والمشغّلات: [CODE_MAP_OS_TO_MODULES_AR.md](CODE_MAP_OS_TO_MODULES_AR.md).

## معيار التسليم — Dealix Delivery Standard

```text
Discover -> Diagnose -> Design -> Build -> Validate -> Deliver -> Prove -> Expand
```

| المرحلة | سؤال مركزي |
|---------|------------|
| Discover | ما المشكلة، الداتا، الفريق، الأدوات، أين الضياع؟ |
| Diagnose | جاهزية بيانات، نضج عمليات، مخاطر، ROI سريع؟ |
| Design | workflow، موافقات، مخرجات، مقاييس؟ |
| Build | أقل تعقيد، human-in-the-loop، سجلات؟ |
| Validate | جودة، أمان، لغة، حالات حافة؟ |
| Deliver | تقارير، SOP، تدريب، handoff؟ |
| Prove | قبل/بعد، أرقام بمصدر، دليل؟ |
| Expand | retainer، workflow إضافي، حوكمة؟ |

## إطار QA (قبل التسليم)

- **Business QA:** أثر إداري، KPI، next action، upsell؟
- **Data QA:** مصدر، تكرار، فراغات، PII، lawful basis؟
- **AI QA:** دقة، مصادر، عربي، edge cases؟
- **Compliance QA:** ادعاءات، إرسال بارد، موافقة، audit؟
- **Delivery QA:** اكتمال المخرجات، وضوح التقرير، renewal؟

## درجة جودة المشروع الداخلية (0–100)

| المعيار | الوزن |
|---------|------:|
| وضوح أثر الأعمال | 20 |
| جودة البيانات | 15 |
| جودة المخرجات لغوياً | 15 |
| سهولة استخدام العميل | 10 |
| الأمان والامتثال | 15 |
| قابلية التكرار كمنتج | 15 |
| قابلية الترقية لـ retainer | 10 |

**قاعدة:** أي مشروع بدرجة أقل من 80 لا يُسلَّم كـ«ممتاز» دون تحسين.

## معنى Full Ops الصحيح

Full Ops **لا** يعني أن الذكاء الاصطناعي يرسل ويحاسب ويتصرف وحده. Full Ops يعني:
النظام يجهّز، يقترح، يحذّر، يسجّل، يتحقق، يصنّف، يولّد draft — والمؤسس يوافق على
الأفعال الخارجية. هذا يحمي من prompt injection وtool misuse وover-automation.
تصميم approval-first ليس بطئاً؛ هو ميزة ثقة.

## التفوق التنافسي

1. **Outcome-first** — كل خدمة بنتيجة قابلة للقياس.
2. **Saudi-localized** — عربي أعمال، قطاعات، مدن، PDPL.
3. **Proof-backed** — Proof ledger وتقارير قبل/بعد.
4. **Governed AI** — مصادر، موافقة، عدم إرسال بارد.
5. **Productized delivery** — نفس القوالب لكل عميل.

**الجملة الحاكمة:** Dealix لا تبيع AI فقط، ولا RevOps فقط. Dealix تبيع التشغيل
المحكوم للإيراد والذكاء الاصطناعي: مصادر واضحة، موافقات، أدلة، قرارات، وقيمة
قابلة للقياس.

## روابط داخلية

- [كتالوج الخدمات السبع](../COMPANY_SERVICE_LADDER.md)
- [حزم الإيراد والأسعار](DEALIX_REVOPS_PACKAGES_AR.md)
- [آلة الحالة CEL](COMMERCIAL_EVIDENCE_STATE_MACHINE.md)
- [البوابات التجارية G1–G7](COMMERCIAL_GATES.md)
- [رسالة البيع](SALES_MESSAGE.md)
- [التموضع التنافسي](../COMPETITIVE_POSITIONING.md)
