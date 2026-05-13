# Dealix Operating Principles

Ten principles that cannot be violated. Every Pull Request, every SOW, every
AI output is graded against them. Violations escalate to CEO.

1. **Outcome before tools.** We sell results in SAR, time, quality, governance — not "AI access."
2. **No data without source.** Every record carries provenance or is flagged. No source = quarantined.
3. **No AI output without QA.** Every model output passes through schema validation + ComplianceGuard + a human reviewer when side-effects are involved.
4. **No external action without approval.** PDPL Art. 13/14 enforced before any outbound. Approval Matrix (`dealix/trust/approval_matrix.py`) is binding.
5. **No source = no answer.** Knowledge OS refuses to answer when no qualifying source exists. The assistant returns "insufficient evidence" rather than hallucinate.
6. **Every project ends with proof.** Stage 7 (Prove) is mandatory within 14 days of delivery. Captured into the Proof Ledger.
7. **Every repeated manual step becomes a product feature.** Rule: when an action is taken manually ≥ 2 times in real delivery, it is filed as a backlog item.
8. **Every service must have a measurable KPI.** "Better" without a number is not a deliverable. KPIs live in the SOW and in the Operating Scorecard.
9. **Arabic quality is a product feature.** Not "added at the end." AR tone, sector terms, bilingual outputs are validated in QA.
10. **Compliance is built into delivery.** Not a separate workstream. Every gate in the 5-gate Quality System has a Compliance check.

## Hard "no" list (forbidden actions enforced by `dealix/trust/forbidden_claims.py` + Governance OS)

- Web scraping without permission.
- Cold WhatsApp / SMS outreach.
- LinkedIn automation.
- Fabricated proof or fake testimonials.
- Guaranteed-outcome claims ("نضمن", "100%", "best in", "risk-free").
- PII in logs.
- Autonomous external communication.

## Owner & cadence
- **Owner**: CEO.
- **Review**: quarterly principle review; any proposed change requires CTO + HoLegal sign-off.

## Cross-links
- `docs/strategy/dealix_operating_partner_positioning.md`
- `docs/strategy/dealix_delivery_standard_and_quality_system.md`
- `docs/strategy/dealix_maturity_and_verification.md`
- `dealix/trust/forbidden_claims.py`
- `dealix/trust/approval_matrix.py`
