# Dealix Operating Kernel

**Dealix لا تدار بالنوايا. تدار بالبوابات، الأدلة، السكورات، والقرارات.**

سياق البيانات والتشغيل: [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

## Core rule

لا تُباع ولا تُسلّم ولا تُوسَّع خدمة إلا بعد اجتياز البوابات المطلوبة — [`DECISION_RULES.md`](DECISION_RULES.md)، [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md)، [`scripts/verify_dealix_ready.py`](../../scripts/verify_dealix_ready.py).

## Components

| # | Engine | Role | Doc / code |
|---|--------|------|------------|
| 1 | **Readiness Registry** | Sellable / Beta / Not Ready / Enterprise-only | [`SERVICE_READINESS_MATRIX.md`](SERVICE_READINESS_MATRIX.md), `verify_dealix_ready.py` |
| 2 | **Service Registry** | وعد، سعر، مدة، مخرجات، استثناءات، KPI، upsell | [`SERVICE_REGISTRY.md`](SERVICE_REGISTRY.md), [`SERVICE_ID_MAP.yaml`](SERVICE_ID_MAP.yaml) |
| 3 | **Delivery Engine** | intake → scope → data → build → QA → report → proof → next | `docs/delivery/*`, `docs/services/*/delivery_checklist.md` |
| 4 | **Quality Engine** | score قبل التسليم | [`QUALITY_REVIEW_BOARD.md`](../quality/QUALITY_REVIEW_BOARD.md), [`OUTPUT_QA_SCORECARD.md`](../quality/OUTPUT_QA_SCORECARD.md) |
| 5 | **Governance Engine** | منع المخاطر | `docs/governance/*`, `governance_os/` |
| 6 | **Proof Engine** | إثبات العمل والأثر | `reporting_os/proof_pack.py`, templates |
| 7 | **Sales Engine** | عرض، رسالة، upsell | `docs/sales/*` |
| 8 | **Learning Engine** | تكرار → أصول داخلية / features / playbooks | [`COMPOUNDING_SYSTEM.md`](COMPOUNDING_SYSTEM.md), [`FEATURE_CANDIDATE_LOG.md`](FEATURE_CANDIDATE_LOG.md), [`CONTENT_AND_LEARNING_LOOP_AR.md`](../strategy/CONTENT_AND_LEARNING_LOOP_AR.md) |

## Constitution stack

- [`DEALIX_READINESS.md`](../../DEALIX_READINESS.md)
- [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md)
- [`EVIDENCE_SYSTEM.md`](EVIDENCE_SYSTEM.md)
- [`OPERATING_SCORECARD.md`](OPERATING_SCORECARD.md)
- [`DEALIX_METHOD_AR.md`](DEALIX_METHOD_AR.md)

**The Day-7 control loop:** [`WEEKLY_OPERATING_REVIEW.md`](WEEKLY_OPERATING_REVIEW.md) + [`MATURITY_BOARD.md`](MATURITY_BOARD.md) + [`DECISION_OPERATING_SYSTEM.md`](DECISION_OPERATING_SYSTEM.md) + [`CLOSED_LOOP_EXECUTION.md`](CLOSED_LOOP_EXECUTION.md) + [`OPERATING_LEDGER.md`](OPERATING_LEDGER.md) / [`CONTROL_PLANE.md`](CONTROL_PLANE.md) + [`CAPABILITY_OPERATING_MODEL.md`](CAPABILITY_OPERATING_MODEL.md).

## Dealix Standard (external/internal one-liner)

1. Data Ready  
2. Process Clear  
3. Human Approved  
4. Source Grounded  
5. Quality Scored  
6. Governance Checked  
7. Proof Delivered  
8. Expansion Planned  
