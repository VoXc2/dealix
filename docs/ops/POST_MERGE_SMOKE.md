# Post-Merge Smoke Runbook — كتيّب الفحص بعد النشر
## Wave 19+ Operational Closure · companion to `scripts/post_merge_smoke.py`

> **When to run:** immediately after Railway finishes auto-deploying `main` post-merge of PR #235. Then again any time production behavior is unclear.
> **Read time:** ≤ 3 minutes. Run time: ≤ 2 minutes.

The smoke script `scripts/post_merge_smoke.py` hits 14 public + 4 admin-gated endpoints and checks both HTTP status AND payload shape. This runbook is the bilingual reference for what each endpoint MUST return for a green light, and the troubleshooting tree when anything fails.

يفحص السكربت ١٤ نقطة نهاية عامّة + ٤ مُحمَيّة بمفتاح المسؤول، ويتحقّق من الحالة + شكل البيانات. هذا الكتيّب يصف ما يجب أن تُعيده كل نقطة، وشجرة استكشاف الأخطاء عند الفشل.

---

## How to run · كيف تشغّله

```bash
# 1. Against production (public endpoints only)
python scripts/post_merge_smoke.py https://api.dealix.me

# 2. Against production with admin endpoints
python scripts/post_merge_smoke.py https://api.dealix.me --admin "$ADMIN_API_KEY"

# 3. JSON output for cron logs
python scripts/post_merge_smoke.py https://api.dealix.me --json | jq .summary

# 4. Local in-process (for tests + offline verification)
python scripts/post_merge_smoke.py --local
```

Exit code 0 = all green. Exit code 1 = at least one endpoint failed.

---

## What each endpoint MUST return for green · المعايير المطلوبة

### `GET /healthz` → 200
- Body: `{"status": "ok", "service": "dealix"}` or similar shape with `status: ok`.
- Used by Railway health checks; if this fails, production is not running.

### `GET /api/v1/dealix-promise` → 200
- `commitments_count` MUST equal `11`. Drops below 11 = doctrine drift.
- `governance_decision: "allow"`.
- 11 commitments listed with `id`, `title_en`, `title_ar`, `enforced_by`.

### `GET /api/v1/dealix-promise/markdown` → 200
- Plain text response. MUST contain the bilingual disclaimer "النتائج التقديرية ليست نتائج مضمونة".

### `GET /api/v1/doctrine` → 200
- `non_negotiables_count` MUST equal `11`.
- `public_framework: true`.
- `license_doctrine` mentions "CC BY 4.0".
- `license_code_examples == "MIT"`.
- `trademark_note` mentions "Dealix".

### `GET /api/v1/doctrine/controls` → 200
- `controls_count` MUST equal `11`.

### `GET /api/v1/doctrine/markdown` → 200
- Bilingual disclaimer present.

### `GET /api/v1/commercial-map` → 200
- `registry_count` MUST equal `3` (the 2026-Q2 reframe: Diagnostic / Retainer / Sprint).

### `GET /api/v1/commercial-map/markdown` → 200
- Bilingual disclaimer present.

### `GET /api/v1/gcc-markets` → 200
- `market_count` MUST equal `4` (Saudi / UAE / Qatar / Kuwait).
- `active_count` MUST equal `1` (Saudi-only beachhead; if this becomes > 1 without an actual signed customer in a new market, the doctrine has drifted).

### `GET /api/v1/gcc-markets/markdown` → 200
- Bilingual disclaimer present.

### `GET /api/v1/capital-assets/public` → 200
- `public_asset_count` ≥ 5 (at least 7 expected currently).
- Each asset MUST NOT include `file_paths` or `commercial_use` (public view is shape-restricted).

### `GET /api/v1/capital-assets/public/markdown` → 200
- Bilingual disclaimer present.

### `GET /api/v1/founder/launch-status/public` → 200
- `governance_decision` present.

### `GET /api/v1/founder/command-center/public` → 200
- MUST NOT contain `arr_pacing` or `anchor_partners` (commercial-sensitive — they belong in the admin view only).

### `GET /api/v1/founder/command-center` (admin) → 200
- Top-level aggregate with all 12 status cards including the 4 Wave 19 cards.

