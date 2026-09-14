"""Frozen KnowledgeSnapshot + relationship provenance attachments.

Attaches immutable, evidence-bound provenance to the EXISTING
approval_center / proof_ledger / case evidence contracts whenever a
customer operation produces an action draft, escalation,
approval-required state, or verified proof.

Reuse only: no new database, no parallel ledger. Proof events carry
provenance inside the existing ``payload`` dict under
``PROVENANCE_KEY``; approvals carry it in the backward-compatible
``ApprovalRequest.provenance`` field; case evidence uses plain ID
refs (snapshot/chunk/relationship URIs — never bodies).

Hard rules enforced here:
- Never persist raw prompt, raw tool args/results, secrets, customer
  message body, or unnecessary PII. Only IDs + source refs + as_of /
  current_only flags are stored. Excerpts/bodies are always dropped.
- Missing or stale current evidence => ASK/HOLD. Proof builders
  refuse (raise) instead of fabricating proof.
- Relationship refs prove relationship ONLY; they never grant channel
  consent (``grants_channel_consent`` is always False).
- Attachment creation never executes the approved action and never
  performs any external effect (pure data construction).
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

PROVENANCE_KEY = "customer_ops_provenance"
PROVENANCE_VERSION = 1

MAX_CHUNK_IDS = 20
MAX_SOURCE_TYPES = 10
MAX_RELATIONSHIP_REFS = 10
MAX_EVIDENCE_REFS = 20
MAX_ID_LEN = 128
MAX_URI_LEN = 256

# Key substrings that must never appear in a provenance attachment.
# Checked recursively on every attach path (fail-closed).
FORBIDDEN_KEY_SUBSTRINGS: tuple[str, ...] = (
    "prompt",
    "tool_arg",
    "tool_result",
    "tool_output",
    "message_text",
    "message_body",
    "message",
    "secret",
    "api_key",
    "apikey",
    "password",
    "passwd",
    "token",
    "bearer",
    "phone",
    "email",
    "national_id",
    "iban",
    "otp",
    "cvv",
    "credit_card",
    "excerpt",
    "body",
    "content",
    "transcript",
)

_SNAPSHOT_KEYS: tuple[str, ...] = (
    "snapshot_id",
    "retrieved_at",
    "as_of",
    "chunk_ids",
    "source_types",
    "current_only",
)


def _safe_str(value: Any, limit: int = MAX_ID_LEN) -> str:
    try:
        text = str(value)
    except Exception:
        return ""
    return text[:limit]


def _safe_uri(value: Any) -> str:
    """Keep only a bounded URI ref (scheme/id style); never a body."""
    return _safe_str(value, MAX_URI_LEN)


def assert_no_raw_payload(obj: Any, *, _path: str = "provenance") -> None:
    """Recursively reject forbidden raw-payload keys (fail-closed)."""
    if isinstance(obj, dict):
        for key, val in obj.items():
            lowered = str(key).lower()
            for bad in FORBIDDEN_KEY_SUBSTRINGS:
                if bad in lowered:
                    raise ValueError(f"provenance_forbidden_key:{_path}.{key}")
            assert_no_raw_payload(val, _path=f"{_path}.{key}")
    elif isinstance(obj, (list, tuple)):
        for idx, item in enumerate(obj):
            assert_no_raw_payload(item, _path=f"{_path}[{idx}]")


def build_snapshot_provenance(snapshot_ref: Mapping[str, Any] | None) -> dict[str, Any]:
    """Project a frozen snapshot ref onto the allowed provenance surface."""
    ref = dict(snapshot_ref or {})
    chunk_ids = ref.get("chunk_ids") or []
    source_types = ref.get("source_types") or []
    if not isinstance(chunk_ids, list):
        chunk_ids = list(chunk_ids)
    if not isinstance(source_types, list):
        source_types = list(source_types)
    return {
        "snapshot_id": _safe_str(ref.get("snapshot_id", "")),
        "retrieved_at": _safe_str(ref.get("retrieved_at", "")),
        "as_of": _safe_str(ref.get("as_of", "")),
        "chunk_ids": [_safe_str(c) for c in chunk_ids[:MAX_CHUNK_IDS] if str(c).strip()],
        "source_types": [_safe_str(s) for s in source_types[:MAX_SOURCE_TYPES] if str(s).strip()],
        "current_only": bool(ref.get("current_only", True)),
    }


def build_relationship_refs(evidence: list[Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    """Project independently-evidenced relationship refs (IDs only).

    Only sources in RELATIONSHIP_EVIDENCE_SOURCES qualify. Each ref
    carries ``grants_channel_consent=False`` explicitly: relationship
    evidence never mints channel consent.
    """
    from auto_client_acquisition.customer_ops.event_contract import (
        RELATIONSHIP_EVIDENCE_SOURCES,
    )

    refs: list[dict[str, Any]] = []
    for item in list(evidence or [])[:MAX_EVIDENCE_REFS]:
        if not isinstance(item, Mapping):
            continue
        source = str(item.get("source", ""))
        if source not in RELATIONSHIP_EVIDENCE_SOURCES:
            continue
        refs.append({
            "source": _safe_str(source),
            "uri_ref": _safe_uri(item.get("uri", "")),
            "evidence_level": _safe_str(item.get("evidence_level", "L0"), 8),
            "retrieved_at": _safe_str(item.get("retrieved_at", "")),
            "current_only": bool(item.get("current_only", True)),
            "proves_relationship": True,
            "grants_channel_consent": False,
        })
        if len(refs) >= MAX_RELATIONSHIP_REFS:
            break
    return refs


def build_evidence_refs(evidence: list[Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    """Sanitized knowledge-evidence refs (no excerpts, no bodies)."""
    refs: list[dict[str, Any]] = []
    for item in list(evidence or [])[:MAX_EVIDENCE_REFS]:
        if not isinstance(item, Mapping):
            continue
        refs.append({
            "source": _safe_str(item.get("source", "")),
            "uri_ref": _safe_uri(item.get("uri", "")),
            "evidence_level": _safe_str(item.get("evidence_level", "L0"), 8),
            "retrieved_at": _safe_str(item.get("retrieved_at", "")),
            "current_only": bool(item.get("current_only", True)),
        })
    return refs


def provenance_status_of(
    snapshot: Mapping[str, Any] | None,
    evidence: list[Mapping[str, Any]] | None,
) -> tuple[str, bool]:
    """Return (status, has_current_evidence).

    - ``missing``: no snapshot id, no chunk ids, or no evidence.
    - ``stale``: snapshot explicitly not current-only.
    - ``current``: frozen current-only snapshot with chunk ids + evidence.
    """
    snap = dict(snapshot or {})
    chunk_ids = [c for c in (snap.get("chunk_ids") or []) if str(c).strip()]
    has_evidence = bool(evidence)
    if not snap.get("snapshot_id") or not chunk_ids or not has_evidence:
        return "missing", False
    if snap.get("current_only") is not True:
        return "stale", False
    return "current", True


def build_provenance_attachment(
    *,
    snapshot_ref: Mapping[str, Any] | None,
    evidence: list[Mapping[str, Any]] | None,
    trace_id: str = "",
    case_id: str = "",
    response_state: str = "",
) -> dict[str, Any]:
    """Build the immutable sanitized attachment for one kernel outcome."""
    snapshot = build_snapshot_provenance(snapshot_ref)
    rel_refs = build_relationship_refs(evidence)
    ev_refs = build_evidence_refs(evidence)
    status, has_current = provenance_status_of(snapshot, ev_refs)
    attachment: dict[str, Any] = {
        "version": PROVENANCE_VERSION,
        "snapshot": snapshot,
        "evidence_refs": ev_refs,
        "relationship_refs": rel_refs,
        "trace_id": _safe_str(trace_id),
        "case_id": _safe_str(case_id),
        "response_state": _safe_str(response_state, 32),
        "provenance_status": status,
        "has_current_evidence": has_current,
    }
    assert_no_raw_payload(attachment)
    return attachment


def require_current_provenance(attachment: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed: verified proof requires current frozen evidence.

    Raises ValueError (caller maps to ASK/HOLD) when the snapshot is
    missing or stale — never fabricate proof.
    """
    att = dict(attachment or {})
    if att.get("has_current_evidence") is not True or att.get("provenance_status") != "current":
        raise ValueError("customer_provenance_missing_or_stale:ASK_OR_HOLD")
    snap = att.get("snapshot") or {}
    if not isinstance(snap, dict) or not snap.get("snapshot_id") or not snap.get("chunk_ids"):
        raise ValueError("customer_provenance_missing_or_stale:ASK_OR_HOLD")
    if snap.get("current_only") is not True:
        raise ValueError("customer_provenance_stale:ASK_OR_HOLD")
    return att


