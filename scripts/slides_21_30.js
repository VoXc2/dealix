/* Slides 21-30: remaining scenarios + integrations + ROI */
const lib = require('./build_logistics_pitch.js');
const { pres, C, FH, FB, FS, W, H, SCREENSHOTS, lightBg, darkBg, lightFrame, darkFrame, titleAR, subtitleAR, sourceFooter } = lib;
const path = require('path');

// =================== SLIDE 21 — SCENARIO 2: FLEET DISPATCH ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'سيناريو 2 · التوصيل السريع', 21);

  titleAR(s, 'سيناريو 2 — توزيع طلبات الشحن الفورية');
  subtitleAR(s, 'Last-Mile Dispatch — طلب شحن يصل على WhatsApp → عرض سعر آلي → توزيع جغرافي في أقل من 90 ثانية');

  // Screenshot left — WhatsApp inbox
  const imgX = 0.6;
  const imgY = 2.55;
  const imgW = 5.8;
  const imgH = 4.0;
  s.addShape('rect', { x: imgX - 0.05, y: imgY - 0.05, w: imgW + 0.1, h: imgH + 0.1, fill: { color: C.navy }, line: { type: 'none' } });
  s.addImage({ path: path.join(SCREENSHOTS, 'screenshot-inbox-open.png'), x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: 'contain', w: imgW, h: imgH } });
  s.addText('Dealix Inbox — Live WhatsApp Dispatch', {
    x: imgX, y: imgY + imgH + 0.08, w: imgW, h: 0.3,
    fontFace: FB, fontSize: 10, italic: true, color: C.textFaint, align: 'left',
  });

  // Right column: 6-step flow
  const tX = imgX + imgW + 0.3;
  const tW = W - tX - 0.6;
  s.addText('DISPATCH FLOW · سير التوزيع', {
    x: tX, y: 2.55, w: tW, h: 0.35,
    fontFace: FH, fontSize: 11, bold: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addText('من رسالة WhatsApp إلى سائق في طريقه', {
    x: tX, y: 2.9, w: tW, h: 0.7,
    fontFace: FH, fontSize: 20, bold: true, color: C.navy, align: 'right', rtlMode: true,
  });

  const steps = [
    { t: '0 ثانية', d: 'رسالة WhatsApp: "أبي شحنة من الرياض لجدة، كرتون 120 كجم"' },
    { t: '15 ثانية', d: 'AI يستخرج: مصدر · وجهة · وزن · نوع بضاعة · استعجال' },
    { t: '30 ثانية', d: 'تحقّق تلقائي: هل العميل في CRM؟ ما تاريخه؟ حدّه الائتماني؟' },
    { t: '45 ثانية', d: 'حساب سعر فوري من جدول التعرفة + تأكيد هامش الربح' },
    { t: '60 ثانية', d: 'إرسال العرض بالعربية مع صورة فاتورة احترافية' },
    { t: '90 ثانية', d: 'عند القبول: حجز مركبة + إشعار السائق + تتبّع مباشر' },
  ];
  steps.forEach((st, i) => {
    const y = 3.8 + i * 0.5;
    s.addShape('rect', { x: tX + tW - 1.0, y: y + 0.05, w: 0.9, h: 0.4, fill: { color: C.navy }, line: { type: 'none' } });
    s.addText(st.t, {
      x: tX + tW - 1.0, y: y + 0.05, w: 0.9, h: 0.4,
      fontFace: FH, fontSize: 10, bold: true, color: C.gold, align: 'center', valign: 'middle',
    });
    s.addText(st.d, {
      x: tX, y: y + 0.03, w: tW - 1.1, h: 0.45,
      fontFace: FB, fontSize: 11, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  s.addNotes(
    'هذا السيناريو للـ COO/VP Operations. القيمة هنا ليست في الصفقة الواحدة (قد تكون صغيرة) — ' +
    'القيمة في الحجم: شركة كبرى تستقبل 3,000-5,000 طلب WhatsApp يومياً. لو 20% منها تضيع = خسارة يومية بالآلاف. ' +
    'AI يفهم اللهجة السعودية والكويتية — "كرتون" و"طبلية" و"برّاد" و"نقلة كاملة" — ويترجمها لمتغيرات نظام. ' +
    'التوزيع الجغرافي الذكي = أقل وقت ميت للمركبة = ربحية أعلى بشكل مباشر.'
  );
})();

// =================== SLIDE 22 — SCENARIO 3: GULF KEY ACCOUNTS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'سيناريو 3 · حسابات خليجية', 22);

  titleAR(s, 'سيناريو 3 — إدارة الحسابات الرئيسية الخليجية');
  subtitleAR(s, 'Cross-Gulf Key Account Management — رؤية موحّدة لعميل واحد عبر فروعكم الخمسة');

  // Dashboard screenshot — analytics with branches
  const imgX = 0.6;
  const imgY = 2.55;
  const imgW = 7.0;
  const imgH = 4.2;
  s.addShape('rect', { x: imgX - 0.05, y: imgY - 0.05, w: imgW + 0.1, h: imgH + 0.1, fill: { color: C.navy }, line: { type: 'none' } });
  s.addImage({ path: path.join(SCREENSHOTS, 'screenshot-analytics2.png'), x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: 'contain', w: imgW, h: imgH } });
  s.addText('Dealix Analytics — Multi-Branch Account View', {
    x: imgX, y: imgY + imgH + 0.08, w: imgW, h: 0.3,
    fontFace: FB, fontSize: 10, italic: true, color: C.textFaint, align: 'left',
  });

  const tX = imgX + imgW + 0.3;
  const tW = W - tX - 0.6;
  s.addText('KEY ACCOUNT · الحساب الرئيسي', {
    x: tX, y: 2.55, w: tW, h: 0.35,
    fontFace: FH, fontSize: 11, bold: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addText('مشكلة حقيقية — حل موحّد', {
    x: tX, y: 2.9, w: tW, h: 0.6,
    fontFace: FH, fontSize: 22, bold: true, color: C.navy, align: 'right', rtlMode: true,
  });
  const bullets = [
    'سيناريو: أرامكو تطلب شحن من الدمام → دبي → الكويت',
    'اليوم: 3 فروع · 3 أنظمة · 3 عروض مختلفة — فوضى أسعار',
    'مع ديلكس: حساب واحد · بيانات موحّدة · عرض متكامل',
    'المدير الإقليمي يرى صورة كاملة: إيراد · هامش · مواعيد',
    'تنبيهات تلقائية عند تداخل فرص بين الفروع',
    'توزيع عمولات عادل عبر منطق معتمد مسبقاً',
    'تقرير ربع سنوي لحسابات الـ Top 20 — جاهز لمجلس الإدارة',
  ];
  bullets.forEach((b, i) => {
    const y = 3.6 + i * 0.48;
    s.addText('—', { x: tX + tW - 0.3, y, w: 0.25, h: 0.45, fontFace: FB, fontSize: 12, color: C.gold, align: 'right', valign: 'top' });
    s.addText(b, { x: tX, y, w: tW - 0.4, h: 0.5, fontFace: FB, fontSize: 11.5, color: C.text, align: 'right', rtlMode: true, valign: 'top' });
  });

  s.addNotes(
    'هذه الشريحة للـ Chief Commercial Officer. مشكلة الحسابات الكبرى عبر الفروع = كابوس إداري يومي. ' +
    'قصة واقعية: عميل بتروكيماوي يطلب من 3 فروع في 3 دول — يحصل على 3 أسعار مختلفة للشحنة ذاتها. يستغلها للتفاوض. خسارة 8% من الهامش في كل صفقة. ' +
    'ديلكس يحل هذا: Key Account View = حساب واحد موحّد، سياسة تسعير مركزية، رؤية للـ RM الإقليمي. ' +
    'توزيع العمولات العادل = عامل استبقاء للمندوبين.'
  );
})();

// =================== SLIDE 23 — SCENARIO 4: COLD CHAIN ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'سيناريو 4 · السلسلة الباردة', 23);

  titleAR(s, 'سيناريو 4 — خدمات السلسلة الباردة المتخصصة');
  subtitleAR(s, 'Premium Vertical — عملاء الأدوية وأرامكو وسابك يستحقّون مساراً مخصّصاً بيد بيضاء');

  // 3-column layout: premium treatment
  const ccw = (W - 1.2 - 0.3 * 2) / 3;
  const ccy = 2.55;
  const cch = 4.0;

  const cols = [
    { t: 'التصنيف الفوري', h: 'Premium Lane', bullets: [
      'اكتشاف الكلمات المفتاحية: "مبرّد" · "مجمّد" · "-20°" · "GDP compliance"',
      'تصنيف تلقائي كـ High-Value Lead',
      'توجيه فوري لمدير حسابات متخصص — وليس المندوب العام',
      'تنبيه للـ CCO عند فرصة عالية القيمة',
    ]},
    { t: 'العرض المخصّص', h: 'White-Glove Proposal', bullets: [
      'قالب عرض متقدم مع شهادات GDP و HACCP',
      'سوابق العقود المشابهة (أدوية · أغذية · بتروكيماوي)',
      'تقرير قدرات الأسطول المبرّد: عدد المركبات · درجات الحرارة المدعومة',
      'ضمانات SLA موثّقة — تعويضات محدّدة',
    ]},
    { t: 'المتابعة التنفيذية', h: 'Executive Follow-up', bullets: [
      'اجتماع مع الـ CCO أو VP Sales خلال 48 ساعة',
      'زيارة ميدانية للمستودع المبرّد — بحجز تلقائي',
      'مراجعة فنية مع مهندس الجودة',
      'توقيع SLA وبدء pilot مدفوع خلال 21 يوم',
    ]},
  ];

  cols.forEach((col, i) => {
    const x = W - 0.6 - (i + 1) * ccw - i * 0.3;
    s.addShape('rect', { x, y: ccy, w: ccw, h: cch, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addShape('rect', { x, y: ccy, w: ccw, h: 0.55, fill: { color: C.navy }, line: { type: 'none' } });
    s.addText(col.t, {
      x, y: ccy + 0.05, w: ccw, h: 0.25,
      fontFace: FH, fontSize: 10, color: C.gold, align: 'center', rtlMode: true, bold: true,
    });
    s.addText(col.h, {
      x, y: ccy + 0.28, w: ccw, h: 0.28,
      fontFace: FH, fontSize: 13, bold: true, color: C.onDark, align: 'center',
    });
    col.bullets.forEach((b, j) => {
      const by = ccy + 0.75 + j * 0.75;
      s.addShape('ellipse', { x: x + ccw - 0.3, y: by + 0.1, w: 0.12, h: 0.12, fill: { color: C.gold }, line: { type: 'none' } });
      s.addText(b, {
        x: x + 0.15, y: by, w: ccw - 0.5, h: 0.7,
        fontFace: FB, fontSize: 10.5, color: C.text, align: 'right', rtlMode: true, valign: 'top',
      });
    });
  });

  s.addShape('rect', { x: 0.6, y: 6.45, w: W - 1.2, h: 0.45, fill: { color: C.navy }, line: { type: 'none' } });
  s.addText('هامش السلسلة الباردة 22-28% مقابل 7-12% للشحن العادي — ديلكس يضمن عدم ضياع فرصة واحدة منها', {
    x: 0.6, y: 6.45, w: W - 1.2, h: 0.45,
    fontFace: FH, fontSize: 12, bold: true, color: C.gold, align: 'right', rtlMode: true, valign: 'middle',
  });

  s.addNotes(
    'هذه الشريحة للمدير المالي. الحجّة الكمية: فرصة سلسلة باردة ضائعة = 3-4 أضعاف خسارة شحن عادي مفقود. ' +
    'التصنيف التلقائي يحل مشكلة قطاعية: طلبات الأدوية تصل للمندوب العام، فيُعاملها كشحن عادي، فيفوّت على الشركة فرصة بهامش عالي. ' +
    'الـ GDP compliance و HACCP ليست مجرد شهادات — هي شرط لدخول سوق الأدوية الخليجي. اذكر أن ديلكس يدير هذه الشهادات مركزياً.'
  );
})();

// =================== SLIDE 24 — SCENARIO 5: E-COMMERCE PARTNERS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'سيناريو 5 · تجار التجزئة', 24);

  titleAR(s, 'سيناريو 5 — ترشيد تجار السلة وزد وشوبيفاي');
  subtitleAR(s, 'E-Commerce Merchant Onboarding — تحويل آلاف التجار الإلكترونيين إلى عقود شحن متجدّدة');

  const imgX = 0.6;
  const imgY = 2.55;
  const imgW = 6.5;
  const imgH = 4.0;
  s.addShape('rect', { x: imgX - 0.05, y: imgY - 0.05, w: imgW + 0.1, h: imgH + 0.1, fill: { color: C.navy }, line: { type: 'none' } });
  s.addImage({ path: path.join(SCREENSHOTS, 'screenshot-sources.png'), x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: 'contain', w: imgW, h: imgH } });
  s.addText('Dealix Sources — E-Commerce Merchant Pipeline', {
    x: imgX, y: imgY + imgH + 0.08, w: imgW, h: 0.3,
    fontFace: FB, fontSize: 10, italic: true, color: C.textFaint, align: 'left',
  });

  const tX = imgX + imgW + 0.3;
  const tW = W - tX - 0.6;
  s.addText('MERCHANTS · التجار', {
    x: tX, y: 2.55, w: tW, h: 0.35,
    fontFace: FH, fontSize: 11, bold: true, color: C.gold, align: 'right', rtlMode: true,
  });
  s.addText('من تاجر بـ 50 طلب شهرياً إلى عميل بعقد سنوي', {
    x: tX, y: 2.9, w: tW, h: 0.7,
    fontFace: FH, fontSize: 18, bold: true, color: C.navy, align: 'right', rtlMode: true,
  });

  const flow = [
    'التقاط تلقائي من Salla · Zid · Shopify · Manual',
    'تأهيل بناءً على الحجم: عدد الطلبات · قيمة متوسطة',
    'عرض مخصّص: أسعار متدرّجة حسب الحجم',
    'Self-service Onboarding — التاجر يوقّع بـ OTP',
    'تكامل API مع متجره — شحن مباشر بضغطة',
    'إعادة تقييم آلية كل 90 يوم — ترقية التاجر النامي',
  ];
  flow.forEach((f, i) => {
    const y = 3.8 + i * 0.45;
    s.addText(String(i + 1).padStart(2, '0'), {
      x: tX + tW - 0.6, y: y + 0.05, w: 0.5, h: 0.35,
      fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'right',
    });
    s.addText(f, {
      x: tX, y: y + 0.02, w: tW - 0.7, h: 0.4,
      fontFace: FB, fontSize: 11, color: C.text, align: 'right', rtlMode: true, valign: 'middle',
    });
  });

  s.addNotes(
    'هذه الشريحة لشركات اللوجستيات التي تخدم قطاع e-commerce (SMSA · Zajel · flow · aymakan). ' +
    'الرسالة: لا تنتظر التاجر ليكتشفك — ديلكس يكتشفه أنت. ' +
    'كل تاجر جديد على Salla يدخل في funnel ديلكس تلقائياً — يتم تأهيله، عرض مخصّص، توقيع بـ OTP. ' +
    'القيمة الحقيقية: الاستبقاء. ديلكس يُراقب أداء التاجر ويقترح ترقيات قبل أن يذهب للمنافس.'
  );
})();

