# ترتيب طبقة الأدلة (Proof Stack) — قبل الديمو وبعده

**الغرض:** إرسال **الحد الأدنى الموثوق** من الأدلة بالترتيب — امتثال وخصوصية أولاً، ثم pilot، ثم حالة نجاح — كما يوصي سوق B2B السعودي (ثقة قبل الميزات).

**لا تُرسل طبقة 4–5** قبل `discovery_completed` إلا بطلب صريح من العميل.

---

## الطبقات (1 → 5)

| طبقة | المحتوى | متى | ملف / مسار |
|------|---------|-----|------------|
| **1 — امتثال وخصوصية** | لغة PDPL آمنة، DPA outline، إقامة/منطقة | أول لمسة warm · قبل أي بيانات عميل | [MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md](../MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) · [INFRA_HOSTING_REGION_RUBRIC_AR.md](../INFRA_HOSTING_REGION_RUBRIC_AR.md) |
| **2 — تموضع Why Now** | صفحة واحدة: مخاطر قرار · Decision Passport vs CRM | مع طلب اجتماع 10 دقائق | [POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md](../POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md) |
| **3 — عيّنة Proof (لا بيانات عميل)** | Proof Pack وكالة · Risk Score · Diagnostic landing | بعد رد إيجابي · قبل ديمو 30 دقيقة | [sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md](sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md) · `/ar/proof-pack` · `/ar/risk-score` |
| **4 — Pilot مقنّن** | نطاق Sprint/تشخيص · SOW قصير · SLA تسليم | بعد Discovery السبعة | [motion_a_agency/SCOPE_AGENCY_AUDIT_AR.md](motion_a_agency/SCOPE_AGENCY_AUDIT_AR.md) · [templates/SCOPE_SPRINT_SAR.md](../templates/SCOPE_SPRINT_SAR.md) · [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](FIRST_PAID_DIAGNOSTIC_DOD_AR.md) |
| **5 — حالة نجاح عربية** | قصة عميل/قطاع (حتى anonymized) · شهادة شريك | بعد `payment_received` أو بإذن كتابي | [samples/LEAD_INTELLIGENCE_SPRINT_SAMPLE_REPORT_AR.md](../samples/LEAD_INTELLIGENCE_SPRINT_SAMPLE_REPORT_AR.md) — **وسّع عند وجود عميل حقيقي** |

---

## تدفق حسب مرحلة الصفقة

```text
warm_touch → طبقة 1 + 2 (PDF/رابط)
reply_positive → طبقة 3
discovery_completed → طبقة 4 (عرض مدفوع واضح)
payment_received → تسليم Proof + طبقة 5 عند الموافقة
```

---

## ما لا يُعدّ دليلاً (ممنوع في الوعود)

- لقطات dashboard بدون `source_id` / SOAEN
- أرقام إيراد من CRM غير مُستوردة في KPI
- «AI يغلق الصفقات» أو cold automation
- case study بأسماء بدون إذن

---

## ربط SOAEN

| حرف | في الطبقة |
|-----|-----------|
| S | مصدر كل ملف مُرسل (`proof_asset_sent` في War Room) |
| O | مالك المتابعة (المؤسس) |
| A | موافقة قبل إرسال خارجي |
| E | مستوى دليل L0–L5 إن طُبّق ([evidence levels API](/api/v1/decision-passport/evidence-levels)) |
| N | `next_action` بعد الإرسال |

---

## قائمة تحقق سريعة (قبل Calendly)

- [ ] طبقة 1 مرسلة أو مذكورة شفهياً
- [ ] طبقة 2 مرفقة في email warm
- [ ] طبقة 3 **فقط** إن طلب «أرني مثالاً»
- [ ] لا مرفقات تحتوي PII عميل آخر
- [ ] سجّل في `evidence_events_tracker.csv`: `proof_asset_sent` أو `message_sent_manual`

**السابق:** [FOUNDER_SALES_LOOP_AR.md](FOUNDER_SALES_LOOP_AR.md) · **التشغيل:** [GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md](../GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md)