def attach_provenance_to_approval(req: Any, attachment: Mapping[str, Any]) -> Any:
    """Set ``req.provenance`` to a deep copy of the sanitized attachment.

    Pure: never changes status/action_mode and never executes anything.
    """
    att = deepcopy(dict(attachment or {}))
    assert_no_raw_payload(att)
    # Structural guard: only the known attachment surface is accepted.
    allowed_top = {
        "version", "snapshot", "evidence_refs", "relationship_refs",
        "trace_id", "case_id", "response_state",
        "provenance_status", "has_current_evidence",
    }
    unknown = set(att) - allowed_top
    if unknown:
        raise ValueError(f"provenance_unknown_keys:{sorted(unknown)}")
    req.provenance = att
    return req


def attach_provenance_to_proof_event(event: Any, attachment: Mapping[str, Any]) -> Any:
    """Merge the attachment into the existing ``payload`` namespace.

    Requires current evidence (fail-closed): raises instead of writing
    a proof event bound to missing/stale provenance.
    """
    att = require_current_provenance(attachment)
    clean = deepcopy(att)
    assert_no_raw_payload(clean)
    payload = dict(getattr(event, "payload", None) or {})
    payload[PROVENANCE_KEY] = clean
    # Mirror the frozen refs at top-level payload keys for ledger queries
    # without duplicating bodies.
    snap = clean.get("snapshot") or {}
    if isinstance(snap, dict):
        payload["knowledge_snapshot_id"] = snap.get("snapshot_id", "")
        payload["knowledge_as_of"] = snap.get("as_of", "")
    event.payload = payload
    return event


