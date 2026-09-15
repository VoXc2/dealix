import { TrackedLink } from "@/components/analytics/TrackedLink";

const layers = [
  { title: "Company Brain", text: "يربط القرارات والمعرفة والسياق التشغيلي بدل بقائها موزعة بين أدوات وأشخاص." },
  { title: "Opportunity Graph", text: "يحوّل signals إلى opportunities مصنفة بالأدلة والمرحلة والـnext action." },
  { title: "Action + Approval", text: "يفصل ما يمكن تنفيذه ذاتيًا عما يحتاج authority مادية محددة." },
  { title: "Proof Ledger", text: "يوثق baseline والتنفيذ والنتيجة وما يصلح أن يصبح Customer Proof." },
];

export default function DealixOSPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">Flagship Product</p>
        <h1>Dealix OS — AI Business Operating System</h1>
        <p style={{ maxWidth: 800, margin: "0 auto" }}>
          طبقة تشغيل فوق CRM وERP والبريد وWhatsApp وSlack والملفات والأنظمة الحالية. تجمع Signal → Decision → Action → Proof في مسار محكوم وقابل للمراجعة.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="dealix_os_execution_diagnostic" surface="dealix_os_hero">ابدأ بمشكلة تشغيل واحدة</TrackedLink>
          <TrackedLink href="/cases" ctaId="dealix_os_to_proof" surface="dealix_os_hero">شاهد منهج الإثبات</TrackedLink>
        </div>
      </section>

      <section className="cards">
        {layers.map((layer) => (
          <article className="card" key={layer.title}>
            <h2 style={{ fontSize: "1.4rem" }}>{layer.title}</h2>
            <p>{layer.text}</p>
          </article>
        ))}
      </section>

      <section className="card">
        <p className="eyebrow">Where it fits</p>
        <h2>Dealix OS ليس شرط البداية لكل عميل.</h2>
        <p>
          نبدأ بالتشخيص والتنفيذ customer-specific. عندما نثبت أن المشكلة متكررة وتحتاج monitoring، orchestration، approvals وproof مستمر، يتحول Dealix OS إلى طبقة التشغيل المناسبة.
        </p>
      </section>
    </main>
  );
}