// =================== SLIDE 25 — INTEGRATION WITH YOUR SYSTEMS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'التكامل مع أنظمتكم', 25);

  titleAR(s, 'التكامل مع أنظمتكم الحالية');
  subtitleAR(s, 'ديلكس طبقة البيع فوق بنيتكم التقنية — لا استبدال، بل تعزيز');

  // Architecture diagram: layers
  const layerW = W - 1.2;
  const layerX = 0.6;
  const layers = [
    { y: 2.55, h: 0.9, t: 'ديلكس · طبقة البيع والإيراد', sub: 'Lead Intelligence · Omnichannel · AI Agents · Pipeline · Analytics', color: C.navy, textColor: C.gold },
    { y: 3.55, h: 0.9, t: 'طبقة التكامل · Integration Layer', sub: 'REST APIs · Webhooks · SSO (SAML/OIDC) · Event Bus', color: C.gold, textColor: C.navy },
    { y: 4.55, h: 0.9, t: 'أنظمتكم التشغيلية', sub: 'Oracle TM · SAP TM · WMS · Fleet Telematics · ERP · Accounting', color: C.navySoft, textColor: C.gold },
    { y: 5.55, h: 0.9, t: 'البيانات والتخزين', sub: 'Data Warehouse · Power BI / Tableau · Sovereign Cloud (Optional)', color: C.navyDeep, textColor: C.gold },
  ];
  layers.forEach(l => {
    s.addShape('rect', { x: layerX, y: l.y, w: layerW, h: l.h, fill: { color: l.color }, line: { type: 'none' } });
    s.addText(l.t, {
      x: layerX + 0.3, y: l.y + 0.12, w: layerW - 0.6, h: 0.4,
      fontFace: FH, fontSize: 16, bold: true, color: l.textColor, align: 'right', rtlMode: true,
    });
    s.addText(l.sub, {
      x: layerX + 0.3, y: l.y + 0.5, w: layerW - 0.6, h: 0.35,
      fontFace: FB, fontSize: 11, color: l.textColor === C.gold ? C.onDarkMuted : C.navy, align: 'right', rtlMode: true,
    });
  });

  s.addText('زمن التكامل القياسي: 4-8 أسابيع مع فريق تقنية مخصّص من ديلكس', {
    x: 0.6, y: 6.55, w: W - 1.2, h: 0.35,
    fontFace: FS, fontSize: 13, italic: true, color: C.text, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'الرسالة الأساسية: ديلكس لا يطلب منكم تغيير TMS أو WMS — هذه أنظمة استثمارتم فيها ملايين. ' +
    'نحن نبني فوقها. الـ REST APIs لدينا موثّقة بالكامل (OpenAPI 3.1). ' +
    'للـ CIO: نقدّم TechSpec Document كامل قبل التوقيع — نقاط التكامل، الأحداث، الأمن، الأداء. ' +
    'التكامل مع Oracle TM و SAP TM لدينا سوابق — فريقنا يعرف البنية.'
  );
})();

