#!/usr/bin/env python3
"""Wave 7.5 §24.5 — Customer Onboarding CLI Wizard.

Run by founder during a setup call with a paying customer (live screen-share).
Walks 8 integration channels + generates personalized integration_plan.md
+ env-var template for Railway + customer-portal token (gitignored).

Usage:
    python3 scripts/dealix_customer_onboarding_wizard.py \\
        --customer-handle acme-real-estate \\
        --company "Acme Riyadh Real Estate" \\
        --sector real_estate

    # Non-interactive mode (uses defaults / from inputs file):
    python3 scripts/dealix_customer_onboarding_wizard.py \\
        --customer-handle acme-real-estate --inputs-json wizard_inputs.json

Outputs (all under data/customers/<handle>/, gitignored per .gitignore):
    - integration_plan.md  (customer-facing setup checklist)
    - env_vars_railway.txt  (founder pastes to Railway dashboard)
    - customer_portal_token.txt  (single-line token)
    - feature_requests.jsonl   (for V14_CUSTOMER_SIGNAL_SYNTHESIS feed)

Hard rules respected:
    - NO_LIVE_SEND, NO_LIVE_CHARGE, NO_COLD_WHATSAPP, NO_SCRAPING
    - NO_FAKE_PROOF: refuses to generate plan if DPA not signed
    - PII protection: customer-portal-token written to gitignored file only
    - No forbidden tokens (نضمن / guaranteed / blast / scraping) in output
"""
from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIVE_DIR_BASE = REPO_ROOT / "data" / "customers"

# ─── Saudi-Arabic prompts (founder reads aloud during setup call) ──
PROMPTS_AR = {
    "intro": "مرحباً، نبدأ بـ wizard إعداد {company} على Dealix. الخطوات ٨ — كل خطوة تأخذ ١-٢ دقيقة. هل نبدأ؟",
    "dpa_check": "هل DPA (اتفاقيّة معالجة البيانات) موقّعة من المحامي مع {company}؟ (y/n)",
    "dpa_blocked": "❌ لا يمكن إكمال الـ wizard بدون DPA موقّعة. راجع docs/LEGAL_ENGAGEMENT.md ثم أعد التشغيل.",
    "channel_whatsapp": "(١/٨) WhatsApp Business — هل {company} تستخدم WhatsApp Business مع رقم رسمي؟ (y/n)",
    "channel_whatsapp_phone": "  → رقم الواتساب (مع رمز الدولة، مثل +966512345678): ",
    "channel_whatsapp_meta_verified": "  → هل تمّت موافقة Meta على رقمكم؟ (y/n)",
    "channel_email": "(٢/٨) Email forwarding — هل تبي توصلكم leads عبر إيميل؟ (y/n)",
    "channel_email_address": "  → عنوان البريد المُحوَّل إليه (مثلاً sales@{handle}.com): ",
    "channel_crm": "(٣/٨) CRM — هل عندكم HubSpot / Zoho / Salesforce؟ (y/n)",
    "channel_crm_provider": "  → أيّ CRM؟ (hubspot / zoho / salesforce / other): ",
    "channel_csv": "(٤/٨) CSV upload — هل عندكم قائمة leads جاهزة (Excel / Sheets / CSV)؟ (y/n)",
    "channel_calendly": "(٥/٨) Calendly — هل تبون تستخدمون Calendly لحجز Demos؟ (y/n)",
    "channel_calendly_link": "  → رابط Calendly (مثل calendly.com/your-name): ",
    "channel_payment": "(٦/٨) Payment — Sprint بنك transfer أو Moyasar؟ (bank/moyasar)",
    "channel_portal": "(٧/٨) Customer Portal — أنشئ الـ token الآن (تلقائي): ",
    "channel_approval": "(٨/٨) قناة الموافقة — كل القرارات تمر عبر /decisions.html. هل المؤسس مرتاح بهذا التدفّق؟ (y/n)",
    "feature_request": "هل عندك طلب ميزة خارج النطاق الحالي؟ (اضغط Enter للتخطّي): ",
    "complete": "✅ الـ wizard اكتمل. الملفات التالية أُنشئت في {output_dir}",
}

