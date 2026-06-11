# Post Deploy Smoke Test

After deploy, run:

```bash
python3 scripts/post_deploy_smoke.py --base-url https://<your-domain>
```

Expected: all 23 paths return HTTP 200.

If any path returns 4xx/5xx:
1. Check Vercel/Railway logs
2. Check env vars
3. Run `python3 scripts/local_smoke_test.py` locally
4. Rollback if needed
