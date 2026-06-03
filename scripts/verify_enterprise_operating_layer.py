from pathlib import Path
import sys

required = [
    "docs/company_os/enterprise/ENTERPRISE_OPERATING_MODEL_AR.md",
    "docs/company_os/enterprise/SERVICE_CATALOG_AR.md",
    "docs/company_os/enterprise/SLA_AND_SUPPORT_MODEL_AR.md",
    "docs/company_os/enterprise/INCIDENT_RESPONSE_RUNBOOK_AR.md",
    "docs/company_os/security/AI_AGENT_SECURITY_MODEL_AR.md",
    "docs/company_os/security/SECRET_ROTATION_RUNBOOK_AR.md",
    "docs/company_os/security/SECURITY_CHECKLIST_AR.md",
    "docs/company_os/customer_success/CUSTOMER_SUCCESS_OS_AR.md",
    "docs/company_os/customer_success/CLIENT_INTAKE_TEMPLATE_AR.md",
    "docs/company_os/customer_success/P2_WEEKLY_REVIEW_TEMPLATE_AR.md",
    "docs/company_os/quality/QUALITY_GATE_MODEL_AR.md",
    "scripts/dealix_enterprise_readiness.py",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("ENTERPRISE_OPERATING_LAYER=FAIL")
    for p in missing:
        print("missing=" + p)
    sys.exit(1)

print("ENTERPRISE_OPERATING_LAYER=PASS")
for p in required:
    print("ok=" + p)
