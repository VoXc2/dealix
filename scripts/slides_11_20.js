/* Slides 11-20: Product detail + scenario tailoring */
const lib = require('./build_logistics_pitch.js');
const { pres, C, FH, FB, FS, W, H, SCREENSHOTS, lightBg, darkBg, lightFrame, darkFrame, titleAR, subtitleAR, sourceFooter } = lib;
const path = require('path');

// Helper: screenshot slide layout (left = screenshot, right = Arabic explainer)
function screenshotSlide(s, opts) {
  // In RTL context, visual primary (screenshot) on LEFT, text on RIGHT
  const imgX = 0.6;
  const imgY = 2.5;
  const imgW = 7.2;
  const imgH = 4.2;

  // Screenshot frame/shadow
  s.addShape('rect', { x: imgX - 0.05, y: imgY - 0.05, w: imgW + 0.1, h: imgH + 0.1, fill: { color: C.navy }, line: { type: 'none' } });
  s.addImage({ path: opts.img, x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: 'contain', w: imgW, h: imgH } });

  // Caption below screenshot
  s.addText(opts.caption, {
    x: imgX, y: imgY + imgH + 0.08, w: imgW, h: 0.3,
    fontFace: FB, fontSize: 10, italic: true, color: C.textFaint, align: 'left',
  });

  // Right column — Arabic
  const tX = imgX + imgW + 0.3;
  const tW = W - tX - 0.6;

  s.addText(opts.tag, {
    x: tX, y: 2.55, w: tW, h: 0.35,
    fontFace: FH, fontSize: 11, bold: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addText(opts.h, {
    x: tX, y: 2.9, w: tW, h: 0.7,
    fontFace: FH, fontSize: 22, bold: true, color: C.navy, align: 'right', rtlMode: true,
  });
  s.addShape('rect', { x: tX + tW - 0.6, y: 3.65, w: 0.5, h: 0.03, fill: { color: C.gold }, line: { type: 'none' } });

  // Bullet list (without bullets — clean)
  // Dynamically size so up to 7 bullets fit safely above source footer (y ~ 6.75)
  const bulletsY = 3.75;
  const bulletsBottom = 6.3; // last bullet top must be <= this; footer sits at 6.75
  const n = opts.bullets.length;
  const step = n > 1 ? Math.min(0.45, (bulletsBottom - bulletsY) / (n - 1)) : 0.45;
  opts.bullets.forEach((b, i) => {
    const y = bulletsY + i * step;
    // dash marker
    s.addText('—', {
      x: tX + tW - 0.3, y, w: 0.25, h: 0.4,
      fontFace: FB, fontSize: 11, color: C.gold, align: 'right', valign: 'top',
    });
    s.addText(b, {
      x: tX, y, w: tW - 0.4, h: step + 0.05,
      fontFace: FB, fontSize: 11, color: C.text, align: 'right', rtlMode: true, valign: 'top',
    });
  });
}

// =================== SLIDE 11 — LEAD INTELLIGENCE ENGINE V2 ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 1', 11);

  titleAR(s, 'محرك استخبارات العملاء V2');
  subtitleAR(s, 'Lead Intelligence Engine — الركيزة الأولى: اكتشاف + تأهيل آلي من أكثر من 8 مصادر محلية وخليجية');

  screenshotSlide(s, {
    img: path.join(SCREENSHOTS, 'v2-overview.png'),
    caption: 'Dealix Dashboard — Lead Intelligence Overview',
    tag: 'INTELLIGENCE · الاكتشاف',
    h: 'ثمانية مصادر · لغتان · خليج واحد',
    bullets: [
      'اتاق (Etimad) · منصة المنافسات الحكومية السعودية — تنبيهات RFP فورية',
      'LinkedIn Sales Navigator + بوابات المناقصات الخليجية (DEWA · ADDED · MPW)',
      'WhatsApp Business API · نماذج الموقع · Google Forms',
      'Salla · Zid · Foodics · Odoo — توريد العملاء التجار',
      'تحليل NLP عربي — يفهم "شحن ثلّاجي" و"مناولة" و"نقل أسطول"',
      'تسجيل تلقائي من 0—100 حسب حجم الفرصة، الاستعجال، والاحتمالية',
      'توزيع فوري على المندوب المناسب حسب المدينة والقطاع والخبرة',
    ],
  });

  sourceFooter(s, [
    { name: 'Dealix Product Specs', url: 'https://dealix.io/lead-intelligence' },
    { name: 'Etimad', url: 'https://etimad.sa/' },
  ]);

  s.addNotes(
    'هذه أول شريحة منتج — وهي قلب ديلكس. محرك استخبارات العملاء هو ما يميّزنا عن كل منافس. ' +
    'أكّد على مصدر "اتاق" (Etimad) — الشركات العالمية لا تستطيع الوصول إليه. ديلكس يُراقب كل مناقصة حكومية دقيقة بدقيقة. ' +
    'التسجيل من 0—100 يعتمد على 40+ متغيّر: حجم الشركة، تاريخ المعاملات، الاستعجال، المنطقة، القطاع. ' +
    'لقطة الشاشة معروضة حيّاً من بيئة العرض — يمكن للفريق الفني رؤيتها مباشرة في جلسة التجربة.'
  );
})();

