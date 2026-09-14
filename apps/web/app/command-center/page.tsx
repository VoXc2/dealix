import Link from "next/link";

export const metadata = {
  title: "Strategic Command Center — Dealix",
  description:
    "A full strategic command room for Dealix: revenue, targeting, sales agents, company brain, delivery, and safety gates.",
};

const lanes = [
  {
    title: "Revenue War Room",
    status: "Active",
    question: "What revenue action must move today?",
    metrics: ["Hot accounts", "Open proposals", "Overdue follow-ups", "Negotiation risks"],
    action: "Prepare one scoped proposal and push three qualified follow-ups.",
  },
  {
    title: "Targeting Engine",
    status: "Active",
    question: "Which sector wedge gives the best chance today?",
    metrics: ["100 researched", "40 verified", "25 drafts", "10-15 manual contacts"],
    action: "Pick one sector and generate company-specific sales packs.",
  },
  {
    title: "AI Sales Agent OS",
    status: "Guarded",
    question: "What should the authorized sales assistant say next?",
    metrics: ["Voice mode", "Objections", "Negotiation levers", "Approval queue"],
    action: "Generate drafts and negotiation guidance, then require founder approval.",
  },
  {
    title: "Company Brain",
    status: "Active",
    question: "What does the CEO need to decide today?",
    metrics: ["CEO decision", "Future radar", "Risks", "Knowledge gaps"],
    action: "Turn scattered context into one daily decision and weekly board memo.",
  },
  {
    title: "Client Delivery OS",
    status: "Ready",
    question: "What proof must be delivered for clients?",
    metrics: ["Scope cards", "Acceptance criteria", "Proof pack", "Renewal chances"],
    action: "Update proof pack and identify one renewal opportunity.",
  },
  {
    title: "Safety & Trust Gates",
    status: "Locked",
    question: "What must remain blocked until approved?",
    metrics: ["draft_only", "Opt-out", "Identity clarity", "No fake claims"],
    action: "Keep external sends blocked until DNS, consent, rate limits, and audit are ready.",
  },
];

const dailyNumbers = [
  ["Research companies", "100"],
  ["Verify targets", "40"],
  ["Draft messages", "25"],
  ["Manual contacts", "10-15"],
  ["Call attempts", "3-5"],
  ["Discovery calls", "1-2"],
  ["Proposals", "1"],
];

const services = [
  "Revenue Command Room OS",
  "Company Brain OS",
  "AI Sales Agent OS",
  "Follow-up Recovery OS",
  "AI Trust & Governance OS",
  "Client Delivery OS",
];

function statusClass(status: string) {
  if (status === "Active") return "badge badge-emerald";
  if (status === "Guarded") return "badge badge-amber";
  if (status === "Locked") return "badge badge-coral";
  return "badge badge-cyan";
}

export default function CommandCenterPage() {
  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Strategic Command Center</p>
        <h1>غرفة قيادة Dealix الاستراتيجية</h1>
        <p style={{ maxWidth: 820, margin: "0 auto" }}>
          شاشة واحدة تجمع الإيراد، الاستهداف، Sales Agent، Company Brain، تسليم العملاء، والحوكمة.
          الهدف ليس عرض أرقام فقط؛ الهدف تحديد ما الذي يجب فعله اليوم لإغلاق فرص حقيقية بأمان.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">احجز مراجعة تشغيلية</Link>
          <Link href="/services">افتح الخدمات</Link>
          <Link href="/sales-agent">Sales Agent OS</Link>
        </div>
      </section>

      <section className="grid-3" aria-label="Daily operating targets">
        {dailyNumbers.map(([label, value]) => (
          <article className="card" key={label} style={{ textAlign: "center" }}>
            <div className="stat-value">{value}</div>
            <p className="stat-label">{label}</p>
          </article>
        ))}
      </section>

      <section aria-labelledby="lanes-title">
        <p className="eyebrow">Operating lanes</p>
        <h2 id="lanes-title">كل مسار له سؤال استراتيجي وفعل يومي واضح.</h2>
        <div className="cards">
          {lanes.map((lane) => (
            <article className="card" key={lane.title}>
              <span className={statusClass(lane.status)}>{lane.status}</span>
              <h3 style={{ marginTop: "var(--sp-4)" }}>{lane.title}</h3>
              <p><strong>Question:</strong> {lane.question}</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--sp-2)", marginBottom: "var(--sp-4)" }}>
                {lane.metrics.map((metric) => (
                  <span className="badge badge-cyan" key={metric}>{metric}</span>
                ))}
              </div>
              <p><strong>Today:</strong> {lane.action}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-cyan">
          <p className="eyebrow">Founder decision</p>
          <h2>قرار اليوم</h2>
          <p>
            اختر قطاعًا واحدًا، ولّد 10 sales packs مخصصة، راجع أفضل 3، ثم ابدأ بمراجعة تشغيلية بدل بيع نظام كامل من أول رسالة.
          </p>
        </article>
        <article className="card">
          <p className="eyebrow">Service stack</p>
          <h2>الخدمات التي تُباع من الغرفة</h2>
          <ul>
            {services.map((service) => <li key={service}>{service}</li>)}
          </ul>
        </article>
      </section>

      <section className="card" aria-labelledby="safety-title">
        <p className="eyebrow">Controlled intelligence</p>
        <h2 id="safety-title">ذكاء تجاري قوي بدون حرق السمعة أو انتحال الهوية.</h2>
        <p>
          Sales Agent يعمل كـauthorized assistant: يكتب، يؤهل، يفاوض ضمن حدود، ويقترح next action.
          أي تواصل خارجي حي يحتاج هوية واضحة، موافقة، opt-out، وسجل تدقيق. baseline يبقى draft_only.
        </p>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Run locally</p>
        <h2>شغّل غرفة القيادة من الريبو</h2>
        <pre style={{ textAlign: "left" }}>make -f Makefile.launch day</pre>
        <p>ثم راجع reports/command_center/latest.md وباقي تقارير commercial قبل أي إجراء خارجي.</p>
      </section>
    </main>
  );
}
