import type { Metadata } from "next";
import { TrackedLink } from "@/components/analytics/TrackedLink";

export const metadata: Metadata = {
  title: "Saudi Opportunity Radar | Dealix",
  description:
    "Fresh Saudi regulatory and market signals translated into evidence-governed B2B diagnostics. Public signals are research, not buyer intent or customer proof.",
};

const signals = [
  {
    authority: "Ministry of Commerce",
    id: "moc-business-q2-2026",
    title: "Q2 2026 · نمو قاعدة الأعمال وإشارات التجارة الإلكترونية والسحابة",
    observed: "9 يوليو 2026",
    deadline: "إشارة سوق حالية — ليست موعدًا تنظيميًا لعميل بعينه",
    who: "شركات سعودية في قطاعات متعددة، مع إشارات رسمية إلى السياحة والتجارة الإلكترونية والحوسبة السحابية ضمن الأنشطة الواعدة.",
    diagnostic: "Free operations diagnostic: اختر workflow واحدًا عالي الاحتكاك في revenue/operations/customer service، حدّد baseline والأدلة والتكاملات، ثم اختبر جدوى automation/AI قبل أي scope مدفوع.",
    boundary: "71k+ سجل جديد و1.91m+ سجل قائم يثبتان نشاطًا اقتصاديًا واسعًا، لا يثبتان buyer intent أو relationship أو budget لشركة محددة.",
    source: "https://mc.gov.sa/ar/mediacenter/News/Pages/09-07-26-01.aspx",
  },
  {
    authority: "ZATCA",
    id: "zatca-wave25",
    title: "Wave 25 · مرحلة الربط والتكامل للفوترة الإلكترونية",
    observed: "24 يوليو 2026",
    deadline: "الربط بحد أقصى 1 فبراير 2027 للمنشآت التي تم إشعارها ضمن الموجة",
    who: "منشآت تجاوزت إيراداتها الخاضعة لضريبة القيمة المضافة 187,500 ر.س في أي من 2022–2025، وفق إعلان زاتكا، مع ضرورة التحقق من الإشعار الفعلي لكل منشأة.",
    diagnostic: "Free Fatoora applicability & readiness diagnostic: إشعار الموجة، وضع ERP/الفوترة، فجوات التكامل، evidence المطلوبة، وخارطة remediation أولية.",
    boundary: "لا رأي ضريبي أو شهادة امتثال أو ادعاء اعتماد من زاتكا. أي opinion تنظيمي متخصص يمر عبر جهة مؤهلة عند الحاجة.",
    source: "https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx",
  },
  {
    authority: "CST",
    id: "cst-ai-adoption",
    title: "دليل تبني الذكاء الاصطناعي لدى الشركات التقنية",
    observed: "2026",
    deadline: "إشارة جاهزية حالية ضمن عام 2026",
    who: "شركات التقنية التي تحوّل AI من توجه استراتيجي إلى تشغيل داخلي أو حلول موجهة للعملاء أو AI agents.",
    diagnostic: "Free AI readiness diagnostic عبر الأبعاد الواردة في الدليل: السياق، البيانات، البنية التحتية، المهارات والخبرات، والثقافة المؤسسية.",
    boundary: "تقييم جاهزية وهندسة أدلة، وليس certification أو ضمان نجاح مبادرة AI أو إثبات أن شركة بعينها تريد الشراء.",
    source: "https://www.cst.gov.sa/knowledge-center/reports/ai-adoption-guide-for-tech-companies",
  },
  {
    authority: "GASTAT",
    id: "gastat-tourism-q1-2026",
    title: "Tourism Establishments · بيانات المنشآت السياحية للربع الأول 2026",
    observed: "5 يوليو 2026",
    deadline: "مصدر إحصائي دوري — يستخدم لتحديث فرضيات القطاع لا لخلق pipeline",
    who: "منشآت الضيافة والسياحة التي تحتاج تحسين workflows مرتبطة بالحجز، خدمة العملاء، التشغيل، المعرفة، التقارير أو back-office.",
    diagnostic: "Free hospitality workflow diagnostic: اختر عملية واحدة، افصل baseline عن الافتراضات، ارسم الأنظمة والبيانات، ثم حدّد automation/AI hypothesis ومعيار قبول قابل للقياس.",
    boundary: "وجود بيانات رسمية حديثة عن القطاع لا يثبت ألمًا أو ميزانية أو قرار شراء لدى منشأة محددة.",
    source: "https://www.stats.gov.sa/ar/statistics-tabs/-/categories/124304?category=124304&tab=436312",
  },
  {
    authority: "GASTAT",
    id: "gastat-construction-cost-2026",
    title: "Construction Cost Index · مصدر حديث لسياق ضغط التكلفة في البناء",
    observed: "2026",
    deadline: "نشرات شهرية مستمرة؛ يجب تحديث القراءة قبل أي proposal مادي",
    who: "مقاولو EPC والبناء وسلاسل التوريد والمشتريات ممن قد يواجهون احتكاكًا في RFI/change orders/procurement/approvals/document control.",
    diagnostic: "Free construction operations diagnostic: baseline لزمن دورة RFI/اعتماد/تغيير/شراء، مسار المستندات، مصادر الحقيقة، ثم hypothesis واحدة قابلة للإثبات.",
    boundary: "المؤشر مصدر لسياق تكلفة المدخلات؛ لا يثبت حجم العقود أو ROI للأتمتة أو demand لدى عميل بعينه.",
    source: "https://www.stats.gov.sa/en/statistics-tabs?category=3453505&delta=20&start=1&tab=436312",
  },
  {
    authority: "NCA",
    id: "nca-ncnicc",
    title: "NCNICC · ضوابط الأمن السيبراني للقطاع الخاص غير CNI",
    observed: "مرجع قائم — تحقق 13 سبتمبر 2026",
    deadline: "مرجع تنظيمي قائم؛ يلزم التحقق من الانطباق على كل منشأة",
    who: "جهات القطاع الخاص من غير ذوات البنى التحتية الحساسة التي تحتاج فهم applicability والأدلة التشغيلية المطلوبة.",
    diagnostic: "Free cybersecurity evidence-readiness diagnostic: نطاق الانطباق، evidence matrix، gaps، owners، وأولوية المعالجة.",
    boundary: "لا اعتماد أو شهادة أو ادعاء وصول حكومي. عند الحاجة لسلطة تخصصية نستخدم partner-or-no-bid.",
    source: "https://nca.gov.sa/ar/regulatory-documents/controls-list/ncnicc/",
  },
  {
    authority: "SAMA",
    id: "sama-open-banking",
    title: "Open Banking · انتقال السوق إلى مرحلة الترخيص",
    observed: "26 مارس 2026",
    deadline: "إشارة سوق/ترخيص حالية؛ أي نشاط منظم يتطلب الجهة المرخصة المناسبة",
    who: "Fintechs والبنوك وشركاؤهم التقنيون ممن يبنون قدرات أو تكاملات مرتبطة بخدمات Open Banking.",
    diagnostic: "Free partner-first technical readiness diagnostic: architecture، data/control boundaries، integration risks، ومسار الشريك المرخص.",
    boundary: "Dealix لا تمثل نفسها كمقدم Open Banking مرخص من SAMA؛ الدعم محصور في نطاق تقني غير مرخص وخلف شريك مناسب عند اللزوم.",
    source: "https://sama.gov.sa/en-US/MediaCenter/News/pages/news-1135.aspx",
  },
] as const;

export default function SaudiOpportunityRadarPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">SAUDI OPPORTUNITY RADAR · OFFICIAL-SOURCE FIRST</p>
        <h1>إشارات سعودية حديثة تتحول إلى تشخيص تجاري وتشغيلي — بدون اختراع طلب عميل.</h1>
        <p style={{ maxWidth: 880, margin: "0 auto" }}>
          هذا الرادار يترجم الإشارات التنظيمية والرسمية العامة إلى أسئلة تنفيذ قابلة للفحص. <strong>Public signal ≠ buyer intent ≠ relationship ≠ consent ≠ pipeline ≠ revenue.</strong>
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book?source=saudi-opportunity-radar" ctaId="saudi_radar_free_diagnostic" surface="saudi_opportunity_radar_hero">
            ابدأ Free Diagnostic — بدون بطاقة
          </TrackedLink>
          <TrackedLink href="/services#intelligence" ctaId="saudi_radar_services" surface="saudi_opportunity_radar_hero">
            شاهد Intelligence & Market Access
          </TrackedLink>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">CURRENT OFFICIAL SIGNALS · VERIFIED 13 SEP 2026</p>
        <h2>{signals.length} إشارات عامة قابلة للتحويل إلى readiness work واضح — لا إلى pipeline تلقائي.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-5)" }}>
          {signals.map((signal) => (
            <article className="card" id={signal.id} key={signal.id}>
              <p className="eyebrow">{signal.authority} · {signal.observed}</p>
              <h3>{signal.title}</h3>
              <p><strong>عامل الزمن:</strong> {signal.deadline}</p>
              <p><strong>من قد يتأثر:</strong> {signal.who}</p>
              <p><strong>ما الذي تستطيع Dealix فحصه مجانًا:</strong> {signal.diagnostic}</p>
              <p><strong>الحد:</strong> {signal.boundary}</p>
              <p>
                <a href={signal.source} target="_blank" rel="noreferrer">المصدر الرسمي ↗</a>
              </p>
              <TrackedLink
                href={`/book?source=saudi-opportunity-radar&signal=${signal.id}`}
                ctaId={`saudi_radar_${signal.id}`}
                surface="saudi_opportunity_radar_signal"
              >
                ابدأ التشخيص المجاني لهذا السياق
              </TrackedLink>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-cyan">
        <p className="eyebrow">TRUTH FIREWALL</p>
        <h2>الإشارة الرسمية دليل على تغير البيئة — وليست دليلًا أن شركة بعينها تريد الشراء.</h2>
        <div className="cards">
          <article className="card"><h3>Research ≠ Relationship</h3><p>لا نرقّي خبرًا أو قائمة عامة إلى فرصة مبيعات أو consent.</p></article>
          <article className="card"><h3>Readiness ≠ Certification</h3><p>نبني gap/evidence/remediation work؛ لا نصدر اعتمادًا تنظيميًا ولا رأيًا قانونيًا أو ضريبيًا.</p></article>
          <article className="card"><h3>Diagnostic ≠ Quote</h3><p>كل التشخيصات هنا مجانية. العرض والسعر والنطاق لا يظهران إلا بعد Qualified Discovery خاص بالعميل.</p></article>
        </div>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">FROM SIGNAL TO VERIFIED MOVEMENT</p>
        <h2>Official Signal → Free Diagnostic → Qualified Problem → Discovery → Customer-Specific Scope → Proof</h2>
        <p style={{ maxWidth: 760, margin: "0 auto" }}>
          إذا لم توجد حالة قابلة للقياس نتوقف. وإذا وجدت، نحدد owner وbaseline وacceptance criteria قبل أي التزام مدفوع.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book?source=saudi-opportunity-radar-bottom" ctaId="saudi_radar_bottom_diagnostic" surface="saudi_opportunity_radar_bottom">
            ابدأ Free Execution Diagnostic
          </TrackedLink>
          <TrackedLink href="/proof-vault" ctaId="saudi_radar_proof" surface="saudi_opportunity_radar_bottom">
            شاهد Proof Model
          </TrackedLink>
        </div>
      </section>
    </main>
  );
}
