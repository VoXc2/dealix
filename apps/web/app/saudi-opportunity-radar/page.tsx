import type { Metadata } from "next";
import { TrackedLink } from "@/components/analytics/TrackedLink";

export const metadata: Metadata = {
  title: "Saudi Opportunity Radar | Dealix",
  description:
    "Fresh Saudi regulatory and market signals translated into evidence-governed B2B diagnostics. Public signals are research, not buyer intent or customer proof.",
};

const signals = [
  {
    authority: "ZATCA",
    id: "zatca-wave25",
    title: "Wave 25 · مرحلة الربط والتكامل للفوترة الإلكترونية",
    observed: "24 يوليو 2026",
    deadline: "الربط بحد أقصى 1 فبراير 2027",
    who: "منشآت تجاوزت إيراداتها الخاضعة لضريبة القيمة المضافة 187,500 ر.س في أي من 2022–2025، وفق إعلان زاتكا.",
    diagnostic: "Free Fatoora applicability & readiness diagnostic: إشعار الموجة، وضع ERP/الفوترة، فجوات التكامل، evidence المطلوبة، وخارطة remediation أولية.",
    boundary: "لا رأي ضريبي أو شهادة امتثال. أي opinion تنظيمي متخصص يمر عبر جهة مؤهلة عند الحاجة.",
    source: "https://zatca.gov.sa/ar/MediaCenter/News/Pages/Wave25-E-invoicing.aspx",
  },
  {
    authority: "CST",
    id: "cst-ai-adoption",
    title: "دليل تبني الذكاء الاصطناعي لدى الشركات التقنية",
    observed: "27 يوليو 2026",
    deadline: "إشارة جاهزية حالية ضمن عام الذكاء الاصطناعي 2026",
    who: "شركات التقنية التي تحوّل AI من توجه استراتيجي إلى تشغيل داخلي أو حلول موجهة للعملاء أو AI agents.",
    diagnostic: "Free AI readiness diagnostic عبر الأبعاد الخمسة في الدليل: السياق، البيانات، البنية التحتية، المهارات والخبرات، والثقافة المؤسسية.",
    boundary: "تقييم جاهزية وهندسة أدلة، وليس certification أو ضمان نجاح مبادرة AI.",
    source: "https://www.cst.gov.sa/knowledge-center/reports/ai-adoption-guide-for-tech-companies",
  },
  {
    authority: "NCA",
    id: "nca-ncnicc",
    title: "NCNICC · ضوابط الأمن السيبراني للقطاع الخاص غير CNI",
    observed: "28 ديسمبر 2025",
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
        <p className="eyebrow">CURRENT OFFICIAL SIGNALS</p>
        <h2>أربع إشارات قابلة للتحويل إلى readiness work واضح.</h2>
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

      <section className="card card-gold">
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
