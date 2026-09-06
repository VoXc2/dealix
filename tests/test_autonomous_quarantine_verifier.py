"""Isolated verifier-logic tests; synthetic fixtures are NOT production proof."""
from __future__ import annotations

import functools
import importlib.util
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace as Node
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/ops/verify_autonomous_quarantine.py"
SPEC = importlib.util.spec_from_file_location("quarantine_verifier_under_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(q)


def endpoint(module: str = "api.routers.agents"):
    def handler():
        return None
    handler.__module__ = module
    return handler


def route(module: str = "api.routers.agents"):
    return Node(endpoint=endpoint(module), tags=[], path="/health")


class TestQuarantineVerifier(unittest.TestCase):
    def test_comments_and_docstrings_are_not_imports(self):
        source = '# api.routers.autonomous remains deliberately unregistered\n'
        source += '"""Do not add autonomous.router or api.routers.autonomous."""\n'
        self.assertEqual(q._registration_findings(source), [])

    def test_import_aliases_and_relative_imports(self):
        for source in (
            "import api.routers.autonomous as legacy",
            "from api.routers import autonomous as legacy",
            "from api.routers.autonomous import router as legacy",
            "from ... import autonomous as legacy",
        ):
            with self.subTest(source=source):
                self.assertTrue(q._registration_findings(source))

    def test_literal_dynamic_import(self):
        self.assertTrue(q._registration_findings(
            "legacy = importlib.import_module('api.routers.autonomous')"
        ))
        self.assertTrue(q._registration_findings("__import__('api.routers.autonomous')"))

    def test_other_module_name_is_not_legacy(self):
        self.assertEqual(q._registration_findings(
            "import api.routers.autonomous_company\nfrom api.routers import agents"
        ), [])

    def test_invalid_syntax_is_not_silently_ignored(self):
        with self.assertRaises(SyntaxError):
            q._registration_findings("from (")

    def test_path_keywords_are_inventoried(self):
        paths = q._route_paths(
            "@router.post(path='/payments/mark-paid')\nasync def pay(): pass\n"
            "@router.get('/customers/onboard')\ndef customer(): pass\n"
        )
        self.assertEqual(paths, {"/payments/mark-paid", "/customers/onboard"})

    def test_lazy_inclusion_without_tags_detects_legacy_endpoint(self):
        lazy = Node(original_router=Node(routes=[route(q.LEGACY_MODULE)]),
                    include_context=Node(prefix="/api/v1", tags=[]))
        count, bad = q._inspect_routes([Node(routes=[lazy])])
        self.assertEqual(count, 1)
        self.assertIn("legacy_endpoint_module", bad)

    def test_lazy_context_tag_is_checked(self):
        lazy = Node(original_router=Node(routes=[route()]),
                    include_context=Node(tags=["autonomous"]))
        self.assertIn("legacy_tag", q._inspect_routes([lazy])[1])

    def test_mount_app_is_traversed(self):
        mounted = Node(app=Node(routes=[route(q.LEGACY_MODULE)]))
        self.assertIn("legacy_endpoint_module", q._inspect_routes([mounted])[1])

    def test_opaque_mount_endpoint_does_not_hide_uninspectable_app(self):
        class Mount:
            routes = []
            app = object()
            endpoint = staticmethod(endpoint())

        with self.assertRaises(q.InspectionError) as caught:
            q._inspect_routes([Mount()])
        self.assertEqual(caught.exception.code, "opaque_route_node")
        self.assertEqual(caught.exception.detail, "builtins.object")

    def test_route_cycle_terminates_and_reused_nodes_deduplicate(self):
        leaf = route()
        root = Node(routes=[leaf, leaf])
        root.routes.append(root)
        self.assertEqual(q._inspect_routes([root]), (1, []))

    def test_partial_and_decorated_endpoints_are_checked(self):
        bad = endpoint(q.LEGACY_MODULE)
        wrapper = endpoint()
        wrapper.__wrapped__ = bad
        for handler in (functools.partial(bad), wrapper):
            self.assertIn("legacy_endpoint_module", q._inspect_routes([
                Node(endpoint=handler, tags=[])
            ])[1])

    def test_empty_router_alongside_real_routes_is_valid(self):
        self.assertEqual(q._inspect_routes([Node(routes=[]), route()]), (1, []))

    def test_empty_inventory_is_not_a_pass(self):
        for roots in ([], [Node(routes=[])]):
            with self.subTest(roots=roots):
                with self.assertRaises(q.InspectionError) as caught:
                    q._inspect_routes(roots)
                self.assertEqual(caught.exception.code, "empty_route_inventory")

    def test_opaque_nodes_are_not_silently_skipped(self):
        with self.assertRaises(q.InspectionError) as caught:
            q._inspect_routes([route(), object()])
        self.assertEqual(caught.exception.code, "opaque_route_node")
        self.assertEqual(caught.exception.detail, "builtins.object")

    def test_unsafe_inspection_detail_is_suppressed(self):
        err = q.InspectionError("opaque_route_node", "unsafe detail with spaces")
        self.assertIsNone(err.detail)

    def test_wrong_source_module_rejected(self):
        with patch.object(q.importlib, "import_module", return_value=Node(__file__="/other.py")):
            with self.assertRaises(q.InspectionError) as caught:
                q._checked_import("api.main", Path("/expected.py"))
            self.assertEqual(caught.exception.code, "module_source_mismatch")

    def test_missing_safety_flags_hold_without_imports(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(q, "_checked_import") as load:
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(q.main(), 4)
            load.assert_not_called()
            self.assertIn("AUTONOMOUS_QUARANTINE=HOLD", output.getvalue())

    def _main_fixture(self, source: str, app_routes=None, load_error=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            domain_path = root / "domain.py"
            legacy_path = root / "legacy.py"
            domain_path.write_text(source, encoding="utf-8")
            legacy_path.write_text("@router.post('/payments/mark-paid')\ndef old(): pass\n")
            domain = Node(get_routers=lambda: [Node(routes=[route()])])
            app = Node(app=Node(routes=app_routes if app_routes is not None else [route()]))
            flags = dict.fromkeys(q.SAFE_FLAGS, "0") | {"APP_ENV": "test"}
            effects = load_error if load_error else [domain, app]
            with patch.object(q, "DOMAIN_INIT", domain_path), patch.object(q, "LEGACY_ROUTER", legacy_path):
                with patch.dict(os.environ, flags, clear=True), patch.object(q, "_checked_import", side_effect=effects):
                    with patch.object(q.sys, "path", q.sys.path.copy()), redirect_stdout(io.StringIO()) as output:
                        code = q.main()
            return code, output.getvalue()

    def test_main_positive_result_is_explicitly_not_deployed_proof(self):
        code, output = self._main_fixture("# api.routers.autonomous is quarantined\n")
        self.assertEqual(code, 0)
        self.assertIn("deployed_production_verified=false", output)
        self.assertIn("tenant_isolation_verified=false", output)
        self.assertIn("re_registration_authorized=false", output)

    def test_source_import_rejected(self):
        code, output = self._main_fixture("from api.routers import autonomous as legacy\n")
        self.assertEqual(code, 2)
        self.assertIn("legacy_domain_import_detected", output)

    def test_application_leak_outside_agents_domain_rejected(self):
        code, output = self._main_fixture("# quarantine\n", [route(q.LEGACY_MODULE)])
        self.assertEqual(code, 3)
        self.assertIn("legacy_endpoint_module", output)

    def test_structural_inspection_hold_exposes_only_safe_stage_code_and_type(self):
        code, output = self._main_fixture("# quarantine\n", [object()])
        self.assertEqual(code, 4)
        self.assertIn("inspection_stage=application_routes", output)
        self.assertIn("inspection_code=opaque_route_node", output)
        self.assertIn("inspection_detail=builtins.object", output)
        self.assertIn("error_type=InspectionError", output)

    def test_incomplete_import_holds_without_leaking_exception_content(self):
        code, output = self._main_fixture("# quarantine\n", load_error=RuntimeError("sensitive-test-value"))
        self.assertEqual(code, 4)
        self.assertIn("inspection_stage=domain_import", output)
        self.assertIn("error_type=RuntimeError", output)
        self.assertNotIn("sensitive-test-value", output)


if __name__ == "__main__":
    unittest.main()
