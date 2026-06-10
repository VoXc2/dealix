import sys
from pathlib import Path

required = [
    "docs/brand/DEALIX_VISUAL_IDENTITY_AR.md",
    "docs/brand/DEALIX_PRESENTATION_STYLE_GUIDE_AR.md",
    "docs/pitch/DEALIX_MASTER_PITCH_DECK_AR.md",
    "docs/pitch/DEALIX_MASTER_PITCH_DECK_EN.md",
    "docs/conversion/DEALIX_HIGH_CONVICTION_SALES_PAGE_AR.md",
    "docs/conversion/DEALIX_OBJECTION_DEEP_PERSUASION_AR.md",
    "docs/conversion/DEALIX_PRODUCTIZED_OFFERS_MATRIX_AR.md",
]

missing = [p for p in required if not Path(p).exists()]
if missing:
    print("BRAND_PITCH_CONVERSION_LAYER=FAIL")
    for p in missing:
        print("missing=" + p)
    sys.exit(1)

print("BRAND_PITCH_CONVERSION_LAYER=PASS")
for p in required:
    print("ok=" + p)
