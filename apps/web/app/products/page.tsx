import type { Metadata } from "next";
import Link from "next/link";
import PageShell from "@/components/PageShell";

export const metadata: Metadata = {
  alternates: { canonical: "/products" },
  title: "المنتجات والـRuntime — Dealix",
  description: "Dealix OS ومنتجات تشغيلية قابلة للتركيب حول Company Brain والإيراد والتسليم والحوكمة والذكاء والتكاملات، بنطاق خاص بكل عميل.",
};

const products = [
  { id: "dealix-os", nameAr: "Dealix OS", nameEn: "AI Business Operating System", text: "المنتج الرئيسي: Company Brain + Opportunity Graph + Action/Approval + Proof Ledger في مسار Signal → Decision → Action → Proof.", href: "/dealix-os" },
  { id: "company-brain", nameAr: "Company Brain", nameEn: "Knowledge & Decision Memory", text: "سياق واحد للقرارات والسياسات والمعرفة والحقائق الحالية، مع فصل التاريخ عن CURRENT_ONLY authority.", href: "/dealix-os" },
  { id: "revenue-command", nameAr: "Revenue Command", nameEn: "Commercial Operations Module", text: "أولويات ومتابعات وعروض وdecision briefs مرتبطة بأدلة وnext actions بدل dashboard نشاط فقط.", href: "/services#revenue" },
  { id: "client-delivery", nameAr: "Client Delivery & Proof", nameEn: "Delivery Operations Module", text: "مراحل تسليم، acceptance، approvals وproof packs تساعد على فصل delivery عن customer-validated outcome.", href: "/services#productization" },
  { id: "trust", nameAr: "AI Trust Controls", nameEn: "Governance & Reliability Module", text: "صلاحيات، approval boundaries، evaluations، traceability وreceipts لتشغيل agents وtools ضمن حدود واضحة.", href: "/services#trust" },
  { id: "knowledge", nameAr: "Document & Knowledge Intelligence", nameEn: "Knowledge Operations Module", text: "بحث واستخراج وربط للوثائق والمعرفة التشغيلية مع provenance واستخدامها في decision workflows.", href: "/services#knowledge" },
  { id: "market", nameAr: "Saudi Opportunity Intelligence", nameEn: "Market & Partner Intelligence Module", text: "Market signals وsector intelligence وpartner/procurement research مع Truth Firewall يمنع تحويل البحث إلى relationship أو pipeline تلقائيًا.", href: "/services#market" },
  { id: "integration", nameAr: "Integration & MCP Fabric", nameEn: "Connector Runtime Module", text: "تكامل APIs وMCP والأدوات الحالية مع reliability checks، permissions ومسار rollback واضح.", href: "/services#integration" },
];

export default function ProductsPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ textAlign: "center", paddingBlock: "clamp(42px,7vw,78px)" }}>
        <p className="eyebrow">Products & Runtime</p>
        <h1>منتج رئيسي، ووحدات تشغيل تتوسع فقط عندما يثبت الاستخدام.</h1>
        <p style={{ maxWidth: 880, margin: "0 auto", fontSize: "1.08rem" }}>
          Dealix OS هو المنتج الرئيسي. الوحدات أدناه capabilities قابلة للتركيب وليست باقات عامة أو التزامًا بأن كل عميل يحتاجها. النطاق والمدة والسعر تُحدد بعد Qualified Discovery لحالة العميل.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/dealix-os">استكشف Dealix OS</Link>
          <Link href="/book">ابدأ التشخيص المجاني</Link>
        </div>
      </section>

      <section>
        <p className="eyebrow">Composable Product Layer</p>
        <h2>نحوّل ما يثبت إلى IP وruntime قابل لإعادة الاستخدام.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {products.map((product) => (
            <article className="card" id={product.id} key={product.id}>
              <span className="badge badge-cyan">{product.nameEn}</span>
              <h3 style={{ marginTop: 14 }}>{product.nameAr}</h3>
              <p>{product.text}</p>
              <Link href={product.href}>اعرف أكثر ↗</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-cyan">
        <p className="eyebrow">Build → Prove → Productize</p>
        <h2>لا نبدأ بفرض SaaS على كل مشكلة.</h2>
        <p>
          قد يكون الحل الأنسب workflow بسيطًا أو integration أو managed operation. عندما يثبت التكرار والقيمة، نرفع الجزء المتكرر إلى Dealix OS أو module قابل للتوسع. هذا يقلل build waste ويحافظ على economics واضحة.
        </p>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Customer-Specific Scope</p>
        <h2>لا fixed public price، ولا fixed delivery window.</h2>
        <p style={{ maxWidth: 760, margin: "0 auto" }}>
          نحدد ما يلزم فقط بعد Diagnostic وDiscovery. أي quote أو acceptance criteria أو rollout plan يخص العميل والنطاق المتفق عليه.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}><Link href="/pricing">شاهد Engagement Path</Link></div>
      </section>
    </PageShell>
  );
}
