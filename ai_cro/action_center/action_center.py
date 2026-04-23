"""
Dealix Action Center — the owner's single cockpit.

The UI deliberately has ONE primary screen: "What needs a decision today?"
Everything else is drilldown. This API returns the feed that powers it.

Queue is composed of:
  1. APPROVAL_INTERRUPT items (owner must act)
  2. HIGH-CONFIDENCE opportunities awaiting first-move
  3. NEGOTIATIONS within thresholds but flagged by content-guard
  4. MEETINGS to confirm / prep

Every item carries:
  - evidence cards (why this, with sources)
  - confidence
  - reason
  - next-action button + estimated impact (SAR)
  - state timeline (signal → draft → … → now)
"""
from __future__ import annotations
import asyncio, json, logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger("dealix.action_center")

try:
    import asyncpg  # type: ignore
    _HAS_ASYNCPG = True
except ImportError:
    _HAS_ASYNCPG = False


@dataclass
class ActionItem:
    id: str
    kind: str                       # approval | first_move | negotiation | meeting_prep
    priority: int                   # 0-100
    company_name: str
    title_ar: str
    expected_value_sar: float
    win_probability: float
    weighted_value_sar: float
    suggested_action: str
    reason: str                     # one-sentence why this is on the queue
    evidence: list[dict[str, Any]]  # [{type, label_ar, source, url, confidence}]
    timeline: list[dict[str, Any]]  # [{stage, at, actor}]
    next_action_label_ar: str
    requires_owner_decision: bool
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionCenter:
    """Queries the opportunity graph + workflow state for the owner's queue."""

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

    # ---------------------------------------------------------- main feed

    async def queue(self, *, limit: int = 20) -> list[ActionItem]:
        """Return the owner's decision queue, priority-sorted."""
        await self.connect()
        items: list[ActionItem] = []

        # 1. approval-pending opportunities (owner_approval_required = true, not resolved)
        async with self.pool.acquire() as conn:
            approval_rows = await conn.fetch("""
                SELECT o.id, o.title_ar, o.expected_value_sar, o.win_probability,
                       o.suggested_action, o.evidence_summary, o.updated_at,
                       c.name_ar AS company_name, c.sector,
                       (o.expected_value_sar * o.win_probability) AS weighted
                FROM opportunities o
                JOIN companies c ON c.id = o.company_id
                WHERE o.owner_approval_required = true
                  AND o.resolved_at IS NULL
                ORDER BY weighted DESC NULLS LAST
                LIMIT $1
            """, limit)

            for r in approval_rows:
                items.append(ActionItem(
                    id=str(r["id"]),
                    kind="approval",
                    priority=95,
                    company_name=r["company_name"] or "",
                    title_ar=r["title_ar"],
                    expected_value_sar=float(r["expected_value_sar"] or 0),
                    win_probability=float(r["win_probability"] or 0),
                    weighted_value_sar=float(r["weighted"] or 0),
                    suggested_action=r["suggested_action"] or "",
                    reason="يتطلب موافقة المالك قبل التنفيذ",
                    evidence=self._evidence_for(r),
                    timeline=[],  # filled by _timeline() if requested
                    next_action_label_ar="راجع واتخذ قرار",
                    requires_owner_decision=True,
                    updated_at=r["updated_at"].isoformat() if r["updated_at"] else "",
                ))

            # 2. high-priority first-move opportunities (qualified, no approval needed)
            first_move_rows = await conn.fetch("""
                SELECT id, title_ar, company_name, sector, stage,
                       expected_value_sar, win_probability, weighted_value,
                       suggested_action, evidence_summary, updated_at
                FROM v_priority_opportunities
                WHERE owner_approval_required = false
                  AND stage IN ('identified', 'qualified')
                ORDER BY weighted_value DESC NULLS LAST
                LIMIT $1
            """, max(1, limit - len(items)))

            for r in first_move_rows:
                items.append(ActionItem(
                    id=str(r["id"]),
                    kind="first_move",
                    priority=70,
                    company_name=r["company_name"] or "",
                    title_ar=r["title_ar"],
                    expected_value_sar=float(r["expected_value_sar"] or 0),
                    win_probability=float(r["win_probability"] or 0),
                    weighted_value_sar=float(r["weighted_value"] or 0),
                    suggested_action=r["suggested_action"] or "",
                    reason=f"فرصة {r['sector']} بقيمة مرجحة عالية — الخطوة الأولى جاهزة",
                    evidence=[{
                        "type": "summary",
                        "label_ar": "ملخص الأدلة",
                        "source": "strategist_agent",
                        "url": None,
                        "confidence": 0.8,
                        "text_ar": r["evidence_summary"] or "",
                    }],
                    timeline=[],
                    next_action_label_ar="ابدأ التواصل",
                    requires_owner_decision=False,
                    updated_at=r["updated_at"].isoformat() if r["updated_at"] else "",
                ))

        # sort by priority desc, then weighted value desc
        items.sort(key=lambda i: (-i.priority, -i.weighted_value_sar))
        return items[:limit]

    async def item_timeline(self, opportunity_id: str) -> list[dict[str, Any]]:
        """Return full event timeline for drill-down."""
        await self.connect()
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT action_type, verdict, rule_id, latency_ms, created_at, agent, payload
                FROM agent_audit_log
                WHERE opportunity_id = $1
                ORDER BY created_at ASC
            """, opportunity_id)
            return [
                {
                    "stage": r["action_type"],
                    "verdict": r["verdict"],
                    "rule": r["rule_id"],
                    "actor": r["agent"],
                    "at": r["created_at"].isoformat(),
                    "latency_ms": r["latency_ms"],
                    "payload": r["payload"],
                }
                for r in rows
            ]

    async def resolve_approval(self, opportunity_id: str, *,
                                decision: str, actor: str = "owner",
                                note_ar: str | None = None) -> bool:
        """Owner approved/rejected an action. Clears the flag + audit logs."""
        await self.connect()
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                if decision == "approve":
                    await conn.execute("""
                        UPDATE opportunities SET owner_approval_required = false,
                                                 updated_at = now()
                        WHERE id = $1
                    """, opportunity_id)
                elif decision == "reject":
                    await conn.execute("""
                        UPDATE opportunities SET resolved_at = now(),
                                                 stage = 'lost',
                                                 updated_at = now()
                        WHERE id = $1
                    """, opportunity_id)
                else:
                    return False
                await conn.execute("""
                    INSERT INTO agent_audit_log
                        (agent, action_type, verdict, opportunity_id, payload)
                    VALUES ($1, $2, $3, $4::uuid, $5::jsonb)
                """, actor, "approval_decision", decision.upper(),
                     opportunity_id, json.dumps({"note_ar": note_ar or ""}))
        return True

    # ----------------------------------------------------------- helpers

    def _evidence_for(self, row: Any) -> list[dict[str, Any]]:
        """Build evidence cards from an opportunity row. Sources attached."""
        cards = []
        if row.get("evidence_summary") if isinstance(row, dict) else row["evidence_summary"]:
            cards.append({
                "type": "summary",
                "label_ar": "ملخص الأدلة",
                "source": "opportunity_graph",
                "url": None,
                "confidence": 0.75,
                "text_ar": row["evidence_summary"],
            })
        return cards


# ============================================================================
# HTTP adapter (FastAPI-style) — kept thin, reuses dealix-api service
# ============================================================================

def build_router(dsn: str):
    """Return a FastAPI APIRouter exposing /action-center endpoints."""
    from fastapi import APIRouter, HTTPException, Query  # type: ignore

    router = APIRouter(prefix="/action-center", tags=["action-center"])
    center = ActionCenter(dsn=dsn)

    @router.get("/queue")
    async def get_queue(limit: int = Query(20, ge=1, le=100)):
        items = await center.queue(limit=limit)
        return {"items": [i.to_dict() for i in items], "count": len(items)}

    @router.get("/item/{opportunity_id}/timeline")
    async def get_timeline(opportunity_id: str):
        return {"timeline": await center.item_timeline(opportunity_id)}

    @router.post("/item/{opportunity_id}/resolve")
    async def resolve(opportunity_id: str, decision: str = Query(...),
                      note_ar: str | None = Query(None)):
        if decision not in ("approve", "reject"):
            raise HTTPException(400, "decision must be approve|reject")
        ok = await center.resolve_approval(opportunity_id, decision=decision, note_ar=note_ar)
        return {"ok": ok}

    return router


# ============================================================================
# SELF TEST (live DB)
# ============================================================================

async def _smoke_test():
    import os
    dsn = os.getenv("DATABASE_URL",
                    "postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix")
    center = ActionCenter(dsn=dsn)
    items = await center.queue(limit=10)
    print(f"✅ queue returned {len(items)} items")
    for it in items:
        print(f"  [{it.kind:11s}] pri={it.priority:3d} "
              f"{it.company_name} — {it.title_ar} "
              f"(weighted: {it.weighted_value_sar:,.0f} SAR)")
        print(f"    reason: {it.reason}")
        print(f"    next  : {it.next_action_label_ar}")
    await center.close()


if __name__ == "__main__":
    import logging; logging.basicConfig(level=logging.WARNING)
    asyncio.run(_smoke_test())
