"""DesignOps generators — bilingual artifact composers.

Six generators that turn data into bilingual (Arabic-first / English
-secondary) artifacts. NO LLM call. NO external HTTP. Pure templating
+ composition over existing v5/v6 modules.

Public API:
    from auto_client_acquisition.designops.generators import (
        generate_mini_diagnostic,
        generate_proof_pack,
        generate_executive_weekly_pack,
        generate_proposal_page,
        generate_pricing_page,
        generate_customer_room_dashboard,
        html_renderer,
        markdown_renderer,
    )
"""
from auto_client_acquisition.designops.generators import (
    html_renderer,
    markdown_renderer,
)
from auto_client_acquisition.designops.generators.customer_room_dashboard import (
    generate_customer_room_dashboard,
)
from auto_client_acquisition.designops.generators.executive_weekly_pack import (
    generate_executive_weekly_pack,
)
from auto_client_acquisition.designops.generators.mini_diagnostic import (
    generate_mini_diagnostic,
)
from auto_client_acquisition.designops.generators.pricing_page import (
    generate_pricing_page,
)
from auto_client_acquisition.designops.generators.proof_pack import (
    generate_proof_pack,
)
from auto_client_acquisition.designops.generators.proposal_page import (
    generate_proposal_page,
)

__all__ = [
    "generate_customer_room_dashboard",
    "generate_executive_weekly_pack",
    "generate_mini_diagnostic",
    "generate_pricing_page",
    "generate_proof_pack",
    "generate_proposal_page",
    "html_renderer",
    "markdown_renderer",
]