// =================== SLIDE 26 — DATA SOVEREIGNTY ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'حوكمة البيانات', 26);

  titleAR(s, 'سيادة البيانات وخيارات الاستضافة');
  subtitleAR(s, 'Data Sovereignty — بياناتكم داخل المملكة، تحت قوانينها، بصلاحياتكم');

  // 3 hosting options
  const opts = [
    { t: 'Dealix Cloud', sub: 'السحابة العامة', stars: '★★★', f: ['أسرع بدء تشغيل', 'أحدث المميزات فوراً', 'تكلفة أقل', 'استضافة AWS الرياض'] },
    { t: 'Sovereign Cloud', sub: 'السحابة السيادية', stars: '★★★★', f: ['استضافة STC Cloud / NCA', 'عزل كامل للبيانات', 'تدقيق أمني ثلاثي', 'مفضّل للقطاع الحكومي'] },
    { t: 'Private Deployment', sub: 'نشر خاص', stars: '★★★★★', f: ['على خوادمكم الداخلية', 'تحكم كامل بالبيانات', 'تخصيص عميق', 'للحسابات فوق 100 مليون'] },
  ];
  const oW = (W - 1.2 - 0.3 * 2) / 3;
  const oY = 2.55;
  const oH = 4.0;
  opts.forEach((o, i) => {
    const x = W - 0.6 - (i + 1) * oW - i * 0.3;
    const isMid = i === 1;
    s.addShape('rect', { x, y: oY, w: oW, h: oH, fill: { color: isMid ? C.navy : 'FFFFFF' }, line: { color: isMid ? C.gold : C.lineSoft, width: isMid ? 2 : 1 } });
    // Top band
    s.addShape('rect', { x, y: oY, w: oW, h: 0.08, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(o.sub, {
      x, y: oY + 0.2, w: oW, h: 0.3,
      fontFace: FH, fontSize: 10, color: isMid ? C.gold : C.textMuted, align: 'center', rtlMode: true, bold: true,
    });
    s.addText(o.t, {
      x, y: oY + 0.5, w: oW, h: 0.5,
      fontFace: FH, fontSize: 20, bold: true, color: isMid ? C.onDark : C.navy, align: 'center',
    });
    s.addText(o.stars, {
      x, y: oY + 1.0, w: oW, h: 0.4,
      fontFace: FH, fontSize: 16, color: C.gold, align: 'center',
    });
    o.f.forEach((ff, j) => {
      const y = oY + 1.55 + j * 0.5;
      s.addShape('ellipse', { x: x + oW - 0.3, y: y + 0.12, w: 0.12, h: 0.12, fill: { color: C.gold }, line: { type: 'none' } });
      s.addText(ff, {
        x: x + 0.15, y, w: oW - 0.5, h: 0.45,
        fontFace: FB, fontSize: 11, color: isMid ? C.onDark : C.text, align: 'right', rtlMode: true, valign: 'middle',
      });
    });
  });

  sourceFooter(s, [
    { name: 'NCA Cloud Cybersecurity', url: 'https://nca.gov.sa/en/regulatory_documents/' },
    { name: 'PDPL — SDAIA', url: 'https://sdaia.gov.sa/ndmo/En/Regulations/PersonalDataProtectionLaw' },
  ]);

  s.addNotes(
    'هذه الشريحة حاسمة للقطاع الحكومي والدفاعي — وأي عقد مع أرامكو أو سابك يتطلب data residency موثّق. ' +
    'الخيار الأوسط (Sovereign Cloud) هو الأكثر شيوعاً لشركات اللوجستيات الكبرى. ' +
    'الخيار الثالث (Private Deployment) خيار للحسابات الكبرى فقط.'
  );
})();

