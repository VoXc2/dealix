# Governance as Code

> Governance documents tell humans what to do. Governance-as-Code makes
> the same rules **executable** — checked at runtime, not at quarterly
> audits. Phase 2 milestone: every governance rule in `docs/governance/`
> has an executable counterpart in `governance_os/rules/*.yaml`.

## The principle

A rule in a markdown file that no code enforces is a rule waiting to be broken. Dealix encodes its non-negotiables as rules that the Governance OS evaluates at every workflow run.

## Rule examples (executable form)

### `no_cold_whatsapp.yaml`

```yaml
rule: no_cold_whatsapp
description: Block WhatsApp sends to contacts without consent or prior relationship.
when:
  - action.channel == "whatsapp"
  - contact.relationship_status not in ["consented", "existing_customer"]
then:
  decision: BLOCK
  message_en: "WhatsApp requires Art. 14 consent or an existing relationship."
  message_ar: "WhatsApp يتطلب موافقة (المادة 14) أو علاقة قائمة."
  escalate: head_of_cs
```

### `no_guaranteed_claims.yaml`

```yaml
rule: no_guaranteed_claims
description: Block outputs containing guaranteed-outcome language.
when:
  - output.text matches /\bguarantee\w*\b|\bنضمن\b|\b100\%\s+\w+|\brisk[- ]free\b/i
then:
  decision: REWRITE_OR_BLOCK
  detector: dealix/trust/forbidden_claims.py
```

### `no_source_no_answer.yaml`

```yaml
rule: no_source_no_answer
description: Knowledge OS must refuse when no qualifying source exists.
when:
  - action.kind == "knowledge_answer"
  - retrieved_sources.count == 0 OR retrieved_sources.max_confidence < confidence_floor
then:
  decision: INSUFFICIENT_EVIDENCE
  response_en: "insufficient evidence — no qualifying source in the knowledge base."
  response_ar: "لا توجد أدلة كافية في القاعدة المعرفية."
```

### `pii_redaction_required.yaml`

```yaml
rule: pii_redaction_required
description: Redact PII (or block) before any output that crosses a customer boundary.
when:
  - output.destination in ["customer_report", "external_message", "public"]
  - pii_scan.has_pii == true
then:
  decision: REDACT
  detector: dealix/trust/pii_detector.py
  exceptions:
    - lawful_basis_recorded == true
```

### `data_source_required.yaml`

```yaml
rule: data_source_required
description: Records without source provenance cannot drive outbound actions.
when:
  - record.source is empty
  - downstream_action in ["outbound", "external_export"]
then:
  decision: QUARANTINE_RESEARCH_ONLY
  detector: auto_client_acquisition/customer_data_plane/validation_rules.py
```

### `approval_for_external_action.yaml`

```yaml
rule: approval_for_external_action
description: Any AI-initiated external action requires the named approver per Approval Matrix.
when:
  - action.level in [4, 5]   # per docs/governance/RUNTIME_GOVERNANCE.md AI Action Taxonomy
then:
  decision: REQUIRE_APPROVAL
  approver_resolver: dealix/trust/approval_matrix.required_approver(action, evidence_level)
```

## Engine

Planned at `auto_client_acquisition/governance_os/engine.py`:

```python
def evaluate(action: Action, context: Context) -> GovernanceDecision:
    for rule in load_rules("governance_os/rules/*.yaml"):
        if rule.when_matches(action, context):
            decision = rule.then_decision()
            audit_log.append(action, rule, decision)
            return decision
    return GovernanceDecision.ALLOW
```

This is **Phase 2 work**. Phase 1 uses Python-coded rules in `dealix/trust/*.py` (already shipped). The YAML form makes rules portable, reviewable by non-engineers, and auditable.

## Why YAML and not code only

- **Reviewability**: HoLegal can read the rule without reading Python.
- **Versionability**: each rule has its own file + git history.
- **Auditability**: customer asks "show me the rule that blocked this" — point to a file.
- **Portability**: rules can be sold (e.g., a customer in BFSI may want their own rule pack).

## Cross-links
- `docs/governance/RUNTIME_GOVERNANCE.md` — the 8 runtime checks
- `docs/governance/FORBIDDEN_ACTIONS.md` — declarative list
- `docs/governance/APPROVAL_MATRIX.md` — action × evidence → approver
- `dealix/trust/forbidden_claims.py` — Phase-1 Python enforcement
- `dealix/trust/approval_matrix.py` — Phase-1 Python enforcement
- `dealix/trust/pii_detector.py` — Phase-1 Python enforcement
