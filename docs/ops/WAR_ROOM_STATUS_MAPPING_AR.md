# War Room Status ↔ LeadStage — جدول التحويل

**المرجع التشغيلي:** [DEALIX_REVENUE_WAR_ROOM_AR.md](DEALIX_REVENUE_WAR_ROOM_AR.md) · **الكود:** [dealix/revenue_ops_autopilot/war_room_mapping.py](../../dealix/revenue_ops_autopilot/war_room_mapping.py)

## لماذا حقلان؟

| الحقل | الغرض |
|--------|--------|
| `war_room_status` | مسار الإرسال اليدوي والموافقة (7 أعمدة في الواجهة) |
| `stage` (`LeadStage`) | مسار CRM الداخلي والسياسات القديمة (`advance-stage`) |

## حالات War Room (outreach)

`not_contacted` → `message_drafted` → `approved_to_send` → `sent_manual` → `replied` → `proof_pack_sent` → `meeting_booked` → `scope_requested` → `invoice_sent` → `paid` → `delivery_started` → `proof_pack_delivered` → `upsell_candidate` | `referral_requested` | `closed_lost`

## ترحيل LeadStage → war_room_status (سجلات قديمة)

| LeadStage | war_room_status الافتراضي |
|-----------|---------------------------|
| new_lead, nurture | not_contacted |
| qualified_A/B, partner_candidate | message_drafted |
| meeting_booked, meeting_done | meeting_booked |
| scope_requested, scope_sent | scope_requested |
| invoice_sent | invoice_sent |
| invoice_paid | paid |
| delivery_started | delivery_started |
| proof_pack_sent | proof_pack_delivered |
| sprint_candidate, retainer_candidate | upsell_candidate |
| closed_lost | closed_lost |

## مزامنة عند تحديث War Room

عند `PATCH /api/v1/ops-autopilot/war-room/{id}` يُحدَّث `war_room_status` ويُزامَن `stage` من `WAR_ROOM_TO_STAGE` ما لم يُمرَّر `sync_stage=false`.

## أحداث الأدلة

| انتقال | event_type مقترح |
|--------|------------------|
| → approved_to_send | war_room_approved_to_send |
| → sent_manual | war_room_sent_manual |
| → meeting_booked | war_room_meeting_booked |
| → paid | war_room_payment_logged |
| → proof_pack_delivered | war_room_proof_delivered |

انظر أيضاً [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](../commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md).
