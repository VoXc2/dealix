# Railway Deploy Checklist — قائمة التحقق من نشر Railway

> Wave 14J — 1-page bilingual operator runbook for the founder to deploy to production via Railway.
>
> دليل تشغيل ثنائي اللغة من صفحة واحدة للمؤسس لنشر الإنتاج عبر Railway.

This runbook is **opinionated and sequential**. Do every step in order. Each section lists its expected time so you can plan the deploy window.

هذا الدليل **مرتّب ومتسلسل**. نفّذ كل خطوة بالترتيب. كل قسم يذكر وقته المتوقع لتتمكن من التخطيط لنافذة النشر.

---

## 0. Pre-flight (15 min) — الفحص قبل الإقلاع (15 دقيقة)

Verify everything is green **locally** before touching Railway:

- **Local tests green:**
  ```bash
  python -m pytest tests/test_no_*.py tests/governance/ tests/test_commercial_map.py tests/test_referral_persistence.py -q --no-cov
  ```
- **Local smoke green** (run uvicorn first in another terminal: `uvicorn main:app --reload`):
  ```bash
  bash scripts/prod_smoke.sh http://localhost:8000
  ```
- **Alembic dry-run:**
  ```bash
  alembic upgrade head --sql > /tmp/alembic.sql && grep -i referral /tmp/alembic.sql
  ```
  Expect: the Wave 14D.1 migration `010_referral_*` is present with `CREATE TABLE` statements for the referral persistence tables.
- **Branch state:**
  ```bash
  git log --oneline main..HEAD
  ```
  Expect: **≥ 50 commits** ahead of `main` (Wave 14A through 14J).

If any of these fail, **stop**. Fix locally before opening the PR.

إذا فشل أي من هذه، **توقف**. أصلح محليًا قبل فتح طلب الدمج.

---

## 1. PR + CI (10 min) — طلب الدمج والتكامل المستمر

- Push the branch (already on `claude/dealix-layers-40-200-HSWI8`):
  ```bash
  git push -u origin claude/dealix-layers-40-200-HSWI8
  ```
- Open a PR to `main` with title:
  > **Wave 14A-J — complete 90-day commercial activation closeout**
- Wait for GitHub Actions to go **fully green**. Railway has "Wait for CI" enabled, so a red CI run will block the deploy automatically — but do not rely on that; treat a red CI as a stop-the-line event.
- Once green, **squash-merge** to `main`. Do not rebase-merge — we want one Wave-14 commit on `main` for easy rollback.

اضغط دمج Squash وليس Rebase — نريد تثبيتًا واحدًا للموجة 14 على `main` لتسهيل التراجع.

---

## 2. Railway auto-deploy watch (~8 min) — مراقبة النشر التلقائي

Railway auto-deploys on every merge to `main`. Watch closely:

- Open Railway dashboard → **production environment** → **deployments** tab.
- Watch the new build start (Dockerfile build, ~3 min).
- Watch the `release: alembic upgrade head` log — **confirm referral tables are created** (look for `CREATE TABLE referrals` etc).
- Watch `web: uvicorn ...` start.
- The **healthcheck at `/healthz` must pass within 300 seconds** or Railway will mark the deploy failed and roll back automatically.

إذا فشل الفحص الصحي خلال 300 ثانية، فإن Railway سيتراجع تلقائيًا. هذا أمان مدمج — استخدمه.

---

## 3. Post-deploy smoke (5 min) — اختبار الدخان بعد النشر

From any machine (local laptop is fine):

```bash
export PROD=https://<your_railway_url>
bash scripts/prod_smoke.sh $PROD
```

**Expected:**
- All curls return **2xx** responses.
- A transactional confirmation email reaches the founder's inbox (the smoke script submits a real diagnostic form with the founder's own email).
- Total smoke run finishes in under 90 seconds.

If any curl returns non-2xx, **stop and roll back** (section 6).

إذا أعاد أي طلب رمزًا غير 2xx، **توقف وتراجع** (القسم 6).

---

## 4. Manual production sanity checks — فحوصات الإنتاج اليدوية

The smoke covers APIs. These steps cover the UI:

