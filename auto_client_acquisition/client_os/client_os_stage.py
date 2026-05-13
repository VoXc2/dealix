"""Client OS staging — post-Sprint / Retainer / Large-account."""

from __future__ import annotations

from enum import IntEnum


class ClientOsStage(IntEnum):
    POST_SPRINT = 1
    RETAINER = 2
    LARGE_ACCOUNT = 3


CLIENT_OS_STAGES: tuple[ClientOsStage, ...] = tuple(ClientOsStage)


def next_stage_after(stage: ClientOsStage) -> ClientOsStage | None:
    if stage is ClientOsStage.LARGE_ACCOUNT:
        return None
    return ClientOsStage(stage + 1)
