import type { Metadata } from "next";
import Link from "next/link";
import PageShell from "@/components/PageShell";
import { capabilityById, sectorCatalog } from "@/lib/public-catalog";

export const metadata: Metadata = {
  title: "القطاعات — Dealix",
  description: "حلول Dealix المخصصة لقطاعات السعودية: الحكومة، البناء، الصناعة، اللوجستيات، الطاقة، التعدين، العقار، الصحة، المالية، التجزئة، السياحة، التقنية وغيرها.",
};

export default function SectorsPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ textAlign: "center", paddingBlock: "clamp(42px,7vw,78px)" }}>
        <p className="eyebrow">Saudi Sector Companies</p>
        <h1>قدرات Dealix تتكيّف مع اقتصاد كل قطاع، buyer والـworkflow الحقيقي.</h1>
        <p style={{ maxWidth: 920, margin: "0 auto", fontSize: "1.08rem" }}>
          نغطي القطاعات الحالية في Company Machine بملفات تشغيلية مختلفة بدل نسخ نفس عرض AI على الجميع. كل ملف يربط مشاكل محتملة بقدرات مناسبة، لكن المشكلة لا تصبح حقيقة عميل إلا بعد Diagnostic وDiscovery.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <Link href="/book">ابدأ تشخيص قطاعك</Link>
          <Link href="/services">كل القدرات</Link>
        </div>
      </section>

      <section>
        <p className="eyebrow">Current Sector Coverage</p>
        <h2>اختر القطاع لعرض أقرب capability mix.</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {sectorCatalog.map((sector) => (
            <article className="card" key={sector.key}>
              <span className="badge badge-cyan">{sector.nameEn}</span>
              <h3 style={{ marginTop: 14 }}>{sector.nameAr}</h3>
              <p>{sector.focus}</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 7, marginTop: 14 }}>
                {sector.capabilityIds.slice(0, 4).map((id) => <span className="badge badge-gold" key={id}>{capabilityById[id].nameAr}</span>)}
              </div>
              <div className="actions" style={{ marginTop: 20 }}>
                <Link href={`/sectors/${sector.slug}`}>عرض ملف القطاع</Link>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="card card-gold">
        <p className="eyebrow">Truth Boundary</p>
        <h2>Sector intelligence ليست claim عن شركتك.</h2>
        <p>
          المشاكل والأمثلة في هذه الصفحات هي hypotheses تشغيلية تساعد على بدء الحوار. لا تعني وجود defect أو relationship أو consent أو eligibility أو compliance status لجهة محددة.
        </p>
      </section>
    </PageShell>
  );
}
