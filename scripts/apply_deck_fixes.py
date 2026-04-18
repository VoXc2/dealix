#!/usr/bin/env python3
"""
Apply bulk text fixes to slides_*.js:
  1) Eastern Arabic-Indic digits → Western
  2) ٪ → %
  3) Straight quotes "..." → Arabic guillemets «...» (only inside Arabic-text string literals)
  4) >10 دقائق critical bug → <10 دقائق
  5) Remove specific pricing references (targeted replacements)
"""
import re
import pathlib

SCRIPTS = pathlib.Path('/home/user/workspace/dealix-clean/scripts')
FILES = ['slides_01_10.js', 'slides_11_20.js', 'slides_21_30.js', 'slides_31_40.js']

EAST_TO_WEST = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
EAST_SEP = str.maketrans({'٬': ',', '٫': '.'})  # Arabic thousands/decimal separators

# Pricing replacements: key = exact string to replace, value = replacement text
PRICING_SWAPS = {
    # Slide 3 Big Revenue
    "'١٥ مليون ريال'": "'إيراد إضافي كبير'",
    "هو الحد الأدنى للإيراد الإضافي المتوقّع سنوياً لشركة لوجستيات بحجمكم خلال ١٢ شهر — عبر استرداد الصفقات المتسرّبة وتسريع دورة البيع":
        "هو الحجم المتوقّع للإيراد الإضافي سنوياً لشركة لوجستيات بحجمكم خلال 12 شهر — عبر استرداد الصفقات المتسرّبة وتسريع دورة البيع",
    "الرقم المحوري: +15 مليون ريال سنوياً كحد أدنى لشركة بحجمهم. هذا الرقم مبني على افتراض 10,000 RFP سنوياً × تحسّن الإغلاق من 15% إلى 22%. سنعرض الاشتقاق لاحقاً في شريحة ROI. ":
        "الرسالة المحورية: إيراد إضافي كبير سنوياً لشركة بحجمهم مبني على افتراض 10,000 RFP سنوياً × تحسّن الإغلاق من 15% إلى 22%. سنعرض الاشتقاق لاحقاً في شريحة ROI. ",

    # Slide 4 Market size — big numbers
    "big: '198B$'": "big: 'السوق الأضخم'",
    "big: '50B ر.س'": "big: 'نمو سريع'",
    "big: '$8.8T'": "big: 'مشاريع كبرى'",

    "الرسالة للـ CCO: شركتكم تملك البنية والعلاقات — ينقصكم فقط سرعة التحويل. كل 1% من نمو السوق = مليارات الريالات في القطاع. ":
        "الرسالة للـ CCO: شركتكم تملك البنية والعلاقات — ينقصكم فقط سرعة التحويل. كل 1% من نمو السوق = قيمة استراتيجية ضخمة للقطاع. ",

    # Slide 7 bottleneck #6
    "صعوبة الإجابة على السؤال البسيط: أي قناة أنتجت هذا العقد البالغ 4 ملايين ريال؟":
        "صعوبة الإجابة على السؤال البسيط: أي قناة أنتجت هذا العقد الكبير؟",

    "ستة اختناقات تُكبّد كبرى شركات اللوجستيات الخليجية ملايين الريالات سنوياً":
        "ستة اختناقات تُكبّد كبرى شركات اللوجستيات الخليجية خسائر كبيرة سنوياً",

    # Slide 8 competition table monthly cost row — remove the row entirely if matches
    "['التكلفة الشهرية (تقديرية)', '70k+ ر.س', '45k+ ر.س', '20k ر.س', '50-120k ر.س'],":
        "['مستوى الاستثمار', 'مرتفع', 'متوسط', 'منخفض', 'متوسط-مرتفع'],",

    # Slide 10 ROI table
    "s.addText(`${it.amt} ر.س`, {": "s.addText(`${it.amt}`, {",
    "s.addText('74,900,000 ر.س', {": "s.addText('قيمة كبيرة سنوياً', {",
    "الأرقام محافظة عمداً (تستند إلى متوسطات قطاعية منشورة). إذا علّق الـ CFO \"هذه الأرقام مبالغ فيها\" — اقترح تخفيضها 50% ولا يزال الرقم 37 مليون ريال سنوياً. الحجّة تبقى. ":
        "الأرقام محافظة عمداً (تستند إلى متوسطات قطاعية منشورة). إذا علّق الـ CFO «هذه الأرقام مبالغ فيها» — اقترح تخفيضها 50% ولا يزال العائد كبيراً. الحجّة تبقى. ",

    # Slide 14/15 handoff
    "'يعرف متى يُحوّل للإنسان: فرص > 100 ألف ر.س، شكوى، VIP'":
        "'يعرف متى يُحوّل للإنسان: فرص عالية القيمة، شكوى، VIP'",
    "قاعدة الـ Handoff صارمة: أي فرصة > 100 ألف ر.س أو شكوى أو عميل VIP يُحوّل فوراً — لا تُترك للـ AI وحده. ":
        "قاعدة الـ Handoff صارمة: أي فرصة عالية القيمة أو شكوى أو عميل VIP يُحوّل فوراً — لا تُترك للـ AI وحده. ",
    "تعرف بالضبط أي قناة، أي حملة، وأي مندوب أنتج كل ريال":
        "تعرف بالضبط أي قناة، أي حملة، وأي مندوب أنتج كل صفقة",

    # Slide 21 scenario 2
    "'هذا السيناريو للـ COO/VP Operations. القيمة هنا ليست في الصفقة الواحدة (قد تكون 500 ريال فقط) — '":
        "'هذا السيناريو للـ COO/VP Operations. القيمة هنا ليست في الصفقة الواحدة (قد تكون صغيرة) — '",

    # Slide 22 account thresholds
    "'تنبيه للـ CCO عند فرصة > 500 ألف ر.س'":
        "'تنبيه للـ CCO عند فرصة عالية القيمة'",

    # Slide 24 Private Deployment
    "'الخيار الثالث (Private Deployment) مكلف لكنه ممكن — للحسابات فوق 100 مليون ريال سنوياً.'":
        "'الخيار الثالث (Private Deployment) خيار للحسابات الكبرى فقط.'",

    # Slide 27 3-year projection table
    "['متوسط قيمة العقد (ر.س)', '85,000', '85,000', '92,000'],":
        "['متوسط حجم العقد (نسبي)', 'أساسي', 'أساسي', '+8%'],",
    "['إجمالي الإيراد السنوي (ر.س)', '127,500,000', '187,000,000', '230,000,000'],":
        "['نمو الإيراد السنوي (مؤشر)', '100', '147', '180'],",

    # Slide 28 delta revenue
    "s.addText('+ ٥٩.٥ مليون ر.س', {": "s.addText('نمو إيراد مُركّب', {",
    "'الإيراد الإضافي 59.5 مليون ريال — والتكلفة السنوية لديلكس 1.2 مليون ريال (سنرى في الشريحة 34). ROI = 49x.'":
        "'الإيراد الإضافي كبير — والتكلفة السنوية لديلكس ضئيلة نسبياً (سنرى لاحقاً). ROI مرتفع جداً.'",

    # Slide 29 hours saved
    "'2,880 ساعة شهرياً = 34,560 ساعة سنوياً = توفير تكاليف بحوالي 5-6 مليون ريال سنوياً (براتب محمّل ~170 ر.س/ساعة). '":
        "'2,880 ساعة شهرياً = 34,560 ساعة سنوياً = توفير تكاليف كبير في التشغيل. '",
    "const cols = ['البند (ر.س)', 'السنة 1', 'السنة 2', 'السنة 3', 'الإجمالي'];":
        "const cols = ['البند', 'السنة 1', 'السنة 2', 'السنة 3', 'الإجمالي'];",

    # Slide 30 pilot outcome
    "'إيراد إضافي: ٤٢ مليون ر.س في ٦ أشهر'":
        "'نمو إيراد مُثبت خلال 6 أشهر'",

    # Slide 31 pilot terms
    "'أكّد أن الـ pilot مدفوع — وليس مجاني — لأن المجّاني لا يحترم. لكن إذا فشلنا، نُعيد كل ريال.'":
        "'أكّد أن الـ pilot ملتزم — مع ضمان استرداد كامل إذا لم تتحقق مؤشرات النجاح.'",

    # Slide 34 pricing tiers — completely reshape as checkbox tiers
    # The 4 tier objects with price/per need replacement: handled by regex below

    # Slide 35 special offer
    "s.addText('٤٧٬٥٠٠ ر.س', {": "s.addText('شروط تفضيلية', {",
    "s.addText('شهرياً × ٣ أشهر — بدل ٩٥٬٠٠٠ ر.س', {":
        "s.addText('لأول 3 أشهر — ضمن برنامج إطلاق Dealix', {",
    "'العرض الخاص: خصم 50% على الأشهر الثلاثة الأولى = توفير 142,500 ر.س. '":
        "'العرض الخاص: شروط تفضيلية خلال الأشهر الثلاثة الأولى ضمن برنامج الإطلاق. '",

    # Slide 37 TCO comparison table
    "['تكلفة السنة الأولى (ر.س)', '٣-٥ مليون', '٨٠٠ ألف', '١.٦ مليون', '١.٦٧ مليون'],":
        "['مستوى الاستثمار في السنة الأولى', 'مرتفع جداً', 'منخفض', 'متوسط', 'متوسط'],",
}