def case_evidence_ids(attachment: Mapping[str, Any]) -> list[str]:
    """ID-only refs for case evidence contracts (e.g. Ticket.evidence_ids)."""
    att = dict(attachment or {})
    snap = att.get("snapshot") if isinstance(att.get("snapshot"), dict) else {}
    ids: list[str] = []
    snap_id = str((snap or {}).get("snapshot_id", "")).strip()
    if snap_id:
        ids.append(snap_id)
    for cid in list((snap or {}).get("chunk_ids") or [])[:MAX_CHUNK_IDS]:
        cid_s = str(cid).strip()
        if cid_s and cid_s not in ids:
            ids.append(cid_s)
    for ref in list(att.get("relationship_refs") or [])[:MAX_RELATIONSHIP_REFS]:
        if isinstance(ref, dict):
            uri = str(ref.get("uri_ref", "")).strip()
            if uri and uri not in ids:
                ids.append(uri)
    return ids


def new_approval_request_for_outcome(
    *,
    outcome: Any,
    account_id: str = "",
    channel: str = "web",
    action_type: str = "support_reply_draft",
    object_id: str = "",
    risk_level: str = "",
) -> Any:
    """Construct (not persist, not execute) an ApprovalRequest with provenance.

    Summaries are derived from intent/sector/state only — the customer
    message body is never copied. The caller persists via the existing
    approval_center store (``create``); this helper performs no I/O.
    """
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    data = outcome.to_dict() if hasattr(outcome, "to_dict") else dict(outcome or {})
    provenance = data.get("provenance") or {}
    if not provenance:
        provenance = build_provenance_attachment(
            snapshot_ref=data.get("knowledge_snapshot"),
            evidence=data.get("evidence"),
            trace_id=str(data.get("trace_id", "")),
            case_id=str(data.get("case_id", "")),
            response_state=str(data.get("response_state", "")),
        )
    intent = _safe_str(data.get("intent", "unknown"), 64)
    sector = _safe_str(data.get("sector", ""), 64)
    state = _safe_str(data.get("response_state", ""), 32)
    action_mode = str(data.get("action_mode", "approval_required"))
    if action_mode not in ("draft_only", "approval_required", "blocked"):
        action_mode = "approval_required"
    req = ApprovalRequest(
        object_type="customer_ops_outcome",
        object_id=_safe_str(object_id or data.get("case_id", "")),
        action_type=_safe_str(action_type, 64),
        action_mode=action_mode,
        channel=_safe_str(channel, 32) or None,
        summary_ar=f"مسودة عملية عميل ({intent}/{sector}/{state}) بانتظار الاعتماد.",
        summary_en=f"Customer-ops draft ({intent}/{sector}/{state}) pending approval.",
        risk_level=_safe_str(risk_level or data.get("priority", "p2"), 16) or "p2",
        proof_impact=f"customer_ops:{state}:{intent}",
        customer_id=_safe_str(account_id, 128) or None,
        proof_target=f"proof:{_safe_str(data.get('case_id', ''))}",
    )
    return attach_provenance_to_approval(req, provenance)


