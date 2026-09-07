#!/usr/bin/env python3
"""Real-Postgres acceptance for Market-to-Delivery intake.

This verifier is deliberately restricted to an explicitly named loopback test
Postgres database. It proves database-backed idempotency/concurrency and can be
run in two phases around an external database restart. It never accepts a
Production-looking URL and never prints credentials.
"""
from __future__ import annotations

import argparse
import asyncio
import os
from typing import Any

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.routers import market_to_delivery_intake as router_module
from auto_client_acquisition.service_catalog.intake_request_contract import MarketToDeliveryIntakeBody
from db.models_commercial_intelligence import CommercialSignalRecord, CommercialSourceRecord
from dealix.commercial_intelligence import SourceKind, SourcePolicyStatus

DB_PREFIX = "dealix_mtd_acceptance_"
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_MTD_POSTGRES_ACCEPTANCE=FAIL:{message}")


def validated_test_url(raw: str):
    if not raw:
        fail("DEALIX_MTD_POSTGRES_URL_REQUIRED")
    try:
        url = make_url(raw)
    except Exception:
        fail("INVALID_DATABASE_URL")
    if not url.drivername.startswith("postgresql"):
        fail("POSTGRESQL_REQUIRED")
    if (url.host or "") not in ALLOWED_HOSTS:
        fail("LOOPBACK_DATABASE_REQUIRED")
    database = str(url.database or "")
    if not database.startswith(DB_PREFIX):
        fail("EPHEMERAL_DATABASE_NAME_REQUIRED")
    if not url.password:
        fail("TEST_DATABASE_PASSWORD_REQUIRED")
    return url


def body(**overrides: Any) -> MarketToDeliveryIntakeBody:
    payload: dict[str, Any] = {
        "request_id": "mtd-postgres-acceptance-001",
        "account_id": "account-acceptance-1",
        "company_name": "Synthetic Acceptance Company",
        "source_id": "source-acceptance-1",
        "project_id": "construction-01",
        "problem": "Synthetic RFI handoff is slow.",
        "current_workflow": "Synthetic manual queue",
        "baseline": "Synthetic acceptance baseline",
        "desired_outcome": "Measure response lead time",
        "constraints": "Synthetic data only; no customer effects",
        "evidence_refs": [{"ref": "synthetic://mtd-postgres-acceptance", "sha256": "a" * 64}],
        "data_authorized": True,
    }
    payload.update(overrides)
    return MarketToDeliveryIntakeBody.model_validate(payload)


async def create_tables_and_source(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(CommercialSignalRecord.__table__.drop, checkfirst=True)
        await conn.run_sync(CommercialSourceRecord.__table__.drop, checkfirst=True)
        await conn.run_sync(CommercialSourceRecord.__table__.create, checkfirst=True)
        await conn.run_sync(CommercialSignalRecord.__table__.create, checkfirst=True)

    maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with maker() as session:
        session.add(
            CommercialSourceRecord(
                id="source-acceptance-1",
                tenant_id="tenant-acceptance-a",
                name="Synthetic MTD Postgres Acceptance Source",
                kind=SourceKind.CLIENT_PROVIDED.value,
                source_url=None,
                policy_status=SourcePolicyStatus.APPROVED.value,
                allowed_use="synthetic_acceptance_only",
                authority_score=100,
                verifiability_score=100,
                freshness_days=1,
                retention_days=1,
                active=True,
                metadata_json={"synthetic": True, "customer_effects": False},
            )
        )
        await session.commit()


async def count_signals(maker) -> int:
    async with maker() as session:
        return int((await session.scalar(select(func.count()).select_from(CommercialSignalRecord))) or 0)


async def call_intake(payload: MarketToDeliveryIntakeBody):
    return await router_module.persist_market_to_delivery_intake(
        payload,
        current_user={"tenant_id": "tenant-acceptance-a"},
    )


async def setup_race(raw_url: str) -> None:
    engine = create_async_engine(raw_url, pool_pre_ping=True, pool_size=4, max_overflow=2)
    try:
        await create_tables_and_source(engine)
        maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        router_module.async_session_factory = lambda: maker

        results = await asyncio.gather(call_intake(body()), call_intake(body()))
        statuses = sorted(str(item.get("status")) for item in results)
        if statuses != ["created", "existing"]:
            fail(f"RACE_STATUS_UNEXPECTED:{statuses}")
        if await count_signals(maker) != 1:
            fail("RACE_DID_NOT_DEDUPE_TO_ONE_SIGNAL")
        for item in results:
            if item.get("relationship_created") is not False:
                fail("RELATIONSHIP_AUTHORITY_DRIFT")
            if item.get("consent_created") is not False:
                fail("CONSENT_AUTHORITY_DRIFT")
            if item.get("opportunity_created") is not False:
                fail("OPPORTUNITY_AUTHORITY_DRIFT")
            if item.get("external_side_effect") is not False:
                fail("EXTERNAL_EFFECT_DRIFT")

        print("MTD_POSTGRES_CONCURRENT_IDEMPOTENCY=PASS")
        print("MTD_POSTGRES_SIGNAL_COUNT=1")
        print("customer_effects=false")
    finally:
        await engine.dispose()


async def replay_after_restart(raw_url: str) -> None:
    engine = create_async_engine(raw_url, pool_pre_ping=True, pool_size=2, max_overflow=1)
    try:
        maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        router_module.async_session_factory = lambda: maker

        result = await call_intake(body())
        if result.get("status") != "existing":
            fail("RESTART_REPLAY_NOT_EXISTING")
        if await count_signals(maker) != 1:
            fail("RESTART_SIGNAL_COUNT_CHANGED")

        try:
            await call_intake(body(problem="Changed synthetic requirement under same request id"))
        except HTTPException as exc:
            if exc.status_code != 409 or exc.detail != "market_to_delivery_request_id_payload_conflict":
                fail("RESTART_CHANGED_PAYLOAD_WRONG_CONFLICT")
        else:
            fail("RESTART_CHANGED_PAYLOAD_DID_NOT_CONFLICT")

        print("MTD_POSTGRES_RESTART_REPLAY=PASS")
        print("MTD_POSTGRES_CHANGED_PAYLOAD_CONFLICT=PASS")
        print("customer_effects=false")
    finally:
        await engine.dispose()


async def async_main(phase: str, raw_url: str) -> None:
    validated_test_url(raw_url)
    if phase == "setup-race":
        await setup_race(raw_url)
    elif phase == "replay-after-restart":
        await replay_after_restart(raw_url)
    else:
        fail("UNKNOWN_PHASE")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True, choices=["setup-race", "replay-after-restart"])
    args = parser.parse_args()
    raw_url = os.getenv("DEALIX_MTD_POSTGRES_URL", "")
    asyncio.run(async_main(args.phase, raw_url))
    print("DEALIX_MTD_POSTGRES_ACCEPTANCE=PASS")
    print(f"phase={args.phase}")
    print("production_db=false")
    print("external_send=false")
    print("payment=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
