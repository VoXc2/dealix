#!/usr/bin/env python3
"""
Dealix Business Need Intelligence Validator
Validates the Business Need Intelligence layer for internal consistency and
the hard rules from the expansion spec. Prints a report and exits 0/1.

Checks:
  - every sector maps to at least 3 needs
  - every need maps to at least one core system
  - every specialized system maps to exactly one core system
  - every specialized sprint maps to one core system
  - every specialized sprint has deliverables, required inputs, acceptance criteria
  - every delivery variant has required inputs and acceptance criteria
  - cross-references resolve (sectors -> sprints/systems/needs/variants)
  - Account Pack example carries the need intelligence fields + valid score
  - Need Fit Score weights sum to 100
  - no guaranteed claims in the new docs/data/reports

Uses jsonschema if installed; otherwise performs structural checks only.
"""

import json
import sys
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent
DATA = BASE / "data" / "business_need_intelligence"
SCHEMAS = BASE / "schemas"
DOCS = BASE / "docs" / "business_need_intelligence"
ACCOUNT_DOCS = BASE / "docs" / "account_intelligence"
SITE_DOCS = BASE / "docs" / "site"
REPORTS = BASE / "reports" / "business_need_intelligence"

CORE_SYSTEMS = {
    "revenue_os",
    "executive_command_os",
    "followup_recovery_os",
    "whatsapp_client_os",
    "proposal_proof_os",
}

NEEDS = {
    "lead_capture", "lead_response", "qualification", "follow_up",
    "sales_execution", "proposal", "customer_support", "client_onboarding",
    "delivery", "reporting", "renewal", "service_quality", "knowledge",
    "finance_visibility", "ai_governance",
}

# Evidence-aware wording rule: these terms read as guarantees and are banned.
BANNED_TERMS = [
    "نضمن", "مضمون", "ضمان", "نتعهد", "guarantee", "guaranteed", "100%",
    "نضاعف أرباحك", "نضاعف ارباحك",
]


