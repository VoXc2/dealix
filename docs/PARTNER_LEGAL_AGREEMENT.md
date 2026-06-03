# Partner Legal Agreement (Referral) — Template — Dealix

**Status:** DRAFT TEMPLATE — must be lawyer-reviewed before signing partner #1
**Owner:** Sami (founder) · co-signed with each agency partner
**Last updated:** 2026-05-07
**Companion docs:** `docs/AGENCY_PARTNER_PITCH.md` · `docs/LEGAL_ENGAGEMENT.md` · Plan §23.5.9

> **Why this doc exists:** Plan §23.5.9 calls for first agency partner by Week 11. Without a written referral agreement, founder will hand-shake-deal his way into either lost commissions, broken trust, or PDPL exposure (partner sharing customer data without DPA chain).
>
> This is a **template draft only**. Lawyer must review per `LEGAL_ENGAGEMENT.md` deliverable L8 before partner #1 signs.

---

## 1. Document title

**اتفاقيّة شراكة إحالة (Referral Partnership Agreement)**

**بين:**
- **Dealix** — [official entity name pending legal registration] (الطرف الأوّل)
- **[Partner Agency Name]** — السجل التجاري رقم [...] (الطرف الثاني)

**التاريخ:** [...]

---

## 2. Recitals (تمهيد)

> الطرف الأوّل (Dealix) يُشغّل منصّة AI Operating Team للشركات الصغيرة والمتوسّطة في المملكة العربيّة السعوديّة، وفق الالتزامات المنصوص عليها في:
> - نظام حماية البيانات الشخصيّة السعودي (PDPL)
> - ٨ بوّابات أمان دستوريّة (NO_LIVE_SEND, NO_LIVE_CHARGE, NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO, NO_SCRAPING, NO_FAKE_PROOF, NO_FAKE_REVENUE, NO_BLAST)
>
> الطرف الثاني (الوكالة) يعمل في تسويق B2B في السعوديّة ولديه عملاء يحتاجون خدمات Dealix.
>
> اتّفق الطرفان على ما يلي:

---

## 3. Scope of partnership (نطاق الشراكة)

### 3.1 What partner does

- Introduces Dealix to qualified prospects in their network
- Acts as **referrer only** (NOT reseller, NOT white-label)
- Maintains relationship with their original customer
- May co-deliver agreed services (back-office model per `AGENCY_PARTNER_PITCH.md`)

### 3.2 What Dealix does

- Owns the customer relationship for AI Operating Team services
- Owns the contract, billing, support, and compliance
- Pays referral commission per §4
- Provides partner with marketing assets (one-pager, deck, demo link)

### 3.3 Out of scope

- Partner does NOT have authority to negotiate price below founding-partner tier
- Partner does NOT receive customer PII before DPA chain is signed (Controller → Processor → sub-processor)
- Partner does NOT use Dealix branding outside agreed marketing assets
- Partner does NOT send cold WhatsApp / scrape / blast on Dealix's behalf

---

## 4. Commission structure

| Customer outcome | Commission % | Payment timing |
|---|---|---|
| Sprint signed (499 SAR paid) | 30% of net revenue (after VAT) | Within 30 days of `payment_confirmed` |
| Partner signed (12K/mo, 4-month commit) | 30% of first 4 months net | Monthly, with each invoice payment_confirmed |
| Partner renewed (months 5-12) | 15% of months 5-12 net | Monthly |
| Partner renewed (year 2+) | 0% (relationship matures, fee tapers off) | N/A |

### 4.1 Net revenue definition

Net = SAR collected - VAT - Moyasar fees (if applicable) - refunds.

Commission is paid only on `payment_confirmed` revenue. Invoice intent does NOT trigger commission.

### 4.2 No commission on

- Refunded amounts (commission must be returned if customer refunds within partner-eligible period)
- Customers partner had no role in introducing (must be sourced via partner channel)
- Customers who came through both partner AND another channel (single-attribution rule, partner notified within 7 days)

---

## 5. PDPL chain (CRITICAL)

### 5.1 Data flow

> Customer (Controller) → Dealix (Processor under DPA) → Partner (Sub-processor only IF needed AND signed sub-processing agreement)

### 5.2 Partner obligations

- Partner does NOT receive customer PII unless explicit need + signed sub-processing agreement with Dealix
- Partner cannot scrape, blast, or cold-outreach using customer data
- Partner notifies Dealix within 24h of any suspected data incident
- Partner names a primary data contact (PDPL DPO equivalent if applicable)

### 5.3 What partner CAN do without PII access

- Make warm intros (partner already has the relationship)
- Co-deliver Sprint Day 1 (kickoff, ICP definition) under partner's existing customer relationship
- Receive aggregated, anonymized reports from Dealix (e.g., "this Sprint generated 8 proof events" — no customer-name-level data without DPA)

