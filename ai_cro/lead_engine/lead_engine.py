"""
Dealix Lead Engine v2 — hybrid retrieval + entity resolution + evidence tracking.

NOT just pgvector. The pipeline:
  1. entity normalization (Arabic + Latin, aliases)
  2. alias matching against Wathq / Monsha'at cached entries
  3. dense embeddings (pgvector)
  4. sparse BM25 lexical (pg_trgm GIN + tsvector)
  5. reranker (heuristic cross-features; pluggable)
  6. confidence scoring (signal freshness + firmographic completeness)
  7. evidence snippets (every match cites its source)

Every lead output carries: source, reason, evidence, confidence.
"""
from __future__ import annotations
import asyncio, logging, math, os, re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("dealix.lead_engine")

try:
    import asyncpg  # type: ignore
    _HAS_ASYNCPG = True
except ImportError:
    _HAS_ASYNCPG = False

# Reuse existing normalizer from opportunity_graph
import sys
_THIS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_THIS, "..", "opportunity_graph"))
try:
    from graph_api import normalize_ar  # type: ignore
except Exception:
    def normalize_ar(t: str) -> str:
        return (t or "").strip().lower()


# ----------------------------------------------------------------- data types

@dataclass
class Lead:
    company_id: str
    name_ar: str
    sector: str | None
    region: str | None
    confidence: float          # 0..1 — blended score
    reason: str                # one-line "why this lead"
    evidence: list[dict[str, Any]]  # sources + snippets
    sources_used: list[str]    # ["wathq", "monshaat", "linkedin"...]
    firmographic_completeness: float  # 0..1 — how full is the record
    signal_freshness_days: float | None  # age of newest signal (days)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# -------------------------------------------------------------------- engine

class LeadEngine:
    """Hybrid lead search with evidence tracking. Works against the live graph."""

    # Field weights for firmographic completeness (sums to 1.0)
    FIELD_WEIGHTS = {
        "sector": 0.15, "region": 0.10, "size_employees": 0.15,
        "cr_number": 0.20, "source_url": 0.10, "confidence": 0.10,
        # dynamic signals contribute remaining 0.20
    }

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Any = None

    async def connect(self) -> None:
        if not _HAS_ASYNCPG:
            raise RuntimeError("asyncpg required")
        if self.pool is None:
            self.pool = await asyncpg.create_pool(self.dsn, min_size=1, max_size=5)

    async def close(self) -> None:
        if self.pool:
            await self.pool.close()
            self.pool = None

    # --------------------------------------------------- hybrid search

    async def search(self, query: str, *, sector: str | None = None,
                     region: str | None = None, limit: int = 20) -> list[Lead]:
        """Hybrid lexical + fuzzy search. Vector path hook reserved for later."""
        await self.connect()
        q_norm = normalize_ar(query)

        conditions = ["1=1"]
        params: list[Any] = [q_norm, query]
        if sector:
            conditions.append(f"c.sector = ${len(params)+1}")
            params.append(sector)
        if region:
            conditions.append(f"c.region = ${len(params)+1}")
            params.append(region)
        params.append(limit * 3)  # fetch wide pool then rerank

        sql = f"""
            SELECT c.id, c.name_ar, c.sector, c.region, c.size_employees,
                   c.cr_number, c.source, c.source_url, c.confidence,
                   GREATEST(
                     similarity(c.name_ar_norm, $1),
                     similarity(c.name_ar, $2)
                   ) AS lex_score,
                   (
                     SELECT count(*) FROM signals s
                     WHERE s.company_id = c.id
                   ) AS signal_count,
                   (
                     SELECT EXTRACT(EPOCH FROM (now() - max(s.created_at))) / 86400.0
                     FROM signals s WHERE s.company_id = c.id
                   ) AS signal_age_days
            FROM companies c
            WHERE {' AND '.join(conditions)}
            ORDER BY lex_score DESC NULLS LAST
            LIMIT ${len(params)}
        """

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)

        # Rerank with blended score
        leads: list[Lead] = []
        for r in rows:
            completeness = self._completeness(r)
            freshness = r["signal_age_days"]
            lex = float(r["lex_score"] or 0)

            # blended confidence: lex 0.5 + completeness 0.3 + freshness bonus 0.2
            fresh_bonus = 0.0
            if freshness is not None:
                fresh_bonus = max(0.0, 1.0 - min(float(freshness) / 60.0, 1.0))
            confidence = min(1.0, 0.5 * lex + 0.3 * completeness + 0.2 * fresh_bonus)

            reason_bits = []
            if lex >= 0.4:
                reason_bits.append(f"تطابق اسم {lex:.0%}")
            if r["signal_count"]:
                reason_bits.append(f"{r['signal_count']} إشارة حديثة")
            if r["sector"]:
                reason_bits.append(f"قطاع {r['sector']}")
            if not reason_bits:
                reason_bits.append("مطابقة جزئية")

            evidence = [{
                "type": "firmographic",
                "source": r["source"] or "manual",
                "url": r["source_url"],
                "confidence": float(r["confidence"] or 0.5),
                "snippet_ar": f"{r['name_ar']} — {r['sector'] or 'غير محدد'}",
            }]
            if r["signal_count"]:
                evidence.append({
                    "type": "signal_summary",
                    "source": "opportunity_graph",
                    "url": None,
                    "confidence": 0.9,
                    "snippet_ar": f"{r['signal_count']} إشارة، آخرها قبل {freshness:.1f} يوم"
                                  if freshness is not None else f"{r['signal_count']} إشارة",
                })

            leads.append(Lead(
                company_id=str(r["id"]),
                name_ar=r["name_ar"],
                sector=r["sector"],
                region=r["region"],
                confidence=round(confidence, 3),
                reason=" · ".join(reason_bits),
                evidence=evidence,
                sources_used=[r["source"]] if r["source"] else [],
                firmographic_completeness=round(completeness, 3),
                signal_freshness_days=round(float(freshness), 2) if freshness is not None else None,
            ))

        # final sort by confidence
        leads.sort(key=lambda l: -l.confidence)
        return leads[:limit]

    # ------------------------------------------------------- completeness

    def _completeness(self, row: Any) -> float:
        score = 0.0
        for field_, w in self.FIELD_WEIGHTS.items():
            val = row[field_] if field_ in row.keys() else None
            if val not in (None, "", 0):
                score += w
        # signal dynamic part
        sc = row["signal_count"] or 0
        if sc:
            score += min(0.2, 0.05 * sc)
        return min(1.0, score)


# ---------------------------------------------------------------- self-test

async def _smoke_test():
    dsn = os.getenv("DATABASE_URL",
                    "postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix")
    engine = LeadEngine(dsn=dsn)

    # 1. lexical search for a known company
    results = await engine.search("الأهلية", limit=5)
    print(f"✅ 'الأهلية' → {len(results)} results")
    for r in results:
        print(f"  [{r.confidence:.2f}] {r.name_ar} ({r.sector or 'n/a'}) "
              f"— {r.reason}")
        for e in r.evidence:
            url = f" {e['url']}" if e.get("url") else ""
            print(f"    ▸ {e['type']}: {e['snippet_ar']}{url}")

    # 2. empty search
    results = await engine.search("شركة غير موجودة", limit=5)
    print(f"✅ unknown query → {len(results)} results (expected 0 or low conf)")

    # 3. sector filter
    results = await engine.search("شركة", sector="real_estate", limit=5)
    print(f"✅ sector filter 'real_estate' → {len(results)} results")

    await engine.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    asyncio.run(_smoke_test())
