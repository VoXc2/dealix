"""Preparation adapter for the existing catalog, Approval Center and Delivery OS.

No model execution, CRM write, approval, send, charge, deploy or provisioning.
A valid artifact is NOT proof that the supplied evidence is genuine/current.
"""
from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).with_name('market_to_delivery_catalog.json')
ENGINE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CANONICAL_AGENTS = ('dealix-pm', 'dealix-sales', 'dealix-delivery', 'dealix-engineer', 'dealix-content')
FORBIDDEN_EFFECTS = ('external_send', 'public_publish', 'commercial_commitment', 'payment',
                     'production_deploy', 'database_migration', 'provision_workers', 'policy_activation')
CAPABILITY_ARMS = {
    'automation': 'automation_integration', 'integration': 'automation_integration',
    'data': 'data_documents', 'documents': 'data_documents', 'software': 'custom_software',
    'ai': 'enterprise_ai', 'cloud': 'cloud_reliability', 'governance': 'governance_security',
    'industrial': 'industrial_field', 'operations': 'managed_operations',
}
FIELDS = {'tenant_id', 'request_id', 'project_id', 'problem', 'current_workflow', 'baseline',
          'desired_outcome', 'constraints', 'evidence_refs', 'data_authorized',
          'estimated_cost_sar', 'target_margin_pct', 'customer_context'}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_catalog() -> dict[str, Any]:
    catalog = json.loads(CATALOG_PATH.read_text(encoding='utf-8'))
    sectors = catalog['sectors']
    rows = [row for sector in sectors for row in sector['projects']]
    if len(sectors) != catalog['sector_count'] or len(rows) != catalog['project_hypothesis_count']:
        raise ValueError('catalog_count_mismatch')
    if len({s['id'] for s in sectors}) != len(sectors) or len({r[0] for r in rows}) != len(rows):
        raise ValueError('catalog_duplicate_id')
    if any(len(row) != 4 or row[1] not in CAPABILITY_ARMS for row in rows):
        raise ValueError('catalog_row_invalid')
    if catalog['defaults']['commercial_commitment_authorized'] is not False:
        raise ValueError('catalog_cannot_grant_authority')
    return catalog


def public_projection(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    """Explicit DTO: no accounts, contacts, prices, evidence or customer data."""
    c = catalog or load_catalog()
    return {
        'schema_version': c['schema_version'], 'catalog_digest': digest(c),
        'as_of': c['as_of'], 'status': 'HYPOTHESES_NOT_PROVEN_DELIVERY',
        'arms': [{'id': a['id'], 'name_ar': a['name_ar'], 'name_en': a['name']} for a in c['commercial_arms']],
        'sectors': [{
            'id': s['id'], 'name_ar': s['name_ar'], 'name_en': s['name_en'],
            'domain_review': s['domain_review'],
            'projects': [{'id': r[0], 'arm': CAPABILITY_ARMS[r[1]], 'name': r[2],
                          'acceptance_measure': r[3]} for r in s['projects']],
        } for s in c['sectors']],
    }


def _text(value: Any, field: str, limit: int = 4000, required: bool = False) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f'invalid_{field}')
    if any(ord(char) < 32 and char not in '\n\t' for char in value):
        raise ValueError(f'invalid_{field}')
    return value.strip()


def _identifier(value: Any, field: str) -> str:
    value = _text(value, field, 80, True)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}', value or ''):
        raise ValueError(f'invalid_{field}')
    return str(value)


def _money(value: Any, field: str, upper: str) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError(f'invalid_{field}')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f'invalid_{field}') from exc
    if not result.is_finite() or result < 0 or result > Decimal(upper):
        raise ValueError(f'invalid_{field}')
    if result != result.quantize(Decimal('0.01')):
        raise ValueError(f'invalid_{field}')
    return result


