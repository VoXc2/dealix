# The Dealix Standard

The 8-standard manifesto. Every customer delivery must satisfy all eight, or
it does not ship under the Dealix name.

> **The phrase**: *Dealix delivers AI Operations through eight standards.
> No client delivery is complete unless all eight standards are satisfied.*

## The 8 standards

### 1. Data Ready
No AI implementation without a Data Readiness check.
- Source documented for every record.
- PII detected and (where required) redacted.
- Completeness, validity, uniqueness, freshness scored.
- Lawful basis under PDPL Art. 5 recorded.

### 2. Process Clear
No automation of an undefined process.
- Owner named.
- Inputs and outputs explicit.
- Error modes and recovery defined.
- KPI for success defined.

### 3. Human Approved
No external action without human approval per `dealix/trust/approval_matrix.py`.
- Outbound email → CSM/AE approves.
- WhatsApp / SMS → Head of CS + consent.
- Public claim → Head of Legal.
- External API write → CTO.
- Policy override → CEO only.

### 4. Source Grounded
In Knowledge OS: **no source = no answer**.
- Every answer returns `source_id`, `chunk_id`, `last_updated`.
- "Insufficient evidence" is a valid (and correct) response.

### 5. Quality Scored
Every output passes the 5-gate QA + 100-point Project Quality Score
(`auto_client_acquisition/delivery_factory/qa_review.py`). Floor: 80. Target: 85+.

### 6. Governance Checked
Every output passes through Governance OS:
- PII check (`dealix/trust/pii_detector.py`).
- Forbidden-claim filter (`dealix/trust/forbidden_claims.py`).
- Approval-matrix decision.
- Audit-event appended to immutable event store.

### 7. Proof Delivered
Every project closes with a Proof Pack (Stage 7 Prove) within 14 days of delivery.
- Inputs → processing → outputs → measured impact → next step.
- Anonymized copy added to `docs/assets/proof_packs/`.

### 8. Expansion Planned
Every project closes with a documented next step:
- Customer self-use plan, OR
- Pilot, OR
- Retainer, OR
- Enterprise upgrade conversation.

A documented "no, not now" still counts — the conversation must happen.

## Why this matters

Competitors sell tools. Dealix sells **outcomes under a standard**. When a
customer asks "how is this different from any AI agency?" the answer is the
8 standards — every one of them enforceable in code or in the operating
cadence, not just slogans.

## Cross-links

- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — operational detail per standard
- `docs/strategy/dealix_maturity_and_verification.md` — verification gates
- `docs/company/DECISION_RULES.md` — binding rules backed by these standards
- `docs/company/DEALIX_OPERATING_KERNEL.md` — runtime that enforces them
- `dealix/trust/policy.py`, `dealix/trust/approval_matrix.py`, `dealix/trust/forbidden_claims.py`, `dealix/trust/pii_detector.py` — code enforcement
- `auto_client_acquisition/delivery_factory/qa_review.py` — Quality scoring
- `auto_client_acquisition/revenue_memory/event_store.py` — append-only audit
