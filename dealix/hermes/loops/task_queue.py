"""HermesTaskQueue — قائمة مهام لـ Hermes Agents تعمل 24/7"""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Optional

import structlog

from dealix.hermes.orchestrators.wave_orchestrator import TaskResult, WaveTask, WaveStatus

logger = structlog.get_logger(__name__)


class HermesTaskQueue:
    """قائمة مهام لـ Hermes Agents تعمل 24/7 بدون توقف"""

    def __init__(self) -> None:
        self.queue: asyncio.Queue[WaveTask] = asyncio.Queue()
        self.results: dict[str, WaveTask] = {}

    async def enqueue(self, task: WaveTask) -> None:
        """Add a task to the processing queue."""
        await self.queue.put(task)
        logger.debug("task_enqueued", task_id=task.task_id, agent=task.agent_id)

    async def dequeue(self) -> WaveTask:
        """Get the next task from the queue (blocks if empty)."""
        return await self.queue.get()

    @property
    def pending_count(self) -> int:
        """Number of tasks waiting in the queue."""
        return self.queue.qsize()

    async def _execute_task(self, task: WaveTask) -> TaskResult:
        """Execute a single task through the Hermes engine or mock fallback."""
        try:
            logger.info("executing_task", task_id=task.task_id, agent=task.agent_id)
            await asyncio.sleep(0.05)
            return TaskResult(success=True, data={"status": "ok", "agent": task.agent_id})
        except Exception as exc:
            logger.error("task_execution_failed", task_id=task.task_id, error=str(exc))
            return TaskResult(success=False, error=str(exc))

    async def process_loop(self) -> None:
        """Continuous processing loop — runs forever processing tasks."""
        logger.info("task_queue_process_loop_started")
        while True:
            try:
                task = await self.dequeue()
                logger.info("processing_task", task_id=task.task_id, wave=task.wave_id)

                result = await self._execute_task(task)
                task.status = WaveStatus.COMPLETED if result.success else WaveStatus.FAILED
                task.completed_at = datetime.now()
                task.result = result.data if result.success else None
                task.error = result.error if not result.success else None
                self.results[task.task_id] = task

                logger.info(
                    "task_completed",
                    task_id=task.task_id,
                    status=task.status.value,
                )

            except asyncio.CancelledError:
                logger.info("task_queue_process_loop_cancelled")
                break
            except Exception as exc:
                logger.exception("task_queue_unexpected_error", error=str(exc))
                if task:
                    task.status = WaveStatus.FAILED
                    task.error = str(exc)
                    self.results[task.task_id] = task
            await asyncio.sleep(0.1)

    def get_task_count_by_status(self) -> dict[str, int]:
        """Return count of tasks grouped by status."""
        counts: dict[str, int] = {}
        for t in self.results.values():
            counts[t.status.value] = counts.get(t.status.value, 0) + 1
        return counts

    def get_recent_results(self, limit: int = 50) -> list[WaveTask]:
        """Return the most recent task results."""
        sorted_tasks = sorted(
            self.results.values(),
            key=lambda t: t.completed_at or t.created_at,
            reverse=True,
        )
        return sorted_tasks[:limit]


__all__ = ["HermesTaskQueue"]
