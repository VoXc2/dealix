"""The 12 canonical integrations — Wave 13 Phase 10 truth registry.

Per plan §32.4A.3:
  L1 = manual / CSV (customer pastes; founder confirms)
  L2 = read-only OAuth (pulls customer data into Dealix)
  L3 = controlled write (approved-only mutations; NEVER live send/charge)

Hard rule: NO entry is L3 unless `L3_proven_by_5_plus_customers=True`.

Constitution:
  Article 4: every entry declares relevant hard gates
  Article 8: last_tested_at is honest (placeholder dates clearly tagged)
  Article 11: pure data — registry only; no integration logic here
"""

from __future__ import annotations

from auto_client_acquisition.integration_capability.schemas import (
    IntegrationCapability,
)

# ── Lead sources ──────────────────────────────────────────────────────
_HUNTER = IntegrationCapability(
    integration_id="hunter_io",
    name_ar="Hunter.io (إثراء البيانات)",
    name_en="Hunter.io (data enrichment)",
    category="lead_source",
    current_level=1,
    supported_directions=("inbound",),
    oauth_required=False,  # API key
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 عند تفعيل HUNTER_API_KEY في Railway."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 once HUNTER_API_KEY env var is set on Railway."
    ),
    hard_gates_respected=("no_scraping", "no_cold_whatsapp"),
    last_tested_at_iso="2026-05-08",
)

_APOLLO = IntegrationCapability(
    integration_id="apollo_io",
    name_ar="Apollo.io (إثراء + بحث)",
    name_en="Apollo.io (enrichment + search)",
    category="lead_source",
    current_level=1,
    supported_directions=("inbound",),
    oauth_required=False,
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 عند توقيع عقد B2B + APOLLO_API_KEY."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 once Apollo B2B contract signed + APOLLO_API_KEY set."
    ),
    hard_gates_respected=("no_scraping",),
    last_tested_at_iso="placeholder_not_tested",
)

# ── CRMs ──────────────────────────────────────────────────────────────
_HUBSPOT = IntegrationCapability(
    integration_id="hubspot",
    name_ar="HubSpot CRM",
    name_en="HubSpot CRM",
    category="crm",
    current_level=1,
    supported_directions=("inbound", "outbound"),
    oauth_required=True,
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 (read-only) عند أوّل عميل يطلب مزامنة contacts."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 (read-only) when first customer asks for contacts sync."
    ),
    hard_gates_respected=("no_live_send", "no_cold_whatsapp"),
    last_tested_at_iso="placeholder_not_tested",
)

_ZOHO = IntegrationCapability(
    integration_id="zoho_crm",
    name_ar="Zoho CRM",
    name_en="Zoho CRM",
    category="crm",
    current_level=1,
    supported_directions=("inbound", "outbound"),
    oauth_required=True,
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 عند أوّل عميل سعودي يستخدم Zoho فعليًا."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 when first Saudi customer actually uses Zoho."
    ),
    hard_gates_respected=("no_live_send",),
    last_tested_at_iso="placeholder_not_tested",
)

_SALESFORCE = IntegrationCapability(
    integration_id="salesforce",
    name_ar="Salesforce CRM",
    name_en="Salesforce CRM",
    category="crm",
    current_level=1,
    supported_directions=("inbound", "outbound"),
    oauth_required=True,
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 عند أوّل عميل enterprise (≥٣ مفاتيح في Salesforce)."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 once first enterprise customer (≥3 Salesforce seats) signs."
    ),
    hard_gates_respected=("no_live_send",),
    last_tested_at_iso="placeholder_not_tested",
)

# ── Spreadsheet / files ───────────────────────────────────────────────
_GOOGLE_SHEETS = IntegrationCapability(
    integration_id="google_sheets",
    name_ar="Google Sheets",
    name_en="Google Sheets",
    category="spreadsheet",
    current_level=1,
    supported_directions=("inbound",),
    oauth_required=True,
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 (read) عند أوّل عميل يشارك Sheet مع scope read-only."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 (read) once first customer shares a Sheet read-only."
    ),
    hard_gates_respected=("no_scraping",),
    last_tested_at_iso="2026-05-08",
)

# ── Calendar ──────────────────────────────────────────────────────────
_CAL_COM = IntegrationCapability(
    integration_id="cal_com",
    name_ar="Cal.com (الحجز المفتوح)",
    name_en="Cal.com (open-source booking)",
    category="calendar",
    current_level=2,
    supported_directions=("inbound",),
    oauth_required=False,  # API key
    trigger_for_next_level_ar=(
        "L3 يتطلب إثبات أنّ ٥+ عملاء يستخدمون Cal.com بأمان لأشهر."
    ),
    trigger_for_next_level_en=(
        "L3 requires 5+ customers using Cal.com safely for months."
    ),
    hard_gates_respected=("no_live_send", "no_blast"),
    last_tested_at_iso="2026-05-08",
)

