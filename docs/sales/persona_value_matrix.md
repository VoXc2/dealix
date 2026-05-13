---
title: Persona-Value Matrix — Saudi Buying Committee × BFSI / Retail / Healthcare
doc_id: W2.T08.persona-value-matrix
owner: CRO
status: draft
last_reviewed: 2026-05-13
audience: [internal, partner]
language: en
ar_companion: docs/sales/persona_value_matrix.ar.md
related: [W0.T00, W1.T05, W1.T01, W1.T17, W2.T02, W2.T03, W2.T04, W2.T09, W2.T28]
kpi:
  metric: persona_tagged_outreach_per_quarter
  target: 1000
  window: 60d
rice:
  reach: 200
  impact: 1
  confidence: 0.9
  effort: 1
  score: 180
---

# Persona-Value Matrix — Saudi Buying Committee × BFSI / Retail / Healthcare

## 1. Context

Saudi enterprise sales is committee selling. A deal stalls when one persona — CEO, CRO, CIO/CTO, DPO/Legal, Head of Sales, Head of Marketing, or Procurement — feels the value claim is generic or alien to their function. This matrix gives each AE the one-line value claim, the one Arabic phrase, the top objection, and the counter-position vs the four named competitor classes (T17) — for every persona × vertical cell. Use it to build the multi-thread plan in any deal above SAR 200K.

## 2. Audience

CRO, AEs, BDRs, partner sellers. Marketing consumes for persona-tagged content. CS consumes for handoff briefing notes.

## 3. Decisions / Content

### 3.1 The seven personas

- **CEO** — narrative buyer; Vision 2030 + revenue growth + investor narrative.
- **CRO / CCO** — economic buyer; pipeline coverage + win rate + CAC.
- **CIO / CTO** — technical buyer; integrations + security + reliability + cost.
- **DPO / Legal** — compliance buyer; PDPL, cross-border transfer, sanctioned-list, audit trail.
- **Head of Sales** — operational buyer; rep productivity + cycle length + forecast accuracy.
- **Head of Marketing** — channel buyer; MQL quality + bilingual campaigns + attribution.
- **Procurement** — gatekeeper; cost defensibility + vendor risk + contractual terms.

### 3.2 The three verticals

- **BFSI** — SAMA-regulated banks, finance companies, fintechs.
- **Retail / eCommerce** — chains, marketplaces, Salla/Zid native merchants.
- **Healthcare** — clusters, NUPCO-served providers, SFDA-licensed medtech, pharma B2B.

### 3.3 Matrix — pain, value, AR phrase, top objection, counter-position

For each cell: top pain in one sentence; Dealix value claim in one sentence; the Arabic phrase a rep can read verbatim; the top objection that will land; the counter-position vs the dominant competitor class for that persona.

#### CEO

- **BFSI**: pain = "regulatory pressure squeezes growth, board expects Vision 2030-aligned new revenue." value = "Dealix is the first Saudi-native Revenue OS with audit-grade PDPL evidence — defensible to SAMA, board-readable." AR = "نظام إيراد سعودي الأصل بأدلة قابلة للتدقيق ومتوافق مع PDPL — جاهز للعرض على المجلس." objection = "Will SAMA accept your tooling?" counter (vs US stack) = "We are SAMA-defensible because we are PDPL-grade and Saudi-resident by default; the US stack has no story for SAMA cycle 1."
- **Retail**: pain = "expansion outside Riyadh stalls; CAC rises with each new city." value = "Outlet-footprint and expansion-signal targeting cuts CAC across regions." AR = "استهداف موقع المنفذ وإشارات التوسع يخفّض كلفة الاكتساب في كل المناطق." objection = "Have you done this with a chain our size?" counter (vs status quo) = "Manual research scales linearly with cities; Dealix scales O(1) per added vertical."
- **Healthcare**: pain = "privatization and Cluster procurement are slow and opaque to outside vendors." value = "Tender + procurement signal triggers + PDPL Art. 27 evidence open Cluster doors." AR = "محفزات المناقصات والمشتريات + أدلة المادة 27 من PDPL تفتح أبواب التجمعات الصحية." objection = "Health data is too sensitive for AI." counter (vs status quo) = "Decision Passport gates every action; the AI never touches Class A data without DPO consent."

#### CRO / CCO

