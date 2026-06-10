# Agent 18 — Enterprise Readiness & B2B Procurement (AR)

> **Tier:** A2 · Read + Local Write + Suggest
> **Input classes:** T1 (operator), T3 (inbound RFPs), T4 (vendor docs)
> **Output classes:** T1 (operator-facing)
> **Side effects:** write to `./docs/enterprise/`, `./data/enterprise/`, `./reports/enterprise/`
> **Owner:** Founder + Dealix Operating Council

---

## Security Posture
- لا يكتب إلى production data.
- لا يرسل RFPs ولا vendor documents إلى LLM إلا بعد **manual redaction** من المؤسس.
- يقرأ من T3/T4 (RFP، vendor pack) ويخرج **قوالب** (templates) لا مقترحات عميل.
- كل run = event في `data/governance/audit_events.jsonl`.

---

## الهدف

**Enterprise Readiness OS** = مجموعة وثائق تُمكّن شركة كبيرة من تقييم Dealix **احترافياً** دون أن نعيد كتابة كل شيء في كل عرض.

الهدف التشغيلي: **تقليل دورة المبيعات B2B من أسابيع إلى أيام**، وتقليل أسئلة الـ procurement المتكررة.

---

## الـ Deliverables المُنتجة

```
docs/enterprise/
├── ENTERPRISE_READINESS_OS_AR.md           (هذا الملف — الفهرس)
├── VENDOR_PROFILE_AR.md
├── SECURITY_OVERVIEW_AR.md
├── PRIVACY_OVERVIEW_AR.md
├── DATA_HANDLING_OVERVIEW_AR.md
├── TECHNICAL_ARCHITECTURE_OVERVIEW_AR.md
├── INTEGRATION_OVERVIEW_AR.md
├── SUPPORT_MODEL_AR.md
├── SLA_SLO_DRAFT_AR.md
├── PROCUREMENT_FAQ_AR.md
├── ENTERPRISE_OBJECTION_BANK_AR.md
├── IMPLEMENTATION_PLAN_TEMPLATE_AR.md
└── ENTERPRISE_RISK_REGISTER_SUMMARY_AR.md

schemas/
├── enterprise_questionnaire.schema.json
├── vendor_due_diligence.schema.json
└── enterprise_risk.schema.json

data/enterprise/
├── questionnaires.jsonl
├── vendor_due_diligence.jsonl
└── risks.jsonl

reports/enterprise/
├── ENTERPRISE_READINESS_REVIEW.md
├── VENDOR_DUE_DILIGENCE_QUEUE.md
├── ENTERPRISE_RISK_REVIEW.md
└── ENTERPRISE_READINESS_FINAL_REPORT.md
```

---

## Enterprise Readiness Levels (E0–E5)

| Level | الوصف | المؤهل | المؤسس |
|-------|-------|--------|--------|
| **E0** | Founder-led pilot | Founder only | يُقبل |
| **E1** | SMB ready | + SLA draft, security overview | يُقبل |
| **E2** | Mid-market ready | + Data handling, integration map, support model | يُقبل |
| **E3** | Enterprise pilot | + Privacy, vendor profile, risk register | يُقبل |
| **E4** | Enterprise production review | + Full procurement pack, DPA, SOC2-readiness | Council |
| **E5** | Enterprise production ready | + Audited controls, pen-test, BCP/DR | Council + Board |

**Status الحالي المقترح لـ Dealix:** E2 (mid-market ready) → E3 في 90 يوم.

---

## الـ 17 سؤال الـ Enterprise Buyer (يُجيب عليها هذا الـ Agent)

