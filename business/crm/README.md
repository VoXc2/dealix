# CRM (Dealix)

## الوضع الحالي
- Mode: `demo_json` افتراضي
- Fallback: `database` (Postgres) إذا كان `DATABASE_URL` مضبوط

## البيانات
- `business/_data/leads.json` (accounts)
- `business/_data/outreach_review_queue.json` (drafts)
- `business/_data/proposals.index.json` (proposals)
- `business/_data/deals.ledger.json` (deals)
- `business/_data/proof_vault.json` (proof items)
- `business/_data/outreach_review_queue.json` (review queue)

## المخطط
- `business/crm/schema.md`

## السكربتات
- `scripts/import_leads_csv.py`
- `scripts/score_leads.py`
- `scripts/generate_outreach_drafts.py`
- `scripts/approve_outreach_draft.py`
- `scripts/reject_outreach_draft.py`
- `scripts/generate_proposal.py`
- `scripts/mark_deal_won.py`
- `scripts/mark_deal_lost.py`

## قواعد
- لا سجل demo يُعرض كانجاز حقيقي
- كل سجل demo يحمل `demo: true` بشكل واضح
- المراجعة البشرية إلزامية قبل أي إرسال
