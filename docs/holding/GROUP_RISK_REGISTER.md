# Group Risk Register — Dealix Group

> Machine-readable mirror: `data/group_risk_register.json`.
> Reviewed quarterly. Each entry has owner, likelihood, impact,
> mitigation, status, last reviewed.

## Risk Categories

1. **Commercial** — pipeline, retention, sales-motion failure.
2. **Operational** — delivery, founder bandwidth, hiring, runway.
3. **Regulatory** — PDPL, SDAIA guidance, cross-border data.
4. **Agentic-AI-specific** — agent identity gaps, prompt injection,
   tool misuse, doctrine drift.

## Top Risks (Initial Register)

| # | Category | Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|:---:|:---:|---|:---:|
| 1 | Commercial | Founder-bottleneck on sales (single-channel) | high | high | `docs/funding/FIRST_3_HIRES.md` Hire #2 trigger; partner-kit (PR8) | open |
| 2 | Commercial | Anchor partner doesn't sign LOI in 90 days | med | high | Multiple archetypes in `data/anchor_partner_pipeline.json` | open |
| 3 | Operational | Founder bandwidth | high | high | Daily routine (PR2); marker-honesty CLIs (PR3) | mitigated |
| 4 | Operational | Runway dips below stage floor | med | high | `operating_finance_os/budget_stage.py` gate; quarterly review | open |
| 5 | Regulatory | PDPL breach via uncontrolled AI run | low | critical | Source Passport + Governance OS (Wave 19) | mitigated |
| 6 | Regulatory | Cross-border data transfer in GCC expansion | med | high | `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` + per-country trust framework | open |
| 7 | Agentic-AI | Prompt-injection escalating agent privileges | med | critical | Agent identity card + kill switch (Wave 19 PR3); `tests/test_agent_requires_identity_card.py` | mitigated |
| 8 | Agentic-AI | Tool misuse by autonomous agent | low | high | No external action without approval (doctrine #2) | mitigated |
| 9 | Agentic-AI | Doctrine drift over time | low | high | Doctrine versioning (PR7) + CI gate (PR4) | mitigated |
| 10 | Operational | Single point of failure (founder unavailable) | low | critical | Operating manual = the repo + `docs/ops/CONTINUOUS_ROUTINE.md` | open |
| 11 | Commercial | Customer demands forbidden feature | med | high | `WHAT_DEALIX_REFUSES.md` + scope kickoff (PR3 `sprint_kickoff.py`) | mitigated |
| 12 | Operational | Verifier drift (file PASS without real signal) | low | high | Honest-marker tests (PR4) + content-aware checks (Wave 19) | mitigated |

## Quarterly Review Process

1. Owner updates `status` for each risk.
2. New risks appended (never deleted; status `closed` instead).
3. Review summary stored in `data/_state/risk_reviews/<YYYY-Qn>.md`.
4. Material changes propagate into the next annual report.

## Verification

- `tests/test_group_risk_register_completeness.py` — every entry in
  `data/group_risk_register.json` has all 7 required fields.
- The annual report (PR12) reads the qualitative risk summary into
  Section 8.