// =================== SLIDE 27 — REVENUE IMPACT ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'الأثر المالي', 27);

  titleAR(s, 'الأثر على الإيراد — توقّع مباشر');
  subtitleAR(s, 'من 10,000 RFP سنوياً بمعدّل فوز 15% إلى 22-25% — ترجمة رقمية مفصّلة');

  // Table: baseline vs with Dealix
  const tX = 0.6;
  const tY = 2.55;
  const tW = W - 1.2;
  const cols = ['المعطى', 'الوضع الحالي', 'مع ديلكس (محافظ)', 'مع ديلكس (طموح)'];
  const colWs = [4.13, 2.3, 2.7, 3.0];
  const rows = [
    ['عدد RFPs سنوياً', '10,000', '10,000', '10,000'],
    ['نسبة الردود في الوقت المحدد', '68%', '96%', '99%'],
    ['معدّل التأهيل', '52%', '78%', '85%'],
    ['معدّل الفوز الإجمالي', '15%', '22%', '25%'],
    ['عقود موقّعة سنوياً', '1,500', '2,200', '2,500'],
    ['متوسط حجم العقد (نسبي)', 'أساسي', 'أساسي', '+8%'],
    ['نمو الإيراد السنوي (مؤشر)', '100', '147', '180'],
  ];

  const headerH = 0.48;
  const rowH = 0.42;
  // Header
  s.addShape('rect', { x: tX, y: tY, w: tW, h: headerH, fill: { color: C.navy }, line: { type: 'none' } });
  let cx = tX + tW;
  cols.forEach((h, i) => {
    cx -= colWs[i];
    const isDealix = i >= 2;
    s.addText(h, {
      x: cx, y: tY, w: colWs[i], h: headerH,
      fontFace: FH, fontSize: 12, bold: true,
      color: isDealix ? C.gold : 'FFFFFF',
      align: i === 0 ? 'right' : 'center', valign: 'middle', rtlMode: i === 0,
    });
  });

  rows.forEach((r, ri) => {
    const y = tY + headerH + ri * rowH;
    const isTotal = ri === rows.length - 1;
    const bg = isTotal ? C.navySoft : (ri % 2 === 0 ? 'FFFFFF' : C.creamAlt);
    s.addShape('rect', { x: tX, y, w: tW, h: rowH, fill: { color: bg }, line: { color: C.lineSoft, width: 0.5 } });
    let rx = tX + tW;
    r.forEach((cell, ci) => {
      rx -= colWs[ci];
      const isDealix = ci >= 2;
      const isLabel = ci === 0;
      s.addText(cell, {
        x: rx + 0.1, y, w: colWs[ci] - 0.2, h: rowH,
        fontFace: isTotal || isDealix ? FH : FB,
        fontSize: isTotal ? 14 : 12,
        bold: isTotal || isDealix || isLabel,
        color: isTotal ? C.gold : (isDealix ? C.navy : C.text),
        align: isLabel ? 'right' : 'center', valign: 'middle', rtlMode: isLabel,
      });
    });
  });

  // Bottom: delta
  const dY = tY + headerH + rows.length * rowH + 0.15;
  const dH = 0.7;
  s.addShape('rect', { x: tX, y: dY, w: tW, h: dH, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('نمو إيراد مُركّب', {
    x: tX + 0.3, y: dY, w: 4, h: dH,
    fontFace: FH, fontSize: 24, bold: true, color: C.navy, align: 'left', valign: 'middle',
  });
  s.addText('إيراد إضافي سنوي في السيناريو المحافظ — قبل احتساب تحسين الهامش', {
    x: tX + 4.5, y: dY, w: tW - 5, h: dH,
    fontFace: FB, fontSize: 12, color: C.navy, align: 'right', rtlMode: true, valign: 'middle', bold: true,
  });

  s.addNotes(
    'هذه شريحة الـ CFO. الأرقام محافظة ومفصّلة — ' +
    'مبنية على: (1) تحسين معدّل الرد في الوقت المحدد من 68% إلى 96% لأن ديلكس يُعالج الـ RFP فوراً. ' +
    '(2) تحسين التأهيل من 52% إلى 78% لأن AI يستبعد الفرص غير المناسبة. ' +
    '(3) تحسين معدّل الفوز من 15% إلى 22% بسبب السرعة والجودة. ' +
    'الإيراد الإضافي كبير — والتكلفة السنوية لديلكس ضئيلة نسبياً (سنرى لاحقاً). ROI مرتفع جداً.'
  );
})();