// =================== SLIDE 12 — OMNICHANNEL ENGAGEMENT ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 2', 12);

  titleAR(s, 'تواصل متعدد القنوات');
  subtitleAR(s, 'Omnichannel Engagement — كل القنوات في صندوق وارد موحّد، مع سياق كامل لكل عميل');

  screenshotSlide(s, {
    img: path.join(SCREENSHOTS, 'screenshot-inbox.png'),
    caption: 'Unified Inbox — WhatsApp · SMS · Email · LinkedIn · Voice',
    tag: 'ENGAGEMENT · التواصل',
    h: 'صندوق وارد واحد لكل فروعكم',
    bullets: [
      'WhatsApp Business API أصلي (ليس عبر وسيط) — توثيق رسمي من Meta',
      'SMS عبر Twilio / Unifonic مع تتبّع التسليم والقراءة',
      'Email Threading ذكي — يفهم تسلسل المحادثة حتى لو تغيّر الموضوع',
      'LinkedIn InMail + Voice Drop — للعملاء على المستوى التنفيذي',
      'مكالمات صوتية مسجّلة مع تحويل الكلام إلى نص عربي',
      'تبديل قناة دون فقد السياق — العميل يبدأ على WhatsApp وينتقل لـ Email',
      'Templates معتمدة ومحدّثة — بالعربية الفصحى واللهجة السعودية',
    ],
  });

  sourceFooter(s, [
    { name: 'Meta WhatsApp Business API', url: 'https://business.whatsapp.com/products/business-platform' },
    { name: 'Twilio Docs', url: 'https://www.twilio.com/docs' },
  ]);

  s.addNotes(
    'قضيّة WhatsApp الأصلي مهمة: معظم المنافسين يستخدمون wrappers بطيئة وعرضة للحظر. ديلكس شريك رسمي معتمد. ' +
    'اذكر أن "تبديل القناة دون فقد السياق" يحل مشكلة قطاعية — العميل يتحدث على WhatsApp صباحاً، ويطلب إيميل رسمي عصراً، والمندوب الجديد يرى كل شيء. ' +
    'رسالة حاسمة: فريق مبيعاتكم سيتوقف عن تبديل 5 تطبيقات في اليوم — كل شيء في مكان واحد. هذا وحده يوفّر 90 دقيقة يومياً لكل مندوب.'
  );
})();

