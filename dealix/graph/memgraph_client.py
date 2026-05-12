"""
Memgraph — high-performance knowledge graph for account ↔ contact ↔
deal ↔ note relationships.

Inert without MEMGRAPH_URL. We use Cypher over the Bolt protocol when
the official driver is installed; otherwise we expose `ping()` for
health-checks only.

Used by ICP-matcher v2 for queries like:
  "Who else at this company should we talk to?"
  "Which deals reference the same partner?"
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class GraphEdge:
    source: str
    target: str
    label: str


def is_configured() -> bool:
    return bool(os.getenv("MEMGRAPH_URL", "").strip())


def _conn_args() -> dict[str, Any]:
    return {
        "host": os.getenv("MEMGRAPH_HOST", "127.0.0.1"),
        "port": int(os.getenv("MEMGRAPH_PORT", "7687")),
        "username": os.getenv("MEMGRAPH_USER", ""),
        "password": os.getenv("MEMGRAPH_PASSWORD", ""),
    }


async def ping() -> bool:
    """Return True when Memgraph is reachable."""
    if not is_configured():
        return False
    try:
        import mgclient  # type: ignore
    except ImportError:
        log.info("mgclient_sdk_not_installed")
        return False
    try:
        conn = mgclient.connect(**_conn_args())
        cur = conn.cursor()
        cur.execute("RETURN 1")
        cur.fetchall()
        conn.close()
        return True
    except Exception:
        log.exception("memgraph_ping_failed")
        return False


async def upsert_edge(edge: GraphEdge) -> bool:
    if not is_configured():
        return False
    try:
        import mgclient  # type: ignore
    except ImportError:
        return False
    try:
        conn = mgclient.connect(**_conn_args())
        cur = conn.cursor()
        cur.execute(
            "MERGE (a:Node {id: $src}) "
            "MERGE (b:Node {id: $tgt}) "
            f"MERGE (a)-[:{edge.label}]->(b)",
            {"src": edge.source, "tgt": edge.target},
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        log.exception("memgraph_upsert_failed")
        return False