- **BFSI**: pain = "pipeline coverage < 2.5×, win rate sliding, BDR cost rising." value = "+50% qualified pipeline, +3pp win rate at conservative, cycle compression 25%." AR = "+50% خط إيراد مؤهَّل، +3 نقاط نسبة فوز، اختصار دورة 25% في السيناريو المتحفظ." objection = "Sounds optimistic; show me Saudi numbers." counter (vs US stack) = "US tools quote US benchmarks; we quote you the Saudi BFSI median from `docs/sales/roi_model_saudi.md`."
- **Retail**: pain = "wholesale and franchise pipelines are agency-dependent and unattributable." value = "Owned engine, attributable pipeline, no agency lock-in." AR = "محرك تملكه أنت، خط إيراد قابل للنسب، بلا ارتباط بوكالة." objection = "Agencies give us human attention." counter (vs agencies) = "You pay once for the engine, not monthly for lists — and you keep the asset."
- **Healthcare**: pain = "tender win rates are < 12%, cycle > 9 months." value = "Pre-positioned evidence + cluster-level entity resolution lifts win rate to 22%." AR = "أدلة مُوضَّعة سلفًا + استبانة كيانية على مستوى التجمع ترفع نسبة الفوز إلى 22%." objection = "Procurement is political, not technical." counter (vs local CRM) = "Local CRMs don't run the tender-signal layer; Decision Passport is the credibility artifact procurement reads."

#### CIO / CTO

- **BFSI**: pain = "vendor sprawl, SOC2 + SAMA cyber framework + PDPL all in one quarter." value = "Single platform replaces 3 vendors; SOC2 Type II, PDPL native, SAMA cyber-framework aligned." AR = "منصة واحدة تستبدل ثلاثة موردين؛ SOC2 Type II ومتوافقة مع PDPL وإطار SAMA السيبراني." objection = "What is your KSA data residency story?" counter (vs US stack) = "We host on KSA cloud regions for Sovereign tier; the US stack cannot guarantee residency."
- **Retail**: pain = "ZATCA Phase 2 and POS integrations dominate budget; little room for new tools." value = "Integration cost amortizes against three vendors we replace." AR = "تكلفة التكامل تتوزّع على ثلاثة موردين نستبدلهم." objection = "Salla/Zid integration?" counter (vs local CRM) = "We have native connectors to Salla/Zid and to your POS via standard APIs; local CRMs require services projects."
- **Healthcare**: pain = "SFDA, MoH, NPHIES interop, all on PDPL Class A data." value = "Decision Passport carries audit trail acceptable to MoH and SFDA reviews." AR = "Decision Passport يحمل سجل تدقيق مقبول لمراجعات وزارة الصحة وهيئة الغذاء والدواء." objection = "Cloud sovereignty for Class A data?" counter (vs US stack) = "Sovereign tier hosts in-Kingdom; US stack cannot."

#### DPO / Legal

- **BFSI**: pain = "PDPL Art. 13/14 enforcement, cross-border transfer rules, sanctioned-list checks per outreach." value = "Every outreach has a Decision Passport with lawful-basis evidence; sanctioned-list check is one API call." AR = "كل تواصل خارجي يحمل Decision Passport بأدلة الأساس القانوني، وفحص قوائم العقوبات بطلب API واحد." objection = "How do you handle data-subject rights requests?" counter (vs all) = "Native DSR workflow in product; competitors require services to wire it up."
- **Retail**: pain = "consumer + B2B mix muddies PDPL classification." value = "We tag B2B intent only; B2C handled separately by your existing stack." AR = "نحن نُعلِّم نية B2B فقط؛ B2C تبقى في منصّتك الحالية." objection = "What about Maroof scraping legality?" counter (vs agencies) = "Lawful basis is documented per source in `docs/product/saudi_lead_engine.md`."
- **Healthcare**: pain = "Class A health data + PDPL Art. 27 + NPHIES rules." value = "Engine never touches Class A; Passport carries scope-limited evidence." AR = "المحرك لا يتعامل مع البيانات الصحية الحساسة، وPassport يحمل أدلة محدودة النطاق." objection = "What is your DPIA?" counter (vs all) = "We supply a templated DPIA via the trust pack."

#### Head of Sales

- **BFSI**: pain = "BDR research time > 60%, AE pipeline coverage thin." value = "Cut BDR research time to <20%; deliver ranked-A leads daily." AR = "خفض وقت بحث BDR إلى أقل من 20%، وتسليم عملاء فئة A جاهزين يوميًا." objection = "Won't reps disengage?" counter (vs status quo) = "Reps still own the conversation; we own the prep work."
- **Retail**: pain = "expansion to new cities requires net-new account list per city." value = "Region/city seeds + Maroof/Maps enrichment delivers ranked lists in 24h." AR = "بذور المنطقة + إثراء Maroof/Maps يسلّم قوائم مرتّبة خلال 24 ساعة." objection = "Bilingual coverage?" counter (vs local CRM) = "Engine resolves entities in Arabic and English natively."
- **Healthcare**: pain = "long, opaque pipelines, hard to forecast." value = "Tender-signal lead time pre-positions us 90 days before RFP." AR = "إشارة المناقصة تمنحنا تموضعًا قبل 90 يومًا من إصدار RFP." objection = "What about clinical buyers?" counter (vs all) = "We index clinical leadership via SCFHS and SHC public registries."