// =================== SLIDE 13 — AI CONVERSATION AGENT ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 3', 13);

  titleAR(s, 'وكيل المحادثة بالذكاء الاصطناعي');
  subtitleAR(s, 'AI Agent بلهجة سعودية — يفهم، يفاوض، ويحوّل للإنسان في اللحظة الصحيحة');

  screenshotSlide(s, {
    img: path.join(SCREENSHOTS, 'screenshot-agents.png'),
    caption: 'Dealix AI Agents — Arabic Conversation Engine',
    tag: 'INTELLIGENCE · الذكاء',
    h: 'يتحدث عربي · يفهم السياق · يحترم الحدود',
    bullets: [
      'نموذج لغوي مدرّب على لهجات الخليج (سعودي · إماراتي · كويتي)',
      'يفهم المصطلحات اللوجستية: "FTL" · "LTL" · "كروس دوك" · "تكوين حمولة"',
      'يتفاوض على السعر ضمن نطاق معتمد مسبقاً — مع تسجيل كامل',
      'يعرف متى يُحوّل للإنسان: فرص عالية القيمة، شكوى، VIP',
      'Handoff سلس — المندوب يرى كامل المحادثة + ملخّص AI',
      'يعمل 24/7 — يستقبل RFP في منتصف الليل ويُؤهّله حتى الصباح',
      'حدود صارمة: لا يُوقّع عقداً ولا يُلزم الشركة دون تأكيد بشري',
    ],
  });

  sourceFooter(s, [
    { name: 'Dealix AI Specs', url: 'https://dealix.io/ai-agent' },
    { name: 'NIST AI RMF', url: 'https://www.nist.gov/itl/ai-risk-management-framework' },
  ]);

  s.addNotes(
    'إذا كان في الغرفة CTO — توقّف هنا وأبرز الضوابط (Guardrails). نحن لا نستبدل المندوب، نحن نضاعف قدرته. ' +
    'اللهجة السعودية نقطة حساسة: الأنظمة الدولية ترد بعربية فصحى جامدة، عملاؤكم يتحدثون لهجة — ديلكس مدرّب على المحادثات الفعلية. ' +
    'قاعدة الـ Handoff صارمة: أي فرصة عالية القيمة أو شكوى أو عميل VIP يُحوّل فوراً — لا تُترك للـ AI وحده. ' +
    'اذكر التزامنا بإطار NIST AI RMF — هذا ليس تسويقاً، هذا التزام موثّق (بوابات الحوكمة الثمانية).'
  );
})();

// =================== SLIDE 14 — PIPELINE + CRM ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 4', 14);

  titleAR(s, 'خط المبيعات وإدارة العلاقات');
  subtitleAR(s, 'Pipeline CRM بصري — سحب وإفلات، مراحل مخصصة لكل قطاع (حكومي · أرامكو · تجزئة · تجار إلكتروني)');

  screenshotSlide(s, {
    img: path.join(SCREENSHOTS, 'screenshot-pipeline.png'),
    caption: 'Dealix Pipeline — Drag & Drop, Multi-Vertical Stages',
    tag: 'EXECUTION · التنفيذ',
    h: 'خط مبيعات يعكس واقع اللوجستيات',
    bullets: [
      'مراحل مخصصة لكل قطاع — تندر حكومي ≠ طلب تاجر ≠ عقد أرامكو',
      'حقول غنية: حجم الحمولة، نوع البضاعة، المنطقة، مستوى الاستعجال',
      'Workflow آلي: كل مرحلة تُشغّل إجراء (إرسال عرض، حجز مراجعة، تصعيد)',
      'توقّعات إيراد أسبوعية بدقة > 85% (مبنية على بيانات 12 شهر)',
      'تاريخ كامل لكل عميل: تواصل، عروض، تندرات سابقة، نتائج',
      'Notes تنفيذية خاصة بالمدير العام — لا يراها المندوب',
      'تصدير تلقائي إلى Excel / Power BI للإدارة العليا',
    ],
  });

  s.addNotes(
    'هذه الشريحة للـ VP Sales. رسالتها: ديلكس ليس CRM ثابت — هو قالب قابل للتشكيل حسب كل قطاع من قطاعاتكم. ' +
    'التوقّعات الإيرادية بدقة > 85% هي ميزة مفقودة تماماً في Salesforce المحلي. ' +
    'اذكر أن "مراحل مخصصة لكل قطاع" يعني أن فريق التندرات الحكومية يرى pipeline مختلفاً عن فريق التاجر الإلكتروني — رغم أنهم في نفس المنصة.'
  );
})();

