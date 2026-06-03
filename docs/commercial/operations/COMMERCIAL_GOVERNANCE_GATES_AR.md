# Commercial Governance Gates — قنوات، DPA، إطلاق

**المرحلة:** حوكمة مستمرة — **قبل كل إرسال خارجي أو عقد عميل.**

---

## 1. قواعد القنوات (غير قابلة للتفاوض)

| قناة | مسموح | ممنوع |
|------|--------|--------|
| LinkedIn | منشور مؤسس، تعليق، DM **بعد** قبول اتصال، يدوي | أتمتة إرسال، scraping، رسائل جماعية |
| Email | تخصيص، CTA واحد، علاقة/بريد علني | إلحاح مزيف، ROI مضمون |
| WhatsApp | inbound، علاقة قائمة، إحالة دافئة موثقة | **بارد**، spam، أتمتة صادرة |
| Partners | رسائل معتمدة، إفصاح | ادعاءات مضللة، spam باسم Dealix |

**مرجع تفصيلي:** [DEALIX_REVENUE_WAR_ROOM_AR.md](../../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) §3 · [.cursor/rules/dealix-v3.mdc](../../../.cursor/rules/dealix-v3.mdc)

---

## 2. بوابة قبل كل رسالة خارجية

- [ ] مسودة مكتوبة  
- [ ] موافقة صريحة (مؤسس)  
- [ ] CTA واحد  
- [ ] لا وعد إيراد مضمون  
- [ ] تسجيل `message_sent_manual` في [evidence_events_tracker.csv](evidence_events_tracker.csv)

---

## 3. بوابة قبل مشاركة بيانات عميل

- [ ] حق معالجة أو موافقة كتابية  
- [ ] مراجعة [DPA_CHECKLIST_AR_EN.md](../../wave8/DPA_CHECKLIST_AR_EN.md) إن وُجد معالج خارجي  
- [ ] لا بيانات في prompts عامة غير محكومة  

---

## 4. بوابة قبل الإطلاق العام / ادعاء «جاهزية كاملة»

- [ ] [LAUNCH_GATES.md](../../LAUNCH_GATES.md)  
- [ ] [LAUNCH_READINESS_REPORT.md](../../LAUNCH_READINESS_REPORT.md)  
- [ ] لا «Revenue Live» قبل `payment_received`  

---

## 5. بوابة قبل البيع التقني

- [ ] [FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md](../../ops/FOUNDER_INTEGRATION_TRUTH_MATRIX_AR.md) — لا بيع تكامل **red**  
- [ ] KPI من `kpi_founder_commercial_import.yaml` فقط — لا أرقام مخترعة  

---

## 6. بوابة قبل upsell

- [ ] `proof_pack_delivered` مسجّل  
- [ ] [EXPANSION_UPSELL_AR.md](motion_a_agency/EXPANSION_UPSELL_AR.md)  

---

## 7. Trust كـ selling point (للموقع والعروض)

- No cold WhatsApp  
- No scraping  
- No fake proof  
- No guaranteed revenue claims  
- Human approval for external actions  

---

## 8. مراجعة أسبوعية (5 دقائق)

| سؤال | مرجع |
|------|------|
| أي قناة فيها waste؟ | [COMMERCIAL_WEEKLY_SCORECARD_AR.md](COMMERCIAL_WEEKLY_SCORECARD_AR.md) |
| أي انتهاك محتمل؟ | هذا الملف §1–2 |
| هل نحتاج DPA جديد؟ | §3 |

---

*مرتبط بـ [DEALIX_MASTER_OPERATING_MODEL_AR.md](../../strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md) وكتالوج Revenue OS في AGENTS.md.*
