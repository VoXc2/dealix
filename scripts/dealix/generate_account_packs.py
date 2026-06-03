"""Generate Account Intelligence Packs.

IMPORTANT — data ethics enforced here:
  * Companies in the seed run are SYNTHETIC demo accounts (clearly labelled).
  * No personal names, emails, or phone numbers are ever invented.
  * Public contact channels reference only a generic website pattern with
    contact_confidence = low. Real runs must replace these with public or
    founder-provided data only (see docs/contacts/CONTACT_DISCOVERY_POLICY_AR.md).

The packs are fully deterministic so checks can re-derive every score.
"""
from __future__ import annotations

import argparse
import sys

from . import seeds
from .lib import dump_jsonl, load_jsonl, ROOT
from .scoring import account_score, cash_priority_score, final_account_score, need_fit_score

# Deterministic sector "weight" (attractiveness) 50..90, stable per sector.
SECTOR_WEIGHT = {sid: 50 + (i * 37) % 41 for i, sid in enumerate(seeds.SECTOR_IDS)}


def _suppression_set():
    path = ROOT / "data/suppression/do_not_contact.jsonl"
    if not path.exists():
        return set()
    return {row.get("domain", "").lower() for row in load_jsonl(path)}


def build_pack(index):
    sector = seeds.SECTOR_IDS[index % len(seeds.SECTOR_IDS)]
    sector_ar = dict(seeds.SECTORS)[sector]
    smap = seeds.sector_need_map()
    primary_need_id = smap[sector][0]
    secondary_need_id = smap[sector][1] if len(smap[sector]) > 1 else smap[sector][0]
    need = seeds.need_by_id(primary_need_id)
    core = need["core_system"]

    specialized = [s for s in seeds.iter_specialized_systems() if s["core_system"] == core]
    rec_specialized = specialized[index % len(specialized)]["id"]

    sprints = [s for s in seeds.iter_sprints() if s["need_id"] == primary_need_id]
    sprint = sprints[0] if sprints else seeds.iter_sprints()[0]

    # Deterministic pseudo-signals (public-observable type)
    signals = [
        "موقع نشط دون نموذج تواصل واضح",
        f"خدمات متعددة لقطاع {sector_ar}",
    ]
    need_conf = ["low", "medium", "high"][index % 3]
    contact_conf = "low"  # demo data: never claim high confidence on contacts

    company_name = f"شركة تجريبية {index + 1:03d}"
    website = f"https://demo-{index + 1:03d}.example.com"
    domain = f"demo-{index + 1:03d}.example.com"

    nf = need_fit_score(need_conf, len(signals))
    cash = cash_priority_score(
        urgency=40 + (index * 7) % 50,
        ticket_potential=SECTOR_WEIGHT[sector],
        speed_to_cash=50 + (index * 11) % 40,
    )
    acct = account_score(SECTOR_WEIGHT[sector], nf, has_public_channel=True)
    final = final_account_score(acct, nf, cash, contact_conf)

    return {
        "company_name": company_name,
        "website": website,
        "domain": domain,
        "sector": sector,
        "subsector": "",
        "city": "",
        "country": "SA",
        "signals_detected": signals,
        "evidence_level": "inferred",
        "detected_business_needs": [primary_need_id, secondary_need_id],
        "primary_need": primary_need_id,
        "secondary_need": secondary_need_id,
        "need_confidence": need_conf,
        "recommended_core_system": core,
        "recommended_specialized_system": rec_specialized,
        "sector_specific_sprint": sprint["id"],
        "delivery_variant": "starter",
        "buyer_roles": [need["buyer_role_ar"]],
        "public_contact_channels": [f"{website}/contact"],
        "contact_confidence": contact_conf,
        "email_angle": f"كيف يعالج {dict_core(core)} مشكلة {need['name_ar']} لدى {sector_ar}",
        "call_angle": f"سؤال تشخيصي عن {need['name_ar']}",
        "mini_proposal_title": f"سبرنت {need['name_ar']} — {sector_ar}",
        "required_inputs": sprint["required_inputs"],
        "acceptance_criteria": sprint["acceptance_criteria"],
        "cash_priority_score": cash,
        "need_fit_score": nf,
        "account_score": acct,
        "final_account_score": final,
        "next_action": "إعداد مسودة بريد + بطاقة احتياج للاعتماد",
        "suppressed": False,
        "demo": True,
    }


def dict_core(core_id):
    for c in seeds.CORE_SYSTEMS:
        if c["id"] == core_id:
            return c["name_ar"]
    return core_id


def build(limit, dry_run=False):
    suppressed = _suppression_set()
    packs = []
    for i in range(limit):
        pack = build_pack(i)
        if pack["domain"].lower() in suppressed:
            pack["suppressed"] = True
            pack["next_action"] = "إيقاف — الشركة في قائمة عدم التواصل"
        packs.append(pack)

    packs.sort(key=lambda p: p["final_account_score"], reverse=True)
    if dry_run:
        return packs, None
    out = "data/account_intelligence/account_packs.jsonl"
    dump_jsonl(out, packs)
    return packs, out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate account intelligence packs")
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    packs, out = build(args.limit, dry_run=args.dry_run)
    top = packs[0] if packs else None
    print(f"Generated {len(packs)} account packs (limit={args.limit}, dry_run={args.dry_run}).")
    if top:
        print(f"  top account: {top['company_name']} | final_score={top['final_account_score']} | need={top['primary_need']}")
    if out:
        print(f"  written: {out}")
    else:
        print("  dry-run: nothing written to disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
