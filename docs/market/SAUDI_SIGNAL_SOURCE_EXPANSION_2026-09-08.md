# Saudi Signal Source Expansion Backlog - 2026-09-08

## Status

`CANDIDATE_NOT_RUNTIME_AUTHORITY`.

The canonical runtime market-source registry remains `config/market/market_signal_sources_v3.json`. These candidates are research backlog entries to be promoted only through the existing source-owner contract after URL/freshness/access verification.

## Verified official candidate sources

### MEWA investment opportunities / Furas
- Official source: https://www.mewa.gov.sa/ar/Ministry/InvestmentOpportunities/Pages/default.aspx
- Value: current environmental, water, agriculture, livestock and land investment opportunities routed through the Furas platform.
- Dealix route: project/asset operations, digital workflow, evidence/proof, partner/subcontract research.
- Truth rule: an investment listing is a signal, not buyer intent or award.

### SAMA Open Banking Framework and Lab
- Official source: https://www.openbanking.sama.gov.sa/index-en.html
- Value: business rules, technical standards, API specifications, operational guidelines, sandbox/testing/certification signals for banks and fintechs.
- Dealix route: governed API operations, integration, evidence and operational-command diagnostics.
- Boundary: regulated financial activity and production/payment decisions remain separately governed.

### GASTAT economic/statistical data
- Official sources: https://www.stats.gov.sa/en/ and https://database.stats.gov.sa/
- Value: macro/sector indicators, industrial production, labor, inflation, FDI, tourism and business-confidence context.
- Dealix route: market timing and sector-priority evidence only; macro data never becomes account-level buyer intent.

### Ministry of Commerce Business Sector quarterly bulletins
- Official source: https://mc.gov.sa/ar/mediacenter/Pages/newslettes.aspx
- Current evidence: the Ministry lists Q1 and Q2 2026 business-sector bulletins alongside the 2025/2024 series.
- Value: commercial-registration growth, regional/sector formation patterns and category momentum for wedge prioritization.
- Dealix route: sector timing, regional prioritization and research-budget allocation.
- Truth rule: registration growth is not account-level demand, budget or buyer intent.

### Saudi Exchange issuer and financial-advisor announcements
- Official source: https://www.saudiexchange.sa/wps/portal/saudiexchange/newsandreports/issuer-news/issuer-announcements
- Value: searchable listed-company disclosures by publisher, market, sector, announcement class and time period; useful for awards, contracts, expansions, financing, governance and strategic-change triggers.
- Dealix route: listed-company trigger verification and account-research timing.
- Truth rule: a disclosure is a public trigger; it is not relationship, consent or a qualified problem.

### Saudi Open Data Portal
- Official source family: https://open.data.gov.sa/
- Value: structured government datasets for sector research, market sizing and provenance-backed context when current dataset access is available.
- Dealix route: research enrichment and macro/sector baselines only.
- Boundary: dataset accessibility/freshness must be checked per dataset; blocked/rejected URLs are not treated as current evidence.

### Monsha'at reports / SME Monitor
- Official source: https://monshaat.gov.sa/en/monshaat-reports
- Value: recurring SME ecosystem statistics, sector focus, regional signals, digital-transformation themes and entrepreneurship-program evidence.
- Dealix route: SME wedge selection, partner mapping, regional prioritization and market timing.
- Truth rule: ecosystem growth is not proof that a named SME has a problem, budget or consent.

### CST Saudi Internet / digital adoption indicators
- Official source family: https://www.cst.gov.sa/
- Current example: Saudi Internet Report 2025 announcement published 2026-07-19.
- Value: internet adoption, AI-tool usage, data consumption, speed, platform behavior and Saudi-domain growth as digital-readiness context.
- Dealix route: channel/product assumptions, digital-readiness baselines and content/distribution strategy.
- Truth rule: population-level adoption metrics never become account-level buying intent.

### MODON industrial transformation signals
- Official source family: https://modon.gov.sa/
- Current evidence example: https://award.modon.gov.sa/
- Value: manufacturing transformation, operational excellence, automation, smart maintenance, cybersecurity and supply-chain maturity signals across Saudi factories.
- Dealix route: factory diagnostics, brownfield integration, maintenance/quality/proof hypotheses.

### Tourism Development Fund programs
- Official source: https://www.tdf.gov.sa/
- Value: tourism financing and SME enablement programs can indicate project formation and operating-expansion windows.
- Dealix route: project operating systems, commercial execution, customer/partner workflow and proof.
- Truth rule: financing availability is not proof that a specific company has budget or buyer intent.

### Digital Government Authority open-source / GPaaS program
- Official source: https://dga.gov.sa/en/programs/GPaas
- Value: government open-source, DevSecOps, code-sharing, integration and software-delivery patterns.
- Dealix route: B2G readiness, DevSecOps evidence, integration and government-delivery architecture research.

### NCA cybersecurity controls
- Official sources: https://nca.gov.sa/en/regulatory-documents/controls-list/ecc/ and https://nca.gov.sa/en/regulatory-documents/controls-list/ccc/
- Value: current cybersecurity-control baselines for national entities and cloud contexts; use implementation guides as evidence references.
- Dealix route: compliance-aware architecture/proof gaps and partner qualification.
- Boundary: Dealix must not claim certification, NCA approval or managed-SOC licensing without evidence.

## Promotion rule

Before adding any candidate to the runtime registry:
1. verify official ownership and current URL;
2. define source family, freshness, access mode and polling cadence;
3. define allowed outputs and forbidden inferences;
4. map only to the five permanent agents;
5. add regression tests to prevent `signal -> opportunity`, `public contact -> consent`, or stale-data promotion;
6. preserve WIP limits and exact L5 gates;
7. preserve source URL, observed timestamp and extraction method in every evidence record;
8. prefer APIs/structured feeds when officially supported, otherwise use bounded public-page retrieval without bypassing access controls.

## Result

`RUNTIME_SOURCE_REGISTRY_MUTATED=false`

`RESEARCH_BACKLOG_EXPANDED=true`

`L5_EXECUTED=NONE`
