"""Evidence-first founder market-entry readiness for Dealix.

This module does not send, publish, charge, deploy, or mutate customer data. It
projects repository and founder-supplied evidence into the highest safe launch
stage and reviewable operating-board exports.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

import yaml

from auto_client_acquisition.finance_os.pricing_catalog import get_pricing_tier

STAGE_ORDER = (
    "blocked",
    "evidence_required",
    "private_pilot_ready",
    "limited_launch_ready",
    "scale_ready",
)

STAGE_LABELS_AR = {
    "blocked": "متوقف — خرق سلامة أو حوكمة",
    "evidence_required": "الأدلة غير كافية",
    "private_pilot_ready": "جاهز لتجربة خاصة دافئة",
    "limited_launch_ready": "جاهز لإطلاق محدود",
    "scale_ready": "جاهز للتوسع المنضبط",
}


@dataclass(frozen=True)
class GateResult:
    gate_id: str
    stage: str
    category: str
    ok: bool
    evidence: str
    reason_ar: str
    remediation_ar: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_market_entry_signals(path: str | Path) -> dict[str, Any]:
    """Load a founder-maintained signal snapshot without inferring evidence."""
    source = Path(path)
    payload = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    if str(payload.get("schema_version")) != "1.0":
        raise ValueError("market entry signals require schema_version 1.0")
    if not isinstance(payload.get("signals", {}), dict):
        raise ValueError("signals must be a mapping")
    if not isinstance(payload.get("metrics", {}), dict):
        raise ValueError("metrics must be a mapping")
    payload["_source_path"] = str(source)
    return payload


def _evidence_ref(row: dict[str, Any]) -> str:
    return str(row.get("evidence_ref") or "").strip()


def _observed_at(row: dict[str, Any]) -> str:
    value = str(row.get("observed_at") or "").strip()
    if not value:
        return ""
    try:
        observed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if observed.tzinfo is None:
        return ""
    return observed.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _signal(payload: dict[str, Any], key: str) -> tuple[str, str]:
    row = (payload.get("signals") or {}).get(key) or {}
    status = str(row.get("status") or "unknown").strip().lower()
    if status not in {"pass", "fail", "unknown"}:
        status = "unknown"
    evidence = _evidence_ref(row)
    if status in {"pass", "fail"} and (not evidence or not _observed_at(row)):
        return "unknown", "missing timestamp or evidence reference"
    return status, evidence


def _metric(payload: dict[str, Any], key: str) -> tuple[float | None, str]:
    row = (payload.get("metrics") or {}).get(key) or {}
    evidence = _evidence_ref(row)
    if not evidence or not _observed_at(row):
        return None, "missing timestamp or evidence reference"
    try:
        value = float(row.get("value"))
    except (TypeError, ValueError):
        return None, "invalid numeric value"
    if value < 0:
        return None, "negative metrics are not accepted"
    return value, evidence


def _repo_gate(
    gate_id: str,
    stage: str,
    category: str,
    ok: bool,
    evidence: str,
    reason_ar: str,
    remediation_ar: str,
) -> GateResult:
    return GateResult(
        gate_id=gate_id,
        stage=stage,
        category=category,
        ok=ok,
        evidence=evidence,
        reason_ar=reason_ar,
        remediation_ar=remediation_ar,
    )


def _signal_gate(
    payload: dict[str, Any],
    *,
    key: str,
    stage: str,
    category: str,
    reason_ar: str,
    remediation_ar: str,
) -> GateResult:
    status, evidence = _signal(payload, key)
    return _repo_gate(
        key,
        stage,
        category,
        status == "pass",
        evidence,
        reason_ar if status != "pass" else "متحقق بدليل مؤرخ.",
        remediation_ar,
    )


def _metric_gate(
    payload: dict[str, Any],
    *,
    key: str,
    threshold: float,
    stage: str,
    category: str,
    label_ar: str,
) -> GateResult:
    value, evidence = _metric(payload, key)
    ok = value is not None and value >= threshold
    shown = "غير موثق" if value is None else f"{value:g}"
    return _repo_gate(
        key,
        stage,
        category,
        ok,
        evidence,
        f"{label_ar}: {shown}؛ المطلوب ≥ {threshold:g}.",
        f"وثّق {label_ar} بمصدر وتاريخ، ثم ارفع القيمة إلى {threshold:g} على الأقل.",
    )


def _metric_max_gate(
    payload: dict[str, Any],
    *,
    key: str,
    threshold: float,
    stage: str,
    category: str,
    label_ar: str,
) -> GateResult:
    value, evidence = _metric(payload, key)
    ok = value is not None and value <= threshold
    shown = "غير موثق" if value is None else f"{value:g}"
    return _repo_gate(
        key,
        stage,
        category,
        ok,
        evidence,
        f"{label_ar}: {shown}؛ المطلوب ≤ {threshold:g}.",
        f"وثّق {label_ar} بمصدر وتاريخ، ثم اخفض القيمة إلى {threshold:g} أو أقل.",
    )


def audit_pilot_pricing(repo_root: Path | None = None) -> dict[str, Any]:
    """Audit the founder-governed launch offer without promoting legacy pricing."""
    root = repo_root or _repo_root()
    offer_gate_path = root / "dealix/config/first_launch_offer_gate.yaml"
    offer_gate = yaml.safe_load(offer_gate_path.read_text(encoding="utf-8")) or {}
    primary = offer_gate.get("primary_motion") or {}
    pricing = offer_gate.get("pricing_experiment") or {}

    tier = get_pricing_tier("revenue_command_pilot_30d")
    product_catalog = yaml.safe_load(
        (root / "data/commercial/product_catalog.yaml").read_text(encoding="utf-8")
    )
    pricing_rules = yaml.safe_load(
        (root / "data/commercial/pricing_rules.yaml").read_text(encoding="utf-8")
    )
    product = next(
        item
        for item in product_catalog["offers"]
        if item["id"] == "revenue_command_pilot_30d"
    )
    price_range = pricing_rules["base_ranges"]["revenue_command_pilot_30d"]
    quote_only_sources = {
        "finance_catalog": {
            "pricing_basis": tier["pricing_basis"],
            "price_sar": tier["price_sar"],
        },
        "product_catalog": {
            "type": product["type"],
            "setup_sar": product["setup_sar"],
        },
        "pricing_rules": {
            "status": price_range["status"],
            "min": price_range["min"],
            "max": price_range["max"],
        },
    }

    raw_amount = pricing.get("public_amount_sar")
    try:
        approved_amount = float(raw_amount) if raw_amount is not None else None
    except (TypeError, ValueError):
        approved_amount = None
    pricing_status = str(pricing.get("status") or "unknown")
    publication_status = str(offer_gate.get("status") or "unknown")
    amount_state_ok = (
        approved_amount is not None
        and approved_amount > 0
        and pricing_status == "approved"
        and publication_status == "approved"
    ) if pricing_status == "approved" else raw_amount is None
    governance_ok = all(
        (
            bool(primary.get("id")),
            bool(primary.get("name_en")),
            primary.get("duration_days") is None,
            primary.get("duration_policy") == "customer_specific_after_qualified_discovery",
            primary.get("public") is False,
            primary.get("checkout_enabled") is False,
            primary.get("external_quote_requires_founder_approval") is True,
            str(pricing.get("currency") or "") == "SAR",
            amount_state_ok,
            tier["pricing_basis"] == "quote_only",
            tier["price_sar"] is None,
            product["type"] == "quote_only_after_discovery",
            product["setup_sar"] is None,
            price_range["status"] == "quote_only_after_discovery",
            price_range["min"] is None,
            price_range["max"] is None,
        )
    )

    return {
        "ok": governance_ok,
        "currency": "SAR",
        "offer_id": primary.get("id"),
        "offer_name": primary.get("name_en"),
        "offer_name_ar": primary.get("name_ar"),
        "duration_days": primary.get("duration_days"),
        "duration_policy": primary.get("duration_policy"),
        "pilot_price": approved_amount if pricing_status == "approved" else None,
        "observed": quote_only_sources,
        "quote_only_sources_consistent": True,
        "legacy_offer_public": False,
        "sources": [
            "dealix/config/first_launch_offer_gate.yaml",
            "auto_client_acquisition/finance_os/pricing_catalog.py",
            "data/commercial/product_catalog.yaml",
            "data/commercial/pricing_rules.yaml",
        ],
        "publication_status": publication_status,
        "pricing_status": pricing_status,
        "decision_issue": offer_gate.get("decision_issue"),
    }


def build_market_entry_snapshot(
    payload: dict[str, Any], *, repo_root: Path | None = None
) -> dict[str, Any]:
    """Return the highest safe stage with exact blockers and next actions."""
    root = repo_root or _repo_root()
    pricing = audit_pilot_pricing(root)
    gates: list[GateResult] = [
        _repo_gate(
            "pilot_pricing_integrity",
            "private_pilot_ready",
            "offer",
            bool(pricing["ok"]),
            ", ".join(pricing["sources"]),
            (
                "سعر التجربة متسق عبر المصادر الكانونية."
                if pricing["ok"]
                else "يوجد تضارب في سعر التجربة."
            ),
            "وحّد السعر في المصادر الكانونية ولا تنشر رقمًا قبل موافقة المؤسس.",
        ),
        _repo_gate(
            "pilot_delivery_contract_present",
            "private_pilot_ready",
            "delivery",
            (root / "dealix/commercial/pilot_delivery.py").is_file(),
            "dealix/commercial/pilot_delivery.py",
            "عقد تسليم التجربة موجود في المستودع.",
            "استعد عقد تسليم تجريبي واحد واختبر مخرجاته.",
        ),
        _repo_gate(
            "approval_contract_present",
            "private_pilot_ready",
            "governance",
            (root / "dealix/commercial_universe_approval.py").is_file(),
            "dealix/commercial_universe_approval.py",
            "عقد الموافقة موجود في المستودع.",
            "اربط كل مسودة خارجية بموافقة بشرية صريحة.",
        ),
        _signal_gate(
            payload,
            key="founder_offer_approved",
            stage="private_pilot_ready",
            category="offer",
            reason_ar="عرض الدخول الأول لم يعتمد بعد.",
            remediation_ar="اعتمد عرضًا واحدًا فقط ونطاقه وسعره قبل عرضه.",
        ),
        _signal_gate(
            payload,
            key="pilot_delivery_dry_run",
            stage="private_pilot_ready",
            category="delivery",
            reason_ar="لا يوجد تسليم جاف كامل موثق.",
            remediation_ar="نفّذ التسليم من intake إلى Proof Pack على بيانات تجريبية.",
        ),
        _signal_gate(
            payload,
            key="approval_queue_dry_run",
            stage="private_pilot_ready",
            category="governance",
            reason_ar="مسار الموافقة لم يُثبت من البداية للنهاية.",
            remediation_ar="اختبر إنشاء المسودة ثم الموافقة/الرفض دون إرسال خارجي.",
        ),
        _signal_gate(
            payload,
            key="external_execution_default_off",
            stage="private_pilot_ready",
            category="safety",
            reason_ar="تعطيل التنفيذ الخارجي افتراضيًا غير مثبت.",
            remediation_ar="أثبت أن الإرسال والنشر والدفع والإنتاج مغلقة افتراضيًا.",
        ),
        _signal_gate(
            payload,
            key="pdpl_intake_reviewed",
            stage="private_pilot_ready",
            category="compliance",
            reason_ar="نموذج جمع بيانات العميل لم يراجع من منظور PDPL.",
            remediation_ar="راجع الحد الأدنى للبيانات والغرض والاحتفاظ والحذف والموافقة.",
        ),
        _metric_gate(
            payload,
            key="warm_permissioned_accounts",
            threshold=5,
            stage="private_pilot_ready",
            category="pipeline",
            label_ar="حسابات دافئة ومسموح بالتواصل معها",
        ),
        _signal_gate(
            payload,
            key="production_health",
            stage="limited_launch_ready",
            category="production",
            reason_ar="صحة الإنتاج غير مثبتة أو فاشلة.",
            remediation_ar="أثبت /health مرتين وسجل deployment ID دون أسرار.",
        ),
        _signal_gate(
            payload,
            key="ci_required_checks_green",
            stage="limited_launch_ready",
            category="production",
            reason_ar="فحوص الدمج المطلوبة ليست خضراء بالكامل.",
            remediation_ar="أصلح السبب الجذري ثم أعد الفحوص المطلوبة.",
        ),
        _signal_gate(
            payload,
            key="production_secrets_rotated",
            stage="limited_launch_ready",
            category="security",
            reason_ar="تدوير أسرار الإنتاج غير مثبت.",
            remediation_ar="دوّر الأسرار داخل المنصة وسجل الأسماء والحالة فقط.",
        ),
        _signal_gate(
            payload,
            key="payment_path_approved",
            stage="limited_launch_ready",
            category="billing",
            reason_ar="مسار التحصيل الحقيقي لم يعتمد.",
            remediation_ar="اعتمد العقد والفاتورة والاسترداد والـwebhook قبل أول تحصيل حي.",
        ),
        _signal_gate(
            payload,
            key="pilot_contract_and_dpa_approved",
            stage="limited_launch_ready",
            category="legal",
            reason_ar="عقد Pilot وحدود معالجة البيانات لم يعتمدا.",
            remediation_ar="اعتمد SOW وDPA ونطاق المسؤولية والإنهاء قبل فتح الإطلاق المحدود.",
        ),
        _signal_gate(
            payload,
            key="incident_and_refund_runbook_verified",
            stage="limited_launch_ready",
            category="operations",
            reason_ar="مسار الحوادث والشكاوى والاسترداد لم يُختبر.",
            remediation_ar="نفّذ تمرينًا جافًا لحادث وطلب استرداد وسجّل زمن الاستجابة.",
        ),
        _metric_gate(
            payload,
            key="paid_pilots_completed",
            threshold=3,
            stage="limited_launch_ready",
            category="proof",
            label_ar="تجارب مدفوعة مكتملة",
        ),
        _metric_gate(
            payload,
            key="signed_proof_packs",
            threshold=3,
            stage="limited_launch_ready",
            category="proof",
            label_ar="حزم إثبات موقعة",
        ),
        _metric_gate(
            payload,
            key="consented_case_studies",
            threshold=1,
            stage="limited_launch_ready",
            category="proof",
            label_ar="دراسات حالة بموافقة نشر",
        ),
        _metric_gate(
            payload,
            key="gross_margin_samples",
            threshold=3,
            stage="limited_launch_ready",
            category="economics",
            label_ar="عينات هامش Pilot موثقة",
        ),
        _metric_gate(
            payload,
            key="pilot_gross_margin_rate",
            threshold=0.55,
            stage="limited_launch_ready",
            category="economics",
            label_ar="هامش Pilot الإجمالي بعد وقت المؤسس والتكلفة المتغيرة",
        ),
        _metric_gate(
            payload,
            key="delivery_capacity_per_month",
            threshold=3,
            stage="limited_launch_ready",
            category="capacity",
            label_ar="سعة Pilots الشهرية دون خفض الجودة",
        ),
        _metric_gate(
            payload,
            key="paid_pilots_completed",
            threshold=5,
            stage="scale_ready",
            category="proof",
            label_ar="تجارب مدفوعة مكتملة",
        ),
        _metric_gate(
            payload,
            key="active_retainer_customers",
            threshold=3,
            stage="scale_ready",
            category="retention",
            label_ar="عملاء Retainer نشطون",
        ),
        _metric_gate(
            payload,
            key="on_time_delivery_samples",
            threshold=5,
            stage="scale_ready",
            category="delivery",
            label_ar="عينات تسليم مكتملة بقياس الوقت",
        ),
        _metric_gate(
            payload,
            key="on_time_delivery_rate",
            threshold=0.9,
            stage="scale_ready",
            category="delivery",
            label_ar="نسبة التسليم في الوقت",
        ),
        _metric_max_gate(
            payload,
            key="median_time_to_first_value_days",
            threshold=7,
            stage="scale_ready",
            category="value",
            label_ar="الوسيط الزمني لأول قيمة بالأيام",
        ),
        _metric_gate(
            payload,
            key="retainer_renewal_samples",
            threshold=3,
            stage="scale_ready",
            category="retention",
            label_ar="قرارات تجديد Retainer موثقة",
        ),
        _metric_gate(
            payload,
            key="retainer_renewal_rate",
            threshold=0.7,
            stage="scale_ready",
            category="retention",
            label_ar="نسبة تجديد Retainer",
        ),
        _metric_gate(
            payload,
            key="cac_samples",
            threshold=5,
            stage="scale_ready",
            category="economics",
            label_ar="عينات تكلفة اكتساب عميل شاملة وقت المؤسس",
        ),
        _metric_max_gate(
            payload,
            key="cac_payback_months",
            threshold=3,
            stage="scale_ready",
            category="economics",
            label_ar="مدة استرداد تكلفة الاكتساب بالشهور",
        ),
    ]

    external_status, external_evidence = _signal(payload, "external_execution_default_off")
    if external_status == "fail":
        stage = "blocked"
        safety_blocker = asdict(
            _repo_gate(
                "external_execution_default_off",
                "blocked",
                "safety",
                False,
                external_evidence,
                "التنفيذ الخارجي ليس مغلقًا افتراضيًا.",
                "أوقف التنفيذ الخارجي افتراضيًا ووثّق الاختبار قبل أي استئناف.",
            )
        )
    else:
        safety_blocker = None
        stage = "evidence_required"
        for candidate in (
            "private_pilot_ready",
            "limited_launch_ready",
            "scale_ready",
        ):
            required = [
                g
                for g in gates
                if STAGE_ORDER.index(g.stage) <= STAGE_ORDER.index(candidate)
                and g.stage != "blocked"
            ]
            if required and all(g.ok for g in required):
                stage = candidate
            else:
                break

    blockers = [asdict(g) for g in gates if not g.ok]
    current_stage_blockers = [
        row
        for row in blockers
        if STAGE_ORDER.index(row["stage"])
        <= min(STAGE_ORDER.index(stage) + 1, STAGE_ORDER.index("scale_ready"))
    ]
    if safety_blocker:
        current_stage_blockers.insert(0, safety_blocker)

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "input_as_of": payload.get("as_of"),
        "input_source": payload.get("_source_path"),
        "stage": stage,
        "stage_label_ar": STAGE_LABELS_AR[stage],
        "external_actions_executed": 0,
        "public_claims_authorized": stage in {"limited_launch_ready", "scale_ready"},
        "scale_authorized": stage == "scale_ready",
        "pricing_audit": pricing,
        "gates": [asdict(g) for g in gates],
        "blockers": blockers,
        "next_stage_blockers": current_stage_blockers,
        "highest_safe_action_ar": _highest_safe_action(stage),
        "operating_plan": _operating_plan(stage),
    }


def _highest_safe_action(stage: str) -> str:
    return {
        "blocked": "أوقف أي إجراء خارجي وأعد تفعيل الحوكمة قبل أي عمل تجاري.",
        "evidence_required": "أكمل الأدلة والاختبارات داخليًا؛ لا تعلن جاهزية سوقية.",
        "private_pilot_ready": "ابدأ بخمسة حسابات دافئة وتجربة خاصة واحدة بموافقة لكل خطوة.",
        "limited_launch_ready": "افتح إطلاقًا محدودًا بسعة معلنة وقياس أسبوعي، دون توسع مدفوع واسع.",
        "scale_ready": "وسّع القناة الأفضل تدريجيًا مع مراقبة الهامش والجودة والاحتفاظ.",
    }[stage]


def _operating_plan(stage: str) -> dict[str, list[dict[str, str]]]:
    return {
        "days_1_14": [
            {
                "days": "1-2",
                "focus_ar": "الثقة والعرض",
                "exit_ar": "صحة موثقة + عرض واحد معتمد + سعر متسق",
            },
            {
                "days": "3-4",
                "focus_ar": "قائمة دافئة",
                "exit_ar": "5 حسابات بمصدر وسبب تواصل وموافقة قناة",
            },
            {
                "days": "5-7",
                "focus_ar": "تشخيص",
                "exit_ar": "مشكلة واحدة قابلة للقياس ونطاق Pilot موقع",
            },
            {
                "days": "8-14",
                "focus_ar": "تسليم وإثبات",
                "exit_ar": "Proof Pack من نتيجة منسوبة، لا من مسودة",
            },
        ],
        "days_15_30": [
            {"focus_ar": "ثلاث تجارب مدفوعة", "exit_ar": "3 فواتير مؤكدة + 3 حزم إثبات موقعة"},
            {"focus_ar": "تثبيت التشغيل", "exit_ar": "زمن تسليم وتكلفة وهامش مقاسان لكل تجربة"},
        ],
        "days_31_60": [
            {
                "focus_ar": "تحويل أفضل عميل إلى Retainer",
                "exit_ar": "استخدام متكرر وقيمة شهرية مثبتة",
            },
            {"focus_ar": "دراسة حالة", "exit_ar": "موافقة نشر صريحة ومقاييس قبل/بعد منسوبة"},
        ],
        "days_61_90": [
            {"focus_ar": "اختيار قناة التوسع", "exit_ar": "قناة واحدة تتفوق ببيانات اكتساب وتحويل"},
            {"focus_ar": "توسيع السعة", "exit_ar": "3 Retainers + هامش وتسليم ضمن الحدود"},
        ],
        "stage_at_generation": [{"stage": stage, "label_ar": STAGE_LABELS_AR[stage]}],
    }


def _write_csv(path: Path, headers: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_market_entry_artifacts(snapshot: dict[str, Any], output_dir: str | Path) -> list[Path]:
    """Write a reviewable founder brief plus sheet-compatible operating boards."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    json_path = out / "market_entry_snapshot.json"
    json_path.write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    written.append(json_path)

    md_path = out / "founder_market_entry_brief_ar.md"
    md_path.write_text(_render_markdown(snapshot), encoding="utf-8")
    written.append(md_path)

    gates_path = out / "launch_gates.csv"
    _write_csv(
        gates_path,
        ["gate_id", "stage", "category", "ok", "evidence", "reason_ar", "remediation_ar"],
        snapshot["gates"],
    )
    written.append(gates_path)

    action_rows = [
        {
            "Action": row["remediation_ar"],
            "Owner": "Founder/assigned owner",
            "Status": "pending",
            "Risk Level": (
                "high" if row["category"] in {"safety", "security", "production"} else "medium"
            ),
            "Due Date": "",
            "Output": row["gate_id"],
            "Evidence Link": row["evidence"],
        }
        for row in snapshot["blockers"]
    ]
    action_path = out / "action_queue.csv"
    _write_csv(
        action_path,
        ["Action", "Owner", "Status", "Risk Level", "Due Date", "Output", "Evidence Link"],
        action_rows,
    )
    written.append(action_path)

    approval_rows = [
        {
            "Approval Item": "اعتماد عرض وسعر Pilot",
            "Type": "pricing_offer",
            "Status": (
                "pending" if not _gate_ok(snapshot, "founder_offer_approved") else "evidenced"
            ),
            "Risk": "commercial",
            "Decision": "approve/reject/request_changes",
            "Due Date": "",
            "Channel": "GitHub/Approval Center",
        },
        {
            "Approval Item": "فتح التحصيل الحقيقي",
            "Type": "payment",
            "Status": "pending" if not _gate_ok(snapshot, "payment_path_approved") else "evidenced",
            "Risk": "financial",
            "Decision": "approve/reject",
            "Due Date": "",
            "Channel": "Founder",
        },
        {
            "Approval Item": "نشر دراسة حالة",
            "Type": "publication",
            "Status": (
                "pending" if not _gate_ok(snapshot, "consented_case_studies") else "evidenced"
            ),
            "Risk": "privacy/reputation",
            "Decision": "approve/reject",
            "Due Date": "",
            "Channel": "Founder + customer",
        },
    ]
    approval_path = out / "approval_queue.csv"
    _write_csv(
        approval_path,
        ["Approval Item", "Type", "Status", "Risk", "Decision", "Due Date", "Channel"],
        approval_rows,
    )
    written.append(approval_path)

    strategy_path = out / "strategy_backlog.csv"
    _write_csv(
        strategy_path,
        [
            "Strategy",
            "Area",
            "Priority",
            "Status",
            "Autonomy Level",
            "Safe Next Step",
            "GitHub Link",
        ],
        [
            {
                "Strategy": "Private proof wedge",
                "Area": "Revenue",
                "Priority": 100,
                "Status": "active",
                "Autonomy Level": "L3",
                "Safe Next Step": snapshot["highest_safe_action_ar"],
                "GitHub Link": "",
            },
            {
                "Strategy": "Limited launch after proof",
                "Area": "GTM",
                "Priority": 70,
                "Status": "gated",
                "Autonomy Level": "L4",
                "Safe Next Step": "أغلق بوابات limited_launch_ready",
                "GitHub Link": "",
            },
            {
                "Strategy": "Scale after retention",
                "Area": "Scale",
                "Priority": 40,
                "Status": "gated",
                "Autonomy Level": "L4",
                "Safe Next Step": "لا توسع قبل scale_ready",
                "GitHub Link": "",
            },
        ],
    )
    written.append(strategy_path)

    empty_tables = {
        "opportunity_graph.csv": [
            "Company",
            "Segment",
            "Offer Match",
            "Score",
            "Reason",
            "Stage",
            "Source URL",
            "Next Action",
        ],
        "proof_ledger.csv": ["Proof Event", "Entity", "Evidence", "Source URL", "Risk", "Date"],
        "self_improvement.csv": [
            "Learning Event",
            "Area",
            "Failure Type",
            "Root Cause",
            "Improvement",
            "Autonomy Bucket",
            "Status",
        ],
        "contacts_radar.csv": [
            "Name",
            "Company",
            "Role",
            "Email",
            "Phone",
            "Source",
            "Status",
            "Notes",
        ],
    }
    for filename, headers in empty_tables.items():
        path = out / filename
        rows: list[dict[str, Any]] = []
        if filename == "self_improvement.csv":
            rows = [
                {
                    "Learning Event": row["gate_id"],
                    "Area": row["category"],
                    "Failure Type": "readiness_gap",
                    "Root Cause": row["reason_ar"],
                    "Improvement": row["remediation_ar"],
                    "Autonomy Bucket": "L3_internal",
                    "Status": "proposed",
                }
                for row in snapshot["blockers"]
            ]
        _write_csv(path, headers, rows)
        written.append(path)

    milestones_path = out / "90_day_milestones.csv"
    milestone_rows: list[dict[str, str]] = []
    for period, rows in snapshot["operating_plan"].items():
        if period == "stage_at_generation":
            continue
        for row in rows:
            milestone_rows.append(
                {
                    "Period": period,
                    "Days": row.get("days", ""),
                    "Focus": row["focus_ar"],
                    "Exit Evidence": row["exit_ar"],
                    "Status": "gated",
                }
            )
    _write_csv(
        milestones_path,
        ["Period", "Days", "Focus", "Exit Evidence", "Status"],
        milestone_rows,
    )
    written.append(milestones_path)

    slack_path = out / "slack_command_update.md"
    slack_path.write_text(
        "# Dealix Market Entry Command\n\n"
        f"- Stage: **{snapshot['stage_label_ar']}**\n"
        f"- Highest safe action: {snapshot['highest_safe_action_ar']}\n"
        f"- Open gates: {len(snapshot['blockers'])}\n"
        "- External actions executed: 0\n",
        encoding="utf-8",
    )
    written.append(slack_path)
    return written


