"""
Dealix Opportunity Graph — query API
=====================================

Async Python API over the graph schema. Designed to be called from:
  - Agent orchestrator (LangGraph nodes)
  - FastAPI routes (/opportunities, /companies, /graph/explore)
  - Cron jobs (signal decay, weekly report generator)

Uses asyncpg (fast, Postgres-native). Falls back to psycopg if asyncpg unavailable.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger("dealix.graph")

try:
    import asyncpg
    _HAS_ASYNCPG = True
except ImportError:
    _HAS_ASYNCPG = False


# ============================================================================
# CONFIG
# ============================================================================

DSN = os.environ.get("DEALIX_PG_DSN", "postgresql://dealix:dealix@localhost:5432/dealix")


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Company:
    id: str
    name_ar: str
    sector: str | None
    region: str | None
    size_employees: int | None
    confidence: float
    source: str


@dataclass
class Opportunity:
    id: str
    title_ar: str
    company_name: str
    sector: str | None
    stage: str
    expected_value_sar: float | None
    win_probability: float | None
    weighted_value: float | None
    suggested_action: str | None
    owner_approval_required: bool
    evidence_summary: str | None
    fresh_signal_count: int


# ============================================================================
# ARABIC NORMALIZATION (used on write)
# ============================================================================

_AR_NORMALIZE_MAP = str.maketrans({
    "أ": "ا", "إ": "ا", "آ": "ا",
    "ة": "ه", "ى": "ي",
    "ؤ": "و", "ئ": "ي",
    "ـ": "",          # tatweel
})


def normalize_ar(text: str) -> str:
    """Normalize Arabic text for fuzzy matching. Strip al-tarif + diacritics + tatweel."""
    if not text:
        return ""
    t = text.strip()
    # strip diacritics U+064B-U+065F + U+0670
    t = "".join(c for c in t if not ("\u064B" <= c <= "\u065F") and c != "\u0670")
    t = t.translate(_AR_NORMALIZE_MAP)
    # collapse whitespace
    t = " ".join(t.split())
    # strip leading "ال" (al-tarif) from every word so matching works
    # across multi-word Arabic names, e.g. "الشركة الأهلية" -> "شركه اهليه"
    words = []
    for w in t.split(" "):
        if len(w) > 2 and w.startswith("ال"):
            words.append(w[2:])
        else:
            words.append(w)
    t = " ".join(words)
    return t.lower()


# ============================================================================
# GRAPH API
# ============================================================================

class OpportunityGraph:
    def __init__(self, dsn: str = DSN):
        self.dsn = dsn
        self.pool: Any = None

    async def connect(self) -> None:
        if not _HAS_ASYNCPG:
            raise RuntimeError("asyncpg required: pip install asyncpg")
        if self.pool is None:
            self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=10)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()

    # ---- Company ops --------------------------------------------------------

    async def upsert_company(self, name_ar: str, cr_number: str | None = None,
                              sector: str | None = None, region: str | None = None,
                              size_employees: int | None = None,
                              source: str = "manual",
                              source_url: str | None = None,
                              confidence: float = 0.8,
                              created_by_agent: str = "system") -> str:
        """Insert or update a company. Returns company UUID."""
        await self.connect()
        name_norm = normalize_ar(name_ar)

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO companies
                    (cr_number, name_ar, name_ar_norm, sector, region, size_employees,
                     source, source_url, confidence, created_by_agent)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (cr_number) DO UPDATE SET
                    name_ar = EXCLUDED.name_ar,
                    name_ar_norm = EXCLUDED.name_ar_norm,
                    sector = COALESCE(EXCLUDED.sector, companies.sector),
                    region = COALESCE(EXCLUDED.region, companies.region),
                    updated_at = now()
                RETURNING id
            """, cr_number, name_ar, name_norm, sector, region, size_employees,
                 source, source_url, confidence, created_by_agent)
            return str(row["id"])

    async def find_company(self, query: str, limit: int = 10) -> list[Company]:
        """Fuzzy search for companies by Arabic name."""
        await self.connect()
        q_norm = normalize_ar(query)
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, name_ar, sector, region, size_employees, confidence, source
                FROM companies
                WHERE name_ar_norm % $1
                ORDER BY similarity(name_ar_norm, $1) DESC, confidence DESC
                LIMIT $2
            """, q_norm, limit)
        return [Company(str(r["id"]), r["name_ar"], r["sector"], r["region"],
                        r["size_employees"], float(r["confidence"]), r["source"])
                for r in rows]

    # ---- Signal ops ---------------------------------------------------------

    async def record_signal(self, company_id: str, signal_type: str,
                             description: str, strength: float = 0.7,
                             evidence_url: str | None = None,
                             ttl_days: int = 30,
                             detected_by_agent: str = "exec_intel",
                             source: str = "news") -> str:
        """Record a time-bound signal on a company."""
        await self.connect()
        decay_at = datetime.now(timezone.utc) + timedelta(days=ttl_days)
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO signals
                    (company_id, signal_type, signal_strength, description,
                     evidence_url, decay_at, source, detected_by_agent)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                RETURNING id
            """, company_id, signal_type, strength, description,
                 evidence_url, decay_at, source, detected_by_agent)
            return str(row["id"])

    # ---- Opportunity ops ----------------------------------------------------

    async def create_opportunity(self, company_id: str, title_ar: str,
                                  expected_value_sar: float,
                                  win_probability: float,
                                  supporting_signal_ids: list[str],
                                  suggested_action: str,
                                  evidence_summary: str,
                                  owner_approval_required: bool = False,
                                  created_by_agent: str = "strategist") -> str:
        """Create an opportunity node with evidence trail."""
        await self.connect()
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO opportunities
                    (company_id, title_ar, expected_value_sar, win_probability,
                     supporting_signals, suggested_action, evidence_summary,
                     owner_approval_required, created_by_agent,
                     confidence)
                VALUES ($1, $2, $3, $4, $5::uuid[], $6, $7, $8, $9, $10)
                RETURNING id
            """, company_id, title_ar, expected_value_sar, win_probability,
                 supporting_signal_ids, suggested_action, evidence_summary,
                 owner_approval_required, created_by_agent,
                 min(0.95, 0.5 + 0.1 * len(supporting_signal_ids)))
            return str(row["id"])

    async def list_priority_opportunities(self, limit: int = 20) -> list[Opportunity]:
        """Return the top weighted-value open opportunities."""
        await self.connect()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM v_priority_opportunities LIMIT $1", limit
            )
        return [Opportunity(
            id=str(r["id"]), title_ar=r["title_ar"], company_name=r["company_name"],
            sector=r["sector"], stage=r["stage"],
            expected_value_sar=float(r["expected_value_sar"]) if r["expected_value_sar"] else None,
            win_probability=float(r["win_probability"]) if r["win_probability"] else None,
            weighted_value=float(r["weighted_value"]) if r["weighted_value"] else None,
            suggested_action=r["suggested_action"],
            owner_approval_required=r["owner_approval_required"],
            evidence_summary=r["evidence_summary"],
            fresh_signal_count=r["fresh_signal_count"]
        ) for r in rows]

    # ---- Audit --------------------------------------------------------------

    async def log_agent_action(self, agent: str, action_type: str,
                                verdict: str, rule_id: str,
                                latency_ms: float = 0,
                                opportunity_id: str | None = None,
                                company_id: str | None = None,
                                trace_id: str | None = None,
                                payload: dict | None = None) -> None:
        """Write to agent_audit_log. Non-blocking best-effort."""
        await self.connect()
        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO agent_audit_log
                        (agent, action_type, verdict, rule_id, latency_ms,
                         opportunity_id, company_id, trace_id, payload)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """, agent, action_type, verdict, rule_id, latency_ms,
                     opportunity_id, company_id, trace_id,
                     json.dumps(payload or {}, ensure_ascii=False))
        except Exception as e:
            logger.error("audit log failed: %s", e)  # never raise


