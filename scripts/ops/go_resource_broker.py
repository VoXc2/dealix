#!/usr/bin/env python3
"""DEALIX_GO_RESOURCE_BROKER - deterministic included-capacity planner.

The broker never treats provider namespace membership as proof that a request
cannot consume paid balance. Automatic OpenCode Go routing requires a current
provider cost-authority receipt proving that console balance fallback is off.
"""
from __future__ import annotations
import argparse
import getpass
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
OPS_DIR = Path(__file__).resolve().parent
if str(OPS_DIR) not in sys.path:
    sys.path.insert(0, str(OPS_DIR))
from model_cost_policy import (
    PAID_PENDING_APPROVAL,
    UNKNOWN_INCLUDED_HIGH,
    UNKNOWN_INCLUDED_LIGHT,
    UNKNOWN_INCLUDED_STRONG,
    explicit_free_models,
    first_available,
    included_opencode_go_models,
)

STATE_PATH = Path('/opt/dealix/company-os/founder-os/model_economics/GO_BROKER_STATE.json')
ROUTER_URL = 'http://127.0.0.1:11999/v1/models'
OLLAMA_URL = 'http://127.0.0.1:11434/api/tags'
_OPENCODE_BIN_CANDIDATES = (
    Path('/home/dealix/.opencode/bin/opencode'),
    Path('/usr/local/bin/opencode'),
    Path('/root/.opencode/bin/opencode'),
)
_CANONICAL_DEALIX_USER = 'dealix'
ROUTE_ORDER = (
    'R0_NO_MODEL', 'R1_DETERMINISTIC', 'R2_LOCAL_OLLAMA',
    'R3_INCLUDED_LIGHT', 'R4_INCLUDED_HIGH', 'R5_STRONG_REASONING',
    'R6_PAID_EXCEPTION',
)
TASK_ROUTES: dict[str, str] = {
    'HEALTH_CHECK': 'R0_NO_MODEL', 'SCHEDULER_AUDIT': 'R1_DETERMINISTIC',
    'FINGERPRINT': 'R1_DETERMINISTIC', 'CLASSIFICATION': 'R2_LOCAL_OLLAMA',
    'EXTRACTION': 'R2_LOCAL_OLLAMA', 'ARABIC': 'R3_INCLUDED_LIGHT',
    'CONTENT_DRAFT': 'R3_INCLUDED_LIGHT', 'DIAGNOSTIC_REASONING': 'R4_INCLUDED_HIGH',
    'CODE_ENGINEERING': 'R4_INCLUDED_HIGH', 'BUG_FIXING': 'R4_INCLUDED_HIGH',
    'TEST_GENERATION': 'R4_INCLUDED_HIGH', 'COMMERCIAL_REASONING': 'R4_INCLUDED_HIGH',
    'RESEARCH_SYNTHESIS': 'R4_INCLUDED_HIGH', 'ARCHITECTURE': 'R5_STRONG_REASONING',
    'SECURITY_REVIEW': 'R5_STRONG_REASONING',
}
BATCHABLE_TASK_CLASSES = frozenset({
    'RESEARCH_SYNTHESIS', 'CONTENT_DRAFT', 'TEST_GENERATION', 'EXTRACTION',
    'CLASSIFICATION', 'DIAGNOSTIC_REASONING',
})
COMPLEXITY_BUMP = {'low': 0, 'medium': 0, 'high': 1, 'critical': 2}
# Local advisory reserve — NOT provider quota. Provider limits are 13k-26k/5h per Go docs; headroom remains UNKNOWN.
# These counters exist only for local telemetry (daily_envelope) and never gate valid included work.
MAX_DAILY_INCLUDED_JOBS = 6  # advisory local reserve; provider is authoritative
MAX_DAILY_STRONG_JOBS = 2  # advisory
RESERVED_INCLUDED_JOBS = 2
OFF_PEAK_HOURS = (0, 8)
UNKNOWN = 'UNKNOWN'
GO_COST_VERIFIED_DISABLED = 'VERIFIED_DISABLED'
GO_COST_VERIFIED_ENABLED = 'VERIFIED_ENABLED'
GO_COST_UNKNOWN = 'UNKNOWN'


