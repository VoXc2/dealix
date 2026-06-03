# Dealix — Founder Product Requirements

## الهدف

تحويل المنتج إلى نظام تشغيل يومي للمؤسس يربط revenue، pipeline، delivery، trust، وsystem health في تجربة واحدة.

## الشخصيات

| Persona | Needs |
|---|---|
| Founder | أين الإيراد؟ ما الخطر؟ ما القرار اليوم؟ |
| Sales operator | من أتابع؟ ماذا أرسل؟ ما الأولوية؟ |
| Delivery lead | ماذا وعدنا؟ ما الدليل؟ ما الحالة؟ |
| Admin/compliance | من وافق؟ ما السجل؟ ما المخاطر؟ |

## Core workflows

1. Founder daily command.
2. Account discovery and scoring.
3. Outreach package generation.
4. Diagnostic delivery.
5. Proposal creation.
6. Approval and audit trail.
7. Post-deploy and production evidence.

## MVP acceptance criteria

- كل opportunity لها status وnext action.
- كل high-risk action لها approval state.
- كل customer-facing artifact له evidence source.
- كل deploy له health proof.
- كل dashboard metric له source وowner.

## Product surfaces

| Surface | Purpose |
|---|---|
| Control plane | operational overview |
| Agents | AI recommendations and tasks |
| Approvals | human approval queue |
| Safety | claims, compliance, policy |
| Value engine | revenue and proof |
| Status | public/ops health |

## Non-functional requirements

- API health under 1 second for `/healthz`.
- Deep health reports dependency state.
- No public secret exposure.
- CI blocks broken Railway surfaces.
- All production changes have rollback path.