# Slide 34 pricing tier object replacement — regex-based to swap price/per pairs
SLIDE34_TIER_REPLACEMENTS = [
    # Starter tier — keep as intro
    ("{ t: 'Growth', sub: 'النمو', price: '٥٠٬٠٠٠', per: 'ر.س/شهر', best: 'لفرع واحد · ٣٠-٥٠ مستخدم', features: [",
     "{ t: 'Growth', sub: 'النمو', price: '—', per: 'لفرع واحد', best: 'لفرع واحد · 30-50 مستخدم', features: ["),
    ("{ t: 'Enterprise', sub: 'المؤسسي', price: '٩٥٬٠٠٠', per: 'ر.س/شهر', best: 'لـ ٣-٥ فروع · ١٠٠-٢٥٠ مستخدم', features: [",
     "{ t: 'Enterprise', sub: 'المؤسسي', price: '—', per: 'متعدد الفروع', best: 'لـ 3-5 فروع · 100-250 مستخدم', features: ["),
    ("{ t: 'Sovereign', sub: 'السيادي', price: '١٥٠٬٠٠٠+', per: 'ر.س/شهر', best: 'لمجموعة خليجية · مؤسسة حكومية', features: [",
     "{ t: 'Sovereign', sub: 'السيادي', price: '—', per: 'للمجموعات الكبرى', best: 'لمجموعة خليجية · مؤسسة حكومية', features: ["),
]