def load_yaml(name: str) -> dict:
    with open(DATA / name, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class Results:
    def __init__(self):
        self.checks: list[tuple[str, bool, list[str]]] = []

    def add(self, name: str, ok: bool, details: list[str] | None = None):
        self.checks.append((name, ok, details or []))

    @property
    def failed(self) -> int:
        return sum(1 for _, ok, _ in self.checks if not ok)


def check_needs_router(router: dict, r: Results):
    needs = {n["id"]: n for n in router.get("needs", [])}
    # every need maps to at least one core system
    bad = []
    for nid, n in needs.items():
        cores = [n.get("primary_core_system")] + list(n.get("secondary_core_systems", []))
        cores = [c for c in cores if c]
        if not cores:
            bad.append(f"need '{nid}' has no core system")
        for c in cores:
            if c not in CORE_SYSTEMS:
                bad.append(f"need '{nid}' references unknown core '{c}'")
    missing = NEEDS - set(needs)
    if missing:
        bad.append(f"missing need definitions: {sorted(missing)}")
    r.add("every need maps to at least one core system (15 needs present)", not bad, bad)

    # every specialized system maps to exactly one core
    bad2 = []
    seen: dict[str, str] = {}
    for s in router.get("specialized_systems", []):
        name, core = s.get("name"), s.get("core_system")
        if core not in CORE_SYSTEMS:
            bad2.append(f"specialized '{name}' -> unknown core '{core}'")
        if name in seen and seen[name] != core:
            bad2.append(f"specialized '{name}' mapped to two cores")
        seen[name] = core
        for nd in s.get("serves_needs", []):
            if nd not in NEEDS:
                bad2.append(f"specialized '{name}' serves unknown need '{nd}'")
    r.add("every specialized system maps to exactly one core system", not bad2, bad2)
    return needs


def check_sectors(sectors_doc: dict, sprints: dict, variants: dict, r: Results):
    sectors = sectors_doc.get("sectors", [])
    bad = []
    for s in sectors:
        sid = s.get("id")
        top = s.get("top_needs", [])
        if len(top) < 3:
            bad.append(f"sector '{sid}' maps to <3 needs ({len(top)})")
        for nd in top:
            if nd not in NEEDS:
                bad.append(f"sector '{sid}' has unknown need '{nd}'")
        for key in ("primary_system", "secondary_system", "expansion_system"):
            val = s.get(key)
            if val and val not in CORE_SYSTEMS:
                bad.append(f"sector '{sid}'.{key} unknown core '{val}'")
        fs = s.get("first_sprint")
        if fs not in sprints:
            bad.append(f"sector '{sid}' first_sprint '{fs}' not in sprint library")
        dv = s.get("delivery_variant")
        if dv not in variants:
            bad.append(f"sector '{sid}' delivery_variant '{dv}' not in variant library")
    r.add("every sector maps to at least 3 needs (refs resolve)", not bad, bad)
    return sectors


def check_sprints(sprints_doc: dict, r: Results):
    sprints = {sp["id"]: sp for sp in sprints_doc.get("sprints", [])}
    bad_core, bad_deliv = [], []
    for sid, sp in sprints.items():
        if sp.get("core_system") not in CORE_SYSTEMS:
            bad_core.append(f"sprint '{sid}' -> unknown core '{sp.get('core_system')}'")
        if sp.get("need") not in NEEDS:
            bad_core.append(f"sprint '{sid}' -> unknown need '{sp.get('need')}'")
        for field in ("deliverables", "required_inputs", "acceptance_criteria"):
            if not sp.get(field):
                bad_deliv.append(f"sprint '{sid}' missing {field}")
    r.add("every specialized sprint maps to one core system", not bad_core, bad_core)
    r.add(
        "every specialized sprint has deliverables, inputs & acceptance criteria",
        not bad_deliv, bad_deliv,
    )
    # core coverage: all 5 cores used by at least one sprint
    used = {sp.get("core_system") for sp in sprints.values()}
    cov = CORE_SYSTEMS - used
    r.add("all 5 core systems are exercised by sprints",
          not cov, [f"unused cores: {sorted(cov)}"] if cov else [])
    return sprints


def check_variants(variants_doc: dict, r: Results):
    variants = variants_doc.get("variants", {})
    bad = []
    for vid, v in variants.items():
        if v.get("core_system") not in CORE_SYSTEMS:
            bad.append(f"variant '{vid}' -> unknown core '{v.get('core_system')}'")
        for field in ("specialized_delivery_pack", "required_inputs", "acceptance_criteria"):
            if not v.get(field):
                bad.append(f"variant '{vid}' missing {field}")
    r.add("every delivery variant has inputs & acceptance criteria", not bad, bad)
    return variants


def check_buyers(buyers_doc: dict, r: Results):
    needs = buyers_doc.get("needs", {})
    bad = []
    for nid, b in needs.items():
        if nid not in NEEDS:
            bad.append(f"buyer map has unknown need '{nid}'")
        if not b.get("primary_roles"):
            bad.append(f"need '{nid}' has no primary buyer roles")
    missing = NEEDS - set(needs)
    if missing:
        bad.append(f"buyer roles missing for needs: {sorted(missing)}")
    r.add("every need has at least one buyer role", not bad, bad)


def check_account_pack(r: Results):
    path = DATA / "account_pack_example.yaml"
    with open(path, "r", encoding="utf-8") as f:
        pack = yaml.safe_load(f)
    required = [
        "detected_business_need", "need_confidence", "recommended_core_system",
        "recommended_specialized_system", "sector_specific_sprint",
        "specialized_delivery_pack", "buyer_role_by_need", "email_angle_by_need",
        "call_angle_by_need", "upsell_path_by_need", "need_fit_score",
    ]
    bad = [f"missing field '{k}'" for k in required if k not in pack]
    if pack.get("detected_business_need") not in NEEDS:
        bad.append("detected_business_need not a valid need")
    if pack.get("recommended_core_system") not in CORE_SYSTEMS:
        bad.append("recommended_core_system not a valid core")
    conf = pack.get("need_confidence")
    if not isinstance(conf, (int, float)) or not (0 <= conf <= 1):
        bad.append("need_confidence not in [0,1]")
    score = pack.get("need_fit_score", {})
    weights = {
        "sector_need_match": 25, "signal_strength": 20, "delivery_readiness": 20,
        "buyer_clarity": 15, "first_sprint_clarity": 10, "upsell_path": 10,
    }
    subtotal = 0
    for k, mx in weights.items():
        v = score.get(k)
        if v is None or not (0 <= v <= mx):
            bad.append(f"score.{k} missing or out of range 0..{mx}")
        else:
            subtotal += v
    if score.get("total") != subtotal:
        bad.append(f"score.total {score.get('total')} != sum {subtotal}")
    r.add("Account Pack example carries need intelligence fields + valid score",
          not bad, bad)

    # Need Fit Score weights sum to 100
    r.add("Need Fit Score weights sum to 100",
          sum(weights.values()) == 100,
          [] if sum(weights.values()) == 100 else [f"weights sum to {sum(weights.values())}"])


def check_solutions(sprints: dict, r: Results):
    """Public web projection must stay consistent and simple (refs resolve)."""
    path = DATA / "sector_solutions.yaml"
    if not path.exists():
        r.add("public sector_solutions projection present", False, ["file missing"])
        return
    with open(path, "r", encoding="utf-8") as f:
        sol = yaml.safe_load(f)
    bad = []
    cores = {c.get("id") for c in sol.get("core_systems", [])}
    if cores != CORE_SYSTEMS:
        bad.append(f"public core_systems != the 5 cores (got {sorted(cores)})")
    for s in sol.get("sectors", []):
        if s.get("primary_system") not in CORE_SYSTEMS:
            bad.append(f"solution '{s.get('id')}' primary_system invalid")
        if s.get("first_sprint") not in sprints:
            bad.append(f"solution '{s.get('id')}' first_sprint not in library")
    for opt in sol.get("diagnostic", {}).get("options", []):
        if opt.get("starting_need") not in NEEDS:
            bad.append(f"diagnostic option starting_need invalid: {opt.get('starting_need')}")
    r.add("public sector_solutions projection is consistent (only 5 systems)",
          not bad, bad)


def check_schemas_present(r: Results):
    required = [
        "business_need.schema.json",
        "specialized_sprint.schema.json",
        "need_to_system_route.schema.json",
        "account_pack_need_intelligence.schema.json",
    ]
    bad = []
    for s in required:
        p = SCHEMAS / s
        if not p.exists():
            bad.append(f"missing schema {s}")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad.append(f"{s} invalid JSON: {e}")
    r.add("JSON schemas present and parseable", not bad, bad)


def check_no_guaranteed_claims(r: Results):
    roots = [DOCS, ACCOUNT_DOCS, SITE_DOCS, DATA, REPORTS]
    hits = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.suffix.lower() not in (".md", ".yaml", ".yml"):
                continue
            text = p.read_text(encoding="utf-8")
            for term in BANNED_TERMS:
                if term in text:
                    hits.append(f"{p.relative_to(BASE)} contains '{term}'")
    r.add("no guaranteed claims in new docs/data/reports", not hits, hits)


def try_jsonschema(sprints: dict, needs_router: dict, r: Results):
    try:
        import jsonschema  # type: ignore
    except ImportError:
        r.add("jsonschema validation (optional)", True,
              ["jsonschema not installed — structural checks used instead (non-blocking)"])
        return
    bad = []
    sprint_schema = json.loads((SCHEMAS / "specialized_sprint.schema.json").read_text("utf-8"))
    route_schema = json.loads((SCHEMAS / "need_to_system_route.schema.json").read_text("utf-8"))
    for sp in sprints.values():
        try:
            jsonschema.validate(sp, sprint_schema)
        except jsonschema.ValidationError as e:
            bad.append(f"sprint '{sp.get('id')}': {e.message}")
    for n in needs_router.get("needs", []):
        try:
            jsonschema.validate(n, route_schema)
        except jsonschema.ValidationError as e:
            bad.append(f"need '{n.get('id')}': {e.message}")
    r.add("jsonschema validation of sprints & routes", not bad, bad)


def main() -> int:
    print("=" * 80)
    print("  DEALIX — BUSINESS NEED INTELLIGENCE VALIDATOR")
    print("=" * 80)
    print()

    r = Results()
    try:
        router = load_yaml("need_to_system_router.yaml")
        sectors_doc = load_yaml("sector_need_map.yaml")
        sprints_doc = load_yaml("specialized_sprint_library.yaml")
        variants_doc = load_yaml("delivery_variant_by_sector.yaml")
        buyers_doc = load_yaml("buyer_role_by_need.yaml")
        load_yaml("sector_signal_library.yaml")  # parse check
    except (FileNotFoundError, yaml.YAMLError) as e:
        print(f"  FATAL: could not load data files: {e}")
        return 1

    check_needs_router(router, r)
    sprints = check_sprints(sprints_doc, r)
    variants = check_variants(variants_doc, r)
    check_sectors(sectors_doc, sprints, variants, r)
    check_buyers(buyers_doc, r)
    check_account_pack(r)
    check_solutions(sprints, r)
    check_schemas_present(r)
    check_no_guaranteed_claims(r)
    try_jsonschema(sprints, router, r)

    print(f"  Loaded: {len(router.get('needs', []))} needs, "
          f"{len(sectors_doc.get('sectors', []))} sectors, "
          f"{len(sprints)} sprints, {len(variants)} delivery variants")
    print()
    for name, ok, details in r.checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        for d in details:
            mark = "        - " if ok else "        ! "
            print(f"{mark}{d}")
    print()
    print("  " + "-" * 76)
    if r.failed == 0:
        print(f"  RESULT: ✅ ALL {len(r.checks)} CHECKS PASSED")
    else:
        print(f"  RESULT: ❌ {r.failed}/{len(r.checks)} CHECKS FAILED")
    print("  " + "=" * 76)
    return 0 if r.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