_CALENDLY = IntegrationCapability(
    integration_id="calendly",
    name_ar="Calendly",
    name_en="Calendly",
    category="calendar",
    current_level=1,
    supported_directions=("inbound",),
    oauth_required=False,  # PAT
    trigger_for_next_level_ar=(
        "ينتقل إلى L2 عند تفعيل CALENDLY_PAT للمؤسس."
    ),
    trigger_for_next_level_en=(
        "Moves to L2 once CALENDLY_PAT env var is set."
    ),
    hard_gates_respected=("no_live_send",),
    last_tested_at_iso="placeholder_not_tested",
)

# ── Messaging ─────────────────────────────────────────────────────────
_WHATSAPP_BUSINESS = IntegrationCapability(
    integration_id="whatsapp_business",
    name_ar="WhatsApp Business (Meta)",
    name_en="WhatsApp Business (Meta)",
    category="messaging",
    current_level=1,
    supported_directions=("inbound",),  # outbound NEVER auto
    oauth_required=False,
    trigger_for_next_level_ar=(
        "L2 inbound فقط بعد موافقة Meta على Webhook. "
        "L3 (outbound automatic) محظور دائمًا — Article 4."
    ),
    trigger_for_next_level_en=(
        "L2 inbound only after Meta approves webhook. "
        "L3 (auto-outbound) PERMANENTLY BLOCKED — Article 4."
    ),
    hard_gates_respected=(
        "no_live_send",
        "no_cold_whatsapp",
        "no_blast",
    ),
    last_tested_at_iso="placeholder_not_tested",
)

# ── Payment ───────────────────────────────────────────────────────────
_MOYASAR = IntegrationCapability(
    integration_id="moyasar",
    name_ar="Moyasar (الدفع السعودي)",
    name_en="Moyasar (Saudi payments)",
    category="payment",
    current_level=2,
    supported_directions=("bidirectional",),
    oauth_required=False,  # API key (sandbox today)
    trigger_for_next_level_ar=(
        "ينتقل إلى L3 (controlled invoice creation) فقط بعد KYC + تفعيل live merchant. "
        "live_charge محظور — يبقى approval_required دائمًا."
    ),
    trigger_for_next_level_en=(
        "Moves to L3 (controlled invoice creation) only after KYC + live merchant. "
        "live_charge BLOCKED — always approval_required."
    ),
    hard_gates_respected=("no_live_charge", "no_fake_revenue"),
    last_tested_at_iso="2026-05-08",
)

# ── Compliance / e-invoicing ──────────────────────────────────────────
_ZATCA = IntegrationCapability(
    integration_id="zatca_phase_2",
    name_ar="ZATCA Phase 2 (Fatoora)",
    name_en="ZATCA Phase 2 (Fatoora)",
    category="compliance",
    current_level=2,
    supported_directions=("outbound",),
    oauth_required=False,
    trigger_for_next_level_ar=(
        "L3 (auto-submit للـ Fatoora portal) محظور — يبقى founder approval إجباري. "
        "Wave 24 deadline: 30 يونيو 2026."
    ),
    trigger_for_next_level_en=(
        "L3 (auto-submit to Fatoora portal) BLOCKED — founder approval mandatory. "
        "Wave 24 deadline: June 30, 2026."
    ),
    hard_gates_respected=("no_live_charge", "no_fake_revenue"),
    last_tested_at_iso="2026-05-08",
)

# ── Email ─────────────────────────────────────────────────────────────
_GMAIL = IntegrationCapability(
    integration_id="gmail",
    name_ar="Gmail (مسودات فقط)",
    name_en="Gmail (drafts only)",
    category="email",
    current_level=1,
    supported_directions=("outbound",),
    oauth_required=True,
    trigger_for_next_level_ar=(
        "L2 = إنشاء مسودات فقط. L3 (إرسال تلقائي) محظور دائمًا — Article 4."
    ),
    trigger_for_next_level_en=(
        "L2 = create drafts only. L3 (auto-send) PERMANENTLY BLOCKED — Article 4."
    ),
    hard_gates_respected=("no_live_send", "no_blast"),
    last_tested_at_iso="placeholder_not_tested",
)


# Canonical 12-integration registry
INTEGRATIONS: tuple[IntegrationCapability, ...] = (
    _HUNTER,
    _APOLLO,
    _HUBSPOT,
    _ZOHO,
    _SALESFORCE,
    _GOOGLE_SHEETS,
    _CAL_COM,
    _CALENDLY,
    _WHATSAPP_BUSINESS,
    _MOYASAR,
    _ZATCA,
    _GMAIL,
)

INTEGRATION_IDS: frozenset[str] = frozenset(i.integration_id for i in INTEGRATIONS)


def list_integrations() -> tuple[IntegrationCapability, ...]:
    return INTEGRATIONS


def get_integration(integration_id: str) -> IntegrationCapability | None:
    for i in INTEGRATIONS:
        if i.integration_id == integration_id:
            return i
    return None
