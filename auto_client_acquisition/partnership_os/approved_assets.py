"""Approved partner messaging library — AR + EN.

Partners may use these assets verbatim. Each asset declares the
claims a partner is allowed to make and the claims that are forbidden
(no guaranteed ROI, no exclusivity, no PDPL/compliance guarantee).

The disclosure asset is mandatory: a partner cannot activate a
referral link without accepting it (enforced by the router).

Pure data + read helpers. No I/O. The router can seed these into
``ApprovedAssetRecord`` rows or serve them directly.
"""

from __future__ import annotations

from typing import Any

_FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "no guaranteed ROI or revenue outcome",
    "no exclusivity claim ('exclusive Dealix partner')",
    "no PDPL/ZATCA compliance guarantee on Dealix's behalf",
    "no cold WhatsApp / LinkedIn automation / scraping in your name",
)

# Each asset: stable id, type, locale, title, body, allowed/forbidden claims.
_ASSETS: tuple[dict[str, Any], ...] = (
    {
        "id": "asset_recruit_intro_ar",
        "asset_type": "recruitment_message",
        "locale": "ar",
        "title": "رسالة تعريف الإحالة",
        "body": (
            "أستخدم Dealix لإدارة الـ inbound العربي بطريقة proof-led: كل قرار "
            "خارجي يمر على موافقة بشرية، وكل أسبوع فيه Proof Pack قابل للتدقيق. "
            "لو تبغى تشوفهم، استخدم رابط الإحالة الخاص فيي — يوصلك تشخيص أولي "
            "بدون أي التزام."
        ),
        "allowed_claims": [
            "Dealix is approval-first and proof-led",
            "first Diagnostic carries no obligation",
        ],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
    {
        "id": "asset_recruit_intro_en",
        "asset_type": "recruitment_message",
        "locale": "en",
        "title": "Referral intro message",
        "body": (
            "I use Dealix to run Arabic inbound in a proof-led way: every "
            "external action goes through human approval, and every week "
            "produces an auditable Proof Pack. If you want to see it, use my "
            "referral link — you get an initial Diagnostic with no obligation."
        ),
        "allowed_claims": [
            "Dealix is approval-first and proof-led",
            "first Diagnostic carries no obligation",
        ],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
    {
        "id": "asset_disclosure_ar",
        "asset_type": "disclosure",
        "locale": "ar",
        "title": "إفصاح الشراكة (إلزامي)",
        "body": (
            "إفصاح: أنا شريك إحالة لـ Dealix وقد أحصل على عمولة إذا اشترك من "
            "أرشّحه. هذا الإفصاح إلزامي ويجب أن يظهر بوضوح مع أي توصية. "
            "لا أقدّم أي ضمان نتائج أو عائد، ولا أمثّل Dealix تمثيلاً حصرياً."
        ),
        "allowed_claims": ["clear paid-referral disclosure"],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
    {
        "id": "asset_disclosure_en",
        "asset_type": "disclosure",
        "locale": "en",
        "title": "Partnership disclosure (mandatory)",
        "body": (
            "Disclosure: I am a Dealix referral partner and may earn a "
            "commission if someone I refer subscribes. This disclosure is "
            "mandatory and must appear clearly with any recommendation. I make "
            "no guarantee of results or ROI and do not represent Dealix "
            "exclusively."
        ),
        "allowed_claims": ["clear paid-referral disclosure"],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
    {
        "id": "asset_link_caption_ar",
        "asset_type": "link_caption",
        "locale": "ar",
        "title": "تعليق رابط الإحالة",
        "body": (
            "رابط إحالة Dealix — تشخيص أولي بدون التزام. (إفصاح: قد أحصل على "
            "عمولة عند الاشتراك.)"
        ),
        "allowed_claims": ["no-obligation Diagnostic", "paid-referral disclosure"],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
    {
        "id": "asset_link_caption_en",
        "asset_type": "link_caption",
        "locale": "en",
        "title": "Referral link caption",
        "body": (
            "Dealix referral link — no-obligation initial Diagnostic. "
            "(Disclosure: I may earn a commission on subscription.)"
        ),
        "allowed_claims": ["no-obligation Diagnostic", "paid-referral disclosure"],
        "forbidden_claims": list(_FORBIDDEN_CLAIMS),
        "version": "1.0",
    },
)


def list_assets(
    *, locale: str | None = None, asset_type: str | None = None
) -> list[dict[str, Any]]:
    """Return approved assets, optionally filtered by locale / type."""
    out: list[dict[str, Any]] = []
    for asset in _ASSETS:
        if locale is not None and asset["locale"] != locale:
            continue
        if asset_type is not None and asset["asset_type"] != asset_type:
            continue
        out.append(dict(asset))
    return out


def get_disclosure(locale: str = "ar") -> dict[str, Any]:
    """Return the mandatory disclosure asset for ``locale`` (falls back to AR)."""
    matches = list_assets(locale=locale, asset_type="disclosure")
    if matches:
        return matches[0]
    return list_assets(locale="ar", asset_type="disclosure")[0]


def disclosure_text(locale: str = "ar") -> str:
    """Return only the disclosure body text for ``locale``."""
    return str(get_disclosure(locale)["body"])


__all__ = ["list_assets", "get_disclosure", "disclosure_text"]