def _gate_ok(snapshot: dict[str, Any], gate_id: str) -> bool:
    return any(row["gate_id"] == gate_id and row["ok"] for row in snapshot["gates"])


def _render_markdown(snapshot: dict[str, Any]) -> str:
    blockers = snapshot["next_stage_blockers"][:10]
    blocker_lines = (
        "\n".join(
            f"- **{row['gate_id']}**: {row['reason_ar']} — {row['remediation_ar']}"
            for row in blockers
        )
        or "- لا توجد بوابات ناقصة للمرحلة التالية."
    )
    pricing = snapshot["pricing_audit"]
    approved_price = pricing.get("pilot_price")
    price_label = "غير معتمد" if approved_price is None else f"{approved_price:g} SAR"
    offer_label = pricing.get("offer_name_ar") or pricing.get("offer_name") or "غير محدد"
    return f"""# قرار دخول Dealix للسوق — Founder Market Entry

## القرار الآن

**{snapshot['stage_label_ar']}** (`{snapshot['stage']}`)

أعلى إجراء آمن: {snapshot['highest_safe_action_ar']}

## قواعد الحقيقة

- التنفيذ الخارجي المنفذ: **{snapshot['external_actions_executed']}**
- السماح بادعاءات إطلاق عام: **{str(snapshot['public_claims_authorized']).lower()}**
- السماح بالتوسع: **{str(snapshot['scale_authorized']).lower()}**
- عرض الدخول المحكوم: **{offer_label}** (`{pricing.get('offer_id')}`)
- السعر العام المعتمد: **{price_label}**
- حالة العرض/السعر: **{pricing.get('publication_status')} / {pricing.get('pricing_status')}**
- أي عرض قصير بسعر ثابت سابق أصبح تراثيًا وغير معتمد للنشر أو الاقتباس أو Checkout.
- نشر السعر أو تغييره يحتاج موافقة المؤسس.

## أهم البوابات التالية

{blocker_lines}

## تسلسل السوق

1. Dealix على Dealix وإغلاق الثقة التشغيلية.
2. خمسة حسابات دافئة فقط مع مصدر وموافقة قناة.
3. تشخيص واحد ثم Pilot واحد بمشكلة قابلة للقياس.
4. لا Case Study دون نتيجة منسوبة وموافقة نشر.
5. لا إطلاق محدود قبل 3 Pilots مدفوعة و3 Proof Packs.
6. لا توسع قبل 3 Retainers وقياس الهامش والتسليم.

## ملاحظة

هذا التقرير بوابة قرار، لا شهادة نتائج تجارية. وجود الكود أو الاختبارات لا يُحوّل
المسودة إلى إيراد ولا الـPilot التجريبي إلى دراسة حالة.
"""
