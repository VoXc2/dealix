# Dealix — Governed Revenue & AI Operations Playbook

## التموضع النهائي

**Dealix — Governed Revenue & AI Operations**  
**Dealix — تشغيل الإيراد والذكاء الاصطناعي بحوكمة وأدلة وقياس قيمة**

صياغة المنتج:

- Dealix لا تبيع AI كأداة منفصلة.
- Dealix لا تبيع RevOps كتقارير فقط.
- Dealix تبني تشغيلًا محكومًا يربط: **Signal, Approval, Evidence, Decision, Value**.

## نجم الشمال

**Governed Value Decisions Created**

التعريف:

عدد القرارات الإيرادية/التشغيلية التي تتضمن:

1. مصدر واضح (Source)
2. موافقة واضحة (Approval)
3. دليل موثق (Evidence)
4. قيمة قابلة للقياس (Value)

## العقيدة التشغيلية

```text
Signal -> Source -> Approval -> Action -> Evidence -> Decision -> Value -> Asset
```

كل نشاط خارج هذه السلسلة يعتبر ضجيجًا غير قابل للتوسع.

## خدمة-إلى-منصة (الترتيب الإلزامي)

```text
Diagnostic -> Sprint -> Retainer -> Reusable Playbook -> Internal Platform -> SaaS Module
```

قواعد:

- لا SaaS-first.
- لا autonomous external actions.
- لا build قبل تكرار workflow ثلاث مرات أو طلب عميل صريح.

## كتالوج الخدمات التشغيلي (7)

1. **Governed Revenue Ops Diagnostic** — 4,999 إلى 25,000 SAR
2. **Revenue Intelligence Sprint** — يبدأ من 25,000 SAR
3. **Governed Ops Retainer** — 4,999 إلى 35,000 SAR / month
4. **AI Governance for Revenue Teams**
5. **CRM / Data Readiness for AI**
6. **Board Decision Memo**
7. **Trust Pack Lite** (on-demand only)

قاعدة GTM: أول مقابلة تعرض 3 خدمات فقط: Diagnostic -> Sprint -> Retainer.

## State Machine (L2 -> L7)

| State | Level |
|---|---|
| prepared_not_sent | L2 |
| sent | L4 |
| replied_interested | L4 |
| meeting_booked | L4 |
| used_in_meeting | L5 |
| scope_requested | L6 |
| pilot_intro_requested | L6 |
| invoice_sent | L7_candidate |
| invoice_paid | L7_confirmed |

## القواعد الصارمة

- لا `sent` بدون `founder_confirmed=true`.
- لا `L7_confirmed` بدون `payment_received=true`.
- لا Revenue قبل `invoice_paid`.
- لا أفعال خارجية تلقائية (`send`, `charge`, `publish`) بدون موافقة.

## Full Ops الحقيقي

Full Ops لا يعني تشغيل خارجي ذاتي بلا رقابة.  
Full Ops يعني:

- النظام يجهّز ويقترح ويحذّر.
- النظام يسجل الأدلة ويصنف المخاطر.
- النظام ينتج Drafts.
- المؤسس يعتمد الأفعال الخارجية.

## بوابات التقدم

1. **First Market Proof**: أول `sent` مثبت
2. **Meeting Proof**: `used_in_meeting`
3. **Pull Proof**: `scope_requested` أو `pilot_intro_requested`
4. **Revenue Proof**: `invoice_paid`
5. **Repeatability**: نفس العرض يباع مرتين
6. **Retainer**: قيمة شهرية متكررة
7. **Platform Signal**: workflow يدوي تكرر 3+ مرات

## ما لا نفعله

- لا cold WhatsApp.
- لا LinkedIn DM automation.
- لا external Gmail send بدون موافقة.
- لا claims تسويقية بدون evidence level مناسب.
- لا رفع artificial KPIs بلا source.

## التنفيذ داخل الكود

- API Contracts: `api/routers/governed_revenue_ops.py`
- Core Model: `auto_client_acquisition/governed_revenue_ops/core.py`
- Tests: `tests/test_governed_revenue_ops.py`

هذه الطبقة هي مرجع التشغيل المحكوم الذي يربط القرار بالقيمة ويمنع التشغيل الخطر.
