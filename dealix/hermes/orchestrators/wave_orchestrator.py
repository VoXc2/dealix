"""Hermes Wave Orchestrator — يدير تنفيذ جميع Waves الـ 9 كـ Agents"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import structlog
from pydantic import BaseModel, Field

logger = structlog.get_logger(__name__)


class WaveStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class WaveConfig(BaseModel):
    wave_id: str
    name_ar: str
    name_en: str
    agents: list[str]
    model: str
    max_turns: int
    approval_required: bool
    sla_hours: int
    dependencies: list[str] = []


class WaveTask(BaseModel):
    task_id: str
    wave_id: str
    agent_id: str
    description: str
    status: WaveStatus = WaveStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class TaskResult(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


WAVE_CONFIGS: dict[str, WaveConfig] = {
    "wave_1_brand": WaveConfig(
        wave_id="wave_1_brand",
        name_ar="الهوية البصرية والعلامة التجارية",
        name_en="Brand & Visual Identity",
        agents=["design_agent", "content_agent"],
        model="claude-sonnet-4-5",
        max_turns=50,
        approval_required=True,
        sla_hours=48,
    ),
    "wave_2_quality": WaveConfig(
        wave_id="wave_2_quality",
        name_ar="تناسق المشروع وجودة الكود",
        name_en="Code Quality & Consistency",
        agents=["lint_agent", "test_agent", "refactor_agent"],
        model="claude-sonnet-4-5",
        max_turns=100,
        approval_required=False,
        sla_hours=24,
    ),
    "wave_3_distribution": WaveConfig(
        wave_id="wave_3_distribution",
        name_ar="مكاين التصريف الأربعة الكبرى",
        name_en="4 Massive Distribution Engines",
        agents=["marketing_agent", "partner_agent", "sales_agent", "revenue_agent"],
        model="claude-opus-4-8",
        max_turns=200,
        approval_required=False,
        sla_hours=24,
    ),
    "wave_4_intelligence": WaveConfig(
        wave_id="wave_4_intelligence",
        name_ar="الذكاء الصناعي الأصيل",
        name_en="True AI Superintelligence",
        agents=["rag_agent", "router_agent", "learning_agent", "evolution_agent"],
        model="claude-opus-4-8",
        max_turns=200,
        approval_required=False,
        sla_hours=48,
    ),
    "wave_5_enterprise": WaveConfig(
        wave_id="wave_5_enterprise",
        name_ar="جاهزية المؤسسات الكبرى",
        name_en="Enterprise Readiness",
        agents=["compliance_agent", "security_agent", "identity_agent"],
        model="claude-opus-4-8",
        max_turns=150,
        approval_required=True,
        sla_hours=72,
    ),
    "wave_6_ux": WaveConfig(
        wave_id="wave_6_ux",
        name_ar="واجهة المستخدم العالمية",
        name_en="World-Class UX",
        agents=["design_agent", "performance_agent", "i18n_agent", "mobile_agent"],
        model="claude-sonnet-4-5",
        max_turns=150,
        approval_required=True,
        sla_hours=48,
    ),
    "wave_7_saudi": WaveConfig(
        wave_id="wave_7_saudi",
        name_ar="السعودية العميقة",
        name_en="Deep Saudi Layer",
        agents=["saudi_layer_agent", "gov_integration_agent"],
        model="claude-opus-4-8",
        max_turns=150,
        approval_required=False,
        sla_hours=48,
    ),
    "wave_8_gulf": WaveConfig(
        wave_id="wave_8_gulf",
        name_ar="التوسع الخليجي",
        name_en="Gulf Expansion",
        agents=["uae_agent", "qatar_agent", "kuwait_agent", "bahrain_agent", "oman_agent"],
        model="claude-sonnet-4-5",
        max_turns=100,
        approval_required=False,
        sla_hours=72,
    ),
    "wave_9_ops": WaveConfig(
        wave_id="wave_9_ops",
        name_ar="التميز التنفيذي والتشغيلي",
        name_en="Executive Ops Excellence",
        agents=["cockpit_agent", "sla_agent", "incident_agent", "ceo_agent"],
        model="claude-opus-4-8",
        max_turns=100,
        approval_required=False,
        sla_hours=24,
    ),
}


class WaveOrchestrator:
    """يدير تنفيذ جميع Waves بالتوازي مع مراعاة التبعيات"""

    def __init__(self, hermes_engine: Any = None) -> None:
        self.engine = hermes_engine
        self.active_waves: dict[str, WaveStatus] = {}
        self.task_queue: list[WaveTask] = []
        self._task_results: dict[str, WaveTask] = {}

    async def start_all_waves(self) -> dict[str, WaveStatus]:
        """إطلاق جميع Waves بالتوازي"""
        results: dict[str, WaveStatus] = {}
        for wave_id in WAVE_CONFIGS:
            results[wave_id] = await self.start_wave(wave_id)
        logger.info("all_waves_started", total=len(results))
        return results

    async def start_wave(self, wave_id: str) -> WaveStatus:
        """إطلاق Wave معينة"""
        config = WAVE_CONFIGS.get(wave_id)
        if not config:
            logger.warning("wave_config_not_found", wave_id=wave_id)
            return WaveStatus.FAILED

        for dep in config.dependencies:
            if self.active_waves.get(dep) != WaveStatus.COMPLETED:
                logger.info("wave_blocked_by_dependency", wave=wave_id, dependency=dep)
                self.active_waves[wave_id] = WaveStatus.BLOCKED
                return WaveStatus.BLOCKED

        self.active_waves[wave_id] = WaveStatus.IN_PROGRESS
        logger.info("wave_started", wave=wave_id, agents=len(config.agents))

        for agent_name in config.agents:
            task = WaveTask(
                task_id=f"{wave_id}_{agent_name}_{uuid.uuid4().hex[:8]}",
                wave_id=wave_id,
                agent_id=agent_name,
                description=f"Execute {agent_name} for {wave_id}",
            )
            self.task_queue.append(task)
            logger.debug("task_enqueued", task_id=task.task_id, agent=agent_name)

        return WaveStatus.IN_PROGRESS

    async def get_wave_status(self, wave_id: str) -> Optional[WaveStatus]:
        """Get current status of a specific wave."""
        return self.active_waves.get(wave_id)

    async def get_all_statuses(self) -> dict[str, WaveStatus]:
        """Get status of all waves."""
        return self.active_waves.copy()

    async def get_pending_approvals(self) -> list[WaveConfig]:
        """Waves that need founder approval."""
        return [
            c for c in WAVE_CONFIGS.values()
            if c.approval_required and self.active_waves.get(c.wave_id) == WaveStatus.IN_PROGRESS
        ]

    async def approve_wave(self, wave_id: str) -> None:
        """Founder approval for a wave — marks it completed."""
        if wave_id in self.active_waves:
            self.active_waves[wave_id] = WaveStatus.COMPLETED
            logger.info("wave_approved", wave_id=wave_id)

    async def fail_wave(self, wave_id: str, error: str) -> None:
        """Mark a wave as failed with an error reason."""
        if wave_id in self.active_waves:
            self.active_waves[wave_id] = WaveStatus.FAILED
            logger.error("wave_failed", wave_id=wave_id, error=error)

    async def complete_task(self, task_id: str, result: dict) -> None:
        """Mark a task as completed with its result."""
        task = self._task_results.get(task_id)
        if task:
            task.status = WaveStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result

    async def fail_task(self, task_id: str, error: str) -> None:
        """Mark a task as failed."""
        task = self._task_results.get(task_id)
        if task:
            task.status = WaveStatus.FAILED
            task.completed_at = datetime.now()
            task.error = error

    async def get_progress_summary(self) -> dict[str, Any]:
        """Get a summary of overall progress across all waves."""
        total_tasks = sum(len(c.agents) for c in WAVE_CONFIGS.values())
        completed_waves = sum(
            1 for s in self.active_waves.values() if s == WaveStatus.COMPLETED
        )
        in_progress = sum(
            1 for s in self.active_waves.values() if s == WaveStatus.IN_PROGRESS
        )
        failed = sum(
            1 for s in self.active_waves.values() if s == WaveStatus.FAILED
        )
        blocked = sum(
            1 for s in self.active_waves.values() if s == WaveStatus.BLOCKED
        )

        return {
            "total_waves": len(WAVE_CONFIGS),
            "total_tasks": total_tasks,
            "completed_waves": completed_waves,
            "in_progress": in_progress,
            "failed": failed,
            "blocked": blocked,
            "overall_pct": (completed_waves / len(WAVE_CONFIGS)) * 100 if WAVE_CONFIGS else 0,
            "wave_statuses": self.active_waves.copy(),
        }


__all__ = [
    "WaveConfig",
    "WaveOrchestrator",
    "WaveStatus",
    "WaveTask",
    "TaskResult",
    "WAVE_CONFIGS",
]