// =================== SLIDE 15 — ANALYTICS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 5', 15);

  titleAR(s, 'تحليلات وإسناد الإيراد');
  subtitleAR(s, 'Analytics & Revenue Attribution — تعرف بالضبط أي قناة، أي حملة، وأي مندوب أنتج كل صفقة');

  screenshotSlide(s, {
    img: path.join(SCREENSHOTS, 'screenshot-analytics.png'),
    caption: 'Dealix Analytics — Executive Dashboard',
    tag: 'ANALYTICS · التحليل',
    h: 'من السؤال الصعب إلى الإجابة في 30 ثانية',
    bullets: [
      'لوحة تنفيذية للمدير العام — تحديث مباشر، بدون انتظار IT',
      'إسناد متعدد اللمسات — العميل رأى LinkedIn، تحدّث WhatsApp، أغلق Email',
      'مقارنة أداء الفروع: الرياض · جدة · الدمام · دبي · الكويت',
      'تحليل قطاعي: أي قطاع يُحقق أعلى هامش (حكومي · بتروكيماوي · تجزئة)',
      'معدّلات التحويل لكل مرحلة — تكتشف الاختناق قبل أن يكلّفك',
      'Cohort Analysis: كم عقد جديد مقابل كم تجديد — صحّة الإيراد',
      'تصدير تنفيذي بضغطة واحدة — PDF أنيق جاهز لمجلس الإدارة',
    ],
  });

  sourceFooter(s, [
    { name: 'Dealix Analytics', url: 'https://dealix.io/analytics' },
  ]);

  s.addNotes(
    'اذكر قصة عملية: الـ CEO الذي سُئل في مجلس الإدارة "كم تكلفتنا في اكتساب عميل حكومي؟" — استغرق فريقه أسبوعين للإجابة. ' +
    'مع ديلكس: الإجابة في 30 ثانية، مع التحليل القطاعي والجغرافي. ' +
    'الـ Cohort Analysis تكشف سراً خطيراً: الشركات تُكافئ المندوبين على عقود جديدة بينما 65% من الإيراد من التجديد — ديلكس يُظهر هذا بوضوح.'
  );
})();

// =================== SLIDE 16 — MULTI-TENANT / GULF EXPANSION ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 6', 16);

  titleAR(s, 'تعدد الفروع والتوسّع الخليجي');
  subtitleAR(s, 'Multi-Tenant Architecture — كل فرع يعمل باستقلالية، مع لوحة موحّدة للإدارة');

  const cx = W / 2;
  const cy = 4.7;
  // Center HQ — rectangle for cleaner text layout
  s.addShape('rect', { x: cx - 1.3, y: cy - 0.65, w: 2.6, h: 1.3, fill: { color: C.navy }, line: { color: C.gold, width: 2 } });
  s.addText('المقر الرئيسي', {
    x: cx - 1.3, y: cy - 0.55, w: 2.6, h: 0.4,
    fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'center', rtlMode: true,
  });
  s.addText('Executive Dashboard', {
    x: cx - 1.3, y: cy - 0.15, w: 2.6, h: 0.3,
    fontFace: FH, fontSize: 10, color: C.onDarkMuted, align: 'center',
  });
  s.addText('رؤية موحّدة · صلاحيات دقيقة', {
    x: cx - 1.3, y: cy + 0.2, w: 2.6, h: 0.3,
    fontFace: FB, fontSize: 9, color: C.onDarkMuted, align: 'center', rtlMode: true,
  });

  // Branches — arranged in 2 columns left and right of HQ (horizontal layout)
  // Left side (3): top, mid, bottom
  // Right side (3): top, mid, bottom
  const branches = [
    { name: 'الرياض', sub: 'Riyadh · HQ Ops', side: 'R', row: 0 },
    { name: 'جدة', sub: 'Jeddah · Red Sea', side: 'R', row: 1 },
    { name: 'الدمام', sub: 'Dammam · Eastern', side: 'R', row: 2 },
    { name: 'دبي', sub: 'Dubai · UAE', side: 'L', row: 0 },
    { name: 'الكويت', sub: 'Kuwait · Gulf', side: 'L', row: 1 },
    { name: 'الدوحة', sub: 'Doha · Qatar', side: 'L', row: 2 },
  ];
  const bW = 1.9;
  const bH = 0.85;
  const rowYs = [3.5, 4.65, 5.8];
  const rightX = cx + 1.55;
  const leftX = cx - 1.55 - bW;
  branches.forEach(b => {
    const by = rowYs[b.row];
    const bx = b.side === 'R' ? rightX : leftX;
    // connector line from HQ to branch
    const hqEdgeX = b.side === 'R' ? cx + 1.3 : cx - 1.3;
    const branchEdgeX = b.side === 'R' ? bx : bx + bW;
    const lineStartX = Math.min(hqEdgeX, branchEdgeX);
    const lineW = Math.abs(hqEdgeX - branchEdgeX);
    s.addShape('line', {
      x: lineStartX, y: by + bH / 2, w: lineW, h: 0,
      line: { color: C.gold, width: 1, dashType: 'dash' },
    });
    // branch card
    s.addShape('rect', { x: bx, y: by, w: bW, h: bH, fill: { color: 'FFFFFF' }, line: { color: C.gold, width: 1 } });
    s.addText(b.name, {
      x: bx, y: by + 0.08, w: bW, h: 0.38,
      fontFace: FH, fontSize: 14, bold: true, color: C.navy, align: 'center', rtlMode: true,
    });
    s.addText(b.sub, {
      x: bx, y: by + 0.46, w: bW, h: 0.3,
      fontFace: FB, fontSize: 9, color: C.textMuted, align: 'center',
    });
  });

  // Bottom description
  s.addText('كل فرع يملك بياناته · لوحته · فريقه — لكن الإدارة العليا تملك المشهد الكامل بضغطة واحدة', {
    x: 0.6, y: 6.8, w: W - 1.2, h: 0.35,
    fontFace: FS, fontSize: 13, italic: true, color: C.text, align: 'center', rtlMode: true,
  });

  s.addNotes(
    'هذه الشريحة حاسمة للـ Regional GM. رسالتها: حكومة البيانات على الفرع، حوكمة الأداء على المقر. ' +
    'التحدي الحالي: شركة لوجستيات بخمسة فروع = خمسة أنظمة = خمس حقائق مختلفة. ديلكس يحلّ هذا دون كسر استقلالية الفرع. ' +
    'اذكر أن كل فرع يمكنه تخصيص اللغة (سعودي/إماراتي/كويتي)، العملة، مراحل Pipeline — لكن البيانات تتجمّع تلقائياً لوحة المقر.'
  );
})();

