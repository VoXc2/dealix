# بروتوكول غرفة حرب الإطلاق

## قبل الإطلاق

- `GET /api/v1/readiness/unified` → `go: true`
- `bash scripts/reliability_drills_scorecard.py`
- PERB قرار Go موثّق

## أثناء الإطلاق

- مالك domain + SLO مراقبة
- لا cutover ledger بدون `external_signal`

## بعد الإطلاق

- weekly proof pack + decision postmortem إن لزم
