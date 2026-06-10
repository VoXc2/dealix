from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PromptVersion:
    prompt_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt_key: str = ""
    version: int = 1
    template: str = ""
    variables: list[str] = field(default_factory=list)
    model: str = ""
    provider: str = ""
    hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str = "system"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class PromptPerformance:
    prompt_id: str
    prompt_key: str
    version: int
    total_calls: int = 0
    total_tokens: int = 0
    avg_tokens_per_call: float = 0.0
    avg_latency_ms: float = 0.0
    success_rate: float = 1.0
    avg_score: float | None = None
    feedback_count: int = 0
    positive_feedback: int = 0
    negative_feedback: int = 0
    last_used: datetime = field(default_factory=datetime.utcnow)
    metrics: dict[str, float] = field(default_factory=dict)


@dataclass
class PromptComparison:
    prompt_key: str
    versions: list[int]
    best_version: int | None = None
    improvements: list[str] = field(default_factory=list)
    regressions: list[str] = field(default_factory=list)


class PromptRegistry:
    def __init__(self):
        self._prompts: dict[str, list[PromptVersion]] = {}
        self._performance: dict[str, dict[int, PromptPerformance]] = {}
        self._latest_key: dict[str, str] = {}

    async def register(self, prompt: PromptVersion) -> None:
        content_hash = self._hash_content(prompt.template)
        prompt.hash = content_hash

        if prompt.prompt_key not in self._prompts:
            self._prompts[prompt.prompt_key] = []
            prompt.version = 1
        else:
            existing = self._prompts[prompt.prompt_key]
            prompt.version = max(v.version for v in existing) + 1

        self._prompts[prompt.prompt_key].append(prompt)
        self._latest_key[prompt.prompt_key] = prompt.prompt_id

        if prompt.prompt_key not in self._performance:
            self._performance[prompt.prompt_key] = {}
        self._performance[prompt.prompt_key][prompt.version] = PromptPerformance(
            prompt_id=prompt.prompt_id,
            prompt_key=prompt.prompt_key,
            version=prompt.version,
        )

        logger.info(
            "Registered prompt '%s' v%d (id: %s)",
            prompt.prompt_key, prompt.version, prompt.prompt_id,
        )

    async def get_latest(self, prompt_key: str) -> PromptVersion | None:
        versions = self._prompts.get(prompt_key, [])
        if not versions:
            return None
        return max(versions, key=lambda v: v.version)

    async def get_version(
        self,
        prompt_key: str,
        version: int,
    ) -> PromptVersion | None:
        versions = self._prompts.get(prompt_key, [])
        for v in versions:
            if v.version == version:
                return v
        return None

    async def get_performance(
        self,
        prompt_id: str,
        version: int | None = None,
    ) -> PromptPerformance | None:
        for key, versions in self._performance.items():
            if version is not None:
                perf = versions.get(version)
                if perf and perf.prompt_id == prompt_id:
                    return perf
            else:
                for v, perf in versions.items():
                    if perf.prompt_id == prompt_id:
                        return perf
        return None

    async def record_call(
        self,
        prompt_id: str,
        tokens_used: int,
        latency_ms: float,
        success: bool,
        score: float | None = None,
        feedback: str | None = None,
    ) -> None:
        for key, versions in self._performance.items():
            for v, perf in versions.items():
                if perf.prompt_id == prompt_id:
                    prev = perf.total_calls
                    perf.total_calls += 1
                    perf.total_tokens += tokens_used
                    perf.avg_tokens_per_call = (
                        (perf.avg_tokens_per_call * prev + tokens_used) / perf.total_calls
                        if perf.total_calls > 0
                        else float(tokens_used)
                    )
                    perf.avg_latency_ms = (
                        (perf.avg_latency_ms * prev + latency_ms) / perf.total_calls
                        if perf.total_calls > 0
                        else float(latency_ms)
                    )
                    perf.success_rate = (
                        (perf.success_rate * prev + (1.0 if success else 0.0)) / perf.total_calls
                        if perf.total_calls > 0
                        else (1.0 if success else 0.0)
                    )
                    if score is not None:
                        perf.avg_score = (
                            ((perf.avg_score or 0) * prev + score) / perf.total_calls
                            if perf.total_calls > 0
                            else score
                        )
                    if feedback == "positive":
                        perf.positive_feedback += 1
                        perf.feedback_count += 1
                    elif feedback == "negative":
                        perf.negative_feedback += 1
                        perf.feedback_count += 1
                    perf.last_used = datetime.utcnow()
                    return

    async def list_prompt_keys(self) -> list[str]:
        return list(self._prompts.keys())

    async def get_version_history(self, prompt_key: str) -> list[PromptVersion]:
        return sorted(
            self._prompts.get(prompt_key, []),
            key=lambda v: v.version,
        )

    async def compare_versions(
        self,
        prompt_key: str,
        versions: list[int] | None = None,
    ) -> PromptComparison:
        all_versions = await self.get_version_history(prompt_key)
        if not all_versions:
            return PromptComparison(prompt_key=prompt_key, versions=[])
        if versions is None:
            versions = [v.version for v in all_versions]
        comparison = PromptComparison(prompt_key=prompt_key, versions=versions)
        best_score = -1.0
        for vnum in versions:
            perf = self._performance.get(prompt_key, {}).get(vnum)
            if perf and (perf.avg_score or 0) > best_score:
                best_score = perf.avg_score or 0
                comparison.best_version = vnum
        if len(versions) >= 2:
            v1 = self._performance.get(prompt_key, {}).get(versions[0])
            v2 = self._performance.get(prompt_key, {}).get(versions[-1])
            if v1 and v2:
                if (v2.avg_score or 0) > (v1.avg_score or 0):
                    comparison.improvements.append(
                        f"Score improved from {v1.avg_score:.3f} to {v2.avg_score:.3f}"
                    )
                if v2.success_rate > v1.success_rate:
                    comparison.improvements.append(
                        f"Success rate improved from {v1.success_rate:.1%} to {v2.success_rate:.1%}"
                    )
                if v2.avg_latency_ms < v1.avg_latency_ms:
                    comparison.improvements.append(
                        f"Latency reduced from {v1.avg_latency_ms:.0f}ms to {v2.avg_latency_ms:.0f}ms"
                    )
        return comparison

    def _hash_content(self, content: str) -> str:
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()[:16]
