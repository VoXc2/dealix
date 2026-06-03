# Partner Onboarding Kit — Dealix

**المرحلة:** 3 · **الهدف:** `partner_intro_created` + أول اتفاق إحالة/إعادة بيع.

**مراجع:** [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](../DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) §11 · [dealix_agency_partnerships.md](../../sales-kit/dealix_agency_partnerships.md) · [dealix_referral_program.md](../../sales-kit/dealix_referral_program.md) · [dealix_agency_partnership_playbook.md](../../sales-kit/v5/dealix_agency_partnership_playbook.md)

---

## 1. Partner one-pager (للإرسال بعد الموافقة)

**Dealix في جملة:** نظام سعودي يثبت **ماذا يحدث بعد الـ lead** — مالك، متابعة، موافقة، دليل، خطوة تالية (SOAEN).

**لمن:** وكالات تسويق، منفّذو CRM، استشاريو أتمتة/AI.

**ما نفعله:** Diagnostic/Proof على workflow واحد أو 10 leads — **لا** إرسال بارد باسم الشريك.

**Motion الافتراضي:** A — Agency Wedge.

---

## 2. Co-sell call outline (10 دقائق)

1. من تجيب الاهتمام؟ من يتابع؟  
2. هل تقدرون تثبتون للعميل ماذا حدث بعد الحملة؟  
3. عرض: Audit على **عميل واحد** للوكالة.  
4. CTA: نطاق + تاريخ بدء — [SCOPE_AGENCY_AUDIT_AR.md](motion_a_agency/SCOPE_AGENCY_AUDIT_AR.md).

---

## 3. Demo 10 دقائق

- شاشة: lead بلا owner → فجوة SOAEN.  
- Sample Proof: [sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md](sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md).  
- لا مبالغة AI — ركّز على **قرار موثّق**.

**نص:** [dealix_demo_script_30min.md](../../sales-kit/dealix_demo_script_30min.md) (اختصر لـ 10).

---

## 4. Pricing & routing card (داخلي للشريك)

| ألم العميل | العرض | مؤشر سعر |
|------------|--------|----------|
| leads تضيع | 10-Lead Audit | 499 |
| proof للعميل | Agency Proof Pack | 990 |
| CRM غير مفيد | Data to Revenue Snapshot | 1,500 |
| workflow جاهز | Governed Diagnostic | 4,999–15,000 |

**لا تعرض كل الصفوف للعميل النهائي دفعة واحدة.**

---

## 5. Referral & rev-share (مسودة — مراجعة قانونية)

| نوع | عمولة إرشادية | شرط |
|-----|---------------|------|
| Referral | 10–20% أول دفع | بعد `invoice_paid` |
| Affiliate | 5–10% أول diagnostic | إفصاح + رسائل معتمدة |
| Co-selling | يتفق case-by-case | Pilot واحد أولاً |

**مسودة اتفاق أول شريك:** انسخ من [dealix_pilot_agreement.md](../../sales-kit/dealix_pilot_agreement.md) وعدّل بنود الإحالة.

**قائمة تحقق توقيع:**

- [ ] نطاق عميل واحد للبداية  
- [ ] لا spam / لا واتساب بارد  
- [ ] لا ادعاءات إيراد مضمونة  
- [ ] صرف عمولة بعد دفع مثبت فقط  

---

## 6. Delivery boundary

| Dealix | الشريك |
|--------|--------|
| Diagnostic, Proof Pack, تقارير SOAEN | علاقة العميل، حملات، تنفيذ CRM |
| مسودات متابعة | إرسال خارجي (بموافقة العميل) |
| توصية توسع | تنفيذ تقني إضافي (إن وُجد) |

---

## 7. Proof expectations

- SLA ~7 أيام من بيانات كاملة.  
- [PROOF_PACK_AGENCY_AR.md](motion_a_agency/PROOF_PACK_AGENCY_AR.md).  
- مراجعة مؤسس قبل التسليم.

---

## 8. Support path

- قناة: بريد مؤسس / Slack داخلي (حسب الإعداد).  
- استجابة هدف: 24h عمل لأسئلة ما قبل الصفقة.  
- تصعيد تسليم: dealix-delivery playbook.

---

## 9. Objection cheat sheet (شريك)

| اعتراض | رد مختصر | أصل |
|--------|----------|-----|
| عندنا CRM | CRM يخزن؛ من يحرّك follow-up؟ | [objection_engine_registry.yaml](objection_engine_registry.yaml) `crm_exists` |
| السعر | نبدأ 10 leads فقط | `price_high` |
| عندنا AI | حوكمة قبل التوسع | `internal_ai` |

---

## 10. تفعيل أول شريك (checklist)

- [ ] `partner_intro_created` في [evidence_events_tracker.csv](evidence_events_tracker.csv)  
- [ ] صف في War Room §10 (Affiliate & Partner Ops)  
- [ ] one-pager مُرسل بعد موافقة  
- [ ] أول عميل end واحد scoped  
- [ ] مراجعة أسبوعية: leads_submitted → paid_deals  
