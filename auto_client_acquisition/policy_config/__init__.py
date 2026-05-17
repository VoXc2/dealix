"""Policy-as-code: declarative governance config consumed by runtime modules.

YAML files in this package are the source of truth for approval routing, doctrine
claim reasons, lead scoring weights, and lead-lifecycle stage transitions. Defaults
are byte-equivalent to the values previously hardcoded in Python, so behaviour is
unchanged — config makes governance editable and auditable, never weaker.
"""

from __future__ import annotations

from auto_client_acquisition.policy_config.loader import (
    CONFIG_DIR,
    load_policy,
    policy_path,
)

__all__ = ["CONFIG_DIR", "load_policy", "policy_path"]