// =================== SLIDE 17 — COMPLIANCE ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · ركيزة 7', 17);

  titleAR(s, 'الامتثال والحوكمة');
  subtitleAR(s, 'مصمّم على PDPL · SAMA · ZATCA · NIST AI RMF — ليس مُضافاً لاحقاً');

  // 4 compliance cards
  const comps = [
    { code: 'PDPL', t: 'نظام حماية البيانات الشخصية', d: 'تصنيف تلقائي للبيانات الحساسة · تشفير في الطبقات الثلاث · حق النسيان · تصدير موثّق', color: C.navy },
    { code: 'SAMA', t: 'مؤسسة النقد العربي السعودي', d: 'تصميم متوافق مع إطار الأمن السيبراني لـ SAMA · سجلات تدقيق كاملة · فصل الأدوار', color: C.navy },
    { code: 'ZATCA', t: 'الزكاة والضريبة والجمارك', d: 'تكامل مع الفوترة الإلكترونية (Phase 2) · ربط آلي مع ERP · توافق تام', color: C.navy },
    { code: '8 Gates', t: 'NIST AI Risk Management', d: 'ثماني بوابات حوكمة للذكاء الاصطناعي · شفافية كاملة · قابلية التفسير · اختبار الانحياز', color: C.navy },
  ];
  const cW = (W - 1.2 - 0.3 * 3) / 4;
  const cY = 2.6;
  comps.forEach((c, i) => {
    const x = W - 0.6 - (i + 1) * cW - i * 0.3;
    s.addShape('rect', { x, y: cY, w: cW, h: 3.2, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addShape('rect', { x, y: cY, w: cW, h: 0.55, fill: { color: c.color }, line: { type: 'none' } });
    s.addText(c.code, {
      x: x + 0.1, y: cY + 0.08, w: cW - 0.2, h: 0.4,
      fontFace: FH, fontSize: 18, bold: true, color: C.gold, align: 'center',
    });
    s.addText(c.t, {
      x: x + 0.15, y: cY + 0.75, w: cW - 0.3, h: 0.8,
      fontFace: FH, fontSize: 12, bold: true, color: C.navy, align: 'right', rtlMode: true, valign: 'top',
    });
    s.addShape('rect', { x: x + cW - 0.75, y: cY + 1.6, w: 0.5, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(c.d, {
      x: x + 0.15, y: cY + 1.75, w: cW - 0.3, h: 1.35,
      fontFace: FB, fontSize: 10, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  // Bottom strap
  s.addShape('rect', { x: 0.6, y: 6.15, w: W - 1.2, h: 0.6, fill: { color: C.navy }, line: { type: 'none' } });
  s.addShape('rect', { x: W - 0.68, y: 6.15, w: 0.08, h: 0.6, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('استضافة اختيارية داخل المملكة — STC Cloud أو سحابة سيادية معتمدة من NCA', {
    x: 0.8, y: 6.15, w: W - 1.8, h: 0.6,
    fontFace: FB, fontSize: 13, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle', bold: true,
  });

  sourceFooter(s, [
    { name: 'PDPL — Saudi Data Authority', url: 'https://sdaia.gov.sa/ndmo/En/Regulations/PersonalDataProtectionLaw' },
    { name: 'ZATCA E-Invoicing', url: 'https://zatca.gov.sa/en/E-Invoicing' },
    { name: 'NIST AI RMF', url: 'https://www.nist.gov/itl/ai-risk-management-framework' },
  ]);

  s.addNotes(
    'هذه شريحة الـ CISO والـ Chief Risk Officer. ' +
    'النقطة الحاسمة: "مصمّم عليه" وليس "مُضاف لاحقاً" — معظم المنافسين يطلبون PDPL add-on بسعر إضافي. ' +
    'بوابات الـ 8 NIST AI RMF هي تمايز فريد: لا يوجد منافس محلي يلتزم بها، ولا يوجد منافس دولي يعلن عنها للعملاء. ' +
    'خيار الاستضافة داخل المملكة يحلّ مشكلة الـ data residency بشكل نهائي — هذا شرط صارم للعقود الحكومية.'
  );
})();

// =================== SLIDE 18 — INTEGRATIONS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'المنتج · التكاملات', 18);

  titleAR(s, 'منظومة التكاملات');
  subtitleAR(s, 'ديلكس يتكامل مع أنظمتكم الحالية — لا يطلب استبدالها');

  // Grid of integration tiles — 5 columns x 3 rows = 15 logos
  const tiles = [
    'Twilio', 'Unifonic', 'WhatsApp', 'Microsoft 365', 'Google Workspace',
    'Salesforce', 'HubSpot', 'Zoho', 'Odoo', 'SAP',
    'Oracle TM', 'Salla', 'Zid', 'Foodics', 'Stripe',
  ];
  const cols = 5;
  const rows = 3;
  const gx = 0.25, gy = 0.2;
  const tW = (W - 1.2 - (cols - 1) * gx) / cols;
  const tH = 0.95;
  const startY = 2.6;

  tiles.forEach((name, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = W - 0.6 - (col + 1) * tW - col * gx;
    const y = startY + row * (tH + gy);
    s.addShape('rect', { x, y, w: tW, h: tH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(name, {
      x, y, w: tW, h: tH,
      fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'center', valign: 'middle',
    });
    // gold dot
    s.addShape('ellipse', { x: x + 0.15, y: y + 0.15, w: 0.12, h: 0.12, fill: { color: C.gold }, line: { type: 'none' } });
  });

  // Bottom: 3 categories
  s.addText('قنوات · أنظمة CRM و ERP · متاجر إلكترونية و دفع — أكثر من 30 تكاملاً جاهزاً', {
    x: 0.6, y: 6.4, w: W - 1.2, h: 0.4,
    fontFace: FS, fontSize: 13, italic: true, color: C.text, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'اذكر أن ديلكس لا يحاول استبدال SAP أو Oracle — يتكامل معها. ' +
    'Salla و Zid مهمة لأن عملاء اللوجستيات الجدد (الشحن للتجار) يأتون من هذه المنصات. ' +
    'Foodics لشركات التوصيل (Jahez/HungerStation clients). ' +
    'SAP/Oracle TM = شركات اللوجستيات الكبرى تستخدمها كـ TMS. ديلكس = طبقة البيع فوقها.'
  );
})();

// =================== SLIDE 19 — HOW DEALIX SERVES ENTERPRISE ===================
(() => {
  const s = pres.addSlide();
  darkBg(s);
  darkFrame(s, 'خاص بشركتكم', 19);

  titleAR(s, 'كيف يخدم ديلكس شركة لوجستيات بحجمكم', 1.0, { color: C.onDark });
  subtitleAR(s, 'انتقال من المنتج العام إلى خصوصيتكم — خمسة سيناريوهات مصمّمة لواقعكم اليومي', 1.85, { color: C.onDarkMuted });

  // Big framing statement
  s.addShape('rect', { x: 0.6, y: 2.7, w: W - 1.2, h: 1.7, fill: { color: C.navySoft }, line: { color: C.gold, width: 1 } });
  s.addText('"ديلكس ليس منصة للشركات الناشئة — هو بنية تحتية للمؤسسات"', {
    x: 0.9, y: 2.85, w: W - 1.8, h: 0.6,
    fontFace: FS, fontSize: 20, italic: true, color: C.gold, align: 'right', rtlMode: true, bold: true,
  });
  s.addText('معمارية متعددة المستأجرين · عقود SLA من الدرجة الأولى · فريق نجاح مخصّص · تكامل عميق مع أنظمتكم الحالية. ديلكس يعمل بمنطق أن شركة بحجمكم تتعامل مع + 10,000 فرصة سنوياً، وأي احتكاك 1% = خسارة بالملايين.', {
    x: 0.9, y: 3.5, w: W - 1.8, h: 0.85,
    fontFace: FB, fontSize: 14, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
  });

  // Preview of 5 scenarios
  const prev = [
    { n: '1', t: 'أتمتة التندرات والـ RFP' },
    { n: '2', t: 'توزيع طلبات الشحن الفورية' },
    { n: '3', t: 'إدارة الحسابات الرئيسية الخليجية' },
    { n: '4', t: 'خدمات السلسلة الباردة المتخصصة' },
    { n: '5', t: 'ترشيد تجار السلّة وزد' },
  ];
  const pW = (W - 1.2 - 0.2 * 4) / 5;
  prev.forEach((p, i) => {
    const x = W - 0.6 - (i + 1) * pW - i * 0.2;
    const y = 4.9;
    s.addShape('rect', { x, y, w: pW, h: 1.5, fill: { color: C.navyDeep }, line: { color: C.gold, width: 0.5 } });
    s.addText(p.n, {
      x, y: y + 0.2, w: pW, h: 0.5,
      fontFace: FH, fontSize: 28, bold: true, color: C.gold, align: 'center',
    });
    s.addShape('rect', { x: x + pW / 2 - 0.25, y: y + 0.8, w: 0.5, h: 0.02, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(p.t, {
      x: x + 0.1, y: y + 0.9, w: pW - 0.2, h: 0.55,
      fontFace: FB, fontSize: 11, color: C.onDark, align: 'center', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'شريحة انتقال — من المنتج العام إلى "ماذا يعني لي أنا كشركة؟". ' +
    'السيناريوهات الخمسة ستأخذ الشرائح التالية. كلّها مبنية على واقع شركات لوجستيات سعودية حقيقية (بأسماء مجهولة). ' +
    'اذكر أن ديلكس لا يبيع مميزات، بل يحلّ مشاكل محدّدة بأرقام قابلة للقياس.'
  );
})();

// =================== SLIDE 20 — SCENARIO 1: TENDER / RFP ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'سيناريو 1 · التندرات', 20);

  titleAR(s, 'سيناريو 1 — أتمتة التندرات والـ RFP');
  subtitleAR(s, 'من وصول التندر إلى تقديم عرض فني/مالي في أقل من 4 ساعات — بدل 14 يوم');

  // Left column: before/after comparison
  const colW = (W - 1.2 - 0.3) / 2;
  const colY = 2.55;
  const colH = 3.8;

  // AFTER (RTL primary — right)
  const afterX = W - 0.6 - colW;
  s.addShape('rect', { x: afterX, y: colY, w: colW, h: colH, fill: { color: C.navy }, line: { type: 'none' } });
  s.addShape('rect', { x: afterX, y: colY, w: colW, h: 0.5, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('مع ديلكس · بعد', {
    x: afterX, y: colY, w: colW, h: 0.5,
    fontFace: FH, fontSize: 15, bold: true, color: C.navy, align: 'center', rtlMode: true, valign: 'middle',
  });
  const afterSteps = [
    'T+0: التندر يصل من اتاق — استخراج تلقائي لكل المتطلبات',
    'T+15د: تصنيف آلي للفرصة (حجم · منطقة · تخصص) + توزيع على الفريق',
    'T+1س: AI يُعدّ مسودة عرض فني مع سوابق عقود مشابهة',
    'T+2س: مدير التندرات يُراجع ويُعدّل — 20 دقيقة بدل يومين',
    'T+3س: عرض مالي من نموذج معتمد + تحليل هوامش تلقائي',
    'T+4س: الإرسال النهائي — مع ختم إلكتروني وتوقيع رقمي',
  ];
  afterSteps.forEach((step, i) => {
    const y = colY + 0.7 + i * 0.5;
    s.addShape('ellipse', { x: afterX + colW - 0.35, y: y + 0.1, w: 0.2, h: 0.2, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(step, {
      x: afterX + 0.2, y, w: colW - 0.55, h: 0.45,
      fontFace: FB, fontSize: 11, color: C.onDark, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  // BEFORE (left, secondary)
  const beforeX = 0.6;
  s.addShape('rect', { x: beforeX, y: colY, w: colW, h: colH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
  s.addShape('rect', { x: beforeX, y: colY, w: colW, h: 0.5, fill: { color: C.creamAlt }, line: { type: 'none' } });
  s.addText('قبل · اليوم', {
    x: beforeX, y: colY, w: colW, h: 0.5,
    fontFace: FH, fontSize: 15, bold: true, color: C.textMuted, align: 'center', rtlMode: true, valign: 'middle',
  });
  const beforeSteps = [
    'اليوم 1: التندر يصل لبريد عام — أحياناً لا يُرى',
    'اليوم 3: توزيع يدوي بعد اجتماع صباحي',
    'اليوم 5: الفريق يبحث عن عقود مشابهة يدوياً',
    'اليوم 8: مسودة عرض فني أولى — غالباً بدون سوابق',
    'اليوم 11: مراجعة مالية متكررة',
    'اليوم 14: إرسال متأخر — أحياناً بعد انتهاء المهلة',
  ];
  beforeSteps.forEach((step, i) => {
    const y = colY + 0.7 + i * 0.5;
    s.addShape('ellipse', { x: beforeX + colW - 0.35, y: y + 0.1, w: 0.2, h: 0.2, fill: { color: C.textFaint }, line: { type: 'none' } });
    s.addText(step, {
      x: beforeX + 0.2, y, w: colW - 0.55, h: 0.45,
      fontFace: FB, fontSize: 11, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  // Bottom: impact stat
  s.addShape('rect', { x: 0.6, y: 6.4, w: W - 1.2, h: 0.55, fill: { color: C.navyDeep }, line: { type: 'none' } });
  s.addText('النتيجة: تسريع 84% في دورة التندر — رفع معدّل الفوز من 15% إلى 25%', {
    x: 0.6, y: 6.4, w: W - 1.2, h: 0.55,
    fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'right', rtlMode: true, valign: 'middle',
  });

  s.addNotes(
    'هذا أهم سيناريو لأي شركة لوجستيات كبرى — التندرات هي العمود الفقري للإيراد. ' +
    'الأرقام (4 ساعات بدل 14 يوم) ليست وعداً تسويقياً: AI يُعدّ مسودة في 60 ثانية، المراجعة البشرية 20-40 دقيقة. ' +
    'اذكر أن الـ AI لا يُرسل أبداً دون مراجعة بشرية — هذا حد أحمر لحوكمة ديلكس. ' +
    'رفع معدّل الفوز من 15% إلى 25% رقم محافظ — بعض العملاء حقّقوا 30%+.'
  );
})();

console.log('[slides 11-20] defined');
