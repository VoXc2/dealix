# Dealix — Business KPI Dashboard Spec
<!-- PHASE 13 | Owner: Founder | Date: 2026-05-07 -->
<!-- All metrics: manual tracking until automated dashboard built -->

---

## 1. مقاييس المبيعات (Sales Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `demos_conducted` | عدد عروض Demo حقيقية أُجريت | أسبوعي | تتبع يدوي |
| `demos_to_pilots` | نسبة Demo → Pilot مكتمل | أسبوعي | demos / pilots |
| `pilots_completed` | عدد Sprints 7 أيام مكتملة | أسبوعي | تتبع يدوي |
| `pilots_to_managed` | نسبة Pilot → Managed Ops | شهري | pilots / managed |
| `avg_deal_cycle_days` | متوسط أيام warm intro → دفع | شهري | تواريخ التتبع |
| `qualified_leads` | leads مرت بـ Qualification Checklist | أسبوعي | Sales Playbook |
| `conversion_rate` | qualified_leads → pilots | شهري | حساب مشتق |

---

## 2. مقاييس الإيرادات (Revenue Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `mrr` | Monthly Recurring Revenue (Managed Ops فقط) | شهري | Billing records |
| `arr` | MRR × 12 | شهري | مشتق |
| `one_time_revenue` | مجموع Sprint + Data Pack (non-recurring) | شهري | Billing |
| `total_revenue` | MRR + one_time_revenue | شهري | مجموع |
| `avg_revenue_per_client` | total_revenue / active_clients | شهري | مشتق |
| `revenue_per_offer` | إيراد مقسوم على نوع الخدمة | شهري | Billing تفصيلي |
| `payments_received` | عدد دفعات مؤكدة (لا draft invoices) | فوري | Bank/Moyasar |

---

## 3. مقاييس الإثبات (Proof Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `proof_events_total` | عدد proof events موثقة (L1+) | أسبوعي | proof_ledger |
| `proof_events_l4_plus` | proof events بمستوى L4+ | شهري | proof_ledger |
| `case_studies_ready` | case studies جاهزة للنشر (موافقة L3+) | شهري | proof_ledger |
| `testimonials_collected` | شهادات مكتوبة من عملاء | شهري | proof_ledger |
| `drafts_approved_rate` | نسبة مسودات وافق عليها العميل | per Sprint | Sprint records |
| `avg_sprint_proof_events` | متوسط proof events لكل Sprint | شهري | مشتق |

---

## 4. مقاييس MRR والـ Churn

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `mrr_new` | MRR جديد هذا الشهر | شهري | Billing |
| `mrr_churned` | MRR ضاع بسبب إلغاء | شهري | Billing |
| `mrr_expansion` | MRR من upsell لعملاء قائمين | شهري | Billing |
| `net_mrr_growth` | mrr_new + expansion - churned | شهري | مشتق |
| `churn_rate` | (clients_churned / clients_start) × 100 | شهري | تتبع يدوي |
| `retention_rate` | 100 - churn_rate | شهري | مشتق |
| `ltv_estimate` | avg_revenue × avg_months | ربعي | مشتق |

---

## 5. مقاييس الهامش (Margin Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `gross_margin_sprint` | (499 - تكاليف مباشرة) / 499 | per Sprint | cost tracking |
| `gross_margin_managed` | (MRR - تكاليف مباشرة) / MRR | شهري | cost tracking |
| `llm_cost_total` | إجمالي تكاليف OpenAI API | شهري | API dashboard |
| `infra_cost_total` | Railway + Supabase + غيرها | شهري | invoices |
| `founder_hours_sprint` | ساعات المؤسس لكل Sprint | per Sprint | time tracking |
| `cost_per_client` | (LLM + infra + founder_time) / clients | شهري | مشتق |

---