def provider_cost_authority(env: dict[str, str] | None = None) -> dict[str, Any]:
    source = env if env is not None else os.environ
    raw = str(source.get('DEALIX_OPENCODE_GO_USE_BALANCE', '')).strip().lower()
    evidence_ref = str(source.get('DEALIX_OPENCODE_GO_COST_AUTHORITY_REF', '')).strip()
    if evidence_ref and raw in {'disabled', 'false', '0', 'off'}:
        state = GO_COST_VERIFIED_DISABLED
    elif evidence_ref and raw in {'enabled', 'true', '1', 'on'}:
        state = GO_COST_VERIFIED_ENABLED
    else:
        state = GO_COST_UNKNOWN
    return {
        'state': state,
        'use_balance': raw.upper() if raw else UNKNOWN,
        'evidence_present': bool(evidence_ref),
        'automatic_go_allowed': state == GO_COST_VERIFIED_DISABLED,
    }


def _run(cmd: list[str], timeout: int = 30) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              check=False, cwd=str(REPO_ROOT) if REPO_ROOT.is_dir() else None).stdout
    except (OSError, subprocess.TimeoutExpired):
        return ''


def resolve_opencode_bin() -> str | None:
    if resolve_canonical_owner():
        for candidate in _OPENCODE_BIN_CANDIDATES:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
    found = shutil.which('opencode')
    if found:
        return found
    for candidate in _OPENCODE_BIN_CANDIDATES:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def resolve_canonical_owner() -> str | None:
    if os.geteuid() == 0:
        try:
            import pwd
            pwd.getpwnam(_CANONICAL_DEALIX_USER)
            return _CANONICAL_DEALIX_USER
        except (ImportError, KeyError):
            return None
    return None


def build_opencode_command(binary: str, args: list[str]) -> list[str]:
    owner = resolve_canonical_owner()
    if owner and owner != getpass.getuser() and shutil.which('sudo'):
        return ['sudo', '-n', '-u', owner, '-H', binary, *args]
    return [binary, *args]


def discover_opencode() -> dict[str, str]:
    binary = resolve_opencode_bin()
    version = _run(build_opencode_command(binary, ['--version']), timeout=20).strip() if binary else UNKNOWN
    name = Path(binary).name if binary else UNKNOWN
    return {'binary': binary or UNKNOWN, 'name': name, 'version': version or UNKNOWN}


def discover_catalog(refresh: bool = False) -> list[str]:
    binary = resolve_opencode_bin()
    if not binary:
        return []
    args = ['models', '--refresh'] if refresh else ['models']
    return [line.strip() for line in _run(build_opencode_command(binary, args), timeout=60).splitlines() if '/' in line]


def discover_router_models() -> list[str]:
    try:
        with urllib.request.urlopen(ROUTER_URL, timeout=5) as response:
            payload = json.loads(response.read().decode('utf-8'))
        return [entry.get('id', UNKNOWN) for entry in payload.get('data', [])]
    except Exception:
        return []


def discover_ollama_models() -> list[str]:
    try:
        with urllib.request.urlopen(OLLAMA_URL, timeout=5) as response:
            payload = json.loads(response.read().decode('utf-8'))
        return [entry.get('name', UNKNOWN) for entry in payload.get('models', [])]
    except Exception:
        return []


