# Evidence Gap Rules

كل gap له **قرار تشغيلي**.

| Gap | القرار |
|-----|--------|
| Source missing passport | **Block AI use** |
| Output missing governance decision | **Block client delivery** |
| External action without approval | **Incident** |
| Claim without proof | **Remove claim** |
| Retainer proposal without value evidence | **Do not push retainer** |
| Agent without auditability card | **No production use** |

## الكود

`auto_client_acquisition/evidence_control_plane_os/evidence_gap_detector.py`
