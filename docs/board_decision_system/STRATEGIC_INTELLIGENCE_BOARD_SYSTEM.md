# Dealix Strategic Intelligence & Board Decision System

## Purpose | الغرض

Dealix لا تكتفي بجمع **إشارات** وتشغيل وProof. هذه الطبقة تحوّل التشغيل إلى **قرارات CEO/Board**: ماذا نبيع، ماذا نبني، ماذا نوقف، أين نرفع السعر، وأي وحدة نجهّزها لتصبح Venture.

## North-star loop | حلقة الشمال

```text
Signals → Decisions → Actions → Proof → Learning
```

## Implementation | التنفيذ في الكود

- Python package: `auto_client_acquisition/board_decision_os/`
- Read API (deterministic, no LLM required): `GET/POST /api/v1/board-decision-os/*`

## External context (informational) | سياق خارجي (معلوماتي)

- Enterprise AI adoption vs strategy/ROI gap is widely reported in trade press (e.g. [IT Pro — AI adoption and strategy](https://www.itpro.com/business/business-strategy/ai-adoption-projects-keep-failing-but-enterprise-fomo-means-investment-is-still-rising)).
- Operational AI + security posture themes appear in industry summaries (e.g. [TechRadar — KPMG AI operational reality](https://www.techradar.com/pro/ai-is-no-longer-a-future-concept-but-an-operational-reality-new-kpmg-report-claims-firms-are-racing-to-deploy-ai-but-need-to-ensure-they-have-the-right-security-protections)).
- Agent identity / accountability research direction: [arXiv:2604.23280](https://arxiv.org/abs/2604.23280).
- Saudi national GenAI survey themes: [arXiv:2601.18234](https://arxiv.org/abs/2601.18234).
- Saudi AI infrastructure initiative (context): [Wikipedia — HUMAIN](https://en.wikipedia.org/wiki/Humain).

Dealix product stance remains: **Saudi Governed AI Operations OS** — not a generic chatbot vendor.

## Doc map | خريطة الوثائق

| Document | Focus |
|----------|--------|
| [BOARD_DECISION_LOOP.md](./BOARD_DECISION_LOOP.md) | Collect → score → options → execute → proof |
| [DECISION_TYPES.md](./DECISION_TYPES.md) | Scale / Build / Hold / Kill patterns |
| [BOARD_SCORECARDS.md](./BOARD_SCORECARDS.md) | Offer / Client / Productization weights |
| [CEO_COMMAND_CENTER.md](./CEO_COMMAND_CENTER.md) | Top-5 decisions view |
| [BOARD_MEMO_AUTOMATION.md](./BOARD_MEMO_AUTOMATION.md) | Monthly board memo sections |
| [STRATEGIC_BETS_FRAMEWORK.md](./STRATEGIC_BETS_FRAMEWORK.md) | 1–3 bets / month |
| [AGENT_DECISION_GOVERNANCE.md](./AGENT_DECISION_GOVERNANCE.md) | Stricter gate for agents |
| [SAUDI_BOARD_VIEW.md](./SAUDI_BOARD_VIEW.md) | PDPL, Arabic QA, WhatsApp boundaries |
| [MARKET_TIMING_BOARD_VIEW.md](./MARKET_TIMING_BOARD_VIEW.md) | Positioning vs generic AI |
| [BOARD_RISK_DECISIONS.md](./BOARD_RISK_DECISIONS.md) | Risk → decision mapping |
| [CAPITAL_ALLOCATION_BOARD.md](./CAPITAL_ALLOCATION_BOARD.md) | Must fund / test / hold / kill |

## Closing sentence | الجملة الختامية

> Dealix تفوز عندما لا يكون عندها فقط بيانات وتشغيل، بل **نظام قيادة**: يقرأ الإشارات، يختار الرهانات، يرفض الإيراد السيئ، يبني فقط ما يتكرر، ويحوّل كل Proof إلى قرار استراتيجي يقرّب الشركة من كونها **Saudi Governed AI Operations OS**.