def pick_model(route: str, catalog: list[str], ollama: list[str], router: list[str],
               provider_state: str | None = None) -> str:
    free = explicit_free_models(catalog)
    state = provider_state or str(provider_cost_authority()['state'])
    included = included_opencode_go_models(catalog) if state == GO_COST_VERIFIED_DISABLED else []
    safe = [*included, *[model for model in free if model not in included]]
    if route in {'R0_NO_MODEL', 'R1_DETERMINISTIC'}:
        return 'none'
    if route == 'R2_LOCAL_OLLAMA':
        return ollama[0] if ollama else 'ollama:UNKNOWN'
    if route == 'R3_INCLUDED_LIGHT':
        return free[0] if free else (included[0] if included else UNKNOWN_INCLUDED_LIGHT)
    if route == 'R4_INCLUDED_HIGH':
        preferred = (
            'opencode-go/deepseek-v4.1-flash', 'opencode-go/deepseek-v4-flash',
            'opencode/deepseek-v4-flash-free', 'opencode/north-mini-code-free',
            'opencode/nemotron-3-ultra-free',
        )
        return first_available(preferred, safe) or UNKNOWN_INCLUDED_HIGH
    if route == 'R5_STRONG_REASONING':
        preferred = (
            'opencode-go/deepseek-v4-pro', 'opencode-go/glm-5.3',
            'opencode/nemotron-3-ultra-free',
        )
        return first_available(preferred, safe) or UNKNOWN_INCLUDED_STRONG
    return PAID_PENDING_APPROVAL


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pass
    return {'schema': 'go_broker_state_v1', 'jobs': [], 'created_at': datetime.now(UTC).isoformat()}


def save_state(state: dict[str, Any], path: Path = STATE_PATH) -> None:
    state['jobs'] = state.get('jobs', [])[-200:]
    state['updated_at'] = datetime.now(UTC).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')


def plan_route(task_class: str, complexity: str = 'medium', value: str = 'medium',
               urgency: str = 'normal', paid_approved: bool = False) -> dict[str, Any]:
    base = TASK_ROUTES.get(task_class, 'R3_INCLUDED_LIGHT')
    index = ROUTE_ORDER.index(base) + COMPLEXITY_BUMP.get(complexity, 0)
    if value == 'critical' and complexity in ('high', 'critical'):
        index = max(index, ROUTE_ORDER.index('R4_INCLUDED_HIGH'))
    emergency = urgency in ('critical', 'customer_obligation', 'production_incident')
    strong_capable = task_class in ('ARCHITECTURE', 'SECURITY_REVIEW') or (emergency and value == 'critical')
    cap = ROUTE_ORDER.index('R5_STRONG_REASONING') if strong_capable else ROUTE_ORDER.index('R4_INCLUDED_HIGH')
    index = min(index, cap)
    route = ROUTE_ORDER[index]
    paid_spill = False
    note = 'included_or_local_route'
    if emergency and value == 'critical' and paid_approved:
        route = 'R6_PAID_EXCEPTION'
        paid_spill = True
        note = 'founder_approved_paid_exception'
    elif emergency and value == 'critical':
        note = 'paid_exception_declined_no_approval__staying_on_strongest_included'
    off_peak = task_class in BATCHABLE_TASK_CLASSES and not emergency and value in ('low', 'medium')
    return {
        'task_class': task_class, 'route': route, 'route_index': ROUTE_ORDER.index(route),
        'paid_spill': paid_spill,
        'paid_spill_firewall': 'R6 requires explicit --paid-approved and critical emergency value',
        'reason': note, 'off_peak_preferred': off_peak,
        'off_peak_window_local': f'{OFF_PEAK_HOURS[0]:02d}:00-{OFF_PEAK_HOURS[1]:02d}:00',
        'off_peak_basis': 'UNKNOWN_OFFICIAL_PEAK_DATA__conservative_recommendation_only',
        'reserve_kept': RESERVED_INCLUDED_JOBS, 'headroom': UNKNOWN,
    }


def daily_envelope(state: dict[str, Any], now: datetime | None = None) -> dict[str, Any]:
    now = now or datetime.now(UTC)
    today = now.date().isoformat()
    jobs = [job for job in state.get('jobs', []) if str(job.get('recorded_at', '')).startswith(today)]
    included_today = len([job for job in jobs if str(job.get('route', '')).startswith(('R3', 'R4'))])
    strong_today = len([job for job in jobs if str(job.get('route')) == 'R5_STRONG_REASONING'])
    return {
        'date': today, 'included_jobs_today': included_today,
        'included_jobs_remaining': max(0, MAX_DAILY_INCLUDED_JOBS - included_today),
        'strong_jobs_today': strong_today,
        'strong_jobs_remaining': max(0, MAX_DAILY_STRONG_JOBS - strong_today),
        'reserved_for_emergency': RESERVED_INCLUDED_JOBS,
        'headroom_source': 'local_telemetry_only__provider_limits_are_authoritative',
    }


