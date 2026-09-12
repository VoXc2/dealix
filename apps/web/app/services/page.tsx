import { TrackedLink } from "@/components/analytics/TrackedLink";

const solutionGroups = [
  {
    id: "strategy",
    label: "01 · STRATEGY & TRANSFORMATION",
    title: "من الاستراتيجية إلى operating model قابل للتنفيذ",
    buyer: "CEO / Founder / GM / Strategy / Transformation",
    capabilities: [
      "Growth & Revenue Strategy",
      "AI Transformation Roadmap",
      "Operating Model & Decision Architecture",
      "Execution Diagnostic & Value Baseline",
      "Executive Command System",
    ],
    outcome: "أولويات أقل، owners أوضح، economics قابلة للقياس، ومسار تنفيذ يربط القرار بالدليل.",
  },
  {
    id: "systems",
    label: "02 · SYSTEMS & AUTOMATION",
    title: "AI systems وautomation فوق الأدوات الحالية",
    buyer: "COO / CIO / CTO / Commercial / Operations",
    capabilities: [
      "Revenue Command & Follow-up Recovery",
      "Company Brain & Knowledge Operations",
      "Governed AI Agents & Workflow Automation",
      "Connector Reliability & Integration Ops",
      "Omnichannel Customer Experience Command",
    ],
    outcome: "خفض الأعمال اليدوية والتسرب التشغيلي مع approval boundaries وreceipts واضحة.",
  },
  {
    id: "intelligence",
    label: "03 · INTELLIGENCE & MARKET ACCESS",
    title: "ذكاء سوق سعودي يتحول إلى قرار تجاري",
    buyer: "Growth / BD / Market Entry / Partners / Enterprise Sales",
    capabilities: [
      "Saudi Opportunity Radar",
      "Saudi Market Access Sprint",
      "Partner / Distributor Desk",
      "Tender & B2G Intelligence",
      "Sector & Regulatory Signal Monitoring",
    ],
    outcome: "تركيز البحث على الفرص والمسارات التي تستحق الوقت بدل تجميع leads أو أخبار بلا قرار.",
  },
  {
    id: "trust",
    label: "04 · TRUST, GOVERNANCE & PROOF",
    title: "حوكمة وProof كطبقة تشغيل وليست ملف PDF",
    buyer: "Risk / Compliance / AI Owner / IT / Delivery",
    capabilities: [
      "AI Governance Readiness",
      "Agent Reliability & Control Assessment",
      "PDPL/Data Operations Workflows",
      "Proof Pack as a Service",
      "Operational Evidence & Reliability Reviews",
    ],
    outcome: "حدود صلاحية وإثبات قابلة للمراجعة بدون ادعاء certification أو compliance غير مثبت.",
  },
];

const products = [
  {
    title: "Dealix OS",
    text: "المنتج الرئيسي: AI Business Operating System يربط Company Brain وOpportunity Graph وAction/Approval وProof Ledger فوق stack العميل.",
    href: "/dealix-os",
    ctaId: "services_product_dealix_os",
  },
  {
    title: "Data & Intelligence Products",
    text: "يتحول الرصد والـdecision intelligence المتكرر إلى feeds، subscriptions وenterprise intelligence عندما يثبت استخدام متكرر وقيمة اقتصادية.",
    href: "/company#products",
    ctaId: "services_product_intelligence",
  },
  {
    title: "Productized Services",
    text: "نحوّل المشاكل المتكررة المثبتة إلى diagnostics وsprints وmanaged operations ذات نطاق واضح قبل تحويلها إلى software.",
    href: "/company#products",
    ctaId: "services_productized_services",
  },
];

const saudiWedges = [
  {
    title: "ZATCA / Fatoora Readiness",
    text: "تشخيص مجاني لفجوات المرحلة الثانية: notification، ERP/integration، owners، testing، exception handling وevidence. لا نمنح حكمًا ضريبيًا أو شهادة امتثال.",
    href: "/zatca-fatoora-readiness",
    ctaId: "services_zatca_readiness",
  },
  {
    title: "AI Governance Readiness",
    text: "تشخيص مجاني لـAI ownership، data/model inventory، approval boundaries وevidence pack مع فصل readiness عن أي اعتماد تنظيمي رسمي.",
    href: "/ai-governance-readiness",
    ctaId: "services_ai_governance_readiness",
  },
];

export default function ServicesPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Strategic B2B Solutions</p>
        <h1>Dealix ليست قائمة خدمات AI. هي طبقة استراتيجية وتنفيذية للشركات.</h1>
        <p style={{ maxWidth: 860, margin: "0 auto" }}>
          نعمل من المشكلة الاقتصادية أو التشغيلية إلى strategy، system، intelligence وproof. Dealix OS منتج داخل هذه المنظومة، وليس تعريف الشركة بالكامل.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="services_execution_diagnostic" surface="services_hero">ابدأ Execution Diagnostic</TrackedLink>
          <TrackedLink href="/company" ctaId="services_to_company" surface="services_hero">افهم نموذج الشركة</TrackedLink>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">SAUDI MONEY-NOW WEDGES</p>
        <h2>ابدأ من ضغط تنفيذي حقيقي، ثم اثبت القيمة قبل التوسع.</h2>
        <div className="cards">
          {saudiWedges.map((wedge) => (
            <article className="card" key={wedge.title}>
              <h3>{wedge.title}</h3>
              <p>{wedge.text}</p>
              <TrackedLink href={wedge.href} ctaId={wedge.ctaId} surface="services_saudi_wedges">افتح التشخيص</TrackedLink>
            </article>
          ))}
        </div>
      </section>

      {solutionGroups.map((group) => (
        <section className="card" id={group.id} key={group.id}>
          <p className="eyebrow">{group.label}</p>
          <h2>{group.title}</h2>
          <p><strong>Buyer:</strong> {group.buyer}</p>
          <div className="cards" style={{ marginTop: "var(--sp-5)" }}>
            {group.capabilities.map((capability) => (
              <article className="card" key={capability}><h3>{capability}</h3></article>
            ))}
          </div>
          <p style={{ marginTop: "var(--sp-5)" }}><strong>Outcome:</strong> {group.outcome}</p>
        </section>
      ))}

      <section className="card card-gold">
        <p className="eyebrow">Products & Scalable Assets</p>
        <h2>نبني الخدمات أولًا حول evidence، ثم نحوّل المتكرر إلى منتجات.</h2>
        <div className="cards">
          {products.map((product) => (
            <article className="card" key={product.title}>
              <h3>{product.title}</h3>
              <p>{product.text}</p>
              <TrackedLink href={product.href} ctaId={product.ctaId} surface="services_products">اعرف أكثر</TrackedLink>
            </article>
          ))}
        </div>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Engagement Path</p>
        <h2>Diagnostic → Discovery → Customer-Specific Sprint → Proof → Retainer / Product</h2>
        <p style={{ maxWidth: 740, margin: "0 auto" }}>
          لا يوجد fixed public pricing أو promise موحد لكل شركة. السعر والنطاق يتبعان المشكلة والبيانات والـrisk والنتيجة المقبولة بعد Qualified Discovery.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="services_bottom_diagnostic" surface="services_bottom">ابدأ التشخيص</TrackedLink>
          <TrackedLink href="/proof-vault" ctaId="services_to_proof" surface="services_bottom">شاهد Proof Model</TrackedLink>
        </div>
      </section>
    </main>
  );
}
