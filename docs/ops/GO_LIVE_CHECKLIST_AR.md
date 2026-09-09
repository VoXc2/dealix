# قائمة التحقق — تدشين Dealix التجاري
# Go-Live Checklist — Dealix Commercial Launch

**الإصدار**: 2.0 | **الحالة**: Quote-only / approval-gated | **المسؤول**: الفاوندر

> هذا المستند تشغيلي ولا يمنح صلاحية تنفيذ مادي. الإطلاق التجاري الحالي لا يستخدم سعرًا عامًا ثابتًا ولا public checkout. المسار المعتمد هو:
>
> **Free Mini Diagnostic → Qualified Discovery → Customer-Specific Quote → Verified Payment → Governed Delivery → Customer-Validated Proof**

---

## 1. Railway — إعداد البيئة بدون أسرار داخل المستودع

ضع القيم السرية فقط في Railway/secret store المناسب. لا تنسخ قيمة سرية إلى Git أو logs أو proof packs.

```bash
# أسماء المتغيرات فقط — القيم الحقيقية تحفظ خارج المستودع.
MOYASAR_SECRET_KEY=<secret-store-value>
MOYASAR_WEBHOOK_SECRET=<secret-store-value>
MOYASAR_LIVE_MODE=0

ZATCA_CSID=<secret-store-value>
ZATCA_SECRET=<secret-store-value>
ZATCA_SANDBOX=true
ZATCA_SELLER_VAT_NUMBER=<registered-vat-number>
ZATCA_SELLER_NAME=Dealix
ZATCA_SELLER_CITY=Riyadh

GMAIL_CREDENTIALS_JSON=<secret-store-value>
GMAIL_SENDER_EMAIL=<approved-sender>

DEALIX_FOUNDER_PHONE=<approved-e164-number>
WHATSAPP_ALLOW_LIVE_SEND=false
WHATSAPP_API_TOKEN=<secret-store-value>

ANTHROPIC_API_KEY=<secret-store-value>
OPENAI_API_KEY=<secret-store-value>

DATABASE_URL=<managed-database-url>
REDIS_URL=<managed-redis-url>

DEALIX_ADMIN_API_KEY=<secret-store-value>
SECRET_KEY=<secret-store-value>
```

### تحقق Railway

- [ ] افحص staged changes قبل أي apply؛ لا تطبقها جماعيًا دون reconciliation.
- [ ] أثبت deployment SHA لكل من Web وAPI.
- [ ] أثبت أن running release يطابق الـSHA المقبول.
- [ ] تحقق من `/healthz` و`/health/deep` على النسخة الصحيحة، لا على مجرد HTTP 200.
- [ ] أبقِ `PRODUCTION_GREEN=false` حتى اكتمال release parity + front-door acceptance.

---

## 2. الدفع والفوترة — بعد Customer-Specific Quote فقط

- [ ] لا يوجد public fixed-price checkout في launch authority الحالية.
- [ ] لا تنشئ payment handoff قبل وجود `qualified_discovery` و`quote_id` و`customer_specific_quote_sar` موثقين.
- [ ] `QUOTE != INVOICE != PAYMENT`.
- [ ] لا تعتبر invoice أو payment link دليل دفع.
- [ ] `Verified Payment` يحتاج provider/payment evidence صالحًا.
- [ ] أبقِ Moyasar live mode معطلًا حتى موافقة تنفيذ مادية محددة.
- [ ] اختبر ZATCA في sandbox قبل أي انتقال production.

---

## 3. الاختبار التجاري الآمن

### أ. Diagnostic inbound

اختبر مسار التشخيص والاستقبال بدون إرسال خارجي أو تحصيل:

```bash
API="https://api.dealix.me"
ADMIN_KEY="<runtime-admin-key>"

curl -X POST "$API/api/v1/commercial/diagnostic/generate" \
  -H "X-API-Key: $ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"company_name":"شركة الاختبار","sector":"b2b_services","pain_points":["lead_gen"]}'
```

### ب. Draft-only commercial movement