#### Head of Marketing

- **BFSI**: pain = "MQL quality is poor; lead vendors recycle the same accounts." value = "Engine output is de-duped against your CRM and against past vendor lists." AR = "مخرَج المحرك مُستبعَد التكرار مقابل CRM وقوائم الموردين السابقة." objection = "Will it integrate with our marketing automation?" counter (vs US stack) = "Native connectors to Marketo, HubSpot, and Microsoft via REST."
- **Retail**: pain = "Arabic campaign creative struggles; agency-dependent." value = "Persona-tagged Arabic outreach drafts; AE owns the send." AR = "مسوّدات تواصل عربية موسومة بالشخصية، وAE هو من يُرسل." objection = "Brand control?" counter (vs agencies) = "Draft_only mode; nothing sends without rep approval."
- **Healthcare**: pain = "clinical and admin audiences need different messaging." value = "Persona-vertical templates split by stakeholder; Decision Passport carries the rationale." AR = "قوالب موزّعة على الأطباء والإداريين، وPassport يوضح المنطق." objection = "Compliance with health advertising rules?" counter (vs all) = "Outreach is B2B, gated by PDPL Art. 27 and SFDA advertising guidance."

#### Procurement

- **BFSI**: pain = "vendor risk, defensibility on cost." value = "Conservative ROI ≥ 240% with worked SAR example in the deck." AR = "عائد متحفظ ≥ 240% مع مثال محسوب بالريال." objection = "What is your vendor risk profile?" counter (vs all) = "Saudi-registered entity, KSA data residency option, SOC2 Type II, PDPL-native — all in `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`."
- **Retail**: pain = "long PO cycles, multiple legal entities." value = "Master agreement per holding company, per-entity SOW." AR = "اتفاقية رئيسية للقابضة، وعقود تنفيذية لكل كيان." objection = "Single-supplier risk?" counter (vs all) = "Optional partner-of-record clause via T6 partner program."
- **Healthcare**: pain = "NUPCO/Cluster procurement constraints." value = "We support NUPCO supplier-registration pathway." AR = "ندعم مسار تسجيل الموردين لدى NUPCO والتجمعات." objection = "Local content?" counter (vs all) = "Roadmap to NCLP (Local Content) accreditation in 12 months — tracked in T11."

### 3.4 Multi-thread playbook

For any opportunity > SAR 200K, an AE must:
- Identify the named individual for each of the 7 personas within 14 days of opportunity creation.
- Send at least one persona-tagged asset to ≥ 4 of the 7 personas before stage advance.
- Capture each persona's top objection in the CRM custom field "stated_objection".
- Use the AR phrase for any persona who has expressed Arabic preference (recorded in the contact's "preferred_language" field).

### 3.5 What the matrix is NOT

- It is not a content library — see T20 bilingual asset index for that.
- It is not a battlecard — see `docs/sales/BATTLECARDS.md` and T17 competitive landscape.
- It is not a replacement for discovery — the AE still asks; this matrix structures what to do with answers.

## 4. KPIs

- 1,000 persona-tagged outreach actions in 60 days.
- ≥ 4 of 7 personas reached on every opp > SAR 200K before stage advance.
- Stated-objection field populated on 100% of late-stage opps.

## 5. Dependencies

- T5 ICP (`docs/go-to-market/icp_saudi.md`) — defines who counts as which persona.
- T1 verticals (`docs/go-to-market/saudi_vertical_positioning.md`) — supplies vertical pain.
- T17 competitive (`docs/strategy/competitive_landscape_sa.md`) — counter-position rows.
- T2 ROI (`docs/sales/roi_model_saudi.md`) — economic numbers for CRO/Procurement.
- T28 enablement (`docs/sales/enablement_program.md`) — reps trained on this matrix before they may run > SAR 200K deals.

## 6. Cross-links

- Master: `docs/strategy/SAUDI_30_TASKS_MASTER_PLAN.md`
- AR companion: `docs/sales/persona_value_matrix.ar.md`
- Sales playbook AR: `docs/SALES_PLAYBOOK.ar.md`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`

## 7. Owner & Review Cadence

- **Owner**: CRO.
- **Review**: monthly with marketing + product; objection rows refreshed from CRM "stated_objection" data every 60 days.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | CRO | Initial 7-persona × 3-vertical matrix with counter-positioning rows |
