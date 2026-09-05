<div align="center" dir="rtl">

# Dealix — منصة التنفيذ الذكي المحكوم للأعمال في السعودية

**حوّل إشارات شركتك إلى قرارات وتنفيذ ونتائج قابلة للإثبات.**

`Signal -> Decision -> Action -> Proof`

سعودي أولًا · عرض خاص بالعميل · تنفيذ محكوم بالدليل والموافقة

**العربية** · **[English](README.md)**

[مصدر الحقيقة](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md) · [التدشين](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md) · [جاهزية الإنتاج](docs/ops/PRODUCTION_READINESS_CHECKLIST.md) · [بوابة الإطلاق التجاري](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)

</div>

---

## ما هي Dealix؟

Dealix **منصة تنفيذ ذكي محكوم للأعمال في السعودية**. تربط الإشارات الرسمية/الأولية الخاصة بالشركة بالبحث والدليل والأولوية والقرار، ثم تضبط التنفيذ ضمن حدود صلاحية واضحة وتوثق ما حدث فعليًا وما الذي ثبت من قيمة.

تحت الواجهة السوقية تعمل Dealix كـ **AI Business Operating System / Company Machine** واحدة تشمل 12 نظام تشغيل: Command وRevenue وProof وClient وDelivery وSupport وFinance وData وGovernance وAcademy وPartner وVenture. وتبقى **Revenue + Proof + Command** لغة قدرة ومدخل اقتصادي مهم، لكنها ليست العنوان العام الحالي لفئة Dealix في السوق.

Dealix ليست Chatbot عامًا، ولا CRM بديلًا، ولا Lead Scraper، ولا ماكينة رسائل جماعية، ولا أسطول Agents غير محكوم، ولا خدمة تضمن الإيراد.

قاعدة التشغيل:

> الذكاء الاصطناعي يستكشف ويحلل ويقترح. الـworkflows المحكومة تنفذ. الأفعال الخارجية المادية تحتاج السلطة والدليل المناسبين في وقت التنفيذ.

## مسار التعامل الكنسي

1. **Execution Diagnostic** — نحدد workflow واحدًا ذا أثر اقتصادي، baseline، التسرب أو الاختناق، الأنظمة، صاحب القرار، حدود البيانات ومعايير الإثبات.
2. **Qualified Discovery + Customer-Specific Quote** — نثبت النطاق وشروط البدء ثم نصدر عرضًا خاصًا بالعميل.
3. **Outcome Sprint** — تنفيذ محكوم لحالة محددة بمعايير قبول قابلة للقياس؛ المدة والنطاق خاصان بالعميل.
4. **Proof Review** — نقارن النتيجة بالـbaseline ونفصل النشاط عن القيمة المثبتة.
5. **Dealix Runtime** — تشغيل مستمر مُدار/منصّي فقط للـworkflows التي أثبتت قيمة قابلة للتكرار.

**لا توجد قائمة أسعار عامة، ولا Checkout عام، ولا ضمان عائد أو إيراد أو نتيجة.**

قد تبقى معرفات داخلية تاريخية مثل `free_mini_diagnostic` و`revenue_command_pilot_30d` كـcompatibility IDs إلى أن يكتمل migration تشغيلي مقبول. هذه المعرفات لا تعيد الأسماء السوقية القديمة ولا تمنح سلطة تسعير عامة.

## شركة واحدة / خمسة ملاك دائمين

- `dealix-pm` — الرئيس: المال، الأولويات، القرارات، المخاطر، الموافقات والخطوة التالية.
- `dealix-sales` — الإشارات، بحث الحسابات، التأهيل، التشخيص، Discovery، وتحضير التفاوض.
- `dealix-delivery` — Onboarding، التنفيذ، الدعم، القبول وإعداد الـProof.
- `dealix-engineer` — الاعتمادية، التكاملات، بوابات الثقة وأي تطوير يزيد Cash أو Trust أو Repeatability.
- `dealix-content` — محتوى المؤسس/الشركة/البحث والتوزيع المبني على دليل.

أي specialist هو workload محدود تحت هؤلاء، وليس Agent دائمًا جديدًا. لا نبني Company OS أو Brain أو CRM أو Opportunity Graph أو Approval Center أو Proof Ledger أو Scheduler أو Model Router أو Control Plane موازية.

## Truth Firewall

لا تخلط Dealix بين:

- research != relationship
- public contact != consent
- lead != buyer intent
- draft != sent
- quote != invoice
- invoice != payment
- synthetic/demo != customer proof
- PR != production
- historical PASS != current exact-head PASS

## ضوابط التواصل والنمو

- لا scraping كاختصار للنمو.
- لا cold WhatsApp automation.
- لا mass/unapproved LinkedIn automation.
- لا إرسال خارجي آلي دون السلطة الحالية المطلوبة.
- لا proof مزيف ولا علاقات مزيفة ولا انتحال هوية ولا ban-evasion.
- يمكن تجهيز رسائل Founder-quality بوضوح على أنها من Dealix أو نيابةً عن المؤسس.

## البدء السريع

```bash
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
make setup
cp .env.example .env
make run
```

توثيق الـAPI محليًا: `http://localhost:8000/docs`

تحقق شبيه بالإنتاج:

```bash
make prod-verify
```

فحوص مفيدة:

```bash
make env-check
make api-contract-check
make security-smoke
make production-smoke
make dependency-inventory
make release-manifest
make test
make security
```

## نموذج المعمارية

| الطبقة | المسؤولية |
|---|---|
| Decision | Agents، reasoning، synthesis وتجميع الأدلة. |
| Execution | workflows حتمية، retries، compensation والتزامات محكومة. |
| Trust | policy، approval، audit، verification وProof. |
| Data | الحقيقة التشغيلية، lineage، metrics والتكاملات. |
| Operating | CI/CD، Docker، الانضباط الإصدارّي، حوكمة الريبو وrunbooks. |

## حقيقة التدشين والإنتاج

قبل أي تفعيل تجاري/عام مادي، اعتمد الدليل الحي وليس ادعاءات README:

- [مصدر الحقيقة للمنصة](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md)
- [Launch Operator Runbook](docs/ops/LAUNCH_OPERATOR_RUNBOOK.md)
- [Production Readiness Checklist](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [Commercial Go-Live Gate](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)
- [Domain Operations](docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md)
- [No-overclaim register](dealix/registers/no_overclaim.yaml)
- [Saudi compliance register](dealix/registers/compliance_saudi.yaml)

وجود الكود في الريبو أو حالة Provider خضراء أو PASS تاريخي لا يثبت وحده هوية الإنتاج الحالية أو وجود عميل مدفوع أو Proof تجاري.

## الأمن والسياق السعودي

Dealix مصممة حول least privilege، وحدود الموافقات والأدلة، وإبقاء الأسرار خارج المصدر، والتحقق من هوية الـruntime/provider، والسياق التشغيلي السعودي. وثائق الامتثال ليست شهادة قانونية شاملة؛ كل claim يبقى محدودًا بما تثبته الأدلة والضوابط الفعلية.

## الرخصة

MIT — راجع [LICENSE](LICENSE).
