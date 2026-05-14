# Product Capability Matrix

يربط **قدرة منتج** في الريبو بالخدمات التي تعتمد عليها. إذا كانت القدرة **Beta** أو **غير جاهزة**، الخدمة التي تعتمد عليها لا تُعلَن كـ Official على نطاق واسع ([`SELLABILITY_POLICY.md`](../company/SELLABILITY_POLICY.md)).

| Capability | Required for | Module / path | MVP | Production |
|------------|--------------|---------------|-----|------------|
| CSV import preview | Lead Intelligence | [`../../auto_client_acquisition/data_os/import_preview.py`](../../auto_client_acquisition/data_os/import_preview.py) | Ready | Partial |
| Data quality score | Lead Intelligence, data work | [`../../auto_client_acquisition/data_os/data_quality_score.py`](../../auto_client_acquisition/data_os/data_quality_score.py) | Ready | Partial |
| Dedupe / validation | Lead Intelligence | [`../../auto_client_acquisition/data_os/dedupe.py`](../../auto_client_acquisition/data_os/dedupe.py)، [`validation_rules.py`](../../auto_client_acquisition/data_os/validation_rules.py) | Ready | Partial |
| Source + PII flags | All data paths | [`../../auto_client_acquisition/data_os/source_attribution.py`](../../auto_client_acquisition/data_os/source_attribution.py)، [`pii_detection.py`](../../auto_client_acquisition/data_os/pii_detection.py) | Ready | Partial |
| Lead scoring + drafts | Lead Intelligence | [`../../auto_client_acquisition/commercial_engagements/lead_intelligence_sprint.py`](../../auto_client_acquisition/commercial_engagements/lead_intelligence_sprint.py)، `revenue_os` | Ready | Partial |
| Proof pack generation | All services | [`../../auto_client_acquisition/reporting_os/proof_pack.py`](../../auto_client_acquisition/reporting_os/proof_pack.py) | Ready | Partial |
| Governance checks | All services | [`../../auto_client_acquisition/governance_os/`](../../auto_client_acquisition/governance_os/)، [`compliance_os/`](../../auto_client_acquisition/compliance_os/) | Ready | Partial |
| Answer + citations | Company Brain | [`../../auto_client_acquisition/knowledge_os/answer_with_citations.py`](../../auto_client_acquisition/knowledge_os/answer_with_citations.py)، API `api/routers/knowledge_v10.py` | Ready | Partial |
| Quick Win rollup | AI Quick Win | [`../../auto_client_acquisition/commercial_engagements/quick_win_ops.py`](../../auto_client_acquisition/commercial_engagements/quick_win_ops.py) | Ready | Partial |
| Workflow automation UI | أتمتة متقدمة | `workflow_os_v10/`، `delivery_factory/` (لا يوجد `workflow_builder.py` واحد بسيط) | Beta | Not Ready |

**قرار:** أي خدمة تعتمد على صف **Production = Not Ready** تبقى **Beta** حتى تكتمل القدرة أو يُحدَّد نطاق «مساعدة يدوية + أدواء محدودة».

خرائط أوسع: [`MODULE_MAP.md`](MODULE_MAP.md)، [`../commercial/CODE_MAP_OS_TO_MODULES_AR.md`](../commercial/CODE_MAP_OS_TO_MODULES_AR.md).
