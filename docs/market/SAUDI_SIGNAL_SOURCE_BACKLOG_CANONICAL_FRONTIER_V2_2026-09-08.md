# Saudi Signal Source Backlog — Canonical Capability Frontier V2

Status: `CANDIDATE_NOT_RUNTIME_AUTHORITY`

This file harvests the useful Saudi signal-source research into the canonical Capability Frontier V2 branch. Runtime authority remains `config/market/market_signal_sources_v3.json`; promotion requires current URL/freshness/access verification, provenance, five-agent ownership, regression tests, WIP limits and Truth Firewall preservation.

## Candidate source families

- MEWA / Furas investment opportunities — environment, water, agriculture, livestock and land investment signals.
- SAMA Open Banking Framework/Lab — API standards, operational rules, sandbox/testing and certification signals.
- GASTAT — macro and sector indicators for timing and prioritization only.
- Ministry of Commerce quarterly business-sector bulletins — registration/category/regional momentum, never account-level intent.
- Saudi Exchange issuer announcements — public awards/contracts/expansion/financing/governance triggers, never relationship or consent.
- Saudi Open Data Portal — structured public datasets when current dataset access and provenance are verified.
- Monsha'at reports / SME Monitor — SME ecosystem, sector and regional timing.
- CST — digital adoption/readiness indicators.
- MODON — industrial transformation, automation, maintenance, quality and supply-chain maturity signals.
- Tourism Development Fund — tourism project formation/financing and SME enablement signals.
- Digital Government Authority GPaaS/open-source — B2G DevSecOps, code-sharing and integration patterns.
- NCA ECC/CCC controls — compliance-aware architecture/proof references; never claim certification or approval.
- National Water Company (NWC) supplier relations and competition announcements — supplier registration/prequalification, materials/local-content readiness and active competition discovery in the Saudi water utility ecosystem. Registration/qualification is not buyer intent, consent or award.
- Saudi Water Partnership Company (SWPC) current/future PPP project program — desalination, purification, wastewater treatment, strategic storage, transmission and dam PPP tendering/project formation. Use primarily for project/consortium/prime-subcontract research; an announced pipeline is not eligibility or award.
- Royal Commission for Jubail and Yanbu (RCJY) investor journey / investment opportunities — industrial-city investment, private-sector participation, industrial/logistics/shared-services/smart-city and digital-transformation signals across Jubail, Yanbu, Ras Al-Khair and Jazan. Investment enablement is a market signal, not a customer relationship.

## Fresh official evidence for the water / industrial-city additions — 2026-09-08

### National Water Company — supplier relations
- Official URL: `https://www.nwc.com.sa/AR/BusinessSector/VendorsRelationships/Pages/default.aspx`
- Current page explicitly covers supplier registration/qualification, supplier performance, local content, iSupplier portal access and competition announcements.
- Candidate lane: `SUPPLIER_NETWORK` + `B2G_PROCUREMENT`.
- Candidate default grade: `D2`, upgrading a specific verified current competition to `D4` only through its exact competition evidence.
- Allowed outputs: `supplier_readiness`, `competition_research`, `category_mapping`, `partner_research`, `account_research`.
- Forbidden inferences: `buyer_intent`, `relationship`, `consent`, `qualification`, `award`.

### Saudi Water Partnership Company — PPP project program
- Official URL: `https://www.swpc.sa/`
- Current SWPC program material states its role tendering PPP water projects spanning desalination/purification/treatment, strategic reservoirs, transmission and dams and managing related offtake agreements.
- Candidate lane: `PPP_PRIVATIZATION`.
- Candidate default grade: `D2`; a current verified RFQ/RFP/EOI may be promoted to `D4` only from exact project evidence.
- Allowed outputs: `project_research`, `consortium_research`, `prime_subcontract_research`, `partner_research`, `bid_no_bid_research`.
- Forbidden inferences: `buyer_intent`, `relationship`, `consent`, `qualification`, `award`.

### Royal Commission for Jubail and Yanbu — investor journey
- Official URL: `https://rcjy.gov.sa/`
- Current official investor material covers private-sector participation and investment processes across the Royal Commission industrial cities; official material also highlights services/logistics/real-estate/smart-city/shared-services and digital-transformation investment themes.
- Candidate lane: `INDUSTRIAL_DIGITIZATION` + `GROWTH_ENABLEMENT`.
- Candidate default grade: `D1/D2` depending on exact current opportunity evidence.
- Allowed outputs: `investment_research`, `industrial_account_research`, `partner_research`, `diagnostic_template_input`, `market_entry_research`.
- Forbidden inferences: `buyer_intent`, `relationship`, `consent`, `budget`, `award`.

## Promotion contract

1. Verify official ownership and current URL.
2. Define source family, freshness, access mode and polling cadence.
3. Define allowed outputs and forbidden inferences.
4. Map only to `dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, or `dealix-content`.
5. Add regression tests preventing `signal -> opportunity`, `public contact -> consent`, and stale-data promotion.
6. Preserve WIP and exact L5 gates.
7. Preserve source URL, observed timestamp and extraction method in every evidence record.
8. Prefer official APIs/structured feeds where supported; otherwise bounded public retrieval without bypassing access controls.
9. Treat supplier registration, prequalification, investment enablement and future-project pipelines as `RESEARCH_ONLY` until a specific current demand signal is verified.

`RUNTIME_SOURCE_REGISTRY_MUTATED=false`
`RESEARCH_BACKLOG_EXPANDED=true`
`L5_EXECUTED=NONE`
