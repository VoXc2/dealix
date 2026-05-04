"""
Learning — Phase 3 skeleton.

Three pure-data analyzers that mine existing tables for patterns:
    - objection_library: which objection responses worked best?
    - message_experiments: which message templates got the highest reply rate?
    - channel_performance: which channels converted at each stage?

Phase 3 is light-weight on launch (real data is sparse < 30 conversations).
The full version triggers on 3 paid pilots + ≥30 conversations.
"""

from auto_client_acquisition.learning.channel_performance import (
    analyze_channels,
)
from auto_client_acquisition.learning.message_experiments import (
    score_messages,
)
from auto_client_acquisition.learning.objection_library import (
    mine_objections,
)

__all__ = ["analyze_channels", "score_messages", "mine_objections"]
