import Link from "next/link";
import { serviceOsSnapshot } from "../../lib/service-os-snapshot";

const statusRows = [
  ["RCMax", serviceOsSnapshot.summary.rcmax_ready],
  ["Auto14", serviceOsSnapshot.summary.auto14_ready],
  ["Client Ops", serviceOsSnapshot.summary.client_ops_ready],
  ["Conversation Intelligence", serviceOsSnapshot.summary.conversation_ready],
  ["Deal Strategy", serviceOsSnapshot.summary.strategy_ready],
  ["Service OS", serviceOsSnapshot.summary.service_os_ready],
];

export default function ServiceOsPage() {
  return (
    <main className="grid">
      <section className="card dot-pattern animate-fade-up" style={{ paddingTop: "clamp(40px,6vw,76px)", paddingBottom: "clamp(40px,6vw,76px)" }}>
        <p className="eyebrow">Commercial Launch · Client Delivery · Approval-first AI</p>
        <h1 style={{ maxWidth: 980 }}>
          Dealix Service OS: واجهة تشغيل تجاري وخدمة عميل جاهزة للانطلاق.
        </h1>
        <p style={{ maxWidth: 780, fontSize: "1.08rem", lineHeight: 1.85 }}>
          نظام واحد يربط البيع، فهم المحادثة، استراتيجية الصفقة، تشغيل العميل، proof report، والمراجعة قبل أي إجراء خارجي حساس.
        </p>
        <div className="actions" aria-label="Service OS actions">
          <Link href="/book">ابدأ التشخيص التنفيذي المجاني</Link>
          <Link href="/services">استعرض الخدمات</Link>
          <Link href="/safety">مراجعة الأمان</Link>
        </div>
      </section>

      <section className="grid-3" aria-label="Service OS readiness">
        {statusRows.map(([name, ready]) => (
          <article className="card" key={String(name)}>
            <span className="badge badge-cyan">{ready ? "READY" : "CHECK"}</span>
            <h2>{name}</h2>
            <p>{ready ? "جاهز ضمن حزمة Service OS." : "يحتاج فحص قبل الإطلاق."}</p>
          </article>
        ))}
      </section>

      <section className="grid-2" aria-label="Client value and safety">
        <article className="card">
          <p className="eyebrow">What the client gets</p>
          <h2>مخرجات خدمة واضحة</h2>
          <ul>
            {serviceOsSnapshot.clientGets.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </article>
        <article className="card">
          <p className="eyebrow">Approval gates</p>
          <h2>الأشياء التي لا تعمل بدون موافقة</h2>
          <ul>
            {serviceOsSnapshot.approvalGates.map((item) => <li key={item}>{item}</li>)}
          </ul>
          <p>Live sends: {serviceOsSnapshot.summary.live_sends} · Final commitments: {serviceOsSnapshot.summary.final_commitments}</p>
        </article>
      </section>

      <section className="card" aria-label="Commercial offers">
        <p className="eyebrow">Commercial offers</p>
        <h2>مسارات قابلة للتخصيص بعد التشخيص</h2>
        <div className="grid-3">
          {serviceOsSnapshot.offers.map((offer) => (
            <article className="card" key={offer.name}>
              <span className="badge">Qualified discovery first</span>
              <h3>{offer.name}</h3>
              <p>{offer.outcome}</p>
              <strong>{offer.commercialAuthority}</strong>
              <p>{offer.scopeAuthority}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card" aria-label="Operating flow">
        <p className="eyebrow">Operating flow</p>
        <h2>من الاستقبال إلى التجديد</h2>
        <ol>
          {serviceOsSnapshot.operatingFlow.map((item) => <li key={item}>{item}</li>)}
        </ol>
      </section>
    </main>
  );
}
