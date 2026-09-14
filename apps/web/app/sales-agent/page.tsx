import Link from "next/link";

const capabilities = [
  "يعرف عروض الشركة وحدودها",
  "يحلل pain hypothesis حسب القطاع",
  "يكتب رسائل أولى ومتابعات كمسودات",
  "يرد على الاعتراضات بأسلوب الشركة",
  "يساعد في التفاوض بدون تخفيض عشوائي",
  "يلخص المكالمات ويقترح next action",
];

const guardrails = [
  "هوية المرسل واضحة ومصرح بها",
  "لا يستخدم اسم مدير حقيقي بدون موافقة صريحة",
  "كل تواصل خارجي يبدأ draft في baseline",
  "واتساب يتطلب opt-in وقالب معتمد عند التشغيل الحي",
  "لا وعود دخل مضمونة ولا proof وهمي",
  "كل رد حساس يحتاج موافقة بشرية",
];

export default function SalesAgentPage() {
  return (
    <main>
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">AI Sales Agent OS</p>
        <h1>Sales Agent يتكلم بصوت شركتك — لكن بأمان ووضوح</h1>
        <p style={{ maxWidth: 780, margin: "0 auto" }}>
          نبني وكيل مبيعات يساعد فريقك في التأهيل، الردود، المتابعة، والتفاوض. يعمل بصوت الشركة،
          ويجهز drafts وnext actions، مع approval gates قبل أي التزام أو تواصل حساس.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/sales-agent-lab">جرّب Sales Agent Lab</Link>
          <Link href="/book">ابنِ Sales Agent</Link>
          <Link href="/safety">راجع قواعد الأمان</Link>
        </div>
      </section>

      <section className="grid-2">
        <article className="card">
          <p className="eyebrow">Capabilities</p>
          <h2>ماذا يفعل؟</h2>
          <ul>
            {capabilities.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </article>
        <article className="card card-cyan">
          <p className="eyebrow">Guardrails</p>
          <h2>ما الحدود؟</h2>
          <ul>
            {guardrails.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </article>
      </section>

      <section className="grid-2">
        <article className="card">
          <p className="eyebrow">API surface</p>
          <h2>جاهز للتكامل الداخلي</h2>
          <p>
            تم تجهيز API داخلي يولد مسودة حسب الشركة والقطاع بدون إرسال خارجي:
          </p>
          <pre>POST /api/sales-agent/draft</pre>
        </article>
        <article className="card">
          <p className="eyebrow">Best use</p>
          <h2>أفضل استخدام تجاري</h2>
          <p>
            ابدأه كـSales Copilot داخلي: يولد المسودات، يجهز الاعتراضات، يقترح التفاوض، ويكتب proposal brief.
            بعد إثبات الجودة وضبط الهوية والقنوات، يمكن الانتقال إلى controlled live mode في PR مستقل.
          </p>
        </article>
      </section>
    </main>
  );
}
