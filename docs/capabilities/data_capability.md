# Capability Blueprint — Data Capability

> One of the 7 capabilities Dealix builds inside customers (per
> `docs/company/CAPABILITY_OPERATING_MODEL.md`). Mirrors the structure of
> `docs/capabilities/revenue_capability.md`. Concerns the **substrate**
> every other capability sits on: clean, deduplicated, source-attributed,
> PDPL-aware records that an AI workflow can safely read.

## Business purpose
Get the customer's data into a state where decisions can be trusted and
AI can be deployed safely. Cleanup, dedupe, quality scoring, PII triage,
and source attribution — done once, then re-run on a cadence. The Data
Capability is the foundation; Revenue / Customer / Operations / Knowledge
all degrade if it's weak.

> **Hard rule**: *no data without source*. Every record carries provenance
> at ingest. Records without a verifiable source are quarantined to
> `research-only` and never flow into outreach, drafts, or reports
> (per `docs/governance/RUNTIME_GOVERNANCE.md` Check 1).

## Typical problems
- Five spreadsheets, three CRMs, and a WhatsApp export — same accounts,
  different spellings.
- Saudi entity names not normalized: "Saudi Aramco" vs "أرامكو السعودية"
  vs "Aramco KSA" appear as three records.
- National ID / IBAN / card numbers sitting unredacted in marketing lists.
- "Source" column blank for half the rows — nobody can say where a lead
  came from or whether consent exists.
- Stale data: 30% of phone numbers disconnected; nobody has run a freshness
  check in 18 months.
- "We tried AI but it gave bad answers" — because the data underneath
  is bad.

## Required inputs from customer
- Raw datasets (CSV / Excel / CRM export / sheet links).
- A description of what each dataset is for and who owns it.
- Source attribution for each record (or willingness to mark unknown
  rows as research-only).
- Lawful basis declaration (per `docs/governance/PDPL_DATA_RULES.md` §3.1).
- Access tier per dataset (All Staff / Department / Restricted).
- PII / special-category acknowledgement when HR, health, or financial
  records are in scope.

## AI functions that build this capability
- Data quality scoring (`dealix/quality/data_quality_score.py`) —
  per-row and per-dataset score across completeness, validity, freshness,
  consistency, uniqueness.
- Saudi entity normalization — bilingual matcher (AR/EN spellings, CR
  numbers, common abbreviations) that collapses duplicates without
  hallucinating mergers.
- Dedupe with explainable match keys (no silent merges).
- PII detection (`dealix/trust/pii_detector.py`) — Saudi mobile, National
  ID, IBAN, card; card and IBAN are auto-BLOCKED from any downstream
  output (per Runtime Governance Check 2).
- Source attribution backfill — pulls origin metadata where available;
  flags the rest as `research-only`.
- Freshness scoring — last-touched date per record vs. dataset SLA.
- Forecasting & scoring (downstream) — once the data is clean, propensity
  / lead scoring / churn risk models can run with confidence intervals
  the customer trusts.

## Governance controls (binding)
- **No data without source** — records without provenance are quarantined,
  not deleted. They become research-only and never enter outreach drafts,
  reports, or training corpora (per `docs/governance/RUNTIME_GOVERNANCE.md`
  Check 1).
- PII detection runs **before** any indexing, scoring, or sharing — not
  after (per `docs/governance/PII_REDACTION_POLICY.md`).
- Card and IBAN data: hard `BLOCKED` verdict, no override
  (per `docs/governance/FORBIDDEN_ACTIONS.md` §3.3).
- Lawful basis tag required per dataset before processing
  (per `docs/governance/PDPL_DATA_RULES.md` §3.1).
- Cross-border transfers only via the documented PDPL Art. 18 bases.
- Dedupe decisions logged with the match key — every merge is auditable.
- No training on customer data; no sharing with third-party LLM training
  pipelines.

## KPIs (measured before/after)
- Data quality score (0–100, per dataset, with sub-scores).
- Duplicate rate before/after (% records collapsed).
- PII exposure: count of unredacted PII fields detected and redacted.
- Source attribution coverage (% records with verified provenance).
- Freshness: median age of last touch.
- Records moved out of `research-only` (data became usable).
- Downstream effect: scoring model AUC improvement after cleanup.

