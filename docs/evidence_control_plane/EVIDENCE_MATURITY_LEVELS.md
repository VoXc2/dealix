# Evidence Maturity Levels

| Level | الاسم | الوصف | مناسب لـ |
|-------|--------|--------|-----------|
| 0 | No Evidence | قرارات في الذاكرة؛ لا logs؛ لا تتبع مصدر | **ممنوع لـ Dealix** |
| 1 | Basic Logs | AI run ID، timestamp، task، output | MVP داخلي فقط |
| 2 | Governance Evidence | Source Passport، policy checks، governance decision، QA score | **MVP حقيقي** |
| 3 | Approval + Proof Evidence | Human review، approval event، Proof Pack، Value Event | Retainers |
| 4 | Enterprise Evidence Control Plane | Evidence graph، audit exports، risk dashboard، policy registry، agent auditability | Enterprise |
| 5 | Continuous Trust OS | مراقبة مستمرة، سجلات مقاومة للتلاعب، حوكمة cross-workflow، تقارير امتثال آلية | اتجاه مستقبلي |

## الكود

عتبات التغطية في `evidence_dashboard.py` — انظر [EVIDENCE_DASHBOARD.md](EVIDENCE_DASHBOARD.md).
