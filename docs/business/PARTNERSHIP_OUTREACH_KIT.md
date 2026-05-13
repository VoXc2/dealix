# Saudi Ecosystem Partnership Outreach Kit (W13.12)

> **Goal:** secure 3 strategic partnerships in Y1 H2 (post-customer #10): 1 government-adjacent (Misk/SDAIA), 1 corporate ecosystem (Aramco/STC), 1 capital (1957/STV).
> **Activation:** customer #10 paying. Until then, no outreach — partners pay for proof.

---

## The 4 Target Partner Categories

### Category 1 — Government / Quasi-Government

These move slowly but unlock massive credibility + distribution.

#### Misk Foundation
- **Why:** Vision 2030 alignment, startup ecosystem builder
- **What they offer:** mentorship, brand stamp, founder events, sometimes co-funding
- **Why fit:** Dealix's Saudi-first thesis aligns with Misk's Vision 2030 mandate
- **Outreach path:** Misk Foundation careers/startup contact → escalate to ecosystem partnerships director
- **Ask:** Co-marketing on Vision 2030 AI initiatives
- **Risk:** slow procurement, brand-aligned constraints

#### SDAIA (Saudi Data and AI Authority)
- **Why:** They REGULATE PDPL. Partnership = both regulatory credibility + bidirectional information flow.
- **What they offer:** PDPL co-pilot opportunities, government tender pre-qualification, conference speaking
- **Outreach path:** SDAIA Open Innovation programs → escalate to AI strategy advisor
- **Ask:** Dealix as reference implementation for Saudi PDPL+ZATCA AI ops
- **Risk:** government timeline drift; respond within their cadence

#### MoCI / MCI (Ministry of Commerce)
- **Why:** They have the Saudi business registry data Dealix already integrates
- **What they offer:** Official data access + integration formalization
- **Outreach path:** Open Data initiatives at data.gov.sa
- **Ask:** Approved-use license for B2B prospect search
- **Risk:** policy changes; design for graceful degradation

---

### Category 2 — Saudi Corporate Ecosystem

These are slower to close but anchor R7 Enterprise PMO pipeline.

#### Aramco Digital
- **Why:** Saudi industrial AI play, $5B+ committed to digital. Real procurement budget.
- **What they offer:** Vendor pre-qualification, Aramco-supplier ecosystem access
- **Outreach path:** Wa'ed Ventures (Aramco's VC arm) → Aramco Digital business development
- **Ask:** Pilot with one Aramco subsidiary (Sadara, SABIC, etc.)
- **Risk:** procurement cycle 6-12 months; bring legal early

#### STC (Saudi Telecom)
- **Why:** Telco-adjacent B2B SaaS opportunity; STC Solutions has 1B+ SAR procurement
- **What they offer:** Distribution to STC B2B customer base
- **Outreach path:** STC Solutions partnership team → reseller program
- **Ask:** White-label Dealix as "STC Sales AI" for SMB customers
- **Risk:** brand dilution if mishandled; require co-branding control

#### Mobily / Zain KSA
- **Why:** Same as STC, smaller scale
- **Risk:** same telco procurement cadence

---

### Category 3 — Capital Partners

(Detail in `INVESTOR_OUTREACH_LIST.md` W13.14 — listed here for cross-reference)