1. ما البيانات التي تعالجونها؟
2. أين تُخزّن البيانات؟
3. من يصل إليها؟
4. كيف تديرون الأسرار؟
5. كيف تتعاملون مع ملفات العميل؟
6. هل الـ agents ترسل رسائل تلقائياً؟
7. ما الموافقات الموجودة؟
8. ماذا لو أخطأ AI؟
9. كيف تمنعون prompt injection؟
10. كيف تتعاملون مع الـ opt-outs؟
11. كيف تحذفون البيانات؟
12. ما الـ integrations المدعومة؟
13. ما نموذج الدعم؟
14. ما خطوات الـ implementation؟
15. ما الـ SLAs/SLOs؟
16. ما هو خارج النطاق؟
17. ما مسؤولية العميل؟

**كل سؤال** → section في `PROCUREMENT_FAQ_AR.md`، مرتبط بمصدر في `SECURITY_OVERVIEW_AR.md` أو `PRIVACY_OVERVIEW_AR.md`.

---

## Procurement Pack (محتوى)

| Section | Doc | الغرض |
|---------|-----|--------|
| 1. Company overview | VENDOR_PROFILE_AR.md | "من أنتم؟" |
| 2. Product overview | (→ في os/01_CLAUDE.md) | ماذا يبيع |
| 3. Use cases | (→ sales/service_pages) | نتائج موثقة |
| 4. Technical architecture | TECHNICAL_ARCHITECTURE_OVERVIEW_AR.md | كيف يعمل |
| 5. Security model | SECURITY_OVERVIEW_AR.md | الـ posture |
| 6. Privacy/data handling | PRIVACY_OVERVIEW_AR.md + DATA_HANDLING_OVERVIEW_AR.md | PDPL, GDPR-style |
| 7. Integrations | INTEGRATION_OVERVIEW_AR.md | WhatsApp, Email, CRM, HubSpot, Calendly |
| 8. Implementation plan | IMPLEMENTATION_PLAN_TEMPLATE_AR.md | 30-60-90 |
| 9. Support model | SUPPORT_MODEL_AR.md | tiers, response |
| 10. Commercial model | (→ pricing page + ops) | pricing logic |
| 11. Risk controls | ENTERPRISE_RISK_REGISTER_SUMMARY_AR.md | ما المخاطر وكيف نخفف |
| 12. FAQ | PROCUREMENT_FAQ_AR.md | أسئلة شائعة |
| 13. Legal review triggers | (→ legal) | متى نحتاج محامي |

---

## Enterprise Objection Bank (الفئات)

- **Security:** "هل أنتم SOC2؟" "هل عندكم pen-test؟" "من الـ CISO؟"
- **Privacy:** "هل أنتم PDPL-compliant؟" "أين servers؟" "من processor البيانات؟"
- **Commercial:** "ليش أنتم أغلى من freelancer؟" "ما ROI المضمون؟"
- **Operational:** "ماذا لو سقطتم أنتم؟" "BCP؟" "SLA uptime؟"
- **AI-specific:** "هل AI يحل محل الفريق؟" "ماذا لو hallucinate؟" "prompt injection؟"
- **Localization:** "كم فريقكم سعودي؟" "هل تدعمون عربي فصيح؟" "فاتورة ZATCA؟"

كل اعتراض → counter script في `ENTERPRISE_OBJECTION_BANK_AR.md` + evidence pointer.

---

## Quality Gates (لكل وثيقة)

- ✅ مبنية على حقائق من الـ repo، لا ادعاءات
- ✅ Arabic-first، English عند الطلب
- ✅ لا وعود لا يمكن تسليمها
- ✅ مرجع (path) لكل ادعاء
- ✅ مراجعة المؤسس إلزامية قبل الإصدار

---

## Final Report

`reports/enterprise/ENTERPRISE_READINESS_FINAL_REPORT.md` يحتوي:
- Current level (E0–E5)
- Missing blockers للانتقال للمستوى التالي
- Enterprise sales risks
- Procurement pack files list
- Founder next actions (top 5)
- Recommended next 5 docs

---

> **Cross-ref:** `docs/enterprise/ENTERPRISE_READINESS.md` (يوجد) → هذا الـ OS **يكمّله**، لا يلغيه.
