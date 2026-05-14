# Risk Register

| ID | Risk | Owner | Likelihood | Impact | Early Warning | Control | Response |
|----|------|-------|------------|--------|---------------|---------|----------|
| R1 | Agency trap | CEO | Medium | High | تزايد النطاق المخصص | Service catalog | kill/reframe scope |
| R2 | Governance incident | Governance Owner | Low | High | مخرجات بلا حالة حوكمة | Governance Runtime | incident response |
| R3 | Bad revenue | CEO | Medium | Medium | هامش منخفض + proof ضعيف | Revenue quality score | reject/reprice |
| R4 | Agent over-permission | Product | Medium | High | طلب أداة إرسال خارجي | Agent Registry | deny tool + approval workflow |
| R5 | Partner covenant breach | Partnership | Low | High | وعود غير معتمدة | Partner Covenant | suspend + audit |

**حقول السجل الكاملة (تشغيليًا):** owner · severity · likelihood · control · early warning · response plan · test/checklist — `risk_register_metadata_complete` في `risk_resilience_os/risk_register.py`.

**صعود:** [`RISK_DASHBOARD.md`](RISK_DASHBOARD.md) · [`../board_decision_system/BOARD_RISK_DECISIONS.md`](../board_decision_system/BOARD_RISK_DECISIONS.md)
