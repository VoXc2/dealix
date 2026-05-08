"""
ARQ async task worker — registers all background job functions.
عامل المهام غير المتزامن — يسجّل جميع وظائف المهام الخلفية.

ARQ (async Redis Queue) provides:
  - Redis-backed job queue (no extra broker infra beyond Redis)
  - Automatic retry with exponential backoff
  - Job deduplication
  - Cron scheduling

Startup command:
    arq core.tasks.worker.WorkerSettings

Job submission from FastAPI:
    from arq import create_pool
    redis = await create_pool(RedisSettings.from_url(settings.redis_url))
    await redis.enqueue_job("run_lead_scoring", lead_id="abc123", tenant_id="t1")
"""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from arq import cron
from arq.connections import RedisSettings

from core.config.settings import get_settings
from core.logging import get_logger

logger = get_logger(__name__)


# ── Job Functions ─────────────────────────────────────────────────

async def run_lead_scoring(ctx: dict[str, Any], lead_id: str, tenant_id: str) -> dict[str, Any]:
    """
    Score a lead using the ICP fit + urgency heuristics + LLM enrichment.
    تقييم العميل المحتمل باستخدام نماذج الذكاء الاصطناعي.
    """
    from core.agents.lead_scoring import LeadScoringAgent
    from db.session import AsyncSessionLocal

    logger.info("job_lead_scoring_start", lead_id=lead_id, tenant_id=tenant_id)
    async with AsyncSessionLocal() as session:
        agent = LeadScoringAgent(session=session)
        result = await agent.score(lead_id=lead_id, tenant_id=tenant_id)
    logger.info("job_lead_scoring_done", lead_id=lead_id, score=result.get("fit_score"))
    return result


async def run_proposal_draft(
    ctx: dict[str, Any],
    deal_id: str,
    tenant_id: str,
    lang: str = "ar",
) -> dict[str, Any]:
    """
    Draft a localised proposal for a deal using the Proposal agent.
    صياغة عرض سعر محلّي للصفقة باستخدام وكيل المقترحات.
    """
    from core.agents.proposal import ProposalAgent
    from db.session import AsyncSessionLocal

    logger.info("job_proposal_draft_start", deal_id=deal_id, lang=lang)
    async with AsyncSessionLocal() as session:
        agent = ProposalAgent(session=session)
        result = await agent.draft(deal_id=deal_id, tenant_id=tenant_id, lang=lang)
    logger.info("job_proposal_draft_done", deal_id=deal_id)
    return result


async def run_outreach_batch(
    ctx: dict[str, Any],
    batch_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Execute a personalised outreach email batch.
    تنفيذ دفعة بريد إلكتروني للتواصل المخصّص.
    """
    from core.agents.outreach import OutreachAgent
    from db.session import AsyncSessionLocal

    logger.info("job_outreach_batch_start", batch_id=batch_id)
    async with AsyncSessionLocal() as session:
        agent = OutreachAgent(session=session)
        result = await agent.execute_batch(batch_id=batch_id, tenant_id=tenant_id)
    logger.info("job_outreach_batch_done", batch_id=batch_id, sent=result.get("sent"))
    return result


async def run_account_enrichment(
    ctx: dict[str, Any],
    account_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Enrich an account profile from public data sources.
    إثراء ملف الحساب من مصادر البيانات العامة.
    """
    from core.agents.enrichment import EnrichmentAgent
    from db.session import AsyncSessionLocal

    logger.info("job_enrichment_start", account_id=account_id)
    async with AsyncSessionLocal() as session:
        agent = EnrichmentAgent(session=session)
        result = await agent.enrich_account(account_id=account_id, tenant_id=tenant_id)
    logger.info("job_enrichment_done", account_id=account_id)
    return result


async def run_embedding_refresh(
    ctx: dict[str, Any],
    entity_type: str,
    entity_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Re-embed an entity into the Revenue Memory vector store.
    إعادة تضمين كيان في مخزن المتجهات — ذاكرة الإيرادات.
    """
    from core.memory.embedding_service import EmbeddingService
    from db.session import AsyncSessionLocal

    logger.info("job_embedding_refresh", entity_type=entity_type, entity_id=entity_id)
    async with AsyncSessionLocal() as session:
        svc = EmbeddingService(session=session)
        result = await svc.refresh(entity_type=entity_type, entity_id=entity_id, tenant_id=tenant_id)
    return result


async def run_zatca_clearance(
    ctx: dict[str, Any],
    invoice_id: str,
    tenant_id: str,
) -> dict[str, Any]:
    """
    Submit invoice to ZATCA for Phase 2 clearance/reporting.
    إرسال الفاتورة إلى هيئة الزكاة والضريبة والجمارك للمقاصة.
    """
    from integrations.zatca import ZATCAClient
    from db.session import AsyncSessionLocal

    logger.info("job_zatca_clearance_start", invoice_id=invoice_id)
    async with AsyncSessionLocal() as session:
        client = ZATCAClient(session=session, tenant_id=tenant_id)
        result = await client.submit_for_clearance(invoice_id=invoice_id)
    logger.info("job_zatca_clearance_done", invoice_id=invoice_id, status=result.get("status"))
    return result


# ── Cron Jobs ─────────────────────────────────────────────────────

async def daily_pipeline_refresh(ctx: dict[str, Any]) -> None:
    """
    Nightly pipeline health check — re-score stale leads, refresh embeddings.
    فحص صحة خط الأنابيب الليلي — إعادة تقييم العملاء المحتملين القديمين.
    """
    logger.info("cron_daily_pipeline_refresh_start")
    # Implementation: query leads older than 7d with status=new and re-enqueue scoring
    pass


# ── ARQ Worker Settings ───────────────────────────────────────────

class WorkerSettings:
    """
    ARQ WorkerSettings class — consumed by: arq core.tasks.worker.WorkerSettings
    إعدادات عامل ARQ.
    """

    functions = [
        run_lead_scoring,
        run_proposal_draft,
        run_outreach_batch,
        run_account_enrichment,
        run_embedding_refresh,
        run_zatca_clearance,
    ]

    cron_jobs = [
        cron(daily_pipeline_refresh, hour=2, minute=0),  # 02:00 AST daily
    ]

    @staticmethod
    def redis_settings() -> RedisSettings:
        settings = get_settings()
        return RedisSettings.from_url(settings.redis_url)

    max_jobs = 20
    job_timeout = timedelta(minutes=10)
    keep_result = timedelta(hours=24)
    retry_jobs = True
    max_tries = 3