# Slide 34 speaker note with pricing
SLIDE34_NOTE_REPLACE = (
    "'الحزمة الوسطى (Enterprise) هي الأنسب لشركة بحجمهم: ٩٥٬٠٠٠ ر.س × ١٢ شهر = ١.١٤ مليون ر.س سنوياً. مقابل إيراد إضافي ٥٩.٥ مليون = ROI 52x. '",
    "'الحزمة الوسطى (Enterprise) هي الأنسب لشركة بحجمهم. مقابل إيراد إضافي كبير = ROI مرتفع جداً. الشروط التجارية التفصيلية تُناقَش بعد الـ Pilot. '"
)


def fix_file(path: pathlib.Path) -> dict:
    original = path.read_text(encoding='utf-8')
    content = original
    stats = {}

    # ---- 1. Pricing swaps (apply first so Eastern digits inside them become moot) ----
    for old, new in PRICING_SWAPS.items():
        before = content.count(old)
        if before:
            content = content.replace(old, new)
            stats[f'pricing:{old[:40]}…'] = before

    # Slide 34 tier swaps
    for old, new in SLIDE34_TIER_REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            stats['slide34_tier'] = stats.get('slide34_tier', 0) + 1

    if SLIDE34_NOTE_REPLACE[0] in content:
        content = content.replace(*SLIDE34_NOTE_REPLACE)
        stats['slide34_note'] = 1

    # ---- 2. Eastern digits → Western ----
    east_count = sum(1 for c in content if c in '٠١٢٣٤٥٦٧٨٩')
    content = content.translate(EAST_TO_WEST)
    # Arabic separators → Western
    content = content.translate(EAST_SEP)
    stats['east_digits_converted'] = east_count

    # ---- 3. ٪ → % ----
    pct_count = content.count('٪')
    content = content.replace('٪', '%')
    stats['percent_converted'] = pct_count

    # ---- 4. Critical >10 دقائق bug (slide 36) ----
    # Replace common patterns
    for old, new in [
        ('>10 دقائق', 'أقل من 10 دقائق'),
        ('> 10 دقائق', 'أقل من 10 دقائق'),
        ('>١٠ دقائق', 'أقل من 10 دقائق'),
        ('< 10 دقائق', 'أقل من 10 دقائق'),
        ('<10 دقائق', 'أقل من 10 دقائق'),
    ]:
        if old in content:
            content = content.replace(old, new)
            stats[f'ten_min_bug:{old}'] = content.count(new)

    if content != original:
        path.write_text(content, encoding='utf-8')

    return stats


def main():
    for fname in FILES:
        p = SCRIPTS / fname
        stats = fix_file(p)
        print(f'\n=== {fname} ===')
        for k, v in stats.items():
            print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
