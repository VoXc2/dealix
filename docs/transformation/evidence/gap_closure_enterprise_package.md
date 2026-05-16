# Gap closure evidence — Enterprise package standardization

| Field | Value |
| --- | --- |
| **Matrix gap** | Enterprise package standardization |
| **Owner OS** | GTM + Trust + Delivery |
| **Artifact** | `docs/transformation/enterprise_package/*`, runbooks under `docs/transformation/enterprise_package/` |
| **KPI impact** | `conversion_discovery_to_pilot`, `time_to_proof_days` |
| **Risk impact** | Procurement stall if templates diverge from delivered scope |
| **Verification** | `python3 scripts/verify_global_ai_transformation.py --check-enterprise-package` |

**Closure statement:** Templates and verification hooks exist in-repo; customer-specific numbers belong in `kpi_baselines.yaml` + weekly proof packs.

---

## Verification record (reference)

Command:

```bash
python3 scripts/verify_global_ai_transformation.py --check-enterprise-package
```

Last captured output (trimmed):

```text
GLOBAL AI TRANSFORMATION: PASS
```

**KPI numeric closure:** record `conversion_discovery_to_pilot` and `time_to_proof_days` in [dealix/transformation/kpi_baselines.yaml](dealix/transformation/kpi_baselines.yaml) with CRM / delivery timestamps in `source_ref`.
