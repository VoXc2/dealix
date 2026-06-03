# Sovereign Data Model — نموذج البيانات الأعلى

كيانات مرجعية لجعل Dealix **قابلة للإدارة كقابضة** (تصميم منطقي — لا يستبدل `docs/architecture/DATA_MODEL.md` التفصيلي).

## كيانات أساسية

Client · Workspace · Project · Capability · Service · Workflow · DataSource · Dataset · AIRun · GovernanceDecision · Approval · AuditEvent · ProofEvent · ProofPack · CapitalAsset · FeatureCandidate · PlaybookUpdate · BusinessUnit · VentureSignal · Partner · Standard · AcademyAsset

## علاقات مختصرة

- Client **has** Projects  
- Project **improves** Capabilities  
- Project **uses** Services  
- Service **produces** Workflows  
- Workflow **uses** DataSources  
- AIRun **belongs to** Workflow  
- GovernanceDecision **gates** AIRun أو Output  
- ProofEvent **belongs to** Project  
- CapitalAsset **comes from** Proof أو Delivery  
- FeatureCandidate **comes from** تكرار عمل يدوي / Capital  
- BusinessUnit **owns** Services  
- VentureSignal **comes from** نضج BusinessUnit  

**مرجع تقني:** [`../architecture/DATA_MODEL.md`](../architecture/DATA_MODEL.md) · [`../product/MVP_DATA_MODEL.md`](../product/MVP_DATA_MODEL.md)

**صعود:** [`../command/COMMAND_SYSTEM.md`](../command/COMMAND_SYSTEM.md) · [`../institutional/DEALIX_CONSTITUTION.md`](../institutional/DEALIX_CONSTITUTION.md)
