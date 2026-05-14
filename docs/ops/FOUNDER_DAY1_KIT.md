# Founder Day-1 Kit — كيتاب اليوم الأول للمؤسس
## The only doc to read after PR #235 merges · الوثيقة الوحيدة التي تُقرَأ بعد دمج PR #235

> **Audience / الجمهور:** المؤسس فقط · Founder only.
> **Duration / المدّة:** ≤ 30 minutes from merge to first outreach sent.
> **Pre-requisite / الشرط المسبق:** PR #235 must be open on GitHub and ready to merge.
> **Wave / الموجة:** 19+ Operational Closure.

This is the single document you read first thing tomorrow morning. Open it on your phone. Follow the seven numbered steps in order. Cross-links go to the exact files you need; nothing else requires reading.

هذه هي الوثيقة الوحيدة التي تقرأها صباح الغد. افتحها من الجوال. اتبع الخطوات السبعة المرقّمة بالترتيب. الروابط المتقاطعة تقودك إلى الملفات التي تحتاجها فقط؛ لا قراءة إضافية مطلوبة.

---

## 0. State of the world this morning · حالة الأمور هذا الصباح

What is shipped (build-complete):
- 11 non-negotiables enforced by passing tests in CI
- 3-offer ladder: Free Strategic Diagnostic / 4,999 SAR/mo Governed Ops Retainer / 25,000 SAR Revenue Intelligence Sprint
- 8 public endpoints (Promise, Doctrine, Commercial Map, GCC Markets, Capital Assets, Launch Status, Command Center public, Health)
- 4 admin-gated founder surfaces (Command Center, Post-deploy Check, Launch Status, Capital Assets)
- 5 strategic landing pages (promise, pricing, founder-command-center, verify, dealix-os)
- 40+ bilingual docs (the doctrine, the GCC pack, the Capital Asset Library, the funding pack, the open-doctrine framework, the operational runbooks)
- 195+ tests passing
- Master verifier scoring 8/10 perfect

What is NOT shipped (waiting on you):
- **Partner Motion** — sits at 3/5 until you send the first outreach.
- **First Invoice Motion** — sits at 3/5 until you issue Invoice #1.

The marker files in `data/*.json` refuse to claim either has happened until it actually has. This is intentional. The verifier flips to `ceo_complete: true` only when both motions become real.

---

## 1. Merge PR #235 · ادمج PR #235 (≤ 1 minute)

1. Open `https://github.com/VoXc2/dealix/pull/235` on your phone.
2. Run the pre-merge readiness check on your machine (or skip if you trust the CI):
   ```bash
   bash scripts/pr235_merge_readiness.sh
   ```
   Expected: `✅ GREEN LIGHT — PR #235 is merge-ready.`
3. Click the green Merge button on GitHub.
4. Railway auto-deploys `main` within ~5 minutes.

**Anti-pattern · ممنوع:** do NOT merge if the master verifier shows any of the 8 build-complete systems below score 5. The 2 market-motion systems (Partner Motion / First Invoice Motion) at 3/5 are expected and OK.

---

## 2. Wait for Railway · انتظر النشر (≤ 5 minutes)

Open Railway dashboard. Watch the deploy log. Expect:
- `alembic upgrade head` runs and exits 0.
- `uvicorn` starts on port assigned by Railway.
- Health check passes within 60 seconds.

If anything red appears in the log, jump to `docs/ops/POST_MERGE_SMOKE.md` § Rollback procedure before continuing.

---

## 3. Run post-merge smoke · شغّل الفحص بعد النشر (≤ 2 minutes)

ONE command verifies every public + admin endpoint:

```bash
# Public-only smoke (no admin key needed)
python scripts/post_merge_smoke.py https://api.dealix.me

# Full smoke including admin endpoints
python scripts/post_merge_smoke.py https://api.dealix.me --admin "$ADMIN_API_KEY"

# Or JSON output for cron logs
python scripts/post_merge_smoke.py https://api.dealix.me --json | jq .summary
```

Expected: `✅ All public surfaces healthy. Production is live.`  All 14 public + 4 admin endpoints return the expected status + shape.

If a shape check fails, the runbook at `docs/ops/POST_MERGE_SMOKE.md` lists exactly what each endpoint MUST return and the troubleshooting tree.

---

## 4. Open the public verify page · افتح صفحة التحقّق العامة (≤ 30 seconds)

