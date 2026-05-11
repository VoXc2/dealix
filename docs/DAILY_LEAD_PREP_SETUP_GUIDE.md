# Daily Autonomous Lead Prep — Founder Setup Guide

**Wave 12.8 + 12.9** — Dealix's daily morning lead-prep system.

> **Promise:** every morning at 8 AM KSA, you wake up to a ranked board
> of today's top 5 leads — bilingual "why now" + recommended action +
> action mode (`draft_only` / `approval_required` / `blocked`). You
> review, approve, send manually. Zero auto-send. Article 4 immutable.

---

## 5-minute setup

### Option 1 — Run manually each morning (no setup)

```bash
cd /home/user/dealix
python3 scripts/dealix_daily_lead_prep.py
```

Output: `data/wave12/daily_lead_prep/{today}.json` + `.md` (gitignored).

If you have inbound leads in `lead_inbox.jsonl` (landing form
submissions), they're auto-sourced. Otherwise the script produces
an empty board with today's season context.

### Option 2 — Add your own candidates (CSV)

```bash
# Copy the template
cp data/workflows/sample_leads_template.csv data/wave12/my_leads.csv

# Edit with your warm intros + partner referrals + inbound leads
# (the template shows 5 example rows + all CSV columns)
nano data/wave12/my_leads.csv

# Run with your CSV
python3 scripts/dealix_daily_lead_prep.py --candidates data/wave12/my_leads.csv --top-n 5
```

Output: same path as Option 1.

### Option 3 — Cron daily at 8 AM KSA (5 AM UTC)

```bash
# Add to your crontab:
crontab -e

# Then add this line (adjust path):
0 5 * * * cd /home/user/dealix && python3 scripts/dealix_daily_lead_prep.py >> data/wave12/cron.log 2>&1
```

Every morning the script runs autonomously. You read the MD output
with your coffee.

### Option 4 — Cron with your CSV (recommended)

```bash
# Same cron syntax + --candidates flag pointing to your maintained CSV
0 5 * * * cd /home/user/dealix && python3 scripts/dealix_daily_lead_prep.py --candidates data/wave12/my_leads.csv --top-n 5 >> data/wave12/cron.log 2>&1
```

---

## What you get every morning

A markdown file at `data/wave12/daily_lead_prep/{today}.md` with:

```
# Dealix Daily Lead Board — 2026-05-15

**Generated:** 2026-05-15T05:00:00+00:00
**Season:** zatca_wave_24_deadline_window (confidence=0.95)

## ملخص اليوم / Today's summary
- AR: بورد اليوم: 5 ليد (P0=2 · P1=2 · محظور=0). الموسم: zatca_wave_24...
- EN: Today's board: 5 leads (P0=2 · P1=2 · blocked=0). Season: zatca...

### الموسم / Season context
- AR: نافذة موعد ZATCA الموجة 24 — ضغط امتثال على شركات > 375K ر.س
- EN: ZATCA Wave 24 deadline window — compliance pressure on >375K SAR firms
- Recommended offer pivot: `Compliance + Growth Ops Monthly (ZATCA readiness)`

---
## Top 5 Leads (out of 12 candidates)

### 1. Acme Real Estate Riyadh — `P0_NOW`
- Composite score: 0.812
- Sector: real_estate · City: Riyadh
- Source: `warm_intro` · Action mode: `approval_required`
- Why now (AR): علاقة قوية أو inbound • وصول للقرار-maker
- Why now (EN): Warm/inbound relationship · Decision-maker accessible
- Recommended action (AR): جهّز رسالة عربية + احجز اتصال هذا الأسبوع
- Recommended action (EN): Draft Arabic message + book call this week
- Saudi scores: arabic=0.85 · dm_access=0.90 · relationship=1.00 ...

[... 4 more leads ...]

---
## Next founder action
> راجع الـ 2 P0 leads + اعتمد الرسائل المرفقة قبل الإرسال اليدوي.
```

---

## CSV columns

Only `name` is required. All others have safe defaults.

