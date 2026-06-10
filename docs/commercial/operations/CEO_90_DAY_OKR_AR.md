# CEO 90-Day OKR — Dealix Founder

> **Ref:** [NORTH_STAR_METRICS_AR.md](../NORTH_STAR_METRICS_AR.md) · `python scripts/run_ceo_master_plan_status.py`

## North Star (unchanged)

أول `payment_received` + `proof_pack_delivered` من عميل **non-network** = Phase 0–1 PASS.

---

## OKR 1 — إغلاق Phase 0–1 (Revenue Proof)

| Key result | Target | Evidence |
|------------|--------|----------|
| KR1 | Diagnostic مدفوع واحد (4999–15000 SAR) | `payment_received` في evidence_events_tracker.csv |
| KR2 | Proof Pack مسلّم خلال 7 أيام | `proof_pack_delivered` + مسار في FIRST_PAID_DIAGNOSTIC_DOD |
| KR3 | KPI 6/6 من HubSpot | `kpi_founder_commercial_import.yaml` + apply |

**Weekly retro:** `python scripts/founder_weekly_ceo_retro.py`

---

## OKR 2 — GTM Blitz Motion A (90 يوم)

| Key result | Target | Tracker |
|------------|--------|---------|
| KR1 | 30 محادثة مؤهّلة | gtm_conversation_tracker.csv |
| KR2 | 5 proposals Diagnostic | proposals/ + render_diagnostic_proposal.py |
| KR3 | 3 اجتماعات in-person | gtm_conversation_log.py --in-person |

**Daily:** `python scripts/gtm_conversation_log.py --company "..." --qualified`

---

## OKR 3 — Production Trust (80%+)

| Key result | Target | Command |
|------------|--------|---------|
| KR1 | dealix.me/ar = 200 | DNS → Railway (DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md) |
| KR2 | API trust endpoints 200 | ceo_production_trust_bundle.py |
| KR3 | SENTRY_DSN على Railway | verify step في bundle |

---

## Weekly retro template

        copy to data/founder_briefs/)

```markdown
## Week YYYY-Www
- One decision served phase: ___
- Evidence events logged: ___
- GTM conversations added: ___
- Production layers %: ___
- Blockers closed: ___
- Stop doing (next week): ___
```

---

## LinkedIn 2×/week (PDPL + governance)

| Week | Topic AR |
|------|----------|
| 1 | لماذا لا cold WhatsApp في B2B السعودي — PDPL |
| 2 | approval-first architecture — لا إرسال بدون موافقة |
| 3 | Trust Pack — ما نعد به وما لا نعد |
| 4 | أول Diagnostic — أدلة قبل upsell |

**Rule:** مسودة فقط — نشر يدوي. `social_queue_today.py`

---

## Commands (morning)

```powershell
powershell -File scripts/run_founder_commercial_day.ps1
py -3 scripts/founder_daily_five_metrics.py
py -3 scripts/run_ceo_master_plan_status.py
```
