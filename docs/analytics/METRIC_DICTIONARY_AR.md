# Dealix Metric Dictionary — Arabic
## قاموس مؤشرات ديلوكس

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. GTM Metrics — مؤشرات GTM

### 1.1 Prospect Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| gtm_prospects_researched | العملاء المحتملين الذين تم بحثهم | Prospects Researched | Number of prospects researched | COUNT(DISTINCT company_id) WHERE event = company.scored | count | daily |
| gtm_prospects_qualified | العملاء المؤهلون | Prospects Qualified | Prospects meeting ICP criteria | COUNT(DISTINCT company_id) WHERE event = lead.qualified AND tier IN (A, B) | count | daily |
| gtm_signals_detected | الإشارات المكتشفة | Signals Detected | Market signals identified | COUNT(event_id) WHERE event = signal.detected | count | daily |
| gtm_qualification_rate | معدل التأهيل | Qualification Rate | % of researched that qualified | gtm_prospects_qualified / gtm_prospects_researched * 100 | % | weekly |

### 1.2 Draft Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| gtm_drafts_generated | المسودات الناتجة | Drafts Generated | Drafts created by AI | COUNT(event_id) WHERE event = message.drafted | count | daily |
| gtm_drafts_passed_quality | المسودات التي اجتازت QA | Drafts QA Passed | Drafts passing quality check | COUNT(event_id) WHERE event = ai.eval_run AND result = pass | count | daily |
| gtm_drafts_approved | المسودات المعتمدة | Drafts Approved | Founder-approved drafts | COUNT(event_id) WHERE event = message.approved | count | daily |
| gtm_draft_quality_rate | معدل جودة المسودات | Draft Quality Rate | % of drafts passing QA | gtm_drafts_passed_quality / gtm_drafts_generated * 100 | % | weekly |
| gtm_approval_rate | معدل الاعتماد | Approval Rate | % of drafts approved by Founder | gtm_drafts_approved / gtm_drafts_passed_quality * 100 | % | weekly |
| gtm_approval_delay_hours | تأخير الاعتماد | Approval Delay | Avg hours to approve | AVG(approved_at - drafted_at) | hours | weekly |

### 1.3 Outreach Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| gtm_emails_sent | الإيميلات المرسلة | Emails Sent | Emails delivered | COUNT(event_id) WHERE event = message.sent AND channel = email | count | daily |
| gtm_replies_received | الردود المستلمة | Replies Received | All reply types | COUNT(event_id) WHERE event = reply.received | count | daily |
| gtm_positive_replies | الردود الإيجابية | Positive Replies | Positive sentiment | COUNT(event_id) WHERE event = reply.classified AND sentiment = positive | count | daily |
| gtm_reply_rate | معدل الرد | Reply Rate | % of emails receiving reply | gtm_replies_received / gtm_emails_sent * 100 | % | weekly |
| gtm_positive_rate | معدل الإيجابية | Positive Rate | % of replies that are positive | gtm_positive_replies / gtm_replies_received * 100 | % | weekly |

### 1.4 Meeting Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| gtm_meetings_booked | الاجتماعات المحجوزة | Meetings Booked | Discovery meetings scheduled | COUNT(event_id) WHERE event = meeting.booked | count | daily |
| gtm_meetings_held | الاجتماعات المعقودة | Meetings Held | Meetings that occurred | COUNT(event_id) WHERE event = meeting.held | count | daily |
| gtm_meetings_no_show | عدم الحضور | No Shows | Meetings missed | COUNT(event_id) WHERE event = meeting.no_show | count | weekly |
| gtm_meeting_show_rate | معدل الحضور | Show Rate | % of booked meetings held | gtm_meetings_held / gtm_meetings_booked * 100 | % | weekly |
| gtm_meeting_to_close_rate | معدل الاجتماع للإغلاق | Meeting-to-Close Rate | Meetings per won deal | gtm_meetings_held / gtm_won_deals | ratio | monthly |

### 1.5 Deal Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| gtm_proposals_requested | طلبات الاقتراح | Proposals Requested | Proposals requested | COUNT(event_id) WHERE event = deal.proposal_sent | count | weekly |
| gtm_won_deals | الصفقات الرابحة | Won Deals | Deals closed won | COUNT(event_id) WHERE event = deal.won | count | monthly |
| gtm_lost_deals | الصفقات الخاسرة | Lost Deals | Deals closed lost | COUNT(event_id) WHERE event = deal.lost | count | monthly |
| gtm_win_rate | معدل الفوز | Win Rate | % of opportunities won | gtm_won_deals / (gtm_won_deals + gtm_lost_deals) * 100 | % | monthly |

---

