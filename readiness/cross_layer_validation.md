# Cross-Layer Validation

## Required chain
Inbound Lead  
→ tenant detected  
→ RBAC checked  
→ agent routed  
→ assurance contract evaluated  
→ runtime safety checked  
→ workflow run registered  
→ risky action escalated  
→ approval queued  
→ approval granted  
→ value metric stored with `source_ref`  
→ trace complete  
→ rollback requested and approval-gated  
→ proposal apply blocked until approval

## Enforcement
- Validation is codified in `tests/test_enterprise_control_plane_e2e.py`.
- Release gate is codified in `scripts/verify_enterprise_control_plane.sh`.
