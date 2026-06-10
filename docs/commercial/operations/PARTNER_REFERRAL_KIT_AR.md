# Partner Referral Kit — Motion A

**الهدف:** 2 محادثات شريك · 1 intro مدفوعة خلال 90 يوم  
**Ref:** [PARTNER_ONBOARDING_KIT_AR.md](PARTNER_ONBOARDING_KIT_AR.md)

---

## من ن partnering مع

- وكالات تسويق (5–50 FTE) · consultancies · HubSpot partners  
- **ليس:** منافس CRM · cold lead sellers

---

## Co-sell pitch (AR)

> «أنتم تجيبون الاهتمام. Dealix يثبت ماذا حدث بعد الاهتمام — Proof Pack لعميلكم خلال 7 أيام، بموافقة وPDPL.»

---

## Referral economics (draft)

| Event | Partner | Dealix |
|-------|---------|--------|
| Intro → Diagnostic paid | 10% first invoice | delivery |
| Diagnostic → Sprint | 5% Sprint | delivery |
| Retainer | negotiate case-by-case | after 3 proofs |

**Rule:** لا commission قبل `payment_received`.

---

## Intro email template

```text
Subject: مقدمة — {{agency}} × Dealix (post-campaign proof)

{{partner_name}} يقدّم {{contact}} من {{company}}.
الحاجة: إثبات post-campaign لعميل end واحد.
الخطوة: Diagnostic 7 أيام — {{calendly_or_reply}}.
Trust Pack attached on request.
```

---

## Tracking

- `partner_intro_created` في [evidence_events_tracker.csv](evidence_events_tracker.csv)  
- [gtm_conversation_tracker.csv](gtm_conversation_tracker.csv) · channel=partner_intro

---

## Kit checklist

- [ ] One-pager AR ([ops_client_pack](../../ops_client_pack/))  
- [ ] Trust Pack  
- [ ] Sample Proof Pack (redacted)  
- [ ] Calendly link