On your phone, open `https://dealix.me/verify.html`. The page live-fetches the 4 public surfaces and renders them. Four green dots = production is healthy and every claim is verifiable from a phone, with no login.

This is the URL you share with anchor partners, CISOs, and procurement reviewers. They confirm Dealix is real in under 30 seconds.

---

## 5. Open the Command Center · افتح مركز القيادة (≤ 30 seconds)

On your phone, open `https://dealix.me/founder-command-center.html`. Paste your `X-Admin-API-Key`. The page renders 12 status cards + the top-3 next actions. Expected:
- Doctrine 5/5, Offer Ladder 5/5, GCC Standard 5/5, Capital Assets 5/5, Open Doctrine 5/5, Funding Pack 5/5, Command Center 5/5, Operational Closure 5/5.
- Partner Motion 3/5 (waiting on you).
- First Invoice Motion 3/5 (waiting on you).

The top-3 next actions list will say: "Send one anchor partner outreach."  Do that next.

---

## 6. Send ONE anchor partner outreach · أرسل تواصل شريك واحد (≤ 15 minutes)

1. Open `data/anchor_partner_pipeline.json`. Pick ONE archetype (Big 4 advisory / SAMA processor / Saudi VC).
2. From the `candidate_partners` array, pick ONE specific company name.
3. Open `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`. Copy the bilingual draft for that archetype.
4. Personalize the draft: replace the `[Name]` placeholder, add a single sentence connecting your existing relationship (this is NOT cold outreach — it's warm intro or a real connection).
5. Send from your personal email or LinkedIn account (NEVER from any automated system — non-negotiable #2 and #3).
6. Append an entry to `data/partner_outreach_log.json`:
   ```json
   {
     "partner_name": "PwC Saudi",
     "archetype": "Big 4 advisory Saudi practice",
     "sent_at": "2026-05-15T08:30:00Z",
     "channel": "email",
     "message_file": "docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md#archetype-1",
     "status": "sent",
     "next_follow_up_at": "2026-05-17T08:30:00Z"
   }
   ```
7. Increment `outreach_sent_count` from `0` to `1`. Commit the change.

---

## 7. Re-run the master verifier · أعِد تشغيل المُحقّق الرئيسي (≤ 30 seconds)

```bash
python scripts/verify_all_dealix.py
```

Expected: Partner Motion flips from `3/5` to `5/5`. Master verifier now reports 9/10 perfect. Only First Invoice Motion remains at 3/5 — and that flips the moment the partner replies, you qualify a buyer, and you issue Invoice #1 per `docs/ops/FIRST_INVOICE_UNLOCK.md`.

---

## What you do NOT do today · ما لا تفعله اليوم

- ❌ Do NOT send the outreach to more than one partner today. One conversation deep > five conversations shallow.
- ❌ Do NOT publish anything on LinkedIn until the partner replies. (Non-negotiable #3 + #4.)
- ❌ Do NOT touch the marker files to claim things that haven't happened. The verifier honesty is the moat.
- ❌ Do NOT start Wave 20. The user already locked: "لا تبدأ Wave 20 قبل 1 partner meeting / 1 invoice conversation / 1 strong market objection".
- ❌ Do NOT hire. Hiring is gated on revenue per `docs/funding/FIRST_3_HIRES.md`.
- ❌ Do NOT publish the open-doctrine repo on GitHub today. Wait until after the first partner conversation confirms the framing lands.

---

## Cross-links · روابط

- Pre-merge readiness: `scripts/pr235_merge_readiness.sh`
- Post-merge smoke: `scripts/post_merge_smoke.py` + `docs/ops/POST_MERGE_SMOKE.md`
- Master verifier: `scripts/verify_all_dealix.py` + `docs/ops/DEALIX_MASTER_STATUS.md`
- Daily routine: `scripts/daily_routine.py` (run every morning thereafter)
- Weekly CEO review: `scripts/weekly_ceo_review.py` (run every Sunday)
- The 11 commitments: `docs/THE_DEALIX_PROMISE.md`
- The open framework: `docs/THE_DEALIX_OS_LICENSE.md` + `open-doctrine/`
- Anchor partner kit: `docs/sales-kit/ANCHOR_PARTNER_OUTREACH.md`
- Investor one-pager: `docs/sales-kit/INVESTOR_ONE_PAGER.md`
- First invoice runbook: `docs/ops/FIRST_INVOICE_UNLOCK.md`
- Comprehensive release notes: `docs/WAVE_16_TO_19_RELEASE_NOTES.md`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
