"""DailyReview — مراجعة يومية لكل الـ Waves + تقرير للـ Founder"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

import structlog
from pydantic import BaseModel, Field

from dealix.hermes.loops.task_queue import HermesTaskQueue
from dealix.hermes.orchestrators.wave_orchestrator import (
    WaveOrchestrator,
    WaveStatus,
    WAVE_CONFIGS,
)

logger = structlog.get_logger(__name__)


class DailyReport(BaseModel):
    date: date
    waves_status: dict[str, WaveStatus]
    pending_approvals: list[str]
    tasks_completed_today: int = 0
    tasks_failed_today: int = 0
    tasks_in_progress: int = 0
    overall_progress_pct: float = 0.0
    recommendations: list[str] = []
    generated_at: datetime = Field(default_factory=datetime.now)
    sla_breached: list[str] = []


class DailyReview:
    """مراجعة يومية لكل الـ Waves + تقرير للـ Founder"""

    def __init__(
        self,
        orchestrator: WaveOrchestrator,
        task_queue: Optional[HermesTaskQueue] = None,
    ) -> None:
        self.orchestrator = orchestrator
        self.task_queue = task_queue or HermesTaskQueue()

    async def generate_daily_report(self) -> DailyReport:
        """Generate a comprehensive daily report of all wave activity."""
        waves_status = await self.orchestrator.get_all_statuses()
        pending = await self.orchestrator.get_pending_approvals()

        today = date.today()
        tasks_today = [
            t
            for t in self.task_queue.results.values()
            if t.completed_at and t.completed_at.date() == today
        ]

        completed_today = [t for t in tasks_today if t.status == WaveStatus.COMPLETED]
        failed_today = [t for t in tasks_today if t.status == WaveStatus.FAILED]
        in_progress = [
            t
            for t in self.task_queue.results.values()
            if t.status == WaveStatus.IN_PROGRESS
        ]

        completed_waves = sum(
            1 for s in waves_status.values() if s == WaveStatus.COMPLETED
        )
        overall_pct = (
            (completed_waves / len(WAVE_CONFIGS)) * 100 if WAVE_CONFIGS else 0
        )

        sla_breached = await self._check_sla_breaches()

        report = DailyReport(
            date=today,
            waves_status=waves_status,
            pending_approvals=[p.wave_id for p in pending],
            tasks_completed_today=len(completed_today),
            tasks_failed_today=len(failed_today),
            tasks_in_progress=len(in_progress),
            overall_progress_pct=overall_pct,
            recommendations=await self._generate_recommendations(waves_status),
            sla_breached=sla_breached,
        )

        logger.info("daily_report_generated", date=today.isoformat())
        return report

    async def _generate_recommendations(
        self, waves_status: dict[str, WaveStatus]
    ) -> list[str]:
        """Generate Arabic recommendations based on current wave status."""
        recs: list[str] = []

        blocked = [w for w, s in waves_status.items() if s == WaveStatus.BLOCKED]
        if blocked:
            names = [WAVE_CONFIGS[w].name_ar for w in blocked if w in WAVE_CONFIGS]
            recs.append(f"الموجات المتوقفة تحتاج مراجعة: {', '.join(names)}")

        failed = [w for w, s in waves_status.items() if s == WaveStatus.FAILED]
        if failed:
            names = [WAVE_CONFIGS[w].name_ar for w in failed if w in WAVE_CONFIGS]
            recs.append(f"الموجات الفاشلة تحتاج تدخل: {', '.join(names)}")

        pending = await self.orchestrator.get_pending_approvals()
        if pending:
            names = [p.name_ar for p in pending]
            recs.append(f"تحتاج موافقة المؤسس: {', '.join(names)}")

        pct = (
            sum(1 for s in waves_status.values() if s == WaveStatus.COMPLETED)
            / len(WAVE_CONFIGS)
        ) * 100
        if pct < 25:
            recs.append("نسبة الإنجاز أقل من 25% — ركز على الموجات الحرجة أولاً")
        elif pct > 75:
            recs.append("نسبة الإنجاز ممتازة — استعد للانتقال للمرحلة التالية")

        return recs

    async def _check_sla_breaches(self) -> list[str]:
        """Check for any SLA breaches across active waves."""
        breached: list[str] = []
        now = datetime.now()

        for wave_id, config in WAVE_CONFIGS.items():
            status = self.orchestrator.active_waves.get(wave_id)
            if status in (WaveStatus.IN_PROGRESS, WaveStatus.PENDING):
                tasks = [
                    t
                    for t in self.task_queue.results.values()
                    if t.wave_id == wave_id and t.created_at
                ]
                for task in tasks:
                    elapsed = (now - task.created_at).total_seconds() / 3600
                    if task.status == WaveStatus.PENDING and elapsed > config.sla_hours:
                        breached.append(
                            f"{config.name_ar}/{task.agent_id}"
                        )

        return breached

    def summary_text(self, report: DailyReport) -> str:
        """Return a human-readable Arabic summary of the daily report."""
        lines = [
            f"ديليكس — تقرير يومي ({report.date.isoformat()})",
            f"● الموجات: {report.overall_progress_pct:.0f}% مكتمل",
            f"● المهام اليوم: {report.tasks_completed_today} تمت — {report.tasks_failed_today} فشلت",
            f"● قيد الانتظار: {report.tasks_in_progress}",
            f"● الموافقات المعلقة: {len(report.pending_approvals)}",
        ]
        if report.sla_breached:
            lines.append(f"● ⚠ انتهاك SLA: {', '.join(report.sla_breached)}")
        if report.recommendations:
            lines.append("● التوصيات:")
            for r in report.recommendations:
                lines.append(f"  - {r}")
        return "\n".join(lines)


__all__ = ["DailyReport", "DailyReview"]