- 1957 Ventures, STV, MEVP, Aramco Ventures (Wa'ed), 500 Global MENA

---

### Category 4 — Agency / Reseller Partners (R6 White-Label activation)

These move FAST and drive volume.

#### TwoFour54 (Abu Dhabi adjacent)
- **Why:** Saudi-adjacent regional agency network
- **What they offer:** Their book of B2B clients for Dealix to white-label
- **Outreach path:** Partner ecosystem director
- **Ask:** 25% rev-share on net new
- **Trigger:** customer #15 + 3 case studies

#### Saudi B2B Marketing Agencies (top 10 by revenue)
- **Why:** They sell B2B services already; Dealix becomes their AI add-on
- **Outreach path:** founder personal LinkedIn outreach
- **Ask:** R6 White-Label partnership (per `agency_partner_kit.md`)
- **Trigger:** customer #10

---

## Outreach Templates (Saudi-adapted)

### Template A — Government / Misk / SDAIA

```
السلام عليكم {recipient name},

أعمل مع Dealix — نظام التشغيل AI السيادي لقطاع B2B السعودي. نحن مبنون
حول 3 محركات: Lead Engine، 7 خدمات AI، Trust Engine (PDPL + ZATCA).

أرى تقاطعاً واضحاً مع {Misk's Vision 2030 mandate / SDAIA's open
innovation program} في:
  1. تطبيق PDPL لـ AI workflows بشكل قابل للتدقيق
  2. ZATCA Phase 2 e-invoice automation
  3. Saudi B2B AI كـ reference implementation

عرضي: 30 دقيقة محادثة لاستكشاف تعاون محتمل. لست راعياً ولست مستثمراً
حالياً — مهتم بـ value alignment لـ Vision 2030.

Public artifacts للتحقق المبدئي:
  - api.dealix.me/api/v1/compliance/status (live PDPL+ZATCA verification)
  - dealix.me/vision (strategic narrative)
  - dealix.me/dpo (PDPL Art. 32 disclosure)

شكراً,
سامي عسيري
+966 5X XXX XXXX
sami@dealix.me
```

### Template B — Aramco Digital / STC / Mobily

```
[English-first for corporate procurement teams]

Subject: Dealix — Saudi-sovereign AI Operating System (partnership exploration)

Dear {recipient name},

I lead Dealix, the Saudi-sovereign AI Operating System for B2B.
Live in production with {N} paying Saudi B2B customers, 87% gross
margin, PDPL+ZATCA wired in code (live verification at
api.dealix.me/api/v1/compliance/status).

I see strategic alignment with {Aramco Digital's industrial AI agenda
/ STC Solutions' B2B platform / Mobily Business solutions} on:

1. {Specific value prop tied to their public initiative}
2. Saudi-sovereign data residency (me-south-1, no cross-border)
3. Vendor pre-qualification path to their internal procurement

Proposed engagement: 30-min business development conversation to
explore {pilot opportunity / reseller arrangement / supplier pre-qual}.

Existing Dealix evidence:
- {N} active Saudi B2B customers (sectors: ...)
- 87% gross margin, NRR > 100% Y1
- 121 routers + 290+ tests + 8 schema migrations
- Founder-led customer onboarding through first 30

Pre-Series A timing — building strategic relationships before raising.

Best regards,
Sami Asiri
Founder & CEO, Dealix
sami@dealix.me · +966 5X XXX XXXX
```

### Template C — Agency / Reseller

```
[More casual, founder-to-founder energy]

السلام عليكم {Agency CEO name},

أنا سامي، مؤسس Dealix. نبني Saudi-native AI ops layer لـ B2B.

ربعك يبيعون لـ Saudi B2B clients — قدّموا لهم AI + WhatsApp answer
+ PDPL audit. Dealix يصير الـ AI layer "خفية" تحت برانديك.

How it works:
  - تختار 5 من عملاءك يحتاجون AI ops
  - Dealix يعمل tenant setup لكلهم تحت رؤيتك
  - branding كامل (logo, name, theme — مدمج في الـ tenant_themes table)
  - عمولة 25% MRR من كل customer قدّمته (lifetime)
  - Setup fee: 1,000 SAR (نسبتي onboarding + Decision Passport audit)

If 5 of your clients each pay 2,999 SAR/mo (Growth) = 14,995 MRR.
25% = 3,748 SAR/mo passive لك. كل شهر. مدى الحياة.

تجرب tenant واحد free 30-day؟ DM وأرتّب.

سامي
```

---

## Tracking Spreadsheet (per partner)

| Partner | Tier | Owner | Stage | Last Touch | Next Action | Date | Notes |
|---------|------|-------|-------|-----------|------------|------|-------|

Stages:
- `prospect` — identified, not contacted
- `contacted` — first email/DM sent
- `responded` — partner engaged
- `meeting` — initial call scheduled or done
- `negotiation` — term sheet or partnership terms discussed
- `signed` — partnership active
- `live` — generating revenue / referrals
- `dormant` — paused
- `dead` — declined

---

## Cadence Discipline

- **Max 3 outreaches/week** (else founder burns out + comes off desperate)
- **Follow-up cadence:** Day 3 nudge, Day 10 second nudge, Day 30 close-file
- **Always have a current Dealix metric to share** (yesterday's MRR, last week's customer count)
- **Never offer free pilot** to partners — it signals desperation
- **Always have a "no" path documented** — what's the polite decline that preserves option to re-engage?

---

## Activation Gate

**Today (2026-05-13):** Pre-revenue. Do not contact partners yet.

**Activate when:**
- Customer #10 paying (proof of validation)
- ≥ 1 case study draft (referenceable)
- Founder calendar has ≥ 10 hours/week for partnership development
- Customer Success playbook (W13.20) operational

**Trigger order:**
1. First 3 Agency outreaches (Category 4) — fastest to revenue
2. Capital partners (Category 3) — overlap with Wave 14 fundraising
3. Government (Category 1) — slow burn, start early but expect Y2 close
4. Corporate (Category 2) — start at customer #25; procurement cycles need runway

---

## Honest Disclosure

Partnership outreach is **third-priority** behind:
1. Customer #1 sales (v4 §15)
2. Customer success retention (W13.20)

If you have 4 hours this week, spend them in this priority order.
Partnerships compound — they reward patience, not panic.
