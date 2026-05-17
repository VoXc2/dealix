# 08 — الأتمتة ومصفوفة الموافقات / Automation & Approval Matrix

## العربية

### ثلاث طبقات أتمتة

**Autopilot** — يشتغل بدونك:
capture lead · create CRM record · score lead · assign stage · create next
action · log evidence · generate brief · generate draft · schedule reminder.

**Copilot** — يقترح عليك:
best message · recommended offer · price tier · meeting questions · scope
draft · invoice draft · upsell path.

**Founder Approval** — لا يتم إلا بموافقتك:
external send · invoice send · final diagnosis · security claim · case study ·
agent action · public proof.

> هذا ليس ضعف أتمتة — هو **جزء من القيمة**. السوق يتجه إلى agentic AI،
> والتحدي الأكبر صار governance و accountability و auditability ووضوح مالك
> القرار.

### الـ 18 أتمتة

| # | المُطلِق | السلسلة | الطبقة |
|---|---|---|---|
| 1 | New lead | form → CRM contact → company → score → stage → first draft → evidence: lead_captured | Autopilot |
| 2 | Proof Pack request | request → send asset *if consent exists* → log event → follow-up in 2 days | Autopilot¹ |
| 3 | High score lead | score ≥ 15 → task: approve booking invite → meeting brief → notify Sami | Copilot |
| 4 | Partner lead | partner signal → partner sequence → referral terms draft → partner call task | Copilot |
| 5 | Meeting booked | booking → CRM meeting_booked → pre-call brief → discovery questions → demo path | Autopilot |
| 6 | Meeting reminder | 24h before → prep reminder → lead context → suggested opening | Autopilot |
| 7 | Meeting done | Sami marks done → ask 5 fields → classify outcome → scope or nurture | Copilot |
| 8 | Scope requested | scope_requested → generate scope → recommend price → invoice draft → approval task | Copilot |
| 9 | Scope sent | scope approved → send scope → follow-up timer → evidence: scope_sent | Founder approval |
| 10 | Invoice sent | invoice approved → send invoice/payment link → evidence: invoice_sent | Founder approval |
| 11 | Invoice paid | payment confirmed → delivery folder → onboarding form → checklist → evidence: invoice_paid | Autopilot |
| 12 | Onboarding submitted | inputs received → missing-info check → diagnostic workplan → proof pack shell | Autopilot |
| 13 | Proof pack draft | analysis done → draft proof pack → founder review → client delivery task | Copilot |
| 14 | Proof pack delivered | final approved → send pack → evidence: proof_pack_sent → upsell recommendation | Founder approval |
| 15 | Upsell candidate | value confirmed → Sprint proposal → Retainer option → approval task | Copilot |
| 16 | Testimonial/referral | positive feedback → ask permission → testimonial request → referral ask draft | Copilot |
| 17 | Nurture | not ready → sequence by objection → educational asset → reactivation task | Autopilot |
| 18 | Weekly CEO review | Friday → pipeline report → blockers → conversion rates → next best actions → no-build warning | Autopilot |

¹ الإرسال التلقائي للـ Proof Pack مسموح **فقط** إذا سُجّل consent عبر النموذج؛
وإلا فهو مسودة بموافقة المؤسس.

### مصفوفة الموافقات

| الإجراء | مؤتمت؟ | يحتاج Sami؟ | السبب |
|---|---|---|---|
| Create CRM contact | نعم | لا | داخلي |
| Score lead | نعم | لا | داخلي |
| Draft message | نعم | لا | مسودة |
| Send cold message | لا | **نعم** | فعل خارجي |
| Send proof pack بعد consent | نعم | مراجعة أولية فقط | منخفض المخاطر |
| Send invoice | لا | **نعم** | التزام مالي |
| Mark revenue | لا | **نعم + payment proof** | لا revenue قبل دفع |
| Publish case study | لا | **نعم + client approval** | ثقة وقانون |
| Make security claim | لا | **نعم + evidence** | خطر عالٍ |
| Final diagnostic conclusion | لا | **نعم** | جودة وثقة |

### الربط بالنظام

