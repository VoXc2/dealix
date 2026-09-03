#!/usr/bin/env python3
"""Dealix Unified Command Room — غرفة القيادة الموحّدة.

The single founder dashboard that brings together every angle of the
commercial launch into one self-contained, offline HTML page:

  * Launch readiness gate + paid-customer counter (Article 13: 0/3).
  * Outreach KPIs + funnel (drafted → sent → reply → meeting → won).
  * Pipeline by stage and value (from the CRM).
  * Follow-ups due today.
  * Sector breakdown with reply rates.
  * The 6-step canonical commercial path (quote-only; no public price catalogue).
  * Today's priority actions (derived from the CRM + ready drafts).
  * The 4 pending founder launch actions.

Doctrine-safe by design:
  * Read-only. It only reads local CSV/markdown outputs and renders HTML.
    It never sends WhatsApp/email/anything and opens no network connection.
  * Stdlib only — no third-party dependencies, no external assets.
  * Every panel degrades gracefully when its source is missing (never crashes).
  * The rendered HTML opens directly in any browser (file://), works offline.

It does not re-run or duplicate the engines — it aggregates their outputs.
Reuses the brand + render helpers from ``dealix_command_room.py``.

Usage:
    python scripts/dealix_unified_command_room.py
    python scripts/dealix_unified_command_room.py --dry-run
    python scripts/dealix_unified_command_room.py --out reports/command_room/index.html

Output:
    reports/command_room/index.html   (self-contained dashboard)
"""
from __future__ import annotations

import argparse
import csv
import html
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Reuse brand colours + render helpers from the original command room.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dealix_command_room import (
    ACCENT,
    DARK,
    PRIMARY,
    _funnel_rows,
    _kpi_card,
    _sector_rows,
    compute_kpis,
    count_ready_drafts,
    latest_drafts_dir,
    read_log,
    resolve_log,
)

DEFAULT_LOG = REPO_ROOT / "data" / "outreach" / "outreach_log.csv"
CRM_PIPELINE = REPO_ROOT / "company" / "crm" / "pipeline.csv"
RUNTIME = REPO_ROOT / "company" / "runtime"
OUT_HTML = REPO_ROOT / "reports" / "command_room" / "index.html"

# ---------------------------------------------------------------------------
# Static launch context (sourced from canonical commercial truth; no network,
# no secrets, no public fixed-price authority).
# ---------------------------------------------------------------------------

LAUNCH_STATUS = "PARTIAL"
ARTICLE_13_TARGET = 3      # validation target; never a guarantee or revenue claim

# The 4 pending founder actions (docs/WAVE17_FOUNDER_DAY1_LAUNCH_KIT.md).
FOUNDER_ACTIONS: list[tuple[str, str]] = [
    ("توقيع اتفاقية معالجة البيانات (DPA)", "Sign the Data Processing Agreement (DPA)"),
    ("إرسال 5 رسائل واتساب دافئة + تسجيلها", "Send 5 warm-intro WhatsApp messages + log them"),
    ("ضبط سجلات DNS (SPF/DKIM/DMARC) على dealix.me", "Set DNS records (SPF/DKIM/DMARC) at dealix.me"),
    ("دمج PR الانحدار المعلّق", "Merge the pending regression PR"),
]

# Compatibility name retained for the renderer/tests. This is the canonical
# launch path, not a catalogue of public tiers or fixed prices.
OFFER_LADDER: list[tuple[str, str]] = [
    ("التشخيص المصغّر المجاني / Free Mini Diagnostic", "دخول مجاني · evidence + problem qualification"),
    ("اكتشاف مؤهل / Qualified Discovery", "تأكيد المشكلة والمالك والبيانات وخط الأساس"),
    ("عرض خاص بالعميل / Customer-Specific Quote", "سلطة السعر الوحيدة · بعد discovery · لا سعر عام ثابت"),
    ("Revenue Command Pilot", "30 يومًا · governed delivery · quote-only"),
    ("دفع مثبت ثم تسليم / Verified Payment → Delivery", "Invoice ≠ Payment · يبدأ المدفوع فقط بعد دليل الدفع"),
    ("Proof Review", "Customer-validated proof → Stop / Expand / Redesign"),
]

