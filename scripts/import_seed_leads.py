#!/usr/bin/env python3
"""
import_seed_leads.py — ingest Tier1-tagged demo leads from YAML via AcquisitionPipeline.

Validates each row against Revenue OS source registry (forbidden / non-storable sources
are rejected) and optional anti-waste intake rules. Persists LeadRecord rows with
tier1_source + dedupe_hint (+ optional targeting_profile) in meta_json.

Usage:
    python scripts/import_seed_leads.py [--yaml data/seed/saudi_demo_leads.yaml]
    python scripts/import_seed_leads.py --dry-run
    python scripts/import_seed_leads.py --no-persist
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml

from auto_client_acquisition.notifications import notify_founder_on_intake
from auto_client_acquisition.pipeline import AcquisitionPipeline
from auto_client_acquisition.revenue_os.dedupe import suggest_dedupe_fingerprint
from auto_client_acquisition.revenue_os.saudi_targeting_profile import (
    anti_waste_violations_for_tier1_intake,
    assert_tier1_storage_allowed,
    map_tier1_to_intake_lead_source,
    parse_tier1_lead_source,
)
from auto_client_acquisition.revenue_os.source_registry import Tier1LeadSource, forbidden_sources
from db.models import LeadRecord
from db.session import async_session_factory


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if callable(reconf):
            try:
                reconf(encoding="utf-8")
            except Exception:
                pass


def _load_entries(path: Path) -> tuple[str | None, list[dict[str, Any]]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SystemExit("YAML root must be a mapping with version + entries")
    default_tier = raw.get("default_tier1_source")
    entries = raw.get("entries")
    if not isinstance(entries, list) or not entries:
        raise SystemExit("YAML must contain non-empty entries: list")
    return (str(default_tier).strip() if default_tier else None, entries)


async def _persist(
    *,
    tier1_value: str,
    result: Any,
    hint_dict: dict[str, Any],
    targeting_profile: dict[str, Any] | None,
) -> None:
    lead = result.lead
    meta = dict(lead.metadata)
    meta["tier1_source"] = tier1_value
    meta["dedupe_hint"] = hint_dict
    if targeting_profile is not None:
        meta["targeting_profile"] = targeting_profile
    async with async_session_factory() as session:
        session.add(
            LeadRecord(
                id=lead.id,
                source=lead.source.value,
                company_name=lead.company_name,
                contact_name=lead.contact_name,
                contact_email=lead.contact_email,
                contact_phone=lead.contact_phone,
                sector=lead.sector,
                region=lead.region,
                company_size=lead.company_size,
                budget=lead.budget,
                status=lead.status.value,
                fit_score=lead.fit_score,
                urgency_score=lead.urgency_score,
                locale=lead.locale,
                message=lead.message,
                pain_points=lead.pain_points,
                meta_json=meta,
                dedup_hash=lead.dedup_hash,
            )
        )
        await session.commit()


async def _run_one(
    pipeline: AcquisitionPipeline,
    *,
    tier1: Tier1LeadSource,
    payload: dict[str, Any],
    targeting_profile: dict[str, Any] | None,
    persist: bool,
) -> tuple[bool, str]:
    intake_src = map_tier1_to_intake_lead_source(tier1)
    full = {**payload, "tier1_source": tier1.value}
    result = await pipeline.run(
        payload=full,
        source=intake_src,
        auto_book=True,
        auto_proposal=False,
    )
    try:
        await notify_founder_on_intake(result.lead)
    except Exception as exc:
        print(f"  founder_alert_skipped: {exc}", file=sys.stderr)

    hint = suggest_dedupe_fingerprint(
        company_name=str(payload.get("company") or ""),
        domain=None,
        phone=str(payload.get("phone") or "") or None,
        email=str(payload.get("email") or "") or None,
    )
    hint_d = asdict(hint)
    result.lead.metadata = dict(result.lead.metadata)
    result.lead.metadata["tier1_source"] = tier1.value
    result.lead.metadata["dedupe_hint"] = hint_d
    if targeting_profile is not None:
        result.lead.metadata["targeting_profile"] = targeting_profile

    if persist:
        try:
            await _persist(
                tier1_value=tier1.value,
                result=result,
                hint_dict=hint_d,
                targeting_profile=targeting_profile,
            )
        except Exception as exc:
            return False, f"db_persist_failed:{exc}"
    return True, result.lead.id


async def amain(args: argparse.Namespace) -> int:
    yaml_path = Path(args.yaml).resolve()
    if not yaml_path.exists():
        print(f"file not found: {yaml_path}", file=sys.stderr)
        return 2

    default_tier, entries = _load_entries(yaml_path)
    forbidden = set(forbidden_sources())
    targeting_profile: dict[str, Any] | None = None
    if args.targeting_profile_json:
        targeting_profile = yaml.safe_load(args.targeting_profile_json)
        if not isinstance(targeting_profile, dict):
            print("--targeting-profile-json must decode to an object", file=sys.stderr)
            return 2

    if args.dry_run:
        print(f"[dry-run] would process {len(entries)} rows from {yaml_path.name}")
        for i, row in enumerate(entries):
            if not isinstance(row, dict):
                print(f"  [{i}] skip: not an object", file=sys.stderr)
                continue
            t1 = str(row.get("tier1_source") or default_tier or "").strip()
            if not t1:
                print(f"  [{i}] skip: missing tier1_source", file=sys.stderr)
                continue
            if t1 in forbidden:
                print(f"  [{i}] reject forbidden tier1={t1}")
                continue
            try:
                tier1 = parse_tier1_lead_source(t1)
                assert_tier1_storage_allowed(tier1)
            except ValueError as exc:
                print(f"  [{i}] reject {exc}")
                continue
            vio = anti_waste_violations_for_tier1_intake(tier1)
            if vio:
                print(f"  [{i}] reject anti_waste {vio!r}")
                continue
            print(f"  [{i}] ok tier1={t1} company={row.get('company')!r}")
        return 0

    pipeline = AcquisitionPipeline()
    ok_n = 0
    for i, row in enumerate(entries):
        if not isinstance(row, dict):
            print(f"[{i}] skip: entry not an object", file=sys.stderr)
            continue
        row = dict(row)
        t1 = str(row.pop("tier1_source", None) or default_tier or "").strip()
        if not t1:
            print(f"[{i}] skip: missing tier1_source", file=sys.stderr)
            continue
        if t1 in forbidden:
            print(f"[{i}] FAIL forbidden tier1_source={t1}", file=sys.stderr)
            continue
        try:
            tier1_enum = parse_tier1_lead_source(t1)
            assert_tier1_storage_allowed(tier1_enum)
        except ValueError as exc:
            print(f"[{i}] FAIL {exc}", file=sys.stderr)
            continue
        if anti_waste_violations_for_tier1_intake(tier1_enum):
            print(f"[{i}] FAIL anti_waste for {t1}", file=sys.stderr)
            continue

        ok, msg = await _run_one(
            pipeline,
            tier1=tier1_enum,
            payload=row,
            targeting_profile=targeting_profile,
            persist=not args.no_persist,
        )
        if ok:
            ok_n += 1
            print(f"[{i}] OK lead_id={msg} persist={not args.no_persist}")
        else:
            print(f"[{i}] FAIL {msg}", file=sys.stderr)

    print(f"done: {ok_n}/{len(entries)} succeeded")
    return 0 if ok_n else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Import Tier1 seed leads from YAML.")
    ap.add_argument(
        "--yaml",
        default=str(_repo_root() / "data" / "seed" / "saudi_demo_leads.yaml"),
        help="Path to saudi_demo_leads.yaml",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate YAML + policies only; do not run pipeline or DB.",
    )
    ap.add_argument(
        "--no-persist",
        action="store_true",
        help="Run pipeline but skip writing LeadRecord rows.",
    )
    ap.add_argument(
        "--targeting-profile-json",
        default=None,
        help='Optional JSON object merged into each lead meta_json as "targeting_profile".',
    )
    args = ap.parse_args()
    _ensure_utf8_stdio()
    return asyncio.run(amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
