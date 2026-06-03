# مسار الإغلاق + Commercial Evidence Events

**المرجع:** [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](../DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) · [DEALIX_REVENUE_WAR_ROOM_AR.md](../../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) · التتبع: [evidence_events_tracker.csv](evidence_events_tracker.csv)

---

## مسار الإغلاق (مرحلة 0)

```text
lead_identified
  → message_drafted → approved_to_send → message_sent_manual
  → reply_received
  → discovery_completed (7 أسئلة — قبل ديمو طويل)
  → demo_booked → demo_held
  → scope_requested → scope_signed
  → invoice_sent → payment_received
  → delivery_started → proof_pack_delivered
  → upsell_candidate | referral_requested | closed_lost
```

**Discovery السبعة** (لا تتخطّها): انظر [DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md](../DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md) §7.

---

## أحداث الأدلة (Commercial Evidence Events)

| event_type | معنى | war_room_status المقترح |
|------------|------|-------------------------|
| `message_sent_manual` | إرسال بموافقة | `sent_manual` |
| `reply_received` | رد مسجّل | `replied` |
| `demo_booked` | ديمو محجوز | `meeting_booked` |
| `scope_requested` | طلب نطاق | `scope_requested` |
| `invoice_sent` | فاتورة | `invoice_sent` |
| `payment_received` | دفع | `paid` |
| `proof_pack_delivered` | Proof مسلّم | `proof_pack_delivered` |
| `partner_intro_created` | مقدّمة شريك | — |
| `referral_requested` | طلب إحالة | `referral_requested` |

---

## حقول Sales Room (إلزامية لكل lead)

| حقل | ملاحظة |
|-----|--------|
| company, contact, source | SOAEN: Source |
| owner | SOAEN: Owner |
| motion | A / B / C / D |
| pain_hypothesis, offer_id | تركيز |
| proof_asset_sent | ما أُرسل |
| objections | نص مختصر |
| evidence_events | ربط بـ CSV أو عمود في War Room |
| next_action, next_action_date, stage | SOAEN: Next Action |
| scope_status, invoice_status | تنفيذ |

---

## قواعد اليوم

- **لا lead بلا next_action** وتاريخ.  
- **لا ديمو 30 دقيقة** قبل إكمال Discovery (مسموح 10 دقائق تأهيل فقط).  
- **كل إرسال خارجي** = مسودة + موافقة (انظر [COMMERCIAL_GOVERNANCE_GATES_AR.md](COMMERCIAL_GOVERNANCE_GATES_AR.md)).  
- **هدف اليوم:** حدث أدلة واحد على الأقل في [evidence_events_tracker.csv](evidence_events_tracker.csv).

---

## ربط الدفع والتسليم

| خطوة | مرجع |
|------|------|
| فاتورة يدوية | [MANUAL_PAYMENT_SOP.md](../../ops/MANUAL_PAYMENT_SOP.md) |
| نطاق Diagnostic | [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](FIRST_PAID_DIAGNOSTIC_DOD_AR.md) |
| Proof Pack | [../delivery/PROOF_PACK_TEMPLATE.md](../../delivery/PROOF_PACK_TEMPLATE.md) |