## 2. Deliverability Metrics — مؤشرات قابلية التوصيل

### 2.1 Volume Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| del_send_volume_daily | حجم الإرسال اليومي | Daily Send Volume | Emails sent today | COUNT(event_id) WHERE event = message.sent AND date = today | count | daily |
| del_send_volume_weekly | حجم الإرسال الأسبوعي | Weekly Send Volume | Emails sent this week | COUNT(event_id) WHERE event = message.sent AND week = this_week | count | weekly |
| del_suppressed_count | عدد المحظورين | Suppressed Count | Total suppressed contacts | COUNT(DISTINCT contact_id) WHERE status = suppressed | count | daily |

### 2.2 Quality Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit | Frequency |
|-----------|-----------|-----------|------------|---------|------|-----------|
| del_bounce_rate | معدل الارتداد | Bounce Rate | % of emails bounced | del_bounces / del_send_volume * 100 | % | daily |
| del_hard_bounce_rate | معدل الارتداد الصعب | Hard Bounce Rate | % of hard bounces | del_hard_bounces / del_send_volume * 100 | % | daily |
| del_soft_bounce_rate | معدل الارتداد الطفيف | Soft Bounce Rate | % of soft bounces | del_soft_bounces / del_send_volume * 100 | % | daily |
| del_unsubscribe_rate | معدل إلغاء الاشتراك | Unsubscribe Rate | % unsubscribed | del_unsubscribes / del_send_volume * 100 | % | weekly |
| del_spam_warning_count | تحذيرات Spam | Spam Warnings | Spam complaints this week | COUNT(event_id) WHERE event = compliance.blocked AND reason = spam | count | weekly |
| del_domain_health_score | درجة صحة المجال | Domain Health Score | Domain reputation (0-100) | Calculated from bounce/complaint rates | score | daily |

---

## 3. Reply Classification Metrics — مؤشرات تصنيف الردود

### 3.1 Reply Type Counts

| Metric ID | Reply Type | الوصف |
|-----------|------------|-------|
| reply_positive_count | Positive | اهتمام فوري بالمنتج |
| reply_interested_later_count | Interested Later | مهتم لكن التوقيت غير مناسب |
| reply_price_question_count | Price Question | سؤال عن السعر أو التكلفة |
| reply_send_more_info_count | Send More Info | يريد معلومات إضافية |
| reply_wrong_person_count | Wrong Person | شخص خاطئ أو جهة غير مناسبة |
| reply_unsubscribe_count | Unsubscribe | طلب إلغاء الاشتراك |
| reply_angry_count | Angry | رد سلبي أو غاضب |
| reply_bounce_count | Bounce | بريد مرتد |

### 3.2 Reply Distribution Metrics

| Metric ID | Name | Formula |
|-----------|------|---------|
| reply_positive_pct | % Positive | reply_positive_count / total_replies * 100 |
| reply_interested_later_pct | % Interested Later | reply_interested_later_count / total_replies * 100 |
| reply_price_question_pct | % Price Question | reply_price_question_count / total_replies * 100 |
| reply_negative_pct | % Negative | (reply_angry_count + reply_unsubscribe_count) / total_replies * 100 |

---

## 4. WhatsApp Metrics — مؤشرات WhatsApp

### 4.1 Session Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Unit | Frequency |
|-----------|-----------|-----------|------------|------|-----------|
| wa_post_reply_sessions | جلسات ما بعد الرد | Post-Reply Sessions | Active WhatsApp sessions after reply | count | daily |
| wa_sessions_started | الجلسات_started | Sessions Started | Sessions initiated | count | daily |
| wa_sessions_completed | الجلسات المكتملة | Sessions Completed | Sessions completed successfully | count | daily |
| wa_session_completion_rate | معدل إكمال الجلسة | Session Completion Rate | % sessions completed | % | weekly |

### 4.2 Action Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Unit | Frequency |
|-----------|-----------|-----------|------------|------|-----------|
| wa_readiness_scans_started | scans البدء | Readiness Scans Started | Scans initiated | count | daily |
| wa_readiness_scans_completed | scans الاكتمال | Readiness Scans Completed | Scans completed | count | daily |
| wa_action_cards_clicked | نقرات بطاقات الإجراءات | Action Cards Clicked | CTA interactions | count | daily |
| wa_proposal_cards_viewed | مشاهدات بطاقات الاقتراح | Proposal Cards Viewed | Proposal views | count | daily |
| wa_payment_handoffs_requested | طلبات الدفع | Payment Handoffs Requested | Payment requests | count | weekly |
| wa_human_handoffs | التحويل للإنسان | Human Handoffs | Handoffs to human agent | count | weekly |

---

