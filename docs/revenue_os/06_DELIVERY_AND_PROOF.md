# 06 — التسليم والإثبات / Delivery & Proof (Layer 6)

## العربية

### قالب النطاق (Scope)

```
Objective              Deliverables
Current workflow       Timeline
Inputs required        Price
Diagnostic activities  Exclusions
Approval process       Payment terms
```

### الاستثناءات (مهمة — تحفظ الثقة والتموضع)

```
No autonomous external sending
No scraping
No live CRM integration in diagnostic
No security / compliance claims without evidence
No revenue claims before proof
```

### الدفع

لا تبني payment الآن. استخدم payment link أو invoice. تحقق من الدعم المحلي
في السعودية والبدائل (Moyasar / Tap / PayTabs / HyperPay) حسب حسابك التجاري.

### تدفق التسليم

```
invoice_paid → onboarding_form → delivery_folder → input_review
  → diagnostic_analysis → proof_pack_draft → founder_review
  → client_delivery → upsell_recommendation
```

### مخرجات التشخيص

1. Revenue Workflow Map
2. CRM / Source Quality Review
3. AI Usage Risk Review
4. Approval Boundaries
5. Evidence Trail Gaps
6. Top 3 Revenue Decisions
7. Proof Pack
8. Sprint / Retainer Recommendation

### الربط بالنظام

- تجميع الـ Proof Pack: `auto_client_acquisition/proof_os/proof_pack.py`
  (14 قسماً، ثنائي اللغة، proof score محسوب).
- الفوترة والتجديد: `auto_client_acquisition/payment_ops/`.
- مساحة عمل العميل: `auto_client_acquisition/client_os/`.
- ⚠️ `no_live_charge` — لا شحن إلا في تدفقات دفع معتمدة. لا تسجيل إيراد قبل
  `invoice_paid`.

---

## English

### Scope template

```
Objective              Deliverables
Current workflow       Timeline
Inputs required        Price
Diagnostic activities  Exclusions
Approval process       Payment terms
```

### Exclusions (important — they protect trust and positioning)

```
No autonomous external sending
No scraping
No live CRM integration in diagnostic
No security / compliance claims without evidence
No revenue claims before proof
```

### Payment

Do not build payment now. Use a payment link or invoice. Verify local support
in Saudi Arabia and the alternatives (Moyasar / Tap / PayTabs / HyperPay)
depending on your merchant account.

### Delivery flow

```
invoice_paid → onboarding_form → delivery_folder → input_review
  → diagnostic_analysis → proof_pack_draft → founder_review
  → client_delivery → upsell_recommendation
```

### Diagnostic deliverables

1. Revenue Workflow Map
2. CRM / Source Quality Review
3. AI Usage Risk Review
4. Approval Boundaries
5. Evidence Trail Gaps
6. Top 3 Revenue Decisions
7. Proof Pack
8. Sprint / Retainer Recommendation

### How it connects to the system

- Proof Pack assembly: `auto_client_acquisition/proof_os/proof_pack.py`
  (14 sections, bilingual, computed proof score).
- Invoicing and renewal: `auto_client_acquisition/payment_ops/`.
- Client workspace: `auto_client_acquisition/client_os/`.
- ⚠️ `no_live_charge` — no charge except in approved payment flows. No revenue
  recorded before `invoice_paid`.
