from pathlib import Path
import sys

required = [
    "docs/data_room/DEALIX_COMPANY_ONE_PAGER_AR.md",
    "docs/data_room/DEALIX_BOARD_BRIEF_AR.md",
    "docs/data_room/INVESTOR_PARTNER_MEMO_AR.md",
    "docs/proof_factory/P1_PROOF_PACK_TEMPLATE_AR.md",
    "docs/delivery_os/P1_DELIVERY_SOP_AR.md",
    "docs/delivery_os/P2_DELIVERY_SOP_AR.md",
    "docs/partner_os/PARTNER_REFERRAL_SYSTEM_AR.md",
    "docs/company_os/metrics/NORTH_STAR_METRICS_AR.md",
    "scripts/dealix_scale_brief.py",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("SCALE_COMPANY_LAYER=FAIL")
    for p in missing:
        print("missing=" + p)
    sys.exit(1)

print("SCALE_COMPANY_LAYER=PASS")
for p in required:
    print("ok=" + p)