def validate_request(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or set(payload) - FIELDS:
        raise ValueError('unknown_or_invalid_request_fields')
    result = {key: _identifier(payload.get(key), key) for key in ('tenant_id', 'request_id', 'project_id')}
    result['problem'] = _text(payload.get('problem'), 'problem', required=True)
    for key in ('customer_context', 'current_workflow', 'baseline', 'desired_outcome', 'constraints'):
        result[key] = _text(payload.get(key), key)
    refs = payload.get('evidence_refs', [])
    if not isinstance(refs, list) or len(refs) > 20:
        raise ValueError('invalid_evidence_refs')
    if 'data_authorized' in payload and type(payload['data_authorized']) is not bool:
        raise ValueError('invalid_data_authorized')
    if payload.get('data_authorized') is not True:
        raise ValueError('authorized_data_required_even_for_preparation')
    result['data_authorized'] = True
    result['evidence_refs'] = []
    for ref in refs:
        if not isinstance(ref, dict) or set(ref) != {'ref', 'sha256', 'tenant_id'}:
            raise ValueError('invalid_evidence_ref')
        if ref['tenant_id'] != result['tenant_id']:
            raise ValueError('evidence_tenant_mismatch')
        if not isinstance(ref['sha256'], str) or not re.fullmatch('[a-f0-9]{64}', ref['sha256']):
            raise ValueError('invalid_evidence_digest')
        item = {'ref': _text(ref['ref'], 'evidence_ref', 256, True),
                'sha256': ref['sha256'], 'tenant_id': result['tenant_id']}
        if item not in result['evidence_refs']:
            result['evidence_refs'].append(item)
    result['evidence_refs'].sort(key=lambda item: (str(item['ref']), item['sha256']))
    cost = _money(payload.get('estimated_cost_sar'), 'estimated_cost_sar', '1000000000')
    margin = _money(payload.get('target_margin_pct'), 'target_margin_pct', '90')
    result['estimated_cost_sar'] = format(cost, '.2f') if cost is not None else None
    result['target_margin_pct'] = format(margin, '.2f') if margin is not None else None
    return result


def prepare(payload: Any) -> dict[str, Any]:
    """Generate a deterministic proposal/project PREPARATION bundle; never approve."""
    data = validate_request(payload)
    catalog = load_catalog()
    match = [(s, r) for s in catalog['sectors'] for r in s['projects'] if r[0] == data['project_id']]
    if not match:
        raise ValueError('unknown_project_id')
    sector, project = match[0]
    missing = [key for key in ('current_workflow', 'baseline', 'desired_outcome', 'constraints') if not data[key]]
    if not data['evidence_refs']:
        missing.append('evidence_refs')
    questions = {
        'current_workflow': 'Which systems, handoffs, owners and exceptions make up the current workflow?',
        'baseline': 'What baseline, measurement period and source can the customer verify?',
        'desired_outcome': 'Which business change should be measured and accepted?',
        'constraints': 'What data boundaries, budget, timing and procurement constraints apply?',
        'evidence_refs': 'Which authorized evidence references support the stated problem?',
    }
    review = bool(sector['domain_review'] or project[1] in {'industrial', 'governance'})
    route = 'QUALIFIED_PARTNER_REVIEW' if 'partner' in sector['route_hint'] else 'VALIDATE_DIRECT_CAPABILITY'
    cost = Decimal(data['estimated_cost_sar']) if data['estimated_cost_sar'] is not None else None
    margin = Decimal(data['target_margin_pct']) if data['target_margin_pct'] is not None else None
    floor = None
    if cost is not None and margin is not None:
        floor = format((cost / (1 - margin / 100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), '.2f')
    return {
        'schema_version': 'dealix.market-to-delivery.preparation.v1',
        'artifact_digest': digest({'engine_sha256': ENGINE_SHA256, 'catalog_digest': digest(catalog), 'input': data}),
        'engine_sha256': ENGINE_SHA256,
        'tenant_id': data['tenant_id'], 'request_id': data['request_id'],
        'catalog_digest': digest(catalog), 'status': 'NEEDS_INPUT' if missing else 'DRAFT_PREPARED_FOR_REVIEW',
        'authority': {effect: False for effect in FORBIDDEN_EFFECTS},
        'evidence_verification': 'REFERENCES_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED',
        'capability_readiness': 'UNVERIFIED_UNTIL_TESTED',
        'routing': {'sector_id': sector['id'], 'arm_id': CAPABILITY_ARMS[project[1]],
                    'route_hypothesis': route, 'domain_review_required': review,
                    'source_route_hint': sector['route_hint'], 'owner': 'dealix-sales'},
        'missing_inputs': missing,
        'discovery_questions': [questions[key] for key in missing],
        'diagnostic': {
            'customer_context': data['customer_context'], 'problem': data['problem'],
            'evidence_refs': data['evidence_refs'], 'current_workflow': data['current_workflow'],
            'baseline': data['baseline'], 'desired_outcome': data['desired_outcome'],
            'constraints': data['constraints'], 'intervention_hypothesis': project[2],
            'candidate_measure': project[3], 'acceptance_criteria': 'REQUIRES_CUSTOMER_VALIDATION',
            'duration_days': None, 'guaranteed_outcome': False,
        },
        'quote_draft': {
            'status': 'NOT_BINDING_NOT_APPROVED', 'scope_hypothesis': project[2],
            'deliverables': ['Validated workflow and baseline', 'Bounded implementation plan',
                             'Acceptance test evidence', 'Handover and proof review'],
            'price_sar': None, 'payment_terms': None, 'sla': None, 'duration_days': None,
            'cost_assumption_sar': data['estimated_cost_sar'],
            'target_margin_assumption_pct': data['target_margin_pct'],
            'internal_cost_based_floor_sar': floor,
            'floor_is_not_market_price_or_approved_quote': True,
            'approval_required': True, 'approval_authority': 'existing_approval_center',
            'quote_authority_source': 'api/routers/commercial_runtime_truth.py',
            'exclusions': ['Unapproved production changes', 'Unqualified specialist work', 'Guaranteed outcome'],
        },
        'negotiation_drafts': [
            {'option': 'NARROW_SCOPE', 'tradeoff': 'Reduce deliverables, not acceptance quality.'},
            {'option': 'PHASE_DELIVERY', 'tradeoff': 'Validate one workflow before expanding.'},
            {'option': 'INTEGRATE_EXISTING', 'tradeoff': 'Evaluate an existing product before custom build.'},
            {'option': 'QUALIFIED_PARTNER', 'tradeoff': 'Verify competence, capacity, data terms and pricing.'},
        ],
        'project_cell_draft': {
            'status': 'NOT_PROVISIONED', 'canonical_owner': 'dealix-delivery',
            'temporary_workloads': ['requirements', 'architecture', 'implementation', 'test',
                                    'independent_review', 'documentation', 'release_evidence'],
            'accountable_human': None, 'independent_reviewer': None, 'approved_region': None,
            'tenant_id': data['tenant_id'], 'budget_sar': None, 'ttl_utc': None,
            'production_credentials_available': False, 'shared_customer_memory': False,
            'prerequisites': ['Approved customer scope', 'Verified start/payment authority',
                              'Qualified delivery capacity', 'Data and subprocessor authorization',
                              'Isolated workspace and credentials', 'Budget, TTL and stop rules',
                              'Independent acceptance review', 'Rollback and exit plan'],
        },
        'canonical_handoffs': [
            {'owner': 'dealix-sales', 'action': 'VALIDATE_DIAGNOSTIC_AND_DISCOVERY'},
            {'owner': 'dealix-pm', 'action': 'EXISTING_APPROVAL_CENTER_REVIEW'},
            {'owner': 'dealix-delivery', 'action': 'VERIFY_SCOPE_START_CAPACITY_AND_ISOLATION'},
            {'owner': 'dealix-engineer', 'action': 'TEST_BOUNDED_IMPLEMENTATION'},
            {'owner': 'dealix-content', 'action': 'DRAFT_ONLY_FROM_PERMISSIONED_VERIFIED_PROOF'},
        ],
        'economic_truth': {'verified_cash_sar': None, 'customer_validated_proof': None},
    }
