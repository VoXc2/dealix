# AI Quick Win Sprint — Delivery Checklist (7 business days)

Day-by-day plan. Owner: HoCS. Counter-sign required at Day 3, Day 5, Day 7 gates. Quality Score >= 80 to ship.

## Day 1 — Discovery & Use-Case Lock / اليوم 1 — الاكتشاف والاختيار
- [ ] 30-min recorded discovery using `intake.md`.
- [ ] ONE use case selected from curated list — BINDING.
- [ ] Sample inputs/outputs received (5+5).
- [ ] Sealed-vault credentials opened (read-only first).
- [ ] PDPL Art. 5 lawful basis (contract) acknowledged.
- [ ] Stage-1 event: `discovery.completed`.

## Day 2 — Skeleton Build / اليوم 2 — الهيكل الأساسي
- [ ] Pipeline skeleton in customer environment.
- [ ] Input schema validated (Pydantic models).
- [ ] PII pass via `dealix/trust/pii_detector.py` configured.
- [ ] Audit-log writer wired (`event_store.append_event`) from minute zero.
- [ ] Dry-run on 3 sample inputs (no side-effects).

## Day 3 — Feedback Round 1 / اليوم 3 — جولة الملاحظات الأولى
- [ ] 45-min review with process owner.
- [ ] Output quality scored against the 5 desired outputs.
- [ ] Edge cases logged (empty input, malformed, missing field).
- [ ] Approval-matrix routing tested against `dealix/trust/approval_matrix.py`.
- [ ] Forbidden-claims auto-check enabled (`dealix/trust/forbidden_claims.py`).
- [ ] Gate #1 — mid-sprint checkpoint signed.

## Day 4 — Hardening / اليوم 4 — التقوية
- [ ] All 5 sample-output pairs match within tolerance.
- [ ] Edge-case handling implemented and tested.
- [ ] No autonomous external comms — every side-effect routes to approval.
- [ ] AR/EN parity check if outputs are bilingual.
- [ ] Performance: <= 30s per run on representative payload.

## Day 5 — Feedback Round 2 + Runbook Draft / اليوم 5 — الملاحظات والدليل
- [ ] 45-min review with process owner.
- [ ] Top-3 polish items implemented.
- [ ] Runbook drafted (>= 3 pages): how to run, what to monitor, when to escalate.
- [ ] Audit-log query snippet documented for the customer.
- [ ] Gate #2 signed.

## Day 6 — ROI Baseline + Internal QA / اليوم 6 — قياس العائد والـQA
- [ ] Before/after measurement on the last 30 runs of the process.
- [ ] Time-per-run, errors, hours-saved/week computed.
- [ ] Internal QA against `qa_checklist.md` — Quality Score >= 80.
- [ ] Proof pack assembled per `proof_pack_template.md`.

## Day 7 — Training & Handoff / اليوم 7 — التدريب والتسليم
- [ ] 1-hour recorded training session with the process owner.
- [ ] Customer self-runs the automation under observation.
- [ ] Renewal proposal (Workflow Automation / Monthly AI Ops) delivered — see `upsell.md`.
- [ ] Stage-6 event: `delivery.handoff_completed`.

## Hard stops during delivery
- Customer asks for autonomous external send -> pause, escalate to HoCS + CRO.
- Use case shifts mid-sprint -> stop, scope is binding from Day 1.
- PII surfaces in outputs unredacted -> halt, fix, re-verify before resume.

## Cross-links
- QA gates: `docs/services/ai_quick_win_sprint/qa_checklist.md`
- Report skeleton: `docs/services/ai_quick_win_sprint/report_template.md`
- Handoff packet: `docs/services/ai_quick_win_sprint/handoff.md`
- 8-stage state machine: `auto_client_acquisition/customer_loop/`
- Delivery standard: `docs/strategy/dealix_delivery_standard_and_quality_system.md`
