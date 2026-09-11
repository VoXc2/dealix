import { TrackedLink } from "@/components/analytics/TrackedLink";

const practices = [
  {
    title: "Strategy & Transformation",
    text: "Strategic operating models, growth architecture, transformation priorities and executive decision systems tied to measurable business movement.",
  },
  {
    title: "Systems & Automation",
    text: "AI systems, workflow automation, integrations, governed agents and reliability layers that operate above the client's existing stack.",
  },
  {
    title: "Intelligence & Market Access",
    text: "Saudi market intelligence, opportunity radar, partner routes, B2B research and decision support grounded in source evidence.",
  },
  {
    title: "Products & Ventures",
    text: "Repeatable proven capabilities become software, APIs, data products and scalable operating assets. Dealix OS is the flagship product in this layer.",
  },
];

const operatingLaws = [
  "One Company Machine — no duplicate CRM, Company Brain, scheduler or approval authority.",
  "Evidence before claims — research does not become relationship, consent, revenue or customer proof.",
  "Sell before build — validate buyer pain and commercial movement before deep productization.",
  "Governed autonomy — low-risk internal work can automate; material external actions remain action-bound.",
];

export default function CompanyPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Dealix Company</p>
        <h1>شركة سعودية تبني الاستراتيجية والأنظمة والذكاء والمنتجات حول نتيجة واحدة: تنفيذ يمكن إثباته.</h1>
        <p style={{ maxWidth: 820, margin: "0 auto" }}>
          Dealix ليست مجرد منصة أو وكالة أتمتة. هي B2B operating company تجمع الاستراتيجية والتنفيذ والذكاء والمنتجات في منظومة واحدة، وتستخدم Dealix OS كمنتج رئيسي حين تكون طبقة تشغيل مستمرة هي الحل الصحيح.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/services" ctaId="company_to_services" surface="company_hero">استكشف الحلول الاستراتيجية</TrackedLink>
          <TrackedLink href="/dealix-os" ctaId="company_to_dealix_os" surface="company_hero">استكشف Dealix OS</TrackedLink>
        </div>
      </section>

      <section className="cards" id="products">
        {practices.map((practice) => (
          <article className="card" key={practice.title}>
            <h2 style={{ fontSize: "1.45rem" }}>{practice.title}</h2>
            <p>{practice.text}</p>
          </article>
        ))}
      </section>

      <section className="card">
        <p className="eyebrow">Operating Law</p>
        <h2>سرعة بدون فوضى تشغيلية</h2>
        <ul>
          {operatingLaws.map((law) => <li key={law}>{law}</li>)}
        </ul>
      </section>

      <section className="card card-gold" style={{ textAlign: "center" }}>
        <p className="eyebrow">How we engage</p>
        <h2>نبدأ بمشكلة تجارية أو تشغيلية واحدة، لا بقائمة منتجات.</h2>
        <p style={{ maxWidth: 720, margin: "0 auto" }}>
          Execution Diagnostic → Qualified Discovery → Customer-Specific Outcome Sprint → Proof Review → Retainer أو Dealix OS عندما يثبت التكرار.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="company_execution_diagnostic" surface="company_engagement">ابدأ Execution Diagnostic</TrackedLink>
        </div>
      </section>
    </main>
  );
}