OPEN_STATUSES = ("needs_review", "replied", "discovery_booked", "proposal_sent", "negotiating")
CLOSED_STATUSES = ("won", "lost")

STAGE_LABELS: dict[str, str] = {
    "needs_review": "بحاجة مراجعة / Needs review",
    "replied": "رد / Replied",
    "discovery_booked": "اجتماع مجدول / Discovery booked",
    "proposal_sent": "عرض مُرسل / Proposal sent",
    "negotiating": "تفاوض / Negotiating",
    "won": "صفقة / Won",
    "lost": "خسارة / Lost",
}


# ---------------------------------------------------------------------------
# CRM reading — all with graceful fallbacks.
# ---------------------------------------------------------------------------

def read_crm(path: Path) -> list[dict[str, str]]:
    """Read the CRM pipeline CSV, tolerating a UTF-8 BOM and missing file."""
    if not path.exists():
        return []
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            clean = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if not clean.get("company"):
                continue
            clean["status"] = clean.get("status", "").lower()
            rows.append(clean)
    return rows


def _to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _payment_verified(row: dict[str, str]) -> bool:
    """Count cash only when status and external payment evidence are both explicit."""
    status = (row.get("payment_status") or "").strip().lower()
    evidence = (
        row.get("payment_evidence_id")
        or row.get("payment_evidence")
        or row.get("payment_receipt")
        or ""
    ).strip()
    return status in {"verified", "paid", "settled"} and bool(evidence)


def crm_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    """Aggregate CRM stages without promoting won deals into verified payment."""
    by_stage: dict[str, dict[str, float]] = {}
    pipeline_value = 0.0
    weighted_value = 0.0
    won = 0
    paid = 0
    for row in rows:
        status = row.get("status") or "needs_review"
        bucket = by_stage.setdefault(status, {"count": 0, "value": 0.0})
        bucket["count"] += 1
        value = _to_float(row.get("deal_value_sar", ""))
        bucket["value"] += value
        if status not in CLOSED_STATUSES:
            pipeline_value += value
            weighted_value += value * (_to_float(row.get("probability", "")) / 100.0)
        if status == "won":
            won += 1
        if _payment_verified(row):
            paid += 1
    return {
        "by_stage": by_stage,
        "pipeline_value": round(pipeline_value),
        "weighted_value": round(weighted_value),
        "won": won,
        "paid": paid,
        "total": len(rows),
    }


def followups_due(rows: list[dict[str, str]], today: str) -> list[dict[str, str]]:
    """Open CRM rows whose next_followup_date is today or earlier."""
    due: list[dict[str, str]] = []
    for row in rows:
        if row.get("status") in CLOSED_STATUSES:
            continue
        when = row.get("next_followup_date", "").strip()
        if when and when <= today:
            due.append(row)
    due.sort(key=lambda r: r.get("next_followup_date", ""))
    return due


def priority_actions(rows: list[dict[str, str]], limit: int = 3) -> list[dict[str, str]]:
    """Top open CRM rows by weighted value — the founder's revenue focus today."""
    open_rows = [r for r in rows if r.get("status") in OPEN_STATUSES]
    open_rows.sort(
        key=lambda r: _to_float(r.get("deal_value_sar", "")) * (_to_float(r.get("probability", "")) / 100.0),
        reverse=True,
    )
    return open_rows[:limit]


# ---------------------------------------------------------------------------
# HTML section renderers.
# ---------------------------------------------------------------------------

def _readiness_banner(crm: dict[str, object]) -> str:
    paid = int(crm["paid"])  # type: ignore[arg-type]
    ok = LAUNCH_STATUS == "READY"
    color = PRIMARY if ok else ACCENT
    label = "جاهز للإطلاق / Launch ready" if ok else "جاهزية جزئية / Partial readiness"
    return (
        f'<div class="banner" style="border-color:{color}">'
        f'<span class="badge" style="background:{color}">{html.escape(label)}</span>'
        f'<span class="banner-text">عملاء مدفوعون نحو البوابة التجارية (Article 13): '
        f'<b>{paid}/{ARTICLE_13_TARGET}</b> · Paid customers toward commercial gate</span>'
        "</div>"
    )


