"""Isolated tests for preparation semantics, not production readiness."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

m = module('mtd', 'auto_client_acquisition/service_catalog/market_to_delivery.py')
runner = module('mtd_runner', 'scripts/commercial/run_market_to_delivery_preparation.py')


def request():
    return {'tenant_id': 'synthetic-tenant', 'request_id': 'test-001',
            'project_id': 'construction-01', 'problem': 'Synthetic RFI handoffs are unclear.',
            'data_authorized': True}


class PreparationTests(unittest.TestCase):
    def test_counts_and_unique_ids(self):
        c = m.load_catalog()
        self.assertEqual(len(c['commercial_arms']), 8)
        self.assertEqual(len(c['sectors']), 20)
        self.assertEqual(sum(len(s['projects']) for s in c['sectors']), 100)

    def test_all_hypotheses_can_prepare_without_authority(self):
        for sector in m.load_catalog()['sectors']:
            for row in sector['projects']:
                with self.subTest(project=row[0]):
                    p = request(); p['project_id'] = row[0]
                    out = m.prepare(p)
                    self.assertTrue(all(v is False for v in out['authority'].values()))
                    self.assertEqual(out['capability_readiness'], 'UNVERIFIED_UNTIL_TESTED')
                    self.assertIsNone(out['economic_truth']['verified_cash_sar'])

    def test_missing_data_not_fabricated(self):
        out = m.prepare(request())
        self.assertEqual(out['status'], 'NEEDS_INPUT')
        self.assertIn('baseline', out['missing_inputs'])
        self.assertIsNone(out['diagnostic']['baseline'])
        self.assertIsNone(out['diagnostic']['duration_days'])

    def test_supplied_data_still_not_verified(self):
        p = request()
        p.update(current_workflow='Synthetic queue', baseline='Synthetic 10 hours',
                 desired_outcome='Measure cycle time', constraints='Synthetic data only',
                 evidence_refs=[{'ref': 'synthetic://fixture', 'sha256': 'a'*64, 'tenant_id': p['tenant_id']}])
        out = m.prepare(p)
        self.assertEqual(out['status'], 'DRAFT_PREPARED_FOR_REVIEW')
        self.assertEqual(out['evidence_verification'], 'REFERENCES_SUPPLIED_NOT_INDEPENDENTLY_VERIFIED')
        self.assertTrue(out['quote_draft']['approval_required'])

    def test_data_authorization_missing_denied(self):
        p = request(); del p['data_authorized']
        with self.assertRaisesRegex(ValueError, 'authorized_data_required'):
            m.prepare(p)

    def test_string_boolean_denied(self):
        p = request(); p['data_authorized'] = 'true'
        with self.assertRaisesRegex(ValueError, 'invalid_data_authorized'):
            m.prepare(p)

    def test_unknown_authority_injection_denied(self):
        p = request(); p['auto_approve'] = True
        with self.assertRaisesRegex(ValueError, 'unknown_or_invalid'):
            m.prepare(p)

    def test_tenant_scope_mismatch_denied(self):
        p = request(); p['evidence_refs'] = [{'ref':'x','sha256':'b'*64,'tenant_id':'other'}]
        with self.assertRaisesRegex(ValueError, 'evidence_tenant_mismatch'):
            m.prepare(p)

    def test_bad_evidence_digest_denied(self):
        p = request(); p['evidence_refs'] = [{'ref':'x','sha256':'fake','tenant_id':p['tenant_id']}]
        with self.assertRaisesRegex(ValueError, 'invalid_evidence_digest'):
            m.prepare(p)

    def test_unknown_project_denied(self):
        p = request(); p['project_id'] = 'fake-01'
        with self.assertRaisesRegex(ValueError, 'unknown_project_id'):
            m.prepare(p)

    def test_request_path_traversal_denied(self):
        p = request(); p['request_id'] = '../../outside'
        with self.assertRaisesRegex(ValueError, 'invalid_request_id'):
            m.prepare(p)

    def test_oversized_problem_denied(self):
        p = request(); p['problem'] = 'x'*4001
        with self.assertRaisesRegex(ValueError, 'invalid_problem'):
            m.prepare(p)

    def test_cost_floor_is_not_quote(self):
        p = request(); p.update(estimated_cost_sar='60000', target_margin_pct='40')
        q = m.prepare(p)['quote_draft']
        self.assertEqual(q['internal_cost_based_floor_sar'], '100000.00')
        self.assertIsNone(q['price_sar'])
        self.assertTrue(q['approval_required'])

    def test_invalid_numbers_denied(self):
        for value in ['NaN', 'Infinity', '-1', True, '0.001', '1E9999']:
            with self.subTest(value=value):
                p = request(); p['estimated_cost_sar'] = value
                with self.assertRaises(ValueError): m.prepare(p)

    def test_invalid_margin_denied(self):
        for value in [100, 91, -5, 'NaN', True]:
            p = request(); p['target_margin_pct'] = value
            with self.assertRaises(ValueError): m.prepare(p)

    def test_identical_inputs_deterministic(self):
        self.assertEqual(m.prepare(request()), m.prepare(request()))

    def test_changed_input_changes_fingerprint(self):
        p = request(); p['problem'] += ' Changed'
        self.assertNotEqual(m.prepare(request())['artifact_digest'], m.prepare(p)['artifact_digest'])

    def test_engine_revision_changes_fingerprint(self):
        from unittest.mock import patch
        original = m.prepare(request())
        with patch.object(m, 'ENGINE_SHA256', 'f' * 64):
            revised = m.prepare(request())
        self.assertNotEqual(original['artifact_digest'], revised['artifact_digest'])
        self.assertEqual(revised['engine_sha256'], 'f' * 64)

    def test_no_provisioning_or_permanent_new_agents(self):
        out = m.prepare(request())
        self.assertEqual(out['project_cell_draft']['status'], 'NOT_PROVISIONED')
        self.assertEqual({h['owner'] for h in out['canonical_handoffs']}, set(m.CANONICAL_AGENTS))

    def test_domain_review_does_not_force_external_partner(self):
        out = m.prepare(request())
        self.assertTrue(out['routing']['domain_review_required'])
        self.assertEqual(out['routing']['route_hypothesis'], 'VALIDATE_DIRECT_CAPABILITY')

    def test_finance_specialist_review(self):
        p = request(); p['project_id'] = 'finance-01'
        out = m.prepare(p)
        self.assertTrue(out['routing']['domain_review_required'])
        self.assertEqual(out['routing']['route_hypothesis'], 'QUALIFIED_PARTNER_REVIEW')

    def test_projection_contains_no_private_fields(self):
        value = json.dumps(m.public_projection())
        for denied in ['evidence_refs', 'buyer_roles', 'price_sar', 'research_accounts', 'tenant_id']:
            self.assertNotIn(denied, value)

    def test_projection_matches_committed_copy(self):
        path = ROOT / 'apps/web/public/market-to-delivery-catalog.json'
        self.assertEqual(json.loads(path.read_text()), m.public_projection())

    def test_idempotent_local_write(self):
        with tempfile.TemporaryDirectory() as d:
            a = runner.write_bundle(m.prepare(request()), Path(d))
            b = runner.write_bundle(m.prepare(request()), Path(d))
            self.assertEqual(a, b)
            self.assertEqual((a/'receipt.json').stat().st_mode & 0o777, 0o600)

    def test_tampered_artifact_fails(self):
        with tempfile.TemporaryDirectory() as d:
            bundle = m.prepare(request()); a = runner.write_bundle(bundle, Path(d))
            (a/'quote-draft.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'tamper'):
                runner.write_bundle(bundle, Path(d))

    def test_symlink_output_denied(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); real=p/'real'; real.mkdir(mode=0o700); link=p/'link'; link.symlink_to(real)
            with self.assertRaisesRegex(ValueError, 'private_non_symlink'):
                runner.write_bundle(m.prepare(request()), link)

    def test_exact_secret_value_not_echoed(self):
        p = request(); p['approved_secret_value'] = 'DO_NOT_ECHO_TEST_VALUE'
        with self.assertRaises(ValueError) as err: m.prepare(p)
        self.assertNotIn('DO_NOT_ECHO', str(err.exception))

if __name__ == '__main__':
    unittest.main()
