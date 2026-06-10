import sys
from pathlib import Path

required = [
    "docs/company_os/STRATEGIC_COMMAND_LAYER_AR.md",
    "docs/company_os/CEO_WAR_ROOM_AR.md",
    "docs/company_os/growth/STRATEGIC_GROWTH_SYSTEM_AR.md",
    "docs/company_os/finance/FINANCE_OS_AR.md",
    "docs/company_os/governance/AGENT_GOVERNANCE_AR.md",
    "docs/company_os/sops/FOUNDER_24H_OPERATING_SOP_AR.md",
    "data/company_os/strategic_backlog.json",
    "scripts/dealix_strategic_brief.py",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("STRATEGIC_COMMAND_LAYER=FAIL")
    for p in missing:
        print(f"missing={p}")
    sys.exit(1)

print("STRATEGIC_COMMAND_LAYER=PASS")
for p in required:
    print(f"ok={p}")