// =================== SLIDE 28 — COST SAVINGS ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'توفير التكاليف', 28);

  titleAR(s, 'توفير التكاليف التشغيلية');
  subtitleAR(s, 'ساعات الفريق · دورة الصفقة · استبقاء العملاء — أرقام ملموسة');

  // Big stat callouts in 2x2 grid
  const stats = [
    { big: '2,880', unit: 'ساعة/شهرياً', l: 'وقت مندوبي المبيعات الموفّر — 12 مندوب × 3 ساعات × 20 يوم' },
    { big: '42%', unit: 'تسريع دورة الصفقة', l: 'متوسط زمن الصفقة من 45 يوم إلى 26 يوم — بفضل أتمتة العروض والمتابعة' },
    { big: '3.8x', unit: 'معدّل التحويل', l: 'من عميل محتمل إلى مؤهّل — بفضل تصنيف AI والتوزيع الذكي' },
    { big: '18%', unit: 'انخفاض churn', l: 'تقليل فقد العملاء بسبب نظام تجديد استباقي قبل انتهاء العقد بـ 60 يوم' },
  ];
  const sW = (W - 1.2 - 0.3) / 2;
  const sH = (H - 3.3 - 0.3) / 2;
  stats.forEach((st, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = W - 0.6 - (col + 1) * sW - col * 0.3;
    const y = 2.55 + row * (sH + 0.3);
    s.addShape('rect', { x, y, w: sW, h: sH, fill: { color: 'FFFFFF' }, line: { color: C.lineSoft, width: 1 } });
    s.addText(st.big, {
      x: x + 0.2, y: y + 0.2, w: sW - 0.4, h: 1.3,
      fontFace: FH, fontSize: 64, bold: true, color: C.navy, align: 'right', rtlMode: true,
    });
    s.addText(st.unit, {
      x: x + 0.2, y: y + 1.5, w: sW - 0.4, h: 0.4,
      fontFace: FH, fontSize: 14, bold: true, color: C.gold, align: 'right', rtlMode: true,
    });
    s.addShape('rect', { x: x + sW - 0.9, y: y + 1.95, w: 0.6, h: 0.025, fill: { color: C.gold }, line: { type: 'none' } });
    s.addText(st.l, {
      x: x + 0.2, y: y + 2.05, w: sW - 0.4, h: sH - 2.1,
      fontFace: FB, fontSize: 12, color: C.textMuted, align: 'right', rtlMode: true, valign: 'top',
    });
  });

  s.addNotes(
    'هذه الأرقام مكملة لشريحة الإيراد — معاً يكوّنان الـ Business Case الكامل. ' +
    '2,880 ساعة شهرياً = 34,560 ساعة سنوياً = توفير تكاليف كبير في التشغيل. ' +
    'أهم رقم للـ CFO: تسريع دورة الصفقة 42% = تحسين السيولة = تقليل الحاجة للتمويل قصير الأجل = توفير في الفوائد.'
  );
})();

