# Enterprise Maturity Model — نموذج النضج المؤسسي

> **The question is not "how many features?" — it is "can Dealix reliably and
> measurably operate an enterprise via AI-first workflows?"**
>
> السؤال ليس "كم feature عندنا؟" — السؤال: "هل Dealix قادر يشغّل مؤسسة عبر
> AI-first workflows بشكل موثوق وقابل للقياس؟"

This model measures **Dealix itself** as a platform. It is distinct from
[`CAPABILITY_MATURITY_MODEL.md`](CAPABILITY_MATURITY_MODEL.md), which scores a
*client's* capability. Canonical code: `auto_client_acquisition/enterprise_maturity_os/`.

## The 5 stages — المراحل الخمس

| Level | Stage | المرحلة |
|------:|-------|---------|
| 1 | AI Tool | أداة ذكاء اصطناعي — prompts و APIs، AI يجاوب فقط |
| 2 | AI SaaS Platform | منصة SaaS — auth، billing، workspaces، usage tracking |
| 3 | Enterprise AI Platform | منصة مؤسسية — tenant isolation، governance، retrieval، evaluation |
| 4 | Agentic Operating Platform | منصة تشغيل وكيلية — agents تنفّذ workflows، human فوق الحلقة، organizational memory |
| 5 | Agentic Enterprise Infrastructure | بنية تحتية وكيلية — Dealix كـ operating layer للمؤسسة، mission-critical |

Each stage carries `entry_signals` — the "how do you know you arrived" checklist.
See `stages.py`.

## The 10 readiness gates — بوابات الجاهزية

Each gate scores **0–100** from weighted boolean evidence (`readiness_gates.py`):

`architecture` · `security` · `governance` · `workflow` · `evaluation` ·
`operational` · `delivery` · `transformation` · `executive` · `scale`

### Score bands — نطاقات الدرجة

| Score | Band | المعنى |
|------:|------|--------|
| 0–59 | `prototype` | نموذج أولي |
| 60–74 | `internal_beta` | beta داخلي |
| 75–84 | `client_pilot` | جاهز لـ pilot مع عميل |
| 85–94 | `enterprise_ready` | جاهز للمؤسسات |
| 95+ | `mission_critical` | بنية حرجة |

## The 5 verification systems — أنظمة التحقق

Gates say what is *built*; verification systems prove it *works*
(`verification_systems.py`):

1. **Real Workflow Testing** — workflows كاملة، approvals، failures، retries، escalations
2. **Governance Validation** — approvals enforced، permissions، audit logs، policy bounds
3. **Operational Evaluations** — AI quality، grounding، workflow completion، business quality
4. **Enterprise Readiness Gates** — كل خدمة لها gate score مسجّل ومُلزَم
5. **Executive Proof System** — إثبات زيادة الإيراد، تقليل الوقت، تحسين العمليات

## How a stage is decided — كيف تُحسب المرحلة

`assess_platform_maturity()` (`maturity_assessment.py`) computes the mean gate
score and mean verification coverage, then promotes a stage **only when both
thresholds are met**:

| Target stage | Min mean gate score | Min mean verification |
|-------------:|--------------------:|----------------------:|
| 2 — AI SaaS Platform | 60 | 40 |
| 3 — Enterprise AI Platform | 75 | 60 |
| 4 — Agentic Operating Platform | 85 | 80 |
| 5 — Agentic Enterprise Infrastructure | 95 | 95 |

This is the core discipline: **high gate scores with weak verification cannot
promote a stage** — a feature collection is not an operational system.

## Reading an assessment — قراءة النتيجة

`GET /api/v1/maturity/current` scores Dealix against the honest baseline in
`maturity_baseline.yaml`:

- `current_stage` / `current_band` — where Dealix stands today
- `next_stage` — the stage being worked toward
- `blockers` — the exact gates/verification systems below the threshold for the
  next stage; this is the prioritized work list

Other endpoints: `GET /stages`, `GET /gates`, `GET /verification-systems`,
`POST /assess` (score arbitrary evidence).

Update `maturity_baseline.yaml` only when a capability is **real, tested, and
recorded** — never to flatter the score. لا تعدّل البيانات لتجميل النتيجة.
