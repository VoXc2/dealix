export const metadata = {
  title: "Data Room — Dealix",
  description: "Investor and partner data room: overview, thesis, architecture, commercial model.",
};

const SECTIONS = [
  { href: "business/data-room/COMPANY_OVERVIEW.md", title: "Company Overview", desc: "One paragraph on what Dealix does" },
  { href: "business/data-room/MARKET_THESIS.md", title: "Market Thesis", desc: "Why now, why Saudi, why Dealix" },
  { href: "business/data-room/PRODUCT_ARCHITECTURE.md", title: "Product Architecture", desc: "Layers, components, integrations" },
  { href: "business/data-room/COMMERCIAL_MODEL.md", title: "Commercial Model", desc: "Seven offers + unit economics" },
  { href: "business/data-room/TRACTION_TEMPLATE.md", title: "Traction Template", desc: "Honest reporting format" },
  { href: "business/data-room/PARTNER_PROGRAM.md", title: "Partner Program", desc: "Four partner types" },
  { href: "business/data-room/STRATEGIC_PARTNERSHIP_TERMS.md", title: "Strategic Terms", desc: "V1 partnership terms" },
];

export default function DataRoomPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-5xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Data Room</p>
          <h1 className="mt-3 text-4xl font-semibold">غرفة بيانات — للمستثمرين والشركاء</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            سبع مستندات. كل الأرقام placeholders حتى تُستبدل بأرقام حقيقية. كل حساب demo لازم
            يكون موسوم.
          </p>
        </header>

        <section className="mt-10 grid gap-3 md:grid-cols-2">
          {SECTIONS.map((s) => (
            <a
              key={s.href}
              href={`https://github.com/Dealix-sa/dealix/blob/main/${s.href}`}
              target="_blank"
              rel="noreferrer"
              className="rounded-2xl border border-white/10 bg-white/5 p-5 transition hover:border-amber-300/30"
            >
              <p className="font-medium">{s.title}</p>
              <p className="text-xs text-white/60">{s.desc}</p>
              <p className="mt-2 text-[10px] text-white/40">{s.href}</p>
            </a>
          ))}
        </section>

        <section className="mt-10 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">ملاحظة مهمة</p>
          <p className="mt-2">
            الأرقام الحالية placeholders. لا نُفبرك traction. كل demo record يحمل demo=true. أول
            رقم حقيقي يضاف، ينضاف بعد إغلاق أول عقد موقّع.
          </p>
        </section>
      </div>
    </main>
  );
}