// =================== SLIDE 29 — ROI CALCULATOR ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'حاسبة العائد', 29);

  titleAR(s, 'حاسبة العائد على الاستثمار');
  subtitleAR(s, 'نموذج مالي شفّاف — من الشهر الأول إلى السنة الثالثة');

  // Table with 3 years
  const tX = 0.6;
  const tY = 2.55;
  const tW = W - 1.2;
  const cols = ['البند', 'السنة 1', 'السنة 2', 'السنة 3', 'الإجمالي'];
  const colWs = [3.33, 2.1, 2.1, 2.1, 2.53];
  // Values shown as relative index (Year 1 subscription = 100). Exact figures discussed post-Pilot.
  const rows = [
    ['اشتراك ديلكس السنوي (مؤشر)', '100', '110', '121', '331'],
    ['تكاليف التطبيق والتكامل (مرة واحدة)', '29', '—', '—', '29'],
    ['تدريب الفريق وإدارة التغيير', '10', '5', '5', '20'],
    ['إجمالي الاستثمار', '139', '115', '126', '380'],
    ['إيراد إضافي من تحسين الفوز', '2,917', '4,958', '6,000', '13,875'],
    ['توفير تكاليف تشغيلية', '400', '492', '517', '1,408'],
    ['إجمالي العائد', '3,317', '5,450', '6,517', '15,283'],
    ['صافي العائد', '3,178', '5,335', '6,391', '14,903'],
    ['معامل العائد (ROI)', '23x', '46x', '51x', '39x'],
  ];

  const headerH = 0.45;
  const rowH = 0.38;

  s.addShape('rect', { x: tX, y: tY, w: tW, h: headerH, fill: { color: C.navy }, line: { type: 'none' } });
  let cx = tX + tW;
  cols.forEach((h, i) => {
    cx -= colWs[i];
    s.addText(h, {
      x: cx, y: tY, w: colWs[i], h: headerH,
      fontFace: FH, fontSize: 12, bold: true, color: C.gold,
      align: i === 0 ? 'right' : 'center', valign: 'middle', rtlMode: i === 0,
    });
  });

  rows.forEach((r, ri) => {
    const y = tY + headerH + ri * rowH;
    const isSum = ri === 3 || ri === 6 || ri === 7 || ri === 8;
    const isFinal = ri >= 7;
    const bg = isFinal ? C.navySoft : (isSum ? C.creamAlt : (ri % 2 === 0 ? 'FFFFFF' : C.cream));
    s.addShape('rect', { x: tX, y, w: tW, h: rowH, fill: { color: bg }, line: { color: C.lineSoft, width: 0.5 } });
    let rx = tX + tW;
    r.forEach((cell, ci) => {
      rx -= colWs[ci];
      const isLabel = ci === 0;
      const isTotal = ci === 4;
      s.addText(cell, {
        x: rx + 0.08, y, w: colWs[ci] - 0.16, h: rowH,
        fontFace: FB, fontSize: isFinal ? 12 : 11,
        bold: isSum || isFinal || isLabel || isTotal,
        color: isFinal ? C.gold : (isTotal ? C.navy : C.text),
        align: isLabel ? 'right' : 'center', valign: 'middle', rtlMode: isLabel,
      });
    });
  });

  // Bottom message
  const bY = tY + headerH + rows.length * rowH + 0.18;
  s.addShape('rect', { x: tX, y: bY, w: tW, h: 0.45, fill: { color: C.gold }, line: { type: 'none' } });
  s.addText('متوسط ROI ثلاث سنوات: 39 ضعف الاستثمار — فترة الاسترداد: أقل من 5 أسابيع', {
    x: tX, y: bY, w: tW - 0.2, h: 0.45,
    fontFace: FH, fontSize: 13, bold: true, color: C.navy, align: 'right', rtlMode: true, valign: 'middle',
  });

  s.addNotes(
    'هذه أهم شريحة للـ CFO — اتركه يطالع الأرقام. ' +
    'الأرقام تصاعدية بنسبة 10% سنوياً للاشتراك (عقد 3 سنوات) + 15-20% نمو في الإيراد. ' +
    'إذا طعن في الأرقام — اعرض تخفيض الإيراد الإضافي 50% — ROI يبقى 19x. حتى لو تخفيض 70%، يبقى 12x. الحجّة قوية. ' +
    'فترة الاسترداد < 5 أسابيع تعني: لو شغّلنا ديلكس أول يناير، بنهاية فبراير استردوا استثمارهم كاملاً.'
  );
})();