---

## 6. Hard rules (mirroring Dealix's 8 gates)

The partner agrees to NEVER:

1. Send cold WhatsApp on Dealix's behalf (NO_COLD_WHATSAPP)
2. Initiate live charges on customer cards (NO_LIVE_CHARGE — only Dealix's payment_ops)
3. Run automated LinkedIn outreach claiming Dealix branding (NO_LINKEDIN_AUTO)
4. Scrape competitor data using Dealix tools (NO_SCRAPING)
5. Publish testimonials / case studies attributed to Dealix without `signed_publish_permission` (NO_FAKE_PROOF / NO_UNAPPROVED_TESTIMONIAL)
6. Quote guaranteed revenue / KPI numbers to prospects (Article 8 — KPI commitment ≠ guarantee)
7. Send blast / mass-message campaigns using Dealix branding (NO_BLAST)
8. Process Saudi customer PII outside of signed DPA chain (PDPL Article violation)

**Breach of any rule = immediate termination + return of all paid commissions + Dealix reserves legal recourse.**

---

## 7. Term + termination

### 7.1 Term

12 months, auto-renew for 12 months unless either party gives 30-day written notice.

### 7.2 Termination by Dealix

- Immediate, no notice: breach of any §6 hard rule
- 30-day notice: business-direction change, partner under-performance (<1 referred customer in 6 months)
- 60-day notice: convenience

### 7.3 Termination by Partner

- 30-day notice: convenience
- Immediate: Dealix material breach (e.g., commissions unpaid 60+ days)

### 7.4 Survival clauses

After termination:
- Partner stops using Dealix branding within 7 days
- Existing referred customers' commissions continue per §4 schedule (unless partner-side breach)
- Confidentiality (§9) survives 3 years
- PDPL data-handling obligations survive indefinitely

---

## 8. Anti-poaching + non-circumvention

- Partner agrees NOT to poach Dealix-introduced customers to a competing AI ops product for 18 months post-introduction
- Partner agrees NOT to circumvent Dealix to deal directly with Dealix's customers regarding Dealix services
- Dealix agrees NOT to poach partner's existing customers for non-Dealix services

---

## 9. Confidentiality

- Both parties keep commercial terms (commission %, customer counts, pricing) confidential
- 3-year survival post-termination
- Exceptions: legal disclosure, lawyer / accountant under their own confidentiality

---

## 10. Marketing usage

- Partner may say: "Authorized referral partner of Dealix" (with Dealix's prior written approval)
- Partner may share Dealix one-pager + demo link
- Partner may NOT claim: "Co-founder", "Co-builder", "White-label provider"
- Joint case studies require both parties' written approval per case (matches `signed_publish_permission` from customer)

---

## 11. Dispute resolution

- First: 30-day good-faith negotiation between parties
- Second: Mediation in Saudi Arabia (founder + partner principal in same room)
- Final: Saudi commercial courts (Riyadh) per Saudi law

Governing law: Kingdom of Saudi Arabia.

---

## 12. Signatures

| Field | Dealix | Partner |
|---|---|---|
| Signatory name | _Sami [last name]_ | _[Partner principal name]_ |
| Title | Founder &amp; CEO | _[Title]_ |
| Date | _[Date]_ | _[Date]_ |
| Signature | _[Sig]_ | _[Sig]_ |
| Witness (optional) | _[Name + sig]_ | _[Name + sig]_ |

---

## 13. Schedule A — referral attribution form (per customer)

Each new customer introduced gets a 1-pager filed by partner:

```
Date of introduction: _____________
Customer name: ______________________
Customer sector: _____________________
Partner contact at customer: _________
Estimated SKU fit (Sprint / Partner): ___
Notes: ______________________________
```

Filed in `docs/wave6/live/partner_referrals.jsonl` (gitignored). Counted toward §4 commission only after Dealix confirms within 14 days.

---

## 14. Lawyer review checkpoints

Before partner #1 signs, lawyer reviews:

- [ ] §3 scope alignment with Saudi commercial agency law
- [ ] §4 commission structure tax treatment (VAT on commission income)
- [ ] §5 PDPL chain compliance (sub-processor contract clauses)
- [ ] §6 hard rules legal enforceability
- [ ] §7 termination clauses Saudi-enforceable
- [ ] §8 non-circumvention clause Saudi-enforceable (limited to 18 months max in Saudi)
- [ ] §11 dispute resolution forum (Saudi courts vs arbitration)

> **Disclaimer:** This template is NOT legal advice. Lawyer review is REQUIRED per `LEGAL_ENGAGEMENT.md` deliverable L8 before signing partner #1. All clauses subject to lawyer revision.
