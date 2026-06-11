# Client Acquisition System (Dealix)

## الهدف
تحويل اهتمام السوق إلى عملاء موقّعين بطريقة قابلة للقياس والتكرار، بدون spam، وبدون
اعتماد على حدس.

## المبدأ
كل إشارة عامة من شركة (إعلان، موقع، تقييم، تغريدة) تمر بسبع مراحل قبل أن تتحول إلى عقد:

1. **Discover** — رصد الإشارات المرئية
2. **Qualify** — احتساب نقاط ICP + BANT
3. **Outreach (Drafts Only)** — توليد مسوّدات عربي/إنجليزي
4. **Human Review Gate** — مراجعة بشرية إلزامية
5. **Workflow Review Call** — مكالمة 20 دقيقة
6. **Proposal** — عرض رسمي ثنائي اللغة
7. **Close** — توقيع العقد

ثم يبدأ **Delivery OS**، ثم **Retain & Expand**.

## قواعد لا تُكسر
- لا إرسال تلقائي. كل مسوّدة تنتظر review_status = approved.
- لا scraping للبيانات الخاصة. الإشارة لازم تكون عامة ومرئية.
- لا ادعاءات ROI مضمونة. لا شهادات زائفة.
- كل عميل demo يحمل `"demo": true` بشكل واضح.

## البيانات
- `business/_data/leads.json`
- `business/_data/scored_leads.json`
- `business/_data/outreach_review_queue.json`
- `business/_data/proposals.index.json`
- `business/_data/deals.ledger.json`

## السكربتات
- `scripts/build_first_100_leads_plan.py`
- `scripts/score_leads.py`
- `scripts/generate_outreach_drafts.py`
- `scripts/approve_outreach_draft.py`
- `scripts/reject_outreach_draft.py`
- `scripts/generate_sales_call_notes.py`
- `scripts/generate_proposal.py`
- `scripts/mark_proposal_sent.py`
- `scripts/mark_deal_won.py`
- `scripts/mark_deal_lost.py`