## 5. Commercial Metrics — المؤشرات التجارية

### 5.1 Pipeline Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula | Unit |
|-----------|-----------|-----------|------------|---------|------|
| com_pipeline_value | قيمة خط الأنابيب | Pipeline Value | Total value of active pipeline | SUM(value_sar) WHERE stage NOT IN (won, lost) | SAR |
| com_qualified_opportunities | الفرص المؤهلة | Qualified Opportunities | Deals at qualified+ stages | COUNT(opp_id) WHERE stage >= qualified | count |
| com_proposal_stage_value | قيمة مرحلة الاقتراح | Proposal Stage Value | Value at proposal stage | SUM(value_sar) WHERE stage = proposal_sent | SAR |
| com_negotiation_stage_value | قيمة مرحلة المفاوضة | Negotiation Stage Value | Value at negotiation stage | SUM(value_sar) WHERE stage = negotiation | SAR |

### 5.2 Rate Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula |
|-----------|-----------|-----------|------------|---------|
| com_proposal_rate | معدل الاقتراح | Proposal Rate | Proposals per qualified opp | com_proposals_sent / com_qualified_opportunities |
| com_close_rate | معدل الإغلاق | Close Rate | Won per qualified opp | gtm_won_deals / com_qualified_opportunities |
| com_average_deal_size | متوسط حجم الصفقة | Average Deal Size | Mean value of won deals | AVG(value_sar) WHERE stage = won |
| com_deal_median_size | median حجم الصفقة | Median Deal Size | Median value of won deals | MEDIAN(value_sar) WHERE stage = won |
| com_discount_rate | معدل الخصم | Discount Rate | Avg discount % | AVG(discount_pct) WHERE discount_applied = true |
| com_price_exception_count | استثناءات السعر | Price Exceptions | Special pricing requests | COUNT(opp_id) WHERE price_exception = true |

### 5.3 Velocity Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| com_avg_days_to_close | متوسط الأيام للإغلاق | AVG(closed_at - created_at) WHERE stage = won |
| com_avg_days_to_proposal | متوسط الأيام للاقتراح | AVG(proposal_sent_at - created_at) WHERE proposal_sent = true |
| com_sales_cycle_length | طول دورة البيع | COM avg_days_to_close by quarter |

---

## 6. Delivery Metrics — مؤشرات التسليم

### 6.1 Client Status Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| del_active_clients | العملاء النشطون | COUNT(client_id) WHERE status = active_delivery |
| del_onboarding_in_progress | Onboarding قيد التنفيذ | COUNT(client_id) WHERE status = onboarding |
| del_onboarding_complete | إكمال Onboarding | COUNT(client_id) WHERE onboarding_completed = true AND created_at >= 90_days_ago |
| del_clients_at_risk | عملاء في خطر | COUNT(client_id) WHERE health_score < 50 |

### 6.2 Task Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| del_delivery_tasks_total | إجمالي مهام التسليم | COUNT(task_id) WHERE type = delivery |
| del_delivery_tasks_completed | مهام التسليم المكتملة | COUNT(task_id) WHERE type = delivery AND status = completed |
| del_delivery_task_completion_rate | معدل إكمال المهام | del_delivery_tasks_completed / del_delivery_tasks_total |
| del_blockers_open | العوائق المفتوحة | COUNT(blocker_id) WHERE status = open |
| del_blockers_critical | العوائق الحرجة | COUNT(blocker_id) WHERE status = open AND severity = critical |

### 6.3 Reporting Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| del_weekly_reports_due | التقارير الأسبوعية المستحقة | COUNT(client_id) WHERE next_qbr_date = today |
| del_weekly_reports_sent | التقارير المرسلة | COUNT(report_id) WHERE type = weekly AND sent_at >= 7_days_ago |
| del_acceptance_checkpoints | نقاط القبول | COUNT(checkpoint_id) WHERE type = acceptance AND status = hit |

---

## 7. Customer Success Metrics — مؤشرات نجاح العميل

### 7.1 Health Metrics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula |
|-----------|-----------|-----------|------------|---------|
| cs_client_health_score | درجة صحة العميل | Client Health Score | Composite health (0-100) | Weighted: engagement (40%) + delivery (30%) + satisfaction (30%) |
| cs_avg_health_score | متوسط درجة الصحة | Average Health Score | Mean health across all clients | AVG(client_health_score) |
| cs_health_distribution | توزيع الصحة | Health Distribution | Count by health band | COUNT(client_id) GROUP BY health_band |

