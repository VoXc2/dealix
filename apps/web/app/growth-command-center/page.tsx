import Link from "next/link";

const services = [
  ["Revenue Command Room OS", "يرتب الفرص والمتابعات والعروض والقرارات اليومية."],
  ["Company Brain OS", "قرار CEO يومي، bottlenecks، future radar، وboard memo."],
  ["AI Sales Agent OS", "مسودات مبيعات، اعتراضات، أسئلة discovery، وحدود تفاوض."],
  ["Offer Intelligence OS", "يحسن العرض، التسعير، الرسائل، والproposal structure."],
  ["Customer Pain Radar", "يحول الأسئلة والشكاوى إلى قرارات وتحسينات."],
  ["Client Delivery OS", "يثبت التسليم عبر acceptance criteria وproof packs."],
  ["AI Trust and Governance OS", "يضبط استخدام AI بالسياسات والمراجعة والسجلات."],
];

const daily = [
  ["100", "Research accounts"],
  ["40", "Verified accounts"],
  ["25", "Drafts generated"],
  ["10-15", "Founder-approved contacts"],
  ["3-5", "Call attempts"],
  ["1-2", "Discovery calls"],
  ["1", "Proposal or diagnostic offer"],
];

const guardrails = [
  "No live outbound by default",
  "No fake ROI or fake case studies",
  "No named executive identity without explicit approval",
  "WhatsApp production requires opt-in and approved templates",
  "Every target needs source_url and verification_status",
  "Founder approval before sensitive commercial action",
];

export const metadata = {
  title: "Growth Command Center — Dealix",
  description: "Dealix founder-led commercial command center for Saudi B2B AI Operating Systems.",
};

export default function GrowthCommandCenterPage() {
  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Growth Command Center</p>
        <h1>غرفة قيادة تجارية تجمع Company Brain + Sales Agent + Revenue OS</h1>
        <p style={{ maxWidth: 860, margin: "0 auto" }}>
          هذه الصفحة تجمع أقوى خدمات Dealix في نظام تشغيل واحد: نعرف ألم الشركة، نختار العرض المناسب،
          نولد مسودات مقنعة، نجهز التفاوض، ونقيس الحركة اليومية بدون إرسال خارجي غير محكوم.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/sales-agent-lab">جرّب Sales Agent Lab</Link>
          <Link href="/hubspot-os">HubSpot OS</Link>
          <Link href="/command-center">Command Center</Link>
        </div>
      </section>

      <section className="grid-3">
        <article className="card"><div className="stat-value">7</div><p className="stat-label">core operating systems</p></article>
        <article className="card"><div className="stat-value">2</div><p className="stat-label">daily qualified call target</p></article>
        <article className="card"><div className="stat-value">8</div><p className="stat-label">weekly qualified call target</p></article>
      </section>

      <section className="card" dir="rtl">
        <p className="eyebrow">Service stack</p>
        <h2>أقوى خدمات Dealix التي تقنع الشركات حسب الألم</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {services.map(([title, description]) => (
            <article className="card hover-cyan" key={title}>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card" dir="rtl">
        <p className="eyebrow">Daily growth rhythm</p>
        <h2>الاستهداف اليومي عالي السرعة بدون spam</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {daily.map(([value, label]) => (
            <article className="card" key={label}>
              <div className="stat-value">{value}</div>
              <p className="stat-label">{label}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-cyan" dir="rtl">
          <p className="eyebrow">Sales Agent</p>
          <h2>يتكلم بصوت الشركة — لكن بتصريح واضح</h2>
          <p>
            الوكيل يولد الرسائل والاعتراضات والتفاوض بصوت الشركة أو ممثل المبيعات المصرح.
            استخدام اسم مدير محدد يتطلب موافقة صريحة، ولا يتم إرسال خارجي من هذه الطبقة.
          </p>
        </article>
        <article className="card" dir="rtl">
          <p className="eyebrow">Guardrails</p>
          <h2>قواعد تمنع حرق السمعة</h2>
          <ul>{guardrails.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Run locally</p>
        <h2>ولّد تقرير Growth Command Center</h2>
        <pre style={{ textAlign: "left" }}>python scripts/commercial/generate_growth_command_center.py</pre>
      </section>
    </main>
  );
}