- [ ] أنشئ draft reply/proposal فقط.
- [ ] تحقق من WHY THEM / WHY NOW / INSIGHT / PROBLEM / CTA.
- [ ] تحقق من relationship state وconsent state قبل أي قناة خارجية.
- [ ] `draft != sent`.
- [ ] public contact data لا يساوي consent.

### ج. Customer-specific quote

- [ ] Discovery evidence موجود.
- [ ] Scope وحدود التسليم موثقة.
- [ ] السعر خاص بالعميل ومربوط بـquote ID.
- [ ] لا يوجد guarantee أو unsupported ROI claim.
- [ ] أي handoff للدفع approval-gated.

---

## 4. WhatsApp / Gmail / القنوات

- [ ] WhatsApp inbound-first وconsent-aware.
- [ ] لا cold WhatsApp blast.
- [ ] لا mass LinkedIn automation.
- [ ] البريد الخارجي يبقى draft-only ما لم توجد صلاحية إرسال محددة.
- [ ] founder LinkedIn يبقى human-operated.
- [ ] كل opt-out أو سحب موافقة يوقف direct marketing المقابل.

---

## 5. Governed Delivery

لا يبدأ delivery لمجرد وجود lead أو diagnostic أو proposal أو invoice.

ابدأ فقط بعد handoff موثق يثبت الحالة المطلوبة، ثم أنشئ:

- [ ] Customer workspace
- [ ] Baseline
- [ ] Acceptance criteria
- [ ] 30-day plan
- [ ] Weekly Proof Pack
- [ ] Decisions / risks / blockers
- [ ] Final Outcome Review
- [ ] Expansion / Stop / Redesign recommendation

`synthetic/demo output != customer proof`.

---

## 6. Front-door acceptance

أثبت السلسلة التالية على exact release:

`accepted main SHA → Railway deployment SHA → running release SHA → Web/API health → dealix.me → www.dealix.me → /ar → TLS/redirects → diagnostic path`

### بوابات الفشل المغلق

- [ ] Python required tests = PASS حقيقي، لا wrapper label فقط.
- [ ] Web typecheck/build = PASS حقيقي.
- [ ] ShellCheck/actionlint/secret scan = PASS.
- [ ] Migration graph = single current head.
- [ ] Brand/public truth verifiers = PASS.
- [ ] أي hosted job لم يبدأ (`steps=[]` / no runner) يصنف `BLOCKED_EXECUTION_PLANE` وليس code PASS أو code FAIL.

---

## 7. شروط Production Green

لا تغيّر `PRODUCTION_GREEN=true` إلا بعد تحقق جميع الآتي على evidence حديث:

- [ ] exact-main acceptance
- [ ] exact Web/API release parity
- [ ] front-door acceptance
- [ ] no unresolved P0 release-trust defects
- [ ] no unreviewed staged production mutations
- [ ] no secret leakage findings
- [ ] rollback path موثق

حتى ذلك الوقت:

```text
PRODUCTION_GREEN=false
MERGE_EXECUTED=false unless specifically authorized
DEPLOY_EXECUTED=false unless specifically authorized
PUBLIC_PUBLISH=false
PAYMENT_EXECUTION=false
```

---

## 8. مؤشرات أول دورة تجارية حقيقية

لا تستخدم أهداف vanity أو وعود مضمونة. تتبع فقط الأدلة التالية:

| المؤشر | الحقيقة المطلوبة |
|---|---|
| Real Interaction | تفاعل موثق، وليس research فقط |
| Qualified Problem | مشكلة مؤهلة بدليل |
| Discovery | جلسة/إثبات discovery فعلي |
| Customer-Specific Quote | quote موثق خاص بالعميل |
| Verified Payment | دليل provider/payment صالح |
| Governed Delivery | خطة وتسليم مع acceptance criteria |
| Customer-Validated Proof | نتيجة مؤكدة من نفس العميل |
| Repeatability | تكرار موثق، لا افتراض |

---

**Dealix — Signals into Action. Execution with Governance. Measurable Outcomes.**
