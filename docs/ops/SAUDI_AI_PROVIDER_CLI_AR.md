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
- `python3 -m saudi_ai_provider proposal --service CUSTOMER_PORTAL_GOLD --intake-file intake/demo_customer_intake.json --lang ar`
- `python3 -m saudi_ai_provider dashboard-export --metrics-json dashboard/sample_metrics.json`
- `python3 -m saudi_ai_provider recurring-model --setup-fee 45000 --monthly 18000 --months 12 --expansion-rate 0.08`
- `python3 -m saudi_ai_provider proposal-scorecard --service CUSTOMER_PORTAL_GOLD --intake-file intake/demo_customer_intake.json`
- `python3 -m saudi_ai_provider auto-package --intake-file intake/demo_customer_intake.json --max-services 4`
- `python3 -m saudi_ai_provider renewal-orchestrator --customer-state-file revenue/demo_customer_state.json`
- `python3 -m saudi_ai_provider p2-monetization --service CUSTOMER_PORTAL_GOLD --intake-file intake/demo_customer_intake.json --customer-state-file revenue/demo_customer_state.json`
- `python3 -m saudi_ai_provider offer-stack --segment enterprise --lang ar`
- `python3 -m saudi_ai_provider launch-pack --segment enterprise --lang ar --output out/launch/final_launch_pack.md`
- `python3 -m saudi_ai_provider agent-apps --service AI_GOVERNANCE_OS --lang ar`
- `python3 -m saudi_ai_provider agent-rollout --segment enterprise --lang ar`

سكربتات التحقق:

- `python3 scripts/validate_pricing.py`
- `python3 scripts/validate_kpis.py`
- `python3 scripts/validate_playbooks.py`
- `python3 scripts/validate_governance.py`
- `python3 scripts/validate_runtime.py`
- `python3 scripts/validate_commercialization.py`
- `python3 scripts/validate_monetization.py`
- `python3 scripts/validate_agent_profiles.py`
- `python3 scripts/final_launch_verify.py`
- `bash scripts/saudi_ai_provider_verify.sh`
