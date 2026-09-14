import Link from "next/link";

const modules = [
  ["Company Brain Map", "يربط الإيراد، العملاء، القنوات، المخاطر، والتسليم في خريطة قرار واحدة."],
  ["Revenue Command Room", "يعرض الفرص الساخنة، المتابعات المتأخرة، العروض المفتوحة، وأولويات اليوم."],
  ["Follow-up Recovery", "يحوّل المحادثات والاستفسارات إلى queue مراجعة واضحة."],
  ["Proposal Co-Pilot", "يحمي النطاق أثناء التفاوض ويقترح trade-offs بدل التخفيض العشوائي."],
  ["Client Delivery OS", "يوحد intake، scope، acceptance criteria، proof pack، والتجديد."],
  ["AI Trust OS", "يضيف policies وapproval gates وسجل مراجعة للمخرجات الحساسة."],
];

const buyerAngles = [
  ["CEO / Founder", "قرار يومي واضح بدل متابعة الفريق يدويًا."],
  ["Sales Director", "Pipeline وfollow-up visible بدون ضياع العروض."],
  ["Operations Manager", "تسليم منظم وproof pack لكل عميل."],
  ["Marketing Manager", "تحويل leads إلى pipeline بدل أرقام حملات فقط."],
];

export default function CompanyBrainOSPage() {
  return (
    <main className="grid">
      <section className="card dot-pattern" style={{ paddingTop: "clamp(44px,7vw,86px)", paddingBottom: "clamp(44px,7vw,86px)" }}>
        <p className="eyebrow">Company Brain + Revenue OS</p>
        <h1>نظام تشغيل كامل للشركة: قرار، إيراد، متابعة، تسليم، وإثبات.</h1>
        <p style={{ maxWidth: 780, fontSize: "1.12rem" }}>
          نبني طبقة تشغيلية فوق واقع الشركة الحالي: نفهم الألم، نحوله إلى workflows،
          نجهز غرفة قيادة يومية، ونربط كل فرصة أو عميل بowner وnext action وproof.
        </p>
        <div className="actions">
          <Link href="/book">احجز مراجعة تشغيلية</Link>
          <Link href="/pricing">شاهد الباقات</Link>
        </div>
      </section>

      <section className="cards">
        {modules.map(([title, text]) => (
          <article className="card" key={title}>
            <span className="badge badge-cyan">Module</span>
            <h2 style={{ fontSize: "1.35rem", marginTop: "var(--sp-4)" }}>{title}</h2>
            <p>{text}</p>
          </article>
        ))}
      </section>

      <section className="card">
        <p className="eyebrow">Buyer-specific value</p>
        <h2>كل شخص داخل الشركة يرى Dealix من زاوية مختلفة.</h2>
        <div className="grid-2">
          {buyerAngles.map(([buyer, angle]) => (
            <article key={buyer} style={{ padding: "var(--sp-4)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "var(--r-lg)" }}>
              <h3>{buyer}</h3>
              <p>{angle}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-cyan" style={{ textAlign: "center" }}>
        <p className="eyebrow">Start with proof</p>
        <h2>ابدأ بـ7 أيام على ألم واحد، ثم وسّع بعد الإثبات.</h2>
        <p>أفضل مدخل تجاري: تشخيص، خريطة ألم، أول dashboard، queue مراجعة، وخطة 30 يوم.</p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">ابدأ الآن</Link>
        </div>
      </section>
    </main>
  );
}