def _actions_list(actions: list[dict[str, str]]) -> str:
    if not actions:
        return '<p class="muted">لا توجد إجراءات إيرادية مفتوحة بعد. / No open revenue actions yet.</p>'
    out: list[str] = ['<ol class="actions">']
    for row in actions:
        company = html.escape(row.get("company", "—"))
        action = html.escape(row.get("next_action", "review"))
        offer = html.escape(row.get("offer", ""))
        value = _to_float(row.get("deal_value_sar", ""))
        meta = f"{offer} · {value:,.0f} SAR" if value else offer
        out.append(f'<li><b>{company}</b> — {action}<span class="meta">{meta}</span></li>')
    out.append("</ol>")
    return "\n".join(out)


def _stage_rows(by_stage: dict[str, dict[str, float]]) -> str:
    if not by_stage:
        return '<tr><td colspan="3" class="muted">لا توجد بيانات بعد / No data yet</td></tr>'
    out: list[str] = []
    order = list(STAGE_LABELS.keys())
    for status in sorted(by_stage, key=lambda s: order.index(s) if s in order else 99):
        bucket = by_stage[status]
        label = STAGE_LABELS.get(status, status)
        out.append(
            "<tr>"
            f"<td>{html.escape(label)}</td>"
            f"<td>{int(bucket['count'])}</td>"
            f"<td>{bucket['value']:,.0f} SAR</td>"
            "</tr>"
        )
    return "\n".join(out)


def _followup_rows(due: list[dict[str, str]]) -> str:
    if not due:
        return '<tr><td colspan="3" class="muted">لا متابعات مستحقة اليوم / No follow-ups due</td></tr>'
    out: list[str] = []
    for row in due[:15]:
        out.append(
            "<tr>"
            f"<td>{html.escape(row.get('company', '—'))}</td>"
            f"<td>{html.escape(STAGE_LABELS.get(row.get('status', ''), row.get('status', '')))}</td>"
            f"<td>{html.escape(row.get('next_followup_date', ''))}</td>"
            "</tr>"
        )
    return "\n".join(out)


def _offer_rows() -> str:
    out: list[str] = []
    for i, (name, detail) in enumerate(OFFER_LADDER, 1):
        out.append(
            '<div class="ladder-row">'
            f'<span class="rung">{i}</span>'
            f'<span class="rung-name">{html.escape(name)}</span>'
            f'<span class="rung-detail">{html.escape(detail)}</span>'
            "</div>"
        )
    return "\n".join(out)


def _founder_actions() -> str:
    out: list[str] = ['<ol class="actions">']
    for ar, en in FOUNDER_ACTIONS:
        out.append(f'<li><b>{html.escape(ar)}</b><span class="meta">{html.escape(en)}</span></li>')
    out.append("</ol>")
    return "\n".join(out)


