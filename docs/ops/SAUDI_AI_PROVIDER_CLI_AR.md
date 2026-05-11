# Saudi AI Provider CLI

أوامر التشغيل الأساسية:

- `python3 -m saudi_ai_provider verify`
- `python3 -m saudi_ai_provider package --segment smb`
- `python3 -m saudi_ai_provider quote --service CUSTOMER_PORTAL_GOLD --employees 120`
- `python3 -m saudi_ai_provider roadmap --days 180`
- `python3 -m saudi_ai_provider kpis --service SECURITY_SILVER`
- `python3 -m saudi_ai_provider pitch --service OBSERVABILITY_BRONZE --lang ar`
- `python3 -m saudi_ai_provider offer --service CUSTOMER_PORTAL_GOLD --segment smb --lang ar`

سكربتات التحقق:

- `python3 scripts/validate_pricing.py`
- `python3 scripts/validate_kpis.py`
- `python3 scripts/validate_playbooks.py`
- `bash scripts/saudi_ai_provider_verify.sh`