### `GET /api/v1/founder/post-deploy-check` (admin) → 200
- In-process smoke; `summary.all_green: true` after Wave 19 merge.

### `GET /api/v1/founder/launch-status` (admin) → 200
- Returns `moyasar_mode` + `zatca_mode` + git status.

### `GET /api/v1/capital-assets` (admin) → 200
- `asset_count` ≥ 15.

---

## Troubleshooting tree · شجرة استكشاف الأخطاء

### Symptom: `/healthz` returns 502 or never responds
- Railway deploy failed. Open Railway dashboard → Activity tab → most recent deploy → log.
- Common causes: `alembic upgrade head` failed (check `DATABASE_URL` env var), uvicorn startup error (check Python import path), Railway built but never started (out-of-memory).
- **Rollback procedure:** Railway → Deployments → pick the previous green deployment → "Redeploy". Then investigate the failed deploy without time pressure.

### Symptom: `dealix-promise.commitments_count != 11`
- The doctrine has lost a commitment. This is a P0 alert.
- Check `auto_client_acquisition/governance_os/non_negotiables.py` on production-deployed commit.
- Re-run `bash scripts/pr235_merge_readiness.sh` on the local branch and verify it reports 11 non-negotiables. If yes, the deploy serves a stale build — redeploy.

### Symptom: `doctrine.public_framework: false` or missing license fields
- Open framework endpoint has been tampered with. P0 alert (the open positioning is a brand moat).
- Verify `api/routers/doctrine.py` on the deployed commit matches the test in `tests/test_doctrine_endpoint.py`.

### Symptom: `commercial-map.registry_count != 3`
- Offer ladder drift. Either a new offer was registered without updating `tests/test_service_catalog.py`, or the 2026-Q2 reframe has been reverted.
- Open `auto_client_acquisition/service_catalog/registry.py` and confirm exactly 3 entries in `OFFERINGS`.

### Symptom: `gcc-markets.active_count > 1`
- A second market has been promoted to `active` without a signed customer. Doctrine drift.
- Open `auto_client_acquisition/governance_os/gcc_markets.py`. Saudi MUST be the only active until the founder explicitly flips a market on signed-customer evidence.

### Symptom: `capital-assets/public` leaks `file_paths` or `commercial_use`
- Public view is supposed to omit those fields. The shape check caught a regression.
- Open `api/routers/capital_assets_public.py::_asset_to_public_dict` and confirm only the 9 public-safe fields are returned.

### Symptom: `command-center/public` leaks `arr_pacing` or `anchor_partners`
- Same class of regression: the public view should not surface commercial-sensitive aggregates.
- Open `api/routers/founder_command_center.py::command_center_public` and confirm the JSON payload.

### Symptom: admin endpoints return 401/403 when the admin key is correct
- `ADMIN_API_KEYS` env var on Railway either empty or mismatched. Check Railway → Variables.
- Test locally: `ADMIN_API_KEYS=test python -m pytest tests/test_founder_command_center.py -q --no-cov` should pass.

### Symptom: every endpoint slow (> 5 s)
- Cold start or DB connection pool exhaustion. Wait 60 s and re-run. If still slow, restart the service from Railway.

---

## What you do NOT do · ما لا تفعله

- ❌ Do NOT POST anything from this script. It is read-only and that is the doctrine.
- ❌ Do NOT skip a failed endpoint by passing a flag. Investigate every failure.
- ❌ Do NOT publish that "production is live" until 18/18 endpoints are green. The verify page (`landing/verify.html`) is the shareable signal.
- ❌ Do NOT modify the marker JSON files in `data/` to mask a regression. The verifier honesty is the moat.

---

## Cross-links · روابط

- Script: `scripts/post_merge_smoke.py`
- Pre-merge readiness: `scripts/pr235_merge_readiness.sh`
- Master verifier: `scripts/verify_all_dealix.py`
- Day-1 kit: `docs/ops/FOUNDER_DAY1_KIT.md`
- Master status doc: `docs/ops/DEALIX_MASTER_STATUS.md`
- The Dealix Promise: `docs/THE_DEALIX_PROMISE.md`

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