PROMPTS_EN = {
    "intro": "Welcome — onboarding wizard for {company} on Dealix. 8 steps, 1-2 min each. Ready?",
    "dpa_check": "Is the DPA (Data Processing Agreement) lawyer-signed for {company}? (y/n)",
    "dpa_blocked": "❌ Cannot proceed without lawyer-signed DPA. See docs/LEGAL_ENGAGEMENT.md then re-run.",
    "complete": "✅ Wizard complete. Files created in {output_dir}",
}

# Forbidden tokens scrub before writing output (Article 8)
_FORBIDDEN_PATTERNS = [
    re.compile(r"\bguaranteed?\b", re.IGNORECASE),
    re.compile(r"\bblast\b", re.IGNORECASE),
    re.compile(r"\bscrap(?:e|ing)\b\s", re.IGNORECASE),
    re.compile(r"\bcold\s+(whatsapp|outreach|email)\b", re.IGNORECASE),
    re.compile(r"نضمن"),
]


def _scrub_forbidden(text: str) -> str:
    """Refuse to emit any forbidden tokens — fail closed."""
    for pat in _FORBIDDEN_PATTERNS:
        if pat.search(text):
            raise ValueError(
                f"REFUSING — generated text contains forbidden token matching pattern {pat.pattern}. "
                "Article 8 violation. Fix the source."
            )
    return text


def _validate_phone(phone: str) -> bool:
    # Saudi format +966[5][8 digits]
    return bool(re.match(r"^\+966[5][0-9]{8}$", phone.strip()))


def _validate_email(email: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email.strip()))


def _validate_handle(handle: str) -> bool:
    return bool(re.match(r"^[a-z0-9-]{1,64}$", handle))


def _generate_token() -> str:
    # 24-char URL-safe token — sufficient for per-customer access gate
    return f"dealix-cust-{secrets.token_urlsafe(16)}"


def _ask_yn(prompt: str, *, interactive: bool, default: bool = False) -> bool:
    if not interactive:
        return default
    while True:
        ans = input(prompt + " ").strip().lower()
        if ans in {"y", "yes", "نعم", "ايه", "اي"}:
            return True
        if ans in {"n", "no", "لا", "ﻻ"}:
            return False
        print("  please answer y/n")


def _ask_str(prompt: str, *, interactive: bool, default: str = "", validator=None) -> str:
    if not interactive:
        return default
    while True:
        ans = input(prompt).strip()
        if not ans and default:
            return default
        if validator and not validator(ans):
            print(f"  invalid format, try again")
            continue
        return ans