| Column | Required | Default | Notes |
|---|---|---|---|
| `name` | ✅ Yes | — | Company name |
| `sector` | ❌ | `""` | e.g. `real_estate`, `agency`, `b2b_services`, `consulting`, `retail`, `healthcare`, `finance` |
| `city` | ❌ | `""` | e.g. `Riyadh`, `Jeddah`, `Dammam`, `Khobar` |
| `country` | ❌ | `""` | e.g. `SA` (use `SA` for Saudi-context score boost) |
| `domain` | ❌ | `""` | e.g. `acme.com.sa` (`.sa` TLD boosts arabic_readiness) |
| `contact_name` | ❌ | `""` | The person you'd reach out to |
| `contact_title` | ❌ | `""` | e.g. `CEO`, `Founder`, `Director`, `المدير العام` (titles boost decision_maker_access) |
| `source` | ❌ | `warm_intro` | See "Allowed sources" below |
| `locale` | ❌ | `ar` | `ar`, `ar-SA`, `en` |
| `annual_turnover_sar` | ❌ | `null` | If > 375K, gets ZATCA Wave 24 compliance uplift |
| `notes` | ❌ | `""` | Free text, max 200 chars |

---

## Allowed sources (Article 4)

| Source | Score boost | Notes |
|---|---|---|
| `warm_intro` | 1.00 (max) | Personal intro from your network |
| `partner_referral` | 1.00 (max) | From an agency partner |
| `founder_intro` | 1.00 (max) | Direct founder-to-founder intro |
| `inbound_form` | 0.85 | Submitted via landing page form |
| `inbound_whatsapp` | 0.85 | Started a WhatsApp conversation |
| `website_inquiry` | 0.85 | Filled out a contact form |
| `event_list_with_permission` | 0.65 | Conference/exhibition list with consent |
| `public_business_info_allowed` | 0.65 | Public business directory (within terms) |
| `customer_uploaded_csv` | 0.55 | Customer's own data they shared with you |
| `crm_import` | 0.55 | Migrated from their CRM |
| `google_sheet` | 0.55 | Customer's Google Sheet they granted access to |
| `manual_linkedin_research` | 0.40 | You researched on LinkedIn manually |
| `(unknown)` | 0.30 | Flagged + needs review |

## **NEVER use these — automatically routed to BLOCKED priority:**

- `cold_outreach` ⛔
- `scraping` ⛔
- `purchased_list` ⛔
- `linkedin_automation` ⛔

These violate Article 4 hard gates and the script will route them to
`BLOCKED` priority + `blocked` action mode regardless of any other score.

---

## Article 4 invariants (built into the script — verified by tests)

✅ All outputs are `draft_only` or `approval_required` or `blocked`
✅ NEVER calls send APIs (WhatsApp, email, LinkedIn, phone)
✅ NEVER calls live charge / live publish
✅ NEVER scrapes — only consumes founder-supplied CSV or `lead_inbox.jsonl`
✅ Blocked sources routed to `BLOCKED` regardless of other scores
✅ Output path is gitignored — no PII committed to git
✅ Every score `is_estimate=True` (Article 8)

---

## Daily founder ritual (≤10 min)

1. **8:00 AM** — open `data/wave12/daily_lead_prep/{today}.md`
2. **Read** the bilingual summary + top 5 leads (≤2 min)
3. **For each P0/P1**: open the suggested message → polish → copy to your WhatsApp/LinkedIn → send manually
4. **For BLOCKED**: investigate the source — likely needs to be reclassified before re-running
5. **Mark sent**: optional — log in `data/wave11/warm_intros.jsonl` (Wave 11) for the funnel metrics

---

## Troubleshooting

**"No candidates and no inbound leads"** — add a CSV via `--candidates` OR
populate `var/lead-inbox.jsonl` via the landing form OR
add inbound landing-form submissions.

**"All leads BLOCKED"** — your CSV `source` column has unsafe values.
Change to `warm_intro` / `inbound_form` / `partner_referral`.

**"Wrong season detected"** — run with `--on-date 2026-05-15` (ISO date)
to override.

**"Want to skip auto-source"** — pass `--no-auto-source` to ignore
`lead_inbox.jsonl` even when the CSV is missing.

---

## What this is NOT

- ❌ NOT an auto-sender (Article 4 NO_LIVE_SEND)
- ❌ NOT a scraper (Article 4 NO_SCRAPING)
- ❌ NOT a CRM (use it alongside whatever CRM you use; output is plain JSON+MD)
- ❌ NOT a guarantee — every score is `is_estimate=True` (Article 8)

## What this IS

- ✅ A morning ritual that turns your CSV/inbox into a ranked board
- ✅ A bilingual decision aid (Arabic + English)
- ✅ A safety-first preparation layer (drafts only, founder approves)
- ✅ Saudi-aware (season detection + 13-dim local scoring)
- ✅ Cron-able + deterministic + zero-cost (no LLM calls, no cloud)

---

## The single most important next step

> **Copy `data/workflows/sample_leads_template.csv` → fill with your 5 warm intros → run the script → read the MD output → send the top message manually today.**