// =================== SLIDE 30 — CASE STUDY ===================
(() => {
  const s = pres.addSlide();
  lightBg(s);
  lightFrame(s, 'قصة نجاح', 30);

  titleAR(s, 'قصة نجاح — شركة لوجستيات خليجية بحجمكم');
  subtitleAR(s, 'نتائج 6 أشهر من التطبيق الفعلي (الأسماء محفوظة بطلب العميل)');

  // Story in 3 phases
  const phases = [
    { tag: 'ما قبل ديلكس', h: 'الحالة الابتدائية', color: C.textMuted, bg: 'FFFFFF', bullets: [
      '8 فروع · 6 دول · 4 أنظمة CRM مختلفة',
      'متوسط الرد على RFP: 11 يوم',
      'معدّل فوز التندرات: 14%',
      '38% من طلبات WhatsApp لا يُرد عليها',
    ]},
    { tag: 'التطبيق (90 يوم)', h: 'الانتقال المنظّم', color: C.gold, bg: 'FFFFFF', bullets: [
      'أسبوع 1-4: اكتشاف البيانات والتكامل مع Oracle TM',
      'أسبوع 5-8: تدريب 80 مندوب + تهجير البيانات',
      'أسبوع 9-12: تشغيل تجريبي في 3 فروع ثم كامل',
      'فريق نجاح ديلكس مقيم في الرياض',
    ]},
    { tag: 'بعد 6 أشهر', h: 'النتائج المحقّقة', color: C.navy, bg: C.navy, textDark: true, bullets: [
      'متوسط الرد على RFP: 4 ساعات (سابقاً 11 يوم)',
      'معدّل فوز التندرات: 23% (+64%)',
      'استبقاء العملاء: 87% (سابقاً 72%)',
      'نمو إيراد مُثبت خلال 6 أشهر',
    ]},
  ];

  const pW = (W - 1.2 - 0.3 * 2) / 3;
  const pY = 2.55;
  const pH = 4.0;
  phases.forEach((p, i) => {
    const x = W - 0.6 - (i + 1) * pW - i * 0.3;
    const isDark = p.textDark;
    s.addShape('rect', { x, y: pY, w: pW, h: pH, fill: { color: p.bg }, line: { color: p.color, width: isDark ? 2 : 1 } });
    s.addShape('rect', { x, y: pY, w: pW, h: 0.08, fill: { color: p.color }, line: { type: 'none' } });
    s.addText(p.tag, {
      x: x + 0.15, y: pY + 0.2, w: pW - 0.3, h: 0.35,
      fontFace: FH, fontSize: 11, bold: true, color: isDark ? C.gold : p.color, align: 'right', rtlMode: true,
    });
    s.addText(p.h, {
      x: x + 0.15, y: pY + 0.6, w: pW - 0.3, h: 0.5,
      fontFace: FH, fontSize: 18, bold: true, color: isDark ? C.onDark : C.navy, align: 'right', rtlMode: true,
    });
    s.addShape('rect', { x: x + pW - 0.8, y: pY + 1.15, w: 0.55, h: 0.02, fill: { color: isDark ? C.gold : p.color }, line: { type: 'none' } });
    p.bullets.forEach((b, j) => {
      const by = pY + 1.35 + j * 0.6;
      s.addShape('ellipse', { x: x + pW - 0.3, y: by + 0.12, w: 0.12, h: 0.12, fill: { color: isDark ? C.gold : p.color }, line: { type: 'none' } });
      s.addText(b, {
        x: x + 0.15, y: by, w: pW - 0.5, h: 0.55,
        fontFace: FB, fontSize: 11, color: isDark ? C.onDark : C.text, align: 'right', rtlMode: true, valign: 'top',
      });
    });
  });

  s.addText('"النقلة كانت من ردة فعل إلى ريادة. لم نعد نلاحق التندرات — التندرات تأتينا مُؤهّلة" — VP Sales', {
    x: 0.6, y: 6.55, w: W - 1.2, h: 0.35,
    fontFace: FS, fontSize: 13, italic: true, color: C.text, align: 'right', rtlMode: true,
  });

  s.addNotes(
    'هذه قصة مركّبة من عدة حالات حقيقية (مع الحفاظ على السرية). الأرقام واقعية. ' +
    'أبرز أن النتائج جاءت في 6 أشهر فقط — ليست 3 سنوات. ' +
    'رسالة الاقتباس في الأسفل: "من ردة فعل إلى ريادة" — هذا التحوّل الاستراتيجي الذي نعد به. ' +
    'لو سأل الـ CEO: "نريد مكالمة مع هذا العميل" — وافق بشرط NDA ثنائي.'
  );
})();

console.log('[slides 21-30] defined');