def run_wizard(
    *,
    customer_handle: str,
    company: str,
    sector: str,
    inputs: dict | None = None,
    interactive: bool = True,
) -> dict:
    """Main wizard entry. Returns the collected inputs dict."""

    if not _validate_handle(customer_handle):
        raise ValueError(f"Invalid customer_handle: {customer_handle}")

    inputs = inputs or {}
    interactive = interactive and inputs == {}

    print("\n" + "=" * 60)
    print(PROMPTS_AR["intro"].format(company=company))
    print(PROMPTS_EN["intro"].format(company=company))
    print("=" * 60)

    # ── DPA gate (Article 8 + Wave 7 §23.5.5) ──
    dpa_signed = inputs.get("dpa_signed", False) if not interactive else _ask_yn(
        PROMPTS_AR["dpa_check"].format(company=company), interactive=interactive
    )
    if not dpa_signed:
        print(PROMPTS_AR["dpa_blocked"])
        print(PROMPTS_EN["dpa_blocked"])
        raise SystemExit(2)

    collected = {
        "customer_handle": customer_handle,
        "company": company,
        "sector": sector,
        "wizard_run_at": datetime.now(timezone.utc).isoformat(),
        "dpa_signed": True,
        "channels": {},
    }

    # ── 1/8 WhatsApp Business ──
    use_whatsapp = inputs.get("channels", {}).get("whatsapp", {}).get("enabled", True) if not interactive else _ask_yn(
        PROMPTS_AR["channel_whatsapp"].format(company=company), interactive=interactive, default=True
    )
    if use_whatsapp:
        wa_phone = inputs.get("channels", {}).get("whatsapp", {}).get("phone", "+966500000000") if not interactive else _ask_str(
            PROMPTS_AR["channel_whatsapp_phone"], interactive=interactive, validator=_validate_phone
        )
        wa_verified = inputs.get("channels", {}).get("whatsapp", {}).get("meta_verified", False) if not interactive else _ask_yn(
            PROMPTS_AR["channel_whatsapp_meta_verified"], interactive=interactive
        )
        collected["channels"]["whatsapp"] = {
            "enabled": True,
            "phone": wa_phone,
            "meta_verified": wa_verified,
            "fallback": "manual_personal_whatsapp" if not wa_verified else "live_meta_api",
            "guide": "docs/integrations/WHATSAPP_BUSINESS_SETUP.md",
        }
    else:
        collected["channels"]["whatsapp"] = {"enabled": False}

    # ── 2/8 Email forwarding ──
    use_email = inputs.get("channels", {}).get("email", {}).get("enabled", True) if not interactive else _ask_yn(
        PROMPTS_AR["channel_email"], interactive=interactive, default=True
    )
    if use_email:
        forwarded_to = f"dealix-{customer_handle}@dealix.me"
        collected["channels"]["email"] = {
            "enabled": True,
            "forwarded_to": forwarded_to,
            "manual_workaround": "founder forwards each Gmail/Outlook lead until lead_intake_email TARGET activates",
            "guide": "docs/integrations/EMAIL_INBOUND_SETUP.md",
        }
    else:
        collected["channels"]["email"] = {"enabled": False}

    # ── 3/8 CRM ──
    use_crm = inputs.get("channels", {}).get("crm", {}).get("enabled", False) if not interactive else _ask_yn(
        PROMPTS_AR["channel_crm"], interactive=interactive
    )
    if use_crm:
        crm_provider = inputs.get("channels", {}).get("crm", {}).get("provider", "hubspot") if not interactive else _ask_str(
            PROMPTS_AR["channel_crm_provider"], interactive=interactive, default="hubspot"
        )
        collected["channels"]["crm"] = {
            "enabled": True,
            "provider": crm_provider,
            "manual_workaround": "weekly CSV export from " + crm_provider + " until connector activates (Wave 8)",
            "guide": "docs/integrations/CRM_CONNECTOR_SETUP.md",
        }
    else:
        collected["channels"]["crm"] = {"enabled": False}

    # ── 4/8 CSV bulk upload ──
    use_csv = inputs.get("channels", {}).get("csv_bulk", {}).get("enabled", True) if not interactive else _ask_yn(
        PROMPTS_AR["channel_csv"], interactive=interactive, default=True
    )
    collected["channels"]["csv_bulk"] = {
        "enabled": use_csv,
        "manual_workaround": "founder imports first batch via CLI; self-serve deferred to Wave 8" if use_csv else None,
        "guide": "docs/integrations/CSV_BULK_UPLOAD.md",
    }

    # ── 5/8 Calendly ──
    use_calendly = inputs.get("channels", {}).get("calendly", {}).get("enabled", True) if not interactive else _ask_yn(
        PROMPTS_AR["channel_calendly"], interactive=interactive, default=True
    )
    if use_calendly:
        calendly_link = inputs.get("channels", {}).get("calendly", {}).get("link", "") if not interactive else _ask_str(
            PROMPTS_AR["channel_calendly_link"], interactive=interactive, default=""
        )
        collected["channels"]["calendly"] = {
            "enabled": True,
            "link": calendly_link,
            "manual_workaround": "Calendly Standard plan ($10/mo); webhook handler deferred to Wave 8",
            "guide": "docs/integrations/CALENDLY_SETUP.md",
        }
    else:
        collected["channels"]["calendly"] = {"enabled": False}

    # ── 6/8 Payment ──
    payment_method = inputs.get("channels", {}).get("payment", {}).get("method", "bank") if not interactive else _ask_str(
        PROMPTS_AR["channel_payment"], interactive=interactive, default="bank"
    )
    collected["channels"]["payment"] = {
        "enabled": True,
        "method": payment_method if payment_method in {"bank", "moyasar"} else "bank",
        "live_charge": False,  # Always — Wave 7 §23.5.6 hard rule
        "moyasar_live": False,  # NO_LIVE_CHARGE during Wave 7
        "founder_must_confirm_manually": True,
        "guide": "docs/integrations/PAYMENT_MOYASAR_LIVE.md",
    }

    # ── 7/8 Customer Portal token ──
    portal_token = _generate_token()
    collected["channels"]["portal"] = {
        "enabled": True,
        "token": portal_token,
        "url": f"https://dealix.me/customer-portal.html?org={customer_handle}&access={portal_token}",
        "guide": "docs/integrations/CUSTOMER_PORTAL_TOKEN.md",
    }

    # ── 8/8 Approval channel ──
    approval_ok = inputs.get("channels", {}).get("approval", {}).get("ok", True) if not interactive else _ask_yn(
        PROMPTS_AR["channel_approval"], interactive=interactive, default=True
    )
    collected["channels"]["approval"] = {
        "enabled": True,
        "founder_owns": approval_ok,
        "url": f"https://dealix.me/decisions.html?org={customer_handle}&access={portal_token}",
        "guide": "docs/integrations/APPROVAL_CHANNEL_SETUP.md",
    }

    # ── Optional feature request ──
    if interactive:
        feat_req = input("\n" + PROMPTS_AR["feature_request"]).strip()
        if feat_req:
            collected["feature_requests"] = [feat_req]
    else:
        collected["feature_requests"] = inputs.get("feature_requests", [])

    return collected


