# حزم Dealix التجارية — Governed Revenue & AI Operations

**المرجع الرسمي للتسعير والنطاق:** هذا الملف هو مصدر الحقيقة التجاري داخل الريبو.

## التموضع المعتمد

**Dealix لا تبيع AI عام.**  
Dealix تبيع تشغيل الإيراد والذكاء الاصطناعي بطريقة محكومة:

```text
Signal → Source → Approval → Action → Evidence → Decision → Value → Asset
```

## North Star (تشغيلي)

**Governed Value Decisions Created**  
عدد القرارات التي لها مصدر واضح + موافقة واضحة + أثر قابل للقياس + evidence trail.

## العروض الثلاثة الأساسية (Go-To-Market)

| العرض | السعر (SAR) | النتيجة المتوقعة |
|------|-------------:|------------------|
| **Governed Revenue Ops Diagnostic** | **4,999 – 15,000** | كشف فجوات pipeline/CRM/AI governance + Decision Passport + فرص Proof |
| **Revenue Intelligence Sprint** | **25,000** | أولوية الحسابات + تقييم المخاطر + Drafts + Proof Pack + خطة قرار |
| **Governed Ops Retainer** | **4,999 – 15,000 / شهر** | مراجعة شهرية للإيراد + الحوكمة + Queue موافقات + تقرير قيمة |

### نطاق Enterprise

- Diagnostic Enterprise: **15,000 – 25,000**
- Retainer Enterprise: **15,000 – 35,000 / شهر**

## عروض داعمة (تُباع عند الحاجة)

| العرض | متى يُعرض | نطاق السعر |
|------|-----------|-----------:|
| **AI Governance for Revenue Teams** | عند وجود استخدام AI بلا حدود موافقات واضحة | حسب SOW |
| **CRM / Data Readiness for AI** | عندما تكون جودة البيانات ضعيفة وتمنع التشغيل | حسب SOW |
| **Board Decision Memo** | عند الحاجة لمذكرة قرار تنفيذية للإدارة | حسب SOW |
| **Trust Pack Lite** | فقط إذا العميل طلب security/trust صراحة | حسب SOW |

## ما نبيعه أولًا وما لا نبيعه أولًا

### نبيع أولًا

1. Diagnostic
2. Sprint
3. Retainer

### لا نبيع أولًا

- SaaS عام.
- Agent autonomy خارجي.
- أي "send automatically".
- Dashboard ضخم بدون استخدام مدفوع متكرر.

## قواعد حوكمة غير قابلة للتفاوض

- لا إرسال خارجي بدون موافقة مؤسس/مالك القرار.
- لا cold WhatsApp.
- لا LinkedIn automation.
- لا scraping إنتاجي لمصادر محظورة.
- لا `revenue` قبل `invoice_paid`.
- لا Proof public قبل تحقق مستوى دليل مناسب + موافقة.

## مخرجات كل عرض (مستوى تنفيذي)

### 1) Governed Revenue Ops Diagnostic

يشمل:
- Revenue Workflow Map
- CRM / Source Quality Review
- Pipeline Risk Map
- Follow-up Gap Analysis
- Decision Passport
- Recommended Sprint / Retainer

لا يشمل:
- إرسال خارجي مباشر
- حملات آلية
- بناء منصة جديدة

### 2) Revenue Intelligence Sprint

يشمل:
- Account Prioritization
- Deal Risk Scoring
- Next Best Action Drafts
- Follow-up Templates (draft-only)
- Revenue Opportunity Ledger
- Decision Passport
- Proof Pack

لا يشمل:
- تنفيذ live send تلقائي
- claim إيراد بدون دفع

### 3) Governed Ops Retainer

يشمل:
- Monthly Revenue Review
- Pipeline Quality Review
- AI Decision Review
- Approved Follow-up Queue
- Risk Register
- Value Report
- Board Memo

## الربط مع الريبو (Product-to-Service)

| المكوّن | المسار |
|--------|--------|
| Decision Passport | `GET /api/v1/decision-passport/golden-chain` + `POST /api/v1/leads` |
| Revenue OS Catalog / Source Rules | `GET /api/v1/revenue-os/catalog` |
| Anti-waste / governance checks | `POST /api/v1/revenue-os/anti-waste/check` |
| Proof + evidence handling | `proof_ledger/` + `proof_engine/` |
| Approval-first safety | `approval_center` + channel policy gates |

## مسار التحويل التشغيلي

```text
Diagnostic → Sprint → Retainer → Repeated workflow signal → Build module
```

## سياسة البناء

لا نبني ميزة جديدة إلا إذا تحقق واحد على الأقل:
- طلب عميل مدفوع.
- نفس workflow تكرر 3 مرات.
- تقليل مخاطرة تشغيلية حقيقية.
- تسريع تسليم مدفوع.
- فتح Retainer واضح.

## روابط داخلية

- [تموضع Enterprise الرسمي](../strategic/ENTERPRISE_OFFER_POSITIONING_AR.md)
- [نموذج التشغيل الأعظم](../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md)
- [الحلقة التجارية اليومية](../ops/DAILY_COMMERCIAL_LOOP_AR.md)
