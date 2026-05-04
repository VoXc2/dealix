# Dealix — Service Tower Contracts

> Per the Doctrine: **"أي خدمة ما عندها هذا الشكل = لا تُباع."**
>
> Every bundle in `api/routers/services.py:CATALOG` is paired with a full
> contract in `api/routers/services.py:SERVICE_CONTRACTS` carrying:
> ideal_customer · required_inputs · workflow_steps · approval_points ·
> blocked_actions · deliverables · proof_metrics · definition_of_done.

## Contract Format

```python
{
    "ideal_customer_ar": [...],
    "required_inputs": [...],
    "workflow_steps": [...],          # ordered steps the team executes
    "approval_points": [...],         # which steps need human approval
    "blocked_actions": [...],         # cold_whatsapp, scraping, etc.
    "deliverables": [...],            # what the customer gets
    "proof_metrics": [...],           # what we measure
    "definition_of_done": [...],      # acceptance criteria for delivery
}
```

## API

- `GET /api/v1/services/catalog` — list of 6 bundles (with `contract` attached)
- `GET /api/v1/services/{bundle_id}/contract` — single contract
- `GET /api/v1/services/{bundle_id}/intake-questions` — required intake form

## The 6 Service Contracts (canonical)

### 1. Free Diagnostic
- **Price:** Free · 24h SLA · one-time
- **DoD:** `diagnostic_report_generated`, `next_action_recommended`, `client_update_sent`
- **Blocked:** none (no outbound)
- **Workflow:** intake → analyze channels → suggest 3 improvements → recommend bundle

### 2. Growth Starter (the wedge — 499 SAR · 7 days)
- **DoD:** `proof_pack_generated`, `next_action_recommended`, `client_update_sent`, `upsell_card_created`
- **Blocked:** `cold_whatsapp`, `linkedin_automation`, `guaranteed_revenue_claim`, `purchased_lists`
- **Approval points:** segment, messages, channel
- **Deliverables:** 10 opps + 6 messages + 3 follow-ups + risk notes + Proof Pack with HMAC

### 3. Data to Revenue (1,500 SAR · 10 days)
- **DoD:** `list_normalized`, `top_50_approved`, `drafts_approved`, `proof_pack_generated`
- **Blocked:** `send_to_no_consent`, `cold_whatsapp_to_purchased`, `scraping`, `linkedin_automation`
- **Workflow includes:** PDPL consent check per record, contactability scoring

### 4. Executive Growth OS (2,999 SAR/mo)
- **DoD:** `weekly_proof_pack_delivered`, `daily_briefs_running`, `monthly_review_held`
- **Blocked:** `cold_whatsapp`, `live_charge_without_explicit_approval`, `linkedin_automation`, `auto_email_send`
- **Approval points:** weekly segment, outbound drafts, upsell offers
- **Deliverables:** 4 daily-ops windows · 9 role briefs · weekly Proof Pack · monthly review

### 5. Partnership Growth (3,000–7,500 SAR · 30 days)
- **DoD:** `partner_pilot_signed`, `co_branded_proof_delivered`, `first_referral_tracked`
- **Blocked:** `exclusivity_before_proof`, `white_label_before_3_pilots`, `revenue_share_without_tracked_referral`

### 6. Full Growth Control Tower (Custom)
- **DoD:** `tenant_provisioned`, `all_integrations_live`, `csm_assigned`, `first_qbr_held`
- **Blocked:** `cross_tenant_data_leak`, `non_ksa_data_residency`, `live_charge_without_csm_approval`

## Workflow Diagram

```
intake (required_inputs)
   ↓
qualify (ICP match)
   ↓
[for each workflow_step]
   ↓
   approval_point? → Approval Queue → Approve/Edit/Skip
   ↓
   execute (blocked_actions enforced)
   ↓
   emit RWU → Proof Ledger
   ↓
deliverables packaged
   ↓
DoD check
   ↓
Proof Pack (HMAC) → Customer Workspace → Upsell card
```

Contracts are immutable per delivery instance — when a sprint starts in
Phase 2, the contract gets snapshotted into `SprintRecord.contract_snapshot_json`
so customers can't be moved to a different definition mid-delivery.