def write_outputs(collected: dict, output_dir: Path) -> dict[str, Path]:
    """Generate the 4 output files. Returns dict of file -> path."""

    output_dir.mkdir(parents=True, exist_ok=True)
    handle = collected["customer_handle"]
    company = collected["company"]

    # ── 1. integration_plan.md (customer-facing) ──
    md_lines = [
        f"# خطّة الإدماج — {company}",
        "",
        f"**Customer handle:** `{handle}`  ",
        f"**Sector:** {collected['sector']}  ",
        f"**Generated:** {collected['wizard_run_at']}  ",
        f"**DPA signed:** ✅",
        "",
        "هذا الملف يلخّص كيف تربط بياناتك مع Dealix.",
        "كل قناة لها guide مفصّل في `docs/integrations/`.",
        "",
        "---",
        "",
        "## القنوات المُفعّلة",
        "",
    ]

    for idx, (channel_name, conf) in enumerate(collected["channels"].items(), 1):
        if not conf.get("enabled"):
            md_lines.append(f"### {idx}. {channel_name} — ⏸️ غير مُفعّل")
            md_lines.append("")
            continue
        md_lines.append(f"### {idx}. {channel_name} — ✅ مُفعّل")
        md_lines.append("")
        for k, v in conf.items():
            if k in {"enabled", "guide"}:
                continue
            if k == "token":
                v = "***REDACTED*** (محفوظ في customer_portal_token.txt — لا يُكشف هنا)"
            md_lines.append(f"- **{k}:** {v}")
        if "guide" in conf:
            md_lines.append(f"- **Setup guide:** [`{conf['guide']}`](../../{conf['guide']})")
        md_lines.append("")

    md_lines.extend([
        "---",
        "",
        "## الخطوات التالية",
        "",
        "1. راجع كل setup guide مذكور أعلاه",
        "2. قدّم لـ Sami أيّ معلومات مطلوبة (Meta tokens, Calendly link, إلخ)",
        "3. Sami يضيف ENV vars على Railway (انظر `env_vars_railway.txt`)",
        "4. ابدأ Sprint Day 0 بعد تأكيد الإدماج",
        "",
        "## للتواصل",
        "",
        f"- WhatsApp المؤسس: مذكور في خطاب الترحيب",
        f"- Customer Portal: عبر الرابط في `customer_portal_token.txt`",
        f"- Decision queue: `https://dealix.me/decisions.html?org={handle}&access=<token>`",
        "",
        "## Hard rules (لا تتغيّر)",
        "",
        "- ❌ Dealix لا يرسل WhatsApp تلقائي (NO_LIVE_SEND)",
        "- ❌ Dealix لا يخصم بطاقة بدون تأكيد المؤسس (NO_LIVE_CHARGE)",
        "- ❌ Dealix لا يستخرج بيانات منافسيك (NO_SCRAPING)",
        "- ✅ كل إجراء خارجي يمر بموافقتك",
        "- ✅ Refund 100% خلال 14 يوم لـ Sprint",
        "",
    ])

    integration_plan_md = "\n".join(md_lines)
    _scrub_forbidden(integration_plan_md)  # Article 8 enforcement
    plan_path = output_dir / "integration_plan.md"
    plan_path.write_text(integration_plan_md, encoding="utf-8")

    # ── 2. env_vars_railway.txt (founder pastes to Railway) ──
    env_lines = [
        "# Railway env vars for customer: " + handle,
        f"# Generated: {collected['wizard_run_at']}",
        "# DO NOT commit this file. See .gitignore (data/customers/**)",
        "",
        f"DEALIX_CUSTOMER_HANDLE={handle}",
        f"DEALIX_CUSTOMER_COMPANY={company}",
        f"DEALIX_CUSTOMER_SECTOR={collected['sector']}",
        "",
    ]
    wa_conf = collected["channels"].get("whatsapp", {})
    if wa_conf.get("enabled") and wa_conf.get("meta_verified"):
        env_lines.extend([
            "# WhatsApp Business — set these from Meta Business dashboard",
            f"WHATSAPP_PHONE_NUMBER_ID_{handle.upper().replace('-', '_')}=<paste-from-meta>",
            f"WHATSAPP_ACCESS_TOKEN_{handle.upper().replace('-', '_')}=<paste-from-meta>",
            "",
        ])
    cal_conf = collected["channels"].get("calendly", {})
    if cal_conf.get("enabled") and cal_conf.get("link"):
        env_lines.append(f"CALENDLY_LINK_{handle.upper().replace('-', '_')}={cal_conf['link']}")
    env_text = "\n".join(env_lines)
    env_path = output_dir / "env_vars_railway.txt"
    env_path.write_text(env_text, encoding="utf-8")

    # ── 3. customer_portal_token.txt (single-line) ──
    portal = collected["channels"].get("portal", {})
    token_path = output_dir / "customer_portal_token.txt"
    token_path.write_text(portal.get("token", ""), encoding="utf-8")

    # ── 4. feature_requests.jsonl (feeds V14_CUSTOMER_SIGNAL_SYNTHESIS) ──
    fr_path = output_dir / "feature_requests.jsonl"
    feat_reqs = collected.get("feature_requests", [])
    fr_lines = []
    for req in feat_reqs:
        fr_lines.append(json.dumps({
            "customer_handle": handle,
            "request_text": req,
            "logged_at": collected["wizard_run_at"],
            "wave_logged": "wave_7_5",
        }, ensure_ascii=False))
    fr_path.write_text("\n".join(fr_lines) + ("\n" if fr_lines else ""), encoding="utf-8")

    return {
        "integration_plan": plan_path,
        "env_vars": env_path,
        "portal_token": token_path,
        "feature_requests": fr_path,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Customer Onboarding Wizard")
    parser.add_argument("--customer-handle", required=True, help="lowercase-hyphenated handle")
    parser.add_argument("--company", default="", help="customer company name (defaults to handle)")
    parser.add_argument("--sector", required=True, choices=[
        "real_estate", "agencies", "services", "consulting",
        "training", "construction", "hospitality", "logistics",
    ])
    parser.add_argument("--inputs-json", default=None, help="non-interactive mode: JSON file of pre-filled inputs")
    parser.add_argument("--output-base-dir", default=str(LIVE_DIR_BASE), help="output directory base (default: data/customers/)")
    args = parser.parse_args()

    company = args.company or args.customer_handle.replace("-", " ").title()

    inputs = None
    interactive = True
    if args.inputs_json:
        inputs_path = Path(args.inputs_json)
        if not inputs_path.exists():
            print(f"Inputs file not found: {inputs_path}", file=sys.stderr)
            return 2
        inputs = json.loads(inputs_path.read_text(encoding="utf-8"))
        interactive = False

    try:
        collected = run_wizard(
            customer_handle=args.customer_handle,
            company=company,
            sector=args.sector,
            inputs=inputs,
            interactive=interactive,
        )
    except SystemExit:
        return 2
    except ValueError as exc:
        print(f"REFUSING — {exc}", file=sys.stderr)
        return 2

    output_dir = Path(args.output_base_dir) / args.customer_handle
    files = write_outputs(collected, output_dir)

    print()
    print(PROMPTS_AR["complete"].format(output_dir=str(output_dir)))
    print(PROMPTS_EN["complete"].format(output_dir=str(output_dir)))
    print()
    for label, path in files.items():
        print(f"  {label}: {path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path}")
    print()
    print("Next steps:")
    print(f"  1. Email integration_plan.md to customer (from your Gmail, manually)")
    print(f"  2. Add env_vars_railway.txt entries to Railway dashboard (founder action)")
    print(f"  3. Schedule Day 1 of Sprint")
    return 0


if __name__ == "__main__":
    sys.exit(main())
