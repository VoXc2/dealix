# AI Quick Win Sprint — QA Checklist

## Business QA
- [ ] Time saved per run is measured (before vs after).
- [ ] Customer can articulate the value to their CEO in one sentence.
- [ ] Next-action recommendation captured.

## Data QA
- [ ] Inputs documented; PII flagged + redacted where needed.
- [ ] Source attribution for every input column.

## AI QA
- [ ] Output schema validated (Pydantic).
- [ ] No forbidden claims (auto-checked).
- [ ] Edge cases: empty input, malformed input, missing field.
- [ ] AR/EN outputs match in meaning where bilingual.

## Compliance QA
- [ ] Every side-effect action passes through `dealix/trust/approval_matrix.py`.
- [ ] Audit log records every run (`event_store.append_event`).
- [ ] No autonomous external communication.

## Delivery QA
- [ ] Runbook present, ≥ 3 pages.
- [ ] Training session recorded.
- [ ] Process owner can run the automation alone.
- [ ] Renewal proposal (Workflow Automation / Monthly AI Ops) drafted.

Floor: Quality Score ≥ 80 to ship.