def new_proof_event_for_outcome(
    *,
    outcome: Any,
    event_type: str = "diagnostic_delivered",
    customer_handle: str = "Saudi B2B customer",
) -> Any:
    """Construct (not record) a verified ProofEvent bound to current evidence.

    Raises ValueError when provenance is missing/stale — the caller must
    ASK/HOLD instead of recording proof.
    """
    from auto_client_acquisition.proof_ledger.schemas import ProofEvent

    data = outcome.to_dict() if hasattr(outcome, "to_dict") else dict(outcome or {})
    provenance = data.get("provenance") or {}
    if not provenance:
        provenance = build_provenance_attachment(
            snapshot_ref=data.get("knowledge_snapshot"),
            evidence=data.get("evidence"),
            trace_id=str(data.get("trace_id", "")),
            case_id=str(data.get("case_id", "")),
            response_state=str(data.get("response_state", "")),
        )
    require_current_provenance(provenance)
    intent = _safe_str(data.get("intent", "unknown"), 64)
    sector = _safe_str(data.get("sector", ""), 64)
    snap = provenance.get("snapshot") or {}
    sources = list(snap.get("source_types") or [])
    event = ProofEvent(
        event_type=event_type,  # type: ignore[arg-type]
        customer_handle=_safe_str(customer_handle, 255) or "Saudi B2B customer",
        summary_ar=f"دليل موثّق ({intent}/{sector}) من لقطة {snap.get('snapshot_id', '')}.",
        summary_en=f"Verified evidence ({intent}/{sector}) from snapshot {snap.get('snapshot_id', '')}.",
        evidence_source=",".join(sources[:MAX_SOURCE_TYPES]),
        approval_status="approval_required",
    )
    return attach_provenance_to_proof_event(event, provenance)


__all__ = [
    "MAX_CHUNK_IDS",
    "MAX_EVIDENCE_REFS",
    "MAX_RELATIONSHIP_REFS",
    "PROVENANCE_KEY",
    "PROVENANCE_VERSION",
    "FORBIDDEN_KEY_SUBSTRINGS",
    "assert_no_raw_payload",
    "attach_provenance_to_approval",
    "attach_provenance_to_proof_event",
    "build_evidence_refs",
    "build_provenance_attachment",
    "build_relationship_refs",
    "build_snapshot_provenance",
    "case_evidence_ids",
    "new_approval_request_for_outcome",
    "new_proof_event_for_outcome",
    "provenance_status_of",
    "require_current_provenance",
]