def render_html(
    kpis: dict[str, object],
    crm: dict[str, object],
    actions: list[dict[str, str]],
    due: list[dict[str, str]],
    source_note: str,
) -> str:
    today = date.today().isoformat()
    by_sector = kpis["by_sector"]  # type: ignore[assignment]
    funnel = kpis["funnel"]  # type: ignore[assignment]

    cards = "\n".join([
        _kpi_card("مسودات جاهزة / Ready drafts", kpis["ready_drafts"], ACCENT),
        _kpi_card("قيمة خط الأنابيب / Pipeline", f"{crm['pipeline_value']:,} SAR", PRIMARY),
        _kpi_card("قيمة مرجّحة / Weighted", f"{crm['weighted_value']:,} SAR", ACCENT),
        _kpi_card("سجلات CRM / CRM rows", crm["total"], PRIMARY),
        _kpi_card("ردود / Replies", kpis["replies"], ACCENT),
        _kpi_card("اجتماعات / Meetings", kpis["meetings"], ACCENT),
        _kpi_card("صفقات / Won", crm["won"], PRIMARY),
        _kpi_card("نسبة الرد / Reply rate", f"{kpis['reply_rate']}%", ACCENT),
    ])

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dealix — غرفة القيادة الموحّدة / Unified Command Room</title>
<style>
  :root {{ --primary: {PRIMARY}; --accent: {ACCENT}; --dark: {DARK}; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: "Tajawal", "Noto Kufi Arabic", "Segoe UI", system-ui, sans-serif;
          background: var(--dark); color: #f4f6f4; line-height: 1.6; }}
  header {{ background: linear-gradient(135deg, var(--primary), var(--dark));
            border-bottom: 3px solid var(--accent); padding: 28px 20px; }}
  header h1 {{ margin: 0; font-size: 1.6rem; }}
  header .sub {{ color: var(--accent); margin-top: 6px; font-size: .95rem; }}
  main {{ max-width: 1040px; margin: 0 auto; padding: 20px; }}
  .banner {{ display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
             background: #11331f; border: 1px solid var(--accent); border-radius: 14px;
             padding: 14px 18px; margin-bottom: 22px; }}
  .badge {{ color: #0D2818; font-weight: 800; padding: 4px 12px; border-radius: 999px; font-size: .85rem; }}
  .banner-text {{ font-size: .9rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
           gap: 14px; margin-bottom: 28px; }}
  .card {{ background: #11331f; border: 1px solid rgba(201,169,76,.25); border-radius: 14px;
           padding: 18px; text-align: center; }}
  .kpi {{ font-size: 1.9rem; font-weight: 800; }}
  .kpi-label {{ font-size: .82rem; color: #b9c7bd; margin-top: 4px; }}
  .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }}
  section {{ background: #11331f; border: 1px solid rgba(201,169,76,.18); border-radius: 14px;
            padding: 20px; margin-bottom: 22px; }}
  section h2 {{ margin: 0 0 16px; font-size: 1.12rem; color: var(--accent);
               border-bottom: 1px solid rgba(201,169,76,.2); padding-bottom: 8px; }}
  .funnel-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
  .funnel-name {{ flex: 0 0 38%; font-size: .9rem; }}
  .funnel-bar {{ flex: 1; background: rgba(255,255,255,.08); border-radius: 8px; height: 18px; overflow: hidden; }}
  .funnel-fill {{ display: block; height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); }}
  .funnel-count {{ flex: 0 0 36px; text-align: left; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 8px; text-align: right; border-bottom: 1px solid rgba(255,255,255,.07); font-size: .88rem; }}
  th {{ color: var(--accent); font-weight: 700; }}
  ol.actions {{ margin: 0; padding-inline-start: 20px; }}
  ol.actions li {{ margin-bottom: 10px; }}
  ol.actions .meta {{ display: block; color: #9fb3a4; font-size: .8rem; }}
  .ladder-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
                 border-bottom: 1px solid rgba(255,255,255,.06); padding-bottom: 8px; }}
  .rung {{ flex: 0 0 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%;
           background: var(--accent); color: #0D2818; font-weight: 800; font-size: .85rem; }}
  .rung-name {{ flex: 1; font-weight: 600; }}
  .rung-detail {{ color: #9fb3a4; font-size: .82rem; }}
  .muted {{ color: #8aa192; text-align: center; }}
  .note {{ background: rgba(201,169,76,.1); border: 1px solid rgba(201,169,76,.3);
           border-radius: 10px; padding: 12px 14px; font-size: .85rem; margin-bottom: 22px; }}
  footer {{ text-align: center; padding: 18px; color: #7e9486; font-size: .8rem; }}
  @media (max-width: 720px) {{ .cols {{ grid-template-columns: 1fr; }} header h1 {{ font-size: 1.3rem; }} }}
</style>
</head>
<body>
<header>
  <h1>غرفة القيادة الموحّدة — Dealix Unified Command Room</h1>
  <div class="sub">كل نواحي الإطلاق التجاري في لوحة واحدة · One view for the whole commercial launch · {today}</div>
</header>
<main>
  {_readiness_banner(crm)}
  <div class="note">المصدر / Source: {html.escape(source_note)} — للقراءة فقط، لا ترسل أي شيء. Read-only, sends nothing.</div>

  <div class="grid">
    {cards}
  </div>

  <div class="cols">
    <section>
      <h2>إجراءات اليوم ذات الأولوية / Today's priority actions</h2>
      {_actions_list(actions)}
    </section>
    <section>
      <h2>إجراءات الإطلاق العالقة / Pending launch actions</h2>
      {_founder_actions()}
    </section>
  </div>

  <section>
    <h2>القمع / Funnel</h2>
    {_funnel_rows(funnel)}
  </section>

  <div class="cols">
    <section>
      <h2>خط الأنابيب حسب المرحلة / Pipeline by stage</h2>
      <table>
        <thead><tr><th>المرحلة / Stage</th><th>عدد / Count</th><th>قيمة / Value</th></tr></thead>
        <tbody>{_stage_rows(crm["by_stage"])}</tbody>
      </table>
    </section>
    <section>
      <h2>متابعات مستحقة اليوم / Follow-ups due</h2>
      <table>
        <thead><tr><th>الشركة / Company</th><th>الحالة / Status</th><th>التاريخ / Date</th></tr></thead>
        <tbody>{_followup_rows(due)}</tbody>
      </table>
    </section>
  </div>

  <div class="cols">
    <section>
      <h2>حسب القطاع / By sector</h2>
      <table>
        <thead><tr><th>القطاع / Sector</th><th>إجمالي / Total</th><th>ردود / Replies</th><th>صفقات / Won</th></tr></thead>
        <tbody>{_sector_rows(by_sector)}</tbody>
      </table>
    </section>
    <section>
      <h2>المسار التجاري / Commercial path</h2>
      {_offer_rows()}
    </section>
  </div>
</main>
<footer>
  Dealix — Saudi-first AI Business Operating System · Revenue + Proof + Command.<br>
  كل المسودات تنتظر المراجعة؛ لا إرسال تلقائي ولا سعر عام ثابت.<br>
  Generated offline · {today}
</footer>
</body>
</html>
"""


def print_summary(kpis: dict[str, object], crm: dict[str, object], out_path: Path) -> None:
    print("غرفة القيادة الموحّدة — Dealix Unified Command Room")
    print(f"  جاهزية الإطلاق:       {LAUNCH_STATUS}")
    print(f"  عملاء مدفوعون:        {crm['paid']}/{ARTICLE_13_TARGET}")
    print(f"  مسودات جاهزة:         {kpis['ready_drafts']}")
    print(f"  سجلات CRM:            {crm['total']}")
    print(f"  قيمة خط الأنابيب:     {crm['pipeline_value']:,} SAR")
    print(f"  قيمة مرجّحة:          {crm['weighted_value']:,} SAR")
    print(f"  ردود:                 {kpis['replies']}")
    print(f"  نسبة الرد:            {kpis['reply_rate']}%")
    print(f"  اللوحة: {out_path}")


def build(log: Path, crm_path: Path, out: Path, write: bool = True) -> str:
    """Build the unified command room HTML. Returns the rendered string."""
    today = date.today().isoformat()
    log_path, used_template = resolve_log(log)
    rows = read_log(log_path)
    drafts_dir = latest_drafts_dir()
    ready = count_ready_drafts(drafts_dir)
    kpis = compute_kpis(rows, ready)

    crm_rows = read_crm(crm_path)
    crm = crm_summary(crm_rows)
    actions = priority_actions(crm_rows)
    due = followups_due(crm_rows, today)

    source_note = f"{log_path.name}" + (" (template)" if used_template else "") + f" + {crm_path.name}"
    html_doc = render_html(kpis, crm, actions, due, source_note)

    if write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_doc, encoding="utf-8")
        print_summary(kpis, crm, out)
    return html_doc


def main() -> int:
    ap = argparse.ArgumentParser(description="Dealix Unified Command Room — offline founder dashboard")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG, help="Path to the outreach log CSV")
    ap.add_argument("--crm", type=Path, default=CRM_PIPELINE, help="Path to the CRM pipeline CSV")
    ap.add_argument("--out", type=Path, default=OUT_HTML, help="Output HTML path")
    ap.add_argument("--dry-run", action="store_true", help="Compute and print KPIs without writing HTML")
    args = ap.parse_args()

    if args.dry_run:
        log_path, used_template = resolve_log(args.log)
        if used_template:
            print(f"[تنبيه] لا يوجد سجل حقيقي ({args.log}) — استخدمت القالب: {log_path}")
        rows = read_log(log_path)
        kpis = compute_kpis(rows, count_ready_drafts(latest_drafts_dir()))
        crm = crm_summary(read_crm(args.crm))
        print("[dry-run] لن تُكتب اللوحة. ملخص المؤشرات:")
        print_summary(kpis, crm, args.out)
        return 0

    build(args.log, args.crm, args.out, write=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())