import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import PageShell from "@/components/PageShell";
import { capabilityById, sectorBySlug, sectorCatalog } from "@/lib/public-catalog";

export function generateStaticParams() {
  return sectorCatalog.map((sector) => ({ slug: sector.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const sector = sectorBySlug[slug];
  if (!sector) return {};
  return {
    title: `${sector.nameAr} — حلول Dealix`,
    description: `حلول Dealix لقطاع ${sector.nameAr}: ${sector.focus}`,
  };
}

export default async function SectorDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const sector = sectorBySlug[slug];
  if (!sector) notFound();

  const capabilities = sector.capabilityIds.map((id) => capabilityById[id]).filter(Boolean);

  return (
    <PageShell>
      <section className="card dot-pattern" style={{ textAlign: "center", paddingBlock: "clamp(42px,7vw,78px)" }}>
        <p className="eyebrow">Sector Playbook · {sector.nameEn}</p>
        <h1>{sector.nameAr}</h1>
        <p style={{ maxWidth: 860, margin: "0 auto", fontSize: "1.08rem" }}>{sector.focus}</p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">ابدأ Free Execution Diagnostic</Link>
          <Link href="/sectors">كل القطاعات</Link>
        </div>
      </section>

      <section className="cards">
        <article className="card">
          <p className="eyebrow">Problem Hypotheses</p>
          <h2 style={{ fontSize: "1.45rem" }}>أين نبدأ الفحص؟</h2>
          <ul>{sector.problems.map((problem) => <li key={problem}>{problem}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Possible Outcomes</p>
          <h2 style={{ fontSize: "1.45rem" }}>أمثلة لما يمكن تحسينه</h2>
          <ul>{sector.examples.map((example) => <li key={example}>{example}</li>)}</ul>
        </article>
      </section>

      <section>
        <p className="eyebrow">Recommended Capability Mix</p>
        <h2>نركب الحل حول الـworkflow، لا حول اسم منتج ثابت.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {capabilities.map((capability) => (
            <article className="card" key={capability.id}>
              <span className="badge badge-cyan">{capability.nameEn}</span>
              <h3 style={{ marginTop: 14 }}>{capability.nameAr}</h3>
              <p>{capability.summary}</p>
              <Link href={`/services#${capability.id}`}>تفاصيل القدرة ↗</Link>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-gold">
        <p className="eyebrow">Evidence First</p>
        <h2>هذه الصفحة ليست تشخيصًا مسبقًا لشركتك.</h2>
        <p>
          نستخدم ملف القطاع لتسريع discovery فقط. لا نفترض أن شركتك تعاني من هذه المشاكل، ولا أن جهة عامة أو تنظيمًا معينًا ينطبق عليك، ولا أن أي نتيجة مضمونة قبل baseline وبيانات وأدلة تخص حالتك.
        </p>
        <div className="actions"><Link href="/book">حوّل الفرضية إلى تشخيص مجاني</Link></div>
      </section>
    </PageShell>
  );
}
