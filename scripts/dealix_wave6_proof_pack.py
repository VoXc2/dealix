#!/usr/bin/env python3
"""Wave 6 Phase 7 — proof pack generator (post-pilot).

Reads a delivery_session.json and emits a Proof Pack draft.

Hard rules:
- If no proof events → output EMPTY_INTERNAL_DRAFT (not a fake pack)
- public_allowed=False by default
- approval_required
- Arabic primary, English secondary
- No fake metrics / testimonials
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LIVE_DIR = Path("docs/wave6/live")


def build_proof_pack(*, company: str, session: dict[str, Any],
                     allow_empty: bool) -> dict[str, Any]:
    proof_event_ids = session.get("proof_event_ids", [])
    deliverables = session.get("deliverables", [])

    if not proof_event_ids and not allow_empty:
        return {
            "status": "EMPTY_INTERNAL_DRAFT",
            "company": company,
            "proof_event_count": 0,
            "deliverable_count": 0,
            "is_publishable": False,
            "public_allowed": False,
            "reason_ar": "لا proof events مسجّلة بعد. هذا draft داخلي فقط — لا ينشر.",
            "reason_en": "No proof events recorded yet. Internal draft only — do not publish.",
        }

    return {
        "status": "INTERNAL_DRAFT" if proof_event_ids else "EMPTY_INTERNAL_DRAFT_FORCED",
        "pack_id": f"pack_w6_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
        "company": company,
        "session_id": session.get("session_id"),
        "service_type": session.get("service_type"),
        "proof_event_count": len(proof_event_ids),
        "deliverable_count": len(deliverables),
        "is_publishable": False,    # always false at this stage
        "public_allowed": False,    # consent required first
        "approval_required": True,
        "consent_required": True,
        "redaction_required": True,
        "narrative_ar": (
            f"دراسة حالة داخليّة لشركة {company}. "
            f"تم تسليم الخدمة عبر جلسة {session.get('session_id', '—')}. "
            f"عدد proof events موثّقة: {len(proof_event_ids)}. "
            f"عدد deliverables: {len(deliverables)}. "
            f"النشر يحتاج توقيع العميل + مراجعة المؤسس."
        ),
        "narrative_en": (
            f"Internal case study for {company}. "
            f"Service delivered via session {session.get('session_id', '—')}. "
            f"Proof events recorded: {len(proof_event_ids)}. "
            f"Deliverables: {len(deliverables)}. "
            f"Publication requires customer signature + founder review."
        ),
        "next_steps_ar": [
            "اطلب توقيع العميل عبر POST /api/v1/proof-ledger/consent/request",
            "بعد التوقيع: شغّل assemble_proof_pack بالأحداث المؤكّدة",
            "بعد الإطار النهائي: أرسل للعميل للموافقة قبل النشر",
        ],
        "next_steps_en": [
            "Request customer signature via POST /api/v1/proof-ledger/consent/request",
            "After signing: run assemble_proof_pack on confirmed events",
            "After final frame: send to customer for approval before publish",
        ],
        "no_fake_proof": True,
        "no_fake_metrics": True,
        "no_fake_testimonial": True,
        "safety_summary": "internal_only_default_consent_required_before_publish",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def render_markdown(p: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Proof Pack (Internal Draft) — {p['company']}")
    lines.append("")
    lines.append(f"**Status:** `{p['status']}`")
    lines.append(f"**Public allowed:** `{p.get('public_allowed', False)}`")
    lines.append(f"**Is publishable:** `{p.get('is_publishable', False)}`")
    lines.append("")
    if p["status"] == "EMPTY_INTERNAL_DRAFT":
        lines.append("## ⚠️ Empty pack")
        lines.append(f"- **AR:** {p['reason_ar']}")
        lines.append(f"- **EN:** {p['reason_en']}")
        return "\n".join(lines)

    lines.append("## النصّ (Internal narrative)")
    lines.append(p["narrative_ar"])
    lines.append("")
    lines.append("**English:**")
    lines.append(p["narrative_en"])
    lines.append("")
    lines.append("## الخطوات التالية")
    for step in p["next_steps_ar"]:
        lines.append(f"- {step}")
    lines.append("")
    lines.append("## Hard rules (Article 8)")
    lines.append("- لا proof مزيّف")
    lines.append("- لا أرقام مخترعة")
    lines.append("- لا testimonial بدون توقيع")
    lines.append(f"- {p['safety_summary']}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 proof pack generator")
    p.add_argument("--company", required=True)
    p.add_argument("--delivery-session", default=str(LIVE_DIR / "delivery_session.json"))
    p.add_argument("--allow-empty", action="store_true",
                   help="Generate placeholder pack even with zero events")
    p.add_argument("--out-md", default=None)
    p.add_argument("--out-json", default=None)
    args = p.parse_args()

    session_path = Path(args.delivery_session)
    if not session_path.exists():
        print(f"REFUSING: delivery_session.json not found at {session_path}", file=sys.stderr)
        return 2

    session = json.loads(session_path.read_text(encoding="utf-8"))

    pack = build_proof_pack(
        company=args.company, session=session, allow_empty=args.allow_empty,
    )

    out_md = Path(args.out_md) if args.out_md else LIVE_DIR / "proof_pack.md"
    out_json = Path(args.out_json) if args.out_json else LIVE_DIR / "proof_pack.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(pack), encoding="utf-8")
    out_json.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: wrote {out_md} + {out_json}")
    print(f"  status: {pack['status']}")
    print(f"  public_allowed: {pack.get('public_allowed', False)}")
    print(f"  proof_event_count: {pack.get('proof_event_count', 0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
