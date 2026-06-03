// seed-sample-data.js
// Emits SAMPLE/seed operational data for the Dealix commercial machine into
// data/**/*.jsonl. All companies below are FICTIONAL examples used to exercise
// the scripts (daily plan, quality gate, control check, daily brief). Real runs
// replace these with packs built from public or founder-provided data.
// Re-run with: node scripts/seed-sample-data.js
import { writeFileSync, mkdirSync } from 'node:fs'
import { dirname, resolve, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const write = (rel, records) => {
  const abs = join(ROOT, rel)
  mkdirSync(dirname(abs), { recursive: true })
  writeFileSync(abs, records.map((r) => JSON.stringify(r)).join('\n') + '\n', 'utf8')
  console.log(`  wrote ${records.length} → ${rel}`)
}

// --- strong email-draft builder (lands at/near 100 on the rubric) ---
const strong = ({ company, website, city, sector, signal, pain, system, why, subject, cta, evidence = 'L2' }) => ({
  company, website, country: 'SA', city, sector, signal,
  likely_pain: pain,
  recommended_system: system,
  why_this_system: why,
  first_mission: 'Sprint قصير يسلّم أول مخرج عملي خلال أيام',
  proof_angle: 'أين تتسرب الفرص فعليًا عبر المراحل',
  email_angle: 'قيمة واضحة قبل أي التزام كبير',
  subject,
  email_body:
    `السلام عليكم،\n\nاطّلعت على ${company} في مجال ${sector}، ولاحظت ${signal}. ` +
    `غالبًا في هذا النوع من الشركات يكون التحدي ${pain}.\n\n` +
    `في ${company} نقترح Sprint قصير نبني فيه أول مخرج عملي بدون تغيير أدواتكم الحالية. ` +
    `الفكرة ليست بيع أداة، بل توضيح أين تتعطل الأمور ثم تسليم مسار قابل للتشغيل.\n\n` +
    `هل تفضّل مكالمة قصيرة 20 دقيقة، أو نرسل لكم تشخيصًا مختصرًا أولًا؟`,
  cta,
  risk_level: 'low',
  evidence_level: evidence,
  approval_status: 'draft',
  send_readiness: 'ready_for_review',
})

const emailDrafts = [
  strong({ company: 'Digital Rise Agency', website: 'www.digitalrise.sa', city: 'الرياض', sector: 'وكالة تسويق',
    signal: 'صفحة خدمات إدارة الحملات تركّز على توليد leads للعملاء دون ذكر نظام متابعة', pain: 'متابعة الفرص بنظام واضح بدل الاجتهاد',
    system: 'revenue-operating-system', why: 'الوكالة تولّد leads لعملائها وغالبًا تواجه التحدي ذاته داخليًا في المتابعة والقرار',
    subject: 'فكرة سريعة لتقليل تسرب الفرص في Digital Rise Agency', cta: 'احجز مكالمة 20 دقيقة' }),
  strong({ company: 'Growth Labs SA', website: 'www.growthlabs.sa', city: 'جدة', sector: 'وكالة تسويق',
    signal: 'إعلانات توظيف لمسؤول مبيعات تشير إلى توسّع تجاري', pain: 'غياب تقرير إيراد دوري وقرار يومي واضح',
    system: 'revenue-operating-system', why: 'مع التوسّع التجاري تزداد الحاجة لمسار متابعة وتقرير إيراد منظّم',
    subject: 'تقرير إيراد يومي لـ Growth Labs SA', cta: 'احجز مكالمة قصيرة' }),
  strong({ company: 'TrainMe KSA', website: 'www.trainme.sa', city: 'الرياض', sector: 'تدريب',
    signal: 'الموقع يعرض رقم واتساب رئيسيًا للاستفسار عن البرامج', pain: 'استفسارات واتساب تدخل وتُنسى قبل المتابعة',
    system: 'follow-up-recovery-os', why: 'تعدد البرامج مع قناة واتساب يعني استفسارات كثيرة تحتاج متابعة منظمة',
    subject: 'استعادة الاستفسارات المتروكة في TrainMe KSA', cta: 'ابدأ تشخيصًا سريعًا' }),
  strong({ company: 'SkillUp Arabia', website: 'www.skilluparabia.com', city: 'الدمام', sector: 'تدريب',
    signal: 'صفحة تسجيل البرامج تعتمد على نموذج بدون تأكيد متابعة', pain: 'انخفاض نسبة إتمام التسجيل بعد الاستفسار',
    system: 'follow-up-recovery-os', why: 'فجوة بين الاستفسار والتسجيل غالبًا سببها غياب مسار متابعة في الوقت المناسب',
    subject: 'رفع نسبة إتمام التسجيل في SkillUp Arabia', cta: 'احجز مكالمة' }),
  strong({ company: 'Bayan Clinics', website: 'www.bayanclinics.sa', city: 'الرياض', sector: 'عيادات',
    signal: 'الحجز والاستفسار يتمّان عبر واتساب حسب صفحة التواصل', pain: 'محادثات واتساب متفرقة بلا مسار أو تصعيد',
    system: 'whatsapp-client-os', why: 'اعتماد الحجز على واتساب يجعل تنظيم المسارات وبطاقات الإجراء أولوية',
    subject: 'تنظيم واتساب الحجوزات في Bayan Clinics', cta: 'ابدأ تشخيصًا سريعًا' }),
  strong({ company: 'Manazel Real Estate', website: 'www.manazel.sa', city: 'جدة', sector: 'عقار',
    signal: 'إعلانات الوحدات تدعو للتواصل عبر واتساب مباشرة', pain: 'ردود متأخرة على استفسارات الوحدات تضيّع فرص بيع',
    system: 'whatsapp-client-os', why: 'حجم استفسارات واتساب العقارية يحتاج مسارات وسياسة تحويل للإنسان',
    subject: 'تقليل زمن الرد على استفسارات Manazel Real Estate', cta: 'احجز مكالمة 20 دقيقة' }),
  strong({ company: 'CloudShift Consulting', website: 'www.cloudshift.sa', city: 'الرياض', sector: 'خدمات B2B',
    signal: 'صفحة الخدمات تعرض عروضًا مخصصة لكل عميل', pain: 'العروض بطيئة وغير موحّدة وبلا إثبات مقنع',
    system: 'proposal-proof-os', why: 'تكرار العروض المخصصة يستفيد من قالب موحّد و Proof Pack يسرّع القرار',
    subject: 'قالب عرض و Proof Pack لـ CloudShift Consulting', cta: 'ابدأ تشخيصًا سريعًا' }),
  strong({ company: 'Nexus IT Solutions', website: 'www.nexusit.sa', city: 'الخبر', sector: 'خدمات B2B',
    signal: 'دراسات حالة قليلة على الموقع مقابل خدمات متعددة', pain: 'غياب إثبات واضح يطيل دورة إغلاق الصفقة',
    system: 'proposal-proof-os', why: 'تعدد الخدمات مع قلة الإثبات يجعل Proof Pack رافعة مباشرة للإغلاق',
    subject: 'تسريع إغلاق الصفقات في Nexus IT Solutions', cta: 'احجز مكالمة قصيرة' }),
  strong({ company: 'Taqnia Group', website: 'www.taqniagroup.sa', city: 'الرياض', sector: 'مجموعة شركات',
    signal: 'هيكل متعدد الوحدات يظهر في صفحة من نحن', pain: 'القرارات تعتمد على المؤسس بلا تقرير قيادة موحّد',
    system: 'executive-command-os', why: 'تعدد الوحدات يحتاج خريطة مؤشرات وتقرير قيادة يومي لتسريع القرار',
    subject: 'تقرير قيادة يومي لـ Taqnia Group', cta: 'احجز مكالمة' }),
  // medium (drops some fields → ~80s)
  { company: 'Elevate Training', website: 'www.elevate.sa', country: 'SA', city: 'الرياض', sector: 'تدريب',
    signal: 'حملات موسمية معلنة على الموقع', likely_pain: 'فرص الحملات الموسمية تضيع بعد انتهاء الحملة',
    recommended_system: 'follow-up-recovery-os', why_this_system: 'الحملات الموسمية تنتج دفعات استفسارات تحتاج متابعة سريعة',
    first_mission: 'بناء قائمة متابعة لموسم الحملة', proof_angle: 'كم استفسار موسمي بلا متابعة', email_angle: 'استعادة فرص الموسم',
    subject: 'متابعة فرص الموسم في Elevate Training',
    email_body: 'السلام عليكم،\n\nلاحظت أن Elevate Training تطلق حملات موسمية. غالبًا تتراكم استفسارات كثيرة في وقت قصير ثم تضيع المتابعة.\n\nنقترح بناء قائمة متابعة بسيطة تستعيد هذه الفرص. هل نحجز مكالمة قصيرة؟',
    cta: 'احجز مكالمة', risk_level: 'low', evidence_level: 'L1', approval_status: 'draft', send_readiness: 'ready_for_review' },
  // weak drafts (below the 75 gate, by design)
  { company: 'Generic Services Co', recommended_system: 'proposal-proof-os',
    subject: 'عرض خدماتنا', email_body: 'السلام عليكم، نقدم خدمات متنوعة. تواصلوا معنا.',
    cta: 'تواصل', risk_level: 'low', evidence_level: 'L0', approval_status: 'draft', send_readiness: 'not_ready' },
  { company: 'Sample Holding', recommended_system: 'executive-command-os',
    subject: 'تعاون', email_body: 'مرحبا، نحب نتعاون معكم.', cta: 'رد', risk_level: 'medium', evidence_level: 'L0',
    approval_status: 'draft', send_readiness: 'not_ready' },
]

const contactTargets = [
  { company: 'Digital Rise Agency', website: 'www.digitalrise.sa', country: 'SA', city: 'الرياض', sector: 'وكالة تسويق',
    recommended_system: 'revenue-operating-system', best_contact_role: 'Founder / CEO',
    public_contact_channels: ['website-contact-form'], source: 'company website', do_not_contact: false, evidence_level: 'L2' },
  { company: 'TrainMe KSA', website: 'www.trainme.sa', country: 'SA', city: 'الرياض', sector: 'تدريب',
    recommended_system: 'follow-up-recovery-os', best_contact_role: 'Sales Manager',
    public_contact_channels: ['website-whatsapp'], source: 'company website', do_not_contact: false, evidence_level: 'L2' },
  { company: 'Bayan Clinics', website: 'www.bayanclinics.sa', country: 'SA', city: 'الرياض', sector: 'عيادات',
    recommended_system: 'whatsapp-client-os', best_contact_role: 'Operations Manager',
    public_contact_channels: ['website-whatsapp'], source: 'company website', do_not_contact: false, evidence_level: 'L2' },
  { company: 'CloudShift Consulting', website: 'www.cloudshift.sa', country: 'SA', city: 'الرياض', sector: 'خدمات B2B',
    recommended_system: 'proposal-proof-os', best_contact_role: 'Business Development Manager',
    public_contact_channels: ['website-contact-form'], source: 'company website', do_not_contact: false, evidence_level: 'L1' },
  { company: 'Taqnia Group', website: 'www.taqniagroup.sa', country: 'SA', city: 'الرياض', sector: 'مجموعة شركات',
    recommended_system: 'executive-command-os', best_contact_role: 'General Manager',
    public_contact_channels: ['website-contact-form'], source: 'company website', do_not_contact: false, evidence_level: 'L1' },
  // explicit do-not-contact target (must never appear in drafts)
  { company: 'Competitor Agency', website: 'www.competitor.sa', country: 'SA', city: 'الرياض', sector: 'وكالة تسويق',
    recommended_system: 'revenue-operating-system', best_contact_role: 'Founder / CEO',
    public_contact_channels: [], source: 'manual', do_not_contact: true, suppression_reason: 'منافس مباشر', evidence_level: 'L1' },
]

const suppression = [
  { company: 'No-Contact Co', suppression_reason: 'طلب عدم التواصل', added: '2026-06-01' },
  { company: 'Old Client LLC', suppression_reason: 'علاقة قائمة تُدار يدويًا', added: '2026-06-01' },
]

const intelligencePacks = [
  { company: 'Digital Rise Agency', website: 'www.digitalrise.sa', country: 'SA', city: 'الرياض', sector: 'وكالة تسويق',
    public_contact_channels: ['website-contact-form'], likely_decision_maker: 'المؤسس', best_contact_role: 'Founder / CEO',
    signal: 'صفحة الخدمات تركّز على توليد leads للعملاء دون ذكر نظام متابعة داخلي',
    likely_pain: 'leads تصل دون مسار متابعة وقرار يومي', recommended_system: 'revenue-operating-system',
    why_this_system: 'الوكالة تولّد leads وغالبًا تواجه التحدي ذاته داخليًا', first_mission: 'خريطة تسرب الإيراد + مسار متابعة خلال 7–10 أيام',
    proof_angle: 'كم فرصة بلا next action عبر المراحل', email_subject: 'فكرة سريعة لتقليل تسرب الفرص',
    email_draft: 'مسودة بريد مخصصة (انظر data/outreach/email_drafts.jsonl)', call_opener: 'السلام عليكم، معك [الاسم] من Dealix...',
    call_questions: ['كيف تتابعون الفرص حاليًا؟', 'هل يوجد تقرير إيراد دوري؟'], expected_objections: ['لدينا فريق يكفي'],
    mini_proposal_angle: 'Sprint إيراد 7–10 أيام', next_action: 'إرسال بريد مخصص ثم مكالمة', risk_level: 'low', evidence_level: 'L2' },
  { company: 'TrainMe KSA', website: 'www.trainme.sa', country: 'SA', city: 'الرياض', sector: 'تدريب',
    public_contact_channels: ['website-whatsapp'], likely_decision_maker: 'الرئيس التنفيذي', best_contact_role: 'Sales Manager',
    signal: 'واتساب قناة رئيسية للاستفسار عن البرامج', likely_pain: 'استفسارات واتساب تُنسى قبل المتابعة',
    recommended_system: 'follow-up-recovery-os', why_this_system: 'تعدد البرامج مع واتساب يعني استفسارات تحتاج متابعة منظمة',
    first_mission: 'قائمة متابعة + رسائل خلال 7 أيام', proof_angle: 'كم استفسار بلا متابعة', email_subject: 'استعادة الاستفسارات المتروكة',
    email_draft: 'مسودة بريد مخصصة', call_opener: 'السلام عليكم، معك [الاسم] من Dealix...',
    call_questions: ['كم استفسار يصلكم أسبوعيًا؟', 'من يتابع حاليًا؟'], expected_objections: ['نتابع يدويًا'],
    mini_proposal_angle: 'Sprint متابعة 7 أيام', next_action: 'بريد مخصص ثم مكالمة', risk_level: 'low', evidence_level: 'L2' },
  { company: 'Bayan Clinics', website: 'www.bayanclinics.sa', country: 'SA', city: 'الرياض', sector: 'عيادات',
    public_contact_channels: ['website-whatsapp'], likely_decision_maker: 'مدير العمليات', best_contact_role: 'Operations Manager',
    signal: 'الحجز عبر واتساب', likely_pain: 'محادثات واتساب بلا مسار أو تصعيد', recommended_system: 'whatsapp-client-os',
    why_this_system: 'اعتماد الحجز على واتساب يجعل تنظيم المسارات أولوية', first_mission: 'خريطة مسارات + بطاقات إجراء خلال 7–10 أيام',
    proof_angle: 'كم محادثة تحتاج إجراء وتتأخر', email_subject: 'تنظيم واتساب الحجوزات', email_draft: 'مسودة بريد مخصصة',
    call_opener: 'السلام عليكم، معك [الاسم] من Dealix...', call_questions: ['كم محادثة يوميًا؟', 'متى تحوّلون للإنسان؟'],
    expected_objections: ['الموظفات يردّون'], mini_proposal_angle: 'Sprint واتساب 7–10 أيام', next_action: 'بريد ثم مكالمة',
    risk_level: 'low', evidence_level: 'L2' },
  { company: 'CloudShift Consulting', website: 'www.cloudshift.sa', country: 'SA', city: 'الرياض', sector: 'خدمات B2B',
    public_contact_channels: ['website-contact-form'], likely_decision_maker: 'مدير تطوير الأعمال', best_contact_role: 'Business Development Manager',
    signal: 'عروض مخصصة لكل عميل', likely_pain: 'عروض بطيئة وبلا إثبات مقنع', recommended_system: 'proposal-proof-os',
    why_this_system: 'تكرار العروض المخصصة يستفيد من قالب موحّد و Proof Pack', first_mission: 'قالب عرض + Proof Pack خلال 5–7 أيام',
    proof_angle: 'كم تأخذ العروض من وقت', email_subject: 'قالب عرض و Proof Pack', email_draft: 'مسودة بريد مخصصة',
    call_opener: 'السلام عليكم، معك [الاسم] من Dealix...', call_questions: ['كم عرض شهريًا؟', 'ما أكثر اعتراض؟'],
    expected_objections: ['لدينا قالب'], mini_proposal_angle: 'Sprint عرض 5–7 أيام', next_action: 'بريد ثم مكالمة',
    risk_level: 'low', evidence_level: 'L1' },
  { company: 'Taqnia Group', website: 'www.taqniagroup.sa', country: 'SA', city: 'الرياض', sector: 'مجموعة شركات',
    public_contact_channels: ['website-contact-form'], likely_decision_maker: 'المدير العام', best_contact_role: 'General Manager',
    signal: 'هيكل متعدد الوحدات', likely_pain: 'قرارات تعتمد على المؤسس بلا تقرير قيادة موحّد', recommended_system: 'executive-command-os',
    why_this_system: 'تعدد الوحدات يحتاج خريطة مؤشرات وتقرير قيادة يومي', first_mission: 'KPI Map + تقرير قيادة خلال 7–14 يومًا',
    proof_angle: 'كم قرار يتأخر بلا صورة موحدة', email_subject: 'تقرير قيادة يومي', email_draft: 'مسودة بريد مخصصة',
    call_opener: 'السلام عليكم، معك [الاسم] من Dealix...', call_questions: ['ما أهم 3 قرارات أسبوعية؟', 'أين تتابع الأرقام؟'],
    expected_objections: ['لدينا داشبورد'], mini_proposal_angle: 'Sprint قيادة 7–14 يومًا', next_action: 'بريد ثم مكالمة',
    risk_level: 'medium', evidence_level: 'L1' },
]

const needCards = intelligencePacks.map((p) => ({
  company: p.company, sector: p.sector, recommended_system: p.recommended_system,
  likely_pain: p.likely_pain, why_this_system: p.why_this_system, first_mission: p.first_mission,
  proof_angle: p.proof_angle, risk_level: p.risk_level, evidence_level: p.evidence_level,
}))

const callBriefs = [
  { company: 'Digital Rise Agency', contact_role: 'Founder / CEO', recommended_system: 'revenue-operating-system',
    likely_pain: 'leads بلا مسار متابعة وقرار يومي', email_sent_summary: 'بريد عن Sprint يكشف تسرب الإيراد',
    call_objective: 'فهم كيف تُتابع الفرص حاليًا وحجز تشخيص', opening_line: 'السلام عليكم، معك [الاسم] من Dealix. أرسلنا لكم رسالة مختصرة عن نظام تشغيل الإيرادات.',
    discovery_questions: ['كيف تتابعون الفرص اليوم؟', 'هل يوجد تقرير إيراد دوري؟', 'من يقرر الخطوة التالية لكل فرصة؟'],
    expected_objection: 'لدينا فريق يتابع', best_response: 'ممتاز، الهدف ليس استبدال الفريق بل إعطاؤه مسارًا وقرارًا واضحًا يقلّل التسرب.',
    next_step: 'حجز تشخيص 20 دقيقة', evidence_level: 'L2' },
  { company: 'TrainMe KSA', contact_role: 'Sales Manager', recommended_system: 'follow-up-recovery-os',
    likely_pain: 'استفسارات واتساب تُنسى', email_sent_summary: 'بريد عن استعادة الاستفسارات المتروكة',
    call_objective: 'تقدير حجم الاستفسارات وحجز تشخيص', opening_line: 'السلام عليكم، معك [الاسم] من Dealix. تواصلنا بخصوص استعادة المتابعة.',
    discovery_questions: ['كم استفسار يصلكم أسبوعيًا؟', 'من يتابع وكم مرة؟', 'كم تقديريًا يضيع بلا رد؟'],
    expected_objection: 'نتابع يدويًا', best_response: 'المتابعة اليدوية تعمل حتى يزيد الضغط؛ نبني قائمة بسيطة تمنع ضياع الفرصة عند الزحام.',
    next_step: 'تشخيص سريع', evidence_level: 'L2' },
  { company: 'CloudShift Consulting', contact_role: 'Business Development Manager', recommended_system: 'proposal-proof-os',
    likely_pain: 'عروض بطيئة وبلا إثبات', email_sent_summary: 'بريد عن قالب عرض و Proof Pack',
    call_objective: 'فهم دورة العرض الحالية', opening_line: 'السلام عليكم، معك [الاسم] من Dealix بخصوص نظام العروض والإثبات.',
    discovery_questions: ['كم عرضًا تخرجون شهريًا؟', 'كم يأخذ العرض من وقت؟', 'ما أكثر اعتراض يتكرر؟'],
    expected_objection: 'لدينا قالب', best_response: 'القالب بداية جيدة؛ نضيف Proof Pack وتحديد نطاق يقصّر النقاش ويسرّع القرار.',
    next_step: 'مكالمة 20 دقيقة', evidence_level: 'L1' },
]

const miniProposals = [
  { title: 'Sprint استعادة المتابعة — 7 أيام', company: 'TrainMe KSA', recommended_system: 'follow-up-recovery-os',
    why_this_system: 'برامج متعددة وقناة واتساب ظاهرة تعني استفسارات تحتاج متابعة منظمة',
    current_likely_pain: 'استفسارات تدخل وتُنسى قبل المتابعة', first_sprint: 'بناء قائمة متابعة ورسائل حسب حالة العميل',
    deliverables: ['قائمة المتابعة', 'نموذج حالة العميل', 'مجموعة الرسائل', 'تقرير الاستعادة الأسبوعي'],
    timeline: '7 أيام', starter_price: 'يبدأ من 3,500 SAR', required_inputs: ['قائمة الاستفسارات الحالية', 'القنوات المستخدمة'],
    expected_first_proof: 'قائمة متابعة جاهزة + أول دفعة رسائل', next_step: 'مكالمة 20 دقيقة لفهم مصادر الاستفسارات',
    approval_required: true, approval_status: 'pending' },
  { title: 'Sprint العروض والإثبات — 5–7 أيام', company: 'CloudShift Consulting', recommended_system: 'proposal-proof-os',
    why_this_system: 'عروض مخصصة متكررة تستفيد من قالب موحّد و Proof Pack', current_likely_pain: 'عروض بطيئة وبلا إثبات مقنع',
    first_sprint: 'بناء قالب عرض و Proof Pack قابلين لإعادة الاستخدام', deliverables: ['قالب العرض', 'قالب Proof Pack', 'تحديد النطاق', 'بطاقة الخطوة التالية'],
    timeline: '5–7 أيام', starter_price: 'يبدأ من 3,000 SAR', required_inputs: ['مثال عرض حالي', 'أكثر اعتراض متكرر'],
    expected_first_proof: 'قالب عرض جاهز للاستخدام', next_step: 'مكالمة قصيرة', approval_required: true, approval_status: 'approved' },
  { title: 'Sprint تشغيل الإيرادات — 7–10 أيام', company: 'Digital Rise Agency', recommended_system: 'revenue-operating-system',
    why_this_system: 'وكالة تولّد leads وتحتاج مسار متابعة وقرار يومي داخلي', current_likely_pain: 'leads بلا next action واضح',
    first_sprint: 'خريطة تسرب الإيراد ومسار متابعة', deliverables: ['خريطة تسرب الإيراد', 'نموذج مراحل الفرص', 'مسار المتابعة', 'تقرير الإيراد'],
    timeline: '7–10 أيام', starter_price: 'يبدأ من 4,500 SAR', required_inputs: ['قائمة الفرص الحالية', 'قنوات الاستفسار'],
    expected_first_proof: 'خريطة تسرب أولى', next_step: 'تشخيص 20 دقيقة', approval_required: true, approval_status: 'pending' },
]

const followUpSequences = [
  { sequence_id: 'fu-revenue-no-reply', recommended_system: 'revenue-operating-system', lead_status: 'no_reply', channel: 'email',
    steps: [
      { order: 1, wait_days: 3, subject: 'متابعة بسيطة', message_draft: 'مرحبًا، أعيد إرسال رسالتي السابقة تحسبًا لانشغالكم. هل تفضّلون مكالمة قصيرة؟', goal: 'تذكير لطيف' },
      { order: 2, wait_days: 4, subject: 'فكرة عملية', message_draft: 'أرفقت مثالًا مختصرًا لكيفية كشف تسرب الإيراد. هل أرسل لكم تشخيصًا سريعًا؟', goal: 'تقديم قيمة' },
      { order: 3, wait_days: 5, subject: 'أغلق الملف؟', message_draft: 'إذا التوقيت غير مناسب، أغلق المتابعة الآن وأعود لاحقًا. فقط ردّوا بكلمة.', goal: 'إغلاق محترم' },
    ], stop_conditions: ['رد العميل', 'طلب عدم التواصل'] },
  { sequence_id: 'fu-followup-quiet', recommended_system: 'follow-up-recovery-os', lead_status: 'gone_quiet', channel: 'email',
    steps: [
      { order: 1, wait_days: 2, subject: 'نكمل؟', message_draft: 'مرحبًا، نتوقف عند نقطة جيدة. هل نكمل ترتيب قائمة المتابعة؟', goal: 'إعادة تفعيل' },
      { order: 2, wait_days: 4, subject: 'مثال سريع', message_draft: 'هذا نموذج قائمة متابعة بسيط يناسب حجمكم. هل نطبّقه في تشخيص قصير؟', goal: 'تقديم قيمة' },
    ], stop_conditions: ['رد العميل', 'حجز مكالمة'] },
]

const objectionResponses = [
  { objection_id: 'price', objection: 'السعر مرتفع', applies_to_systems: [],
    response: 'نبدأ بـ Sprint صغير محدد النطاق لتروا القيمة قبل أي التزام أكبر.', reframe: 'القيمة مقابل تسرب الفرص الحالي', proof_to_offer: 'أول مخرج خلال أيام', avoid: 'وعود بعائد محدد' },
  { objection_id: 'timing', objection: 'ليس الوقت المناسب', applies_to_systems: [],
    response: 'مفهوم. نحدد موعدًا لاحقًا، وأترك لكم تشخيصًا مختصرًا تستفيدون منه الآن.', reframe: 'خطوة صغيرة بدل مشروع كبير', proof_to_offer: 'تشخيص مجاني مختصر', avoid: 'إلحاح' },
  { objection_id: 'have-someone', objection: 'لدينا من يقوم بذلك', applies_to_systems: [],
    response: 'ممتاز، الهدف دعم فريقكم بمسار وقرار أوضح لا استبداله.', reframe: 'تمكين الفريق', proof_to_offer: 'قالب جاهز للتجربة', avoid: 'انتقاد الفريق' },
  { objection_id: 'no-system', objection: 'ليس لدينا نظام أصلًا', applies_to_systems: ['follow-up-recovery-os'],
    response: 'هذا الوضع الأنسب للبدء؛ نبني بنية بسيطة قابلة للتشغيل فورًا.', reframe: 'نبدأ من الصفر بوضوح', proof_to_offer: 'مخرج أول سريع', avoid: 'تعقيد' },
  { objection_id: 'data-pdpl', objection: 'ماذا عن خصوصية البيانات؟', applies_to_systems: [],
    response: 'نعمل على بيانات عامة أو ما تزوّدوننا به فقط، وبدون أي بيانات حساسة في السجلات.', reframe: 'حوكمة واضحة', proof_to_offer: 'سياسة البيانات', avoid: 'تجاوز الخصوصية' },
  { objection_id: 'send-info', objection: 'أرسل لي معلومات', applies_to_systems: [],
    response: 'بكل سرور، وأقترح مكالمة 15 دقيقة بعدها لنخصص ما يناسبكم بدل معلومات عامة.', reframe: 'تخصيص بدل عمومية', proof_to_offer: 'ملخص نظام مختصر', avoid: 'اختفاء بعد الإرسال' },
]

const pipelines = [
  { pipeline_id: 'pl-001', company: 'CloudShift Consulting', recommended_system: 'proposal-proof-os', state: 'won',
    owner: 'founder', starter_price_sar: 3000, required_inputs_received: false, blockers: ['بانتظار مثال عرض حالي من العميل'],
    created_at: '2026-05-28', updated_at: '2026-06-02' },
  { pipeline_id: 'pl-002', company: 'TrainMe KSA', recommended_system: 'follow-up-recovery-os', state: 'mini_proposal_ready',
    owner: 'founder', starter_price_sar: 3500, required_inputs_received: false, blockers: [], created_at: '2026-05-30', updated_at: '2026-06-02' },
  { pipeline_id: 'pl-003', company: 'Bayan Clinics', recommended_system: 'whatsapp-client-os', state: 'delivery_started',
    owner: 'founder', starter_price_sar: 4500, required_inputs_received: true, blockers: [], created_at: '2026-05-20', updated_at: '2026-06-02' },
  { pipeline_id: 'pl-004', company: 'Digital Rise Agency', recommended_system: 'revenue-operating-system', state: 'qualified',
    owner: 'founder', starter_price_sar: 4500, required_inputs_received: false, blockers: [], created_at: '2026-06-01', updated_at: '2026-06-02' },
  { pipeline_id: 'pl-005', company: 'Manazel Real Estate', recommended_system: 'whatsapp-client-os', state: 'first_output_ready',
    owner: 'founder', starter_price_sar: 4500, required_inputs_received: true, blockers: [], created_at: '2026-05-18', updated_at: '2026-06-01' },
  { pipeline_id: 'pl-006', company: 'SkillUp Arabia', recommended_system: 'follow-up-recovery-os', state: 'intake_required',
    owner: 'founder', starter_price_sar: 3500, required_inputs_received: false, blockers: ['بانتظار قائمة الاستفسارات الحالية'],
    created_at: '2026-06-01', updated_at: '2026-06-02' },
]

const tasks = [
  { task_id: 't-001', pipeline_id: 'pl-003', recommended_system: 'whatsapp-client-os', title: 'بناء خريطة مسارات واتساب', deliverable: 'WhatsApp Flow Map', status: 'done' },
  { task_id: 't-002', pipeline_id: 'pl-003', recommended_system: 'whatsapp-client-os', title: 'إنشاء بطاقات الإجراء', deliverable: 'Action Cards', status: 'in_progress' },
  { task_id: 't-003', pipeline_id: 'pl-003', recommended_system: 'whatsapp-client-os', title: 'سياسة التحويل للإنسان', deliverable: 'Human Handoff Policy', status: 'todo' },
  { task_id: 't-004', pipeline_id: 'pl-005', recommended_system: 'whatsapp-client-os', title: 'مراجعة المخرج الأول مع العميل', deliverable: 'Readiness Scan', status: 'in_progress' },
  { task_id: 't-005', pipeline_id: 'pl-001', recommended_system: 'proposal-proof-os', title: 'تجهيز قالب العرض', deliverable: 'Proposal Template', status: 'blocked', blocker_reason: 'بانتظار مثال عرض حالي' },
  { task_id: 't-006', pipeline_id: 'pl-001', recommended_system: 'proposal-proof-os', title: 'بناء Proof Pack', deliverable: 'Proof Pack Template', status: 'todo' },
]

const weeklyValueReports = [
  { report_id: 'wvr-001', pipeline_id: 'pl-003', company: 'Bayan Clinics', recommended_system: 'whatsapp-client-os', week_of: '2026-05-26',
    delivered_this_week: ['خريطة مسارات واتساب الأولى', 'مسودة بطاقات الإجراء'],
    evidence: ['تغطية 4 أنواع محادثات في الخريطة', 'تحديد نقطتي تأخر في الرد'],
    next_week_focus: ['إكمال بطاقات الإجراء', 'سياسة التحويل للإنسان'], client_inputs_needed: ['عينة محادثات أسبوع'], renewal_signal: false },
  { report_id: 'wvr-002', pipeline_id: 'pl-005', company: 'Manazel Real Estate', recommended_system: 'whatsapp-client-os', week_of: '2026-05-26',
    delivered_this_week: ['فحص الجاهزية', 'المخرج الأول لمسارات الاستفسار'],
    evidence: ['توثيق زمن الرد الحالي كخط أساس'], next_week_focus: ['مراجعة العميل للمخرج الأول'], client_inputs_needed: [], renewal_signal: true },
]

const acceptanceGates = [
  { gate_id: 'ag-001', pipeline_id: 'pl-003', recommended_system: 'whatsapp-client-os',
    criteria: [
      { criterion: 'كل نوع محادثة له مسار وبطاقة إجراء', met: false },
      { criterion: 'سياسة التحويل للإنسان واضحة ومطبّقة', met: false },
      { criterion: 'أول مراجعة أسبوعية تم تسليمها', met: true },
    ], all_met: false, client_signed_off: false },
  { gate_id: 'ag-002', pipeline_id: 'pl-005', recommended_system: 'whatsapp-client-os',
    criteria: [
      { criterion: 'لا توجد محادثة مهمة بلا مسار', met: true },
      { criterion: 'أول مراجعة أسبوعية تم تسليمها', met: true },
    ], all_met: true, client_signed_off: false },
]

console.log('Seeding sample data…')
write('data/outreach/email_drafts.jsonl', emailDrafts)
write('data/acquisition/contact_targets.jsonl', contactTargets)
write('data/acquisition/suppression_list.jsonl', suppression)
write('data/acquisition/company_intelligence_packs.jsonl', intelligencePacks)
write('data/acquisition/client_need_cards.jsonl', needCards)
write('data/acquisition/call_briefs.jsonl', callBriefs)
write('data/acquisition/mini_proposals.jsonl', miniProposals)
write('data/acquisition/follow_up_sequences.jsonl', followUpSequences)
write('data/acquisition/objection_responses.jsonl', objectionResponses)
write('data/delivery/pipelines.jsonl', pipelines)
write('data/delivery/tasks.jsonl', tasks)
write('data/delivery/weekly_value_reports.jsonl', weeklyValueReports)
write('data/delivery/acceptance_gates.jsonl', acceptanceGates)
console.log('Done.')