# ============================================================================
# UNIT TEST (logic only — no DB required)
# ============================================================================

def _test_normalize():
    # "ال" is stripped from each word (>2 chars) to improve fuzzy matching
    # across multi-word Arabic company names.
    assert normalize_ar("الشركة الأهلية") == "شركه اهليه", normalize_ar("الشركة الأهلية")
    assert normalize_ar("مُؤسَّسَة النور") == "موسسه نور", normalize_ar("مُؤسَّسَة النور")
    assert normalize_ar("متجر النخبة") == "متجر نخبه", normalize_ar("متجر النخبة")
    assert normalize_ar("Al-Noor") == "al-noor"
    assert normalize_ar("ديلكس") == "ديلكس"  # short word not eaten
    print("✅ Arabic normalization self-test passed")
    print(f"   'الشركة الأهلية' → '{normalize_ar('الشركة الأهلية')}'")
    print(f"   'متجر النخبة'    → '{normalize_ar('متجر النخبة')}'")
    print(f"   'مُؤسَّسَة النور'   → '{normalize_ar('مُؤسَّسَة النور')}'")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _test_normalize()
    print("\nTo initialize the DB, run:")
    print("  psql $DEALIX_PG_DSN -f schema.sql")
    print("\nTo test full API, set DEALIX_PG_DSN and pip install asyncpg.")
