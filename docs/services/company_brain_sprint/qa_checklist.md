# Company Brain Sprint — QA Checklist

## Business QA
- [ ] Sample answers solve real employee questions (verified on the 10 intake samples).
- [ ] Search-time reduction measured (before/after).
- [ ] Customer can articulate the business win in one sentence.

## Data QA
- [ ] Document inventory complete and owners attributed.
- [ ] PII detected via `dealix/trust/pii_detector.py` before indexing.
- [ ] Sensitive docs flagged and access-restricted.
- [ ] Freshness report present (auto-flag > 90 days).

## AI QA
- [ ] ≥ 95% of test answers carry a verifiable citation.
- [ ] "no source = no answer" rule enforced — verified on 3 questions outside the corpus.
- [ ] No PII surfaced in any answer.
- [ ] AR/EN tone appropriate.
- [ ] Eval cases pass: latest-doc citation, restricted-content blocking, multi-source synthesis.

## Compliance QA
- [ ] Access rules enforced (verified across 3 personas).
- [ ] Audit log records every query + retrieval.
- [ ] Right-to-erasure path tested (delete one doc → re-test answers).

## Delivery QA
- [ ] Training session recorded.
- [ ] Admin guide present.
- [ ] Customer team confirms self-service usability.
- [ ] Renewal proposal (Sales Knowledge Assistant / Policy Assistant) drafted.

Floor: Quality Score ≥ 80 to ship.