## Maturity ladder (per `docs/company/CAPABILITY_OPERATING_MODEL.md`)
- **Level 0** — data scattered across personal drives; no inventory.
- **Level 1** — datasets exist but no quality measurement, no dedupe,
  no PII triage.
- **Level 2** — data inventory documented; owner per dataset; PDPL
  lawful basis tagged.
- **Level 3** — cleanup + dedupe + PII pass run once
  (Data Readiness Assessment + Data Cleanup & Unification).
- **Level 4** — quality dashboard live; freshness SLAs enforced;
  monthly re-clean cadence (AI Business Dashboard + Forecasting & Scoring).
- **Level 5** — Data OS: continuous quality monitoring, model-grade
  features, automated PII gate, customer team self-serves.

## Dealix services that build / advance this capability
| Service | Lifts capability from → to | Indicative price |
|---------|----------------------------|------------------|
| AI Ops Diagnostic | n/a → measured baseline | SAR 7,500–25,000 |
| Data Readiness Assessment | L0–L1 → L2 | scoped (Phase 2) |
| Data Cleanup & Unification | L1–L2 → L3 | scoped per dataset volume |
| AI Business Dashboard | L3 → L4 | scoped (Phase 2) |
| Forecasting & Scoring | L3 → L4 | scoped per model |
| Data OS Retainer | L3 → L4–L5 | Phase 3+ |

Status note: Data Readiness Assessment and AI Business Dashboard are
currently in the Phase-2 / Designed bucket of
`docs/company/SERVICE_REGISTRY.md` and the Data Capability Package in
`docs/company/CAPABILITY_PACKAGES.md`. The AI Ops Diagnostic
(SAR 7,500–25,000, Sellable today) is the entry door — it produces the
Data Readiness Review and recommends the right next Sprint.

## Agents involved (per `docs/product/AI_AGENT_INVENTORY.md`)
- **DataQualityAgent** — autonomy level 1; runs quality scoring,
  dedupe candidates, PII flags, source attribution checks. Read/write on
  `data_os` modules. Status: MVP.
- **ComplianceGuardAgent** — mandatory gate. Confirms lawful basis,
  blocks card/IBAN passthrough, enforces source check (per
  `docs/governance/RUNTIME_GOVERNANCE.md`).
- (Downstream) **RevenueAgent / KnowledgeAgent / ReportingAgent** — all
  consume cleaned datasets; they refuse to operate on `research-only`
  records.

## Proof types produced
- **Quality Proof** — data quality score delta (before/after), duplicate
  rate cut, source-coverage lift. This is the headline.
- **Risk Proof** — PII redaction count, card/IBAN blocks logged, lawful-
  basis tags applied, PDPL Art. 13 acknowledgements captured (per
  `docs/governance/AUDIT_LOG_POLICY.md`).
- **Time Proof** — analyst-hours saved per month on manual cleanup once
  the pipeline is in place.
- **Revenue Proof (downstream)** — pipeline value identified once the
  scored, deduped account list flows into the Revenue Capability.

## Saudi-specific notes
- Saudi entity normalization handles AR/EN bilingual records, the common
  spellings of major holdings (Aramco, SABIC, STC, Almarai, etc.), and CR
  numbers as a stable join key.
- PDPL Art. 5 lawful-basis tagging is enforced at ingest — not retro-fitted.
- ZATCA-relevant fields (VAT numbers, invoice records) stay with the
  customer as record owner; Dealix never becomes the data controller.
- Kingdom Residency option (Enterprise plan) pins all processing to
  Kingdom-eligible regions per `docs/governance/PDPL_DATA_RULES.md` §3.4.
- Bilingual deliverables: cleanup report and quality scoreboard ship in
  AR/EN side-by-side.

## Cross-links
- `docs/services/ai_ops_diagnostic/offer.md`
- `docs/company/CAPABILITY_OPERATING_MODEL.md`
- `docs/company/AI_CAPABILITY_FACTORY.md`
- `docs/company/CAPABILITY_PACKAGES.md`
- `docs/company/VALUE_REALIZATION_SYSTEM.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/governance/PDPL_DATA_RULES.md`
- `docs/governance/PII_REDACTION_POLICY.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/governance/DATA_RETENTION.md`