### 7.2 Retention Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| cs_renewal_candidates | مرشحو التجديد | COUNT(client_id) WHERE renewal_due_date <= 90_days |
| cs_churn_risk_count | مخاطر المغادرة | COUNT(client_id) WHERE churn_probability > 0.7 |
| cs_expansion_opportunities | فرص التوسع | COUNT(client_id) WHERE expansion_signals > 2 |
| cs_client_escalations | التصعيدات | COUNT(escalation_id) WHERE created_at >= 30_days_ago |

### 7.3 Satisfaction Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| cs_nps_score | درجة NPS | Net Promoter Score (-100 to 100) |
| cs_satisfaction_avg | متوسط الرضا | AVG(satisfaction_score) WHERE score_available = true |
| cs_nps_response_rate | معدل استجابة NPS | NPS responses / NPS surveys sent |

---

## 8. Finance Metrics — المؤشرات المالية

### 8.1 Unit Economics

| Metric ID | Name (AR) | Name (EN) | Definition | Formula |
|-----------|-----------|-----------|------------|---------|
| fin_cost_per_draft | التكلفة لكل مسودة | Cost Per Draft | AI cost per generated draft | total_ai_cost / gtm_drafts_generated |
| fin_cost_per_reply | التكلفة لكل رد | Cost Per Reply | AI cost per reply received | total_ai_cost / gtm_replies_received |
| fin_cost_per_meeting | التكلفة لكل اجتماع | Cost Per Meeting | Cost per meeting booked | total_ai_cost / gtm_meetings_booked |
| fin_cost_per_proposal | التكلفة لكل اقتراح | Cost Per Proposal | Cost per proposal sent | total_ai_cost / gtm_proposals_requested |
| fin_cac | تكلفة اكتساب العميل | Customer Acquisition Cost | Cost to acquire one customer | total_sales_cost / gtm_won_deals |
| fin_payback_period | فترة الاسترداد | Payback Period | Months to recover CAC | fin_cac / (avg_monthly_revenue_per_customer) |

### 8.2 Margin Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| fin_gross_margin_pct | هامش الربح الإجمالي | (revenue - cost_of_goods) / revenue * 100 |
| fin_gross_margin_by_offer | الهامش حسب العرض | gross_margin_pct GROUP BY offer_id |
| fin_tool_cost_monthly | التكلفة الشهرية للأدوات | SUM(tool_subscriptions) |
| fin_founder_time_cost | تكلفة وقت Founder | founder_hours * hourly_rate |

---

## 9. Agent Productivity Metrics — مؤشرات إنتاجية الوكلاء

### 9.1 Activity Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| agent_tasks_completed | المهام المكتملة | COUNT(task_id) WHERE status = completed |
| agent_tasks_in_progress | المهام قيد التنفيذ | COUNT(task_id) WHERE status = in_progress |
| agent_tasks_failed | المهام الفاشلة | COUNT(task_id) WHERE status = failed |
| agent_files_changed | الملفات المعدلة | COUNT(file_id) WHERE actor_type = agent |
| agent_tests_run | الاختبارات | COUNT(test_id) WHERE run_at >= 24_hours_ago |
| agent_tests_passed | الاختبارات الناجحة | COUNT(test_id) WHERE run_at >= 24_hours_ago AND result = pass |

### 9.2 Quality Metrics

| Metric ID | Name (AR) | Definition |
|-----------|-----------|------------|
| agent_safety_gate_failures | فشل Safety Gate | COUNT(event_id) WHERE event = agent.action_rejected AND reason = safety_gate |
| agent_rework_count | إعادة العمل | COUNT(draft_id) WHERE rework_reason IS NOT NULL |
| agent_collision_count | التعارضات | COUNT(collision_id) WHERE detected = true |
| agent_success_rate | معدل النجاح | agent_tasks_completed / (agent_tasks_completed + agent_tasks_failed) |
| agent_quality_score | درجة الجودة | Weighted: safety (50%) + efficiency (30%) + accuracy (20%) |

---

## 10. Metric Naming Convention

### 10.1 Format
```
{domain}_{metric_name}
```

### 10.2 Domains
| Domain | الوصف |
|--------|-------|
| gtm | Go-To-Market |
| del | Deliverability |
| wa | WhatsApp |
| com | Commercial |
| del | Delivery |
| cs | Customer Success |
| fin | Finance |
| agent | Agent Productivity |

### 10.3 Units
| Unit | Suffix | Example |
|------|--------|---------|
| count | _count | prospects_researched_count |
| rate | _rate | bounce_rate |
| percentage | _pct | positive_pct |
| score | _score | health_score |
| value | _value | pipeline_value |
| days | _days | avg_days_to_close |
| hours | _hours | approval_delay_hours |

---

**Next:** See `EVENT_TAXONOMY_AR.md` for extended event definitions.
