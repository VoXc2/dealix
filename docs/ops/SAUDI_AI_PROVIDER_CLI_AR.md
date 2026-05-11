# Saudi AI Provider CLI

أوامر التشغيل الأساسية:

- `python3 -m saudi_ai_provider verify`
- `python3 -m saudi_ai_provider package --segment smb`
- `python3 -m saudi_ai_provider quote --service CUSTOMER_PORTAL_GOLD --employees 120`
- `python3 -m saudi_ai_provider roadmap --days 180`
- `python3 -m saudi_ai_provider kpis --service SECURITY_SILVER`
- `python3 -m saudi_ai_provider pitch --service OBSERVABILITY_BRONZE --lang ar`
- `python3 -m saudi_ai_provider offer --service CUSTOMER_PORTAL_GOLD --segment smb --lang ar`
- `python3 -m saudi_ai_provider generate-offer --service SECURITY_GOLD --segment enterprise --industry banking --lang ar`
- `python3 -m saudi_ai_provider roi --service CUSTOMER_PORTAL_GOLD --tickets 50000 --agent-cost 18 --automation-rate 0.42`

سكربتات التحقق:

- `python3 scripts/validate_pricing.py`
- `python3 scripts/validate_kpis.py`
- `python3 scripts/validate_playbooks.py`
- `python3 scripts/validate_governance.py`
- `python3 scripts/validate_runtime.py`
- `bash scripts/saudi_ai_provider_verify.sh`
