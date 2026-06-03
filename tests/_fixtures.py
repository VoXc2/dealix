"""Shared fixtures/builders for safety tests."""


def good_cold_email():
    """A personalized (>=P1), claim-free cold email with an unsubscribe path."""
    return {
        "company": "Digital Rise Agency",
        "decision_maker": "Founder / CEO",
        "pain": "Leads not converting",
        "subject": "فرص Digital Rise Agency بعد أول رد",
        "body": (
            "السلام عليكم Founder،\n"
            "لاحظت أن Digital Rise Agency تستقبل عملاء محتملين لكن Leads not converting "
            "بسبب بطء المتابعة وعدم وضوح المسار.\n"
            "نحن في Dealix نساعد وكالات التسويق على تحسين التحويل خلال 5 أيام عبر "
            "Revenue Intelligence Sprint.\n"
            "هل يناسبك أرسل لك مثال مختصر على التقرير؟\n\n"
            "لإلغاء الاشتراك: أرسل كلمة إيقاف."
        ),
    }


def generic_bad_draft():
    """An un-personalized (P0) draft with an unresolved placeholder, no opt-out."""
    return {
        "subject": "عرض خاص",
        "body": "السلام عليكم [الاسم]، عندنا عرض. تواصل معنا الحين.",
    }


PRODUCT_CATALOG = [
    {"id": "P1_SPRINT", "name": "Revenue Intelligence Sprint"},
    {"id": "P2_RETAINER", "name": "AI Sales Ops Retainer"},
]
