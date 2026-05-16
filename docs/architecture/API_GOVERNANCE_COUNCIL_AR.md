# مجلس حوكمة API

## الهدف

تقليل تعقيد `api/main.py` ورفع قيمة كل domain.

## إيقاع

- شهري — مراجعة routers الجديدة والمهملة
- مخرج — تحديث `API_DOMAIN_OWNERSHIP.md`

## معايير قبول endpoint

- مالك domain في `OWNERS.yaml`
- SLO في `slo_by_domain.yaml` إن كان critical
- lane tag: `fast_lane` أو `governed_lane`