- مصفوفة الموافقات منفّذة في `governance_os/approval_policy.py` و `approval_center/`.
- القواعد الصارمة في `auto_client_acquisition/safe_send_gateway/doctrine.py`.
- الـ 18 أتمتة هي **تنسيق (orchestration)** فوق ما هو مبني — تُبنى في
  **المرحلة 5** من `ENGINEERING_ROADMAP.md`. كل فعل خارجي يبقى **مسودة +
  بوابة موافقة**.

---

## English

### Three automation tiers

**Autopilot** — runs without you:
capture lead · create CRM record · score lead · assign stage · create next
action · log evidence · generate brief · generate draft · schedule reminder.

**Copilot** — suggests to you:
best message · recommended offer · price tier · meeting questions · scope
draft · invoice draft · upsell path.

**Founder Approval** — only happens with your approval:
external send · invoice send · final diagnosis · security claim · case study ·
agent action · public proof.

> This is not weak automation — it is **part of the value**. The market is
> moving to agentic AI, and the bigger challenge is now governance,
> accountability, auditability, and clarity of who owns the decision.

### The 18 automations

| # | Trigger | Chain | Tier |
|---|---|---|---|
| 1 | New lead | form → CRM contact → company → score → stage → first draft → evidence: lead_captured | Autopilot |
| 2 | Proof Pack request | request → send asset *if consent exists* → log event → follow-up in 2 days | Autopilot¹ |
| 3 | High score lead | score ≥ 15 → task: approve booking invite → meeting brief → notify Sami | Copilot |
| 4 | Partner lead | partner signal → partner sequence → referral terms draft → partner call task | Copilot |
| 5 | Meeting booked | booking → CRM meeting_booked → pre-call brief → discovery questions → demo path | Autopilot |
| 6 | Meeting reminder | 24h before → prep reminder → lead context → suggested opening | Autopilot |
| 7 | Meeting done | Sami marks done → ask 5 fields → classify outcome → scope or nurture | Copilot |
| 8 | Scope requested | scope_requested → generate scope → recommend price → invoice draft → approval task | Copilot |
| 9 | Scope sent | scope approved → send scope → follow-up timer → evidence: scope_sent | Founder approval |
| 10 | Invoice sent | invoice approved → send invoice/payment link → evidence: invoice_sent | Founder approval |
| 11 | Invoice paid | payment confirmed → delivery folder → onboarding form → checklist → evidence: invoice_paid | Autopilot |
| 12 | Onboarding submitted | inputs received → missing-info check → diagnostic workplan → proof pack shell | Autopilot |
| 13 | Proof pack draft | analysis done → draft proof pack → founder review → client delivery task | Copilot |
| 14 | Proof pack delivered | final approved → send pack → evidence: proof_pack_sent → upsell recommendation | Founder approval |
| 15 | Upsell candidate | value confirmed → Sprint proposal → Retainer option → approval task | Copilot |
| 16 | Testimonial/referral | positive feedback → ask permission → testimonial request → referral ask draft | Copilot |
| 17 | Nurture | not ready → sequence by objection → educational asset → reactivation task | Autopilot |
| 18 | Weekly CEO review | Friday → pipeline report → blockers → conversion rates → next best actions → no-build warning | Autopilot |

¹ Auto-sending the Proof Pack is allowed **only** if consent was recorded via
the form; otherwise it is a draft requiring founder approval.

### The approval matrix

| Action | Automated? | Needs Sami? | Reason |
|---|---|---|---|
| Create CRM contact | Yes | No | Internal |
| Score lead | Yes | No | Internal |
| Draft message | Yes | No | A draft |
| Send cold message | No | **Yes** | External action |
| Send proof pack after consent | Yes | Initial review only | Low risk |
| Send invoice | No | **Yes** | Financial commitment |
| Mark revenue | No | **Yes + payment proof** | No revenue before payment |
| Publish case study | No | **Yes + client approval** | Trust and legal |
| Make security claim | No | **Yes + evidence** | High risk |
| Final diagnostic conclusion | No | **Yes** | Quality and trust |

### How it connects to the system

- The approval matrix is implemented in `governance_os/approval_policy.py` and
  `approval_center/`.
- The hard rules live in `auto_client_acquisition/safe_send_gateway/doctrine.py`.
- The 18 automations are **orchestration** on top of what is already built —
  built in **Phase 5** of `ENGINEERING_ROADMAP.md`. Every external action stays
  a **draft + approval gate**.
