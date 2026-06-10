# DoD — أول Diagnostic / Audit مدفوع + Proof Pack

**المرحلة:** 1 من [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../MASTER_COMMERCIAL_OPERATING_PLAN_AR.md)

---

## Definition of Done (كل البنود إلزامية)

### قبل الدفع

- [ ] Discovery السبعة مكتملة ومُسجّلة في Sales Room  
- [ ] Motion محدد (A/B/C/D) وعرض واحد فقط (لا قائمة 8 باقات)  
- [ ] نطاق موقّع أو التزام مكتوب (بريد/واتساب opt-in) يحدد: workflow واحد، 10 leads أو عميل وكالة واحد، مدة ~7 أيام  
- [ ] SOAEN: Source + Owner + Approval على أي بيانات عميل  
- [ ] `invoice_sent` مسجّل في [evidence_events_tracker.csv](evidence_events_tracker.csv)  
- [ ] لا وعود إيراد مضمون · لا تكامل **red** في Truth Matrix  

### عند الدفع

- [ ] `payment_received` مسجّل (مبلغ، تاريخ، مرجع دفع)  
- [ ] لا upsell قبل بدء التسليم  

### التسليم (خلال SLA المتفق — افتراض 7 أيام عمل)

- [ ] `delivery_started`  
- [ ] Proof Pack يتبع [PROOF_PACK_TEMPLATE.md](../../delivery/PROOF_PACK_TEMPLATE.md) (10 أقسام)  
- [ ] كل finding له مصدر أو `مفقود` صريح  
- [ ] Top 3 قرارات محكومة + توصية Sprint/Retainer أو «توقف عند التشخيص»  
- [ ] مراجعة بشرية (مؤسس) قبل الإرساء النهائي للعميل  
- [ ] `proof_pack_delivered` + تاريخ تسليم  

### بعد التسليم

- [ ] اجتماع ختام 30–45 دقيقة (أو async موافق عليه)  
- [ ] `upsell_candidate` أو `closed_lost` مع سبب  
- [ ] تحديث [COMMERCIAL_WEEKLY_SCORECARD_AR.md](COMMERCIAL_WEEKLY_SCORECARD_AR.md) — Proof مسلّم +1  

---

## عروض الدخول (routing)

| Motion | عرض دخول نموذجي | مرجع سعر |
|--------|-----------------|----------|
| A Agency | 10-Lead Audit / Agency Proof Pack | [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](../DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) §3 |
| B Direct | Risk Score → Audit → Diagnostic | [DEALIX_REVOPS_PACKAGES_AR.md](../DEALIX_REVOPS_PACKAGES_AR.md) |
| C Consultant | Diagnostic layer | نفس المرجع |
| D Executive | AI & RevOps Diagnostic | لغة Control Tower — لا «10 leads» للكبار |

**سلّم المؤسس:** Diagnostic 4,999–15,000 SAR → Sprint/Data Pack بعد قبول → Growth 2,999 فقط بعد Proof.

---

## ممنوعات (مراجعة قبل الإغلاق)

- لا أرقام CRM مخترعة في التقرير  
- لا cold WhatsApp / LinkedIn آلي  
- لا ادعاء «Revenue Live» قبل `payment_received`  
- لا Proof مزيّف أو KPI بدون مصدر  

---

## قائمة تحقق سريعة (نسخ لكل صفقة)

```text
[ ] discovery_7_done
[ ] scope_signed
[ ] invoice_sent → payment_received
[ ] proof_pack_10_sections
[ ] proof_pack_delivered
[ ] weekly_scorecard_updated
```