def record_job(state: dict[str, Any], task_class: str, route: str, model: str,
               outcome: str = 'planned') -> dict[str, Any]:
    job = {
        'recorded_at': datetime.now(UTC).isoformat(), 'task_class': task_class,
        'route': route, 'model': model, 'outcome': outcome,
        'cost_observable': False, 'tokens_observable': False,
    }
    state.setdefault('jobs', []).append(job)
    return job


def status_payload(refresh_models: bool = False) -> dict[str, Any]:
    opencode = discover_opencode()
    catalog = discover_catalog(refresh=refresh_models) if opencode['binary'] != UNKNOWN else []
    state = load_state()
    cost_authority = provider_cost_authority()
    return {
        'generated_at': datetime.now(UTC).isoformat(), 'opencode': opencode,
        'catalog_size': len(catalog), 'catalog_free_models': explicit_free_models(catalog)[:5],
        'catalog_included_go_models': included_opencode_go_models(catalog)[:5],
        'catalog_unproven_models': [model for model in catalog
            if model not in explicit_free_models(catalog) and model not in included_opencode_go_models(catalog)][:5],
        'router_models': discover_router_models(), 'ollama_models': discover_ollama_models(),
        'envelope': daily_envelope(state), 'provider_cost_authority': cost_authority,
        'auto_select_policy': 'explicit_free_or_verified_use_balance_disabled_go',
        'paid_spill': 'DISABLED_BY_DEFAULT',
    }


def render_status(status: dict[str, Any]) -> str:
    authority = status['provider_cost_authority']
    lines = [
        'GO_BROKER=ACTIVE', f"OPENCODE={status['opencode']['name']}@{status['opencode']['version']}",
        f"CATALOG_SIZE={status['catalog_size']}", f"FREE_MODELS={status['catalog_free_models']}",
        f"INCLUDED_GO_MODELS={status['catalog_included_go_models']}",
        f"UNPROVEN_MODELS={status['catalog_unproven_models']}",
        f"ROUTER_MODELS={status['router_models']}", f"OLLAMA_MODELS={status['ollama_models']}",
        f"INCLUDED_JOBS_TODAY={status['envelope']['included_jobs_today']}",
        f"INCLUDED_JOBS_REMAINING={status['envelope']['included_jobs_remaining']}",
        f"STRONG_JOBS_REMAINING={status['envelope']['strong_jobs_remaining']}",
        f"HEADROOM={status['envelope']['headroom_source']}",
        f"GO_COST_AUTHORITY={authority['state']}",
        f"GO_USE_BALANCE={authority['use_balance']}",
        f"GO_COST_EVIDENCE_PRESENT={authority['evidence_present']}",
        f"AUTO_SELECT_POLICY={status['auto_select_policy']}", f"PAID_SPILL={status['paid_spill']}",
    ]
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Dealix Go Resource Broker (deterministic planner)')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--plan', metavar='TASK_CLASS')
    parser.add_argument('--complexity', default='medium')
    parser.add_argument('--value', default='medium')
    parser.add_argument('--urgency', default='normal')
    parser.add_argument('--paid-approved', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--refresh-models', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.plan:
        plan = plan_route(args.plan, args.complexity, args.value, args.urgency, args.paid_approved)
        catalog = discover_catalog(refresh=args.refresh_models)
        authority = provider_cost_authority()
        plan['provider_cost_authority'] = authority
        plan['model_hint'] = pick_model(plan['route'], catalog, discover_ollama_models(), discover_router_models(), str(authority['state']))
        if args.record:
            state = load_state()
            record_job(state, args.plan, plan['route'], plan['model_hint'])
            save_state(state)
            plan['recorded'] = True
        print(json.dumps(plan, indent=2, ensure_ascii=False) if args.json else '\n'.join(f'{k}={v}' for k, v in plan.items()))
        return 0
    status = status_payload(refresh_models=args.refresh_models)
    print(json.dumps(status, indent=2, ensure_ascii=False) if args.json else render_status(status))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