- Open `https://dealix.sa/diagnostic.html` (or your prod URL). Fill the form. Verify:
  - `"ok": true` response within 2–4 seconds
  - confirmation email reaches the submitted address
  - qualification decision badge renders inline
- Open `https://dealix.sa/customer-portal.html?handle=Slot-A`. Verify the **10 panels** render (mostly `null` values are OK for a fresh account).
- Open `https://dealix.sa/sprint-sample.html`. Verify the **8-step run** renders end-to-end.
- Open `https://dealix.sa/data-pack.html`. Upload `data/demo/saudi_b2b_demo.csv`. Verify the **DQ score** returns.
- Open `https://dealix.sa/architecture.html`. Click the **Trust Pack** link. Verify the procurement bundle downloads (or the markdown fallback renders if WeasyPrint is unavailable on the deployed runtime).

افتح كل صفحة على Safari وعلى Chrome — اختبر RTL على iOS Safari تحديدًا.

---

## 5. First-real-customer kickoff — انطلاق أول عميل حقيقي

After smoke is green and UI checks pass:

- Open `landing/founder-leads.html?key=<admin_key>`.
- Triage any pilot leads that arrived since the last review.
- Send the **first 5 warm-list messages** following `docs/sales-kit/WARM_LIST_WORKFLOW.md`.
- Schedule **day-1** of the 30-day plan from `/root/.claude/plans/wiggly-cooking-sketch.md`.

هذه هي اللحظة التي يتحول فيها 90 يومًا من الهندسة إلى إيراد. لا تؤجلها بعد نجاح النشر.

---

## 6. Rollback — التراجع

If anything breaks at any point:

- **Option A (fastest, ~2 min):** Railway dashboard → previous deploy → **Redeploy this version**.
- **Option B (cleanest, ~5 min):** Revert the merge commit:
  ```bash
  git revert -m 1 <merge_sha>
  git push origin main
  ```
  Railway will auto-deploy the revert.

The rollback window is **5 minutes** end-to-end. Practice it once on staging if you have not already.

نافذة التراجع **5 دقائق** من البداية إلى النهاية. تدرّب عليها مرة واحدة على بيئة التجريب إن لم تفعل بعد.

---

## 7. Variable verification on Railway — التحقق من المتغيرات على Railway

Confirm the **13 service variables** are set in Railway → Variables tab:

1. `DATABASE_URL` (Postgres connection string)
2. `APP_SECRET_KEY` (64-byte hex; generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
3. `MOYASAR_SECRET_KEY` (`sk_test_…` for now, `sk_live_…` after manual cutover)
4. `MOYASAR_WEBHOOK_SECRET`
5. `GMAIL_SENDER_EMAIL`, `GMAIL_OAUTH_REFRESH_TOKEN`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`
6. `GROQ_API_KEY` (LLM gateway fallback)
7. `GOOGLE_SEARCH_API_KEY` / `GOOGLE_SEARCH_CX` (sector intel)
8. `GREENAPI_INSTANCE_ID` / `GREENAPI_TOKEN` (WhatsApp safe-send only — never cold)
9. `POSTHOG_API_KEY` (analytics)
10. `CALENDLY_URL` (booking)
11. `APP_URL` (Moyasar callback domain)
12. `ZATCA_SANDBOX=true` (keep `true` in prod **only** until manual ZATCA cutover per `docs/MOYASAR_LIVE_CUTOVER.md`)

If any are missing, the related feature will degrade gracefully (the codebase enforces `no_silent_failures`) — but the founder will see warnings on the dashboard and the daily founder brief will flag the gap.

إذا غاب أي متغير، فإن الميزة المرتبطة ستتدهور بأمان — لكن لوحة المؤسس ستعرض تحذيرًا.

---

## 8. Doctrine reaffirmation — إعادة تأكيد المبادئ

Even in production, the **11 non-negotiables** are enforced by passing tests. If CI ever fails on a `tests/test_no_*` doctrine guard:

- **Do not merge.**
- **Do not bypass CI.**
- Investigate the root cause, fix it, re-run CI.

The doctrine is the moat. The moment we ship around it, the brand value collapses.

المبادئ هي الحاجز التنافسي. في اللحظة التي نتجاوزها فيها، تنهار قيمة العلامة التجارية.

---

## Footer

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
