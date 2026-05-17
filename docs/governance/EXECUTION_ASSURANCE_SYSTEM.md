# Execution Assurance System — نظام ضمان التنفيذ

> Dealix sells *governed execution*. If our own automation runs without
> evidence, approvals, or tests, we break the company's promise. The
> Execution Assurance System is how Dealix proves — to itself — that every
> machine actually works.
>
> ديالكس تبيع "تنفيذاً محوكماً". لا تُعتبر أي أتمتة ناجحة لأنها اشتغلت مرة.
> تُعتبر ناجحة فقط إذا باعت، خدمت، التزمت بالحوكمة، سجّلت الدليل، وكشفت
> أخطاءها قبل العميل.

---

## 1. The format — الصيغة الحاكمة

Every machine passes through one fixed loop:

```
Strategy → System → Scorecard → Tests → Audit → Weekly CEO Review → Improvement Loop
```

Nothing is "done" because it ran once. A machine is done only when it
**sells, serves, obeys governance, records evidence, and surfaces its own
failures before a customer does.**

Every machine declares, in the registry:

- a clear **goal** — هدف واضح
- clear **inputs** and **outputs** — مدخلات ومخرجات واضحة
- a clear **owner** — مالك واضح
- clear **KPIs** — قياسات واضحة
- clear **tests** — اختبارات واضحة
- clear **failure modes** — حالات فشل واضحة
- **approval at the point of risk** — موافقة عند الخطر
- **evidence for every event** — دليل لكل حدث

---

## 2. The ten machines — الماكينات العشر

| Machine | الماكينة | Target | Owner |
|---|---|---|---|
| Sales Autopilot | مبيعات | 4/5 | founder |
| Support Autopilot | دعم | 4/5 | founder |
| Marketing Factory | تسويق | 3/5 | founder |
| Affiliate Machine | أفلييت | 4/5 | founder |
| Partner Channel | شركاء | 3/5 | founder |
| Media Engine | إعلام | 3/5 | founder |
| Delivery Factory | تسليم | 4/5 | founder |
| Billing Ops | فوترة | 4/5 | founder |
| Governance Layer | حوكمة | 5/5 | founder |
| Evidence Ledger | سجل الأدلة | 5/5 | founder |

The single source of truth is
[`dealix/registers/machine_registry.yaml`](../../dealix/registers/machine_registry.yaml).
Update by editing the YAML and opening a PR — never edit the Python.

---

## 3. The maturity ladder — سلّم النضج (0–5)

| Level | Meaning | المعنى |
|---|---|---|
| 0 | Absent | غير موجودة |
| 1 | Manual — run by hand | يدوية |
| 2 | Partial — templates, not automated | جزئية مع قوالب |
| 3 | Automated — runs internally | مؤتمتة داخلياً |
| 4 | Governed — automated + measured + approvals | محكومة |
| 5 | Self-improving — learns from failure | تتحسن ذاتياً |

**No fake green.** A Definition-of-Done item may only be marked `met: true`
if it carries a concrete `evidence_ref`. A docs-only machine scores 1, not
green — Marketing, Affiliate, and Media Engine are honestly at level 1
today. The scorecard cross-checks the declared score against
Definition-of-Done completion and flags any inconsistency.

---

## 4. The scorecard — لوحة القياس

`auto_client_acquisition/execution_assurance_os/` computes:

- **`score_machine`** — an honest 0–5 maturity score per machine, with a
  consistency flag (declared score vs. Definition-of-Done completion).
- **`aggregate_score`** — a portfolio score and readiness label.
- **`build_full_ops_health`** — the Full Ops Health dashboard: one row per
  machine plus the 10 portfolio KPIs.

The legacy `full_ops_radar` score (a binary "does the module import?"
proxy) is superseded: `compute_full_ops_score()` now also surfaces the
canonical, evidence-attested score under the `execution_assurance` key.

The 10 portfolio KPIs, and the one that matters most:

- Lead capture success rate — 95%+
- Lead scoring coverage — 100%
- Qualified lead response time — <24h
- Meeting brief generation rate — 100%
- Scope-to-invoice / invoice-to-paid conversion — tracked
- Support auto-resolution rate — 40–60%
- Support escalation accuracy — 100%
- Approval compliance rate — 100%
- Evidence completeness score — 90%+
- **High-risk auto-send — 0%.** Any non-zero value is a trust failure.

---

## 5. The tests — الاختبارات

`tests/assurance/` red-teams the machines (contract-style, CI-safe):

- **`test_registry_invariants.py`** — the fake-green tripwire: 10 machines,
  scores in range, no `met: true` without evidence, owners present,
  docs-only machines score honestly low.
- **`test_red_team_machines.py`** — the 8 red-team tests: Lead test,
  Qualified-lead test, Low-fit test, Support low-risk, Support high-risk,
  Affiliate compliance, Invoice guard, Revenue guard.
- **`test_agent_red_team.py`** — no never-auto-execute action can
  auto-execute; every high-risk action routes to human approval.

Run them: `pytest tests/assurance/ -q`.

---

## 6. The audit — التدقيق

`scripts/monthly_quality_audit.py` reconciles the registry's declared
Definition-of-Done claims against what the Evidence Ledger actually
contains. A machine claiming Automated maturity while its expected
evidence is entirely absent is flagged as a **contradiction**.

---

## 7. The Weekly CEO Review — مراجعة الرئيس التنفيذي الأسبوعية

`scripts/weekly_ceo_review.py` prints the founder's 12 standing questions
— with what the system can already answer pre-filled — the machines below
their acceptance gate, and the standing weekly decision:

> Double down · Fix bottleneck · Kill channel · Improve message ·
> Improve proof asset · Improve KB · Improve agent guardrail · No-build ·
> Build only a repeated workflow.

---

## 8. The improvement loop — حلقة التحسين

The acceptance gates (`GET /api/v1/execution-assurance/acceptance-gate`)
define what "ready to scale" means. A machine passes its gate only when it
has reached its target maturity **and** every Definition-of-Done item is
met. Anything less is reported with concrete unmet reasons.

Each week the funnel question — *is the problem in the build, the message,
the market, or the proof?* — routes to one decision. Build only a
repeated, paid workflow; otherwise fix, sell, or kill.

---

## 9. API surface

Read-only, under `/api/v1/execution-assurance/`:

| Endpoint | Returns |
|---|---|
| `GET /status` | registry validity + maturity ladder |
| `GET /scorecard` | portfolio + per-machine maturity scores |
| `GET /health` | Full Ops Health dashboard |
| `GET /acceptance-gate` | per-machine gate pass/fail + unmet reasons |
| `GET /machines/{id}` | one machine: score, DoD, gate, failure modes |

---

## See also

- [`docs/company/DEFINITION_OF_DONE.md`](../company/DEFINITION_OF_DONE.md)
  — the service / project / feature Definition of Done.
- [`dealix/registers/machine_registry.yaml`](../../dealix/registers/machine_registry.yaml)
  — the source of truth.
- [`dealix/registers/no_overclaim.yaml`](../../dealix/registers/no_overclaim.yaml)
  — every public claim, tracked with evidence.
