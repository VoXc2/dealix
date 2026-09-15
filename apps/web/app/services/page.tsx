import type { Metadata } from "next";
import Link from "next/link";
import PageShell from "@/components/PageShell";
import { capabilityCatalog } from "@/lib/public-catalog";

export const metadata: Metadata = {
  alternates: { canonical: "/services" },
  title: "الخدمات والحلول — Dealix",
  description: "خدمات Dealix للشركات السعودية: استراتيجية وتحول، AI agents، أتمتة، إيراد، عملاء، بيانات، معرفة، تكاملات، حوكمة، جاهزية أمنية، Fatoora، سوق وشركاء وDealix OS.",
};

const engagement = [
  ["01", "Free Execution Diagnostic", "نحدد workflow أو قرارًا واحدًا، baseline، owner، الأدلة والفجوات. لا بطاقة ولا التزام شراء."],
  ["02", "Qualified Discovery", "نثبت المشكلة والبيانات والمخاطر ومعايير القبول قبل أي quote أو scope."],
  ["03", "Customer-Specific Outcome Sprint", "نبني أو نكيّف أو ندمج الحل الأنسب. السعر والمدة والنطاق تخص العميل بعد Discovery فقط."],
  ["04", "Proof Review", "نقارن النتيجة بالـbaseline ونوثق ما ثبت وما بقي غير مثبت."],
  ["05", "Runtime / Managed Operation", "إذا ثبت التكرار والقيمة، ننتقل إلى تشغيل مستمر عبر Dealix OS أو managed operation مناسب."],
] as const;

export default function ServicesPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ textAlign: "center", paddingBlock: "clamp(42px,7vw,78px)" }}>
        <p className="eyebrow">Dealix Capability System</p>
        <h1>خدمات قوية تُركّب حول المشكلة والقطاع — لا حول باقة ثابتة.</h1>
        <p style={{ maxWidth: 900, margin: "0 auto", fontSize: "1.08rem" }}>
          Dealix تجمع strategy، AI systems، commercial operations، data، knowledge، governance، market intelligence وproductization في شركة واحدة.
          نختار أقل مجموعة قدرات كافية لتحريك نتيجة قابلة للقياس، ثم نوسع فقط إذا أثبتت القيمة.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">ابدأ Free Execution Diagnostic</Link>
          <Link href="/saudi-opportunity-radar" data-cta-id="services_saudi_opportunity_radar">شاهد Saudi Opportunity Radar</Link>
          <Link href="/sectors">اختر قطاعك</Link>
        </div>
      </section>

      <section>
        <p className="eyebrow">Full Capability Catalog</p>
        <h2>من القرار الاستراتيجي إلى التشغيل والـproof.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {capabilityCatalog.map((item, index) => (
            <article className="card" key={item.id} id={item.id}>
              <span className="badge badge-cyan">{String(index + 1).padStart(2, "0")} · {item.nameEn}</span>
              <h3 style={{ marginTop: "var(--sp-4)" }}>{item.nameAr}</h3>
              <p>{item.summary}</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 16 }}>
                {item.outcomes.map((outcome) => <span className="badge badge-cyan" key={outcome}>{outcome}</span>)}
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-cyan">
        <p className="eyebrow">Sector Fit</p>
        <h2>نفس القدرة لا تُطبّق بالطريقة نفسها في كل قطاع.</h2>
        <p>
          في البناء قد تبدأ المشكلة من RFQ والوثائق والموردين، وفي التجزئة من conversion وخدمة العملاء، وفي المالية من evidence والعمليات المنظمة.
          لذلك ربطنا القدرات بملفات قطاعية واضحة بدل صفحة خدمات عامة فقط.
        </p>
        <div className="actions">
          <Link href="/sectors">استكشف القطاعات</Link>
          <Link href="/products">استكشف المنتجات والـruntime</Link>
        </div>
      </section>

      <section>
        <p className="eyebrow">Engagement Path</p>
        <h2>مسار تجاري واحد، مع نطاق خاص بكل عميل.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {engagement.map(([step, title, text]) => (
            <article className="card" key={step}>
              <span className="badge badge-ocean">{step}</span>
              <h3 style={{ marginTop: 14 }}>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Start Small, Prove Fast</p>
        <h2>أفضل نقطة بداية ليست “أي خدمة تريد؟” بل “أي مشكلة تستحق أن نثبتها؟”</h2>
        <p style={{ maxWidth: 760, margin: "0 auto" }}>
          التشخيص الأولي مجاني وcard-free. إذا لم نجد حالة تنفيذ مناسبة نتوقف؛ وإذا وجدت، نبني عرضًا customer-specific بمعايير قبول واضحة.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}><Link href="/book">ابدأ التشخيص المجاني</Link></div>
      </section>
    </PageShell>
  );
}
