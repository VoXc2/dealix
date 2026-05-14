"""The 11 non-negotiables — single source of truth for the manifesto.

Wave 17. The canonical text lives in `docs/00_constitution/NON_NEGOTIABLES.md`.
This module mirrors it as Python data so the public manifesto endpoint
(`api/routers/dealix_promise.py`) and the doctrine surface tests can
read from one place and never drift.

Each non-negotiable carries:
- `id`: stable string slug
- `title_en` / `title_ar`: bilingual short title
- `promise_en` / `promise_ar`: what we promise to do
- `refusal_en` / `refusal_ar`: what we refuse to do (the safety surface)
- `enforced_by`: list of file paths (tests, middleware, modules) that
  enforce the rule today

If the canonical doc gains a 12th rule, this module gains one entry +
one matching test path. There is no other place to update.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NonNegotiable:
    id: str
    title_en: str
    title_ar: str
    promise_en: str
    promise_ar: str
    refusal_en: str
    refusal_ar: str
    enforced_by: tuple[str, ...]


NON_NEGOTIABLES: tuple[NonNegotiable, ...] = (
    NonNegotiable(
        id="no_scraping",
        title_en="No scraping",
        title_ar="لا تجريف بيانات",
        promise_en=(
            "Every contact we use comes from a legitimate source you can name "
            "— a Source Passport you provided, a public registry you authorize, "
            "a referral with consent."
        ),
        promise_ar=(
            "كل جهة اتصال نستخدمها مصدرها معروف يمكنك تسميته — Source Passport "
            "قدّمته أنت، سجل عام تأذن لنا باستخدامه، أو تحويل برضا صريح."
        ),
        refusal_en=(
            "We do not scrape websites, social platforms, or third-party UIs "
            "to harvest contacts or content. Any data acquired by scraping is "
            "quarantined and excluded from drafts and proof."
        ),
        refusal_ar=(
            "لا نقوم بتجريف المواقع أو منصات التواصل أو الواجهات الخارجية "
            "لجمع جهات الاتصال أو المحتوى. أي بيانات يتم الحصول عليها بالتجريف "
            "تُعزل وتُستبعد من المسودات والإثباتات."
        ),
        enforced_by=(
            "tests/test_no_scraping_engine.py",
        ),
    ),
    NonNegotiable(
        id="no_cold_whatsapp",
        title_en="No cold WhatsApp",
        title_ar="لا واتساب بارد",
        promise_en=(
            "Every WhatsApp message Dealix produces is a draft tied to a "
            "consented relationship — you (the founder) approve every send "
            "individually. The recipient already opted in."
        ),
        promise_ar=(
            "كل رسالة واتساب ينتجها Dealix هي مسودة مرتبطة بعلاقة موافَق عليها "
            "— أنت (المؤسس) توافق على كل إرسال على حدة. المستلم وافق مسبقاً."
        ),
        refusal_en=(
            "We do not send WhatsApp messages to recipients without explicit, "
            "recorded, opt-in consent tied to a Source Passport. Cold WhatsApp "
            "sends are blocked at the safe_send_gateway layer."
        ),
        refusal_ar=(
            "لا نرسل رسائل واتساب لمستقبلين بدون موافقة صريحة موثّقة مرتبطة "
            "بـ Source Passport. الإرسال البارد محجوب في طبقة safe_send_gateway."
        ),
        enforced_by=("tests/test_no_cold_whatsapp.py",),
    ),
    NonNegotiable(
        id="no_linkedin_automation",
        title_en="No LinkedIn automation",
        title_ar="لا أتمتة LinkedIn",
        promise_en=(
            "Dealix uses LinkedIn data only when you provide a legitimate "
            "export you own. We help you write the message; you send it from "
            "your own account."
        ),
        promise_ar=(
            "Dealix يستخدم بيانات LinkedIn فقط عندما تقدّم تصديراً شرعياً تملكه. "
            "نساعدك في صياغة الرسالة؛ أنت ترسلها من حسابك الشخصي."
        ),
        refusal_en=(
            "We do not automate LinkedIn connection requests, messages, "
            "scraping, or feed actions. Any integration that automates "
            "LinkedIn is rejected at PR review and at runtime."
        ),
        refusal_ar=(
            "لا نقوم بأتمتة طلبات الاتصال أو الرسائل أو تجريف بيانات LinkedIn "
            "أو إجراءات الواجهة. أي تكامل يقوم بأتمتة LinkedIn مرفوض على "
            "مستوى مراجعة PR والتشغيل."
        ),
        enforced_by=(
            "tests/test_no_linkedin_automation.py",
        ),
    ),
    NonNegotiable(
        id="no_unsourced_claims",
        title_en="No fake or un-sourced claims",
        title_ar="لا ادعاءات بلا مصدر",
        promise_en=(
            "Every number, quote, case study, and proof artifact carries a "
            "`source_ref` and links to a Source Passport. If you ask where a "
            "number came from, we can show you the file in the same minute."
        ),
        promise_ar=(
            "كل رقم واقتباس ودراسة حالة وإثبات يحمل `source_ref` ويرتبط بـ "
            "Source Passport. لو سألت عن مصدر رقم، نرجع لك بالملف خلال نفس الدقيقة."
        ),
        refusal_en=(
            "We do not publish a number, quote, case study, or proof artifact "
            "without a source. Content without a source is downgraded to "
            "`draft_only` and public proof is blocked."
        ),
        refusal_ar=(
            "لا ننشر رقماً أو اقتباساً أو دراسة حالة أو إثباتاً بدون مصدر. "
            "المحتوى بدون مصدر يُخفّض إلى `draft_only` ويُحجب الإثبات العام."
        ),
        enforced_by=("tests/test_no_guaranteed_claims.py",),
    ),
    NonNegotiable(
        id="no_guaranteed_outcomes",
        title_en="No guaranteed sales outcomes",
        title_ar="لا ضمانات مبيعات",
        promise_en=(
            "We commit to commitments, never guarantees. Our KPI promises read "
            "'we keep working at no cost until X is reached', never 'we ensure "
            "X will close'. The estimate is always marked as such."
        ),
        promise_ar=(
            "نلتزم بالتزامات، لا بضمانات. وعود KPI نقول فيها 'نواصل بدون مقابل "
            "حتى يتحقق X'، ولا نقول أبداً 'نضمن X'. التقدير يُسمّى تقديراً."
        ),
        refusal_en=(
            "We do not promise a fixed revenue, deal count, or conversion rate. "
            "Words like 'guarantee', 'ensure', and 'we will close X deals' are "
            "redacted from drafts."
        ),
        refusal_ar=(
            "لا نَعِد بإيراد ثابت أو عدد صفقات أو معدّل تحويل. كلمات مثل "
            "'نضمن' و'سنغلق X صفقة' تُحذف من المسودات."
        ),
        enforced_by=(
            "tests/test_no_guaranteed_claims.py",
            "tests/test_customer_safe_product_language.py",
        ),
    ),
    NonNegotiable(
        id="no_pii_in_logs",
        title_en="No PII in logs",
        title_ar="لا PII في السجلات",
        promise_en=(
            "Personal data (names, phone numbers, national IDs, emails, "
            "addresses) is redacted at the middleware boundary before any log "
            "writer sees it. PDPL-aligned by construction, not by promise."
        ),
        promise_ar=(
            "البيانات الشخصية (الأسماء، الأرقام، الهويات، البريد، العناوين) "
            "تُحذف عند حدّ الـ middleware قبل أن يراها أي كاتب سجل. متوافق مع "
            "PDPL هندسياً، لا وعداً."
        ),
        refusal_en=(
            "We do not write raw personal data into application logs, friction "
            "logs, or telemetry. A leak is treated as a P0 incident."
        ),
        refusal_ar=(
            "لا نكتب بيانات شخصية خام في سجلات التطبيق أو سجلات الاحتكاك أو "
            "القياسات. أي تسريب يُعالَج كحادثة P0."
        ),
        enforced_by=(
            "api/middleware/bopla_redaction.py",
            "auto_client_acquisition/friction_log/sanitizer.py",
        ),
    ),
    NonNegotiable(
        id="no_sourceless_ai",
        title_en="No source-less knowledge answers",
        title_ar="لا إجابة بلا مصدر",
        promise_en=(
            "Every AI answer about your business cites a Source Passport. If we "
            "lack a source, we return 'source required' — we do not invent an "
            "answer to look helpful."
        ),
        promise_ar=(
            "كل إجابة AI عن عملك مستندة إلى Source Passport. لو ما عندنا مصدر، "
            "نرجع 'مصدر مطلوب' — لا نختلق جواباً لنبدو مفيدين."
        ),
        refusal_en=(
            "We do not answer a knowledge or research question without a "
            "Source Passport. AI responses are blocked when no source is bound "
            "to the query."
        ),
        refusal_ar=(
            "لا نجيب على سؤال معرفي أو بحثي بدون Source Passport. ردود AI "
            "تُحجب عند عدم ربط مصدر بالطلب."
        ),
        enforced_by=("tests/test_no_source_passport_no_ai.py",),
    ),
    NonNegotiable(
        id="no_external_action_without_approval",
        title_en="No external action without approval",
        title_ar="لا فعل خارجي بلا موافقة",
        promise_en=(
            "Every external send, charge, publish, or share waits for an "
            "explicit human approval logged with an approver identity and "
            "timestamp. The audit chain shows who clicked approve, when, and on what."
        ),
        promise_ar=(
            "كل إرسال أو دفعة أو نشر أو مشاركة خارجية ينتظر موافقة بشرية "
            "صريحة موثّقة بهوية الموافِق ووقت الموافقة. سلسلة التدقيق تُظهر "
            "من ضغط 'موافق' ومتى وعلى ماذا."
        ),
        refusal_en=(
            "We do not send, charge, publish, or share externally without "
            "approval. Bypass attempts are rejected by `decide(action, context)` "
            "with `REQUIRE_APPROVAL` or `BLOCK`."
        ),
        refusal_ar=(
            "لا نرسل ولا نَخصم ولا ننشر ولا نشارك خارجياً بدون موافقة. محاولات "
            "الالتفاف تُرفض بواسطة `decide(action, context)` بـ `REQUIRE_APPROVAL` "
            "أو `BLOCK`."
        ),
        enforced_by=(
            "tests/test_pii_external_requires_approval.py",
            "auto_client_acquisition/governance_os/runtime_decision.py",
        ),
    ),
    NonNegotiable(
        id="no_agent_without_identity",
        title_en="No agent without identity",
        title_ar="لا عميل ذكي بلا هوية",
        promise_en=(
            "Every autonomous workflow ties to a registered agent identity "
            "(name, version, owner, governance scope). Every action traces to "
            "an identity in the audit chain."
        ),
        promise_ar=(
            "كل سير عمل ذاتي مرتبط بهوية عميل ذكي مسجّلة (الاسم، الإصدار، "
            "المالك، نطاق الحوكمة). كل إجراء يعود إلى هوية في سلسلة التدقيق."
        ),
        refusal_en=(
            "We do not run an autonomous workflow without a registered agent "
            "identity. Unregistered agents are rejected at the runtime registry."
        ),
        refusal_ar=(
            "لا نُشغّل أي سير عمل ذاتي بدون هوية عميل ذكي مسجّلة. الوكلاء غير "
            "المسجّلين يُرفضون في سجل التشغيل."
        ),
        enforced_by=(
            "auto_client_acquisition/agent_os/agent_registry.py",
            "auto_client_acquisition/secure_agent_runtime_os/four_boundaries.py",
        ),
    ),
    NonNegotiable(
        id="no_project_without_proof_pack",
        title_en="No project without a Proof Pack",
        title_ar="لا مشروع بلا Proof Pack",
        promise_en=(
            "Every closed engagement assembles a 14-section Proof Pack with a "
            "computed proof score. You receive a signed, exportable PDF before "
            "the engagement is invoiced as complete."
        ),
        promise_ar=(
            "كل ارتباط مغلق يجمّع Proof Pack من ١٤ قسماً مع نقاط إثبات محسوبة. "
            "تستلم PDF موقّعاً قابلاً للتصدير قبل تَسجيل الارتباط كمكتمل."
        ),
        refusal_en=(
            "We do not close a project without assembling a Proof Pack. "
            "Projects without a Proof Pack cannot be invoiced, cannot be "
            "referenced in case studies, and cannot trigger retainer eligibility."
        ),
        refusal_ar=(
            "لا نغلق مشروعاً بدون Proof Pack. المشاريع بدون Proof Pack لا "
            "يمكن إصدار فاتورة لها، لا يمكن الاستشهاد بها في حالات، ولا تفعّل "
            "أهلية الريتينر."
        ),
        enforced_by=(
            "tests/test_proof_pack_required.py",
            "auto_client_acquisition/proof_os/proof_pack.py",
        ),
    ),
    NonNegotiable(
        id="no_project_without_capital_asset",
        title_en="No project without a Capital Asset",
        title_ar="لا مشروع بلا أصل رأسمالي",
        promise_en=(
            "Every closed engagement deposits at least one reusable Capital "
            "Asset — a scoring rule, draft template, governance rule, sector "
            "insight, productization signal, or proof example. The next "
            "engagement starts ahead because of yours."
        ),
        promise_ar=(
            "كل ارتباط مغلق يودع أصلاً رأسمالياً واحداً على الأقل قابلاً لإعادة "
            "الاستخدام — قاعدة تسجيل، قالب مسودة، قاعدة حوكمة، insight قطاع، "
            "إشارة منتَج، أو نموذج إثبات. الارتباط القادم يبدأ متقدّماً بسبب ارتباطك."
        ),
        refusal_en=(
            "We do not close a project without depositing at least one "
            "Capital Asset. Zero-capital projects are flagged in the weekly "
            "capital review as a productization failure, not a delivery success."
        ),
        refusal_ar=(
            "لا نغلق مشروعاً بدون إيداع أصل رأسمالي واحد على الأقل. مشاريع "
            "صفر-رأسمال تُرفع في مراجعة الأصول الأسبوعيّة كإخفاق في الإنتاج، "
            "لا كنجاح في التسليم."
        ),
        enforced_by=("auto_client_acquisition/capital_os/capital_ledger.py",),
    ),
)


def list_non_negotiables() -> tuple[NonNegotiable, ...]:
    """Return all 11 non-negotiables in canonical order."""
    return NON_NEGOTIABLES


def get_non_negotiable(id_: str) -> NonNegotiable | None:
    for n in NON_NEGOTIABLES:
        if n.id == id_:
            return n
    return None


__all__ = [
    "NonNegotiable",
    "NON_NEGOTIABLES",
    "list_non_negotiables",
    "get_non_negotiable",
]