## 6. مقاييس رضا العملاء (Satisfaction Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `client_satisfaction_score` | متوسط تقييم العملاء (1–5) | per Sprint | استبيان Day 7 |
| `nps_score` | Net Promoter Score | ربعي | استبيان ربعي |
| `sprint_completion_rate` | نسبة Sprints أُكملت بدون شكاوى | شهري | records |
| `support_tickets` | عدد طلبات دعم مستلمة | أسبوعي | تتبع يدوي |
| `avg_response_time` | متوسط وقت رد الدعم | أسبوعي | تتبع يدوي |

---

## 7. مقاييس الإحالات (Referral Metrics)

| المقياس | التعريف | التردد | المصدر |
|---------|---------|--------|--------|
| `referrals_received` | عملاء جاؤوا عبر إحالة | شهري | السؤال في Kick-off |
| `referral_conversion_rate` | إحالات → pilots | شهري | مشتق |
| `partner_leads` | leads من Agency Partners | شهري | partner channel |
| `organic_leads` | leads من محتوى LinkedIn / موقع | شهري | تتبع يدوي |

---

## 8. ملخص Dashboard — السطر الواحد

### تقرير يومي للمؤسس (Daily Pulse)
```
📊 Dealix Daily — [التاريخ]
Active clients: X | MRR: X SAR | Demos this week: X
Proof events (this month): X | Avg satisfaction: X.X/5
[⚠️ تنبيه: إذا كان churn_rate > 20% أو satisfaction < 3.5]
```

### تقرير أسبوعي
```
Week [رقم] Summary:
✓ Sprints completed: X
✓ Proofs documented: X
✓ Revenue collected: X SAR
→ Priority this week: [الأولوية]
```

---

## 9. محفزات الإجراء (Action Triggers)

> **المبدأ:** كل مقياس يجب أن يربط بإجراء محدد عند تجاوز عتبة ما. بدون محفز = رقم بلا قيمة.

| المقياس | العتبة الحمراء | الإجراء الفوري | العتبة الخضراء |
|---------|---------------|----------------|----------------|
| `churn_rate` | > 20%/شهر | مراجعة Churn Reasons + تواصل مباشر مع العملاء خلال 24 ساعة | < 10%/شهر |
| `client_satisfaction_score` | < 3.5 / 5 | Escalation للمؤسس + مكالمة إنقاذ خلال 24 ساعة | ≥ 4.0 / 5 |
| `drafts_approved_rate` | < 60% | مراجعة جودة المسودات + طلب ملاحظات العميل المفصلة | ≥ 80% |
| `gross_margin_sprint` | < 80% | مراجعة وقت التسليم + رفع السعر لـ 699 SAR أو تقليل النطاق | ≥ 85% |
| `gross_margin_managed` | < 65% | رفع السعر لـ 3,999 SAR أو توظيف مساعد تسليم | ≥ 70% |
| `avg_response_time` (دعم) | > 4 ساعات (عاجل) | تنبيه المؤسس فوري + اعتذار للعميل | < 2 ساعة |
| `proof_events_total` | 0 بعد Sprint مكتمل | إعادة مراجعة SOP + يوم 7 من السبرينت إلزامي | ≥ 3/Sprint |
| `mrr_churned` | > 30% من MRR | توقف عن بيع جديد + تحليل Churn كامل أولاً | 0 |
| `conversion_rate` | < 20% (qualified → pilot) | مراجعة Sales Playbook + demo script | > 40% |
| `nps_score` | < 30 | مراجعة شاملة لعملية التسليم + Customer Success | ≥ 50 |

---

## 10. أدوات التتبع المقترحة (قبل Dashboard مؤتمت)

| الأداة | ما تتبعه | الوضع |
|--------|---------|-------|
| Google Sheet / Notion | كل المقاييس يدوياً | متاح الآن |
| Billing records | payments, MRR, churn | يدوي |
| `/proof_ledger` في الكود | proof events | موجود |
| Calendar tracking | founder hours | يدوي |
| Railway logs | infra costs | تلقائي |
| OpenAI dashboard | LLM costs | تلقائي |

---

*Version 1.0 | Manual tracking until automated KPI dashboard is built*
